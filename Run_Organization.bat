@echo off
echo ===================================================
echo       FILE ORGANIZER - START ORGANIZATION
echo ===================================================
echo.
echo WARNING: This operation will physically move files
echo based on the rules set in config.json.
echo.
pause
echo.
py main.py
echo.
echo Operation completed. Press any key to exit.
pause >nul
