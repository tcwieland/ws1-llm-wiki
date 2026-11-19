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

Ziel: Der Agent baut aus den Rohdokumenten ein Wiki und schreibt ein eigenes Werkzeug dafür. Ihr steuert über Schema und Spezifikation, prüft das Ergebnis und erlebt den Unterschied zwischen zwei Modellen.

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
- [ ] **Review durch eure Partnerin oder euren Partner** (ca. 8 Min) – das Vier-Augen-Prinzip, bevor etwas nach `main` darf:
  1. **Zugriff geben** (Repo-Inhaber): *Settings → Collaborators → Add people*, GitHub-Namen eintragen. Die Einladung wird per Mail oder unter github.com/notifications angenommen.
  2. **PR öffnen** (Partner): Reiter *Pull requests* → PR `wiki-v1` → Reiter **Files changed**.
  3. **Zwei Kommentare** (über eine Zeile fahren, blaues **+**, *Start a review*):
     - eine Stelle, die **stimmt** – gegen das Rohdokument in `raw/` geprüft (z. B. „Inspektion alle 500 Betriebsstunden – passt zum Wartungshandbuch“);
     - eine Stelle, die **fehlt oder falsch ist** (z. B. Widerspruch nicht markiert, veraltete Zahl, fehlende Quelle, Rohdokument nicht eingearbeitet).
  4. **Abschließen:** *Review changes* → *Comment*, *Approve* oder *Request changes* → *Submit review*.
  5. **Optional nachbessern** (Repo-Inhaber): *„Lies über GitHub die Review-Kommentare in meinem Pull Request und arbeite sie ein.“* Danach läuft die Pipeline erneut.

  *Die Pipeline prüft die Form – ob der Inhalt stimmt, merkt nur ein Mensch.*

### 2.5 Code erzeugen: der Linkgraph (20 Min)
Der Agent schreibt ein Python-Skript, das zeigt, wie die Wiki-Seiten miteinander verlinkt sind – als Grafik, die GitHub direkt darstellt.

- [ ] Neuer Branch auf Basis eures Wikis aus 2.2: `git switch wiki-v1 && git switch -c linkgraph` (auf `main` gibt es noch keine Wiki-Seiten)
- [ ] **Planmodus einschalten:** in Claude Code zweimal **Shift + Tab**, bis unten „plan mode“ steht. Der Agent plant jetzt nur und ändert noch nichts.
- [ ] **Spezifizieren** – gebt den Auftrag ein (gern mit eigenen Ergänzungen):

  > Schreibe ein Python-Skript `tools/wiki_graph.py`, nur mit der Standardbibliothek. Es liest alle Markdown-Dateien in `wiki/`, findet relative Links auf andere Wiki-Seiten und schreibt nach `docs/wiki-graph.md` ein Mermaid-Diagramm (`graph LR`): ein Knoten pro Seite mit dem `titel` aus der Kopfzeile, ein Pfeil pro Link. Seiten, auf die keine andere Seite verlinkt, werden farbig markiert. Schreibe dazu einen Test `tests/test_wiki_graph.py` mit `unittest`, der mit einem kleinen Beispiel-Wiki in einem temporären Ordner arbeitet. Zeig mir zuerst deinen Plan.

- [ ] **Plan prüfen:** Passt er zu eurem Auftrag? Korrigieren oder freigeben – dann setzt der Agent um und fragt vor jeder neuen Datei nach.
- [ ] **Prüfen:** `python -m unittest discover -s tests` – grün? Dann `python tools/wiki_graph.py` ausführen und den Code im Diff lesen: Versteht ihr, was er tut?
- [ ] **Ausliefern:** committen und pushen (`git push -u origin linkgraph`). Auf GitHub den Branch `linkgraph` auswählen und `docs/wiki-graph.md` öffnen – die Grafik erscheint. Welche Seite ist rot markiert, und warum?

*Zusatz für Schnelle – Regel wird Code:* Lasst eure eigene Regel aus 2.1 als zusätzliche Prüfung in `scripts/check_wiki.py` programmieren, mit Test. Dafür müsst ihr die Regel `"Edit(./scripts/**)"` in `.claude/settings.json` selbst von `deny` nach `ask` verschieben – überlegt vorher, warum sie dort stand.

### 2.6 Derselbe Agent, anderes Modell (30 Min)
- [ ] Zurück auf `main`, neuer Branch: `git switch main && git switch -c wiki-hs`
- [ ] Claude Code mit dem Dienst der Hochschule starten: `./scripts/start-hs.sh` (Windows: `.\scripts\start-hs.ps1`)
- [ ] `/ingest raw/2026-10-22-protokoll-lenkungskreis.md raw/2026-10-14-mail-lieferant.md`
- [ ] Dieselben drei Fragen stellen, `/lint` ausführen, Pipeline laufen lassen.
- [ ] Wer Zeit hat: denselben Code-Auftrag aus 2.5 an den HS-Dienst geben (`git switch wiki-v1 && git switch -c linkgraph-hs`) und Code und Test vergleichen.
- [ ] Tabelle ausfüllen:

| | Cloud-Modell (`wiki-v1`) | HS-Dienst (`wiki-hs`) |
|---|---|---|
| Dauer für den Ingest | | |
| Anzahl Seiten | | |
| Quellenangaben korrekt? | | |
| Widersprüche erkannt? | | |
| Fehler in der Pipeline | | |
| Was steht unter „Auffälligkeiten“ im Log? | | |
| Code und Test aus 2.5 (falls verglichen) | | |
| Wo würdet ihr welches Modell einsetzen? | | |

**Ergebnis:** ein geprüftes Wiki, ein Review, ein selbst spezifiziertes und getestetes Skript, ein begründeter Modellvergleich.
**Zum Nachdenken:** Welche Aufgabe würdet ihr dem lokalen Modell geben, welche nicht – und was bedeutet das für Datenschutz und Kosten (LE 1–3)?

---

## Aufgabe 3 und 4

Teil C und D bearbeitet ihr auf den Arbeitsblättern. Für das Agent-Manifest gibt es zusätzlich die Vorlage [manifest/AGENT-MANIFEST.md](manifest/AGENT-MANIFEST.md): Am Ende übersetzt ihr eure Regeln in `.claude/settings.json` und `AGENTS.md` – Governance als Konfiguration.
