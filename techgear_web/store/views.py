import requests
from django.shortcuts import render, redirect

API_URL = "http://127.0.0.1:8001"

def inicio(request):
    return render(request, "inicio.html")

def catalogo(request):
    try:
        resp = requests.get(f"{API_URL}/productos", timeout=10)
        if resp.status_code == 200:
            productos = resp.json()
            for p in productos:
                if "_id" in p:
                    p["id"] = str(p["_id"])
        else:
            productos = []
    except Exception as e:
        print("Error en catalogo:", e)
        productos = []
    return render(request, "catalogo.html", {"productos": productos})

def login(request):
    if request.method == "POST":
        correo = request.POST.get("correo", "")
        contraseña_form = request.POST.get("contrasena", "")
        
        datos = {
            "correo": correo,
            "password": contraseña_form
        }
        
        print("Enviando login:", datos)
        
        try:
            resp = requests.post(f"{API_URL}/login", json=datos, timeout=10)
            print("Respuesta API:", resp.status_code, resp.text)
            
            if resp.status_code == 200:
                usuario = resp.json()
                request.session["nombre"] = usuario.get("nombre", "")
                request.session["correo"] = usuario.get("correo", "")
                request.session["es_admin"] = usuario.get("es_admin", False)
                
                if usuario.get("es_admin", False):
                    return redirect("panel_admin")
                else:
                    return redirect("inicio")
                    
        except Exception as e:
            print("Error de conexion login:", e)
    
    return render(request, "login.html")

def registro(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "")
        correo = request.POST.get("correo", "")
        contraseña_form = request.POST.get("contrasena", "")
        
        datos = {
            "nombre": nombre,
            "correo": correo,
            "password": contraseña_form
        }
        
        print("Enviando registro:", datos)
        
        try:
            resp = requests.post(f"{API_URL}/registro", json=datos, timeout=10)
            print("Respuesta registro:", resp.status_code)
            if resp.status_code in (200, 201):
                return redirect("login")
        except Exception as e:
            print("Error de conexion registro:", e)
    
    return render(request, "registro.html")

def panel_admin(request):
    if not request.session.get("es_admin", False):
        return redirect("inicio")
    
    try:
        resp = requests.get(f"{API_URL}/productos", timeout=10)
        if resp.status_code == 200:
            productos = resp.json()
        else:
            productos = []
    except Exception as e:
        print("Error en panel:", e)
        productos = []
    
    return render(request, "panel_admin.html", {
        "nombre": request.session.get("nombre", ""),
        "productos": productos
    })

def crear_producto(request):
    if not request.session.get("es_admin", False):
        return redirect("inicio")
    
    if request.method == "POST":
        correo_admin = request.session.get("correo", "")
        datos = {
            "nombre": request.POST.get("nombre", ""),
            "descripcion": request.POST.get("descripcion", ""),
            "precio": float(request.POST.get("precio", 0)),
            "cantidad": int(request.POST.get("cantidad", 0)),
            "categoria": request.POST.get("categoria", ""),
            "imagen_url": request.POST.get("imagen_url", "")
        }
        
        try:
            resp = requests.post(
                f"{API_URL}/productos",
                json=datos,
                params={"correo_admin": correo_admin},
                timeout=10
            )
            print("Producto creado:", resp.status_code)
        except Exception as e:
            print("Error crear producto:", e)
    
    return redirect("panel_admin")

def eliminar_producto(request, producto_id):
    if not request.session.get("es_admin", False):
        return redirect("inicio")
    
    correo_admin = request.session.get("correo", "")
    
    try:
        resp = requests.post(
            f"{API_URL}/productos/eliminar",
            json={
                "correo_admin": correo_admin,
                "producto_id": producto_id
            },
            timeout=10
        )
        print("Producto eliminado:", resp.status_code)
    except Exception as e:
        print("Error eliminar producto:", e)
    
    return redirect("panel_admin")

def ver_pedidos(request):
    correo = request.session.get("correo", "")
    if not correo:
        return redirect("login")
    
    try:
        resp = requests.get(f"{API_URL}/pedidos/{correo}", timeout=10)
        if resp.status_code == 200:
            pedidos = resp.json()
        else:
            pedidos = []
    except Exception as e:
        print("Error ver pedidos:", e)
        pedidos = []
    
    return render(request, "pedidos_admin.html", {"pedidos": pedidos})

def ver_carrito(request):
    correo = request.session.get("correo", "")
    if not correo:
        return redirect("login")
    
    try:
        resp = requests.get(f"{API_URL}/carrito/{correo}", timeout=10)
        if resp.status_code == 200:
            carrito = resp.json()
        else:
            carrito = []
    except Exception as e:
        print("Error ver carrito:", e)
        carrito = []
    
    total = sum(item.get("precio", 0) * item.get("cantidad", 1) for item in carrito)
    
    return render(request, "carrito.html", {"carrito": carrito, "total": total})

def agregar_carrito(request, producto_id):
    correo = request.session.get("correo", "")
    if not correo:
        return redirect("login")
    
    try:
        resp = requests.post(
            f"{API_URL}/carrito/agregar",
            json={
                "correo_usuario": correo,
                "producto_id": producto_id,
                "cantidad": 1
            },
            timeout=10
        )
        print("✅ Agregado al carrito:", resp.status_code, resp.text)
    except Exception as e:
        print("❌ Error agregar carrito:", e)
    
    return redirect("ver_carrito")

def eliminar_del_carrito(request, item_id):
    correo = request.session.get("correo", "")
    if not correo:
        return redirect("login")
    
    try:
        resp = requests.post(
            f"{API_URL}/carrito/agregar",
            json={
                "correo_usuario": correo,
                "producto_id": item_id,
                "cantidad": -1
            },
            timeout=10
        )
        print("✅ Eliminado del carrito:", resp.status_code)
    except Exception as e:
        print("❌ Error eliminar item:", e)
    
    return redirect("ver_carrito")

def crear_pedido(request):
    correo = request.session.get("correo", "")
    if not correo:
        return redirect("login")
    
    try:
        resp = requests.post(
            f"{API_URL}/pedidos/crear",
            json={"correo_usuario": correo},
            timeout=10
        )
        print("✅ Pedido creado:", resp.status_code)
    except Exception as e:
        print("❌ Error crear pedido:", e)
    
    return redirect("ver_pedidos")

def cerrar_sesion(request):
    request.session.flush()
    return redirect("inicio")
