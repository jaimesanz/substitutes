import django_filters
from django import forms
from django.db.models import Q

from catalog.models import Comuna, Region, Subject
from teachers.models import TeacherProfile

REPLACEMENT_CHOICES = [
    ("short", "Reemplazo corto"),
    ("long", "Reemplazo largo"),
]

WEEKDAY_CHOICES = [
    ("available_mon", "Lunes"),
    ("available_tue", "Martes"),
    ("available_wed", "Miércoles"),
    ("available_thu", "Jueves"),
    ("available_fri", "Viernes"),
]


class TeacherFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(
        method="filter_search", label="Buscar",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre, idioma, palabra clave…"}),
    )
    subject = django_filters.ModelChoiceFilter(
        field_name="subjects", queryset=Subject.objects.all(), label="Asignatura",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    region = django_filters.ModelChoiceFilter(
        field_name="region", queryset=Region.objects.all(), label="Región",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    comuna = django_filters.ModelChoiceFilter(
        method="filter_comuna", queryset=Comuna.objects.all(), label="Comuna",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    replacement = django_filters.ChoiceFilter(
        method="filter_replacement", choices=REPLACEMENT_CHOICES, label="Tipo de reemplazo",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    weekday = django_filters.ChoiceFilter(
        method="filter_weekday", choices=WEEKDAY_CHOICES, label="Disponible día",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    is_bilingual = django_filters.BooleanFilter(
        field_name="is_bilingual", method="filter_bilingual", label="Solo bilingües",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = TeacherProfile
        fields = ["q", "subject", "region", "comuna", "replacement", "weekday", "is_bilingual"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(full_name__icontains=value)
            | Q(bio__icontains=value)
            | Q(languages__icontains=value)
        )

    def filter_comuna(self, queryset, name, value):
        # Match residence comuna OR a preferred work comuna.
        return queryset.filter(
            Q(comuna=value) | Q(preferred_comunas=value)
        ).distinct()

    def filter_replacement(self, queryset, name, value):
        if value == "short":
            return queryset.filter(available_short=True)
        if value == "long":
            return queryset.filter(available_long=True)
        return queryset

    def filter_weekday(self, queryset, name, value):
        if value in dict(WEEKDAY_CHOICES):
            return queryset.filter(**{value: True})
        return queryset

    def filter_bilingual(self, queryset, name, value):
        # Only narrow when the box is checked; unchecked (False) is a no-op.
        if value:
            return queryset.filter(is_bilingual=True)
        return queryset
