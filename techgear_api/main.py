from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from pymongo import MongoClient
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

MONGODB_URI = "mongodb+srv://techgear_user:nZBVljAiCnmNoWVG@cluster0.bvjdyrp.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "techgear_db"

SECRET_KEY = "clave_secreta_techgear_2026_ultra_segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=15000)
    db = client[DB_NAME]
    usuarios_col = db["usuarios"]
    productos_col = db["productos"]
    client.admin.command("ping")
    print("✅ CONECTADO A MONGODB ATLAS")
except Exception as e:
    print(f"❌ ERROR: {e}")
    raise

app = FastAPI(title="TechGear API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    
    nuevo = {
        "nombre": datos.nombre,
        "correo": datos.correo,
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
    }

@app.get("/productos")
def listar_productos():
    lista = []
    for p in productos_col.find():
        p["_id"] = str(p["_id"])
        lista.append(p)
    if not lista:
        productos_ejemplo = [
            {"nombre": "Moto Deportiva 150cc", "descripcion": "Ideal para ciudad", "precio": 5200000, "stock": 15, "categoria": "Deportivas"},
            {"nombre": "Moto Trail 250cc", "descripcion": "Todo terreno", "precio": 6800000, "stock": 8, "categoria": "Aventura"},
            {"nombre": "Moto Urbana 125cc", "descripcion": "Económica y ágil", "precio": 3400000, "stock": 25, "categoria": "Urbanas"}
        ]
        productos_col.insert_many(productos_ejemplo)
        lista = list(productos_col.find())
        for p in lista: p["_id"] = str(p["_id"])
    return {"productos": lista}
