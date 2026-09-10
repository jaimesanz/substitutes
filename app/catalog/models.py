from django.db import models


class Region(models.Model):
    name = models.CharField("región", max_length=100, unique=True)
    order = models.PositiveSmallIntegerField("orden", default=0)

    class Meta:
        verbose_name = "región"
        verbose_name_plural = "regiones"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Comuna(models.Model):
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="comunas", verbose_name="región"
    )
    name = models.CharField("comuna", max_length=100)

    class Meta:
        verbose_name = "comuna"
        verbose_name_plural = "comunas"
        ordering = ["name"]
        unique_together = ("region", "name")

    def __str__(self):
        return self.name


class Subject(models.Model):
    """Asignatura / especialidad que un profe puede cubrir."""

    name = models.CharField("asignatura", max_length=100, unique=True)
    order = models.PositiveSmallIntegerField("orden", default=0)

    class Meta:
        verbose_name = "asignatura"
        verbose_name_plural = "asignaturas"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name
