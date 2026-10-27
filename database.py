from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

cliente = MongoClient(os.getenv("MONGODB_URI"))
base_datos = cliente["techgear"]

productos_collection = base_datos["productos"]
pedidos_collection = base_datos["pedidos"]
usuarios_collection = base_datos["usuarios"]
