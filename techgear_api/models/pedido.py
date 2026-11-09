from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# Para el carrito de compras
class CarritoItem(BaseModel):
    producto_id: str
    nombre: str
    precio: float
    imagen_url: str
    cantidad: int = Field(..., gt=0, description="La cantidad debe ser mayor a 0")

# Para pedidos completos
class ItemPedido(BaseModel):
    producto_id: str = Field(..., description="Identificador del producto")
    cantidad: int = Field(..., gt=0, description="La cantidad debe ser mayor a 0")

class Pedido(BaseModel):
    usuario_correo: str
    items: List[CarritoItem]
    total: float
    fecha: datetime = None
    estado: Optional[str] = Field(default="pendiente", pattern="^(pendiente|enviado|entregado|cancelado)$")

class PedidoUpdate(BaseModel):
    estado: Optional[str] = Field(None, pattern="^(pendiente|enviado|entregado|cancelado)$")
