# 🛒 TechGear — Tienda en Línea

> 
> Tienda virtual desarrollada con **Django + FastAPI + MongoDB** como proyecto formativo de SENA.

---

## 🚀 Enlaces de Despliegue

Tabla

| Servicio | URL |
| --- | --- |
| 🌐 **Frontend (Vercel)** | [https://t2-py-fast-api.vercel.app](https://t2-py-fast-api.vercel.app) |
| ⚡ **API Backend (Render)** | [https://t2-pyfastapi-kmt2.onrender.com](https://t2-pyfastapi-kmt2.onrender.com) |
| 📚 **Documentación API (Swagger)** | [https://t2-pyfastapi-kmt2.onrender.com/docs](https://t2-pyfastapi-kmt2.onrender.com/docs) |

---

## 📋 Descripción del Proyecto

TechGear es una plataforma de comercio electrónico que permite a los usuarios explorar un catálogo de productos, registrarse, iniciar sesión, agregar productos al carrito y realizar pedidos. El proyecto está dividido en dos componentes principales:

- **Frontend:** Desarrollado con Django, plantillas HTML y CSS. Desplegado en Vercel.
- **Backend API:** Desarrollado con FastAPI. Desplegado en Render.
- **Base de Datos:** MongoDB Atlas — almacena usuarios, productos, carrito y pedidos.

---

## 👤 Usuarios y Acceso

### 🔑 Administrador

- **Correo:** `admin@techgear.com`
- **Contraseña:** `Admin12345`
- ✅ Se crea automáticamente al iniciar la API por primera vez.
- ⚠️ Solo el administrador puede crear y eliminar productos desde el panel de control.

### 👥 Usuarios Regulares

- **No requieren aprobación previa** ✅
- Cualquier persona puede registrarse libremente con su correo y contraseña
- Pueden navegar el catálogo, agregar al carrito y crear pedidos
- Al cerrar sesión, los productos del catálogo siguen visibles para todos los visitantes

---

## ✨ Funcionalidades Principales

- ✅ Página de inicio con presentación de la tienda
- ✅ Catálogo de productos cargados dinámicamente desde MongoDB
- ✅ Sistema de registro e inicio de sesión con autenticación por token
- ✅ Carrito de compras (agregar/eliminar/actualizar cantidades)
- ✅ Creación y visualización de pedidos
- ✅ Panel de administración exclusivo para gestionar productos
- ✅ Cerrar sesión y limpieza de sesión

---

## 🛠️ Tecnologías Utilizadas

Tabla

| Componente | Tecnología |
| --- | --- |
| **Frontend** | Django 5.0, HTML5, CSS3 |
| **Backend** | FastAPI, Python 3.11+ |
| **Base de Datos** | MongoDB Atlas |
| **Autenticación** | JWT (JSON Web Tokens) |
| **Despliegue Frontend** | Vercel |
| **Despliegue API** | Render |

---

## 📁 Estructura del Proyecto

```
techgear_web/          # Proyecto Django (Frontend)
├── store/             # Aplicación principal
│   ├── templates/     # Archivos HTML
│   ├── views.py       # Lógica de conexión con la API
│   └── urls.py        # Rutas del sitio
└── ...

techgear_api/          # FastAPI (Backend)
├── main.py           # Punto de entrada y rutas de la API
├── database.py       # Conexión con MongoDB
└── requirements.txt  # Dependencias de Python
```
