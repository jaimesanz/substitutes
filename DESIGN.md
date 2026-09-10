---
name: Reemplazos de Profes
description: A certified registry of vetted substitute teachers for Chilean schools.
colors:
  registry-pine: "#1f5c46"
  pine-hover: "#1a4d3a"
  deep-pine: "#123528"
  pine-tint: "#e7efe9"
  pine-tint-2: "#d8e6dc"
  certified-brass: "#a9761f"
  brass-deep: "#8c6017"
  brass-tint: "#f6ecd6"
  cool-paper: "#f1f3ee"
  surface: "#ffffff"
  surface-sunk: "#f8f9f5"
  chalk-ink: "#17241e"
  ink-soft: "#45564d"
  muted-sage: "#78877d"
  line: "#e3e6df"
  line-strong: "#d3d7cc"
  pending-amber: "#b07d16"
  rejected-clay: "#a23c2b"
typography:
  display:
    fontFamily: "Spectral, Georgia, 'Times New Roman', serif"
    fontSize: "clamp(2rem, 5vw, 3rem)"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Spectral, Georgia, serif"
    fontSize: "1.6rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Spectral, Georgia, serif"
    fontSize: "1.1rem"
    fontWeight: 600
    lineHeight: 1.3
  body:
    fontFamily: "'Public Sans', system-ui, -apple-system, 'Segoe UI', sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.65
  label:
    fontFamily: "'IBM Plex Mono', ui-monospace, SFMono-Regular, monospace"
    fontSize: "0.72rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.14em"
rounded:
  sm: "0.4rem"
  md: "0.55rem"
  lg: "0.875rem"
  pill: "50%"
spacing:
  xs: "0.5rem"
  sm: "0.75rem"
  md: "1.25rem"
  lg: "2rem"
components:
  button-primary:
    backgroundColor: "{colors.registry-pine}"
    textColor: "{colors.surface}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "0.5rem 1.1rem"
  button-primary-hover:
    backgroundColor: "{colors.pine-hover}"
    textColor: "{colors.surface}"
  button-outline:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.registry-pine}"
    rounded: "{rounded.md}"
    padding: "0.5rem 1.1rem"
  badge-verified:
    backgroundColor: "{colors.pine-tint}"
    textColor: "{colors.pine-hover}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "0.3rem 0.55rem"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.chalk-ink}"
    rounded: "{rounded.lg}"
    padding: "1.25rem"
  input-field:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.chalk-ink}"
    rounded: "{rounded.md}"
    padding: "0.55rem 0.8rem"
---

# Design System: Reemplazos de Profes

## Overview

**Creative North Star: "The Certified Registry"**

Reemplazos de Profes looks and behaves like an official register of vetted
professionals, because that is exactly what it sells: a database of substitute
teachers each screened by a sicóloga laboral before they appear. The interface
carries the quiet authority of a credentialing body — a deep evergreen that reads
as academic and institutional, a warm brass reserved almost exclusively for the
verification seal, and a cool paper ground that feels like a well-kept record
rather than a marketing site. Every approved teacher is presented as an entry
"on file": stamped, dated in spirit, and legible at a glance.

The system is **refined and institutional**. Brand personality lives in small
exact details — a mono label strip, a hairline divider, a brass wax-seal disc —
not in loud gradients or oversized flourishes. Density is comfortable, not
crowded; the Jefe/a de UTP scanning for a replacement under time pressure should
find the subject, comuna, availability and seal without hunting. Trust is the
product, so the design never oversells: it states, it certifies, it gets out of
the way.

The rejected world is the generic SaaS starter — indigo-to-violet hero gradients,
Inter as the safe default, one rounded-card shadow stamped on everything, emoji
section markers. This project is the opposite: a committed palette, a serif with
gravitas, and structure that encodes real meaning (a seal means vetted; a mono
label means a record).

**Key Characteristics:**
- Evergreen + brass on cool paper — an academic credential palette, never the default blue.
- A recurring brass **verification seal** as the system's signature mark.
- Serif headlines (Spectral) for authority; a government-grade sans (Public Sans) for trust; mono (IBM Plex Mono) for anything that reads as data or record.
- Flat, hairline-bordered surfaces that lift only on interaction.
- Spanish-Chilean vernacular treated as content, not decoration.

## Colors

An academic credential palette: a single authoritative evergreen, a scarce
ceremonial brass, and a warm-neutral paper system — no cool greys, no default
blue anywhere.

### Primary
- **Registry Pine** (`#1f5c46`): the brand voice. Primary buttons, links, active
  icons, subject badges, the feature-icon tiles. The workhorse accent.
- **Deep Pine** (`#123528`): the institutional frame — navbar, footer, and the
  base of the hero gradient. Anchors the page in authority.
- **Pine Hover** (`#1a4d3a`): the pressed/hover state of pine surfaces.

