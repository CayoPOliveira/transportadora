from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from models import engine
from crud import (
    create_item,
    read_item,
    read_items,
    update_item,
    delete_item,
    create_caminhao,
    read_caminhao,
    read_caminhoes,
    update_caminhao,
    delete_caminhao,
    create_galpao,
    read_galpao,
    read_galpoes,
    update_galpao,
    delete_galpao,
    create_cliente,
    read_cliente,
    read_clientes,
    update_cliente,
    delete_cliente,
    create_pedido,
    read_pedido,
    read_pedidos,
    update_pedido,
    delete_pedido,
)

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

# ========================================================================================
# Item CRUD
@app.post("/items/", response_model=Item)
def create_item_api(item: Item, db: Session = Depends(get_db)):
    return create_item(db, item)

@app.get("/items/{item_id}", response_model=Item)
def read_item_api(item_id: int, db: Session = Depends(get_db)):
    return read_item(db, item_id)

@app.get("/items/", response_model=List[Item])
def read_items_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return read_items(db, skip=skip, limit=limit)

@app.put("/items/{item_id}", response_model=Item)
def update_item_api(item_id: int, item: Item, db: Session = Depends(get_db)):
    return update_item(db, item_id, item)

@app.delete("/items/{item_id}", response_model=Item)
def delete_item_api(item_id: int, db: Session = Depends(get_db)):
    return delete_item(db, item_id)

# ========================================================================================
# Caminhao CRUD
@app.post("/caminhoes/", response_model=Caminhao)
def create_caminhao_api(caminhao: Caminhao, db: Session = Depends(get_db)):
    return create_caminhao(db, caminhao)

@app.get("/caminhoes/{caminhao_id}", response_model=Caminhao)
def read_caminhao_api(caminhao_id: int, db: Session = Depends(get_db)):
    return read_caminhao(db, caminhao_id)

@app.get("/caminhoes/", response_model=List[Caminhao])
def read_caminhoes_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return read_caminhoes(db, skip=skip, limit=limit)

@app.put("/caminhoes/{caminhao_id}", response_model=Caminhao)
def update_caminhao_api(caminhao_id: int, caminhao: Caminhao, db: Session = Depends(get_db)):
    return update_caminhao(db, caminhao_id, caminhao)

@app.delete("/caminhoes/{caminhao_id}", response_model=Caminhao)
def delete_caminhao_api(caminhao_id: int, db: Session = Depends(get_db)):
    return delete_caminhao(db, caminhao_id)

# ========================================================================================
# Galpao CRUD
@app.post("/galpoes/", response_model=Galpao)
def create_galpao_api(galpao: Galpao, db: Session = Depends(get_db)):
    return create_galpao(db, galpao)

@app.get("/galpoes/{galpao_id}", response_model=Galpao)
def read_galpao_api(galpao_id: int, db: Session = Depends(get_db)):
    return read_galpao(db, galpao_id)

@app.get("/galpoes/", response_model=List[Galpao])
def read_galpoes_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return read_galpoes(db, skip=skip, limit=limit)

@app.put("/galpoes/{galpao_id}", response_model=Galpao)
def update_galpao_api(galpao_id: int, galpao: Galpao, db: Session = Depends(get_db)):
    return update_galpao(db, galpao_id, galpao)

@app.delete("/galpoes/{galpao_id}", response_model=Galpao)
def delete_galpao_api(galpao_id: int, db: Session = Depends(get_db)):
    return delete_galpao(db, galpao_id)

# ========================================================================================
# Cliente CRUD
@app.post("/clientes/", response_model=Cliente)
def create_cliente_api(cliente: Cliente, db: Session = Depends(get_db)):
    return create_cliente(db, cliente)

@app.get("/clientes/{cliente_id}", response_model=Cliente)
def read_cliente_api(cliente_id: int, db: Session = Depends(get_db)):
    return read_cliente(db, cliente_id)

@app.get("/clientes/", response_model=List[Cliente])
def read_clientes_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return read_clientes(db, skip=skip, limit=limit)

@app.put("/clientes/{cliente_id}", response_model=Cliente)
def update_cliente_api(cliente_id: int, cliente: Cliente, db: Session = Depends(get_db)):
    return update_cliente(db, cliente_id, cliente)

@app.delete("/clientes/{cliente_id}", response_model=Cliente)
def delete_cliente_api(cliente_id: int, db: Session = Depends(get_db)):
    return delete_cliente(db, cliente_id)

# ========================================================================================
# Pedido CRUD
@app.post("/pedidos/", response_model=Pedido)
def create_pedido_api(pedido: Pedido, db: Session = Depends(get_db)):
    return create_pedido(db, pedido)

@app.get("/pedidos/{pedido_id}", response_model=Pedido)
def read_pedido_api(pedido_id: int, db: Session = Depends(get_db)):
    return read_pedido(db, pedido_id)

@app.get("/pedidos/", response_model=List[Pedido])
def read_pedidos_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return read_pedidos(db, skip=skip, limit=limit)

@app.put("/pedidos/{pedido_id}", response_model=Pedido)
def update_pedido_api(pedido_id: int, pedido: Pedido, db: Session = Depends(get_db)):
    return update_pedido(db, pedido_id, pedido)

@app.delete("/pedidos/{pedido_id}", response_model=Pedido)
def delete_pedido_api(pedido_id: int, db: Session = Depends(get_db)):
    return delete_pedido(db, pedido_id)

# ========================================================================================
# MAIN
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
