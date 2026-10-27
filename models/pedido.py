from pydantic import BaseModel, Field
from typing import Optional

class Pedido(BaseModel):
    producto_id: str = Field(..., description="ID del producto")
    cantidad: int = Field(..., gt=0, description="La cantidad debe ser mayor a 0")
    estado: str = Field(default="pendiente", pattern="^(pendiente|enviado|entregado|cancelado)$")

class PedidoUpdate(BaseModel):
    producto_id: Optional[str] = None
    cantidad: Optional[int] = Field(None, gt=0)
    estado: Optional[str] = Field(None, pattern="^(pendiente|enviado|entregado|cancelado)$")
