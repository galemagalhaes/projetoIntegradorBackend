from flask_sqlalchemy import SQLAlchemy


TRACK_MODIFICATIONS = False

db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = "clientes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    telefone = db.Column(db.String, nullable=True)

    def __init__(self, cpf, nome, email, telefone):
        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.telefone = telefone

    def to_dict(self):
        return {
            "id": self.id,
            "cpf": self.cpf,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone
        }

class Sale(db.Model):
    __tablename__ = "vendas"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    data = db.Column(db.Date, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    pendente = db.Column(db.Boolean, default=True)

    def __init__(self, cliente_id, data, valor, pendente=True):
        self.cliente_id = cliente_id
        self.data = data
        self.valor = valor
        self.pendente = pendente

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "data": self.data.isoformat() if self.data else None,
            "valor": self.valor,
            "pendente": self.pendente
        }

class User(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True, index=True)
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

class Receita_total_mes(db.Model):
    __tablename__ = "receita_total"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ano = db.Column(db.Integer, nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    receita_total_mes = db.Column(db.Float, nullable=False)

    def __init__(self, ano, mes, receita_total_mes):
        self.ano = ano
        self.mes = mes
        self.receita_total_mes = receita_total_mes

    