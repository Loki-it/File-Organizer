# 🗂️ File-Organizer

This Python script automatically organizes files from a **source directory** into categorized folders based on file type. It supports **multithreading** for efficient parallel file processing and includes logging, file size filtering, and conflict handling via timestamp renaming.

---

## ⚙️ How It Works

- Scans a specified source directory (`old/`) recursively.
- Identifies the file type by extension and classifies it into predefined categories (e.g., Images, Music, Documents).
- Moves each file to a corresponding subfolder under the destination base (`new/`).
- Skips files smaller than a configured size threshold.
- Automatically renames files if a name conflict occurs (adds a timestamp).
- Logs all actions and warnings to both console and a `.log` file.

---

## 🚀 Features

- ✅ Multi-threaded file processing (`ThreadPoolExecutor`)
- ✅ Customizable categories and extensions
- ✅ File size filtering
- ✅ Duplicate file handling with timestamp renaming
- ✅ Detailed logging to console and file
- ✅ Graceful error handling and keyboard interrupt support

---

## 🛠 Configuration

You can change behavior by editing the `CONFIG` dictionary in the script:

```python
CONFIG = {
    "SOURCE_DIR": "old",                  # Directory to organize
    "DEST_BASE": "new",                   # Base destination directory
    "LOG_FILE": "file_organizer.log",     # Log file name
    "THREADS": 4,                         # Number of worker threads
    "MIN_FILE_SIZE_KB": 10,               # Minimum file size in KB
    "CATEGORIES": {
        "Images": (".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff"),
        "Music": (".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"),
        "Videos": (".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"),
        "Documents": (".doc", ".docx", ".pdf", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"),
        "Archives": (".zip", ".rar", ".7z", ".tar", ".gz"),
        "Programs": (".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm"),
        "Code": (".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".php", ".sh"),
    },
    "DEFAULT_CATEGORY": "Other"
}
```
## 📁 Example Folder Structure

**Before:**
```
old/
├── picture.jpg
├── song.mp3
├── archive.zip
└── report.pdf
```
**After:**
```
new/
├── Images/
│ └── picture.jpg
├── Music/
│ └── song.mp3
├── Archives/
│ └── archive.zip
├── Documents/
│ └── report.pdf
```
---

## ▶️ How to Run

1. Place your files in the source folder (e.g., `old/`)
2. Run the script:

```bash
python3 main.py
