"""
Testes de integração para camara_repository.py (requer BD PostgreSQL ativo).
Execução: python -m unittest tests.test_camara_repository
Pré-requisito: DATABASE_URL configurada no ambiente e migration aplicada.
"""
import os
import sys
import unittest
from datetime import date, datetime, timezone

os.environ.setdefault("FLASK_ENV", "testing")


def _get_app():
    from src.backend.app import app
    return app


class TestUpsertProposicoes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = _get_app()
        cls.ctx = cls.app.app_context()
        cls.ctx.push()
        from src.backend.database import db
        from src.backend.models import Proposicao, Partido
        cls.db = db

        # Garante que existe um partido de teste
        partido = db.session.query(Partido).filter_by(sigla="TEST").first()
        if not partido:
            from src.backend.models import Partido
            partido = Partido(sigla="TEST", nome="Partido de Teste")
            db.session.add(partido)
            db.session.commit()
        cls.partido_id = partido.id

    @classmethod
    def tearDownClass(cls):
        from src.backend.database import db
        from src.backend.models import Proposicao
        db.session.query(Proposicao).filter(Proposicao.id.in_([9999901, 9999902])).delete()
        db.session.commit()
        cls.ctx.pop()

    def _dto(self, id_=9999901, **override):
        base = {
            "id": id_,
            "sigla_tipo": "PL",
            "numero": id_,
            "ano": 2099,
            "ementa": "Ementa de teste",
            "data_apresentacao": date(2099, 1, 1),
            "descricao_situacao": "Em tramitação",
            "sigla_partido": "TEST",
            "data_coleta": datetime.now(timezone.utc),
            "classificacao_status": "pendente_classificacao",
        }
        base.update(override)
        return base

    def test_upsert_insere_proposicao_nova(self):
        from src.backend.repository.camara_repository import upsert_proposicoes_lote
        from src.backend.models import Proposicao

        self.db.session.query(Proposicao).filter_by(id=9999901).delete()
        self.db.session.commit()

        resultado = upsert_proposicoes_lote([self._dto(9999901)])
        self.assertEqual(resultado["inseridos"], 1)
        self.assertEqual(resultado["atualizados"], 0)

    def test_upsert_atualiza_proposicao_existente(self):
        from src.backend.repository.camara_repository import upsert_proposicoes_lote

        upsert_proposicoes_lote([self._dto(9999901)])
        resultado = upsert_proposicoes_lote([self._dto(9999901, ementa="Ementa atualizada")])
        self.assertEqual(resultado["atualizados"], 1)
        self.assertEqual(resultado["inseridos"], 0)

        from src.backend.models import Proposicao
        prop = self.db.session.get(Proposicao, 9999901)
        self.assertEqual(prop.ementa, "Ementa atualizada")

    def test_idempotencia_sem_mudancas(self):
        from src.backend.repository.camara_repository import upsert_proposicoes_lote

        dto = self._dto(9999901)
        upsert_proposicoes_lote([dto])
        resultado = upsert_proposicoes_lote([dto])

        self.assertEqual(resultado["inseridos"], 0)
        self.assertEqual(resultado["atualizados"], 1)


class TestSyncExecution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = _get_app()
        cls.ctx = cls.app.app_context()
        cls.ctx.push()
        from src.backend.database import db
        cls.db = db

    @classmethod
    def tearDownClass(cls):
        cls.ctx.pop()

    def test_criar_e_atualizar_sync_execution(self):
        from src.backend.repository.camara_repository import (
            criar_sync_execution,
            atualizar_sync_execution,
            get_ultimas_execucoes,
        )
        from src.backend.models import SyncExecution

        execucao = criar_sync_execution()
        self.assertIsNotNone(execucao.id)
        self.assertEqual(execucao.status, SyncExecution.STATUS_EM_ANDAMENTO)

        atualizar_sync_execution(
            execucao.id,
            status=SyncExecution.STATUS_CONCLUIDO,
            total_processados=10,
            total_inseridos=5,
            total_atualizados=5,
            finalizado_em=datetime.now(timezone.utc),
        )

        self.db.session.expire_all()
        atualizada = self.db.session.get(SyncExecution, execucao.id)
        self.assertEqual(atualizada.status, SyncExecution.STATUS_CONCLUIDO)
        self.assertEqual(atualizada.total_processados, 10)

    def test_get_ultimas_execucoes(self):
        from src.backend.repository.camara_repository import (
            criar_sync_execution,
            get_ultimas_execucoes,
        )

        criar_sync_execution()
        execucoes = get_ultimas_execucoes(limite=5)
        self.assertLessEqual(len(execucoes), 5)
        self.assertGreater(len(execucoes), 0)


class TestRunSyncIntegration(unittest.TestCase):
    """Testes de run_sync() com API da Câmara mockada."""

    @classmethod
    def setUpClass(cls):
        cls.app = _get_app()
        cls.ctx = cls.app.app_context()
        cls.ctx.push()

    @classmethod
    def tearDownClass(cls):
        cls.ctx.pop()

    def test_run_sync_completo_sucesso(self):
        from unittest.mock import patch
        from src.backend.services.camara_service import CamaraService

        dados_mock = [{
            "id": 9999999,
            "siglaTipo": "PL",
            "numero": 9999,
            "ano": 2099,
            "ementa": "Proteção contra cyberbullying em redes sociais",
            "dataApresentacao": "2099-01-01",
            "descricaoSituacao": "Em tramitação",
            "siglaPartido": "PT",
        }]

        with patch("src.backend.services.camara_service._buscar_proposicoes_api",
                   side_effect=[dados_mock, []]):
            with patch.object(CamaraService, "_categorizar_com_rate_limit",
                              return_value="cyberbullying"):
                resumo = CamaraService().run_sync()

        self.assertIn(resumo["status"], ["concluido", "concluido_parcial"])
        self.assertGreaterEqual(resumo["total_processados"], 1)

    def test_run_sync_erro_api_registra_sync_execution(self):
        from unittest.mock import patch
        import requests
        from src.backend.services.camara_service import CamaraService
        from src.backend.models import SyncExecution
        from src.backend.database import db

        with patch("src.backend.services.camara_service._buscar_proposicoes_api",
                   side_effect=requests.ConnectionError("timeout")):
            resumo = CamaraService().run_sync()

        self.assertEqual(resumo["status"], SyncExecution.STATUS_ERRO_API)


if __name__ == "__main__":
    unittest.main()
