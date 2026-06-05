"""
Testa a criação e integridade das tabelas do banco de dados.
Execute na raiz do projeto com o venv ativado:

    python src/backend/migrations/test_tables.py
"""

import sys
import os
from datetime import date, datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from src.backend.app import app, db
from src.backend.models import (
    Partido,
    Proposicao,
    Tramitacao,
    Usuario,
    Favorito,
    HistoricoConsulta,
    RequisicaoApi,
)

TABELAS_ESPERADAS = {
    "partidos",
    "proposicoes",
    "tramitacoes",
    "usuarios",
    "favoritos",
    "historico_consultas",
    "requisicoes_api",
}

erros = []


def ok(msg):
    print(f"  ✅ {msg}")


def erro(msg):
    print(f"  ❌ {msg}")
    erros.append(msg)


def checar_tabelas(conn):
    print("\n── 1. Verificando tabelas ───────────────────────────────")
    tabelas = db.engine.dialect.get_table_names(conn)
    for t in sorted(TABELAS_ESPERADAS):
        if t in tabelas:
            ok(f"Tabela '{t}' existe")
        else:
            erro(f"Tabela '{t}' NÃO encontrada")


def checar_campo_categoria(conn):
    print("\n── 2. Verificando campo 'categoria' em proposicoes ─────")
    colunas = [c["name"] for c in db.engine.dialect.get_columns(conn, "proposicoes")]
    if "categoria" in colunas:
        ok("Campo 'categoria' existe em 'proposicoes'")
    else:
        erro("Campo 'categoria' NÃO encontrado em 'proposicoes'")


def checar_insercao():
    print("\n── 3. Testando inserção de dados ───────────────────────")

    # Partido
    partido = Partido(id=99999, sigla="XX", nome="Partido Teste")
    db.session.add(partido)
    db.session.flush()
    ok("Inseriu partido")

    # Proposição
    prop = Proposicao(
        id=99999,
        sigla_tipo="PL",
        numero=1,
        ano=2024,
        ementa="Proposição de teste para validação do banco.",
        data_apresentacao=date(2024, 1, 1),
        descricao_situacao="Em tramitação",
        partido_id=99999,
        sigla_partido="XX",
        categoria="proteção de dados",
    )
    db.session.add(prop)
    db.session.flush()
    ok("Inseriu proposição com categoria")

    # Tramitação
    tram = Tramitacao(
        proposicao_id=99999,
        data_hora=datetime.utcnow(),
        id_situacao=1,
        descricao_situacao="Em tramitação",
        descricao_tramitacao="Enviado à comissão.",
        sigla_orgao="CCJC",
    )
    db.session.add(tram)
    db.session.flush()
    ok("Inseriu tramitação")

    # Usuário
    usuario = Usuario(
        nome="Usuário Teste",
        email="teste@legiskids.com",
        google_id="google_teste_123",
    )
    db.session.add(usuario)
    db.session.flush()
    ok("Inseriu usuário")

    # Favorito
    fav = Favorito(usuario_id=usuario.id, proposicao_id=99999)
    db.session.add(fav)
    db.session.flush()
    ok("Inseriu favorito")

    # Histórico
    hist = HistoricoConsulta(usuario_id=usuario.id, termo_busca="cyberbullying")
    db.session.add(hist)
    db.session.flush()
    ok("Inseriu histórico de consulta")

    # Requisição API
    req = RequisicaoApi(
        endpoint="/proposicoes",
        quantidade_registros=10,
        status_requisicao="sucesso",
        tempo_execucao_ms=320,
    )
    db.session.add(req)
    db.session.flush()
    ok("Inseriu requisição de API")


def checar_consulta():
    print("\n── 4. Testando consultas e relacionamentos ──────────────")

    prop = Proposicao.query.get(99999)
    if prop:
        ok(f"Consultou proposição: {prop}")
    else:
        erro("Não encontrou proposição inserida")
        return

    if prop.categoria == "proteção de dados":
        ok(f"Campo categoria correto: '{prop.categoria}'")
    else:
        erro(f"Campo categoria incorreto: '{prop.categoria}'")

    if prop.partido and prop.partido.sigla == "XX":
        ok(f"Relacionamento partido OK: {prop.partido.sigla}")
    else:
        erro("Relacionamento partido falhou")

    if prop.tramitacoes.count() == 1:
        ok("Relacionamento tramitações OK")
    else:
        erro("Relacionamento tramitações falhou")

    usuario = Usuario.query.filter_by(email="teste@legiskids.com").first()
    if usuario and usuario.favoritos.count() == 1:
        ok("Relacionamento favoritos OK")
    else:
        erro("Relacionamento favoritos falhou")

    if usuario and usuario.historico_consultas.count() == 1:
        ok("Relacionamento histórico OK")
    else:
        erro("Relacionamento histórico falhou")


def limpar():
    print("\n── 5. Limpando dados de teste ──────────────────────────")
    db.session.rollback()
    ok("Dados de teste descartados (rollback)")


with app.app_context():
    print("═" * 55)
    print("  LegisKids — Teste de tabelas do banco de dados")
    print("═" * 55)

    db.create_all()
    ok("Conexão com o banco estabelecida")

    with db.engine.connect() as conn:
        checar_tabelas(conn)
        checar_campo_categoria(conn)

    try:
        checar_insercao()
        checar_consulta()
    finally:
        limpar()

    print("\n" + "═" * 55)
    if erros:
        print(f"  RESULTADO: {len(erros)} erro(s) encontrado(s):")
        for e in erros:
            print(f"    • {e}")
        sys.exit(1)
    else:
        print("  RESULTADO: todos os testes passaram ✅")
    print("═" * 55)