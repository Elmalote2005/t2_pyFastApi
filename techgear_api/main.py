from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
import hashlib

# 🔴 CONEXIÓN CORRECTA A TU BASE DE DATOS EN LA NUBE
URI = "mongodb+srv://techgear_user:h7S3p2YBjXhOPB5b@cluster0.bvjdyrp.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(URI, serverSelectionTimeoutMS=5000)

try:
    client.admin.command("ping")
    print("✅ Conexión exitosa a MongoDB Atlas")
    db = client["techgear_db"]
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    raise

# Colecciones
usuarios_collection = db["usuarios"]
productos_collection = db["productos"]

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

app = FastAPI()

class LoginData(BaseModel):
    correo: EmailStr
    password: str

class RegistroData(BaseModel):
    nombre: str
    correo: EmailStr
    password: str

@app.post("/registro")
def registro(datos: RegistroData):
    existe = usuarios_collection.find_one({"correo": datos.correo})
    if existe:
        raise HTTPException(status_code=400, detail="El correo ya existe")
    nuevo = {
        "nombre": datos.nombre,
        "correo": datos.correo,
        "password": hash_pw(datos.password),
        "es_admin": False
    }
    usuarios_collection.insert_one(nuevo)
    return {"mensaje": "Registrado correctamente"}

@app.post("/login")
def login(datos: LoginData):
    usuario = usuarios_collection.find_one({"correo": datos.correo})
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    if usuario["password"] != hash_pw(datos.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"mensaje": "Bienvenido", "nombre": usuario["nombre"], "es_admin": usuario.get("es_admin", False)}

@app.get("/productos")
def listar_productos():
    productos = list(productos_collection.find())
    for p in productos:
        p["_id"] = str(p["_id"])
    return productos
