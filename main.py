from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
import hashlib
import secrets
import os
from dotenv import load_dotenv

# Cargar credenciales desde .env o usar la directa
load_dotenv()
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://administrador:admin@cluster0.bvjdyrp.mongodb.net/?retryWrites=true&w=majority"
)
DB_NAME = os.getenv("DB_NAME", "techgear")

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=15000)
    db = client[DB_NAME]
    usuarios_col = db["usuarios"]
    productos_col = db["productos"]
    pedidos_col = db["pedidos"]
    carritos_col = db["carritos"]
    client.admin.command("ping")
    print("✅ CONECTADO A MONGODB ATLAS")
except Exception as e:
    print(f"ERROR DE CONEXIÓN: {e}")
    raise

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== Modelos ==========
class RegistroDatos(BaseModel):
    nombre: str
    correo: str
    contraseña: str

class LoginDatos(BaseModel):
    correo: str
    contraseña: str

class ProductoDatos(BaseModel):
    nombre: str
    descripcion: str = None
    precio: float
    cantidad: int
    categoria: str = "General"
    imagen_url: str = None

class ItemCarrito(BaseModel):
    producto_id: str
    nombre: str
    precio: float
    imagen_url: str = None
    cantidad: int = 1

# ========== Utilidades ==========
def hash_password_simple(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

# ========== Rutas públicas ==========
@app.get("/")
def inicio():
    return {"mensaje": "API funcionando correctamente"}

@app.post("/registro")
def registro(datos: RegistroDatos):
    existe = usuarios_col.find_one({"correo": datos.correo})
    if existe:
        raise HTTPException(400, detail="Este correo ya se encuentra registrado")
    
    rol_asignado = "admin" if datos.correo.endswith("@admin.com") else "usuario"
    
    nuevo = {
        "nombre": datos.nombre,
        "correo": datos.correo,
        "password": hash_password_simple(datos.contraseña),
        "rol": rol_asignado,
        "fecha_registro": datetime.utcnow()
    }
    usuarios_col.insert_one(nuevo)
    return {"mensaje": "Cuenta creada correctamente", "rol": rol_asignado}

@app.post("/login")
def login(datos: LoginDatos):
    usuario = usuarios_col.find_one({"correo": datos.correo})
    if not usuario or usuario["password"] != hash_password_simple(datos.contraseña):
        raise HTTPException(401, detail="Credenciales incorrectas")
    
    token = f"token_{secrets.token_hex(16)}"
    return {
        "access_token": token,
        "usuario": {
            "nombre": usuario["nombre"],
            "correo": usuario["correo"],
            "rol": usuario.get("rol", "usuario")
        }
    }

# ========== Productos ==========
@app.get("/productos")
def listar_productos():
    lista = []
    for p in productos_col.find():
        p["_id"] = str(p["_id"])
        # Asegurar compatibilidad de campos
        if "stock" in p and "cantidad" not in p:
            p["cantidad"] = p["stock"]
        if "imagen" in p and "imagen_url" not in p:
            p["imagen_url"] = p["imagen"]
        lista.append(p)
    return lista

@app.post("/productos")
def crear_producto(datos: ProductoDatos):
    nuevo = {
        "nombre": datos.nombre,
        "descripcion": datos.descripcion,
        "precio": datos.precio,
        "cantidad": datos.cantidad,
        "categoria": datos.categoria,
        "imagen_url": datos.imagen_url,
        "creado": datetime.utcnow()
    }
    resultado = productos_col.insert_one(nuevo)
    nuevo["_id"] = str(resultado.inserted_id)
    return {"mensaje": "Producto creado", "producto": nuevo}

@app.delete("/productos/{nombre}")
def eliminar_producto(nombre: str):
    resultado = productos_col.delete_one({"nombre": nombre})
    if resultado.deleted_count == 0:
        raise HTTPException(404, "Producto no encontrado")
    return {"mensaje": "Producto eliminado"}

# ========== Carrito ==========
@app.get("/carrito/{correo_usuario}")
def ver_carrito(correo_usuario: str):
    carrito = carritos_col.find_one({"correo_usuario": correo_usuario})
    if not carrito:
        return {"items": [], "total": 0}
    total = sum(item["precio"] * item["cantidad"] for item in carrito.get("items", []))
    return {"items": carrito.get("items", []), "total": total}

@app.post("/carrito/{correo_usuario}/agregar")
def agregar_al_carrito(correo_usuario: str, item: ItemCarrito):
    carrito = carritos_col.find_one({"correo_usuario": correo_usuario})
    if not carrito:
        carrito = {"correo_usuario": correo_usuario, "items": []}
    
    # Buscar si ya existe el producto
    existe = False
    for i in carrito["items"]:
        if i["producto_id"] == item.producto_id:
            i["cantidad"] += item.cantidad
            existe = True
            break
    if not existe:
        carrito["items"].append({
            "producto_id": item.producto_id,
            "nombre": item.nombre,
            "precio": item.precio,
            "imagen_url": item.imagen_url,
            "cantidad": item.cantidad
        })
    
    carritos_col.update_one(
        {"correo_usuario": correo_usuario},
        {"$set": {"items": carrito["items"]}},
        upsert=True
    )
    return {"mensaje": "Agregado al carrito"}

@app.delete("/carrito/{correo_usuario}/item/{producto_id}")
def eliminar_del_carrito(correo_usuario: str, producto_id: str):
    carrito = carritos_col.find_one({"correo_usuario": correo_usuario})
    if not carrito:
        raise HTTPException(404, "Carrito no encontrado")
    
    carrito["items"] = [i for i in carrito["items"] if i["producto_id"] != producto_id]
    
    carritos_col.update_one(
        {"correo_usuario": correo_usuario},
        {"$set": {"items": carrito["items"]}}
    )
    return {"mensaje": "Eliminado del carrito"}

# ========== Pedidos ==========
@app.post("/pedidos/{correo_usuario}/confirmar")
def confirmar_pedido(correo_usuario: str):
    carrito = carritos_col.find_one({"correo_usuario": correo_usuario})
    if not carrito or not carrito.get("items"):
        raise HTTPException(400, "El carrito está vacío")
    
    # Descontar stock
    for item in carrito["items"]:
        productos_col.update_one(
            {"nombre": item["nombre"]},
            {"$inc": {"cantidad": -item["cantidad"]}}
        )
    
    total = sum(i["precio"] * i["cantidad"] for i in carrito["items"])
    pedido = {
        "correo_usuario": correo_usuario,
        "items": carrito["items"],
        "total": total,
        "estado": "pendiente",
        "fecha": datetime.utcnow()
    }
    pedidos_col.insert_one(pedido)
    
    # Vaciar carrito
    carritos_col.delete_one({"correo_usuario": correo_usuario})
    return {"mensaje": "Pedido confirmado"}

# ========== Admin ==========
@app.get("/admin/pedidos")
def listar_pedidos():
    lista = []
    for p in pedidos_col.find():
        p["_id"] = str(p["_id"])
        p["usuario_correo"] = p.get("correo_usuario", "desconocido")
        lista.append(p)
    return lista
