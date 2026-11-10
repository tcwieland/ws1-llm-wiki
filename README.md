# Workshop 1 · LLM-Wiki mit Claude Code

**AI Solution Architect 2026 · Workshop 1: Agentic Coding, MCP & Ethik**
Prof. Dr. Thomas Wieland, Hochschule Coburg

In diesem Repository baut ihr im Laufe des Tages ein **LLM-Wiki**: Ein Agent liest Rohdokumente und pflegt daraus ein verlinktes Markdown-Wiki. Eine Pipeline prüft jede Änderung, und am Ende schreibt ihr die Regeln, nach denen der Agent arbeiten darf.

| Teil | Was ihr hier macht | Datei |
|---|---|---|
| A | Repo, Agent, GitHub-MCP-Server und Pipeline einrichten | [AUFGABEN.md](AUFGABEN.md#aufgabe-1) |
| B | Das Wiki vom Agenten bauen lassen – mit Cloud-Modell und mit dem Dienst der Hochschule | [AUFGABEN.md](AUFGABEN.md#aufgabe-2) |
| C | Human-in-the-Loop-Leitlinien (Arbeitsblatt) | – |
| D | Agent-Manifest – für das Team und als Konfiguration | [manifest/AGENT-MANIFEST.md](manifest/AGENT-MANIFEST.md) |

## Aufbau

```
raw/                 Rohdokumente (fiktiv) – der Agent liest, ändert aber nie
wiki/                das Wiki – hier schreibt der Agent
AGENTS.md            Schema und Regeln für den Agenten (Codex liest diese Datei direkt)
CLAUDE.md            bindet AGENTS.md für Claude Code ein
.claude/             Befehle /ingest, /query, /lint und die Rechte des Agenten
.github/workflows/   Pipeline: prüft das Wiki nach jedem Push
scripts/             Prüfskript und Startskripte (Anthropic-API oder HS-Dienst)
manifest/            Vorlage für euer Agent-Manifest (Teil D)
```

## Schnellstart

1. Oben rechts **Use this template → Create a new repository** (privat), dann klonen.
2. `.env.example` nach `.env` kopieren und die Zugangsdaten eintragen, die ihr im Workshop bekommt.
3. Claude Code starten: `./scripts/start-claude.sh` (Windows: `.\scripts\start-claude.ps1`).
4. Weiter mit [AUFGABEN.md](AUFGABEN.md).

Installation und Voraussetzungen: [SETUP.md](SETUP.md).

## Prüfen

```bash
python scripts/check_wiki.py
```

Prüft Kopfzeilen, Quellen, Links, verwaiste Seiten, erlaubte externe Domains, versehentlich eingecheckte Schlüssel und ob jemand `raw/` verändert hat. Dieselbe Prüfung läuft in GitHub Actions.
