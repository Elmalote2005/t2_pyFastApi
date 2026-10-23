from fastapi import FastAPI
from models.productos import ProductoModel, ProductoUpdateModel
from models.pedido import PedidoModel, PedidoUpdateModel
from database import productos_collection, pedidos_collection


app = FastAPI(
    title="TechGear API",
    description="Esquemas de Producto y Pedido con Pydantic",
    version="1.0.0"
)