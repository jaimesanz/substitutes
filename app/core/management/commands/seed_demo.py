"""Populate the database with a large batch of synthetic data.

Its purpose is to showcase the *whole* platform at once: a screened universe of
teachers in every state (aprobado / pendiente / rechazado), with certificates,
varied subjects, locations, availability and bilingual profiles; several school
organizations with multiple members and pending invitations; and a couple of
staff evaluators.

Run inside the web container:

    python manage.py seed_demo               # create ~50 teachers + 6 schools
    python manage.py seed_demo --teachers 120 --schools 12
    python manage.py seed_demo --flush        # wipe previous synthetic data first

All synthetic accounts use the password ``demo1234`` and live under the
``@demo.cl`` email domain, so ``--flush`` can find and remove them without
touching any real accounts you may have created. The run is deterministic
(fixed random seed) so re-running produces the same catalog.
"""
import random

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from catalog.models import Comuna, Region, Subject
from evaluations.models import Evaluation
from schools.models import School, SchoolInvitation, SchoolMembership
from teachers.models import Certificate, TeacherProfile

User = get_user_model()

PASSWORD = "demo1234"
DEMO_DOMAIN = "demo.cl"  # every synthetic account lives here

FIRST_NAMES = [
    "Ana", "Bruno", "Carla", "Diego", "Elena", "Fabián", "Gloria", "Hugo",
    "Isidora", "Javier", "Karla", "Leonardo", "María", "Nicolás", "Olivia",
    "Pablo", "Queulat", "Rocío", "Sebastián", "Teresa", "Ulises", "Valentina",
    "Wladimir", "Ximena", "Yasna", "Zacarías", "Camila", "Benjamín", "Daniela",
    "Esteban", "Francisca", "Gonzalo", "Constanza", "Matías", "Paula", "Ignacio",
    "Antonia", "Cristóbal", "Josefa", "Tomás", "Amanda", "Vicente", "Florencia",
    "Agustín", "Emilia", "Maximiliano", "Catalina", "Joaquín", "Trinidad", "Álvaro",
]
LAST_NAMES = [
    "González", "Muñoz", "Rojas", "Díaz", "Pérez", "Soto", "Contreras", "Silva",
    "Martínez", "Sepúlveda", "Morales", "Rodríguez", "López", "Fuentes", "Hernández",
    "Torres", "Araya", "Flores", "Espinoza", "Valenzuela", "Castillo", "Tapia",
    "Reyes", "Gutiérrez", "Castro", "Vergara", "Álvarez", "Vásquez", "Sánchez",
    "Fernández", "Ramírez", "Carrasco", "Gómez", "Cortés", "Herrera", "Núñez",
    "Vega", "Riquelme", "Bravo", "Figueroa", "Cárdenas", "Salazar", "Miranda",
]

BIOS = [
    "Docente con {yrs} años de experiencia en aula. Comprometida con el aprendizaje "
    "significativo y el buen clima de convivencia.",
    "Profesor apasionado por su asignatura, con {yrs} años cubriendo reemplazos en "
    "colegios particulares y subvencionados.",
    "Experiencia en enseñanza básica y media ({yrs} años). Disponible para reemplazos "
    "cortos y proyectos de mediano plazo.",
    "Educadora con {yrs} años de trayectoria. Manejo de plataformas digitales y "
    "planificación por objetivos de aprendizaje.",
    "Profesional flexible y responsable, {yrs} años de experiencia. Puedo integrarme "
    "rápido al equipo docente y a los cursos.",
]

CERT_TEMPLATES = [
    (Certificate.DocType.TITULO, "Título Profesional"),
    (Certificate.DocType.ANTECEDENTES, "Certificado de Antecedentes"),
    (Certificate.DocType.DIPLOMA, "Diploma de Postítulo"),
    (Certificate.DocType.CV, "Currículum Vitae"),
]

SCHOOL_NAMES = [
    "Colegio San Ignacio", "Liceo Bicentenario Andrés Bello", "Colegio Santa María",
    "Escuela República de Chile", "Colegio Alemán del Sur", "Instituto O'Higgins",
    "Colegio Los Robles", "Liceo Manuel de Salas", "Colegio San Francisco",
    "Escuela Gabriela Mistral", "Colegio The English School", "Liceo Industrial",
]

APPROVED_NOTES = [
    "Perfil sólido. Entrevista muy positiva, buena disposición y experiencia comprobada.",
    "Cumple con todos los requisitos. Referencias verificadas, se recomienda.",
    "Excelente manejo pedagógico. Documentación completa y al día.",
    "Candidata idónea para reemplazos. Buena comunicación y puntualidad.",
]
REJECTED_NOTES = [
    "Documentación incompleta; falta certificado de antecedentes vigente.",
    "No se logró verificar la experiencia declarada en la entrevista.",
    "Perfil no se ajusta al estándar requerido por el momento.",
]


