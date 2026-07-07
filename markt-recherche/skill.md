---
name: markt-recherche
description: Hamburger Bildungsmarkt mit Firecrawl analysieren — Bildungsträger, IHK, Ausschreibungen, Trends
user_invocable: true
---

# Marktrecherche — Hamburger Bildungsszene

Analysiere den Hamburger Bildungsmarkt mit Firecrawl für Business-Opportunities.

## API-Key

```bash
source .env  # FIRECRAWL_API_KEY
```

Oder direkt: Lies den Key aus `C:\Users\mail\entwicklung\docker\.env` (Variable `FIRECRAWL_API_KEY`).

## Ablauf

### 1. Nutzer fragt nach Modus

Frage den Nutzer welchen Recherche-Modus er will:

| Modus | Was wird gecrawlt | Credits (~) |
|-------|------------------|-------------|
| **schnell** | Top 5 Quellen, nur Hauptseiten | ~10 |
| **standard** | Alle 12 Quellen, Hauptseiten + Kursverzeichnisse | ~50 |
| **tief** | Alle Quellen + Unterseiten (max 10 pro Domain) | ~120 |
| **gezielt** | Nutzer gibt URLs oder Keywords vor | variabel |

### 2. Quellen crawlen

Nutze Firecrawl API via curl/Bash:

```bash
curl -s -X POST https://api.firecrawl.dev/v1/scrape \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "formats": ["markdown"],
    "onlyMainContent": true
  }'
```

Für ganze Websites (crawl statt scrape):
```bash
curl -s -X POST https://api.firecrawl.dev/v1/crawl \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "limit": 10,
    "scrapeOptions": {
      "formats": ["markdown"],
      "onlyMainContent": true
    }
  }'
```

Crawl-Status prüfen (Crawl ist asynchron!):
```bash
curl -s https://api.firecrawl.dev/v1/crawl/{crawl_id} \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY"
```

### 3. Quellen-Katalog

#### Kategorie A: Bildungsträger (Kurs-Kataloge)

| # | Quelle | URL | Was suchen |
|---|--------|-----|------------|
| 1 | WBS Training | https://www.wbs-training.de/hamburg | KI-Kurse, Dozenten-Bedarf, neue Themen |
| 2 | COMCAVE College | https://www.comcave.de/standorte/hamburg | Digitale Angebote, Lücken |
| 3 | DAA Hamburg | https://www.daa-hamburg.de/ | Kursangebot, Moodle-Nutzung |
| 4 | GFN | https://www.gfn.de/standorte/hamburg | IT-/KI-Kurse, Dozenten gesucht |
| 5 | IHK/HKBiS | https://hkbis.de/themenwelten/ki/ | KI-Manager, Preise, Termine |
| 6 | Hamburger VHS | https://www.vhs-hamburg.de/ | Digitale Bildung, Programmierung |

#### Kategorie B: Fortbildung & Institutionen

| # | Quelle | URL | Was suchen |
|---|--------|-----|------------|
| 7 | LI Hamburg | https://li.hamburg.de/fortbildung | Lehrerfortbildungen, externe Dozenten |
| 8 | MMKH | https://www.mmkh.de/schulungen/ | KI-Schulungen für Hochschulen |
| 9 | fobizz | https://fobizz.com/fortbildungen/ | KI-Fortbildungen, Preise, Konkurrenz |

#### Kategorie C: Ausschreibungen & Jobs

| # | Quelle | URL | Was suchen |
|---|--------|-----|------------|
| 10 | Hamburg Vergabe | https://gateway.hamburg.de/hamburggateway/fvp/ | E-Learning, Moodle, Digitalisierung |
| 11 | Freelancermap | https://www.freelancermap.de/projekte?query=e-learning+hamburg | Projektausschreibungen |
| 12 | LinkedIn Jobs | https://www.linkedin.com/jobs/search/?keywords=E-Learning+Hamburg | Stellen, Trends |

#### Kategorie D: Förderprogramme

| # | Quelle | URL | Was suchen |
|---|--------|-----|------------|
| 13 | BMBF Förderungen | https://www.bmbf.de/bmbf/de/forschung/digitalisierung-und-ki/digitalisierung-und-ki_node.html | Neue Programme |
| 14 | IFB Hamburg | https://www.ifbhh.de/foerderprogramm | Hamburger Förderprogramme |

### 4. Analyse-Framework

Für jede Quelle extrahiere und analysiere:

#### Bildungsträger
- **Kursangebot:** Welche KI/Digital-Kurse gibt es?
- **Preise:** Was kosten sie? (Vergleich mit Dirks 75-100€/h)
- **Lücken:** Was fehlt? (Moodle, interaktive Lernmodule, H5P)
- **Dozenten:** Werden externe gesucht?
- **Format:** Online, Präsenz, Hybrid?

#### Ausschreibungen
- **Thema:** E-Learning, Moodle, KI, Digitalisierung?
- **Budget:** Falls angegeben
- **Deadline:** Bewerbungsfrist
- **Anforderungen:** Was wird gesucht?

#### Trends
- **Neue Themen:** Was taucht auf, was gab es vor 3 Monaten nicht?
- **Preisentwicklung:** Werden KI-Kurse teurer/günstiger?
- **Format-Shift:** Mehr Online? Mehr Hybrid?

### 5. Report erstellen

Erstelle einen strukturierten Report:

```markdown
# Marktrecherche Hamburg — Bildungsszene
Datum: {YYYY-MM-DD}

## Executive Summary
- X Quellen analysiert
- Y relevante Opportunities gefunden
- Top-3 Handlungsempfehlungen

## Opportunities (nach Priorität)

### Sofort umsetzbar
- [Opportunity 1]: Beschreibung, Quelle, nächster Schritt

### Mittelfristig (1-3 Monate)
- [Opportunity 2]: ...

### Beobachten
- [Trend 1]: ...

## Konkurrenz-Update
| Anbieter | Neue Kurse | Preise | Bemerkung |
|----------|-----------|--------|-----------|

## Ausschreibungen
| Titel | Quelle | Deadline | Passt? |
|-------|--------|----------|--------|

## Empfehlungen
1. ...
2. ...
3. ...
```

### 6. Report speichern

Speichere den Report in: `C:\Users\mail\entwicklung\_DEV_DOCS\_DEV_DOCS\Business\Marktrecherche\{YYYY-MM-DD}-marktrecherche.md`

## Hinweise

- **Free Tier:** 500 Credits/Monat. Standard-Recherche verbraucht ~50.
- **LinkedIn:** Braucht oft Login — Firecrawl kann das nicht. Nutze stattdessen die öffentliche Job-Suche.
- **Dynamische Seiten:** Firecrawl rendert JavaScript, WebFetch nicht. Für SPA-Seiten (React-basierte Kursverzeichnisse) Firecrawl bevorzugen.
- **Rate Limit:** Nicht mehr als 5 Requests parallel, sonst 429.
