from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('cerrar/', views.cerrar_sesion, name='cerrar'),
    path('catalogo/', views.catalogo, name='catalogo'),
    
    path('admin/', views.panel_admin, name='panel_admin'),
    path('admin/crear/', views.crear_producto, name='crear_producto'),
    path('admin/editar/<str:id_producto>/', views.editar_producto, name='editar_producto'),
    path('admin/eliminar/<str:id_producto>/', views.eliminar_producto, name='eliminar_producto'),
]
