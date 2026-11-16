import requests
from django.shortcuts import render, redirect
from django.contrib import messages

API_URL = "https://t2-pyfastapi-kmt2onrender.com"


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
        password_form = request.POST.get("password", "")  # ✅ Corregido: era "contrasena"
        
        datos = {
            "correo": correo,
            "password": password_form
        }
        
        try:
            resp = requests.post(f"{API_URL}/login", json=datos, timeout=10)
            
            if resp.status_code == 200:
                usuario = resp.json()
                request.session["nombre"] = usuario.get("nombre", "")
                request.session["correo"] = usuario.get("correo", "")
                request.session["es_admin"] = usuario.get("es_admin", False)
                request.session["token"] = usuario.get("access_token", "")  # ✅ Guardamos el token
                
                if usuario.get("es_admin", False):
                    return redirect("panel_admin")
                else:
                    return redirect("inicio")
            else:
                return render(request, "login.html", {
                    "error": "Credenciales incorrectas. Verifica tus datos."
                })
        except Exception as e:
            print("❌ Error de conexion login:", e)
            return render(request, "login.html", {
                "error": "No se pudo conectar con el servidor. Verifica tu conexión e intenta nuevamente."
            })
    
    return render(request, "login.html")


def registro(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "")
        correo = request.POST.get("correo", "")
        password_form = request.POST.get("password", "")  # ✅ Corregido: era "contrasena"
        
        datos = {
            "nombre": nombre,
            "correo": correo,
            "password": password_form
        }
        
        try:
            resp = requests.post(f"{API_URL}/registro", json=datos, timeout=10)
            
            if resp.status_code in (200, 201):
                messages.success(request, "✅ Cuenta creada exitosamente. Inicia sesión.")
                return redirect("login")
            elif resp.status_code == 400:
                return render(request, "registro.html", {
                    "error": "Este correo ya está registrado."
                })
            else:
                return render(request, "registro.html", {
                    "error": "No se pudo completar el registro. Intenta más tarde."
                })
        except Exception as e:
            print("❌ Error de conexion registro:", e)
            return render(request, "registro.html", {
                "error": "No se pudo conectar con el servidor. Verifica tu conexión e intenta nuevamente."
            })
    
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
            if resp.status_code == 200:
                messages.success(request, "✅ Producto creado exitosamente")
            else:
                messages.error(request, "❌ No se pudo crear el producto")
        except Exception as e:
            print("Error crear producto:", e)
            messages.error(request, "❌ Error de conexión al crear producto")
    
    return redirect("panel_admin")


def eliminar_producto(request, producto_id):
    if not request.session.get("es_admin", False):
        return redirect("inicio")
    
    correo_admin = request.session.get("correo", "")
    
    try:
        resp = requests.delete(
            f"{API_URL}/productos/{producto_id}",
            params={"correo_admin": correo_admin},
            timeout=10
        )
        if resp.status_code == 200:
            messages.success(request, "✅ Producto eliminado")
        else:
            messages.error(request, "❌ No se pudo eliminar")
    except Exception as e:
        print("Error eliminar producto:", e)
        messages.error(request, "❌ Error de conexión")
    
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
            carrito = {"items": [], "total": 0}
    except Exception as e:
        print("Error ver carrito:", e)
        carrito = {"items": [], "total": 0}
    
    return render(request, "carrito.html", {"carrito": carrito})


def agregar_carrito(request):
    correo = request.session.get("correo", "")
    if not correo:
        return redirect("login")
    
    if request.method == "POST":
        producto_id = request.POST.get("producto_id")  # ✅ Desde POST, no desde URL
        cantidad = int(request.POST.get("cantidad", 1))
        
        if not producto_id:
            messages.error(request, "❌ Falta información del producto")
            return redirect("catalogo")
        
        try:
            resp = requests.post(
                f"{API_URL}/carrito/agregar",
                json={
                    "correo_usuario": correo,
                    "producto_id": producto_id,
                    "cantidad": cantidad
                },
                timeout=10
            )
            if resp.status_code == 200:
                messages.success(request, "✅ Agregado al carrito")
            else:
                messages.error(request, "❌ No se pudo agregar al carrito")
        except Exception as e:
            print("❌ Error agregar carrito:", e)
            messages.error(request, "❌ Error de conexión")
    
    return redirect("catalogo")


def eliminar_del_carrito(request, producto_id):
    correo = request.session.get("correo", "")
    if not correo:
        return redirect("login")
    
    try:
        resp = requests.post(
            f"{API_URL}/carrito/agregar",
            json={
                "correo_usuario": correo,
                "producto_id": producto_id,
                "cantidad": -9999  # ✅ Indicar que se elimina — o crear endpoint dedicado
            },
            timeout=10
        )
        messages.success(request, "✅ Eliminado del carrito")
    except Exception as e:
        print("❌ Error eliminar del carrito:", e)
        messages.error(request, "❌ No se pudo eliminar")
    
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
        if resp.status_code == 200:
            messages.success(request, "✅ Pedido creado exitosamente")
        else:
            messages.error(request, "❌ No se pudo crear el pedido")
    except Exception as e:
        print("❌ Error crear pedido:", e)
        messages.error(request, "❌ Error de conexión")
    
    return redirect("ver_pedidos")


def cerrar_sesion(request):
    request.session.flush()
    messages.success(request, "✅ Sesión cerrada correctamente")
    return redirect("inicio")
