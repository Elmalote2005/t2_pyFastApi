from typing import Optional
from pydantic import BaseModel


class ProductoModel(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    categoria: str
    precio: float
    stock: int
    imagen_url: Optional[str] = None


class ProductoUpdateModel(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    imagen_url: Optional[str] = None