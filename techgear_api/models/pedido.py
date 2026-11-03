<<<<<<< HEAD
﻿from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr


class ItemPedido(BaseModel):
    producto_id: str = Field(..., description="Identificador del producto")
    cantidad: int = Field(..., gt=0, description="La cantidad debe ser mayor a 0")


class Pedido(BaseModel):
    nombre_cliente: str = Field(..., min_length=3, max_length=100, description="Nombre completo")
    email_cliente: EmailStr = Field(..., description="Correo electrónico válido")
    direccion: str = Field(..., min_length=5, max_length=200, description="Dirección de entrega")
    items: List[ItemPedido] = Field(..., min_length=1, description="Debe incluir al menos un producto")
    estado: Optional[str] = Field(default="pendiente", description="Estado del pedido")


class PedidoUpdate(BaseModel):
    estado: Optional[str] = Field(None, description="Nuevo estado del pedido")
=======
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr

class ItemPedido(BaseModel):
    producto_id: str
    cantidad: int = Field(..., gt=0, description="La cantidad debe ser mayor a 0")

class PedidoModel(BaseModel):
    nombre_cliente: str = Field(..., min_length=3, max_length=100)
    email_cliente: EmailStr
    direccion: str = Field(..., min_length=5)
    items: List[ItemPedido]
    estado: Optional[str] = Field(default="pendiente", pattern="^(pendiente|enviado|entregado|cancelado)$")

class PedidoUpdateModel(BaseModel):
    estado: Optional[str] = Field(None, pattern="^(pendiente|enviado|entregado|cancelado)$")
>>>>>>> e6e4704bc7c0245cbbd63bcbb0f8a3b5ec54bf50
