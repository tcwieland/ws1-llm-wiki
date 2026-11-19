# Setup für Workshop 1

Bitte **vor dem Workshop** erledigen. Am Workshoptag bekommt ihr die Zugangsdaten; die Installation sollte dann schon laufen.

## 1 Voraussetzungen

- Laptop mit Administrationsrechten (bei Firmengeräten vorher prüfen)
- **Git** – Test: `git --version`
  - Windows: [Git for Windows](https://git-scm.com/download/win) installieren (Claude Code braucht die mitgelieferte Git Bash)
- **Python 3.12** oder neuer – habt ihr seit LE 0. Test: `python --version`
- **GitHub-Konto** mit aktivierter Zwei-Faktor-Anmeldung
- Ein Editor, z. B. VS Code (optional, aber hilfreich, um das Wiki anzusehen)

## 2 Claude Code installieren

macOS, Linux, WSL:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Windows (PowerShell):

```powershell
irm https://claude.ai/install.ps1 | iex
```

Test: `claude --version` zeigt eine Versionsnummer. Anmelden müsst ihr euch noch nicht – den API-Zugang bekommt ihr im Workshop.

## 3 MCP-SDK für Python

Für den eigenen MCP-Server im Workshop (im selben Python, in dem ihr auch sonst arbeitet, z. B. eurer venv aus LE 0):

```bash
pip install "mcp[cli]<2"
```

Wichtig: Version **unter 2**. `scripts/wiki_mcp.py` nutzt `FastMCP` aus dem SDK 1.x; in mcp 2.x wurde das umbenannt, und der Server startet dann nicht (`CONNECTION_CLOSED`).

Test: `python -c "from mcp.server.fastmcp import FastMCP; print('ok')"` (macOS ggf. `python3`).

## 4 Optional: Codex

Wer Codex zusätzlich ausprobieren möchte (eigenes ChatGPT-Konto oder mit dem HS-Dienst):

```bash
npm install -g @openai/codex     # braucht Node.js 18 oder neuer
```

Codex liest `AGENTS.md` direkt. Für den HS-Dienst in `~/.codex/config.toml`:

```toml
model = "MODELLNAME"
model_provider = "hs"

[model_providers.hs]
name = "HS Coburg"
base_url = "https://HOST-DES-DIENSTES/v1"
env_key = "HS_API_KEY"
wire_api = "responses"
```

## 5 Am Workshoptag (gemeinsam)

1. **Repo anlegen:** auf der Repo-Seite *Use this template → Create a new repository*, Sichtbarkeit **privat**. Dann klonen.
2. **`.env` anlegen:** `.env.example` kopieren, API-Schlüssel und HS-Zugang eintragen. `.env` wird nie committet.
3. **GitHub-Token:** *Settings → Developer settings → Fine-grained tokens → Generate new token*
   - Repository access: *Only select repositories* → euer Workshop-Repo
   - Permissions: Contents, Issues, Pull requests: *Read and write*; Actions: *Read*
   - Token als `GITHUB_PAT` in `.env` eintragen
4. **GitHub-MCP-Server anbinden** (im Repo-Ordner):

   ```bash
   set -a; . ./.env; set +a
   claude mcp add --transport http github https://api.githubcopilot.com/mcp -H "Authorization: Bearer $GITHUB_PAT"
   ```

   Windows (PowerShell), Token direkt einsetzen:

   ```powershell
   claude mcp add --transport http github https://api.githubcopilot.com/mcp -H "Authorization: Bearer <euer Token>"
   ```

   Test: `claude mcp list` zeigt `github` als verbunden. Die Konfiguration liegt lokal bei euch, nicht im Repo.

5. **Eigenen MCP-Server `wiki-tools` anbinden** (im Repo-Ordner):

   ```bash
   claude mcp add wiki-tools -- python "$(pwd)/scripts/wiki_mcp.py"
   ```

   Windows (PowerShell):

   ```powershell
   claude mcp add wiki-tools -- python "$PWD\scripts\wiki_mcp.py"
   ```

   Nehmt das Python, in dem `mcp` installiert ist (macOS ggf. `python3`, venv: vollständiger Pfad zum Python der venv). Test: `claude mcp list` zeigt `wiki-tools` als verbunden.

## Hilfe

- `claude doctor` prüft die Installation.
- Im Workshop gilt: Wer hängt, arbeitet zu zweit an einem Rechner weiter. Niemand verpasst etwas.
