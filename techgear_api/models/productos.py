<<<<<<< HEAD
﻿from typing import Optional
from pydantic import BaseModel, Field


class Producto(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre del producto")
    descripcion: Optional[str] = Field(None, max_length=500)
    categoria: str = Field(..., min_length=2, max_length=50)
    precio: float = Field(..., gt=0, description="El precio debe ser mayor a 0")
    stock: int = Field(..., ge=0, description="El stock no puede ser negativo")
    imagen_url: Optional[str] = None


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    categoria: Optional[str] = Field(None, min_length=2, max_length=50)
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    imagen_url: Optional[str] = None
=======
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl

class ProductoModel(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=250)
    categoria: str = Field(..., min_length=2, max_length=50)
    precio: float = Field(..., gt=0, description="El precio debe ser mayor a 0")
    stock: int = Field(..., ge=0, description="El stock no puede ser negativo")
    imagen_url: Optional[HttpUrl] = None

class ProductoUpdateModel(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=250)
    categoria: Optional[str] = Field(None, min_length=2, max_length=50)
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    imagen_url: Optional[HttpUrl] = None
>>>>>>> e6e4704bc7c0245cbbd63bcbb0f8a3b5ec54bf50
