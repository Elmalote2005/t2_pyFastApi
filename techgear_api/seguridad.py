from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from database import usuarios_collection

SECRET_KEY = "tu_clave_secreta_muy_segura_2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verificar_contraseña(contraseña_plana: str, contraseña_hash: str) -> bool:
    return pwd_context.verify(contraseña_plana, contraseña_hash)

def encriptar_contraseña(contraseña: str) -> str:
    return pwd_context.hash(contraseña)

def crear_token_acceso(datos: dict, expiracion: Optional[timedelta] = None):
    datos_a_codificar = datos.copy()
    if expiracion:
        tiempo_expiracion = datetime.utcnow() + expiracion
    else:
        tiempo_expiracion = datetime.utcnow() + timedelta(minutes=15)
    datos_a_codificar.update({"exp": tiempo_expiracion})
    token_jwt = jwt.encode(datos_a_codificar, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

async def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    credenciales_excepcion = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        datos = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo: str = datos.get("sub")
        if correo is None:
            raise credenciales_excepcion
    except JWTError:
        raise credenciales_excepcion
    usuario = usuarios_collection.find_one({"correo": correo})
    if usuario is None:
        raise credenciales_excepcion
    return usuario
