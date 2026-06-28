"""
Testes de integração para camara_repository.py (requer BD PostgreSQL ativo).
Execução: python -m unittest tests.test_camara_repository
Pré-requisito: DATABASE_URL configurada no ambiente e ambas as migrations aplicadas.
"""
import os
import sys
import unittest
from datetime import date, datetime, timezone

os.environ.setdefault("FLASK_ENV", "testing")


def _get_app():
    from src.backend.app import app
    return app


class TestSeedCategorias(unittest.TestCase):
    """6.1 — seed_categorias() insere as 8 categorias e é idempotente."""

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

    def test_seed_insere_8_categorias(self):
        from src.backend.repository.camara_repository import seed_categorias, SEED_CATEGORIAS
        from src.backend.models import Categoria

        seed_categorias()
        nomes_seed = {c["nome"] for c in SEED_CATEGORIAS}
        nomes_banco = {
            r[0]
            for r in self.db.session.query(Categoria.nome)
            .filter(Categoria.nome.in_(nomes_seed))
            .all()
        }
        self.assertEqual(nomes_banco, nomes_seed)

    def test_seed_e_idempotente(self):
        from src.backend.repository.camara_repository import seed_categorias, SEED_CATEGORIAS
        from src.backend.models import Categoria

        seed_categorias()
        seed_categorias()  # segunda chamada não deve duplicar

        nomes_seed = [c["nome"] for c in SEED_CATEGORIAS]
        count = (
            self.db.session.query(Categoria)
            .filter(Categoria.nome.in_(nomes_seed))
            .count()
        )
        self.assertEqual(count, len(SEED_CATEGORIAS))


class TestVincularCategoria(unittest.TestCase):
    """6.2 — vincular_categoria() cria vínculo na junction table e é idempotente."""

    @classmethod
    def setUpClass(cls):
        cls.app = _get_app()
        cls.ctx = cls.app.app_context()
        cls.ctx.push()
        from src.backend.database import db
        cls.db = db

        # Seed para garantir que categorias existam
        from src.backend.repository.camara_repository import seed_categorias
        seed_categorias()

        # Proposição de teste
        from src.backend.repository.camara_repository import upsert_proposicoes_lote
        upsert_proposicoes_lote([{
            "id": 9999800,
            "sigla_tipo": "PL",
            "numero": 9998,
            "ano": 2099,
            "ementa": "Proteção contra cyberbullying em escolas",
            "data_apresentacao": date(2099, 1, 1),
            "descricao_situacao": "Em tramitação",
            "sigla_partido": "TEST",
            "data_coleta": datetime.now(timezone.utc),
            "classificacao_status": "pendente_classificacao",
        }])

    @classmethod
    def tearDownClass(cls):
        from src.backend.models import Proposicao
        cls.db.session.query(Proposicao).filter_by(id=9999800).delete()
        cls.db.session.commit()
        cls.ctx.pop()

    def test_vincular_cria_relacao(self):
        from src.backend.repository.camara_repository import vincular_categoria
        from src.backend.models import Proposicao

        vincular_categoria(9999800, "cyberbullying")

        prop = self.db.session.get(Proposicao, 9999800)
        self.db.session.refresh(prop)
        categorias = prop.categorias.all()
        nomes = [c.nome for c in categorias]
        self.assertIn("cyberbullying", nomes)

    def test_vincular_e_idempotente(self):
        from src.backend.repository.camara_repository import vincular_categoria
        from src.backend.models import Proposicao, proposicao_categoria
        from sqlalchemy import func

        vincular_categoria(9999800, "cyberbullying")
        vincular_categoria(9999800, "cyberbullying")  # segunda vez não duplica

        count = self.db.session.query(
            func.count(proposicao_categoria.c.categoria_id)
        ).filter(
            proposicao_categoria.c.proposicao_id == 9999800
        ).scalar()
        self.assertEqual(count, 1)

    def test_vincular_categoria_inexistente_nao_explode(self):
        from src.backend.repository.camara_repository import vincular_categoria
        vincular_categoria(9999800, "categoria_que_nao_existe")  # deve logar warning e não lançar


