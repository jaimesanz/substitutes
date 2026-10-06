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

## Producción (EC2 compartida)
Se sirve en **https://jaimesa.nz/substitutes/** con `docker-compose.prod.yml`, detrás del
Caddy compartido del host (repo `load-balancer`), que tiene los puertos 80/443, el certificado
TLS y sirve `/substitutes/media/` desde el volumen `substitutes_media_volume`. La app se une a la
red Docker externa `edge` como `substitutes-web`; Gunicorn corre la app y WhiteNoise sirve los
estáticos.

1. En el servidor, junto al compose: `cp .env.production.example .env` y completa los secretos
   (`openssl rand -hex 32`). Sin ellos, compose no arranca.
2. `docker network create edge` (una vez por host) y `docker compose -f docker-compose.prod.yml up -d`.
3. En el repo `load-balancer`: el bloque `handle_path /substitutes/*` de `jaimesa.nz`.

`DJANGO_SCRIPT_NAME=/substitutes` hace que Django agregue el prefijo a todas sus URLs y limite
las cookies a esa ruta. Sin él (desarrollo), la app vive en la raíz. Los enlaces en plantillas
van siempre con `{% url %}`; un test falla si aparece un `href="/..."` literal.

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
