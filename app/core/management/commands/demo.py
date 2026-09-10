"""Populate the app with realistic demo data for showcasing the MVP.

Run:  python manage.py demo
Idempotent-ish: it skips users that already exist. Passwords are all `demo1234`.
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from catalog.models import Comuna, Region, Subject
from evaluations.models import Evaluation
from schools.models import School, SchoolMembership
from teachers.models import TeacherProfile

User = get_user_model()
PASSWORD = "demo1234"

TEACHERS = [
    # email, name, comuna, subjects, bilingual, short, long, status, rating
    ("ana@demo.cl", "Ana Díaz", "Ñuñoa", ["Lenguaje y Comunicación"], True, True, True, "approved", 5),
    ("bruno@demo.cl", "Bruno Rojas", "Providencia", ["Matemática", "Física"], False, True, True, "approved", 4),
    ("carla@demo.cl", "Carla Muñoz", "Maipú", ["Inglés"], True, True, False, "approved", 5),
    ("diego@demo.cl", "Diego Pérez", "La Florida", ["Historia y Geografía"], False, False, True, "approved", 4),
    ("elena@demo.cl", "Elena Soto", "Las Condes", ["Educación General Básica"], False, True, True, "approved", 3),
    ("fabian@demo.cl", "Fabián Vega", "Puente Alto", ["Biología", "Química"], False, True, False, "pending", None),
    ("gloria@demo.cl", "Gloria Reyes", "Santiago", ["Educación Parvularia"], False, True, True, "pending", None),
]


class Command(BaseCommand):
    help = "Crea datos de demostración (profes, evaluaciones, un colegio)."

    def handle(self, *args, **options):
        rm = Region.objects.filter(name__icontains="Metropolitana").first()

        # Staff evaluator
        if not User.objects.filter(email="evaluadora@demo.cl").exists():
            User.objects.create_user("evaluadora@demo.cl", PASSWORD, role="staff",
                                     first_name="Paula", last_name="Evaluadora")
            self.stdout.write("Evaluadora creada: evaluadora@demo.cl")

        for email, name, comuna_name, subjects, bil, short, long, status, rating in TEACHERS:
            if User.objects.filter(email=email).exists():
                continue
            user = User.objects.create_user(email, PASSWORD, role="applicant",
                                            first_name=name.split()[0])
            comuna = Comuna.objects.filter(name=comuna_name).first()
            profile = TeacherProfile.objects.create(
                user=user, full_name=name, phone="+569" + str(10000000 + len(name) * 11111),
                contact_email=email, bio=f"{name}, docente disponible para reemplazos.",
                region=rm, comuna=comuna, is_bilingual=bil,
                languages="Inglés avanzado" if bil else "",
                available_short=short, available_long=long, is_active=True,
            )
            for s_name in subjects:
                s = Subject.objects.filter(name=s_name).first()
                if s:
                    profile.subjects.add(s)
            if comuna:
                profile.preferred_comunas.add(comuna)
            Evaluation.objects.create(
                profile=profile, status=status, rating=rating,
                notes="Evaluación de demostración." if status != "pending" else "",
                evaluated_at=timezone.now() if status != "pending" else None,
            )

        # Demo school with an owner
        if not User.objects.filter(email="colegio@demo.cl").exists():
            owner = User.objects.create_user("colegio@demo.cl", PASSWORD, role="school",
                                             first_name="Rita", last_name="Directora")
            comuna = Comuna.objects.filter(name="Providencia").first()
            school = School.objects.create(name="Colegio Demo", region=rm, comuna=comuna,
                                           phone="+56222345678")
            SchoolMembership.objects.create(school=school, user=owner,
                                            school_role=SchoolMembership.Role.OWNER)
            self.stdout.write("Colegio demo creado: colegio@demo.cl")

        self.stdout.write(self.style.SUCCESS(
            "Datos de demo listos. Contraseña para todas las cuentas: demo1234"
        ))
