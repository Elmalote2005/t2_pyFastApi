from django.shortcuts import render, redirect
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
