from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.engine.url import URL

# BANCO ========================================================
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
    cliente_origem = relationship("Cliente", foreign_keys=[cliente_origem_id])
    cliente_destino_id = Column(Integer, ForeignKey('clientes.id'))
    cliente_destino = relationship("Cliente", foreign_keys=[cliente_destino_id])
    item_id = Column(Integer, ForeignKey('itens.id'))
    item = relationship("Item")
    quantidade = Column(Integer)
    status = Column(String, nullable=False)  # Status do pedido
    caminhao_id = Column(Integer, ForeignKey('caminhoes.id'))
    caminhao = relationship("Caminhao")
    # Adicione outros campos conforme necessário

# Adicionando a relação entre Cliente e Pedido
Cliente.pedidos = relationship("Pedido", order_by=Pedido.id, back_populates="cliente")

# Crie as tabelas no banco de dados
Base.metadata.create_all(engine)

# API ========================================================
class Item(BaseModel):
    id: int
    nome: str
    descricao: str = None
    peso: float
    medida_x: float
    medida_y: float
    medida_z: float
    # Adicione outros campos conforme necessário

class Caminhao(BaseModel):
    id: int
    modelo: str
    capacidade_carga: float
    localizacao: str  # Informação de localização do caminhão
    galpao_origem_id: int
    galpao_destino_id: int
    status: str  # Status do caminhão
    # Adicione outros campos conforme necessário

class Galpao(BaseModel):
    id: int
    nome: str
    cidade: str
    estado: str
    cep: str
    numero: str
    complemento: str
    capacidade_armazenamento: float
    # Adicione outros campos conforme necessário

class Cliente(BaseModel):
    id: int
    nome: str
    telefone: str
    cpf: str
    email: str = None
    cidade: str
    estado: str
    cep: str
    numero: str
    complemento: str
    # Adicione outros campos conforme necessário

class Pedido(BaseModel):
    id: int
    cliente_origem_id: int
    cliente_destino_id: int
    item_id: int
    quantidade: int
    status: str  # Status do pedido
    caminhao_id: int
    # Adicione outros campos conforme necessário

app = FastAPI()

# ========================================================================================
# Dependency to get the database session
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def api_is_running():
    return {"status": "API IS RUNNING"}

# Item CRUD
@app.post("/items/", response_model=Item)
def create_item_api(item: Item, db: Session = Depends(get_db)):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/{item_id}", response_model=Item)
def read_item_api(item_id: int, db: Session = Depends(get_db)):
    return db.query(Item).filter(Item.id == item_id).first()

@app.get("/items/", response_model=List[Item])
def read_items_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Item).offset(skip).limit(limit).all()

@app.put("/items/{item_id}", response_model=Item)
def update_item_api(item_id: int, item: Item, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    for field, value in item.dict().items():
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}", response_model=Item)
def delete_item_api(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    db.delete(db_item)
    db.commit()
    return db_item

# ========================================================================================
# Caminhao CRUD
@app.post("/caminhoes/", response_model=Caminhao)
def create_caminhao_api(caminhao: Caminhao, db: Session = Depends(get_db)):
    db_caminhao = Caminhao(**caminhao.dict())
    db.add(db_caminhao)
    db.commit()
    db.refresh(db_caminhao)
    return db_caminhao

@app.get("/caminhoes/{caminhao_id}", response_model=Caminhao)
def read_caminhao_api(caminhao_id: int, db: Session = Depends(get_db)):
    return db.query(Caminhao).filter(Caminhao.id == caminhao_id).first()

@app.get("/caminhoes/", response_model=List[Caminhao])
def read_caminhoes_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Caminhao).offset(skip).limit(limit).all()

@app.put("/caminhoes/{caminhao_id}", response_model=Caminhao)
def update_caminhao_api(caminhao_id: int, caminhao: Caminhao, db: Session = Depends(get_db)):
    db_caminhao = db.query(Caminhao).filter(Caminhao.id == caminhao_id).first()
    for field, value in caminhao.dict().items():
        setattr(db_caminhao, field, value)
    db.commit()
    db.refresh(db_caminhao)
    return db_caminhao

