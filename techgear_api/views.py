from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
import hashlib
import jwt
from bson import ObjectId
from .database import get_database
from .models import Producto, ProductoUpdate, Pedido, PedidoUpdate, Usuario, LoginData

# 🔑 MISMA CLAVE que en main.py — importante para que los tokens funcionen
SECRET_KEY = "clave_secreta_techgear_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

router = APIRouter()

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

def crear_token(datos: dict, expira_en=ACCESS_TOKEN_EXPIRE_HOURS):
    payload = datos.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=expira_en)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@router.get("/")
def raiz():
    return {"mensaje": "API TechGear funcionando ✅"}


@router.post("/registro")
def registro(usuario: Usuario):
    db = get_database()
    usuarios_collection = db["usuarios"]
    
    existe = usuarios_collection.find_one({"correo": usuario.correo})
    if existe:
        raise HTTPException(400, "El correo ya está registrado")
    
    es_admin = usuario.correo.endswith("@admin.com")
    
    nuevo_usuario = {
        "nombre": usuario.nombre,
        "correo": usuario.correo,
        "password": hash_pw(usuario.password),  # ✅ Coincide con main.py
        "es_admin": es_admin,                     # ✅ Coincide con main.py
        "fecha_registro": datetime.utcnow()
    }
    usuarios_collection.insert_one(nuevo_usuario)
    return {"mensaje": "Usuario registrado ✅", "es_admin": es_admin}


@router.post("/login")
def login(datos: LoginData):
    db = get_database()
    usuarios_collection = db["usuarios"]
    
    usuario = usuarios_collection.find_one({"correo": datos.correo})
    if not usuario:
        raise HTTPException(401, "Credenciales incorrectas")
    
    if usuario["password"] != hash_pw(datos.password):  # ✅ Coincide con campo
        raise HTTPException(401, "Credenciales incorrectas")
    
    es_admin = usuario.get("es_admin", False)
    token = crear_token({
        "sub": str(usuario["_id"]),
        "correo": usuario["correo"],
        "nombre": usuario["nombre"],
        "es_admin": es_admin
    })
    return {
        "access_token": token,
        "token_type": "bearer",
        "nombre": usuario["nombre"],
        "correo": usuario["correo"],
        "es_admin": es_admin
    }


@router.get("/productos")
def listar_productos(limit: int = 100):
    db = get_database()
    productos_collection = db["productos"]
    productos = []
    for p in productos_collection.find().limit(limit):  # ✅ Límite para rendimiento
        p["id"] = str(p["_id"])
        del p["_id"]
        productos.append(p)
    return productos


@router.post("/productos")
def crear_producto(producto: Producto):
    db = get_database()
    productos_collection = db["productos"]
    nuevo = producto.model_dump()
    nuevo["fecha_creacion"] = datetime.utcnow()
    productos_collection.insert_one(nuevo)
    return {"mensaje": "Producto creado ✅", "producto": nuevo}


@router.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: str):
    db = get_database()
    productos_collection = db["productos"]
    resultado = productos_collection.delete_one({"_id": ObjectId(producto_id)})
    if resultado.deleted_count == 0:
        raise HTTPException(404, "Producto no encontrado")
    return {"mensaje": "Producto eliminado ✅"}


@router.get("/carrito/{correo_usuario}")
def ver_carrito(correo_usuario: str):
    db = get_database()
    carrito_collection = db["carrito"]
    carrito = carrito_collection.find_one({"correo_usuario": correo_usuario}, {"_id": 0})
    return carrito if carrito else {"items": [], "total": 0}


@router.post("/carrito/agregar")
def agregar_al_carrito(correo_usuario: str, producto_id: str, cantidad: int = 1):
    db = get_database()
    productos_collection = db["productos"]
    carrito_collection = db["carrito"]
    
    # Verificar que el producto existe
    producto = productos_collection.find_one({"_id": ObjectId(producto_id)})
    if not producto:
        raise HTTPException(404, "Producto no encontrado")
    
    carrito = carrito_collection.find_one({"correo_usuario": correo_usuario}) or {
        "correo_usuario": correo_usuario,
        "items": [],
        "total": 0
    }
    
    existe = False
    for i in carrito["items"]:
        if i["producto_id"] == producto_id:
            i["cantidad"] += cantidad
            existe = True
            break
    
    if not existe:
        carrito["items"].append({
            "producto_id": producto_id,
            "nombre_producto": producto["nombre"],
            "precio": producto["precio"],
            "imagen_url": producto.get("imagen_url"),
            "cantidad": cantidad
        })
    
    carrito["total"] = sum(i["precio"] * i["cantidad"] for i in carrito["items"])
    carrito_collection.update_one(
        {"correo_usuario": correo_usuario},
        {"$set": carrito},
        upsert=True
    )
    return {"mensaje": "Agregado al carrito ✅", "carrito": carrito}


@router.post("/pedidos/confirmar")
def confirmar_pedido(correo_usuario: str):
    db = get_database()
    carrito_collection = db["carrito"]
    pedidos_collection = db["pedidos"]
    productos_collection = db["productos"]
    
    carrito = carrito_collection.find_one({"correo_usuario": correo_usuario})
    if not carrito or not carrito.get("items"):
        raise HTTPException(400, "El carrito está vacío")
    
    pedido = {
        "correo_usuario": correo_usuario,
        "items": carrito["items"],
        "total": carrito["total"],
        "fecha": datetime.utcnow(),
        "estado": "pendiente"
    }
    resultado = pedidos_collection.insert_one(pedido)
    
    # Actualizar stock
    for item in carrito["items"]:
        productos_collection.update_one(
            {"nombre": item.get("nombre_producto")},
            {"$inc": {"cantidad": -item["cantidad"]}}
        )
    
    carrito_collection.delete_many({"correo_usuario": correo_usuario})
    return {
        "mensaje": "Pedido confirmado ✅",
        "pedido_id": str(resultado.inserted_id),
        "total": carrito["total"]
    }


@router.get("/pedidos/{correo_usuario}")
def ver_pedidos_usuario(correo_usuario: str):
    db = get_database()
    pedidos_collection = db["pedidos"]
    pedidos = list(pedidos_collection.find(
        {"correo_usuario": correo_usuario},
        {"_id": 0}
    ).sort("fecha", -1))
    return pedidos


@router.get("/admin/pedidos")
def ver_todos_pedidos():
    db = get_database()
    pedidos_collection = db["pedidos"]
    pedidos = list(pedidos_collection.find({}, {"_id": 0}).sort("fecha", -1))
    return pedidos
