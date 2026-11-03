from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

cliente = MongoClient(os.getenv("MONGODB_URI"))
base_datos = cliente["techgear"]

<<<<<<< HEAD
productos_collection = base_datos["productos"]
pedidos_collection = base_datos["pedidos"]
usuarios_collection = base_datos["usuarios"]
=======
settings = Settings()

client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)

try:
    client.admin.command("ping")
    print("✅ Conexión exitosa a MongoDB Atlas")
    db = client.techgear_db
    
    # Colecciones
    productos_collection = db.productos
    pedidos_collection = db.pedidos
    usuarios_collection = db.usuarios  # ← Nueva colección para autenticación
    
except ConnectionFailure as e:
    print(f"❌ Error de conexión: {e}")
    client.close()
>>>>>>> e6e4704bc7c0245cbbd63bcbb0f8a3b5ec54bf50
