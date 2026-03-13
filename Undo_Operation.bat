@echo off
echo ===================================================
echo       FILE ORGANIZER - UNDO OPERATION
echo ===================================================
echo.
echo WARNING: This will attempt to restore files
echo moved during the LAST program execution.
echo Make sure you haven't modified the files meanwhile.
echo.
pause
echo.
python main.py --undo
echo.
echo Restore completed. Press any key to exit.
pause >nul
