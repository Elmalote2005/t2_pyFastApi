from fastapi import FastAPI, HTTPException
from bson import ObjectId
from database import productos_collection, pedidos_collection, usuarios_collection
from models import Producto, ProductoUpdate, Pedido, PedidoUpdate, Usuario, UsuarioUpdate

app = FastAPI(
    title="TechGear - Sistema de Catálogo y Pedidos",
    description="API RESTful para gestión de productos, pedidos y usuarios",
    version="1.0.0"
)

# ---------------- PRODUCTOS ----------------
@app.get("/productos", tags=["Productos"])
def listar_productos():
    productos = list(productos_collection.find())
    for p in productos:
        p["_id"] = str(p["_id"])
    return {"productos": productos}

@app.get("/productos/{producto_id}", tags=["Productos"])
def obtener_producto(producto_id: str):
    producto = productos_collection.find_one({"_id": ObjectId(producto_id)})
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto["_id"] = str(producto["_id"])
    return producto

@app.post("/productos", tags=["Productos"])
def crear_producto(producto: Producto):
    nuevo = producto.model_dump()
    resultado = productos_collection.insert_one(nuevo)
    return {"mensaje": "Producto creado", "id": str(resultado.inserted_id)}

@app.put("/productos/{producto_id}", tags=["Productos"])
def actualizar_producto(producto_id: str, datos: ProductoUpdate):
    cambios = {k: v for k, v in datos.model_dump().items() if v is not None}
    if not cambios:
        raise HTTPException(status_code=400, detail="Sin datos para actualizar")
    res = productos_collection.update_one({"_id": ObjectId(producto_id)}, {"$set": cambios})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto actualizado"}

@app.delete("/productos/{producto_id}", tags=["Productos"])
def eliminar_producto(producto_id: str):
    res = productos_collection.delete_one({"_id": ObjectId(producto_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto eliminado"}

# ---------------- PEDIDOS ----------------
@app.get("/pedidos", tags=["Pedidos"])
def listar_pedidos():
    pedidos = list(pedidos_collection.find())
    for p in pedidos:
        p["_id"] = str(p["_id"])
    return {"pedidos": pedidos}

@app.get("/pedidos/{pedido_id}", tags=["Pedidos"])
def obtener_pedido(pedido_id: str):
    pedido = pedidos_collection.find_one({"_id": ObjectId(pedido_id)})
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    pedido["_id"] = str(pedido["_id"])
    return pedido

@app.post("/pedidos", tags=["Pedidos"])
def crear_pedido(pedido: Pedido):
    if not productos_collection.find_one({"_id": ObjectId(pedido.producto_id)}):
        raise HTTPException(status_code=404, detail="El producto no existe")
    nuevo = pedido.model_dump()
    resultado = pedidos_collection.insert_one(nuevo)
    return {"mensaje": "Pedido creado", "id": str(resultado.inserted_id)}

@app.put("/pedidos/{pedido_id}", tags=["Pedidos"])
def actualizar_pedido(pedido_id: str, datos: PedidoUpdate):
    cambios = {k: v for k, v in datos.model_dump().items() if v is not None}
    if not cambios:
        raise HTTPException(status_code=400, detail="Sin datos para actualizar")
    if "producto_id" in cambios:
        if not productos_collection.find_one({"_id": ObjectId(cambios["producto_id"])}):
            raise HTTPException(status_code=404, detail="El producto no existe")
    res = pedidos_collection.update_one({"_id": ObjectId(pedido_id)}, {"$set": cambios})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"mensaje": "Pedido actualizado"}

@app.delete("/pedidos/{pedido_id}", tags=["Pedidos"])
def eliminar_pedido(pedido_id: str):
    res = pedidos_collection.delete_one({"_id": ObjectId(pedido_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"mensaje": "Pedido eliminado"}

# ---------------- USUARIOS ----------------
@app.get("/usuarios", tags=["Usuarios"])
def listar_usuarios():
    usuarios = list(usuarios_collection.find({}, {"contraseña": 0}))
    for u in usuarios:
        u["_id"] = str(u["_id"])
    return {"usuarios": usuarios}

@app.get("/usuarios/{usuario_id}", tags=["Usuarios"])
def obtener_usuario(usuario_id: str):
    usuario = usuarios_collection.find_one({"_id": ObjectId(usuario_id)}, {"contraseña": 0})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario["_id"] = str(usuario["_id"])
    return usuario

@app.post("/usuarios", tags=["Usuarios"])
def crear_usuario(usuario: Usuario):
    existe = usuarios_collection.find_one({"correo": usuario.correo})
    if existe:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    nuevo = usuario.model_dump()
    resultado = usuarios_collection.insert_one(nuevo)
    return {"mensaje": "Usuario creado", "id": str(resultado.inserted_id)}

@app.put("/usuarios/{usuario_id}", tags=["Usuarios"])
def actualizar_usuario(usuario_id: str, datos: UsuarioUpdate):
    cambios = {k: v for k, v in datos.model_dump().items() if v is not None}
    if not cambios:
        raise HTTPException(status_code=400, detail="Sin datos para actualizar")
    if "correo" in cambios:
        existe = usuarios_collection.find_one({"correo": cambios["correo"]})
        if existe and str(existe["_id"]) != usuario_id:
            raise HTTPException(status_code=400, detail="El correo ya está en uso")
    res = usuarios_collection.update_one({"_id": ObjectId(usuario_id)}, {"$set": cambios})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario actualizado"}

@app.delete("/usuarios/{usuario_id}", tags=["Usuarios"])
def eliminar_usuario(usuario_id: str):
    res = usuarios_collection.delete_one({"_id": ObjectId(usuario_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado"}
