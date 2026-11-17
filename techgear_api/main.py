import hashlib
import logging
from datetime import datetime, timedelta
from threading import Lock

import jwt
from bson import ObjectId
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from pymongo.errors import PyMongoError

if __package__:
    from .database import get_database
    from .exceptions import DatabaseError
else:
    from database import get_database
    from exceptions import DatabaseError

SECRET_KEY = "clave_secreta_techgear_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_admin_initialized = False
_admin_lock = Lock()

# ─── Configuración de la aplicación ───
app = FastAPI(title="TechGear API", version="1.0.0")

# 🔓 CORS — PERMITE QUE VERCEL HABLE CON RENDER
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción reemplaza con tu dominio real: "https://tu-app.vercel.app"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Funciones auxiliares ───
def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

def crear_token(datos: dict):
    payload = datos.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def init_admin_db():
    """Inicializa usuario admin una sola vez. Devuelve la instancia de BD"""
    global _admin_initialized
    db = get_database()
    
    if not _admin_initialized:
        with _admin_lock:
            if not _admin_initialized:
                usuarios_collection = db["usuarios"]
                admin = usuarios_collection.find_one({"correo": "admin@techgear.com"})
                if not admin:
                    usuarios_collection.insert_one({
                        "nombre": "Administrador TechGear",
                        "correo": "admin@techgear.com",
                        "password": hash_pw("Admin12345"),
                        "es_admin": True,
                        "fecha_registro": datetime.utcnow()
                    })
                    logger.info("✅ Usuario admin creado")
                _admin_initialized = True
    return db

# ─── Manejadores de errores ───
@app.exception_handler(DatabaseError)
async def database_error_handler(request: Request, exc: DatabaseError):
    logger.error("%s (path=%s)", exc, request.url.path)
    return JSONResponse(status_code=503, content={"detail": str(exc)})

@app.exception_handler(PyMongoError)
async def pymongo_error_handler(request: Request, exc: PyMongoError):
    logger.error(
        "MongoDB operation failed (%s, path=%s)",
        type(exc).__name__,
        request.url.path,
        exc_info=(type(exc), exc, exc.__traceback__),
    )
    return JSONResponse(
        status_code=503,
        content={"detail": "No fue posible completar la operación en MongoDB."},
    )

# ─── Rutas de verificación ───
@app.get("/")
def root():
    return {"mensaje": "API de TechGear funcionando correctamente ✅", "docs": "/docs", "estado": "activo"}

@app.get("/health")
def health_check():
    try:
        db = get_database()
        db.command("ping")
        return {"estado": "ok", "base_datos": "conectada"}
    except Exception as e:
        return {"estado": "error", "detalle": str(e)}

# === MODELOS ===
class RegistroData(BaseModel):
    nombre: str
    correo: EmailStr
    password: str

class LoginData(BaseModel):
    correo: EmailStr
    password: str

class ProductoData(BaseModel):
    nombre: str
    descripcion: str = None
    precio: float
    cantidad: int = 0
    categoria: str
    imagen_url: str = None

class CarritoAgregar(BaseModel):
    correo_usuario: str
    producto_id: str
    cantidad: int = 1

# === AUTENTICACIÓN ===
@app.on_event("startup")
async def startup_event():
    """Se ejecuta una sola vez al iniciar la API"""
    init_admin_db()

@app.post("/registro")
def registro(datos: RegistroData):
    db = init_admin_db()
    usuarios_collection = db["usuarios"]
    
    existe = usuarios_collection.find_one({"correo": datos.correo})
    if existe:
        raise HTTPException(400, "El correo ya está registrado")
    
    es_admin = (datos.correo == "admin@techgear.com")
    
    usuario = {
        "nombre": datos.nombre,
        "correo": datos.correo,
        "password": hash_pw(datos.password),
        "es_admin": es_admin,
        "fecha_registro": datetime.utcnow()
    }
    usuarios_collection.insert_one(usuario)
    logger.info(f"✅ Usuario registrado: {datos.correo}")
    return {"mensaje": "Usuario registrado exitosamente", "correo": datos.correo}

@app.post("/login")
def login(datos: LoginData):
    db = init_admin_db()
    usuarios_collection = db["usuarios"]
    
    usuario = usuarios_collection.find_one({"correo": datos.correo})
    if not usuario:
        raise HTTPException(401, "Credenciales incorrectas")
    
    if usuario["password"] != hash_pw(datos.password):
        raise HTTPException(401, "Credenciales incorrectas")
    
    token = crear_token({
        "id": str(usuario["_id"]),
        "correo": usuario["correo"],
        "nombre": usuario["nombre"],
        "es_admin": usuario.get("es_admin", False)
    })
    
    logger.info(f"✅ Inicio de sesión: {datos.correo}")
    return {
        "access_token": token,
        "token_type": "bearer",
        "nombre": usuario["nombre"],
        "correo": usuario["correo"],
        "es_admin": usuario.get("es_admin", False)
    }

