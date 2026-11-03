from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import os

load_dotenv()

try:
    cliente = MongoClient(os.getenv("MONGODB_URI"), serverSelectionTimeoutMS=5000)
    cliente.admin.command("ping")
    print("Conexión exitosa a MongoDB")
    base_datos = cliente["techgear"]
    
    productos_collection = base_datos["productos"]
    pedidos_collection = base_datos["pedidos"]
    usuarios_collection = base_datos["usuarios"]

except ConnectionFailure as e:
    print(f"Error de conexión: {e}")
