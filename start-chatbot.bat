@echo off
cd /d "%~dp0"

REM Lanzador automatico: crea venv e instala dependencias si es necesario

if not exist ".venv\Scripts\activate.bat" (
	echo.
	echo [ZOOTEC-IA] Creando entorno virtual .venv...
	python -m venv .venv
	if errorlevel 1 (
		echo ERROR: No se pudo crear el entorno virtual.
		echo Asegurate de tener Python 3.8+ instalado.
		pause
		exit /b 1
	)
	echo.
	echo [ZOOTEC-IA] Instalando dependencias...
	call .venv\Scripts\activate.bat
	pip install -r requirements.txt
	if errorlevel 1 (
		echo ERROR: No se pudieron instalar las dependencias.
		pause
		exit /b 1
	)
) else (
	call .venv\Scripts\activate.bat
)

echo.
echo [ZOOTEC-IA] Iniciando servidor en http://localhost:8000
echo Presiona Ctrl+C para detener el servidor.
echo.
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
