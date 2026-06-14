from datetime import datetime
from .. import db


class Autor(db.Model):
    __tablename__ = 'autores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    partido = db.Column(db.String(50))
    uf = db.Column(db.String(2))
    tipo = db.Column(db.String(50))  # 'deputado', 'senador', 'comissao', etc.
    id_externo = db.Column(db.Integer, unique=True)  # ID na API da Câmara
    url_foto = db.Column(db.String(300))
    email = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    proposicoes = db.relationship('Proposicao', back_populates='autor', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'partido': self.partido,
            'uf': self.uf,
            'tipo': self.tipo,
            'id_externo': self.id_externo,
            'url_foto': self.url_foto,
            'email': self.email,
            'total_proposicoes': self.proposicoes.count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def to_dict_simple(self):
        """Versão simplificada para uso em relacionamentos (evita recursão)."""
        return {
            'id': self.id,
            'nome': self.nome,
            'partido': self.partido,
            'uf': self.uf,
            'tipo': self.tipo,
            'url_foto': self.url_foto,
        }

    def __repr__(self):
        return f'<Autor {self.id} - {self.nome} ({self.partido}/{self.uf})>'