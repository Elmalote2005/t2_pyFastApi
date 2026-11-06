from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime, timedelta
import hashlib
import jwt

# Conectar a MongoDB
cliente = MongoClient("mongodb+srv://techgear_user:nZBVljAiCnmNoWVG@cluster0.bvjdyrp.mongodb.net/?retryWrites=true&w=majority")
db = cliente["techgear_db"]
usuarios_col = db["usuarios"]
productos_col = db["productos"]

app = FastAPI()
SECRET_KEY = "clave_secreta_para_tokens"

# Función de hash USANDO EL MISMO SISTEMA
def hash_password_simple(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

def crear_token(datos: dict, expira_en=24):
    payload = datos.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=expira_en)
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

class RegistroDatos(BaseModel):
    nombre: str
    correo: str
    password: str

class LoginDatos(BaseModel):
    correo: str
    password: str

@app.get("/")
def raiz():
    return {"mensaje": "API funcionando correctamente"}

@app.post("/registro")
def registro(datos: RegistroDatos):
    existe = usuarios_col.find_one({"correo": datos.correo})
    if existe:
        raise HTTPException(400, "El correo ya está registrado")
    
    # Determinar rol
    rol = "admin" if datos.correo.endswith("@admin.com") else "usuario"
    
    nuevo_usuario = {
        "nombre": datos.nombre, "imagen": datos.imagen, "descripcion": datos.descripcion,
        "correo": datos.correo,
        "password": hash_password_simple(datos.password),
        "rol": rol,
        "fecha_registro": datetime.utcnow()
    }
    usuarios_col.insert_one(nuevo_usuario)
    return {"mensaje": "Usuario registrado correctamente", "rol": rol}

@app.post("/login")
def login(datos: LoginDatos):
    usuario = usuarios_col.find_one({"correo": datos.correo})
    if not usuario:
        raise HTTPException(401, "Credenciales incorrectas")
    
    # Comparar con el MISMO sistema de hash
    hash_entrada = hash_password_simple(datos.password)
    if usuario["password"] != hash_entrada:
        raise HTTPException(401, "Credenciales incorrectas")
    
    rol = usuario.get("rol", "usuario")
    token = crear_token({"sub": usuario["correo"], "rol": rol})
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "nombre": usuario["nombre"],
            "correo": usuario["correo"],
            "rol": rol
        }
    }

@app.get("/productos")
def listar_productos():
    productos = list(productos_col.find({}, {"_id": 0}))
    return {"productos": productos}

@app.post("/productos")
def crear_producto(datos: dict):
    datos["fecha_creacion"] = datetime.utcnow()
    productos_col.insert_one(datos)
    return {"mensaje": "Producto creado"}

@app.put("/productos/{id_producto}")
def editar_producto(id_producto: str, datos: dict):
    from bson import ObjectId
    productos_col.update_one({"_id": ObjectId(id_producto)}, {"$set": datos})
    return {"mensaje": "Producto actualizado"}

@app.delete("/productos/{id_producto}")
def eliminar_producto(id_producto: str):
    from bson import ObjectId
    productos_col.delete_one({"_id": ObjectId(id_producto)})
    return {"mensaje": "Producto eliminado"}
