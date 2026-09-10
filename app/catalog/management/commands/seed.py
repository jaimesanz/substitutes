"""Idempotent seed of reference data: Chilean regions, key comunas, subjects.

Safe to run on every boot — uses get_or_create so it never duplicates.
Comuna list focuses on the Región Metropolitana (main market) plus regional
capitals and major cities; extend freely via the Django admin.
"""
from django.core.management.base import BaseCommand

from catalog.models import Comuna, Region, Subject

REGIONS = [
    ("Arica y Parinacota", 1, ["Arica", "Putre"]),
    ("Tarapacá", 2, ["Iquique", "Alto Hospicio", "Pozo Almonte"]),
    ("Antofagasta", 3, ["Antofagasta", "Calama", "Tocopilla", "Mejillones"]),
    ("Atacama", 4, ["Copiapó", "Vallenar", "Caldera", "Chañaral"]),
    ("Coquimbo", 5, ["La Serena", "Coquimbo", "Ovalle", "Illapel", "Vicuña"]),
    ("Valparaíso", 6, [
        "Valparaíso", "Viña del Mar", "Quilpué", "Villa Alemana", "Concón",
        "Quillota", "San Antonio", "San Felipe", "Los Andes", "La Calera",
    ]),
    ("Metropolitana de Santiago", 7, [
        "Santiago", "Providencia", "Las Condes", "Vitacura", "Lo Barnechea",
        "Ñuñoa", "La Reina", "Macul", "Peñalolén", "La Florida",
        "Puente Alto", "San Bernardo", "Maipú", "Estación Central", "Cerrillos",
        "Pudahuel", "Quilicura", "Renca", "Independencia", "Recoleta",
        "Conchalí", "Huechuraba", "Quinta Normal", "Lo Prado", "Cerro Navia",
        "San Miguel", "San Joaquín", "La Cisterna", "El Bosque", "La Granja",
        "La Pintana", "Lo Espejo", "Pedro Aguirre Cerda", "San Ramón",
        "Peñaflor", "Talagante", "Melipilla", "Buin", "Colina", "Lampa",
    ]),
    ("Libertador General Bernardo O'Higgins", 8, [
        "Rancagua", "San Fernando", "Rengo", "Machalí", "Santa Cruz",
    ]),
    ("Maule", 9, ["Talca", "Curicó", "Linares", "Constitución", "Cauquenes"]),
    ("Ñuble", 10, ["Chillán", "Chillán Viejo", "San Carlos", "Bulnes"]),
    ("Biobío", 11, [
        "Concepción", "Talcahuano", "Los Ángeles", "Chiguayante", "San Pedro de la Paz",
        "Coronel", "Hualpén", "Lota", "Tomé",
    ]),
    ("La Araucanía", 12, ["Temuco", "Padre Las Casas", "Villarrica", "Angol", "Pucón"]),
    ("Los Ríos", 13, ["Valdivia", "La Unión", "Río Bueno", "Panguipulli"]),
    ("Los Lagos", 14, ["Puerto Montt", "Osorno", "Castro", "Ancud", "Puerto Varas"]),
    ("Aysén del General Carlos Ibáñez del Campo", 15, ["Coyhaique", "Puerto Aysén"]),
    ("Magallanes y de la Antártica Chilena", 16, ["Punta Arenas", "Puerto Natales"]),
]

SUBJECTS = [
    "Educación Parvularia", "Educación Diferencial", "Educación General Básica",
    "Lenguaje y Comunicación", "Matemática", "Historia y Geografía",
    "Biología", "Física", "Química", "Ciencias Naturales",
    "Inglés", "Francés", "Artes Visuales", "Música", "Educación Física",
    "Tecnología", "Religión", "Filosofía", "Psicopedagogía",
]


class Command(BaseCommand):
    help = "Carga datos de referencia (regiones, comunas, asignaturas) de forma idempotente."

    def handle(self, *args, **options):
        regions_created = comunas_created = subjects_created = 0

        for name, order, comunas in REGIONS:
            region, created = Region.objects.get_or_create(
                name=name, defaults={"order": order}
            )
            if not created and region.order != order:
                region.order = order
                region.save(update_fields=["order"])
            regions_created += int(created)
            for comuna_name in comunas:
                _, c_created = Comuna.objects.get_or_create(
                    region=region, name=comuna_name
                )
                comunas_created += int(c_created)

        for i, subject_name in enumerate(SUBJECTS):
            _, created = Subject.objects.get_or_create(
                name=subject_name, defaults={"order": i}
            )
            subjects_created += int(created)

        self.stdout.write(self.style.SUCCESS(
            f"Seed listo. Regiones nuevas: {regions_created}, "
            f"comunas nuevas: {comunas_created}, asignaturas nuevas: {subjects_created}."
        ))
