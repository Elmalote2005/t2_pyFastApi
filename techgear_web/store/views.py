from django.shortcuts import render, redirect
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
