# Startet Claude Code mit dem Anthropic-API-Zugang aus .env (Windows PowerShell).
Set-Location (Join-Path $PSScriptRoot "..")
if (Test-Path .env) {
  Get-Content .env | Where-Object { $_ -match '^\s*([A-Z_]+)\s*=\s*([^#]*)' } | ForEach-Object {
    [Environment]::SetEnvironmentVariable($Matches[1], $Matches[2].Trim(), "Process") }
}
if (-not $env:ANTHROPIC_API_KEY) { Write-Error "Bitte ANTHROPIC_API_KEY in .env eintragen"; exit 1 }
claude @args
