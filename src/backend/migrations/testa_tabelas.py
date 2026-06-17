"""
Testa a criação e integridade das tabelas do banco de dados,
a partir das definições em models.py (SQLAlchemy).
Execute na raiz do projeto com o venv ativado:

    python src/backend/migrations/testa_models.py
"""

import sys
import os
from datetime import date, datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from sqlalchemy.exc import IntegrityError

from src.backend.app import app, db
from src.backend.models import (
    Categoria,
    Partido,
    Proposicao,
    Tramitacao,
    Usuario,
    Favorito,
    HistoricoConsulta,
    RequisicaoApi,
)

TABELAS_ESPERADAS = {
    "categorias",
    "proposicao_categoria",
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


def checar_tabela_associativa(conn):
    print("\n── 2. Verificando tabela associativa proposicao_categoria ─")
    colunas = [c["name"] for c in db.engine.dialect.get_columns(conn, "proposicao_categoria")]
    if "proposicao_id" in colunas and "categoria_id" in colunas:
        ok("Tabela 'proposicao_categoria' possui as colunas esperadas")
    else:
        erro("Tabela 'proposicao_categoria' NÃO possui as colunas esperadas")


def checar_constraint_status():
    print("\n── 3. Testando CheckConstraint de descricao_situacao ───")

    prop_invalida = Proposicao(
        id=99998,
        sigla_tipo="PL",
        numero=2,
        ano=2024,
        ementa="Proposição com status inválido para teste de constraint.",
        data_apresentacao=date(2024, 1, 1),
        descricao_situacao="Status Inexistente",
        sigla_partido="XX",
    )
    db.session.add(prop_invalida)
    try:
        db.session.flush()
        erro("CheckConstraint NÃO bloqueou status inválido")
        db.session.rollback()
    except IntegrityError:
        ok("CheckConstraint bloqueou status inválido corretamente")
        db.session.rollback()


def checar_insercao():
    print("\n── 4. Testando inserção de dados ───────────────────────")

    # Categoria
    categoria = Categoria(
        nome="Proteção de Dados Teste",
        descricao="Categoria de teste para validação do banco.",
        cor="#FF0000",
        icone="shield",
        ativa=True,
    )
    db.session.add(categoria)
    db.session.flush()
    ok("Inseriu categoria")

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
    )
    db.session.add(prop)
    db.session.flush()
    ok("Inseriu proposição")

    # Associação N:N proposicao <-> categoria
    prop.categorias.append(categoria)
    db.session.flush()
    ok("Associou proposição à categoria (N:N)")

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
    print("\n── 5. Testando consultas e relacionamentos ──────────────")

    prop = Proposicao.query.get(99999)
    if prop:
        ok(f"Consultou proposição: {prop}")
    else:
        erro("Não encontrou proposição inserida")
        return

    if prop.partido and prop.partido.sigla == "XX":
        ok(f"Relacionamento partido OK: {prop.partido.sigla}")
    else:
        erro("Relacionamento partido falhou")

    if prop.categorias.count() == 1 and prop.categorias.first().nome == "Proteção de Dados Teste":
        ok("Relacionamento N:N categorias (via proposição) OK")
    else:
        erro("Relacionamento N:N categorias (via proposição) falhou")

    categoria = Categoria.query.filter_by(nome="Proteção de Dados Teste").first()
    if categoria and categoria.proposicoes.count() == 1:
        ok("Relacionamento N:N proposições (via categoria) OK")
    else:
        erro("Relacionamento N:N proposições (via categoria) falhou")

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


def checar_to_dict():
    print("\n── 6. Testando métodos to_dict() ────────────────────────")

    prop = Proposicao.query.get(99999)
    dados = prop.to_dict()
    if dados.get("id") == 99999 and "categorias" in dados and "partido" in dados:
        ok("Proposicao.to_dict() OK")
    else:
        erro("Proposicao.to_dict() retornou estrutura inesperada")

    categoria = Categoria.query.filter_by(nome="Proteção de Dados Teste").first()
    if categoria.to_dict().get("nome") == "Proteção de Dados Teste":
        ok("Categoria.to_dict() OK")
    else:
        erro("Categoria.to_dict() retornou estrutura inesperada")

    usuario = Usuario.query.filter_by(email="teste@legiskids.com").first()
    if usuario.to_dict().get("email") == "teste@legiskids.com":
        ok("Usuario.to_dict() OK")
    else:
        erro("Usuario.to_dict() retornou estrutura inesperada")


def limpar():
    print("\n── 7. Limpando dados de teste ──────────────────────────")
    db.session.rollback()
    ok("Dados de teste descartados (rollback)")


with app.app_context():
    print("═" * 55)
    print("  LegisKids — Teste de models (SQLAlchemy)")
    print("═" * 55)

    db.create_all()
    ok("Conexão com o banco estabelecida")

    with db.engine.connect() as conn:
        checar_tabelas(conn)
        checar_tabela_associativa(conn)

    try:
        checar_constraint_status()
        checar_insercao()
        checar_consulta()
        checar_to_dict()
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