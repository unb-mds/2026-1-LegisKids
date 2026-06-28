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


class TestClassificarLoteViaGemini(unittest.TestCase):
    """Testa _classificar_lote_via_gemini — classificação em batch com múltiplas categorias."""

    def _mock_client(self, texto_resposta: str):
        mock_response = MagicMock()
        mock_response.text = texto_resposta
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response
        return mock_client

    def _chamar(self, texto_resposta: str, ementas=None):
        if ementas is None:
            ementas = ["ementa qualquer"]
        mock_client = self._mock_client(texto_resposta)
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "fake-key"}):
            with patch("google.genai.Client", return_value=mock_client):
                from src.backend.services.camara_service import _classificar_lote_via_gemini
                return _classificar_lote_via_gemini(ementas)

    def test_resposta_irrelevante_retorna_lista_irrelevante(self):
        resultado = self._chamar("1: irrelevante")
        self.assertEqual(resultado, [["irrelevante"]])

    def test_categoria_valida_retornada(self):
        resultado = self._chamar("1: cyberbullying")
        self.assertEqual(resultado, [["cyberbullying"]])

    def test_multiplas_categorias_por_ementa(self):
        resultado = self._chamar("1: cyberbullying, proteção de dados de menores")
        self.assertEqual(resultado, [["cyberbullying", "proteção de dados de menores"]])

    def test_lote_com_multiplas_ementas(self):
        resultado = self._chamar(
            "1: cyberbullying\n2: irrelevante\n3: segurança digital infantil",
            ementas=["e1", "e2", "e3"],
        )
        self.assertEqual(resultado[0], ["cyberbullying"])
        self.assertEqual(resultado[1], ["irrelevante"])
        self.assertEqual(resultado[2], ["segurança digital infantil"])

    def test_resposta_malformada_cai_para_irrelevante(self):
        resultado = self._chamar("1: categoria_que_nao_existe")
        self.assertEqual(resultado, [["irrelevante"]])

    def test_sem_api_key_lanca_runtime_error(self):
        env_sem_key = {k: v for k, v in os.environ.items() if k != "GOOGLE_API_KEY"}
        with patch.dict(os.environ, env_sem_key, clear=True):
            from src.backend.services.camara_service import _classificar_lote_via_gemini
            with self.assertRaises(RuntimeError):
                _classificar_lote_via_gemini(["ementa"])

    def test_429_aguarda_e_retenta(self):
        class FakeResourceExhausted(Exception):
            pass

        mock_response = MagicMock()
        mock_response.text = "1: cyberbullying"
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = [
            FakeResourceExhausted("429 ResourceExhausted"),
            mock_response,
        ]

        with patch.dict(os.environ, {"GOOGLE_API_KEY": "fake-key"}):
            with patch("google.genai.Client", return_value=mock_client):
                with patch("time.sleep") as mock_sleep:
                    from src.backend.services.camara_service import _classificar_lote_via_gemini
                    resultado = _classificar_lote_via_gemini(["ementa com cyberbullying"])

        mock_sleep.assert_called_once_with(60)
        self.assertEqual(resultado, [["cyberbullying"]])
        self.assertEqual(mock_client.models.generate_content.call_count, 2)


class TestClassificarEFiltrar(unittest.TestCase):
    """Testa _classificar_e_filtrar — retorna (dto, list[str] | None)."""

    def _service(self):
        from src.backend.services.camara_service import CamaraService
        return CamaraService()

    def _dto(self):
        return {
            "id": 42,
            "ementa": "Proteção de dados de crianças na internet",
            "classificacao_status": "pendente_classificacao",
        }

    def test_categoria_valida_retorna_dto_e_lista(self):
        svc = self._service()
        with patch("src.backend.services.camara_service._classificar_lote_via_gemini",
                   return_value=[["cyberbullying"]]):
            dto, resultado = svc._classificar_e_filtrar(self._dto())
        self.assertEqual(resultado, ["cyberbullying"])
        self.assertEqual(dto["classificacao_status"], "classificado")

    def test_multiplas_categorias_retornadas(self):
        svc = self._service()
        with patch("src.backend.services.camara_service._classificar_lote_via_gemini",
                   return_value=[["cyberbullying", "proteção de dados de menores"]]):
            dto, resultado = svc._classificar_e_filtrar(self._dto())
        self.assertEqual(resultado, ["cyberbullying", "proteção de dados de menores"])
        self.assertEqual(dto["classificacao_status"], "classificado")

    def test_irrelevante_retorna_sentinel(self):
        svc = self._service()
        with patch("src.backend.services.camara_service._classificar_lote_via_gemini",
                   return_value=[["irrelevante"]]):
            dto, resultado = svc._classificar_e_filtrar(self._dto())
        self.assertEqual(resultado, ["irrelevante"])
        self.assertEqual(dto["classificacao_status"], "pendente_classificacao")

    def test_falha_gemini_retorna_none_e_pendente(self):
        svc = self._service()
        with patch("src.backend.services.camara_service._classificar_lote_via_gemini",
                   side_effect=ValueError("falha")):
            dto, resultado = svc._classificar_e_filtrar(self._dto())
        self.assertIsNone(resultado)
        self.assertEqual(dto["classificacao_status"], "pendente_classificacao")

    def test_timeout_retorna_none_e_pendente(self):
        svc = self._service()
        with patch("src.backend.services.camara_service._classificar_lote_via_gemini",
                   side_effect=TimeoutError("timeout")):
            dto, resultado = svc._classificar_e_filtrar(self._dto())
        self.assertIsNone(resultado)
        self.assertEqual(dto["classificacao_status"], "pendente_classificacao")


if __name__ == "__main__":
    unittest.main()
