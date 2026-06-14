from datetime import datetime
from .. import db


# Tabela associativa many-to-many entre Proposicao e Categoria
proposicao_categoria = db.Table(
    'proposicao_categoria',
    db.Column('proposicao_id', db.Integer, db.ForeignKey('proposicoes.id'), primary_key=True),
    db.Column('categoria_id', db.Integer, db.ForeignKey('categorias.id'), primary_key=True),
)


class Categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.Text)
    cor = db.Column(db.String(7))  # hex color, ex: '#3B82F6'
    icone = db.Column(db.String(50))  # nome do ícone, ex: 'saude', 'educacao'
    ativa = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    proposicoes = db.relationship(
        'Proposicao',
        secondary=proposicao_categoria,
        back_populates='categorias',
        lazy='dynamic',
    )

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'cor': self.cor,
            'icone': self.icone,
            'ativa': self.ativa,
            'total_proposicoes': self.proposicoes.count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def to_dict_simple(self):
        """Versão simplificada para uso em relacionamentos."""
        return {
            'id': self.id,
            'nome': self.nome,
            'cor': self.cor,
            'icone': self.icone,
        }

    def __repr__(self):
        return f'<Categoria {self.id} - {self.nome}>'