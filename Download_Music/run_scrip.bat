@echo off
cd /d "%~dp0"
git pull --ff-only
.venv\Scripts\python.exe main.py
pause