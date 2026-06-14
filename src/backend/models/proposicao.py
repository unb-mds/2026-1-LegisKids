from datetime import datetime
from .. import db
from .categoria import proposicao_categoria


class Proposicao(db.Model):
    __tablename__ = 'proposicoes'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(500), nullable=False)
    ementa = db.Column(db.Text)
    tipo = db.Column(db.String(50))           # 'PL', 'PEC', 'MPV', etc.
    numero = db.Column(db.Integer)
    ano = db.Column(db.Integer)
    status = db.Column(db.String(100))
    situacao = db.Column(db.String(200))
    data_apresentacao = db.Column(db.Date)
    url_api = db.Column(db.String(300), unique=True)
    url_inteiro_teor = db.Column(db.String(300))
    keywords = db.Column(db.Text)             # tags separadas por vírgula
    id_externo = db.Column(db.Integer, unique=True)  # ID na API da Câmara
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Chave estrangeira
    autor_id = db.Column(db.Integer, db.ForeignKey('autores.id'), nullable=True)

    # Relacionamentos
    autor = db.relationship('Autor', back_populates='proposicoes')
    categorias = db.relationship(
        'Categoria',
        secondary=proposicao_categoria,
        back_populates='proposicoes',
        lazy='joined',
    )
    favoritos = db.relationship('Favorito', back_populates='proposicao', lazy='dynamic')

    # Validações
    @staticmethod
    def _validate_tipo(tipo):
        tipos_validos = {'PL', 'PEC', 'MPV', 'PDC', 'PLP', 'REQ', 'RIC', 'MSC', 'INC', 'PRC'}
        if tipo and tipo.upper() not in tipos_validos:
            raise ValueError(f"Tipo inválido: '{tipo}'. Válidos: {tipos_validos}")
        return tipo.upper() if tipo else tipo

    def __init__(self, **kwargs):
        if 'tipo' in kwargs:
            kwargs['tipo'] = self._validate_tipo(kwargs['tipo'])
        super().__init__(**kwargs)

    @property
    def sigla(self):
        """Retorna a sigla completa, ex: 'PL 1234/2023'."""
        if self.tipo and self.numero and self.ano:
            return f"{self.tipo} {self.numero}/{self.ano}"
        return self.titulo

    def to_dict(self, include_autor=True, include_categorias=True):
        data = {
            'id': self.id,
            'titulo': self.titulo,
            'sigla': self.sigla,
            'ementa': self.ementa,
            'tipo': self.tipo,
            'numero': self.numero,
            'ano': self.ano,
            'status': self.status,
            'situacao': self.situacao,
            'data_apresentacao': self.data_apresentacao.isoformat() if self.data_apresentacao else None,
            'url_api': self.url_api,
            'url_inteiro_teor': self.url_inteiro_teor,
            'keywords': self.keywords.split(',') if self.keywords else [],
            'id_externo': self.id_externo,
            'total_favoritos': self.favoritos.count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_autor:
            data['autor'] = self.autor.to_dict_simple() if self.autor else None

        if include_categorias:
            data['categorias'] = [c.to_dict_simple() for c in self.categorias]

        return data

    def __repr__(self):
        return f'<Proposicao {self.id} - {self.sigla}>'