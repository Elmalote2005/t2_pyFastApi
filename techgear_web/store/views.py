from django.shortcuts import render, redirect
<<<<<<< HEAD
import requests

API_URL = "http://127.0.0.1:8001"

def es_admin(request):
    usuario = request.session.get("usuario")
    return usuario and usuario.get("rol") == "admin"

def inicio(request):
    return render(request, "inicio.html")

def registro(request):
    if request.method == "POST":
        datos = {
            "nombre": request.POST.get("nombre"),
            "correo": request.POST.get("correo"),
            "password": request.POST.get("password")
        }
        resp = requests.post(f"{API_URL}/registro", json=datos)
        if resp.status_code == 200:
            return redirect("login")
        return render(request, "registro.html", {"error": resp.json().get("detail", "Error al registrar")})
    return render(request, "registro.html")

def iniciar_sesion(request):
    if request.method == "POST":
        datos = {
            "correo": request.POST.get("correo"),
            "password": request.POST.get("password")
        }
        resp = requests.post(f"{API_URL}/login", json=datos)
        if resp.status_code == 200:
            request.session["usuario"] = resp.json()["usuario"]
            return redirect("catalogo")
        return render(request, "login.html", {"error": "Credenciales incorrectas"})
    return render(request, "login.html")

def cerrar_sesion(request):
    request.session.flush()
    return redirect("inicio")

def catalogo(request):
    resp = requests.get(f"{API_URL}/productos")
    productos = resp.json().get("productos", [])
    for p in productos:
        p["id"] = p.get("_id")
    return render(request, "catalogo.html", {
        "productos": productos,
        "usuario": request.session.get("usuario")
    })

def panel_admin(request):
    if not request.session.get("usuario"):
        return redirect("login")
    if not es_admin(request):
        return render(request, "no_permitido.html", {
            "mensaje": "Solo el administrador puede gestionar productos"
        })
    resp = requests.get(f"{API_URL}/productos")
    productos = resp.json().get("productos", [])
    for p in productos:
        p["id"] = p.get("_id")
    return render(request, "panel_admin.html", {"productos": productos})

def crear_producto(request):
    if not es_admin(request):
        return redirect("catalogo")
    if request.method == "POST":
        datos = {
            "nombre": request.POST.get("nombre"),
            "descripcion": request.POST.get("descripcion"),
            "precio": float(request.POST.get("precio")),
            "stock": int(request.POST.get("stock")),
            "categoria": request.POST.get("categoria"),
            "imagen": request.POST.get("imagen", "")
        }
        requests.post(f"{API_URL}/productos", json=datos)
        return redirect("panel_admin")
    return render(request, "form_producto.html", {"accion": "Crear"})

def editar_producto(request, id):
    if not es_admin(request):
        return redirect("catalogo")
    if request.method == "POST":
        datos = {
            "nombre": request.POST.get("nombre"),
            "descripcion": request.POST.get("descripcion"),
            "precio": float(request.POST.get("precio")),
            "stock": int(request.POST.get("stock")),
            "categoria": request.POST.get("categoria"),
            "imagen": request.POST.get("imagen", "")
        }
        requests.put(f"{API_URL}/productos/{id}", json=datos)
        return redirect("panel_admin")
    resp = requests.get(f"{API_URL}/productos")
    productos = resp.json().get("productos", [])
    producto = next((p for p in productos if p["_id"] == id), None)
    return render(request, "form_producto.html", {"accion": "Editar", "producto": producto, "id": id})

def eliminar_producto(request, id):
    if not es_admin(request):
        return redirect("catalogo")
    requests.delete(f"{API_URL}/productos/{id}")
    return redirect("panel_admin")
=======
from django.contrib import messages
import requests

API_BASE = "http://127.0.0.1:8001"

def registro(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        correo = request.POST.get("correo", "").strip()
        password = request.POST.get("password", "").strip()

        if not nombre or not correo or not password:
            messages.error(request, "Todos los campos son obligatorios")
            return render(request, "registro.html")

        try:
            respuesta = requests.post(
                f"{API_BASE}/registro",
                json={"nombre": nombre, "correo": correo, "password": password},
                timeout=15
            )
            if respuesta.status_code == 200:
                messages.success(request, "Cuenta creada correctamente. Inicia sesión")
                return redirect("login")
            else:
                try:
                    msg = respuesta.json().get("detail", "Error al crear la cuenta")
                except:
                    msg = "Error en el servidor"
                messages.error(request, msg)
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    
    return render(request, "registro.html")

def login(request):
    if request.method == "POST":
        correo = request.POST.get("correo", "").strip()
        password = request.POST.get("password", "").strip()

        try:
            respuesta = requests.post(
                f"{API_BASE}/login",
                json={"correo": correo, "password": password},
                timeout=15
            )
            if respuesta.status_code == 200:
                datos = respuesta.json()
                request.session["token"] = datos.get("access_token")
                request.session["usuario"] = datos.get("usuario", {})
                messages.success(request, f'Bienvenido {datos["usuario"]["nombre"]}')
                return redirect("catalogo")
            else:
                messages.error(request, "Correo o contraseña incorrectos")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    
    return render(request, "login.html")

def catalogo(request):
    try:
        respuesta = requests.get(f"{API_BASE}/productos", timeout=15)
        productos = respuesta.json().get("productos", []) if respuesta.status_code == 200 else []
    except:
        productos = []
        messages.warning(request, "No se pudieron cargar los productos")
    
    return render(request, "catalogo.html", {"productos": productos})

def cerrar_sesion(request):
    request.session.flush()
    messages.info(request, "Sesión cerrada correctamente")
    return redirect("login")
>>>>>>> e6e4704bc7c0245cbbd63bcbb0f8a3b5ec54bf50
