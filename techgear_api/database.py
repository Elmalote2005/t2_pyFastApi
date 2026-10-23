from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str

    class Config:
        env_file = ".env"

settings = Settings()

client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)

try:
    client.admin.command("ping")
    print("Conexion exitosa a MongoDB Atlas")
    db = client.techgear_db
    productos_collection = db.productos
    pedidos_collection = db.pedidos
except ConnectionFailure as e:
    print(f"Error de conexion: {e}")