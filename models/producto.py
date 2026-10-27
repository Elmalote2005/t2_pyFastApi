from pydantic import BaseModel, Field, constr
from typing import Optional

class Producto(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100, description="Nombre del producto")
    descripcion: Optional[str] = Field(None, max_length=250)
    precio: float = Field(..., gt=0, description="El precio debe ser mayor a 0")
    stock: int = Field(..., ge=0, description="El stock no puede ser negativo")
    categoria: Optional[str] = None

class ProductoUpdate(BaseModel):
    nombre: Optional[constr(min_length=3, max_length=100)] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    categoria: Optional[str] = None
