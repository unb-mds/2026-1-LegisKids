"""
Testes de integração para models.py — cobre to_dict() e relacionamentos
(Partido, Proposicao, Usuario, Favorito) contra um Postgres real.
Execução: python -m unittest tests.integration.test_models
Pré-requisito: DATABASE_URL configurada no ambiente e migrations aplicadas.
"""
import os
import unittest
from datetime import date

os.environ.setdefault("FLASK_ENV", "testing")


def _get_app():
    from src.backend.app import app
    return app


class TestToDictERelacionamentos(unittest.TestCase):
    """to_dict() de Partido/Proposicao/Usuario/Favorito serializa os campos e relações corretamente."""

    ID_PROPOSICAO = 9999900

    @classmethod
    def setUpClass(cls):
        cls.app = _get_app()
        cls.ctx = cls.app.app_context()
        cls.ctx.push()

        from src.backend.database import db
        from src.backend.models import Favorito, Partido, Proposicao, Usuario
        cls.db = db

        cls.partido = Partido(sigla="ZZZTEST", nome="Partido de Teste")
        db.session.add(cls.partido)
        db.session.flush()

        cls.proposicao = Proposicao(
            id=cls.ID_PROPOSICAO,
            sigla_tipo="PEC",
            numero=8888,
            ano=2099,
            ementa="Teste to_dict",
            data_apresentacao=date(2099, 1, 1),
            descricao_situacao="Em tramitação",
            sigla_partido="ZZZTEST",
            partido=cls.partido,
        )
        db.session.add(cls.proposicao)

        cls.usuario = Usuario(
            nome="Teste Dict",
            email="dict-teste@exemplo.com",
            google_id="google-dict-teste-1",
        )
        db.session.add(cls.usuario)
        db.session.commit()

        cls.favorito = Favorito(usuario=cls.usuario, proposicao=cls.proposicao)
        db.session.add(cls.favorito)
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        from src.backend.models import Favorito, Partido, Proposicao, Usuario
        cls.db.session.query(Favorito).filter(Favorito.id == cls.favorito.id).delete()
        cls.db.session.query(Proposicao).filter(Proposicao.id == cls.ID_PROPOSICAO).delete()
        cls.db.session.query(Usuario).filter(Usuario.id == cls.usuario.id).delete()
        cls.db.session.query(Partido).filter(Partido.id == cls.partido.id).delete()
        cls.db.session.commit()
        cls.ctx.pop()

    def test_partido_to_dict(self):
        self.assertEqual(
            self.partido.to_dict(),
            {"id": self.partido.id, "sigla": "ZZZTEST", "nome": "Partido de Teste"},
        )

    def test_proposicao_to_dict_inclui_partido_aninhado(self):
        dado = self.proposicao.to_dict()
        self.assertEqual(dado["id"], self.ID_PROPOSICAO)
        self.assertEqual(dado["sigla_tipo"], "PEC")
        self.assertEqual(dado["data_apresentacao"], "2099-01-01")
        self.assertEqual(dado["partido"], self.partido.to_dict())
        self.assertEqual(dado["categorias"], [])

    def test_usuario_to_dict(self):
        dado = self.usuario.to_dict()
        self.assertEqual(dado["email"], "dict-teste@exemplo.com")
        self.assertEqual(dado["google_id"], "google-dict-teste-1")
        self.assertIsNotNone(dado["data_criacao"])

    def test_favorito_to_dict_referencia_usuario_e_proposicao(self):
        dado = self.favorito.to_dict()
        self.assertEqual(dado["usuario_id"], self.usuario.id)
        self.assertEqual(dado["proposicao_id"], self.ID_PROPOSICAO)


if __name__ == "__main__":
    unittest.main()
