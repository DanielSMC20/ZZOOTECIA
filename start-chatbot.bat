@echo off
echo ============================================
echo   CHATBOT IA - ZOOTEC
echo ============================================
echo.

cd /d "%~dp0"

echo Iniciando chatbot en http://localhost:8000
echo.
echo Para detener: Presiona Ctrl+C
echo.

python chatbot.py

pause
