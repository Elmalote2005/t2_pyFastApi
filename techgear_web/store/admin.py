from django.contrib import admin
from .models import Usuario, Producto, Pedido

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'is_staff', 'date_joined')
    search_fields = ('nombre', 'correo')
    list_filter = ('is_staff', 'is_active')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'cantidad', 'categoria')
    search_fields = ('nombre', 'categoria')
    list_filter = ('categoria',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'correo_usuario', 'total', 'fecha')
    search_fields = ('correo_usuario',)
    list_filter = ('fecha',)
    readonly_fields = ('fecha',)
