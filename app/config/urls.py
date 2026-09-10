from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("cuenta/", include("accounts.urls")),
    path("profe/", include("teachers.urls")),
    path("colegio/", include("schools.urls")),
    path("evaluaciones/", include("evaluations.urls")),
]

# In DEBUG, Django serves media; in production Nginx handles /media/ and /static/.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
