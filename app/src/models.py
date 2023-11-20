from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.engine.url import URL

# Configuração da URL do PostgreSQL
db_url = URL.create(
    drivername='postgresql+psycopg2',
    username='admin',
    password='admin',
    host='localhost',
    database='postgres',
    port=5432
)

# Configuração da conexão com o PostgreSQL
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)

Base = declarative_base()

class Item(Base):
    __tablename__ = 'itens'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    peso = Column(Float)
    medida_x = Column(Float)
    medida_y = Column(Float)
    medida_z = Column(Float)
    # Adicione outros campos conforme necessário

class Caminhao(Base):
    __tablename__ = 'caminhoes'
    id = Column(Integer, primary_key=True)
    modelo = Column(String, nullable=False)
    capacidade_carga = Column(Float, nullable=False)
    localizacao = Column(String, nullable=False)  # Informação de localização do caminhão
    galpao_origem_id = Column(Integer, ForeignKey('galpoes.id'))
    galpao_origem = relationship("Galpao", foreign_keys=[galpao_origem_id])
    galpao_destino_id = Column(Integer, ForeignKey('galpoes.id'))
    galpao_destino = relationship("Galpao", foreign_keys=[galpao_destino_id])
    status = Column(String, nullable=False)  # Status do caminhão
    # Adicione outros campos conforme necessário

class Galpao(Base):
    __tablename__ = 'galpoes'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cidade = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    cep = Column(String, nullable=False)
    numero = Column(String, nullable=False)
    complemento = Column(String, nullable=False)
    capacidade_armazenamento = Column(Float, nullable=False)
    # Adicione outros campos conforme necessário

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    cpf = Column(String, nullable=False)
    email = Column(String)
    cidade = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    cep = Column(String, nullable=False)
    numero = Column(String, nullable=False)
    complemento = Column(String, nullable=False)
    # Adicione outros campos conforme necessário

class Pedido(Base):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key=True)
    cliente_origem_id = Column(Integer, ForeignKey('clientes.id'))
    cliente_origem = relationship("Cliente", back_populates="pedidos")
    cliente_destino_id = Column(Integer, ForeignKey('clientes.id'))
    cliente_destino = relationship("Cliente", back_populates="pedidos")
    item_id = Column(Integer, ForeignKey('itens.id'))
    item = relationship("Item", back_populates="pedidos")
    quantidade = Column(Integer)
    status = Column(String, nullable=False)  # Status do pedido
    caminhao_id = Column(Integer, ForeignKey('caminhao.id'))
    caminhao = relationship("Caminhao", back_populates="pedidos")
    # Adicione outros campos conforme necessário

# Adicionando a relação entre Cliente e Pedido
Cliente.pedidos = relationship("Pedido", order_by=Pedido.id, back_populates="cliente")

# Crie as tabelas no banco de dados
Base.metadata.create_all(engine)

