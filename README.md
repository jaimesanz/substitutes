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

## Producción (Raspberry Pi)
Se sirve en **https://substitutes.jaimesa.nz/** con `docker-compose.prod.yml`, a través de un
Cloudflare Tunnel. Postgres, los respaldos, el túnel y Watchtower vienen del stack compartido del
host (`services/shared` en el repo `self_hosted`). Gunicorn corre la app, WhiteNoise sirve los
estáticos y el contenedor `media` sirve `/media/` desde el volumen `substitutes_media_volume`. Los
contenedores corren sin root, sin capabilities y con sistema de archivos de solo lectura, y `web` no
tiene acceso a internet.

1. En Postgres compartido, crea la base y el usuario, y las redes `substitutes-data` y
   `substitutes-tunnel` (ver el compose de `services/shared`).
2. En el servidor, junto al compose: `cp .env.production.example .env` y completa los secretos
   (`openssl rand -hex 32`). Sin ellos, compose no arranca.
3. `docker compose -f docker-compose.prod.yml up -d`.
4. En Cloudflare, en el túnel: `/media/*` a `http://substitutes-media:8080` y el resto a
   `http://substitutes-web:8000`.

Si la app se sirve bajo una ruta, `DJANGO_SCRIPT_NAME` hace que Django agregue el prefijo a todas
sus URLs y limite las cookies a esa ruta. Los enlaces en plantillas van siempre con `{% url %}`; un
test falla si aparece un `href="/..."` literal.

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
interna, envío real de emails (invitaciones hoy son por enlace),
calendario de disponibilidad avanzado, almacenamiento de archivos en S3.
