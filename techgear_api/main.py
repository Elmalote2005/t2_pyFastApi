from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< HEAD
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
import hashlib
import secrets
=======
from pydantic import BaseModel, Field, EmailStr
from pymongo import MongoClient
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
>>>>>>> e6e4704bc7c0245cbbd63bcbb0f8a3b5ec54bf50

MONGODB_URI = "mongodb+srv://techgear_user:nZBVljAiCnmNoWVG@cluster0.bvjdyrp.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "techgear_db"

<<<<<<< HEAD
=======
SECRET_KEY = "clave_secreta_techgear_2026_ultra_segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

>>>>>>> e6e4704bc7c0245cbbd63bcbb0f8a3b5ec54bf50
try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=15000)
    db = client[DB_NAME]
    usuarios_col = db["usuarios"]
    productos_col = db["productos"]
    client.admin.command("ping")
<<<<<<< HEAD
    print("CONECTADO A MONGODB ATLAS")
except Exception as e:
    print(f"ERROR DE CONEXION: {e}")
    raise

app = FastAPI()
=======
    print("✅ CONECTADO A MONGODB ATLAS")
except Exception as e:
    print(f"❌ ERROR: {e}")
    raise

app = FastAPI(title="TechGear API")
>>>>>>> e6e4704bc7c0245cbbd63bcbb0f8a3b5ec54bf50

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< HEAD
class RegistroDatos(BaseModel):
    nombre: str
    correo: str
    password: str
    rol: str = "usuario"

class LoginDatos(BaseModel):
    correo: str
    password: str

class ProductoDatos(BaseModel):
    nombre: str
    descripcion: str = None
    precio: float
    stock: int
    categoria: str = None
    imagen: str = None

def hash_password_simple(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

@app.get("/")
def inicio():
    return {"mensaje": "API funcionando correctamente"}

@app.post("/registro")
def registro(datos: RegistroDatos):
    existe = usuarios_col.find_one({"correo": datos.correo})
    if existe:
        raise HTTPException(status_code=400, detail="El correo ya esta registrado")
    
    rol_asignado = "admin" if datos.correo.endswith("@admin.com") else "usuario"
=======
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class DatosRegistro(BaseModel):
    nombre: str
    correo: EmailStr
    password: str

class DatosLogin(BaseModel):
    correo: EmailStr
    password: str

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_token(data: dict):
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({**data, "exp": exp}, SECRET_KEY, algorithm=ALGORITHM)

@app.get("/")
def root():
    return {"mensaje": "API funcionando ✅"}

@app.post("/registro")
def registro(datos: DatosRegistro):
    if usuarios_col.find_one({"correo": datos.correo}):
        raise HTTPException(400, "El correo ya está registrado")
>>>>>>> e6e4704bc7c0245cbbd63bcbb0f8a3b5ec54bf50
    
    nuevo = {
        "nombre": datos.nombre,
        "correo": datos.correo,
<<<<<<< HEAD
        "password": hash_password_simple(datos.password),
        "rol": rol_asignado,
        "fecha_registro": datetime.utcnow()
    }
    usuarios_col.insert_one(nuevo)
    return {"mensaje": "Cuenta creada correctamente", "rol": rol_asignado}

@app.post("/login")
def login(datos: LoginDatos):
    usuario = usuarios_col.find_one({"correo": datos.correo})
    if not usuario or usuario["password"] != hash_password_simple(datos.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    token = f"token_{secrets.token_hex(16)}"
    return {
        "access_token": token,
        "usuario": {
            "nombre": usuario["nombre"],
            "correo": usuario["correo"],
            "rol": usuario.get("rol", "usuario")
        }
=======
        "password": hash_password(datos.password),
        "rol": "usuario",
        "is_active": True,
        "fecha_registro": datetime.utcnow()
    }
    res = usuarios_col.insert_one(nuevo)
    print(f"✅ Usuario guardado — {datos.correo}")
    return {"mensaje": "Cuenta creada correctamente ✅"}

@app.post("/login")
def login(datos: DatosLogin):
    u = usuarios_col.find_one({"correo": datos.correo})
    if not u or not verify_password(datos.password, u["password"]):
        raise HTTPException(401, "Credenciales incorrectas")
    
    token = create_token({"sub": u["correo"], "nombre": u["nombre"], "rol": u["rol"]})
    return {
        "access_token": token,
        "usuario": {"nombre": u["nombre"], "correo": u["correo"], "rol": u["rol"]}
>>>>>>> e6e4704bc7c0245cbbd63bcbb0f8a3b5ec54bf50
    }

@app.get("/productos")
def listar_productos():
    lista = []
    for p in productos_col.find():
        p["_id"] = str(p["_id"])
        lista.append(p)
    if not lista:
<<<<<<< HEAD
        productos_iniciales = [
            {"nombre": "Moto Deportiva 150cc", "descripcion": "Ideal para ciudad", "precio": 5200000, "stock": 15, "categoria": "Deportivas", "imagen": "/moto1.jpg"},
            {"nombre": "Moto Trail 250cc", "descripcion": "Todo terreno", "precio": 6800000, "stock": 8, "categoria": "Aventura", "imagen": "/moto2.jpg"},
            {"nombre": "Moto Urbana 125cc", "descripcion": "Economica y agil", "precio": 3400000, "stock": 25, "categoria": "Urbanas", "imagen": "/moto3.jpg"}
        ]
        productos_col.insert_many(productos_iniciales)
        lista = list(productos_col.find())
        for p in lista:
            p["_id"] = str(p["_id"])
    return {"productos": lista}

@app.post("/productos")
def crear_producto(datos: ProductoDatos):
    nuevo = {
        "nombre": datos.nombre,
        "descripcion": datos.descripcion,
        "precio": datos.precio,
        "stock": datos.stock,
        "categoria": datos.categoria,
        "imagen": datos.imagen,
        "creado": datetime.utcnow()
    }
    resultado = productos_col.insert_one(nuevo)
    nuevo["_id"] = str(resultado.inserted_id)
    return {"mensaje": "Producto creado", "producto": nuevo}

@app.put("/productos/{id_producto}")
def actualizar_producto(id_producto: str, datos: ProductoDatos):
    from bson import ObjectId
    actualizado = {
        "nombre": datos.nombre,
        "descripcion": datos.descripcion,
        "precio": datos.precio,
        "stock": datos.stock,
        "categoria": datos.categoria,
        "imagen": datos.imagen
    }
    resultado = productos_col.update_one({"_id": ObjectId(id_producto)}, {"$set": actualizado})
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto actualizado"}

@app.delete("/productos/{id_producto}")
def eliminar_producto(id_producto: str):
    from bson import ObjectId
    resultado = productos_col.delete_one({"_id": ObjectId(id_producto)})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto eliminado"}
=======
        productos_ejemplo = [
            {"nombre": "Moto Deportiva 150cc", "descripcion": "Ideal para ciudad", "precio": 5200000, "stock": 15, "categoria": "Deportivas"},
            {"nombre": "Moto Trail 250cc", "descripcion": "Todo terreno", "precio": 6800000, "stock": 8, "categoria": "Aventura"},
            {"nombre": "Moto Urbana 125cc", "descripcion": "Económica y ágil", "precio": 3400000, "stock": 25, "categoria": "Urbanas"}
        ]
        productos_col.insert_many(productos_ejemplo)
        lista = list(productos_col.find())
        for p in lista: p["_id"] = str(p["_id"])
    return {"productos": lista}
>>>>>>> e6e4704bc7c0245cbbd63bcbb0f8a3b5ec54bf50
