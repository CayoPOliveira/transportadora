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
    session_item = Item(
        nome = item.nome,
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

@app.put("/items/")
async def update_item_api(request_item: Request_Item):
    try:
        item = session.query(Item).filter(Item.id == request_item.id).first()
        original_item = Item(
            id = item.id,
            nome = item.nome,
            descricao = item.descricao,
            peso = item.peso
        )
        item.nome = request_item.nome
        item.descricao = request_item.descricao
        item.peso = request_item.peso

        session.commit()
        session.refresh(item)
        return {
            "status": "SUCESS",
            "original": original_item,
            "data": item
        }
    except Exception as e:
        return{
            "status": "NOT SUCESS",
            "data": "ITEM NÃO ENCONTRADO",
            "error": e
        }

@app.delete("/items/{item_id}")
def delete_item_api(item_id: int):
    item = session.query(Item).filter(Item.id == item_id).first()
    session.delete(item)
    session.commit()
    return {
        "status": "SUCESS",
        "data": item
    }

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
# Cliente CRUD
@app.post("/clientes/")
def create_cliente_api(cliente: Request_Cliente):
    session_cliente = Cliente(
        nome        = cliente.nome,
        telefone    = cliente.telefone,
        cpf         = cliente.cpf,
        cep         = cliente.cep,
        numero      = cliente.numero,
        complemento = cliente.complemento
    )

    session.add(session_cliente)
    session.commit()
    session.refresh(session_cliente)
    return {
        "status": "SUCESS",
        "data": session_cliente
    }

@app.get("/clientes/{cliente_id}")
def read_clientes_api(cliente_id: int):
    return {
        "status": "SUCESS",
        "data": session.query(Cliente).filter(Cliente.id == cliente_id).first()
    }

@app.get("/clientes/")
def read_clientes_api():
    return {
        "status": "SUCESS",
        "data": session.query(Cliente).all()
    }

@app.put("/clientes/{cliente_id}")
async def update_cliente_api(request_cliente: Request_Cliente):
    try:
        cliente = session.query(Cliente).filter(read_clientes_api.id == request_cliente.id).first()
        original_cliente = Cliente(
            id          = cliente.id,
            nome        = cliente.nome,
            telefone    = cliente.telefone,
            cpf         = cliente.cpf,
            cep         = cliente.cep,
            numero      = cliente.numero,
            complemento = cliente.complemento
        )
        cliente.nome        = request_cliente.nome,
        cliente.telefone    = request_cliente.telefone,
        cliente.cpf         = request_cliente.cpf,
        cliente.cep         = request_cliente.cep,
        cliente.numero      = request_cliente.numero,
        cliente.complemento = request_cliente.complemento

        session.commit()
        session.refresh(cliente)
        return {
            "status": "SUCESS",
            "original": original_cliente,
            "data": cliente
        }
    except Exception as e:
        return{
            "status": "NOT SUCESS",
            "data": "CLIENTE NÃO ENCONTRADO",
            "error": e
        }

@app.delete("/clientes/{cliente_id}")
def delete_cliente_api(cliente_id: int):
    cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()
    session.delete(cliente)
    session.commit()
    return {
        "status": "SUCESS",
        "data": cliente
    }

# # ========================================================================================
# Pedido CRUD
@app.post("/pedidos/")
def create_pedido_api(pedido: Request_Pedido):
    session_pedido = Pedido(
        quantidade  = pedido.quantidade,
        status      = pedido.status,
        cliente_id  = pedido.cliente_id,
        item_id     = pedido.item_id,
        caminhao_id = pedido.caminhao_id,
    )
    session.add(session_pedido)
    session.commit()
    session.refresh(session_pedido)
    return {
        "status": "SUCESS",
        "data": session_pedido
    }

@app.get("/pedidos/{pedido_id}")
def read_pedidos_api(pedido_id: int):
    return {
        "status": "SUCESS",
        "data": session.query(Pedido).filter(Pedido.id == pedido_id).first()
    }

@app.get("/pedidos/")
def read_pedidos_api():
    return {
        "status": "SUCESS",
        "data": session.query(Pedido).all()
    }

@app.put("/pedidos/")
def update_pedido_api(request_pedido: Request_Pedido):
    try:
        pedido = session.query(Pedido).filter(Pedido.id == request_pedido.id).first()
        original_pedido = Pedido(
            id          = pedido.id,
            quantidade  = pedido.quantidade,
            status      = pedido.status,
            cliente_id  = pedido.cliente_id,
            item_id     = pedido.item_id,
            caminhao_id = pedido.caminhao_id
        )
        pedido.quantidade   = request_pedido.quantidade,
        pedido.status       = request_pedido.status,
        pedido.cliente_id   = request_pedido.cliente_id,
        pedido.item_id      = request_pedido.item_id,
        pedido.caminhao_id  = request_pedido.caminhao_id

        session.commit()
        session.refresh(pedido)
        return {
            "status": "SUCESS",
            "original": original_pedido,
            "data": pedido
        }
    except Exception as e:
        return{
            "status": "NOT SUCESS",
            "data": "PEDIDO NÃO ENCONTRADO",
            "error": e
        }

@app.delete("/pedidos/{pedido_id}")
def delete_pedido_api(pedido_id: int):
    pedido = session.query(Pedido).filter(Pedido.id == pedido_id).first()
    session.delete(pedido)
    session.commit()
    return {
        "status": "SUCESS",
        "data": pedido
    }

# # ========================================================================================
# # MAIN
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

# Abrindo guias para monitoramento
import webbrowser
import time
time.sleep(3)
webbrowser.open('localhost:8080', new=2)
time.sleep(5)
webbrowser.open('localhost:8000', new=2)