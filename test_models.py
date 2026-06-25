import sys, os, json
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.backend.app import app
from src.backend.database import db
from src.backend.models import Partido, Proposicao, Usuario, Favorito
from datetime import date

with app.app_context():
    db.create_all()

    partido = Partido(sigla='MDB', nome='Movimento Democratico Brasileiro')
    db.session.add(partido)
    db.session.flush()

    prop = Proposicao(
        sigla_tipo='PEC',
        numero=8888,
        ano=2025,
        ementa='Teste to_dict',
        data_apresentacao=date(2025, 1, 1),
        descricao_situacao='Em tramitacao',
        sigla_partido='MDB',
        partido=partido,
    )
    db.session.add(prop)

    usuario = Usuario(
        nome='Teste Dict',
        email='dict@exemplo.com',
        google_id='google-dict-1',
    )
    db.session.add(usuario)
    db.session.commit()

    fav = Favorito(usuario=usuario, proposicao=prop)
    db.session.add(fav)
    db.session.commit()

    print('=== REPR ===')
    print(partido)
    print(prop)
    print(usuario)
    print(fav)

    print('\n=== TO_DICT ===')
    print('Partido:', json.dumps(partido.to_dict(), indent=2, ensure_ascii=False))
    print('Proposicao:', json.dumps(prop.to_dict(), indent=2, ensure_ascii=False))
    print('Usuario:', json.dumps(usuario.to_dict(), indent=2, ensure_ascii=False))
    print('Favorito:', json.dumps(fav.to_dict(), indent=2, ensure_ascii=False))

    print('\nOK Todos os to_dict() funcionando!')
