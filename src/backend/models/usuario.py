from datetime import datetime
import re
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    senha_hash = db.Column(db.String(256), nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)
    papel = db.Column(db.String(20), default='usuario', nullable=False)  # 'usuario', 'admin'
    ultimo_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    favoritos = db.relationship('Favorito', back_populates='usuario', lazy='dynamic',
                                cascade='all, delete-orphan')

    # ---------- Propriedades e métodos de senha ----------

    @property
    def senha(self):
        raise AttributeError('A senha não pode ser lida diretamente.')

    @senha.setter
    def senha(self, senha_plain):
        self._validate_senha(senha_plain)
        self.senha_hash = generate_password_hash(senha_plain)

    def verificar_senha(self, senha_plain):
        return check_password_hash(self.senha_hash, senha_plain)

    # ---------- Validações ----------

    @staticmethod
    def _validate_email(email):
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        if not re.match(padrao, email):
            raise ValueError(f"E-mail inválido: '{email}'")
        return email.lower().strip()

    @staticmethod
    def _validate_senha(senha):
        if len(senha) < 8:
            raise ValueError('A senha deve ter pelo menos 8 caracteres.')
        if not re.search(r'[A-Z]', senha):
            raise ValueError('A senha deve conter pelo menos uma letra maiúscula.')
        if not re.search(r'\d', senha):
            raise ValueError('A senha deve conter pelo menos um número.')

    @staticmethod
    def _validate_papel(papel):
        papeis_validos = {'usuario', 'admin'}
        if papel not in papeis_validos:
            raise ValueError(f"Papel inválido: '{papel}'. Válidos: {papeis_validos}")
        return papel

    def __init__(self, **kwargs):
        # Extrai a senha antes de chamar super().__init__
        senha_plain = kwargs.pop('senha', None)

        if 'email' in kwargs:
            kwargs['email'] = self._validate_email(kwargs['email'])
        if 'papel' in kwargs:
            kwargs['papel'] = self._validate_papel(kwargs['papel'])

        super().__init__(**kwargs)

        if senha_plain:
            self.senha = senha_plain

    # ---------- Métodos auxiliares ----------

    @property
    def is_admin(self):
        return self.papel == 'admin'

    def registrar_login(self):
        self.ultimo_login = datetime.utcnow()
        db.session.commit()

    def to_dict(self, include_favoritos=False):
        data = {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'ativo': self.ativo,
            'papel': self.papel,
            'total_favoritos': self.favoritos.count(),
            'ultimo_login': self.ultimo_login.isoformat() if self.ultimo_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_favoritos:
            data['favoritos'] = [f.to_dict(include_usuario=False) for f in self.favoritos]

        return data

    def to_dict_public(self):
        """Versão pública sem dados sensíveis."""
        return {
            'id': self.id,
            'nome': self.nome,
            'papel': self.papel,
        }

    def __repr__(self):
        return f'<Usuario {self.id} - {self.email} [{self.papel}]>'