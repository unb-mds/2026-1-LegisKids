from datetime import datetime
from .. import db


class Favorito(db.Model):
    __tablename__ = 'favoritos'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    proposicao_id = db.Column(db.Integer, db.ForeignKey('proposicoes.id'), nullable=False)
    nota = db.Column(db.Text)               # anotação pessoal do usuário
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Garante que um usuário não favorite a mesma proposição duas vezes
    __table_args__ = (
        db.UniqueConstraint('usuario_id', 'proposicao_id', name='uq_favorito_usuario_proposicao'),
    )

    # Relacionamentos
    usuario = db.relationship('Usuario', back_populates='favoritos')
    proposicao = db.relationship('Proposicao', back_populates='favoritos')

    def to_dict(self, include_usuario=True, include_proposicao=True):
        data = {
            'id': self.id,
            'nota': self.nota,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

        if include_usuario:
            data['usuario'] = self.usuario.to_dict_public() if self.usuario else None

        if include_proposicao:
            data['proposicao'] = self.proposicao.to_dict(
                include_autor=True, include_categorias=True
            ) if self.proposicao else None
        else:
            data['proposicao_id'] = self.proposicao_id

        return data

    @classmethod
    def existe(cls, usuario_id, proposicao_id):
        """Verifica se o favorito já existe sem lançar erro."""
        return cls.query.filter_by(
            usuario_id=usuario_id,
            proposicao_id=proposicao_id
        ).first() is not None

    def __repr__(self):
        return f'<Favorito {self.id} - Usuario {self.usuario_id} → Proposicao {self.proposicao_id}>'