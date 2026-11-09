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
                p["id"] = str(p.get("_id", ""))
        else:
            productos = []
    except Exception:
        productos = []
    return render(request, "catalogo.html", {"productos": productos})

def login(request):
    if request.method == "POST":
        correo = request.POST.get("correo", "")
        contraseña = request.POST.get("contraseña", "")
        datos = {"correo": correo, "password": contraseña}
        try:
            resp = requests.post(f"{API_URL}/login", json=datos, timeout=10)
            if resp.status_code == 200:
                return redirect("catalogo")
        except Exception:
            pass
    return render(request, "login.html")

def registro(request):
    if request.method == "POST":
        datos = {
            "nombre": request.POST.get("nombre", ""),
            "correo": request.POST.get("correo", ""),
            "password": request.POST.get("contraseña", "")
        }
        try:
            requests.post(f"{API_URL}/registro", json=datos, timeout=10)
            return redirect("login")
        except Exception:
            pass
    return render(request, "registro.html")