### Secondary
- **Certified Brass** (`#a9761f`): the ceremonial accent. Reserved for the
  verification seal, star ratings, mono eyebrows, and the single highest-emphasis
  nav CTA. Its scarcity is what makes a stamped profile feel earned.
- **Brass Deep** (`#8c6017`): brass text on tinted grounds and brass hover.

### Tertiary (state hues — not brand accents)
- **Pending Amber** (`#b07d16`): the "pendiente de evaluación" state only.
- **Rejected Clay** (`#a23c2b`): the "rechazado" state and destructive actions only.

### Neutral
- **Cool Paper** (`#f1f3ee`): the page ground — warm-neutral with a faint green
  bias, deliberately not cream and not white.
- **Surface** (`#ffffff`): cards, panels, inputs.
- **Surface Sunk** (`#f8f9f5`): recessed fills, light badges, table zebra.
- **Chalk Ink** (`#17241e`): primary text — near-black with a green undertone.
- **Ink Soft** (`#45564d`): secondary text, form labels.
- **Muted Sage** (`#78877d`): meta text, captions, placeholders.
- **Line** (`#e3e6df`) / **Line Strong** (`#d3d7cc`): hairline dividers and input borders.
- **Pine Tint** (`#e7efe9`) / **Pine Tint 2** (`#d8e6dc`): the fill + border of verified badges, avatars, and success alerts.
- **Brass Tint** (`#f6ecd6`): the fill behind rating chips and bilingual badges.

### Named Rules
**The Scarce Brass Rule.** Brass is ceremonial, not structural. It appears only
where the product certifies something — the seal, a rating, a mono eyebrow, or
the one primary nav CTA — and never as a general-purpose button or background.
If brass is doing the job pine could do, it is being wasted.

**The No-Blue Rule.** There is no blue in this system. The instinct to reach for
a trustworthy SaaS blue is exactly the generic default this identity rejects;
trust is carried by evergreen and the seal.

## Typography

**Display Font:** Spectral (with Georgia, 'Times New Roman', serif)
**Body Font:** Public Sans (with system-ui, Segoe UI, sans-serif)
**Label/Mono Font:** IBM Plex Mono

**Character:** Spectral brings the gravitas of an institutional document — a
literary serif that says "on the record." Public Sans is a neutral,
government-grade sans built for legibility and trust, so body copy and UI never
compete with the headlines. IBM Plex Mono handles anything that is a datum — a
count, a rating, a category eyebrow — giving those elements the feel of a
registry entry.

### Hierarchy
- **Display** (Spectral 700, `clamp(2rem, 5vw, 3rem)`, 1.1, `-0.02em`): hero and page-defining headlines. `text-wrap: balance`.
- **Headline** (Spectral 600, ~1.6rem, 1.2): section titles ("Cómo funciona", "Buscar profesores").
- **Title** (Spectral 600, ~1.1rem, 1.3): card and profile names.
- **Body** (Public Sans 400, 1rem, 1.65): all running text; keep measure ~65ch.
- **Label** (IBM Plex Mono 600, 0.72rem, `+0.14em`, UPPERCASE): eyebrows, step indices, counts, and data microcopy.

### Named Rules
**The Mono-Means-Record Rule.** Monospace is never decorative. It marks text that
is a datum or a category label — a result count, a rating, "PASO 01", "SELLO DE
EVALUACIÓN". If it isn't a record, it isn't mono.

**The Serif-Authority Rule.** Headings and proper names of people/schools are set
in Spectral; UI chrome and controls are Public Sans. Never set a button or form
label in the serif.

## Layout

A centered single-column container (Bootstrap `.container`, ~1140px max) over the
cool-paper ground, with generous vertical rhythm between sections (~3rem, the
`mb-5` step). Content is organized as **records and panels**: the directory is a
responsive card grid (1 col mobile → 2 → 3 at `lg`), profiles use an 8/4
two-column split (dossier + sticky contact rail), and dashboards pair a summary
panel with a work panel. The hero is a 6/6 split — thesis copy beside a live
sample profile card — sized to its content, never `100vh`. Spacing follows an
8px-based rhythm (`0.5 / 0.75 / 1.25 / 2rem`). On narrow viewports columns stack,
the sticky contact rail releases to flow, and the nav collapses to a toggle.

## Elevation & Depth

**Flat by default, lift on interaction.** Surfaces rest flat: a card is a white
fill with a 1px `Line` hairline and only a whisper of shadow. Depth is a response
to state — cards translate up 3px and take a soft medium shadow on hover; the hero
and the floating sample card are the deliberate exceptions that use real
elevation to read as "lifted off the page." Depth is never used to decorate a
resting surface.

