@echo off
REM Convenience launcher for Windows.
REM Sets up the virtual environment (via run.py) and starts the app.
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel%==0 (
    python run.py
) else (
    py run.py
)

pause
