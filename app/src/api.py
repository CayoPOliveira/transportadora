from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from models import session, Item, Caminhao, Cliente, Pedido

# API ========================================================
class Request_Item(BaseModel):
    id: int
    nome: str
    descricao: str
    peso: float

class Request_Caminhao(BaseModel):
    id: int
    modelo: str
    capacidade_carga: float
    localizacao: str
    status: str
    motorista: str

class Request_Cliente(BaseModel):
    id: int
    nome: str
    telefone: str
    cpf: str
    cep: str
    numero: str
    complemento: str

class Request_Pedido(BaseModel):
    id: int
    quantidade: int
    status: str  # Status do pedido
    cliente_id: int
    item_id: int
    caminhao_id: int

app = FastAPI()

# ========================================================================================

@app.get("/")
def api_is_running():
    return {"status": "API IS RUNNING"}

# Item CRUD
@app.post("/items/")
def create_item_api(item: Request_Item):
    session_item = Item(nome = item.nome,
                        descricao = item.descricao,
                        peso = item.peso
    )
    session.add(session_item)
    session.commit()
    session.refresh(session_item)
    return {
        "status": "SUCESS",
        "data": session_item
    }

@app.get("/items/{item_id}")
def read_items_api(item_id: int):
    return {
        "status": "SUCESS",
        "data": session.query(Item).filter(Item.id == item_id).first()
    }

@app.get("/items/")
def read_items_api():
    return {
        "status": "SUCESS",
        "data": session.query(Item).all()
    }

# @app.put("/items/{item_id}", response_model=Item)
# def update_item_api(item_id: int, item: Item):
#     session_item = session.query(Item).filter(Item.id == item_id).first()
#     for field, value in item.dict().items():
#         setattr(session_item, field, value)
#     session.commit()
#     session.refresh(session_item)
#     return session_item

# @app.delete("/items/{item_id}", response_model=Item)
# def delete_item_api(item_id: int):
#     session_item = session.query(Item).filter(Item.id == item_id).first()
#     session.delete(session_item)
#     session.commit()
#     return session_item

# # ========================================================================================
# # Caminhao CRUD
# @app.post("/caminhoes/", response_model=Caminhao)
# def create_caminhao_api(caminhao: Caminhao):
#     session_caminhao = Caminhao(**caminhao.dict())
#     session.add(session_caminhao)
#     session.commit()
#     session.refresh(session_caminhao)
#     return session_caminhao

# @app.get("/caminhoes/{caminhao_id}", response_model=Caminhao)
# def read_caminhao_api(caminhao_id: int):
#     return session.query(Caminhao).filter(Caminhao.id == caminhao_id).first()

# @app.get("/caminhoes/", response_model=List[Caminhao])
# def read_caminhoes_api(skip: int = 0, limit: int = 100):
#     return session.query(Caminhao).offset(skip).limit(limit).all()

# @app.put("/caminhoes/{caminhao_id}", response_model=Caminhao)
# def update_caminhao_api(caminhao_id: int, caminhao: Caminhao):
#     session_caminhao = session.query(Caminhao).filter(Caminhao.id == caminhao_id).first()
#     for field, value in caminhao.dict().items():
#         setattr(session_caminhao, field, value)
#     session.commit()
#     session.refresh(session_caminhao)
#     return session_caminhao

# @app.delete("/caminhoes/{caminhao_id}", response_model=Caminhao)
# def delete_caminhao_api(caminhao_id: int):
#     session_caminhao = session.query(Caminhao).filter(Caminhao.id == caminhao_id).first()
#     session.delete(session_caminhao)
#     session.commit()
#     return session_caminhao

# # ========================================================================================
# # Cliente CRUD
# @app.post("/clientes/", response_model=Cliente)
# def create_cliente_api(cliente: Cliente):
#     session_cliente = Cliente(**cliente.dict())
#     session.add(session_cliente)
#     session.commit()
#     session.refresh(session_cliente)
#     return session_cliente

# @app.get("/clientes/{cliente_id}", response_model=Cliente)
# def read_cliente_api(cliente_id: int):
#     return session.query(Cliente).filter(Cliente.id == cliente_id).first()

# @app.get("/clientes/", response_model=List[Cliente])
# def read_clientes_api(skip: int = 0, limit: int = 100):
#     return session.query(Cliente).offset(skip).limit(limit).all()

# @app.put("/clientes/{cliente_id}", response_model=Cliente)
# def update_cliente_api(cliente_id: int, cliente: Cliente):
#     session_cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()
#     for field, value in cliente.dict().items():
#         setattr(session_cliente, field, value)
#     session.commit()
#     session.refresh(session_cliente)
#     return session_cliente

# @app.delete("/clientes/{cliente_id}", response_model=Cliente)
# def delete_cliente_api(cliente_id: int):
#     session_cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()
#     session.delete(session_cliente)
#     session.commit()
#     return session_cliente

# # ========================================================================================
# # Pedido CRUD
# @app.post("/pedidos/", response_model=Pedido)
# def create_pedido_api(pedido: Pedido):
#     session_pedido = Pedido(**pedido.dict())
#     session.add(session_pedido)
#     session.commit()
#     session.refresh(session_pedido)
#     return session_pedido

# @app.get("/pedidos/{pedido_id}", response_model=Pedido)
# def read_pedido_api(pedido_id: int):
#     return session.query(Pedido).filter(Pedido.id == pedido_id).first()

# @app.get("/pedidos/", response_model=List[Pedido])
# def read_pedidos_api(skip: int = 0, limit: int = 100):
#     return session.query(Pedido).offset(skip).limit(limit).all()

# @app.put("/pedidos/{pedido_id}", response_model=Pedido)
# def update_pedido_api(pedido_id: int, pedido: Pedido):
#     session_pedido = session.query(Pedido).filter(Pedido.id == pedido_id).first()
#     for field, value in pedido.dict().items():
#         setattr(session_pedido, field, value)
#     session.commit()
#     session.refresh(session_pedido)
#     return session_pedido

# @app.delete("/pedidos/{pedido_id}", response_model=Pedido)
# def delete_pedido_api(pedido_id: int):
#     session_pedido = session.query(Pedido).filter(Pedido.id == pedido_id).first()
#     session.delete(session_pedido)
#     session.commit()
#     return session_pedido

# # ========================================================================================
# # MAIN
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
