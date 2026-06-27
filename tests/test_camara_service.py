"""
Testes unitários para camara_service.py (sem BD real — dependências mockadas).
Execução: python -m pytest tests/ ou python -m unittest tests.test_camara_service
"""
import os
import unittest
from datetime import date
from unittest.mock import MagicMock, patch

os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost/test")
os.environ.setdefault("FLASK_ENV", "testing")


class TestValidarProposicao(unittest.TestCase):
    def setUp(self):
        from src.backend.services.camara_service import _validar_proposicao
        self._fn = _validar_proposicao

    def _dado_valido(self, **override):
        base = {
            "id": 1,
            "siglaTipo": "PL",
            "numero": 100,
            "ano": 2025,
            "ementa": "Proteção de dados de crianças na internet",
            "dataApresentacao": "2025-01-15",
            "descricaoSituacao": "Em tramitação",
            "siglaPartido": "PT",
        }
        base.update(override)
        return base

    def test_dado_valido_retorna_dto(self):
        dto = self._fn(self._dado_valido())
        self.assertIsNotNone(dto)
        self.assertEqual(dto["id"], 1)
        self.assertEqual(dto["sigla_tipo"], "PL")
        self.assertIsInstance(dto["data_apresentacao"], date)
        self.assertEqual(dto["classificacao_status"], "pendente_classificacao")

    def test_campo_obrigatorio_ausente_retorna_none(self):
        dado = self._dado_valido()
        dado.pop("ementa")
        with self.assertLogs("src.backend.services.camara_service", level="WARNING") as cm:
            resultado = self._fn(dado)
        self.assertIsNone(resultado)
        self.assertTrue(any("campo obrigatório ausente" in msg for msg in cm.output))

    def test_ementa_vazia_retorna_none(self):
        dto = self._fn(self._dado_valido(ementa="   "))
        self.assertIsNone(dto)

    def test_data_invalida_retorna_none(self):
        dto = self._fn(self._dado_valido(dataApresentacao="nao-e-data"))
        self.assertIsNone(dto)

    def test_status_invalido_normaliza_para_em_tramitacao(self):
        dto = self._fn(self._dado_valido(descricaoSituacao="Status Desconhecido"))
        self.assertEqual(dto["descricao_situacao"], "Em tramitação")

    def test_data_com_hora_normaliza_corretamente(self):
        dto = self._fn(self._dado_valido(dataApresentacao="2025-03-20T00:00:00"))
        self.assertEqual(dto["data_apresentacao"], date(2025, 3, 20))


