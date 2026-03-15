🗂️ File-Organizer

File-Organizer is a smart and safe Python script that automatically organizes files from a source directory into categorized folders based on file type.

Unlike basic organizers, it detects and skips folders belonging to installed software, games, or development projects (such as folders containing .exe, .dll, .pak files or protected directories like .git and .venv), preventing accidental damage to your system.

⚙️ How It Works

- Scans a specified source directory up to a configurable depth (MAX_DEPTH=0 by default, meaning only root-level loose files are organized)
- Identifies the file type by extension and classifies it into predefined categories (e.g., Images, Music, Documents, 3D, ISO, CSV, SQL)
- Moves each file to a corresponding subfolder under the destination base
- Skips folders that appear to belong to applications, games, or development environments
- Automatically renames files if a name conflict occurs (incremental renaming: foto_1.jpg, foto_2.jpg)
- Logs all actions and warnings to both console and a .log file

🚀 Features

✅ Smart app, game, and project folder detection
✅ Max depth control to limit recursion
✅ Dry-run mode to preview actions without moving files (--dry-run)
✅ Undo mode to restore all moved files to their original location (--undo)
✅ Auto-generated config.json for easy customization without editing source code
✅ Duplicate file handling with incremental renaming (no overwrite)
✅ Extended categories: 3D files, ISO, CSV, SQL and more
✅ Detailed logging and graceful error handling

🛠 Configuration

On first launch, the script automatically generates a config.json file. From there you can customize source and destination folders, categories, extensions, scan depth, and protected folder rules — no need to touch the source code.

⏪ Undo

Every operation is recorded in history.json. To restore all moved files to their original location:
python main.py --undo

🧪 Dry-Run

To simulate the entire process without moving any file:
python main.py --dry-run

▶️ How to Run

Place your files in the source folder and run:
python main.py
