# Markplan AiH - Projekt Log

## GitHub Repository
https://github.com/jxrgen/veg

## Live App
- **Bruger-app:** https://jxrgen.github.io/veg/
- **Admin:** https://jxrgen.github.io/veg/admin.html (kode: `aihmarkadmin`)

---

## App Beskrivelse
Single-page web-app der giver medlemmer af Grøntsagsordningen i AiH overblik over afgrøders placering på marken, lugegruppe-ansvar og frigivet-status til høst.

---

## Filer
- `index.html` — Bruger-app (Supabase-drevet)
- `admin.html` — Admin-side (Supabase Auth + RLS)
- `markplan_2026.csv` — Markplan-data for 2026-sæsonen
- `lugegrupper_2026.csv` — Lugegruppeliste med medlemsdata for 2026
- `markplan_aih.csv` — Gammel CSV (2025, ikke længere i brug)
- `setup_db.py` — Database-opsætningsscript (ignoreret af git — indeholder credentials)
- `.gitignore` — Ekskluderer setup_db.py, __pycache__, .DS_Store

---

## Database: Supabase
**Projekt URL:** https://ujxmftvftcbjrdmzhlrw.supabase.co
**Anon/publishable key:** sb_publishable_EeimAI1x6_X1KxT-Clw5Bg_zIveRDYb
**Secret key:** Opbevares kun lokalt i setup_db.py (aldrig i Git)

### Tabeller
| Tabel | Indhold | RLS |
|---|---|---|
| `beds` | 114 rækker: bed_number, section (T/M/B), crop_name, luge_gruppe | Offentlig læsning |
| `crops` | 25 unikke afgrøder med is_released (boolean) | Offentlig læsning, kun admin kan ændre |
| `members` | 101 medlemmer: name, address, email, phone, luge_gruppe, bg | Kun autentificeret admin kan læse |
| `weeding_groups` | 10 grupper: group_number, description, bed_count, beds_text | Offentlig læsning |

### Admin-bruger (Supabase Auth)
- Email: `jxrgen@gmail.com` (hardcodet i admin.html, brugeren ser det ikke)
- Password: `aihmarkadmin`

---

## Funktioner (index.html)

### Afgrøder-fane
- Alfabetisk liste over alle afgrøder
- Søgefelt
- **Hængelås-ikon** (grå) = ikke klar til høst
- **Grønt check-ikon** = klar til høst
- **★ Favorit-knap** på hver afgrøde — gemmes i localStorage
- Favoritter vises øverst i listen
- Klik på afgrøde → skifter til Markoversigt og fremhæver bedene

### Markoversigt-fane
- Sub-tabs: Top / Midt / Bund
- Bed-kort viser: bed-nummer, afgrødenavn, gruppe-badge (G1–G10)
- Grøn top-kant på bed = afgrøde frigivet
- Klik på G-badge → fremhæver alle bed for den lugegruppe (toggle)
- Brugerens valgte lugegruppe (fra "Min side") markeres med grøn kant

### Min side-fane
- Vælg din lugegruppe (G1–G10) — gemmes i localStorage
- Viser gruppens beskrivelse og bede
- Knap: "Vis mine bede i markoversigten"
- Liste over favorit-afgrøder med status-ikon
- Ryd alle favoritter

### Header
- **?-knap** → hjælpeoverlay med brugerinstruktioner
- **☀-knap** → sollys-tilstand (høj-kontrast, mørkt tema), gemmes i localStorage
- **Skjult admin-adgang:** 5 tryk på overskriften inden for 3 sekunder → `admin.html`

---

## Funktioner (admin.html)

- Login med kun password (email hardcodet)
- **Lugegrupper & Medlemmer:** tabel med filter per gruppe (G1–G10), viser navn, adresse, telefon, email, BG
- **Afgrøder & Høst:** toggle-switches der opdaterer `is_released` direkte i Supabase
- Optimistisk UI (øjeblikkelig visuel opdatering, rollback ved fejl)
- Session persistens (forbliver logget ind ved genindlæsning)

---

## Termer / Mapping
| I CSV-filer | I app'en / databasen |
|---|---|
| Øverst | Top (section = 'T') |
| Mellem | Midt (section = 'M') |
| Nederst | Bund (section = 'B') |
| BG | Bostedsgruppe — gemmes i members.bg, vises i admin |

---

## Teknisk Stack
- **Frontend:** Ren HTML + inline CSS + inline JavaScript, ingen build-step
- **Styling:** Tailwind CSS (CDN) + CSS custom properties til theming
- **Database:** Supabase (PostgreSQL) med Row Level Security
- **Auth:** Supabase Auth (email+password) kun til admin
- **Hosting:** GitHub Pages (statisk)

---

## Data-setup (køres én gang lokalt)
```
cd /Users/jxrgen/claude/markapp/veg
python3 setup_db.py
```
Kræver: `psycopg2-binary` (`pip3 install psycopg2-binary`). Scriptet dropper og genskaber alle tabeller, seeder data fra CSV-filer og opretter admin-Auth-bruger.

---

## Dato-notation i markplan_2026.csv
Nogle afgrøder i CSV har et tal bagved (f.eks. "Grønkål 15/1"). Disse ignoreres ved import — crop_name i databasen er kun selve afgrødenavnet.

---

## Kendte begrænsninger
- Admin kan kun ændre `is_released` per afgrøde (alle bede af samme afgrøde frigives samlet)
- Ingen mulighed for at redigere markplan eller medlemmer via admin — kræver ny CSV + genkøre setup_db.py
- GitHub Pages tillader ikke server-side skrivning, så al data går via Supabase REST API

---

## Historik
| Dato | Ændring |
|---|---|
| 2026-04-19 | Første version med CSV-baseret data, lugegrupper, frigivet-status |
| 2026-04-19 | Admin-side med download-funktion |
| 2026-06-04 | Komplet migrering til Supabase |
| 2026-06-04 | Ny markplan og lugegruppeliste (2026-sæson) |
| 2026-06-04 | Ny index.html: tabs, søgning, lugegruppe-badges, hængelås/check-ikoner |
| 2026-06-04 | Ny admin.html: Supabase Auth, medlemsoversigt, afgrøde-frigiv-toggles |
| 2026-06-04 | Tilføjet: Min side, favoritter, ?-hjælpeside, 5-tap admin-adgang |
