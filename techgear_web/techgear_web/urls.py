<<<<<<< HEAD
﻿from django.contrib import admin
=======
"""
URL configuration for techgear_web project.
"""
from django.contrib import admin
>>>>>>> e6e4704bc7c0245cbbd63bcbb0f8a3b5ec54bf50
from django.urls import path
from store import views

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('cerrar/', views.cerrar_sesion, name='cerrar'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('tienda-admin/', views.panel_admin, name='panel_admin'),
    path('tienda-admin/crear/', views.crear_producto, name='crear_producto'),
    path('tienda-admin/editar/<str:id_producto>/', views.editar_producto, name='editar_producto'),
    path('tienda-admin/eliminar/<str:id_producto>/', views.eliminar_producto, name='eliminar_producto'),
=======
    path('', views.login, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login, name='login'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
>>>>>>> e6e4704bc7c0245cbbd63bcbb0f8a3b5ec54bf50
]
