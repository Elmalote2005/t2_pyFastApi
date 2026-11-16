from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# ========== Productos ==========
class Producto(BaseModel):
    nombre: str = Field(..., min_length=2, description="Nombre del producto")
    descripcion: Optional[str] = Field(None, description="Descripción detallada")
    precio: float = Field(..., gt=0, description="El precio debe ser mayor a 0")
    cantidad: int = Field(default=0, ge=0, description="Cantidad en inventario")
    categoria: str = Field(..., min_length=2, description="Categoría del producto")
    imagen_url: Optional[str] = Field(None, description="URL de la imagen")

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    cantidad: Optional[int] = None
    categoria: Optional[str] = None
    imagen_url: Optional[str] = None

# ========== Carrito ==========
class CarritoItem(BaseModel):
    producto_id: str = Field(..., description="ID del producto")
    nombre: str = Field(..., description="Nombre del producto")
    precio: float = Field(..., gt=0, description="Precio unitario")
    imagen_url: Optional[str] = None
    cantidad: int = Field(default=1, ge=1, description="Mínimo 1 unidad")

# ========== Pedidos ==========
class Pedido(BaseModel):
    usuario_correo: Optional[str] = None
    items: Optional[List[CarritoItem]] = None
    total: Optional[float] = Field(None, ge=0)
    estado: str = Field(default="pendiente")
    fecha: Optional[datetime] = None

class PedidoUpdate(BaseModel):
    estado: Optional[str] = None

# ========== Usuarios ==========
class Usuario(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    correo: EmailStr
    password: str = Field(..., min_length=6, description="Mínimo 6 caracteres")
    es_admin: bool = Field(default=False)

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[EmailStr] = None
    password: Optional[str] = None
    es_admin: Optional[bool] = None

# ========== Autenticación ==========
class LoginData(BaseModel):
    correo: EmailStr
    password: str = Field(..., min_length=6)

class RegistroData(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    correo: EmailStr
    password: str = Field(..., min_length=6, description="Mínimo 6 caracteres")
