# 🗂️ File-Organizer

File-Organizer is a smart and safe Python script that automatically organizes files from a source directory into categorized folders based on file type.

Unlike basic organizers, it detects and skips folders belonging to installed software, games, or development projects (such as directories containing `.exe`, `.dll`, `.pak` files or protected folders like `.git` and `.venv`), preventing accidental damage to important files.

## ⚙️ How It Works

- Scans a specified source directory up to a configurable depth.
- Uses `MAX_DEPTH = 0` by default, meaning only loose files in the root folder are organized.
- Identifies file types by extension and classifies them into predefined categories such as Images, Music, Documents, 3D, ISO, CSV, and SQL.
- Moves each file into the corresponding destination subfolder.
- Skips folders that appear to belong to applications, games, or development environments.
- Automatically renames duplicate files with incremental naming such as `foto_1.jpg`, `foto_2.jpg`.
- Logs actions, warnings, and errors to both console and log file.

## 🚀 Features

- ✅ Smart app, game, and project folder detection
- ✅ Max depth control to limit recursion
- ✅ Dry-run mode to preview actions without moving files
- ✅ Undo mode to restore moved files to their original locations
- ✅ Automatic `config.json` generation for easy customization
- ✅ Duplicate-safe renaming with no overwrite
- ✅ Extended file categories including 3D, ISO, CSV, and SQL
- ✅ Detailed logging and graceful error handling

## 🛠️ Configuration

At first launch, the script automatically generates a `config.json` file.

From there, you can customize:

- Source and destination folders
- File categories and extensions
- Maximum scan depth
- Protected folder rules
- General behavior of the organizer

This makes the project easier to configure without editing the source code directly.

## ⏪ Undo

Every move operation is recorded in `history.json`.

To restore moved files to their original locations, run:

```bash
python main.py --undo
```

## 🧪 Dry-Run

To simulate the organization process without moving any files, run:

```bash
python main.py --dry-run
```

This mode lets you preview exactly what the script would do while keeping all files untouched.

## ▶️ How to Run

Place your files in the source folder and run:

```bash
python main.py
```

On first launch, the script will automatically generate `config.json`.

