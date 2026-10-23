from typing import Optional, List
from pydantic import BaseModel


class ItemPedido(BaseModel):
    producto_id: str
    cantidad: int


class PedidoModel(BaseModel):
    nombre_cliente: str
    email_cliente: str
    direccion: str
    items: List[ItemPedido]
    estado: Optional[str] = "pendiente"


class PedidoUpdateModel(BaseModel):
    estado: Optional[str] = None