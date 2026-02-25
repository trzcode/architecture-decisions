# architecture-decisions
Playground for documenting architecture decisions

# Architektur-Dokumentation (ADRs)

Dieses Repository verwaltet unsere Architektur-Entscheidungen datengetrieben. Die Webseite wird automatisch via GitHub Pages bereitgestellt.

## Neues ADR anlegen

1. Erstelle eine neue Datei in `docs/adr/`, z.B. `005-neue-technologie.md`.
2. Kopiere das folgende Template in die Datei:

---
id: ADR-XXX
title: "Titel der Entscheidung"
status: proposed  # Werte: proposed, accepted, deprecated, superseded
date: 2026-02-25
tags:
  - technologie
  - backend
dependencies:
  - ADR-001
references: []
---

{{ render_adr_header() }}

## Kontext
Warum müssen wir diese Entscheidung treffen?

## Entscheidung
Was haben wir entschieden?

## Konsequenzen
Was sind die positiven/negativen Folgen?
---

3. **Push:** Sobald du die Datei nach `main` pushst, aktualisiert die GitHub Action automatisch den Index und alle Verlinkungen.

## Lokale Vorschau
Um die Seite lokal zu testen, installiere die Requirements und starte den Server:
`pip install -r requirements.txt`
`mkdocs serve`
