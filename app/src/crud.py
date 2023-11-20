from sqlalchemy.orm import Session
from models import Item, Caminhao, Galpao, Cliente, Pedido

# CRUD Item
def create_item(db: Session, item: Item):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def read_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def read_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()

def update_item(db: Session, item_id: int, item: Item):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    for field, value in item.dict().items():
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    db.delete(db_item)
    db.commit()
    return db_item

# CRUD Caminhao
def create_caminhao(db: Session, caminhao: Caminhao):
    db_caminhao = Caminhao(**caminhao.dict())
    db.add(db_caminhao)
    db.commit()
    db.refresh(db_caminhao)
    return db_caminhao

def read_caminhao(db: Session, caminhao_id: int):
    return db.query(Caminhao).filter(Caminhao.id == caminhao_id).first()

def read_caminhoes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Caminhao).offset(skip).limit(limit).all()

def update_caminhao(db: Session, caminhao_id: int, caminhao: Caminhao):
    db_caminhao = db.query(Caminhao).filter(Caminhao.id == caminhao_id).first()
    for field, value in caminhao.dict().items():
        setattr(db_caminhao, field, value)
    db.commit()
    db.refresh(db_caminhao)
    return db_caminhao

def delete_caminhao(db: Session, caminhao_id: int):
    db_caminhao = db.query(Caminhao).filter(Caminhao.id == caminhao_id).first()
    db.delete(db_caminhao)
    db.commit()
    return db_caminhao

# CRUD Galpao
def create_galpao(db: Session, galpao: Galpao):
    db_galpao = Galpao(**galpao.dict())
    db.add(db_galpao)
    db.commit()
    db.refresh(db_galpao)
    return db_galpao

def read_galpao(db: Session, galpao_id: int):
    return db.query(Galpao).filter(Galpao.id == galpao_id).first()

def read_galpoes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Galpao).offset(skip).limit(limit).all()

def update_galpao(db: Session, galpao_id: int, galpao: Galpao):
    db_galpao = db.query(Galpao).filter(Galpao.id == galpao_id).first()
    for field, value in galpao.dict().items():
        setattr(db_galpao, field, value)
    db.commit()
    db.refresh(db_galpao)
    return db_galpao

def delete_galpao(db: Session, galpao_id: int):
    db_galpao = db.query(Galpao).filter(Galpao.id == galpao_id).first()
    db.delete(db_galpao)
    db.commit()
    return db_galpao

# CRUD Cliente
def create_cliente(db: Session, cliente: Cliente):
    db_cliente = Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def read_cliente(db: Session, cliente_id: int):
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()

def read_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Cliente).offset(skip).limit(limit).all()

def update_cliente(db: Session, cliente_id: int, cliente: Cliente):
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    for field, value in cliente.dict().items():
        setattr(db_cliente, field, value)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def delete_cliente(db: Session, cliente_id: int):
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    db.delete(db_cliente)
    db.commit()
    return db_cliente

# CRUD Pedido
def create_pedido(db: Session, pedido: Pedido):
    db_pedido = Pedido(**pedido.dict())
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def read_pedido(db: Session, pedido_id: int):
    return db.query(Pedido).filter(Pedido.id == pedido_id).first()

def read_pedidos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Pedido).offset(skip).limit(limit).all()

def update_pedido(db: Session, pedido_id: int, pedido: Pedido):
    db_pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    for field, value in pedido.dict().items():
        setattr(db_pedido, field, value)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def delete_pedido(db: Session, pedido_id: int):
    db_pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    db.delete(db_pedido)
    db.commit()
    return db_pedido

