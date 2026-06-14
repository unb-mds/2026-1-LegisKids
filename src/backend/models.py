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

    def to_dict(self):
        return {
            'id': self.id,
            'sigla': self.sigla,
            'nome': self.nome,
        }

# ── Proposição ────────────────────────────────────────────────────────────────
class Proposicao(db.Model):
    __tablename__ = "proposicoes"
    __table_args__ = (
    db.UniqueConstraint("sigla_tipo", "numero", "ano"),
    db.Index('idx_proposicoes_sigla_tipo',         'sigla_tipo'),
    db.Index('idx_proposicoes_descricao_situacao', 'descricao_situacao'),
    db.Index('idx_proposicoes_data_apresentacao',  'data_apresentacao'),
    db.Index('idx_proposicoes_partido_id',         'partido_id'),
    db.Index('idx_proposicoes_categoria',          'categoria'),
    db.Index('idx_proposicoes_ano',                'ano'),
    db.Index('idx_proposicoes_tipo_ano',           'sigla_tipo', 'ano'),
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

    def to_dict(self):
        return {
            'id': self.id,
            'sigla_tipo': self.sigla_tipo,
            'numero': self.numero,
            'ano': self.ano,
            'ementa': self.ementa,
            'data_apresentacao': self.data_apresentacao.isoformat() if self.data_apresentacao else None,
            'descricao_situacao': self.descricao_situacao,
            'sigla_partido': self.sigla_partido,
            'categoria': self.categoria,
            'data_coleta': self.data_coleta.isoformat() if self.data_coleta else None,
            'partido': self.partido.to_dict() if self.partido else None,
        }

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
    
    def to_dict(self):
        return {
            'id': self.id,
            'proposicao_id': self.proposicao_id,
            'data_hora': self.data_hora.isoformat() if self.data_hora else None,
            'id_situacao': self.id_situacao,
            'descricao_situacao': self.descricao_situacao,
            'descricao_tramitacao': self.descricao_tramitacao,
            'sigla_orgao': self.sigla_orgao,
        }


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
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'google_id': self.google_id,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
        }


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

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'proposicao_id': self.proposicao_id,
            'data_favorito': self.data_favorito.isoformat() if self.data_favorito else None,
        }

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

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'termo_busca': self.termo_busca,
            'data_consulta': self.data_consulta.isoformat() if self.data_consulta else None,
        }

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
    
    def to_dict(self):
        return {
            'id': self.id,
            'endpoint': self.endpoint,
            'data_requisicao': self.data_requisicao.isoformat() if self.data_requisicao else None,
            'quantidade_registros': self.quantidade_registros,
            'status_requisicao': self.status_requisicao,
            'tempo_execucao_ms': self.tempo_execucao_ms,
        }