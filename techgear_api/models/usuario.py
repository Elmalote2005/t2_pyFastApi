from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class Usuario(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre completo")
    correo: EmailStr = Field(..., description="Correo electrónico válido")
    contraseña: str = Field(..., min_length=6, description="Mínimo 6 caracteres")


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    correo: Optional[EmailStr] = None
    contraseña: Optional[str] = Field(None, min_length=6)


class LoginData(BaseModel):
    correo: EmailStr
    contraseña: str
