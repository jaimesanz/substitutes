from django.conf import settings
from django.db import models


def certificate_upload_path(instance, filename):
    return f"certificates/user_{instance.profile.user_id}/{filename}"


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
    )

    # --- Personal / contact ---
    full_name = models.CharField("nombre completo", max_length=200)
    phone = models.CharField("teléfono de contacto", max_length=30, blank=True)
    contact_email = models.EmailField("email de contacto", blank=True)
    birth_date = models.DateField("fecha de nacimiento", null=True, blank=True)
    bio = models.TextField("presentación", blank=True,
                           help_text="Cuéntale al colegio sobre tu experiencia.")

    # --- Location ---
    region = models.ForeignKey(
        "catalog.Region", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="teachers", verbose_name="región de residencia",
    )
    comuna = models.ForeignKey(
        "catalog.Comuna", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="teachers", verbose_name="comuna de residencia",
    )
    preferred_comunas = models.ManyToManyField(
        "catalog.Comuna", blank=True, related_name="preferred_by_teachers",
        verbose_name="comunas donde prefiero trabajar",
    )

    # --- Professional ---
    subjects = models.ManyToManyField(
        "catalog.Subject", blank=True, related_name="teachers",
        verbose_name="asignaturas que puedo cubrir",
    )
    is_bilingual = models.BooleanField("bilingüe", default=False)
    languages = models.CharField(
        "idiomas", max_length=200, blank=True,
        help_text="Ej: Inglés (avanzado), Francés (intermedio).",
    )

    # --- Replacement type preference ---
    available_short = models.BooleanField("reemplazos cortos (días/semanas)", default=True)
    available_long = models.BooleanField("reemplazos largos (meses)", default=True)

    # --- Availability ---
    available_mon = models.BooleanField("lunes", default=True)
    available_tue = models.BooleanField("martes", default=True)
    available_wed = models.BooleanField("miércoles", default=True)
    available_thu = models.BooleanField("jueves", default=True)
    available_fri = models.BooleanField("viernes", default=True)
    available_from = models.DateField("disponible desde", null=True, blank=True)
    availability_notes = models.CharField("notas de disponibilidad", max_length=300, blank=True)

    # --- Visibility ---
    is_active = models.BooleanField(
        "perfil activo", default=True,
        help_text="Desactívalo si por ahora no quieres aparecer para los colegios.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "perfil de profe"
        verbose_name_plural = "perfiles de profes"

    def __str__(self):
        return self.full_name or self.user.email

    @property
    def available_weekdays(self):
        days = [
            ("Lun", self.available_mon), ("Mar", self.available_tue),
            ("Mié", self.available_wed), ("Jue", self.available_thu),
            ("Vie", self.available_fri),
        ]
        return [label for label, on in days if on]

    @property
    def is_complete(self):
        """Rough completeness check used to nudge the applicant."""
        return bool(
            self.full_name and self.phone and self.region_id
            and self.subjects.exists()
        )


class Certificate(models.Model):
    class DocType(models.TextChoices):
        TITULO = "titulo", "Título profesional"
        ANTECEDENTES = "antecedentes", "Certificado de antecedentes"
        DIPLOMA = "diploma", "Diploma / postítulo"
        CV = "cv", "Currículum"
        OTRO = "otro", "Otro"

    profile = models.ForeignKey(
        TeacherProfile, on_delete=models.CASCADE, related_name="certificates"
    )
    doc_type = models.CharField(
        "tipo de documento", max_length=20, choices=DocType.choices, default=DocType.TITULO
    )
    name = models.CharField("nombre del documento", max_length=200)
    file = models.FileField("archivo", upload_to=certificate_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "certificado"
        verbose_name_plural = "certificados"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.get_doc_type_display()} — {self.name}"
