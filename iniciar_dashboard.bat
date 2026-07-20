@echo off
setlocal

cd /d %~dp0

if not exist .venv-win\Scripts\activate.bat (
  echo Ambiente nao instalado. Rode instalar_pc.bat primeiro.
  pause
  exit /b 1
)

call .venv-win\Scripts\activate.bat
python executar_site.py --open