### Shadow Vocabulary
- **Hairline rest** (`box-shadow: 0 1px 2px rgba(23,36,30,.05), 0 1px 3px rgba(23,36,30,.04)`): the near-flat resting state of every card and panel.
- **Lift** (`box-shadow: 0 6px 18px -8px rgba(18,53,40,.18), 0 2px 6px rgba(18,53,40,.06)`): hover/active elevation for interactive cards.
- **Floating** (`box-shadow: 0 24px 48px -20px rgba(18,53,40,.28)`): the hero container and the sample profile card only.

### Named Rules
**The Flat-At-Rest Rule.** If a surface isn't being interacted with, it carries at
most the hairline shadow. A page full of drop-shadowed cards is the generic look
this system rejects; let the border do the separating.

## Shapes

A calm, consistent radius family — nothing sharp, nothing pill-soft except where
it means something. Cards and panels use a 14px radius (`rounded.lg`); buttons and
inputs use ~9px (`rounded.md`); badges and small chips use ~6px (`rounded.sm`).
The one fully-round form is the **circle**, reserved for identity and
certification: the avatar disc and the brass verification seal. Borders are
hairline (1px `Line` / `Line Strong`) and do real structural work — the system
leans on them instead of shadow. Dashed hairlines (`1px dashed Line`) separate
rows inside a dossier data list, evoking a filled-in form.

## Components

### Buttons
- **Shape:** ~9px radius (`rounded.md`), weight 600, comfortable padding (`0.5rem 1.1rem`; `lg` = `0.7rem 1.5rem`).
- **Primary:** `Registry Pine` fill, white text, hairline shadow. Hover → `Pine Hover`.
- **Brass (rare):** `Certified Brass` fill, white text — only for a single highest-emphasis CTA (e.g. "Crear cuenta" in the nav).
- **Outline:** white fill, `Line Strong` border, pine text; hover inverts to pine fill / white text.
- **Focus:** 2px `Certified Brass` outline, 2px offset — the seal color doubles as the focus signal.

### Chips
- **Subject badge:** `Pine Tint` fill, `Pine Hover` text, `Pine Tint 2` border, weight 500 — the default categorizer.
- **Rating chip:** `Brass Tint` fill, `Brass Deep` text, mono, tabular numerals, with a filled star — reads as a certified score.
- **State pills (mono, uppercase):** verified = pine tint; pending = amber tint; rejected = clay tint. State is encoded in both color and label, never color alone.

### Cards / Containers
- **Corner Style:** 14px (`rounded.lg`).
- **Background:** `Surface` white on the `Cool Paper` ground.
- **Shadow Strategy:** hairline at rest, `Lift` on hover (see Elevation).
- **Border:** 1px `Line`, warming to `Pine Tint 2` on hover.
- **Internal Padding:** `1.25rem` (`spacing.md`); cards end with a hairline-topped footer row for meta + action.

### Inputs / Fields
- **Style:** white fill, `Line Strong` 1px border, ~9px radius, `0.55rem 0.8rem` padding.
- **Focus:** border shifts to `Registry Pine` with a soft `rgba(31,92,70,.15)` ring.
- **Labels:** Public Sans 600, `Ink Soft`. Checkboxes check in `Registry Pine`.

### Navigation
- **Style:** `Deep Pine` bar; brand set in Spectral with a small brass seal-disc mark. Links are translucent white, brightening with a faint white wash on hover. The primary CTA is the brass solid button; secondary actions use a ghost (bordered-white) button.
- **Mobile:** collapses to a bordered toggle; links stack.

### Verification Seal (signature component)
The identity's defining mark: a circular brass disc with a radial highlight
(top-left light source), a white inset ring, and a soft brass drop shadow,
holding a `patch-check` glyph. Sizes scale via a `--sz` custom property — ~2rem on
directory cards, ~3–3.4rem on profiles, ~5rem in the trust panel. It always means
one thing: **evaluated and approved**. Never use it decoratively on an unvetted
element.

## Do's and Don'ts

### Do:
- **Do** keep brass ceremonial — seal, ratings, mono eyebrows, one nav CTA — per the Scarce Brass Rule.
- **Do** set headings and proper names in Spectral, and all UI chrome in Public Sans.
- **Do** use IBM Plex Mono only for data/record text (counts, ratings, "PASO 01", eyebrows).
- **Do** keep surfaces flat at rest (hairline shadow) and reserve real elevation for hover, the hero, and the floating sample card.
- **Do** encode state in color **and** label together (verified/pending/rejected pills).
- **Do** speak the real vernacular — comuna, RBD, asignatura, reemplazo corto/largo — as visible content.

### Don't:
- **Don't** introduce blue, or an indigo→violet gradient — the No-Blue Rule is absolute.
- **Don't** stamp a drop shadow on every card; let the hairline border separate resting surfaces.
- **Don't** spend brass as a general button or background color.
- **Don't** use the verification seal on anything that isn't an approved profile.
- **Don't** set body copy or controls in the serif, or a data label in the body sans.
- **Don't** center everything or reach for emoji as section markers; structure should encode real meaning.