class TestUpsertProposicoes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = _get_app()
        cls.ctx = cls.app.app_context()
        cls.ctx.push()
        from src.backend.database import db
        from src.backend.models import Partido
        cls.db = db

        partido = db.session.query(Partido).filter_by(sigla="TEST").first()
        if not partido:
            partido = Partido(sigla="TEST", nome="Partido de Teste")
            db.session.add(partido)
            db.session.commit()
        cls.partido_id = partido.id

    @classmethod
    def tearDownClass(cls):
        from src.backend.models import Proposicao
        cls.db.session.query(Proposicao).filter(Proposicao.id.in_([9999901, 9999902])).delete()
        cls.db.session.commit()
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


class TestGetIdsExistentes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = _get_app()
        cls.ctx = cls.app.app_context()
        cls.ctx.push()
        from src.backend.database import db
        from src.backend.repository.camara_repository import upsert_proposicoes_lote
        cls.db = db
        upsert_proposicoes_lote([{
            "id": 9999850,
            "sigla_tipo": "PL",
            "numero": 9850,
            "ano": 2099,
            "ementa": "Ementa para teste de ids existentes",
            "data_apresentacao": date(2099, 1, 1),
            "descricao_situacao": "Em tramitação",
            "sigla_partido": "TEST",
            "data_coleta": datetime.now(timezone.utc),
            "classificacao_status": "pendente_classificacao",
        }])

    @classmethod
    def tearDownClass(cls):
        from src.backend.models import Proposicao
        cls.db.session.query(Proposicao).filter_by(id=9999850).delete()
        cls.db.session.commit()
        cls.ctx.pop()

    def test_retorna_ids_existentes(self):
        from src.backend.repository.camara_repository import get_ids_existentes
        resultado = get_ids_existentes([9999850, 1, 2])
        self.assertIn(9999850, resultado)
        self.assertNotIn(1, resultado)
        self.assertNotIn(2, resultado)

    def test_lista_vazia_retorna_set_vazio(self):
        from src.backend.repository.camara_repository import get_ids_existentes
        self.assertEqual(get_ids_existentes([]), set())

    def test_nenhum_existente_retorna_set_vazio(self):
        from src.backend.repository.camara_repository import get_ids_existentes
        self.assertEqual(get_ids_existentes([1, 2, 3]), set())

    def test_todos_existentes(self):
        from src.backend.repository.camara_repository import get_ids_existentes
        resultado = get_ids_existentes([9999850])
        self.assertEqual(resultado, {9999850})


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
    """Testes de run_sync() com API da Câmara e Gemini mockados."""

    @classmethod
    def setUpClass(cls):
        cls.app = _get_app()
        cls.ctx = cls.app.app_context()
        cls.ctx.push()
        from src.backend.repository.camara_repository import seed_categorias
        seed_categorias()

    @classmethod
    def tearDownClass(cls):
        from src.backend.database import db
        from src.backend.models import Proposicao
        db.session.query(Proposicao).filter(Proposicao.id.in_([9999999, 9999998])).delete()
        db.session.commit()
        cls.ctx.pop()

    def _dado_mock(self, id_=9999999, ementa="Proteção contra cyberbullying em redes sociais"):
        return {
            "id": id_,
            "siglaTipo": "PL",
            "numero": id_,
            "ano": 2099,
            "ementa": ementa,
            "dataApresentacao": "2099-01-01",
            "descricaoSituacao": "Em tramitação",
            "siglaPartido": "PT",
        }

    def test_run_sync_completo_sucesso(self):
        from unittest.mock import patch
        from src.backend.services.camara_service import CamaraService

        with patch("src.backend.services.camara_service._buscar_proposicoes_api",
                   side_effect=[[self._dado_mock(9999999)], []]):
            with patch("src.backend.services.camara_service._classificar_lote_via_gemini",
                       return_value=[["cyberbullying"]]):
                resumo = CamaraService().run_sync()

        self.assertIn(resumo["status"], ["concluido", "concluido_parcial"])
        self.assertGreaterEqual(resumo["total_processados"], 1)
        self.assertEqual(resumo["total_inseridos"], 1)

    # 6.3 — Gemini retorna "irrelevante": proposição não é persistida
    def test_run_sync_irrelevante_nao_persiste(self):
        from unittest.mock import patch
        from src.backend.services.camara_service import CamaraService
        from src.backend.models import Proposicao
        from src.backend.database import db

        db.session.query(Proposicao).filter_by(id=9999998).delete()
        db.session.commit()

        with patch("src.backend.services.camara_service._buscar_proposicoes_api",
                   side_effect=[[self._dado_mock(9999998)], []]):
            with patch("src.backend.services.camara_service._classificar_lote_via_gemini",
                       return_value=[["irrelevante"]]):
                resumo = CamaraService().run_sync()

        self.assertEqual(resumo["total_descartados"], 1)
        self.assertEqual(resumo["total_inseridos"], 0)
        prop = db.session.get(Proposicao, 9999998)
        self.assertIsNone(prop)

    def test_run_sync_erro_api_registra_sync_execution(self):
        from unittest.mock import patch
        import requests
        from src.backend.services.camara_service import CamaraService
        from src.backend.models import SyncExecution

        with patch("src.backend.services.camara_service._buscar_proposicoes_api",
                   side_effect=requests.ConnectionError("timeout")):
            resumo = CamaraService().run_sync()

        self.assertEqual(resumo["status"], SyncExecution.STATUS_ERRO_API)

    # 6.7 — Retry de pendentes: proposição pendente é classificada e vinculada
    def test_retry_pendentes_classifica_e_vincula(self):
        from unittest.mock import patch
        from src.backend.repository.camara_repository import (
            upsert_proposicoes_lote,
            vincular_categoria,
            get_proposicoes_pendentes,
        )
        from src.backend.services.camara_service import CamaraService
        from src.backend.models import Proposicao
        from src.backend.database import db

        # Criar proposição pendente
        upsert_proposicoes_lote([{
            "id": 9999997,
            "sigla_tipo": "PL",
            "numero": 9997,
            "ano": 2099,
            "ementa": "Proteção de dados de menores em redes sociais",
            "data_apresentacao": date(2099, 1, 1),
            "descricao_situacao": "Em tramitação",
            "sigla_partido": "TEST",
            "data_coleta": datetime.now(timezone.utc),
            "classificacao_status": "pendente_classificacao",
        }])

        # run_sync com API vazia mas Gemini classifica o pendente
        with patch("src.backend.services.camara_service._buscar_proposicoes_api",
                   return_value=[]):
            with patch("src.backend.services.camara_service._classificar_lote_via_gemini",
                       return_value=[["proteção de dados de menores"]]):
                CamaraService().run_sync()

        db.session.expire_all()
        prop = db.session.get(Proposicao, 9999997)
        self.assertEqual(prop.classificacao_status, "classificado")
        categorias = prop.categorias.all()
        self.assertTrue(any(c.nome == "proteção de dados de menores" for c in categorias))

        # Limpeza
        db.session.delete(prop)
        db.session.commit()

    # 6.8 — Retry de pendentes com "irrelevante": proposição é deletada
    def test_retry_pendentes_irrelevante_deleta(self):
        from unittest.mock import patch
        from src.backend.repository.camara_repository import upsert_proposicoes_lote
        from src.backend.services.camara_service import CamaraService
        from src.backend.models import Proposicao
        from src.backend.database import db

        upsert_proposicoes_lote([{
            "id": 9999996,
            "sigla_tipo": "PL",
            "numero": 9996,
            "ano": 2099,
            "ementa": "Regulação de trânsito urbano",
            "data_apresentacao": date(2099, 1, 1),
            "descricao_situacao": "Em tramitação",
            "sigla_partido": "TEST",
            "data_coleta": datetime.now(timezone.utc),
            "classificacao_status": "pendente_classificacao",
        }])

        with patch("src.backend.services.camara_service._buscar_proposicoes_api",
                   return_value=[]):
            with patch("src.backend.services.camara_service._classificar_lote_via_gemini",
                       return_value=[["irrelevante"]]):
                CamaraService().run_sync()

        db.session.expire_all()
        prop = db.session.get(Proposicao, 9999996)
        self.assertIsNone(prop)

    def test_early_stop_quando_todos_ids_conhecidos(self):
        """Paginação encerra quando todos os IDs brutos da página já estão no banco."""
        from unittest.mock import patch, call
        from src.backend.repository.camara_repository import upsert_proposicoes_lote
        from src.backend.services.camara_service import CamaraService
        from src.backend.database import db

        upsert_proposicoes_lote([{
            "id": 9999995,
            "sigla_tipo": "PL",
            "numero": 9995,
            "ano": 2099,
            "ementa": "Proteção de crianças na internet",
            "data_apresentacao": date(2099, 1, 1),
            "descricao_situacao": "Em tramitação",
            "sigla_partido": "TEST",
            "data_coleta": datetime.now(timezone.utc),
            "classificacao_status": "classificado",
        }])

        dado_conhecido = {
            "id": 9999995,
            "siglaTipo": "PL",
            "numero": 9995,
            "ano": 2099,
            "ementa": "Proteção de crianças na internet",
            "dataApresentacao": "2099-01-01",
            "descricaoSituacao": "Em tramitação",
        }

        with patch("src.backend.services.camara_service._buscar_proposicoes_api",
                   side_effect=[[dado_conhecido], []]) as mock_api:
            with patch("src.backend.services.camara_service._classificar_lote_via_gemini") as mock_gemini:
                CamaraService().run_sync()

        # API chamada apenas uma vez (parou após página 1 com ID conhecido)
        self.assertEqual(mock_api.call_count, 1)
        # Gemini não foi chamado para proposição já no banco
        mock_gemini.assert_not_called()

        db.session.query(__import__('src.backend.models', fromlist=['Proposicao']).Proposicao).filter_by(id=9999995).delete()
        db.session.commit()

    def test_skip_gemini_para_id_ja_no_banco(self):
        """Proposição com ID já no banco não é enviada ao Gemini no run principal."""
        from unittest.mock import patch
        from src.backend.repository.camara_repository import upsert_proposicoes_lote
        from src.backend.services.camara_service import CamaraService
        from src.backend.database import db

        upsert_proposicoes_lote([{
            "id": 9999994,
            "sigla_tipo": "PL",
            "numero": 9994,
            "ano": 2099,
            "ementa": "Proteção de crianças na internet",
            "data_apresentacao": date(2099, 1, 1),
            "descricao_situacao": "Em tramitação",
            "sigla_partido": "TEST",
            "data_coleta": datetime.now(timezone.utc),
            "classificacao_status": "classificado",
        }])

        dado_conhecido = {
            "id": 9999994,
            "siglaTipo": "PL",
            "numero": 9994,
            "ano": 2099,
            "ementa": "Proteção de crianças na internet",
            "dataApresentacao": "2099-01-01",
            "descricaoSituacao": "Em tramitação",
        }
        dado_novo = {
            "id": 8888881,
            "siglaTipo": "PL",
            "numero": 8881,
            "ano": 2099,
            "ementa": "Segurança digital infantil em redes sociais",
            "dataApresentacao": "2099-01-01",
            "descricaoSituacao": "Em tramitação",
        }

        with patch("src.backend.services.camara_service._buscar_proposicoes_api",
                   side_effect=[[dado_conhecido, dado_novo], []]):
            with patch("src.backend.services.camara_service._classificar_lote_via_gemini",
                       return_value=[["segurança digital infantil"]]) as mock_gemini:
                CamaraService().run_sync()

        # Gemini chamado apenas com o DTO novo (id 8888881), não com o já conhecido
        self.assertEqual(mock_gemini.call_count, 1)
        ementas_enviadas = mock_gemini.call_args[0][0]
        self.assertEqual(len(ementas_enviadas), 1)
        self.assertIn("Segurança digital infantil", ementas_enviadas[0])

        from src.backend.models import Proposicao
        db.session.query(Proposicao).filter(Proposicao.id.in_([9999994, 8888881])).delete()
        db.session.commit()


if __name__ == "__main__":
    unittest.main()
