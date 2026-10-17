$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    throw 'uv is required. Install it from https://docs.astral.sh/uv/getting-started/installation/ and rerun this script.'
}
if (-not (Test-Path -LiteralPath '.venv\Scripts\python.exe')) {
    uv --cache-dir tmp/uv-cache venv --python 3.12 .venv
    if ($LASTEXITCODE -ne 0) { throw "uv venv failed: $LASTEXITCODE" }
}
$requirementsPath = if (Test-Path -LiteralPath 'requirements.lock.txt') { 'requirements.lock.txt' } else { 'requirements.txt' }
uv --cache-dir tmp/uv-cache pip install --python .venv/Scripts/python.exe -r $requirementsPath
if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed: $LASTEXITCODE" }
Write-Host 'Ready. Double-click Run Capture.cmd, or run .venv\Scripts\python.exe app.py'
