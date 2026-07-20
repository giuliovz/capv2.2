@echo off
setlocal

cd /d %~dp0

echo ========================================
echo CAPTADOR IMOVEIS - INSTALACAO WINDOWS
echo ========================================

where py >nul 2>nul
if %errorlevel% neq 0 (
  echo Python nao encontrado. Instale Python 3.11+ e tente novamente.
  pause
  exit /b 1
)

if not exist .venv-win (
  echo Criando ambiente virtual...
  py -3 -m venv .venv-win
)

call .venv-win\Scripts\activate.bat

echo Atualizando pip...
python -m pip install --upgrade pip

echo Instalando dependencias...
pip install -r requirements.txt

echo Instalando navegador do Playwright...
python -m playwright install chromium

echo ========================================
echo Instalacao concluida.
echo ========================================
echo Para iniciar o sistema: iniciar_dashboard.bat
pause
