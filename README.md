# Elecciones Ballotage - Dinardi Challenge 🗳️

Este proyecto es una aplicación web para gestionar elecciones tipo ballotage, desarrollada como parte del **Dinardi Challenge**.

---

## 🛠️ Tecnologías utilizadas

- Python 3.11  
- Django  
- PostgreSQL  
- Docker & Docker Compose  
- Bootstrap 5
- Celery

---

## 🚀 Pasos para levantar la aplicación

1. **Iniciar Docker**

```bash
set -a
source .var_envs
docker compose up --build
```

2. **Ingresar al contenedor**

```bash
docker exec -it app_ballot bash
```

3. **Aplicar migraciones a la base de datos**

```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Crear superusuario para el panel de administración**

```bash
python manage.py createsuperuser
```

5. **Recolectar archivos estáticos**

```bash
python manage.py collectstatic
```

---

## 📂 Estructura del proyecto

```
├── ballot/                 # App principal
├── config/                 # Configuración general de Django
├── static/                 # Archivos estáticos
├── templates/              # Templates HTML
├── .var_envs               # Variables de entorno
├── docker-compose.yml      # Configuración de Docker Compose
├── Dockerfile              # Imagen de la app
└── manage.py
```

---

