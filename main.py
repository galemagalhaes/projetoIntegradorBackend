from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Float, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

db = create_engine("postgresql://postgres:fq6eGrDwj2k9L2mq@horrifyingly-beefy-accentor.data-1.use1.tembo.io:5432/postgres")

Session = sessionmaker(bind=db) 
session = Session()

Base = declarative_base()

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    cpf = Column("cpf", String)
    nome = Column("nome", String)
    email = Column("email", String)
    telefone = Column("telefone", String)

def __init__(self, cpf, nome, email, telefone):
    self.cpf = cpf
    self.nome = nome
    self.email = email
    self.telefone = telefone
    

class Venda(Base):
    __tablename__ = "vendas"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    cliente = Column("cliente", ForeignKey("clientes.id"))
    data = Column("data", String)
    valor_venda = Column("valor_venda", Float)
    status_venda = Column("status_venda", Boolean)

def __init__(self, cliente, data, valor_venda, status_venda=False):
    self.cliente = cliente
    self.data = data
    self.valor_venda = valor_venda
    self.status_venda = status_venda


class Usuario(Base):
    __tablename__ = "usuario"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String)
    senha = Column("senha", String)

def __init__(self, nome, email, senha):
    self.nome = nome
    self.email = email
    self.senha = senha

Base.metadata.create_all(bind=db) 

#cliente = Cliente(cpf="919.199.640-61", nome="Fulano Pires Cavalcante", email="fulano@email.com", telefone="11 947897589")
#session.add(cliente)
#session.commit()


#lista_clientes = session.query(Cliente).all()
#print(lista_clientes[0])
