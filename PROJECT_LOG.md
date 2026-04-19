# Markplan AiH - Projekt Log

## GitHub Repository
https://github.com/jxrgen/veg

## App Beskrivelse
Web-app der giver medlemmer af Grøntsagsordningen i AiH overblik over afgrøders placering på marken.

## Filer
- `index.html` - Hovedapp ( https://jxrgen.github.io/veg/ )
- `admin.html` - Admin-side for at redigere frigivet-status ( kode: aihmark )
- `markplan_aih.csv` - Data-fil

## Funktioner (index.html)
1. **Dynamisk Data** - Indlæser fra markplan_aih.csv
2. **Interaktiv Afgrødeliste** - Alfabetisk liste med klik -> puls-animation
3. **Grafisk Markoversigt** - Top/Midt/Bund sektioner
4. **Lugegrupper** - Vises kun når bruger vælger en gruppe i indstillinger
5. **Frigivet-status** - Låst (🔒 rød) / Kan høstes (✅ grøn)
6. **Sollys-tilstand** - High-contrast tema
7. **Brugerindstillinger** - Gem i localStorage
8. **Ikoner** - Sol og person

## Data Format (CSV)
- Bed: Bed-nummer
- Top/Midt/Bund: Afgrødenavn
- Lugegruppe: 1-15
- Frigivet: 0 (låst) eller 1 (frigivet)

## Historie
- 2026-04-19: Tilføjet lugegrupper og frigivet-status
- 2026-04-19: Tilføjet farvekodede baggrunde
- 2026-04-19: Tilføjet brugerindstillinger
- 2026-04-19: Lugegrupper vises kun ved valg
- 2026-04-19: Nye ikoner (sol og person)
- 2026-04-19: Gult favorit-border, orange lugegruppe-badges
- 2026-04-19: Ny admin.html (afgrøde-liste, toggle, upload)

## Ubesvarede spørgsmål
- Lugegruppe 0? - Kan ikke finde i CSV
- Admin gemme virker ikke - skal laves som download?