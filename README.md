# 🗂️ File-Organizer

File-Organizer is an advanced Python-based file organization tool designed to sort files safely and intelligently. It classifies files by type, avoids dangerous recursion into software and project directories, and provides modern safeguards such as dry-run simulation, undo support, configurable scan depth, and external configuration.

## ⚙️ How It Works

The script scans a target directory and organizes files by extension into predefined categories.  
Before entering folders, it checks whether they appear to belong to installed software, games, or development projects. If it detects executable files, libraries, system-related files, or protected folders such as `.git` or `.venv`, it skips them automatically.

By default, the script only organizes loose files in the selected root folder. This prevents accidental modification of nested application, game, or project directories.

## 🚀 Features

- ✅ Smart app, game, and project detection
- ✅ Safer folder scanning with automatic skip rules
- ✅ Max depth control to limit recursion
- ✅ Dry-run mode to preview actions without moving files
- ✅ Undo mode to restore moved files to their original locations
- ✅ Automatic `config.json` generation for easy customization
- ✅ Duplicate file handling with incremental renaming
- ✅ Support for additional file categories, including 3D, ISO, CSV, and SQL files
- ✅ Detailed logging and error handling

## 🛡️ Safety Improvements

This version was redesigned to avoid the main issue of the old implementation: blindly scanning every subfolder and moving files only by extension.  
Now the script applies protective checks before processing directories, making it much safer to use on disks containing programs, games, websites, and development environments.

## 🛠 Configuration

The script automatically generates a `config.json` file on first launch.  
You can use it to customize:

- Source and destination folders
- Category rules and extensions
- Maximum scan depth
- Protected folders and file patterns
- General organizer behavior without editing the source code

## ⏪ Undo Support

Every moved file is recorded in `history.json`.  
If something is moved incorrectly, you can restore everything with:

```bash
python main.py --undo
