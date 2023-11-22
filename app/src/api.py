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
        nome        = item.nome,
        descricao   = item.descricao,
        peso        = item.peso
    )
    session.add(session_item)
    session.commit()
    session.refresh(session_item)
    return {
        "status": "SUCESS",
        "data": session_item
    }

@app.get("/items/{item_id}")
def read_itens_api(item_id: int):
    return {
        "status": "SUCESS",
        "data": session.query(Item).filter(Item.id == item_id).first()
    }

@app.get("/items/")
def read_itens_api():
    return {
        "status": "SUCESS",
        "data": session.query(Item).all()
    }

@app.put("/items/")
async def update_item_api(request_item: Request_Item):
    try:
        item = session.query(Item).filter(Item.id == request_item.id).first()
        original_item = Item(
            id          = item.id,
            nome        = item.nome,
            descricao   = item.descricao,
            peso        = item.peso
        )

        item.nome       = request_item.nome
        item.descricao  = request_item.descricao
        item.peso       = request_item.peso

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

# ========================================================================================
# Caminhao CRUD
@app.post("/caminhoes/")
def create_caminhao_api(caminhao: Request_Caminhao):
    session_caminhao = Caminhao(
        modelo              = caminhao.modelo,
        capacidade_carga    = caminhao.capacidade_carga,
        localizacao         = caminhao.localizacao,
        status              = caminhao.status,
        motorista           = caminhao.motorista
    )
    session.add(session_caminhao)
    session.commit()
    session.refresh(session_caminhao)
    return {
        "status": "SUCESS",
        "data": session_caminhao
    }

@app.get("/caminhoes/{caminhao_id}")
def read_caminhoes_api(caminhao_id: int):
    return {
        "status": "SUCESS",
        "data": session.query(Caminhao).filter(Caminhao.id == caminhao_id).first()
    }

@app.get("/caminhoes/")
def read_caminhoes_api():
    return {
        "status": "SUCESS",
        "data": session.query(Caminhao).all()
    }

@app.put("/caminhoes/")
async def update_caminhao_api(request_caminhao: Request_Caminhao):
    try:
        caminhao = session.query(Caminhao).filter(Caminhao.id == request_caminhao_id).first()
        original_caminhao = Caminhao(
            id = caminhao.id,
            modelo = caminhao.modelo,
            capacidade_carga = caminhao.capacidade_carga,
            localizacao = caminhao.localizacao,
            status = caminhao.status,
            motorista = caminhao.motorista
        )

        caminhao.modelo = request_caminhao.modelo
        caminhao.capacidade_carga = request_caminhao.capacidade_carga
        caminhao.localizacao = request_caminhao.localizacao
        caminhao.status = request_caminhao.status
        caminhao.motorista = request_caminhao.motorista

        session.commit()
        session.refresh(caminhao)
        return {
            "status": "SUCESS",
            "original": original_caminhao,
            "data": caminhao
        }
    except Exception as e:
        return{
            "status": "NOT SUCESS",
            "data": "ITEM NÃO ENCONTRADO",
            "error": e
        }

@app.delete("/caminhoes/{caminhao_id}")
def delete_caminhao_api(caminhao_id: int):
    caminhao = session.query(Caminhao).filter(Caminhao.id == caminhao_id).first()
    session.delete(caminhao)
    session.commit()
    return {
        "status": "SUCESS",
        "data": caminhao
    }

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
# Pedido CRUD
@app.post("/pedidos/")
def create_pedido_api(pedido: Request_Pedido):
    session_pedido = Pedido(
        quantidade = pedido.quantidade,
        status = pedido.status,
        cliente_id = pedido.cliente_id,
        item_id = pedido.item_id,
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

# abrindo guias
import webbrowser
import time
time.sleep(3)
webbrowser.open('localhost:8080', new=2)
time.sleep(5)
webbrowser.open('localhost:8000', new=2)