```
# 🛒 TechGear — Tienda en Línea
Aplicación web de comercio electrónico desarrollada con **FastAPI + Django + MongoDB**
> Autor: **Santiago Avendaño Zapata** — Estudiante de ADSO

---

## 📂 Estructura del Proyecto
```

t2_pyFastApi/
├── techgear_api/          # Backend — FastAPI
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── requirements.txt
└── techgear_web/          # Frontend — Django
├── manage.py
├── store/
│   ├── views.py
│   ├── models.py
│   ├── urls.py
│   └── templates/
├── techgear_web/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── vercel.json
└── requirements.txt

```

---

## 🔗 Enlaces del Proyecto
| Servicio | Plataforma | Enlace |
|---|---|---|
| **API (Backend)** | Render | *(Pendiente — se agrega mañana)* |
| **Web Django (Frontend)** | Vercel | *(Pendiente — se agrega mañana)* |
| **Repositorio GitHub** | GitHub | https://github.com/Elmalote2005/t2_pyFastApi |

---

## 🔑 Credenciales de Acceso

### 👑 Administrador
| Campo | Valor |
|---|---|
| **Correo** | administrador1@admin.com |
| **Contraseña** | Admin12345 |
| **Permisos** | Acceso al panel de administración, agregar/editar/eliminar productos, gestionar pedidos |

### 👤 Usuarios Registrados de Prueba
| Nombre | Correo | Contraseña | Rol |
|---|---|---|---|
| Carlos | carlos@correo.com | Carlos123 | Cliente |
| Wilson | wilson@correo.com | Wilson123 | Cliente |
| Jairo | jairo@correo.com | Jairo123 | Cliente |
| Fabiana | fabiana@correo.com | Fabiana123 | Cliente |

### 📋 Funcionalidades por Rol
- **Administrador** ✅ → Ver catálogo completo, agregar productos, gestionar pedidos, acceder al panel de control
- **Usuario registrado** ✅ → Navegar catálogo, agregar productos al carrito, realizar pedidos, ver historial de compras
- **Visitante** ⚠️ → Solo puede ver productos; debe iniciar sesión para comprar

---

## ⚙️ Tecnologías Utilizadas
- **Backend**: FastAPI + Python 3.12
- **Base de Datos**: MongoDB Atlas
- **Frontend**: Django 4.2 + HTML/CSS
- **Despliegue API**: Render
- **Despliegue Web**: Vercel
- **Control de Versiones**: Git + GitHub

---

## 🚀 Ejecución en Entorno Local

### 1. Levantar la API (terminal 1)
```bash
cd techgear_api
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

> 
> La API estará disponible en: `http://127.0.0.1:8001`

### 2. Levantar Django (terminal 2)

```
cd techgear_web
pip install -r requirements.txt
python manage.py runserver
```

> 
> La web estará disponible en: `http://127.0.0.1:8000`

---

## 📌 Notas Importantes

- La conexión con MongoDB Atlas se configura mediante la variable `MONGO_URI` en el archivo `database.py` de la API
- La variable `API_URL` en `settings.py` de Django apunta a la dirección de la API
- En producción, la API_URL se actualizará con el enlace público de Render
- Las contraseñas se almacenan encriptadas con SHA-256
- El despliegue en Vercel se configura mediante el archivo `vercel.json` en la carpeta `techgear_web/`

---

> 
> ✅ Proyecto en desarrollo — actualizaciones pendientes: enlaces públicos de Vercel y Render

```

---

## 📋 Cómo agregarlo al proyecto:
1. En la carpeta principal `t2_pyFastApi` → **New File** → nombre: `README.md`
2. Pega todo el bloque de arriba ✅
3. **Commit changes** → `git push`

¡Listo para mañana! Descansa bien y seguimos dejando todo perfecto 🔥💪
```
