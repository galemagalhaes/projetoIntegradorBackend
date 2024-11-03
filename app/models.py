from flask_sqlalchemy import SQLAlchemy

DATABASE_URI = 'postgresql://postgres:fq6eGrDwj2k9L2mq@horrifyingly-beefy-accentor.data-1.use1.tembo.io:5432/postgres'
TRACK_MODIFICATIONS = False
# Inicialize o SQLAlchemy (não configuramos a URI aqui ainda)
db = SQLAlchemy()

# Modelo de Cliente
class Client(db.Model):
    __tablename__ = "clientes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cpf = db.Column(db.String, nullable=False)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    telefone = db.Column(db.String, nullable=True)

    def __init__(self, cpf, nome, email, telefone):
        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.telefone = telefone

# Modelo de Venda
class Sale(db.Model):
    __tablename__ = "vendas"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    data = db.Column(db.String, nullable=False)
    valor_venda = db.Column(db.Float, nullable=False)
    status_venda = db.Column(db.Boolean, default=False)

    def __init__(self, cliente_id, data, valor_venda, status_venda=False):
        self.cliente_id = cliente_id
        self.data = data
        self.valor_venda = valor_venda
        self.status_venda = status_venda

# Modelo de Usuario
class User(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    senha = db.Column(db.String, nullable=False)

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

    def to_dict(self):
        return {
        "id": self.id,
        "nome": self.nome,
        "email": self.email
            }