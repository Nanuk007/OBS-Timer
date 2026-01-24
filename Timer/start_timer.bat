@echo off
REM OBS Timer Server Launcher
REM Run this from OBS Scripts section to start the timer

cd /d "%~dp0"
python timer.py
pause
