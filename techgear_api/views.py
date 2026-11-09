from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
import hashlib
import jwt
from bson import ObjectId
from .database import (
    usuarios_collection,
    productos_collection,
    pedidos_collection,
    carrito_collection
)
from .models import Producto, ProductoUpdate, Pedido, PedidoUpdate, Usuario, LoginData

router = APIRouter()
SECRET_KEY = "clave_secreta_para_tokens"

def hash_password_simple(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

def crear_token(datos: dict, expira_en=24):
    payload = datos.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=expira_en)
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@router.get("/")
def raiz():
    return {"mensaje": "API TechGear funcionando ✅"}

@router.post("/registro")
def registro(usuario: Usuario):
    existe = usuarios_collection.find_one({"correo": usuario.correo})
    if existe:
        raise HTTPException(400, "El correo ya está registrado")
    
    rol = "admin" if usuario.correo.endswith("@admin.com") else "usuario"
    
    nuevo_usuario = {
        "nombre": usuario.nombre,
        "correo": usuario.correo,
        "contraseña": hash_password_simple(usuario.password),
        "rol": rol,
        "fecha_registro": datetime.utcnow()
    }
    usuarios_collection.insert_one(nuevo_usuario)
    return {"mensaje": "Usuario registrado ✅", "rol": rol}

@router.post("/login")
def login(datos: LoginData):
    usuario = usuarios_collection.find_one({"correo": datos.correo})
    if not usuario:
        raise HTTPException(401, "Credenciales incorrectas")
    
    if usuario["contraseña"] != hash_password_simple(datos.password):
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

@router.get("/productos")
def listar_productos():
    productos = []
    for p in productos_collection.find():
        p["id"] = str(p["_id"])   # Convertimos _id a id ✅
        del p["_id"]              # Quitamos el guion bajo
        productos.append(p)
    return productos

@router.post("/productos")
def crear_producto(producto: Producto):
    nuevo = producto.model_dump()
    nuevo["fecha_creacion"] = datetime.utcnow()
    productos_collection.insert_one(nuevo)
    return {"mensaje": "Producto creado ✅"}

@router.delete("/productos/{nombre}")
def eliminar_producto(nombre: str):
    productos_collection.delete_one({"nombre": nombre})
    return {"mensaje": "Producto eliminado ✅"}

@router.get("/carrito/{correo}")
def ver_carrito(correo: str):
    carrito = carrito_collection.find_one({"usuario_correo": correo}, {"_id": 0})
    return carrito if carrito else {"items": [], "total": 0}

@router.post("/carrito/{correo}/agregar")
def agregar_al_carrito(correo: str, item: dict):
    carrito = carrito_collection.find_one({"usuario_correo": correo}) or {
        "usuario_correo": correo,
        "items": [],
        "total": 0
    }
    existe = False
    for i in carrito["items"]:
        if i["producto_id"] == item["producto_id"]:
            i["cantidad"] += 1
            existe = True
            break
    if not existe:
        carrito["items"].append(item)
    carrito["total"] = sum(i["precio"] * i["cantidad"] for i in carrito["items"])
    carrito_collection.update_one({"usuario_correo": correo}, {"$set": carrito}, upsert=True)
    return carrito

@router.post("/pedidos/{correo}/confirmar")
def confirmar_pedido(correo: str):
    carrito = carrito_collection.find_one({"usuario_correo": correo})
    if not carrito or not carrito["items"]:
        raise HTTPException(400, "Carrito vacío")
    
    pedido = {
        "usuario_correo": correo,
        "items": carrito["items"],
        "total": carrito["total"],
        "fecha": datetime.utcnow(),
        "estado": "pendiente"
    }
    pedidos_collection.insert_one(pedido)
    
    for item in carrito["items"]:
        productos_collection.update_one(
            {"nombre": item["nombre"]},
            {"$inc": {"cantidad": -item["cantidad"]}}
        )
    
    carrito_collection.delete_one({"usuario_correo": correo})
    return {"mensaje": "Pedido confirmado ✅"}

@router.get("/admin/pedidos")
def ver_todos_pedidos():
    return list(pedidos_collection.find({}, {"_id": 0}))
