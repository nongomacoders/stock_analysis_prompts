@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Run setup.ps1 first to create the local environment.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" app.py %*
if errorlevel 1 pause
