"""
Modelos SQLAlchemy — LegisKids
Espelham exatamente o schema definido em create_tables.sql
e a documentação de arquitetura do projeto.
"""

from datetime import datetime
from src.backend.database import db


# ── Partido ───────────────────────────────────────────────────────────────────
class Partido(db.Model):
    __tablename__ = "partidos"

    id    = db.Column(db.Integer, primary_key=True)   # ID oficial da API da Câmara
    sigla = db.Column(db.String(20),  nullable=False, unique=True)
    nome  = db.Column(db.String(150), nullable=False)

    proposicoes = db.relationship("Proposicao", back_populates="partido", lazy="dynamic")

    def __repr__(self):
        return f"<Partido {self.sigla}>"


# ── Proposição ────────────────────────────────────────────────────────────────
class Proposicao(db.Model):
    __tablename__ = "proposicoes"
    __table_args__ = (
        db.UniqueConstraint("sigla_tipo", "numero", "ano"),
    )

    id                 = db.Column(db.Integer,      primary_key=True)  # ID oficial da API
    sigla_tipo         = db.Column(db.String(20),   nullable=False)
    numero             = db.Column(db.Integer,       nullable=False)
    ano                = db.Column(db.Integer,       nullable=False)
    ementa             = db.Column(db.Text,          nullable=False)
    data_apresentacao  = db.Column(db.Date,          nullable=False)
    descricao_situacao = db.Column(db.String(150),   nullable=False)
    partido_id         = db.Column(db.Integer,       db.ForeignKey("partidos.id", ondelete="SET NULL"), nullable=True)
    sigla_partido      = db.Column(db.String(20),    nullable=False)
    categoria          = db.Column(db.String(100))   # classificação temática derivada das palavras-chave
    data_coleta        = db.Column(db.DateTime,      nullable=False, default=datetime.utcnow)

    partido      = db.relationship("Partido",     back_populates="proposicoes")
    tramitacoes  = db.relationship("Tramitacao",  back_populates="proposicao", lazy="dynamic", cascade="all, delete-orphan")
    favoritos    = db.relationship("Favorito",    back_populates="proposicao", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Proposicao {self.sigla_tipo} {self.numero}/{self.ano}>"


# ── Tramitação ────────────────────────────────────────────────────────────────
class Tramitacao(db.Model):
    __tablename__ = "tramitacoes"

    id                   = db.Column(db.Integer,   primary_key=True)
    proposicao_id        = db.Column(db.Integer,   db.ForeignKey("proposicoes.id", ondelete="CASCADE"), nullable=False)
    data_hora            = db.Column(db.DateTime,  nullable=False)
    id_situacao          = db.Column(db.Integer,   nullable=False)
    descricao_situacao   = db.Column(db.String(150), nullable=False)
    descricao_tramitacao = db.Column(db.Text,      nullable=False)
    sigla_orgao          = db.Column(db.String(50), nullable=False)

    proposicao = db.relationship("Proposicao", back_populates="tramitacoes")

    def __repr__(self):
        return f"<Tramitacao prop={self.proposicao_id} {self.data_hora}>"


# ── Usuário ───────────────────────────────────────────────────────────────────
class Usuario(db.Model):
    __tablename__ = "usuarios"

    id           = db.Column(db.Integer,    primary_key=True)
    nome         = db.Column(db.String(100), nullable=False)
    email        = db.Column(db.String(150), nullable=False, unique=True)
    google_id    = db.Column(db.String(100), nullable=False, unique=True)
    data_criacao = db.Column(db.DateTime,   nullable=False, default=datetime.utcnow)

    favoritos           = db.relationship("Favorito",          back_populates="usuario", lazy="dynamic", cascade="all, delete-orphan")
    historico_consultas = db.relationship("HistoricoConsulta", back_populates="usuario", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Usuario {self.email}>"


# ── Favorito ──────────────────────────────────────────────────────────────────
class Favorito(db.Model):
    __tablename__ = "favoritos"
    __table_args__ = (
        db.UniqueConstraint("usuario_id", "proposicao_id"),
    )

    id            = db.Column(db.Integer,  primary_key=True)
    usuario_id    = db.Column(db.Integer,  db.ForeignKey("usuarios.id",    ondelete="CASCADE"), nullable=False)
    proposicao_id = db.Column(db.Integer,  db.ForeignKey("proposicoes.id", ondelete="CASCADE"), nullable=False)
    data_favorito = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    usuario    = db.relationship("Usuario",    back_populates="favoritos")
    proposicao = db.relationship("Proposicao", back_populates="favoritos")

    def __repr__(self):
        return f"<Favorito user={self.usuario_id} prop={self.proposicao_id}>"


# ── Histórico de Consultas ────────────────────────────────────────────────────
class HistoricoConsulta(db.Model):
    __tablename__ = "historico_consultas"

    id            = db.Column(db.Integer,    primary_key=True)
    usuario_id    = db.Column(db.Integer,    db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    termo_busca   = db.Column(db.String(255), nullable=False)
    data_consulta = db.Column(db.DateTime,   nullable=False, default=datetime.utcnow)

    usuario = db.relationship("Usuario", back_populates="historico_consultas")

    def __repr__(self):
        return f"<HistoricoConsulta user={self.usuario_id} '{self.termo_busca}'>"


# ── Requisições API ───────────────────────────────────────────────────────────
class RequisicaoApi(db.Model):
    __tablename__ = "requisicoes_api"

    id                   = db.Column(db.Integer,    primary_key=True)
    endpoint             = db.Column(db.String(255), nullable=False)
    data_requisicao      = db.Column(db.DateTime,   nullable=False, default=datetime.utcnow)
    quantidade_registros = db.Column(db.Integer,    nullable=False)
    status_requisicao    = db.Column(db.String(50), nullable=False)
    tempo_execucao_ms    = db.Column(db.Integer)    # nullable — monitoramento opcional

    def __repr__(self):
        return f"<RequisicaoApi {self.endpoint} {self.status_requisicao}>"