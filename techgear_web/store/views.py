from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
import requests

API_URL = "https://techgear-api.onrender.com"

def inicio(request):
    return render(request, "inicio.html")

def registro(request):
    if request.method == "POST":
        datos = {
            "nombre": request.POST.get("nombre"),
            "correo": request.POST.get("correo"),
            "password": request.POST.get("password")
        }
        try:
            resp = requests.post(f"{API_URL}/registro", json=datos, timeout=15)
            if resp.status_code == 200:
                messages.success(request, "Cuenta creada. Inicia sesión.")
                return redirect("login")
            else:
                error = resp.json().get("detail", "Error al registrar")
                messages.error(request, error)
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    return render(request, "registro.html")

def iniciar_sesion(request):
    if request.method == "POST":
        datos = {
            "correo": request.POST.get("correo"),
            "password": request.POST.get("password")
        }
        try:
            resp = requests.post(f"{API_URL}/login", json=datos, timeout=15)
            if resp.status_code == 200:
                datos_resp = resp.json()
                usuario = datos_resp["usuario"]
                request.session["token"] = datos_resp["access_token"]
                request.session["usuario"] = usuario
                request.session["rol"] = usuario.get("rol", "usuario")
                messages.success(request, f"Bienvenido, {usuario['nombre']}")
                return redirect("catalogo")
            else:
                messages.error(request, "Credenciales incorrectas")
        except Exception as e:
            messages.error(request, f"Error de conexión: {str(e)}")
    return render(request, "login.html")

def cerrar_sesion(request):
    request.session.flush()
    logout(request)
    return redirect("inicio")

def catalogo(request):
    try:
        resp = requests.get(f"{API_URL}/productos", timeout=15)
        productos = resp.json().get("productos", [])
    except:
        productos = []
    return render(request, "catalogo.html", {"productos": productos, "rol": request.session.get("rol")})

def panel_admin(request):
    rol = request.session.get("rol")
    if rol != "admin":
        return render(request, "no_permitido.html")
    try:
        resp = requests.get(f"{API_URL}/productos", timeout=15)
        productos = resp.json().get("productos", [])
    except:
        productos = []
    return render(request, "panel_admin.html", {"productos": productos})

def crear_producto(request):
    if request.session.get("rol") != "admin":
        return render(request, "no_permitido.html")
    if request.method == "POST":
        datos = {
            "nombre": request.POST.get("nombre"),
            "descripcion": request.POST.get("descripcion"),
            "precio": float(request.POST.get("precio")),
            "stock": int(request.POST.get("stock")),
            "categoria": request.POST.get("categoria"),
            "imagen": request.POST.get("imagen")
        }
        requests.post(f"{API_URL}/productos", json=datos, timeout=15)
        return redirect("panel_admin")
    return render(request, "form_producto.html", {"accion": "Crear"})

def editar_producto(request, id_producto):
    if request.session.get("rol") != "admin":
        return render(request, "no_permitido.html")
    if request.method == "POST":
        datos = {
            "nombre": request.POST.get("nombre"),
            "descripcion": request.POST.get("descripcion"),
            "precio": float(request.POST.get("precio")),
            "stock": int(request.POST.get("stock")),
            "categoria": request.POST.get("categoria"),
            "imagen": request.POST.get("imagen")
        }
        requests.put(f"{API_URL}/productos/{id_producto}", json=datos, timeout=15)
        return redirect("panel_admin")
    return render(request, "form_producto.html", {"accion": "Editar", "id_producto": id_producto})

def eliminar_producto(request, id_producto):
    if request.session.get("rol") != "admin":
        return render(request, "no_permitido.html")
    requests.delete(f"{API_URL}/productos/{id_producto}", timeout=15)
    return redirect("panel_admin")
