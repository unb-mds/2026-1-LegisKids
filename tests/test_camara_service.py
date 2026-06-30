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


class TestRunSyncFilaAcumulada(unittest.TestCase):
    """
    Testa o comportamento de fila acumulada entre páginas no run_sync().
    Tasks 3.1–3.4 do change sync-camara-gemini-batch-queue.
    """

    def _raw(self, id_):
        return {
            "id": id_,
            "siglaTipo": "PL",
            "numero": id_,
            "ano": 2025,
            "ementa": "proteção de dados de crianças na internet",
            "dataApresentacao": "2025-01-15",
            "descricaoSituacao": "Em tramitação",
            "siglaPartido": "PT",
        }

    def _service(self, batch_size=10):
        from src.backend.services.camara_service import CamaraService
        svc = CamaraService()
        svc._batch_size = batch_size
        return svc

    def _setup_criar(self, mock_criar):
        mock_exec = MagicMock()
        mock_exec.id = 1
        mock_criar.return_value = mock_exec

    def _classificar_ok(self, dtos):
        for dto in dtos:
            dto["classificacao_status"] = "classificado"
        return [(dto, ["cyberbullying"]) for dto in dtos]

    def _classificar_none(self, dtos):
        return [(dto, None) for dto in dtos]

    @patch("src.backend.services.camara_service.repo.get_proposicoes_pendentes", return_value=[])
    @patch("src.backend.services.camara_service.repo.vincular_categorias_lote")
    @patch("src.backend.services.camara_service.repo.upsert_proposicoes_lote",
           return_value={"inseridos": 1, "atualizados": 0})
    @patch("src.backend.services.camara_service.repo.get_ids_existentes", return_value=set())
    @patch("src.backend.services.camara_service.repo.atualizar_sync_execution")
    @patch("src.backend.services.camara_service.repo.criar_sync_execution")
    @patch("src.backend.services.camara_service._buscar_proposicoes_api")
    def test_3_1_acumula_multiplas_paginas_antes_do_gemini(
        self, mock_api, mock_criar, mock_atualizar, mock_ids, mock_upsert, mock_vincular, mock_pendentes
    ):
        """Proposições de múltiplas páginas acumulam na fila antes de acionar _classificar_lote."""
        self._setup_criar(mock_criar)
        svc = self._service(batch_size=10)

        page1 = [self._raw(i) for i in range(1, 5)]   # 4 proposições
        page2 = [self._raw(i) for i in range(5, 11)]  # 6 → fila chega a 10 e drena
        mock_api.side_effect = [page1, page2, []]

        with patch.object(svc, "_classificar_lote", side_effect=self._classificar_ok) as mock_cl:
            svc.run_sync()

        self.assertEqual(mock_cl.call_count, 1, "deve ter uma única chamada ao Gemini com lote de 10")
        args, _ = mock_cl.call_args
        self.assertEqual(len(args[0]), 10)

    @patch("src.backend.services.camara_service.repo.get_proposicoes_pendentes", return_value=[])
    @patch("src.backend.services.camara_service.repo.vincular_categorias_lote")
    @patch("src.backend.services.camara_service.repo.upsert_proposicoes_lote",
           return_value={"inseridos": 1, "atualizados": 0})
    @patch("src.backend.services.camara_service.repo.get_ids_existentes", return_value=set())
    @patch("src.backend.services.camara_service.repo.atualizar_sync_execution")
    @patch("src.backend.services.camara_service.repo.criar_sync_execution")
    @patch("src.backend.services.camara_service._buscar_proposicoes_api")
    def test_3_2_lote_residual_classificado_apos_paginacao(
        self, mock_api, mock_criar, mock_atualizar, mock_ids, mock_upsert, mock_vincular, mock_pendentes
    ):
        """Proposições que não completam um lote cheio são classificadas após a paginação terminar."""
        self._setup_criar(mock_criar)
        svc = self._service(batch_size=10)

        page1 = [self._raw(i) for i in range(1, 4)]  # 3 proposições — abaixo do BATCH_SIZE
        mock_api.side_effect = [page1, []]

        with patch.object(svc, "_classificar_lote", side_effect=self._classificar_ok) as mock_cl:
            svc.run_sync()

        self.assertEqual(mock_cl.call_count, 1, "lote residual deve ser classificado após paginação")
        args, _ = mock_cl.call_args
        self.assertEqual(len(args[0]), 3)

    @patch("src.backend.services.camara_service.repo.get_proposicoes_pendentes", return_value=[])
    @patch("src.backend.services.camara_service.repo.vincular_categorias_lote")
    @patch("src.backend.services.camara_service.repo.upsert_proposicoes_lote",
           return_value={"inseridos": 5, "atualizados": 0})
    @patch("src.backend.services.camara_service.repo.get_ids_existentes", return_value=set())
    @patch("src.backend.services.camara_service.repo.atualizar_sync_execution")
    @patch("src.backend.services.camara_service.repo.criar_sync_execution")
    @patch("src.backend.services.camara_service._buscar_proposicoes_api")
    def test_3_3_cota_esgotada_pula_gemini_nos_lotes_seguintes(
        self, mock_api, mock_criar, mock_atualizar, mock_ids, mock_upsert, mock_vincular, mock_pendentes
    ):
        """Quando o Gemini esgota a cota, lotes subsequentes marcam como pendente sem chamar o Gemini."""
        self._setup_criar(mock_criar)
        svc = self._service(batch_size=5)

        page1 = [self._raw(i) for i in range(1, 6)]   # 5 → lote 1, quota esgota
        page2 = [self._raw(i) for i in range(6, 11)]  # 5 → lote 2, deve pular Gemini
        mock_api.side_effect = [page1, page2, []]

        with patch.object(svc, "_classificar_lote", side_effect=self._classificar_none) as mock_cl:
            svc.run_sync()

        self.assertEqual(mock_cl.call_count, 1, "cota esgotada deve impedir chamadas subsequentes ao Gemini")

    @patch("src.backend.services.camara_service.repo.get_proposicoes_pendentes", return_value=[])
    @patch("src.backend.services.camara_service.repo.get_ids_existentes", return_value=set())
    @patch("src.backend.services.camara_service.repo.atualizar_sync_execution")
    @patch("src.backend.services.camara_service.repo.criar_sync_execution")
    @patch("src.backend.services.camara_service._buscar_proposicoes_api")
    def test_3_4_totais_acumulam_ao_longo_dos_lotes(
        self, mock_api, mock_criar, mock_atualizar, mock_ids, mock_pendentes
    ):
        """total_inseridos e total_descartados acumulam corretamente de múltiplos drenos da fila."""
        self._setup_criar(mock_criar)
        svc = self._service(batch_size=5)

        page1 = [self._raw(i) for i in range(1, 6)]    # 5 → lote 1
        page2 = [self._raw(i) for i in range(6, 11)]   # 5 → lote 2
        page3 = [self._raw(i) for i in range(11, 14)]  # 3 → residual
        mock_api.side_effect = [page1, page2, page3, []]

        processar_retornos = [
            (3, 0, 2, False),  # lote 1: 3 inseridos, 2 descartados
            (4, 0, 1, False),  # lote 2: 4 inseridos, 1 descartado
            (2, 0, 1, False),  # residual: 2 inseridos, 1 descartado
        ]

        with patch.object(svc, "_processar_lote", side_effect=processar_retornos):
            svc.run_sync()

        kwargs = mock_atualizar.call_args[1]
        self.assertEqual(kwargs["total_inseridos"], 9)    # 3 + 4 + 2
        self.assertEqual(kwargs["total_descartados"], 4)  # 2 + 1 + 1


if __name__ == "__main__":
    unittest.main()
