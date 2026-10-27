from pydantic import BaseModel, Field, constr
from typing import Optional

class Usuario(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    correo: str = Field(..., description="Correo electrónico")
    rol: str = Field(default="usuario", pattern="^(usuario|admin)$")

class UsuarioUpdate(BaseModel):
    nombre: Optional[constr(min_length=3, max_length=100)] = None
    correo: Optional[str] = None
    rol: Optional[str] = Field(None, pattern="^(usuario|admin)$")
