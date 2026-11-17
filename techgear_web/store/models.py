from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    rol = models.CharField(
        max_length=20,
        default="usuario",
        choices=[("usuario", "Usuario"), ("admin", "Administrador")]
    )
    is_active = models.BooleanField(default=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.FloatField()
    cantidad = models.IntegerField(default=0)  # ✅ Antes era 'stock' — coincide con formularios
    categoria = models.CharField(max_length=50)
    imagen_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    ESTADO_OPCIONES = [
        ("pendiente", "Pendiente"),
        ("enviado", "Enviado"),
        ("entregado", "Entregado"),
        ("cancelado", "Cancelado"),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="pedidos", null=True, blank=True)
    nombre_cliente = models.CharField(max_length=100)
    correo_usuario = models.EmailField()  # ✅ Antes era 'email_cliente' — coincide con plantillas
    direccion = models.CharField(max_length=255, blank=True, null=True)  # ✅ Opcional por ahora
    estado = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default="pendiente")
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.nombre_cliente}"


# ✅ Modelo necesario para registrar qué productos tiene cada pedido
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    nombre_producto = models.CharField(max_length=100)  # Guardamos el nombre en caso de que el producto se elimine
    precio = models.FloatField()
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad}x {self.nombre_producto}"
    
    def subtotal(self):
        return self.precio * self.cantidad
