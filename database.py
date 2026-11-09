from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import os

load_dotenv()

# URI de conexión — asegúrate de que el .env tenga:
# MONGODB_URI=mongodb+srv://<usuario>:<contraseña>@cluster0.bvjdyrp.mongodb.net/?retryWrites=true&w=majority

MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    # Si no tienes .env creado, pon aquí tu cadena directamente:
    MONGODB_URI = "mongodb+srv://administrador:admin@cluster0.bvjdyrp.mongodb.net/?retryWrites=true&w=majority"

try:
    cliente = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    cliente.admin.command("ping")
    print("✅ Conexión exitosa a MongoDB Atlas")
    
    base_datos = cliente["techgear"]
    
    productos_collection = base_datos["productos"]
    pedidos_collection = base_datos["pedidos"]
    usuarios_collection = base_datos["usuarios"]

except ConnectionFailure as e:
    print(f"❌ Error de conexión a MongoDB: {e}")
    raise
