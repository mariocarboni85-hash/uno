@echo off
REM Installazione Super Agent su Windows
python --version >nul 2>&1 || (echo Python non trovato, installalo manualmente & exit /b)
pip install --upgrade pip
pip install flask requests psutil pyjwt
xcopy /E /I super_agent "C:\Program Files\SuperAgent"
REM Configura servizi con nssm
nssm install SuperAgentAuth "C:\Program Files\SuperAgent\services\auth_service.py"
nssm start SuperAgentAuth
nssm install SuperAgentExecutor "C:\Program Files\SuperAgent\services\executor\service.py"
nssm start SuperAgentExecutor
REM Ripeti per tutti i servizi...
echo Installazione completata. Avvia Super Agent dal collegamento sul desktop.
pause
