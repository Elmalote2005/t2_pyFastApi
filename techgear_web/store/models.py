from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    rol = models.CharField(max_length=20, default="usuario",
                            choices=[("usuario", "Usuario"), ("admin", "Administrador")])
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
    stock = models.IntegerField(default=0)
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
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="pedidos")
    nombre_cliente = models.CharField(max_length=100)
    email_cliente = models.EmailField()
    direccion = models.CharField(max_length=255)
    estado = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default="pendiente")
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.nombre_cliente}"
