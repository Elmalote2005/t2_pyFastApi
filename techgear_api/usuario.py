from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from models import LoginData

router = APIRouter()

URI = "mongodb+srv://techgear_user:nZBVljAiCnmNoWVG@cluster0.bvjdyrp.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(URI)
db = client["techgear_db"]
usuarios_collection = db["usuarios_collection"]

@router.post("/login")
def login(datos: LoginData):
    usuario = usuarios_collection.find_one({"correo": datos.correo})
    if not usuario:
        raise HTTPException(401, "Credenciales incorrectas")
    
    if usuario["contraseña"] != datos.password:
        raise HTTPException(401, "Credenciales incorrectas")
    
    return {
        "access_token": "ok",
        "usuario": {
            "nombre": usuario["nombre"],
            "correo": usuario["correo"],
            "rol": usuario["rol"]
        }
    }
