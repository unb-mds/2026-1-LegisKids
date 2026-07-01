"""
Testes de integração para proposicoes_controller.py (requer BD PostgreSQL ativo).
Execução: python -m unittest tests.test_proposicoes_controller
Pré-requisito: DATABASE_URL configurada no ambiente e ambas as migrations aplicadas.
"""
import os
import unittest
from datetime import date, datetime, timezone

os.environ.setdefault("FLASK_ENV", "testing")


def _get_app():
    from src.backend.app import app
    return app


class TestSerializacaoSubtemas(unittest.TestCase):
    """Serializer expõe `subtemas` (array) com todas as categorias vinculadas."""

    ID_MULTIPLAS = 9999700
    ID_SEM_CATEGORIA = 9999701

    @classmethod
    def setUpClass(cls):
        cls.app = _get_app()
        cls.client = cls.app.test_client()
        cls.ctx = cls.app.app_context()
        cls.ctx.push()

        from src.backend.database import db
        from src.backend.repository.camara_repository import (
            seed_categorias,
            upsert_proposicoes_lote,
            vincular_categorias_lote,
        )
        cls.db = db
        seed_categorias()

        upsert_proposicoes_lote([
            {
                "id": cls.ID_MULTIPLAS,
                "sigla_tipo": "PL",
                "numero": 9700,
                "ano": 2099,
                "ementa": "Proteção de dados e segurança digital de crianças em redes sociais",
                "data_apresentacao": date(2099, 1, 1),
                "descricao_situacao": "Em tramitação",
                "sigla_partido": "TEST",
                "data_coleta": datetime.now(timezone.utc),
                "classificacao_status": "classificado",
            },
            {
                "id": cls.ID_SEM_CATEGORIA,
                "sigla_tipo": "PL",
                "numero": 9701,
                "ano": 2099,
                "ementa": "Ementa de teste sem categoria vinculada",
                "data_apresentacao": date(2099, 1, 1),
                "descricao_situacao": "Em tramitação",
                "sigla_partido": "TEST",
                "data_coleta": datetime.now(timezone.utc),
                "classificacao_status": "pendente_classificacao",
            },
        ])
        vincular_categorias_lote(
            cls.ID_MULTIPLAS,
            ["proteção de dados de menores", "segurança digital infantil"],
        )

    @classmethod
    def tearDownClass(cls):
        from src.backend.models import Proposicao
        cls.db.session.query(Proposicao).filter(
            Proposicao.id.in_([cls.ID_MULTIPLAS, cls.ID_SEM_CATEGORIA])
        ).delete(synchronize_session=False)
        cls.db.session.commit()
        cls.ctx.pop()

    def test_listagem_retorna_todos_os_subtemas(self):
        resp = self.client.get("/api/proposicoes?por_pagina=50")
        self.assertEqual(resp.status_code, 200)
        items = resp.get_json()["items"]
        item = next(i for i in items if i["id"] == self.ID_MULTIPLAS)

        self.assertIn("subtemas", item)
        self.assertNotIn("subtema", item)
        self.assertEqual(
            set(item["subtemas"]),
            {"proteção de dados de menores", "segurança digital infantil"},
        )

    def test_detalhe_retorna_todos_os_subtemas(self):
        resp = self.client.get(f"/api/proposicoes/{self.ID_MULTIPLAS}")
        self.assertEqual(resp.status_code, 200)
        prop = resp.get_json()["proposicao"]

        self.assertIn("subtemas", prop)
        self.assertNotIn("subtema", prop)
        self.assertEqual(
            set(prop["subtemas"]),
            {"proteção de dados de menores", "segurança digital infantil"},
        )

    def test_proposicao_sem_categoria_retorna_lista_vazia(self):
        resp = self.client.get(f"/api/proposicoes/{self.ID_SEM_CATEGORIA}")
        self.assertEqual(resp.status_code, 200)
        prop = resp.get_json()["proposicao"]

        self.assertEqual(prop["subtemas"], [])


if __name__ == "__main__":
    unittest.main()
