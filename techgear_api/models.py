from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# ========== Productos ==========
class Producto(BaseModel):
    nombre: str = Field(..., min_length=2)
    descripcion: Optional[str] = None
    precio: float = Field(..., gt=0)
    cantidad: int = Field(default=0, ge=0)
    stock: Optional[int] = Field(default=0, ge=0)
    categoria: str = Field(..., min_length=2)
    imagen_url: Optional[str] = None

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    cantidad: Optional[int] = None
    stock: Optional[int] = None
    categoria: Optional[str] = None
    imagen_url: Optional[str] = None

# ========== Carrito ==========
class CarritoItem(BaseModel):
    producto_id: str
    nombre: str
    precio: float
    imagen_url: Optional[str] = None
    cantidad: int = Field(default=1, ge=1)

# ========== Pedidos ==========
class Pedido(BaseModel):
    producto_id: Optional[str] = None
    nombre_cliente: str = Field(..., min_length=2)
    email_cliente: EmailStr
    direccion: str = Field(..., min_length=5)
    estado: str = Field(default="pendiente")
    usuario_correo: Optional[str] = None
    items: Optional[List[CarritoItem]] = None
    total: Optional[float] = None
    fecha: Optional[datetime] = None

class PedidoUpdate(BaseModel):
    producto_id: Optional[str] = None
    nombre_cliente: Optional[str] = None
    email_cliente: Optional[EmailStr] = None
    direccion: Optional[str] = None
    estado: Optional[str] = None

# ========== Usuarios ==========
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

# ========== Autenticación ==========
# Usamos LoginData para que coincida con todo el código
class LoginData(BaseModel):
    correo: EmailStr
    password: str = Field(..., min_length=6)

class RegistroDatos(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    correo: EmailStr
    password: str = Field(..., min_length=6)
