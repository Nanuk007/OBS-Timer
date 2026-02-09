@echo off
REM OBS Timer Server Launcher
REM Run this to start the timer server on http://localhost:5000

cd /d "%~dp0"
call venv\Scripts\activate.bat
python app.py
pause
