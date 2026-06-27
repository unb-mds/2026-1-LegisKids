"""
Testes unitários para camara_service.py (sem BD real — dependências mockadas).
Execução: python -m pytest tests/ ou python -m unittest tests.test_camara_service
"""
import unittest
from datetime import date
from unittest.mock import MagicMock, patch

import os
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


class TestCategorizarViaGemini(unittest.TestCase):
    def test_categoria_valida_retornada(self):
        mock_response = MagicMock()
        mock_response.text = "cyberbullying"

        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response

        with patch.dict(os.environ, {"GOOGLE_API_KEY": "fake-key"}):
            with patch("google.generativeai.configure"):
                with patch("google.generativeai.GenerativeModel", return_value=mock_model):
                    from src.backend.services.camara_service import _categorizar_via_gemini
                    resultado = _categorizar_via_gemini("Proteção contra cyberbullying")
        self.assertEqual(resultado, "cyberbullying")

    def test_categoria_invalida_lanca_excecao(self):
        mock_response = MagicMock()
        mock_response.text = "categoria_inexistente"

        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response

        with patch.dict(os.environ, {"GOOGLE_API_KEY": "fake-key"}):
            with patch("google.generativeai.configure"):
                with patch("google.generativeai.GenerativeModel", return_value=mock_model):
                    from src.backend.services.camara_service import _categorizar_via_gemini
                    with self.assertRaises(ValueError):
                        _categorizar_via_gemini("alguma ementa")

    def test_sem_api_key_lanca_runtime_error(self):
        env = {k: v for k, v in os.environ.items() if k != "GOOGLE_API_KEY"}
        with patch.dict(os.environ, env, clear=True):
            with patch("google.generativeai.configure"):
                from src.backend.services import camara_service
                with self.assertRaises(RuntimeError):
                    camara_service._categorizar_via_gemini("ementa")


class TestCategorizarComFallback(unittest.TestCase):
    def _service(self):
        from src.backend.services.camara_service import CamaraService
        return CamaraService()

    def _dto(self):
        return {
            "id": 42,
            "ementa": "Proteção de dados de crianças",
            "classificacao_status": "pendente_classificacao",
        }

    def test_fallback_em_timeout(self):
        svc = self._service()
        with patch.object(svc, "_categorizar_com_rate_limit", side_effect=TimeoutError("timeout")):
            dto = svc._categorizar_com_fallback(self._dto())
        self.assertEqual(dto["classificacao_status"], "pendente_classificacao")

    def test_fallback_categoria_invalida(self):
        svc = self._service()
        with patch.object(svc, "_categorizar_com_rate_limit", side_effect=ValueError("cat inválida")):
            dto = svc._categorizar_com_fallback(self._dto())
        self.assertEqual(dto["classificacao_status"], "pendente_classificacao")

    def test_sem_fallback_quando_sucesso(self):
        svc = self._service()
        with patch.object(svc, "_categorizar_com_rate_limit", return_value="cyberbullying"):
            dto = svc._categorizar_com_fallback(self._dto())
        self.assertEqual(dto["classificacao_status"], "classificado")


if __name__ == "__main__":
    unittest.main()
