@echo off
REM Avvia SuperAgent come servizio Windows

set VENV_PATH=C:\Users\user\Desktop\m\SuperAgent\venv_superagent
set PYTHON_EXE=%VENV_PATH%\Scripts\python.exe
set SUPERAGENT_PATH=C:\Users\user\Desktop\m\SuperAgent
set LOGFILE=%SUPERAGENT_PATH%\superagent_service.log
cd /d %SUPERAGENT_PATH%
echo Avvio servizio SuperAgent > "%LOGFILE%" 2>&1
"%PYTHON_EXE%" super_agent.py >> "%LOGFILE%" 2>&1
echo Codice uscita: %ERRORLEVEL% >> "%LOGFILE%" 2>&1
