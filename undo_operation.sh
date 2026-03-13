#!/bin/bash
echo "==================================================="
echo "      FILE ORGANIZER - UNDO OPERATION"
echo "==================================================="
echo ""
echo "WARNING: This will attempt to restore files"
echo "moved during the LAST program execution."
echo "Make sure you haven't modified the files meanwhile."
echo ""
read -p "Press Enter to continue..."
echo ""
python3 main.py --undo
echo ""
echo "Restore completed."
