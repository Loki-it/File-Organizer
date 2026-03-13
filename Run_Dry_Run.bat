@echo off
echo ===================================================
echo       FILE ORGANIZER - DRY RUN MODE
echo ===================================================
echo.
echo This is a SIMULATION (Dry-Run).
echo Files will NOT be physically moved.
echo Only logs of what would be done will be shown.
echo.
py main.py --dry-run
echo.
echo Simulation completed. Press any key to exit.
pause >nul
