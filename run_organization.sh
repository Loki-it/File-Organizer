#!/bin/bash
echo "==================================================="
echo "      FILE ORGANIZER - START ORGANIZATION"
echo "==================================================="
echo ""
echo "WARNING: This operation will physically move files"
echo "based on the rules set in config.json."
echo ""
read -p "Press Enter to continue..."
echo ""
python3 main.py
echo ""
echo "Operation completed."
