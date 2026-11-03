from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional

class Usuario(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    correo: EmailStr = Field(..., description="Correo electrónico válido")
    password: str = Field(..., min_length=6, description="Contraseña con mínimo 6 caracteres")
    rol: str = Field(default="usuario")
    is_active: bool = Field(default=True, description="Usuario activo por defecto")

    @field_validator('rol')
    def validar_rol(cls, v):
        if v not in ("usuario", "admin"):
            raise ValueError("El rol debe ser 'usuario' o 'admin'")
        return v

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)
    correo: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    rol: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator('rol')
    def validar_rol(cls, v):
        if v is not None and v not in ("usuario", "admin"):
            raise ValueError("El rol debe ser 'usuario' o 'admin'")
        return v