# === PRODUCTOS ===
@app.get("/productos")
def listar_productos(limit: int = 100):
    """Lista productos con límite opcional para mejor rendimiento"""
    db = init_admin_db()
    productos_collection = db["productos"]
    productos = list(productos_collection.find().limit(limit))
    for p in productos:
        p["id"] = str(p["_id"])
        del p["_id"]
    return productos

@app.post("/productos")
def crear_producto(datos: ProductoData, correo_admin: str):
    db = init_admin_db()
    usuarios_collection = db["usuarios"]
    productos_collection = db["productos"]
    
    admin = usuarios_collection.find_one({"correo": correo_admin})
    if not admin or not admin.get("es_admin", False):
        raise HTTPException(403, "Solo el administrador puede crear productos")
    
    producto = {
        "nombre": datos.nombre,
        "descripcion": datos.descripcion,
        "precio": datos.precio,
        "cantidad": datos.cantidad,
        "categoria": datos.categoria,
        "imagen_url": datos.imagen_url,
        "creado_por": correo_admin,
        "fecha": datetime.utcnow()
    }
    resultado = productos_collection.insert_one(producto)
    logger.info(f"✅ Producto creado: {datos.nombre}")
    return {"mensaje": "Producto creado", "id": str(resultado.inserted_id), "producto": producto}

# === CARRITO ===
@app.post("/carrito/agregar")
def agregar_carrito(datos: CarritoAgregar):
    db = init_admin_db()
    productos_collection = db["productos"]
    carrito_collection = db["carrito"]
    
    producto = productos_collection.find_one({"_id": ObjectId(datos.producto_id)})
    if not producto:
        raise HTTPException(404, "Producto no encontrado")
    
    existe = carrito_collection.find_one({
        "correo_usuario": datos.correo_usuario,
        "producto_id": datos.producto_id
    })
    
    if existe:
        carrito_collection.update_one(
            {"_id": existe["_id"]},
            {"$inc": {"cantidad": datos.cantidad}}
        )
        mensaje = "Cantidad actualizada en el carrito ✅"
    else:
        carrito_collection.insert_one({
            "correo_usuario": datos.correo_usuario,
            "producto_id": datos.producto_id,
            "nombre_producto": producto["nombre"],
            "precio": producto["precio"],
            "cantidad": datos.cantidad,
            "imagen_url": producto.get("imagen_url")
        })
        mensaje = "Agregado al carrito ✅"
    
    return {"mensaje": mensaje}

@app.get("/carrito/{correo_usuario}")
def ver_carrito(correo_usuario: str):
    db = init_admin_db()
    carrito_collection = db["carrito"]
    items = list(carrito_collection.find({"correo_usuario": correo_usuario}))
    for item in items:
        item["id"] = str(item["_id"])
        del item["_id"]
    return items

# === PEDIDOS ===
@app.post("/pedidos/crear")
def crear_pedido(correo_usuario: str):
    db = init_admin_db()
    carrito_collection = db["carrito"]
    pedidos_collection = db["pedidos"]
    
    carrito = list(carrito_collection.find({"correo_usuario": correo_usuario}))
    if not carrito:
        raise HTTPException(400, "El carrito está vacío")
    
    total = sum(item["precio"] * item["cantidad"] for item in carrito)
    pedido = {
        "correo_usuario": correo_usuario,
        "items": carrito,
        "total": total,
        "estado": "pendiente",
        "fecha": datetime.utcnow()
    }
    resultado = pedidos_collection.insert_one(pedido)
    
    carrito_collection.delete_many({"correo_usuario": correo_usuario})
    logger.info(f"✅ Pedido creado para: {correo_usuario}")
    return {"mensaje": "Pedido creado", "id": str(resultado.inserted_id), "total": total}

@app.get("/pedidos/{correo_usuario}")
def ver_pedidos(correo_usuario: str):
    db = init_admin_db()
    pedidos_collection = db["pedidos"]
    pedidos = list(pedidos_collection.find({"correo_usuario": correo_usuario}).sort("fecha", -1))
    for p in pedidos:
        p["id"] = str(p["_id"])
        del p["_id"]
    return pedidos

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
