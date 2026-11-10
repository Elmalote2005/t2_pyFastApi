from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("catalogo/", views.catalogo, name="catalogo"),
    path("login/", views.login, name="login"),
    path("registro/", views.registro, name="registro"),
    path("panel-admin/", views.panel_admin, name="panel_admin"),
    path("crear-producto/", views.crear_producto, name="crear_producto"),
    path("eliminar-producto/<str:producto_id>/", views.eliminar_producto, name="eliminar_producto"),
    path("pedidos/", views.ver_pedidos, name="ver_pedidos"),
    path("carrito/", views.ver_carrito, name="ver_carrito"),
    path("carrito/agregar/<str:producto_id>/", views.agregar_carrito, name="agregar_carrito"),
    path("carrito/eliminar/<str:item_id>/", views.eliminar_del_carrito, name="eliminar_del_carrito"),
    path("pedidos/crear/", views.crear_pedido, name="crear_pedido"),
    path("cerrar-sesion/", views.cerrar_sesion, name="cerrar_sesion"),  # ✅ Nueva
]
