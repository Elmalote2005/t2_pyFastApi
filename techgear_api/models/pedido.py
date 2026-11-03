from typing import Optional, List
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