@app.delete("/caminhoes/{caminhao_id}", response_model=Caminhao)
def delete_caminhao_api(caminhao_id: int, db: Session = Depends(get_db)):
    db_caminhao = db.query(Caminhao).filter(Caminhao.id == caminhao_id).first()
    db.delete(db_caminhao)
    db.commit()
    return db_caminhao

# ========================================================================================
# Galpao CRUD
@app.post("/galpoes/", response_model=Galpao)
def create_galpao_api(galpao: Galpao, db: Session = Depends(get_db)):
    db_galpao = Galpao(**galpao.dict())
    db.add(db_galpao)
    db.commit()
    db.refresh(db_galpao)
    return db_galpao

@app.get("/galpoes/{galpao_id}", response_model=Galpao)
def read_galpao_api(galpao_id: int, db: Session = Depends(get_db)):
    return db.query(Galpao).filter(Galpao.id == galpao_id).first()

@app.get("/galpoes/", response_model=List[Galpao])
def read_galpoes_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Galpao).offset(skip).limit(limit).all()

@app.put("/galpoes/{galpao_id}", response_model=Galpao)
def update_galpao_api(galpao_id: int, galpao: Galpao, db: Session = Depends(get_db)):
    db_galpao = db.query(Galpao).filter(Galpao.id == galpao_id).first()
    for field, value in galpao.dict().items():
        setattr(db_galpao, field, value)
    db.commit()
    db.refresh(db_galpao)
    return db_galpao

@app.delete("/galpoes/{galpao_id}", response_model=Galpao)
def delete_galpao_api(galpao_id: int, db: Session = Depends(get_db)):
    db_galpao = db.query(Galpao).filter(Galpao.id == galpao_id).first()
    db.delete(db_galpao)
    db.commit()
    return db_galpao

# ========================================================================================
# Cliente CRUD
@app.post("/clientes/", response_model=Cliente)
def create_cliente_api(cliente: Cliente, db: Session = Depends(get_db)):
    db_cliente = Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@app.get("/clientes/{cliente_id}", response_model=Cliente)
def read_cliente_api(cliente_id: int, db: Session = Depends(get_db)):
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()

@app.get("/clientes/", response_model=List[Cliente])
def read_clientes_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Cliente).offset(skip).limit(limit).all()

@app.put("/clientes/{cliente_id}", response_model=Cliente)
def update_cliente_api(cliente_id: int, cliente: Cliente, db: Session = Depends(get_db)):
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    for field, value in cliente.dict().items():
        setattr(db_cliente, field, value)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@app.delete("/clientes/{cliente_id}", response_model=Cliente)
def delete_cliente_api(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    db.delete(db_cliente)
    db.commit()
    return db_cliente

# ========================================================================================
# Pedido CRUD
@app.post("/pedidos/", response_model=Pedido)
def create_pedido_api(pedido: Pedido, db: Session = Depends(get_db)):
    db_pedido = Pedido(**pedido.dict())
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

@app.get("/pedidos/{pedido_id}", response_model=Pedido)
def read_pedido_api(pedido_id: int, db: Session = Depends(get_db)):
    return db.query(Pedido).filter(Pedido.id == pedido_id).first()

@app.get("/pedidos/", response_model=List[Pedido])
def read_pedidos_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Pedido).offset(skip).limit(limit).all()

@app.put("/pedidos/{pedido_id}", response_model=Pedido)
def update_pedido_api(pedido_id: int, pedido: Pedido, db: Session = Depends(get_db)):
    db_pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    for field, value in pedido.dict().items():
        setattr(db_pedido, field, value)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

@app.delete("/pedidos/{pedido_id}", response_model=Pedido)
def delete_pedido_api(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    db.delete(db_pedido)
    db.commit()
    return db_pedido
# ========================================================================================
# MAIN
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
