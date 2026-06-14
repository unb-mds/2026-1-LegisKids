import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.backend.app import app
from src.backend.database import db
from src.backend.models import Partido, Proposicao, Tramitacao, Usuario, Favorito, HistoricoConsulta, RequisicaoApi

with app.app_context():
    db.create_all()

    partido = Partido(id=1, sigla='PT', nome='Partido dos Trabalhadores')
    db.session.add(partido)

    from datetime import date, datetime
    prop = Proposicao(
        id=1,
        sigla_tipo='PL',
        numero=1234,
        ano=2024,
        ementa='Dispõe sobre saúde pública',
        data_apresentacao=date(2024, 3, 1),
        descricao_situacao='Em tramitação',
        sigla_partido='PT',
        partido=partido,
    )
    db.session.add(prop)

    usuario = Usuario(
        nome='João Cidadão',
        email='joao@exemplo.com',
        google_id='google-123',
    )
    db.session.add(usuario)
    db.session.commit()

    fav = Favorito(usuario=usuario, proposicao=prop)
    db.session.add(fav)
    db.session.commit()

    print(partido)
    print(prop)
    print(usuario)
    print(fav)
    print('\n✅ Todos os relacionamentos funcionando!')