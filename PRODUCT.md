# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

- **Primary buyer/user — Jefe/a de UTP (Unidad Técnico-Pedagógica):** the academic
  coordinator at a Chilean colegio who has to cover a teacher absence, often on
  short notice, and today resorts to phone calls and WhatsApp groups. Needs to
  find a screened, available substitute for a specific subject, comuna, and
  replacement length, and contact them directly. A colegio is an organization:
  several staff members can belong to one school account, but the Jefe/a de UTP
  is the persona to design for.
- **Postulante / profe (applicant):** a teacher looking for reemplazo work who
  builds a profile (títulos, certificado de antecedentes, subjects, availability,
  preferred comunas, bilingual flag) and wants to be found by colegios.
- **Sicóloga laboral (staff evaluator):** reviews and approves/rejects each
  applicant; her vetting is what gives the database its value.

## Product Purpose

A curated, vetted database of substitute teachers ("reemplazos de profes") that
Chilean schools can search and filter to fill absences quickly. Applicants
create profiles; a work psychologist (sicóloga laboral) evaluates each one; only
approved profiles are visible to schools, who filter and contact teachers
directly. Success = a colegio reliably finds a suitable, pre-screened substitute
without cold-calling, and a vetted teacher gets matched to work.

## Positioning

The differentiator is the **human vetting**: every teacher is reviewed and
interviewed by a sicóloga laboral before appearing, so schools browse a
pre-screened pool rather than raw résumés. A school cannot build this itself — a
ready, screened universe of teachers who don't already work there. Direct
contact, no per-placement intermediary in the hiring itself.

## Operating Context

- Chile-specific: regions and comunas as location taxonomy, RBD as the optional
  school identifier, Spanish-language UI throughout, timezone America/Santiago.
- Replacement framing schools think in: **corto** (days/weeks) vs **largo**
  (months), by asignatura, by comuna, and by weekday availability; bilingual is a
  common concrete requirement.
- Documents that matter to the decision: título profesional, certificado de
  antecedentes, diploma/postítulo, CV — uploaded by applicants, downloadable by
  schools on an approved profile.
- The vetting workflow: applicant registers → completes profile + uploads docs →
  enters the sicóloga's evaluation queue (pending) → approved/rejected with a
  rating and internal notes → approved profiles become searchable.
- Schools operate as multi-member orgs: the first user to register a school is
  its owner and can invite colleagues via a link.

## Capabilities and Constraints

- Roles: applicant (profe), school (colegio member), staff (sicóloga/evaluator),
  admin (superuser; sales/ops folded into admin for the MVP).
- Evaluation gating: schools see only profiles with status = approved and marked
  active.
- Directory filtering by subject, region, comuna, replacement type, weekday, and
  bilingual; free-text search.
- School org model: School, SchoolMembership (owner/member), link-based
  SchoolInvitation.
- Contact reveal: approved profiles show the teacher's phone and email directly —
  no in-app messaging in the MVP.
- Explicitly out of scope for the MVP (do not present as existing): payments /
  subscriptions, school-approval gating, dedicated sales/ops role, in-app
  messaging, transactional email delivery (invites are link-based), HTTPS/Let's
  Encrypt hardening, advanced availability calendar, school-side ratings, S3
  media storage.
- Stack (existing, not a new decision): Django 5 + Gunicorn, Postgres 16,
  Bootstrap 5 server-rendered templates, WhiteNoise static, django-filter,
  crispy-forms; Docker Compose deploy to a single EC2 host (Caddy reverse proxy,
  GHCR image + Watchtower auto-update).

## Brand Commitments

- Product name **"Reemplazos de Profes" is a working title / placeholder**, not a
  committed brand. Future work may rename it; do not treat the current name, the
  brass "verification seal" mark, or the evergreen palette as locked identity.
- UI language is **Spanish (Chile)** — this is binding.
- The vetting-by-sicóloga-laboral story is the core promise and should remain
  central to how the product presents itself.

## Evidence on Hand

- Origin: a real WhatsApp conversation describing the idea (source concept from
  "Paula Araya"). No real customers, schools, testimonials, pricing, or usage
  metrics exist yet — future work must not fabricate them.
- Synthetic showcase data exists for demos only: `python manage.py seed_demo`
  generates ~50 teachers (varied approved/pending/rejected), certificates, and
  several school orgs. This is clearly-marked demo data, not real users.
- No logo asset yet; the current mark is an emoji/icon-based "patch-check" seal
  chosen during the MVP build, not a commissioned identity.

## Product Principles

1. **The vetting is the product.** Everything hinges on schools trusting that
   every visible profile was screened by a person; design and copy must earn and
   protect that trust.
2. **Show only what's approved.** Schools never see unvetted candidates; the
   approved/active gate is a hard product rule, not a filter.
3. **Speak Chilean-school vernacular.** Comunas, RBD, asignaturas, UTP, reemplazo
   corto/largo — use the real terms the Jefe/a de UTP already uses.
4. **Remove friction from a stressful moment.** The buyer is often covering an
   absence under time pressure; find-and-contact must be fast and unambiguous.
5. **Honest about the stage.** It's an early MVP; don't imply scale, payments, or
   partnerships that don't exist yet.

## Accessibility & Inclusion

Spanish-language, Chile. No product-specific accessibility standard has been
established beyond general good practice (legible contrast, keyboard-operable
forms, works on the modest hardware school staff use).
