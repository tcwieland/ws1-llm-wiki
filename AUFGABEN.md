# Aufgaben im Workshop

## Aufgabe 1

**Teil A · Repo, Agent, MCP und Pipeline · 65 Minuten · zu zweit**

Ziel: Ein Agent arbeitet in eurem Repository, spricht über MCP mit GitHub und mit einem eigenen Server, und eine Pipeline prüft, was er tut.

1. **Repo und Agent**
   - [ ] Repo aus dem Template anlegen, klonen, `.env` füllen ([SETUP.md](SETUP.md#5-am-workshoptag-gemeinsam)).
   - [ ] Claude Code starten: `./scripts/start-claude.sh`
   - [ ] Fragt den Agenten: *„Erkläre mir dieses Repository in fünf Sätzen. Was darfst du, was nicht?“*
   - [ ] Gebt `/permissions` ein und vergleicht mit `.claude/settings.json`. Welche Regel überrascht euch?
2. **GitHub-MCP-Server**
   - [ ] Server anbinden ([SETUP.md](SETUP.md#5-am-workshoptag-gemeinsam), Schritt 4), in Claude Code mit `/mcp` prüfen.
   - [ ] *„Lege in meinem Repository ein Issue ‚Wiki aufbauen‘ mit drei Aufgaben als Checkliste an.“* – Beobachtet die Rückfrage, bevor der Agent schreibt.
3. **Eigener MCP-Server `wiki-tools`**
   - [ ] Öffnet `scripts/wiki_mcp.py` und lest den Code: Jede Funktion mit `@mcp.tool()` wird ein Werkzeug. Der Docstring ist die Beschreibung, die der Agent sieht.
   - [ ] Server anbinden ([SETUP.md](SETUP.md#5-am-workshoptag-gemeinsam), Schritt 5) und Claude Code neu starten. Mit `/mcp` prüfen: Welche vier Werkzeuge bietet er an?
   - [ ] *„Nutze wiki-tools und gib mir eine Statistik des Wikis.“* – Fragt der Agent vorher nach? Vergleicht mit `.claude/settings.json`: Warum darf er diese Werkzeuge ohne Rückfrage nutzen, die von GitHub aber nicht?
   - [ ] Zusatz für Schnelle: Ergänzt selbst ein eigenes Werkzeug, z. B. `seiten_ohne_quelle()` (der Agent darf `scripts/` nicht ändern – probiert es ruhig aus), startet Claude Code neu und testet es.
4. **Pipeline: rot, dann grün**
   - [ ] Im Repo unter *Actions* prüfen, ob der Workflow *Wiki-Check* aktiv ist.
   - [ ] *„Lege auf einem neuen Branch `test-ci` die Seite `wiki/test.md` mit einem Satz und ohne Kopfzeile an, committe, pushe und öffne einen Pull Request.“*
   - [ ] Die Pipeline schlägt fehl. *„Lies über GitHub das Ergebnis des Wiki-Checks in meinem Pull Request und behebe die Fehler.“*
   - [ ] Pipeline grün? Pull Request schließen, ohne zu mergen.

**Ergebnis:** Issue angelegt, eigener MCP-Server läuft, ein roter und ein grüner Pipeline-Lauf.
**Zum Nachdenken:** Wer hat den Fehler gefunden – der Agent, die Pipeline oder ihr?

---

## Aufgabe 2

**Teil B · Das LLM-Wiki bauen · 70 + 60 Minuten · einzeln, Review zu zweit**

Ziel: Der Agent baut aus den Rohdokumenten ein Wiki. Ihr steuert über das Schema, prüft das Ergebnis und erlebt den Unterschied zwischen zwei Modellen.

### 2.1 Schema anpassen (10 Min)
- [ ] Lest `AGENTS.md`. Ergänzt unter **Eigene Regeln** zwei Regeln, die euch für ein Firmenwiki wichtig sind (z. B. „Jede Seite endet mit ‚Ansprechperson‘“).
- [ ] Optional: eigene, unkritische Dokumente nach `raw/` legen.

### 2.2 Ingest (25 Min)
- [ ] Neuer Branch: `git switch -c wiki-v1`
- [ ] `/ingest` – lasst den Agenten arbeiten und lest mit, was er tut.
- [ ] Schaut euch `wiki/index.md`, zwei Seiten und `wiki/log.md` an. Stimmt, was da steht?

### 2.3 Query (15 Min)
Stellt mit `/query` mindestens drei Fragen, zum Beispiel:
- [ ] *Wer darf eine Kulanzleistung über 400 EUR freigeben?*
- [ ] *Wie oft muss die FX-200 inspiziert werden?*
- [ ] *Wie lange dauert es derzeit, ein Spindellager SL-40 zu bekommen?*
- [ ] Speichert eine gute Antwort als Seite vom Typ `frage`.

### 2.4 Lint und Pull Request (20 Min)
- [ ] `/lint` – welche Befunde meldet der Agent?
- [ ] `python scripts/check_wiki.py` – grün?
- [ ] Pushen, Pull Request öffnen, Pipeline abwarten.
- [ ] Eure Partnerin oder euer Partner reviewt den Pull Request auf GitHub: eine Stelle, die stimmt, eine, die fehlt oder falsch ist.

### 2.5 Derselbe Agent, anderes Modell (40 Min)
- [ ] Zurück auf `main`, neuer Branch: `git switch main && git switch -c wiki-hs`
- [ ] Claude Code mit dem Dienst der Hochschule starten: `./scripts/start-hs.sh` (Windows: `.\scripts\start-hs.ps1`)
- [ ] `/ingest raw/2026-10-22-protokoll-lenkungskreis.md raw/2026-10-14-mail-lieferant.md raw/2024-onboarding-service.md`
- [ ] Dieselben drei Fragen stellen, `/lint` ausführen, Pipeline laufen lassen.
- [ ] Tabelle ausfüllen:

| | Cloud-Modell (`wiki-v1`) | HS-Dienst (`wiki-hs`) |
|---|---|---|
| Dauer für den Ingest | | |
| Anzahl Seiten | | |
| Quellenangaben korrekt? | | |
| Widersprüche erkannt? | | |
| Fehler in der Pipeline | | |
| Was steht unter „Auffälligkeiten“ im Log? | | |
| Wo würdet ihr welches Modell einsetzen? | | |

**Ergebnis:** ein geprüftes Wiki, ein Review, ein begründeter Modellvergleich.
**Zum Nachdenken:** Welche Aufgabe würdet ihr dem lokalen Modell geben, welche nicht – und was bedeutet das für Datenschutz und Kosten (LE 1–3)?

---

## Aufgabe 3 und 4

Teil C und D bearbeitet ihr auf den Arbeitsblättern. Für das Agent-Manifest gibt es zusätzlich die Vorlage [manifest/AGENT-MANIFEST.md](manifest/AGENT-MANIFEST.md): Am Ende übersetzt ihr eure Regeln in `.claude/settings.json` und `AGENTS.md` – Governance als Konfiguration.
