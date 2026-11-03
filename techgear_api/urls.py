from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.RegistroUsuario.as_view(), name='registro'),
    path('login/', views.Login.as_view(), name='login'),
    path('cerrar-sesion/', views.CerrarSesion.as_view(), name='cerrar_sesion'),
]