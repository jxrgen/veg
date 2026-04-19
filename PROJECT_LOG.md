# Markplan AiH - Projekt Log

## GitHub Repository
https://github.com/jxrgen/veg

## App Beskrivelse
Web-app der giver medlemmer af Grøntsagsordningen i AiH overblik over afgrøders placering på marken.

## Funktioner
1. **Dynamisk Data** - Indlæser fra markplan_aih.csv med hardcodede fallback-data
2. **Interaktiv Afgrødeliste** - Alfabetisk liste med klik -> puls-animation på matchende bede
3. **Grafisk Markoversigt** - Viser Top/Midt/Bund sektioner med bed-numre og afgrødenavne
4. **Lugegrupper** - Viser hvilke grupper der har ansvaret for hvilke bede
5. **Frigivet-status** - Låst (🔒 rød) / Kan høstes (✅ grøn)
6. **Sollys-tilstand** - High-contrast tema gemt i localStorage
7. **Responsivt Design** - Tailwind CSS, mobil-optimeret
8. **Navigation** - "Til toppen" links med tilfældige grøntsags-emojis

## Data Format (CSV)
- Bed: Bed-nummer
- Top/Midt/Bund: Afgrødenavn i hver sektion
- Lugegruppe: Nummer på lugegruppe (1-15)
- Frigivet: 0 (låst) eller 1 (kan høstes)

## Teknisk Info
- **Format**: Ren HTML med inline CSS og JavaScript
- **Styling**: Tailwind CDN + custom CSS variables
- **Data**: CSV-parser med hybrid online/offline tilstand
- **Fejlhåndtering**: try-catch i fetchCsvData()

## Historie
- 2026-04-19: Tilføjet lugegrupper og frigivet-status med ikoner
- 2026-04-19: Tilføjet farvekodede baggrunde (rød=låst, grøn=frigivet)