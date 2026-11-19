#!/usr/bin/env python3
"""wiki-tools: ein eigener MCP-Server für das LLM-Wiki.

Stellt dem Agenten vier Werkzeuge bereit – alle nur lesend:
  wiki_suchen     Begriff im Wiki suchen
  seite_lesen     eine Wiki-Seite lesen
  wiki_pruefen    scripts/check_wiki.py ausführen
  wiki_statistik  Überblick: Seiten, Quellen, Widersprüche, Auffälligkeiten

Installation:  pip install "mcp[cli]"
Anbinden:      claude mcp add wiki-tools -- python "$(pwd)/scripts/wiki_mcp.py"
Testen:        mcp dev scripts/wiki_mcp.py   (öffnet den MCP Inspector im Browser)
"""
from __future__ import annotations

import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

from mcp.server.fastmcp import FastMCP

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"

mcp = FastMCP("wiki-tools")


def _seiten() -> list[Path]:
    return sorted(WIKI.glob("**/*.md"))


def _typ(text: str) -> str:
    m = re.search(r"^typ:\s*(\w+)", text, re.M)
    return m.group(1) if m else "ohne Typ"


@mcp.tool()
def wiki_suchen(begriff: str, max_treffer: int = 10) -> str:
    """Sucht einen Begriff (ohne Groß-/Kleinschreibung) in allen Wiki-Seiten.
    Gibt pro Treffer die Seite und die passende Zeile zurück."""
    treffer = []
    for seite in _seiten():
        for nr, zeile in enumerate(seite.read_text(encoding="utf-8").splitlines(), 1):
            if begriff.lower() in zeile.lower():
                treffer.append(f"{seite.relative_to(ROOT)}:{nr}: {zeile.strip()}")
                if len(treffer) >= max_treffer:
                    return "\n".join(treffer) + "\n… (weitere Treffer abgeschnitten)"
    return "\n".join(treffer) if treffer else f"Keine Treffer für „{begriff}“ im Wiki."


@mcp.tool()
def seite_lesen(name: str) -> str:
    """Liest eine Wiki-Seite, z. B. 'index' oder 'freigabe-von-kulanz.md'.
    Nur Dateien im Ordner wiki/ sind erlaubt."""
    datei = (WIKI / (name if name.endswith(".md") else f"{name}.md")).resolve()
    if WIKI.resolve() not in datei.parents:
        return "Abgelehnt: Es dürfen nur Seiten im Ordner wiki/ gelesen werden."
    if not datei.exists():
        return f"Seite {name} gibt es nicht. Verfügbar: " + ", ".join(p.stem for p in _seiten())
    return datei.read_text(encoding="utf-8")


@mcp.tool()
def wiki_pruefen() -> str:
    """Führt die Wiki-Prüfung (scripts/check_wiki.py) aus – dieselbe Prüfung wie in der Pipeline."""
    lauf = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_wiki.py")],
                          cwd=ROOT, capture_output=True, text=True, timeout=60)
    return (lauf.stdout + lauf.stderr).strip()


@mcp.tool()
def wiki_statistik() -> str:
    """Überblick über das Wiki: Seiten nach Typ, eingearbeitete und offene Rohdokumente,
    markierte Widersprüche und Einträge unter „Auffälligkeiten“."""
    seiten = [p for p in _seiten() if p.name not in ("index.md", "log.md")]
    texte = {p: p.read_text(encoding="utf-8") for p in seiten}
    typen = Counter(_typ(t) for t in texte.values())
    zitiert = {q for t in texte.values() for q in re.findall(r"raw/[\w\-.]+\.md", t)}
    rohdokumente = {f"raw/{p.name}" for p in RAW.glob("*.md") if p.name != "README.md"}
    widersprueche = sum(t.count("**Widerspruch:**") for t in texte.values())
    log = (WIKI / "log.md").read_text(encoding="utf-8") if (WIKI / "log.md").exists() else ""
    auffaellig = log.split("## Auffälligkeiten", 1)[1] if "## Auffälligkeiten" in log else ""
    eintraege = [z for z in auffaellig.splitlines() if z.strip().startswith(("-", "|", "*")) and "---" not in z]
    zeilen = [f"Seiten: {len(seiten)} (" + ", ".join(f"{k}: {v}" for k, v in sorted(typen.items())) + ")",
              f"Rohdokumente: {len(rohdokumente)}, davon im Wiki zitiert: {len(rohdokumente & zitiert)}",
              f"Noch nicht zitiert: {', '.join(sorted(rohdokumente - zitiert)) or '–'}",
              f"Markierte Widersprüche: {widersprueche}",
              f"Einträge unter „Auffälligkeiten“: {len(eintraege)}"]
    return "\n".join(zeilen)


if __name__ == "__main__":
    mcp.run()   # spricht über stdio mit dem Agenten
