#!/usr/bin/env python3
"""Prüft das LLM-Wiki auf die Regeln aus AGENTS.md.

Aufruf:  python scripts/check_wiki.py
Ergebnis: Liste der Fehler, Exit-Code 1 bei Fehlern. Läuft lokal und in GitHub Actions.
Nur Standardbibliothek – keine Installation nötig.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"
SONDERSEITEN = {"index.md", "log.md"}
TYPEN = {"thema", "begriff", "rolle", "dokument", "frage"}
PFLICHT = ("titel", "typ", "quellen", "stand")
GEHEIMNISSE = [
    (r"sk-ant-[A-Za-z0-9_\-]{20,}", "Anthropic-API-Schlüssel"),
    (r"\bsk-(?!ant-)[A-Za-z0-9_\-]{20,}", "API-Schlüssel"),
    (r"\bghp_[A-Za-z0-9]{30,}", "GitHub-Token"),
    (r"\bgithub_pat_[A-Za-z0-9_]{30,}", "GitHub-Token"),
    (r"\bAKIA[0-9A-Z]{16}\b", "AWS-Schlüssel"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "privater Schlüssel"),
]
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
NACKTE_URL = re.compile(r"(?<![(\[<])\bhttps?://[^\s)>\]]+")

fehler: list[tuple[str, str]] = []


def melde(datei: Path | str, text: str) -> None:
    rel = str(datei.relative_to(ROOT)) if isinstance(datei, Path) else datei
    fehler.append((rel, text))


def frontmatter(text: str) -> dict | None:
    """Einfacher YAML-Teilparser: key: wert, Listen mit '- ' oder [a, b]."""
    if not text.startswith("---"):
        return None
    teile = text.split("\n---", 1)
    if len(teile) < 2:
        return None
    daten, schluessel = {}, None
    for zeile in teile[0].splitlines()[1:]:
        roh = zeile.split(" #", 1)[0].rstrip()
        if not roh.strip():
            continue
        m = re.match(r"^([A-Za-zäöüÄÖÜß_]+):\s*(.*)$", roh)
        if m:
            schluessel, wert = m.group(1), m.group(2).strip()
            if wert.startswith("[") and wert.endswith("]"):
                daten[schluessel] = [w.strip().strip("'\"") for w in wert[1:-1].split(",") if w.strip()]
            else:
                daten[schluessel] = wert.strip("'\"") if wert else []
        elif roh.lstrip().startswith("- ") and schluessel:
            if not isinstance(daten.get(schluessel), list):
                daten[schluessel] = []
            daten[schluessel].append(roh.lstrip()[2:].strip().strip("'\""))
    return daten


def erlaubte_domains() -> set[str]:
    datei = ROOT / ".wiki-allowlist"
    if not datei.exists():
        return set()
    return {z.strip().lower() for z in datei.read_text(encoding="utf-8").splitlines()
            if z.strip() and not z.lstrip().startswith("#")}


def domain_erlaubt(url: str, erlaubt: set[str]) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return any(host == d or host.endswith("." + d) for d in erlaubt)


def pruefe_seiten() -> None:
    erlaubt = erlaubte_domains()
    seiten = sorted(WIKI.glob("**/*.md"))
    index = WIKI / "index.md"
    if not index.exists():
        melde("wiki/index.md", "fehlt")
    if not (WIKI / "log.md").exists():
        melde("wiki/log.md", "fehlt")
    verlinkt_von_index: set[Path] = set()

    for seite in seiten:
        text = seite.read_text(encoding="utf-8")

        # Links prüfen
        for ziel in LINK.findall(text):
            if ziel.startswith(("http://", "https://")):
                if not domain_erlaubt(ziel, erlaubt):
                    melde(seite, f"externer Link auf nicht erlaubte Domain: {ziel}")
                continue
            if ziel.startswith(("#", "mailto:")):
                continue
            pfad = (seite.parent / ziel.split("#", 1)[0]).resolve()
            if not pfad.exists():
                melde(seite, f"Link ins Leere: {ziel}")
            elif seite == index:
                verlinkt_von_index.add(pfad)
        for url in NACKTE_URL.findall(text):
            if not domain_erlaubt(url, erlaubt):
                melde(seite, f"externe URL auf nicht erlaubte Domain: {url}")

        if seite.name in SONDERSEITEN and seite.parent == WIKI:
            continue

        # Frontmatter prüfen
        fm = frontmatter(text)
        if fm is None:
            melde(seite, "Frontmatter fehlt (Kopf zwischen --- und ---, siehe AGENTS.md)")
            continue
        for feld in PFLICHT:
            if feld not in fm or fm[feld] in ("", []):
                melde(seite, f"Pflichtfeld '{feld}' fehlt oder ist leer")
        if fm.get("typ") and fm["typ"] not in TYPEN:
            melde(seite, f"unbekannter typ '{fm['typ']}' (erlaubt: {', '.join(sorted(TYPEN))})")
        if fm.get("stand"):
            try:
                date.fromisoformat(str(fm["stand"]))
            except ValueError:
                melde(seite, f"stand '{fm['stand']}' ist kein Datum im Format JJJJ-MM-TT")
        quellen = fm.get("quellen") or []
        if isinstance(quellen, str):
            quellen = [quellen]
        for q in quellen:
            if not q.startswith("raw/"):
                melde(seite, f"Quelle '{q}' liegt nicht in raw/")
            elif not (ROOT / q).exists():
                melde(seite, f"Quelle '{q}' existiert nicht")

    for seite in seiten:
        if seite.name in SONDERSEITEN and seite.parent == WIKI:
            continue
        if seite.resolve() not in verlinkt_von_index:
            melde(seite, "nicht von wiki/index.md aus verlinkt (verwaiste Seite)")


def pruefe_geheimnisse() -> None:
    for datei in ROOT.rglob("*"):
        if not datei.is_file() or ".git" in datei.parts or datei.name in (".env", "check_wiki.py"):
            continue
        if datei.suffix.lower() not in {".md", ".txt", ".json", ".yml", ".yaml", ".toml", ".py", ".sh", ".ps1", ".csv", ""}:
            continue
        try:
            text = datei.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for muster, art in GEHEIMNISSE:
            if re.search(muster, text):
                melde(datei, f"mögliches Geheimnis gefunden ({art}) – entfernen und Schlüssel sperren!")


def pruefe_raw_unveraendert() -> None:
    """raw/ darf ergänzt, aber nicht verändert oder gelöscht werden."""
    basis = os.environ.get("GITHUB_BASE_REF")
    bereich = f"origin/{basis}...HEAD" if basis else "HEAD~1..HEAD"
    try:
        aus = subprocess.run(["git", "diff", "--name-status", bereich, "--", "raw/"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return   # kein Git-Verlauf verfügbar (z. B. erster Commit) – Prüfung überspringen
    for zeile in aus.splitlines():
        status, *pfade = zeile.split("\t")
        if status[0] in "MDR":
            melde(pfade[-1], f"Rohdokument wurde verändert oder gelöscht (Status {status}) – raw/ ist unveränderlich")


def main() -> int:
    pruefe_seiten()
    pruefe_geheimnisse()
    pruefe_raw_unveraendert()
    in_actions = os.environ.get("GITHUB_ACTIONS") == "true"
    seiten = [p for p in WIKI.glob("**/*.md") if p.name not in SONDERSEITEN]
    if not fehler:
        print(f"✅ Wiki-Check bestanden: {len(seiten)} Seiten, keine Fehler.")
        return 0
    print(f"❌ Wiki-Check: {len(fehler)} Fehler in {len(seiten)} Seiten\n")
    for datei, text in fehler:
        print(f"  {datei}: {text}")
        if in_actions:
            print(f"::error file={datei}::{text}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
