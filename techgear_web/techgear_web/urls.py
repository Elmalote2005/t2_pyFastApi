"""
URL configuration for techgear_web project.
"""
"""
URL configuration for techgear_web project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),

    # Todas las rutas de la tienda están en store/urls.py
    path('', include('store.urls')),
]
