# Reemplazos de Profes — MVP

Base de datos de **profesores para reemplazos**, evaluados por una sicóloga laboral,
que los colegios pueden filtrar y contactar. Django + PostgreSQL + Docker, lista para
desplegar en una instancia EC2 con `docker compose`.

## Roles
- **Postulante (profe):** crea su perfil, sube títulos/certificados, define disponibilidad y preferencias.
- **Evaluador/a (sicóloga):** revisa y aprueba/rechaza cada perfil (estado + puntaje + notas).
- **Colegio:** organización con varios miembros; busca y filtra profes **aprobados** y ve su contacto.
- **Admin:** superusuario (Django admin); incluye funciones de ventas/operaciones por ahora.

Los colegios ven **solo** perfiles con evaluación *aprobada*.

## Stack
Django 5 (templates + Bootstrap 5) · PostgreSQL 16 · Gunicorn · Nginx · Docker Compose.

## Correr localmente
```bash
cp .env.example .env      # edita SECRET_KEY, contraseñas, superusuario
docker compose up -d --build
```
Abre http://localhost

El arranque aplica migraciones, junta estáticos, siembra regiones/comunas/asignaturas
(`manage.py seed`) y crea el superusuario definido en `.env`.

### Datos de demostración (opcional)
```bash
docker compose exec web python manage.py demo
```
Crea profes de ejemplo (aprobados y pendientes), una evaluadora y un colegio.
Contraseña de todas las cuentas demo: `demo1234`. Cuentas: `colegio@demo.cl`,
`evaluadora@demo.cl`, `ana@demo.cl`, etc.

## Desplegar en EC2
1. Instala Docker + plugin Compose en la instancia.
2. Clona el repo y crea `.env` con valores de producción:
   - `DEBUG=0`
   - `ALLOWED_HOSTS=tu-dominio.cl,tu-ec2-public-dns`
   - `CSRF_TRUSTED_ORIGINS=https://tu-dominio.cl`
   - contraseñas fuertes para Postgres y el superusuario.
3. `docker compose up -d --build`
4. Abre el puerto **80** (y 443 al agregar HTTPS) en el security group.

Nginx sirve `/static/` y `/media/`; Gunicorn corre la app. Los volúmenes
`postgres_data`, `static_volume` y `media_volume` persisten datos y archivos subidos.

### Comandos útiles
```bash
docker compose logs -f web                       # logs
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py seed    # re-sembrar catálogo (idempotente)
docker compose down                              # detener (los volúmenes persisten)
```

## Estructura
```
app/
  config/       # settings, urls, wsgi
  accounts/     # User custom (login por email), registro
  catalog/      # Region, Comuna, Subject + comando seed
  teachers/     # TeacherProfile, Certificate, panel del profe
  schools/      # School, Membership, Invitation, directorio + filtros
  evaluations/  # Evaluation + flujo de la evaluadora
  core/         # landing, mixins de rol, comando demo
  templates/    # HTML (Bootstrap 5, en español)
nginx/          # reverse proxy
docker-compose.yml
```

## Pendiente (fuera del MVP)
Pagos/suscripciones, aprobación de colegios, rol de ventas dedicado, mensajería
interna, envío real de emails (invitaciones hoy son por enlace), HTTPS/Let's Encrypt,
calendario de disponibilidad avanzado, almacenamiento de archivos en S3.
