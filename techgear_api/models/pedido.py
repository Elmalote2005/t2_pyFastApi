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
