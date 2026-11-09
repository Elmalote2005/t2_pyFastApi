from pymongo import MongoClient
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    MONGO_URI: str = os.getenv(
        "MONGODB_URI",
        "mongodb+srv://techgear_user:h7S3p2YBjXhOPB5b@cluster0.bvjdyrp.mongodb.net/?retryWrites=true&w=majority"
    )
    class Config:
        env_file = ".env"

settings = Settings()

client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)

try:
    client.admin.command("ping")
    print("✅ Conexión exitosa a MongoDB Atlas")
    db = client["techgear_db"]
    
    # Colecciones
    productos_collection = db["productos"]
    pedidos_collection = db["pedidos"]
    usuarios_collection = db["usuarios"]
    carrito_collection = db["carrito"]
    
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    raise
