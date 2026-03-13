import os
import shutil
import logging
import json
import argparse
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

DEFAULT_CONFIG = {
    "paths": {
        "source_folder": "to_organize",
        "destination_folder": "organized_files"
    },
    "behavior": {
        "max_depth": 0,
        "min_size_kb": 0,
        "dry_run": False
    },
    "security": {
        "ignore_app_folders": True,
        "app_folder_indicators": [
            ".exe", ".dll", ".ini", ".bat", ".sh", "node_modules", ".git", 
            "bin", "lib", "Program Files", ".app", "package.json", "steamapps", ".pak"
        ],
        "specific_folders_to_ignore": [
            ".git", ".svn", "node_modules", "venv", ".venv", "__pycache__", "Windows", "Program Files", "AppData"
        ]
    },
    "system": {
        "log_file": "file_organizer.log",
        "history_file": "history.json",
        "threads": 4
    },
    "categories": {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".svg", ".raw", ".ico", ".heic"],
        "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma", ".midi"],
        "Video": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".mpeg"],
        "Documents": [".doc", ".docx", ".pdf", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".md"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".iso", ".bz2", ".xz"],
        "Programs_and_Installers": [".msi", ".dmg", ".pkg", ".deb", ".rpm", ".apk"],
        "Code_Development": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".php", ".json", ".xml", ".sql", ".ts"],
        "Graphics_and_3D": [".obj", ".fbx", ".blend", ".stl", ".psd", ".ai", ".prproj"]
    },
    "default_category": "Other"
}

def setup_logger(log_file):
    logger = logging.getLogger("FileOrganizer")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    return logger