class Command(BaseCommand):
    help = "Genera una gran cantidad de datos sintéticos para mostrar la plataforma."

    def add_arguments(self, parser):
        parser.add_argument("--teachers", type=int, default=50,
                            help="Cantidad de profes a crear (por defecto 50).")
        parser.add_argument("--schools", type=int, default=6,
                            help="Cantidad de colegios a crear (por defecto 6).")
        parser.add_argument("--flush", action="store_true",
                            help="Elimina los datos sintéticos previos (@demo.cl) antes de crear.")

    @transaction.atomic
    def handle(self, *args, **opts):
        rng = random.Random(2024)  # deterministic

        if opts["flush"]:
            self._flush()

        regions = list(Region.objects.all())
        subjects = list(Subject.objects.all())
        if not regions or not subjects:
            self.stdout.write(self.style.ERROR(
                "Faltan datos base. Corre primero:  python manage.py seed"))
            return

        # Prefer the Metropolitana region for the bulk of comunas.
        rm = Region.objects.filter(name__icontains="Metropolitana").first() or regions[0]
        rm_comunas = list(Comuna.objects.filter(region=rm))

        evaluators = self._ensure_evaluators()
        n_teachers = self._make_teachers(rng, opts["teachers"], rm, rm_comunas,
                                         regions, subjects, evaluators)
        n_schools = self._make_schools(rng, opts["schools"], rm, rm_comunas)

        self.stdout.write(self.style.SUCCESS(
            f"\nListo. {n_teachers} profes, {n_schools} colegios y "
            f"{len(evaluators)} evaluadoras creadas.\n"
            f"Contraseña de todas las cuentas: {PASSWORD}\n"
            f"Evaluadora: sicologa1@{DEMO_DOMAIN}  |  "
            f"Colegio (dueño): {self._school_owner_email(0)}"
        ))

    # ------------------------------------------------------------------ helpers

    def _flush(self):
        qs = User.objects.filter(email__endswith=f"@{DEMO_DOMAIN}")
        count = qs.count()
        # Schools linked to those users get orphaned memberships; drop the schools
        # whose only members are synthetic. Simplest: delete schools created here
        # by name match, then the users (cascades profiles/evaluations/certs).
        School.objects.filter(name__in=SCHOOL_NAMES).delete()
        qs.delete()
        self.stdout.write(self.style.WARNING(f"Flush: {count} cuentas @{DEMO_DOMAIN} eliminadas."))

    def _ensure_evaluators(self):
        evaluators = []
        specs = [
            ("sicologa1", "Paula", "Araya"),
            ("sicologa2", "Marcela", "Fuentes"),
        ]
        for handle, first, last in specs:
            email = f"{handle}@{DEMO_DOMAIN}"
            user = User.objects.filter(email=email).first()
            if not user:
                user = User.objects.create_user(
                    email, PASSWORD, role="staff", first_name=first, last_name=last)
            evaluators.append(user)
        return evaluators

    def _make_teachers(self, rng, count, rm, rm_comunas, regions, subjects, evaluators):
        created = 0
        for i in range(count):
            email = f"profe{i + 1}@{DEMO_DOMAIN}"
            if User.objects.filter(email=email).exists():
                continue

            first = rng.choice(FIRST_NAMES)
            last = f"{rng.choice(LAST_NAMES)} {rng.choice(LAST_NAMES)}"
            full_name = f"{first} {last}"

            # ~80% of teachers live in the Metropolitana region for a dense directory.
            if rm_comunas and rng.random() < 0.8:
                region, comuna = rm, rng.choice(rm_comunas)
            else:
                region = rng.choice(regions)
                r_comunas = list(Comuna.objects.filter(region=region))
                comuna = rng.choice(r_comunas) if r_comunas else None

            user = User.objects.create_user(
                email, PASSWORD, role="applicant", first_name=first, last_name=last)

            bilingual = rng.random() < 0.3
            yrs = rng.randint(1, 25)
            short = rng.random() < 0.85
            long = rng.random() < 0.6
            if not short and not long:  # never fully unavailable
                short = True
            weekdays = {d: rng.random() < 0.8 for d in
                        ("mon", "tue", "wed", "thu", "fri")}
            if not any(weekdays.values()):
                weekdays["mon"] = True

            profile = TeacherProfile.objects.create(
                user=user,
                full_name=full_name,
                phone=f"+569{rng.randint(40000000, 99999999)}",
                contact_email=email,
                bio=rng.choice(BIOS).format(yrs=yrs),
                region=region, comuna=comuna,
                is_bilingual=bilingual,
                languages="Inglés (avanzado)" if bilingual else "",
                available_short=short, available_long=long,
                available_mon=weekdays["mon"], available_tue=weekdays["tue"],
                available_wed=weekdays["wed"], available_thu=weekdays["thu"],
                available_fri=weekdays["fri"],
                availability_notes=rng.choice(
                    ["", "Prefiero jornada de mañana.", "Con aviso de un día.",
                     "Disponible también sábados para talleres."]),
                is_active=rng.random() < 0.92,  # a few inactive profiles
            )
            # 1–3 subjects
            for s in rng.sample(subjects, k=min(rng.randint(1, 3), len(subjects))):
                profile.subjects.add(s)
            # preferred comunas (0–4 from the RM pool)
            if rm_comunas:
                for c in rng.sample(rm_comunas, k=min(rng.randint(0, 4), len(rm_comunas))):
                    profile.preferred_comunas.add(c)

            self._make_certificates(rng, profile)
            self._make_evaluation(rng, profile, evaluators)
            created += 1

        self.stdout.write(f"Profes creados: {created}")
        return created

    def _make_certificates(self, rng, profile):
        # Every teacher has at least their título; most add antecedentes + more.
        chosen = [CERT_TEMPLATES[0]]
        for tpl in CERT_TEMPLATES[1:]:
            if rng.random() < 0.6:
                chosen.append(tpl)
        for doc_type, label in chosen:
            content = (
                f"{label}\n\n"
                f"Nombre: {profile.full_name}\n"
                f"Documento de demostración generado automáticamente.\n"
                f"Este archivo es sólo un marcador de posición para el MVP.\n"
            ).encode("utf-8")
            fname = f"{doc_type}_{profile.user_id}.txt"
            cert = Certificate(profile=profile, doc_type=doc_type, name=label)
            cert.file.save(fname, ContentFile(content), save=True)

    def _make_evaluation(self, rng, profile, evaluators):
        roll = rng.random()
        if roll < 0.68:
            status = Evaluation.Status.APPROVED
            rating = rng.randint(3, 5)
            notes = rng.choice(APPROVED_NOTES)
        elif roll < 0.88:
            status = Evaluation.Status.PENDING
            rating = None
            notes = ""
        else:
            status = Evaluation.Status.REJECTED
            rating = rng.randint(1, 2)
            notes = rng.choice(REJECTED_NOTES)

        evaluated = status != Evaluation.Status.PENDING
        Evaluation.objects.create(
            profile=profile,
            status=status,
            rating=rating,
            notes=notes,
            evaluated_by=rng.choice(evaluators) if evaluated else None,
            evaluated_at=timezone.now() if evaluated else None,
        )

    def _school_owner_email(self, idx):
        return f"colegio{idx + 1}@{DEMO_DOMAIN}"

    def _make_schools(self, rng, count, rm, rm_comunas):
        created = 0
        names = SCHOOL_NAMES[:count] if count <= len(SCHOOL_NAMES) else (
            SCHOOL_NAMES + [f"Colegio Demo {i}" for i in range(count - len(SCHOOL_NAMES))])
        for idx, name in enumerate(names[:count]):
            owner_email = self._school_owner_email(idx)
            if User.objects.filter(email=owner_email).exists():
                continue

            comuna = rng.choice(rm_comunas) if rm_comunas else None
            owner = User.objects.create_user(
                owner_email, PASSWORD, role="school",
                first_name=rng.choice(FIRST_NAMES), last_name=rng.choice(LAST_NAMES))
            school = School.objects.create(
                name=name, region=rm, comuna=comuna,
                rbd=str(rng.randint(1000, 40000)),
                phone=f"+562{rng.randint(20000000, 29999999)}")
            SchoolMembership.objects.create(
                school=school, user=owner, school_role=SchoolMembership.Role.OWNER)

            # 0–3 additional members
            for m in range(rng.randint(0, 3)):
                member_email = f"colegio{idx + 1}-miembro{m + 1}@{DEMO_DOMAIN}"
                member = User.objects.create_user(
                    member_email, PASSWORD, role="school",
                    first_name=rng.choice(FIRST_NAMES), last_name=rng.choice(LAST_NAMES))
                SchoolMembership.objects.create(
                    school=school, user=member, school_role=SchoolMembership.Role.MEMBER)

            # a pending invitation on some schools, to showcase the invite flow
            if rng.random() < 0.5:
                SchoolInvitation.objects.create(
                    school=school,
                    email=f"invitado{idx + 1}@ejemplo.cl",
                    invited_by=owner)
            created += 1

        self.stdout.write(f"Colegios creados: {created}")
        return created
