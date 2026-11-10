from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
from bson import ObjectId
import hashlib
import jwt
from datetime import datetime, timedelta

# Conexión a MongoDB Atlas
MONGO_URI = "mongodb+srv://techgear_user:h7S3p2YBjXhOPB5b@cluster0.bvjdyrp.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client["techgear_db"]
usuarios_collection = db["usuarios"]
productos_collection = db["productos"]
carrito_collection = db["carrito"]
pedidos_collection = db["pedidos"]

try:
    client.admin.command("ping")
    print("✅ Conexion exitosa a MongoDB Atlas")
except Exception as e:
    print("❌ Error de conexion:", e)

SECRET_KEY = "clave_secreta_techgear_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

def crear_token(datos: dict):
    payload = datos.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

app = FastAPI(title="TechGear API")

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
@app.post("/registro")
def registro(datos: RegistroData):
    existe = usuarios_collection.find_one({"correo": datos.correo})
    if existe:
        raise HTTPException(400, "El correo ya esta registrado")
    
    es_admin = (datos.correo == "admin@techgear.com")
    
    usuario = {
        "nombre": datos.nombre,
        "correo": datos.correo,
        "password": hash_pw(datos.password),
        "es_admin": es_admin,
        "fecha_registro": datetime.utcnow()
    }
    usuarios_collection.insert_one(usuario)
    return {"mensaje": "Usuario registrado exitosamente", "correo": datos.correo}

@app.post("/login")
def login(datos: LoginData):
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
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "nombre": usuario["nombre"],
        "correo": usuario["correo"],
        "es_admin": usuario.get("es_admin", False)
    }

# === PRODUCTOS ===
@app.get("/productos")
def listar_productos():
    productos = list(productos_collection.find())
    for p in productos:
        p["id"] = str(p["_id"])
        del p["_id"]
    return productos

@app.post("/productos")
def crear_producto(datos: ProductoData, correo_admin: str):
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
    productos_collection.insert_one(producto)
    return {"mensaje": "Producto creado", "producto": producto}

# === CARRITO — CORREGIDO para recibir JSON desde Django ===
@app.post("/carrito/agregar")
def agregar_carrito(datos: CarritoAgregar):
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
    else:
        carrito_collection.insert_one({
            "correo_usuario": datos.correo_usuario,
            "producto_id": datos.producto_id,
            "nombre_producto": producto["nombre"],
            "precio": producto["precio"],
            "cantidad": datos.cantidad,
            "imagen_url": producto.get("imagen_url")
        })
    return {"mensaje": "Agregado al carrito ✅"}

@app.get("/carrito/{correo_usuario}")
def ver_carrito(correo_usuario: str):
    items = list(carrito_collection.find({"correo_usuario": correo_usuario}))
    for item in items:
        item["id"] = str(item["_id"])
        del item["_id"]
    return items

# === PEDIDOS ===
@app.post("/pedidos/crear")
def crear_pedido(correo_usuario: str):
    carrito = list(carrito_collection.find({"correo_usuario": correo_usuario}))
    if not carrito:
        raise HTTPException(400, "El carrito esta vacio")
    
    total = sum(item["precio"] * item["cantidad"] for item in carrito)
    pedido = {
        "correo_usuario": correo_usuario,
        "items": carrito,
        "total": total,
        "estado": "pendiente",
        "fecha": datetime.utcnow()
    }
    pedidos_collection.insert_one(pedido)
    
    carrito_collection.delete_many({"correo_usuario": correo_usuario})
    return {"mensaje": "Pedido creado", "total": total}

@app.get("/pedidos/{correo_usuario}")
def ver_pedidos(correo_usuario: str):
    pedidos = list(pedidos_collection.find({"correo_usuario": correo_usuario}).sort("fecha", -1))
    for p in pedidos:
        p["id"] = str(p["_id"])
        del p["_id"]
    return pedidos

# === CREAR ADMIN AUTOMÁTICAMENTE ===
@app.on_event("startup")
def crear_admin_si_no_existe():
    admin = usuarios_collection.find_one({"correo": "admin@techgear.com"})
    if not admin:
        usuarios_collection.insert_one({
            "nombre": "Administrador TechGear",
            "correo": "admin@techgear.com",
            "password": hash_pw("Admin12345"),
            "es_admin": True,
            "fecha_registro": datetime.utcnow()
        })
        print("✅ Administrador creado: admin@techgear.com / Admin12345")
    else:
        print("✅ Administrador ya existe en la base de datos")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