class TestClassificarViaGemini(unittest.TestCase):
    """Testa _classificar_via_gemini — nova função com suporte a "irrelevante"."""

    def _mock_model(self, texto_resposta: str):
        mock_response = MagicMock()
        mock_response.text = texto_resposta
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        return mock_model

    def _chamar(self, texto_resposta: str, ementa: str = "ementa qualquer"):
        mock_model = self._mock_model(texto_resposta)
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "fake-key"}):
            with patch("google.generativeai.configure"):
                with patch("google.generativeai.GenerativeModel", return_value=mock_model):
                    # Recarrega para pegar nova versão
                    import importlib
                    import src.backend.services.camara_service as svc
                    importlib.reload(svc)
                    return svc._classificar_via_gemini(ementa)

    # 6.3 — resposta "irrelevante" → proposição descartada
    def test_resposta_irrelevante_retorna_irrelevante(self):
        resultado = self._chamar("irrelevante")
        self.assertEqual(resultado, "irrelevante")

    # 6.4 — categoria válida → retorna categoria
    def test_categoria_valida_retornada(self):
        resultado = self._chamar("cyberbullying")
        self.assertEqual(resultado, "cyberbullying")

    # 6.5 — resposta malformada → lança ValueError (caller trata como pendente)
    def test_resposta_malformada_lanca_excecao(self):
        mock_model = self._mock_model("categoria_que_nao_existe")
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "fake-key"}):
            with patch("google.generativeai.configure"):
                with patch("google.generativeai.GenerativeModel", return_value=mock_model):
                    import importlib
                    import src.backend.services.camara_service as svc
                    importlib.reload(svc)
                    with self.assertRaises(ValueError):
                        svc._classificar_via_gemini("ementa qualquer")

    def test_sem_api_key_lanca_runtime_error(self):
        env_sem_key = {k: v for k, v in os.environ.items() if k != "GOOGLE_API_KEY"}
        with patch.dict(os.environ, env_sem_key, clear=True):
            import importlib
            import src.backend.services.camara_service as svc
            importlib.reload(svc)
            with self.assertRaises(RuntimeError):
                svc._classificar_via_gemini("ementa")

    # 6.6 — 429 na primeira tentativa → aguarda 60s e re-tenta; segunda falha → pendente via caller
    def test_429_aguarda_e_retenta(self):
        class FakeResourceExhausted(Exception):
            pass

        mock_response = MagicMock()
        mock_response.text = "cyberbullying"
        mock_model = MagicMock()
        # Primeira chamada: 429. Segunda: sucesso.
        mock_model.generate_content.side_effect = [
            FakeResourceExhausted("429 ResourceExhausted"),
            mock_response,
        ]

        with patch.dict(os.environ, {"GOOGLE_API_KEY": "fake-key"}):
            with patch("google.generativeai.configure"):
                with patch("google.generativeai.GenerativeModel", return_value=mock_model):
                    with patch("time.sleep") as mock_sleep:
                        import importlib
                        import src.backend.services.camara_service as svc
                        importlib.reload(svc)
                        resultado = svc._classificar_via_gemini("ementa com cyberbullying")

        # Deve ter dormido 60s uma vez
        mock_sleep.assert_called_once_with(60)
        self.assertEqual(resultado, "cyberbullying")
        self.assertEqual(mock_model.generate_content.call_count, 2)


class TestClassificarEFiltrar(unittest.TestCase):
    """Testa _classificar_e_filtrar — retorna (dto, resultado)."""

    def _service(self):
        from src.backend.services.camara_service import CamaraService
        return CamaraService()

    def _dto(self):
        return {
            "id": 42,
            "ementa": "Proteção de dados de crianças na internet",
            "classificacao_status": "pendente_classificacao",
        }

    # 6.4 — categoria válida: dto classificado e categoria retornada
    def test_categoria_valida_retorna_dto_e_categoria(self):
        svc = self._service()
        with patch.object(svc, "_classificar_com_rate_limit", return_value="cyberbullying"):
            dto, resultado = svc._classificar_e_filtrar(self._dto())
        self.assertEqual(resultado, "cyberbullying")
        self.assertEqual(dto["classificacao_status"], "classificado")

    # 6.3 — irrelevante: dto não modificado, resultado é "irrelevante"
    def test_irrelevante_retorna_sentinel(self):
        svc = self._service()
        with patch.object(svc, "_classificar_com_rate_limit", return_value="irrelevante"):
            dto, resultado = svc._classificar_e_filtrar(self._dto())
        self.assertEqual(resultado, "irrelevante")
        # classificacao_status não deve ser alterado para irrelevante
        self.assertEqual(dto["classificacao_status"], "pendente_classificacao")

    # 6.5 — resposta malformada: resultado None, status pendente
    def test_falha_gemini_retorna_none_e_pendente(self):
        svc = self._service()
        with patch.object(svc, "_classificar_com_rate_limit", side_effect=ValueError("inválido")):
            dto, resultado = svc._classificar_e_filtrar(self._dto())
        self.assertIsNone(resultado)
        self.assertEqual(dto["classificacao_status"], "pendente_classificacao")

    # 6.5 — timeout: resultado None, status pendente
    def test_timeout_retorna_none_e_pendente(self):
        svc = self._service()
        with patch.object(svc, "_classificar_com_rate_limit", side_effect=TimeoutError("timeout")):
            dto, resultado = svc._classificar_e_filtrar(self._dto())
        self.assertIsNone(resultado)
        self.assertEqual(dto["classificacao_status"], "pendente_classificacao")


if __name__ == "__main__":
    unittest.main()
