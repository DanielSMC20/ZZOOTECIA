# Start server (PowerShell)
Write-Host "ZOOTEC IA - Iniciando servidor (PowerShell)"
Set-Location -Path $PSScriptRoot

if (-not (Test-Path -Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "Creando entorno virtual .venv..."
    python -m venv .venv
    Write-Host "Instalando dependencias..."
    .\.venv\Scripts\pip.exe install -r requirements.txt
}

Write-Host "Activando entorno virtual"
. .\.venv\Scripts\Activate.ps1

Write-Host "Iniciando uvicorn main:app en http://localhost:8000"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
