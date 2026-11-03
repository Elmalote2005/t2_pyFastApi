"""
URL configuration for techgear_web project.
"""
from django.contrib import admin
from django.urls import path
from store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login, name='login'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
]
