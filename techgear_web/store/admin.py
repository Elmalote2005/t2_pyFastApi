from django.contrib import admin
from .models import Usuario, Producto, Pedido

<<<<<<< HEAD
# Register your models here.
# Nota: Los datos de negocio se gestionan en MongoDB desde techgear_api/main.py
=======
admin.site.register(Usuario)
admin.site.register(Producto)
admin.site.register(Pedido)
>>>>>>> e6e4704bc7c0245cbbd63bcbb0f8a3b5ec54bf50