class FileOrganizer:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.parse_config()
        
        self.logger = setup_logger(self.log_file)
        self.history = []
        
    def load_config(self):
        if not os.path.exists(self.config_path):
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
            print(f"[INFO] Configuration 'config.json' automatically created at: {self.config_path}")
            return DEFAULT_CONFIG
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(f"[ERROR] The file {self.config_path} is not a valid JSON. Default configuration will be used.")
                return DEFAULT_CONFIG

    def parse_config(self):
        paths = self.config.get("paths", DEFAULT_CONFIG["paths"])
        behavior = self.config.get("behavior", DEFAULT_CONFIG["behavior"])
        security = self.config.get("security", DEFAULT_CONFIG["security"])
        system = self.config.get("system", DEFAULT_CONFIG["system"])

        self.source_dir_default = paths.get("source_folder", "to_organize")
        self.dest_base_default = paths.get("destination_folder", "organized_files")

        self.max_depth = behavior.get("max_depth", 0)
        self.min_size_kb = behavior.get("min_size_kb", 0)
        self.dry_run_default = behavior.get("dry_run", False)

        self.ignore_apps = security.get("ignore_app_folders", True)
        self.app_indicators = security.get("app_folder_indicators", DEFAULT_CONFIG["security"]["app_folder_indicators"])
        self.ignore_dirs = set(security.get("specific_folders_to_ignore", DEFAULT_CONFIG["security"]["specific_folders_to_ignore"]))

        self.log_file = system.get("log_file", "file_organizer.log")
        self.history_file = system.get("history_file", "history.json")
        self.threads = system.get("threads", 4)

        self.categories = self.config.get("categories", DEFAULT_CONFIG["categories"])
        self.default_category = self.config.get("default_category", "Other")

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def save_history(self):
        if not self.history:
            return
            
        existing_history = self.load_history()
        existing_history.extend(self.history)
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(existing_history, f, indent=4, ensure_ascii=False)

    def undo_last_operation(self):
        historyList = self.load_history()
        if not historyList:
            self.logger.info("Nothing to undo. The history is empty.")
            return

        self.logger.info(f"Undo in progress: restoring {len(historyList)} files/folders...")
        
        failed_restores = []
        for move in reversed(historyList):
            original = move['original_path']
            current = move['new_path']
            
            if os.path.exists(current):
                os.makedirs(os.path.dirname(original), exist_ok=True)
                try:
                    shutil.move(current, original)
                    self.logger.info(f"Restored: {original}")
                except Exception as e:
                    self.logger.error(f"Cannot restore {current} to {original}: {e}")
                    failed_restores.append(move)
            else:
                self.logger.warning(f"File not found for restoration: {current}")
                failed_restores.append(move)

        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(failed_restores, f, indent=4, ensure_ascii=False)
            
        success_count = len(historyList) - len(failed_restores)
        self.logger.info(f"Undo completed. {success_count} succeeded, {len(failed_restores)} failed.")

    def is_app_folder(self, folder_path):
        """Intelligently detects if a folder is a software installation, game, or source code."""
        if not self.ignore_apps:
            return False
            
        try:
            items = os.listdir(folder_path)
            exe_dll_count = sum(1 for item in items if item.lower().endswith(('.exe', '.dll', '.so', '.pak')))
            if exe_dll_count > 0:
                return True
                
            for item in items:
                if item in self.app_indicators:
                    return True
                if any(item.lower().endswith(ind.lower()) for ind in self.app_indicators if ind.startswith('.')):
                    return True
        except PermissionError:
            return True
        except Exception as e:
            self.logger.debug(f"Error checking app folder {folder_path}: {e}")
            
        return False

    def get_category(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        for category, extensions in self.categories.items():
            if ext in extensions:
                return category
        return self.default_category

    def generate_unique_path(self, dest_path):
        if not os.path.exists(dest_path):
            return dest_path
            
        base, ext = os.path.splitext(dest_path)
        counter = 1
        new_path = f"{base}_{counter}{ext}"
        while os.path.exists(new_path):
            counter += 1
            new_path = f"{base}_{counter}{ext}"
        return new_path

    def process_file(self, file_path, dest_base, dry_run=False):
        try:
            file_size_kb = os.path.getsize(file_path) / 1024
            if self.min_size_kb > 0 and file_size_kb < self.min_size_kb:
                self.logger.debug(f"Skipped too small file ({file_size_kb:.2f} KB): {os.path.basename(file_path)}")
                return None

            filename = os.path.basename(file_path)
            category = self.get_category(file_path)
            category_dir = os.path.join(dest_base, category)
            dest_path = os.path.join(category_dir, filename)
            
            dest_path = self.generate_unique_path(dest_path)

            if dry_run:
                self.logger.info(f"[DRY-RUN] Would move: {file_path} -> {dest_path}")
                return None

            os.makedirs(category_dir, exist_ok=True)
            shutil.move(file_path, dest_path)
            
            self.logger.info(f"Moved: {os.path.basename(file_path)} -> {category}")
            
            return {
                "original_path": file_path,
                "new_path": dest_path,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {str(e)}")
            return None

    def gather_files_to_process(self, source_dir):
        files_to_process = []
        source_path = Path(source_dir).resolve()
        
        for root, dirs, files in os.walk(source_dir):
            root_path = Path(root).resolve()
            
            try:
                depth = len(root_path.relative_to(source_path).parts)
            except ValueError:
                depth = 0 
                
            if self.max_depth != -1 and depth > self.max_depth:
                dirs.clear() 
                continue
                
            for i in range(len(dirs)-1, -1, -1):
                d = dirs[i]
                d_path = os.path.join(root, d)
                
                if d in self.ignore_dirs:
                    self.logger.debug(f"Skipped ignored directory by name: {d_path}")
                    del dirs[i]
                    continue
                    
                if self.is_app_folder(d_path):
                    self.logger.warning(f"✔ DETECTED SOFTWARE/GAME FOLDER, skipping to protect it: {d_path}")
                    del dirs[i]
                    continue

            for file in files:
                files_to_process.append(os.path.join(root, file))
                
        return files_to_process

    def run(self, source_dir=None, dest_base=None, dry_run=None):
        source_dir = source_dir or self.source_dir_default
        dest_base = dest_base or self.dest_base_default
        dry_run = dry_run if dry_run is not None else self.dry_run_default
        
        self.logger.info(f"Starting file organization.\nSource Dir: {source_dir}\nDestination Dir: {dest_base}")
        if dry_run:
            self.logger.info("============== DRY-RUN MODE ACTIVE - NO FILES WILL BE MOVED ==============")
            
        if not os.path.exists(source_dir):
            self.logger.warning(f"Source folder not found: '{source_dir}'. Creating it automatically...")
            os.makedirs(source_dir, exist_ok=True)
            
        if not os.path.isdir(source_dir):
            self.logger.error(f"The source path is not a folder: {source_dir}")
            return
            
        if not os.path.exists(dest_base):
            self.logger.warning(f"Destination folder not found: '{dest_base}'. Creating it automatically...")
            os.makedirs(dest_base, exist_ok=True)
            
        files_to_process = self.gather_files_to_process(source_dir)
        self.logger.info(f"Found {len(files_to_process)} suitable files to process.")
        
        if not files_to_process:
            self.logger.info("No files to process. Operation terminated.")
            return
            
        start_time = datetime.now()
        successful_moves = 0
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            future_to_file = {
                executor.submit(self.process_file, fp, dest_base, dry_run): fp 
                for fp in files_to_process
            }
            
            for future in as_completed(future_to_file):
                result = future.result()
                if result:
                    self.history.append(result)
                    successful_moves += 1
                    
        if not dry_run and self.history:
            self.save_history()
            
        elapsed = datetime.now() - start_time
        self.logger.info(f"Operation completed! Successfully processed {successful_moves} files in {elapsed}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Smart File Organizer")
    parser.add_argument("--source", type=str, help="Source folder")
    parser.add_argument("--dest", type=str, help="Destination folder")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without moving files")
    parser.add_argument("--undo", action="store_true", help="Restore the last organization operation")
    
    args = parser.parse_args()
    
    organizer = FileOrganizer()
    
    if args.undo:
        organizer.undo_last_operation()
    else:
        dr_param = True if args.dry_run else None
        organizer.run(source_dir=args.source, dest_base=args.dest, dry_run=dr_param)
