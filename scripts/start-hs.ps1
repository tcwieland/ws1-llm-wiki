# Startet Claude Code gegen den Dienst der Hochschule Coburg (Windows PowerShell).
Set-Location (Join-Path $PSScriptRoot "..")
if (Test-Path .env) {
  Get-Content .env | Where-Object { $_ -match '^\s*([A-Z_]+)\s*=\s*([^#]*)' } | ForEach-Object {
    [Environment]::SetEnvironmentVariable($Matches[1], $Matches[2].Trim(), "Process") }
}
if (-not $env:HS_BASE_URL -or -not $env:HS_MODEL) { Write-Error "Bitte HS_BASE_URL und HS_MODEL in .env eintragen"; exit 1 }
Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
$env:ANTHROPIC_BASE_URL = $env:HS_BASE_URL
$env:ANTHROPIC_AUTH_TOKEN = if ($env:HS_API_KEY) { $env:HS_API_KEY } else { "unbenutzt" }
$env:ANTHROPIC_MODEL = $env:HS_MODEL
$env:ANTHROPIC_DEFAULT_OPUS_MODEL = $env:HS_MODEL
$env:ANTHROPIC_DEFAULT_SONNET_MODEL = $env:HS_MODEL
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL = $env:HS_MODEL
$env:CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC = "1"
Write-Host "Claude Code mit HS-Dienst: $($env:HS_MODEL) @ $($env:HS_BASE_URL)"
claude @args
