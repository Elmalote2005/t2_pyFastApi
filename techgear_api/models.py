from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class Producto(BaseModel):
    nombre: str = Field(..., min_length=2)
    descripcion: Optional[str] = None
    precio: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)
    categoria: str = Field(..., min_length=2)
    imagen_url: Optional[str] = None

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    categoria: Optional[str] = None
    imagen_url: Optional[str] = None

class Pedido(BaseModel):
    producto_id: str
    nombre_cliente: str = Field(..., min_length=2)
    email_cliente: EmailStr
    direccion: str = Field(..., min_length=5)
    estado: str = Field(default="pendiente")

class PedidoUpdate(BaseModel):
    producto_id: Optional[str] = None
    nombre_cliente: Optional[str] = None
    email_cliente: Optional[EmailStr] = None
    direccion: Optional[str] = None
    estado: Optional[str] = None

class Usuario(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    correo: EmailStr
    password: str = Field(..., min_length=6)
    rol: str = Field(default="usuario")
    is_active: bool = Field(default=True)

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[EmailStr] = None
    password: Optional[str] = None
    rol: Optional[str] = None
    is_active: Optional[bool] = None
