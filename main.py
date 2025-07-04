import os
import shutil
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

CONFIG = {
    "SOURCE_DIR": "old",
    "DEST_BASE": "new",
    "LOG_FILE": "file_organizer.log",
    "THREADS": 4,
    "MIN_FILE_SIZE_KB": 10,
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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(CONFIG["LOG_FILE"]),
        logging.StreamHandler()
    ]
)

def get_category(file_extension):
    for category, extensions in CONFIG["CATEGORIES"].items():
        if file_extension.lower() in extensions:
            return category
    return CONFIG["DEFAULT_CATEGORY"]

def handle_existing_file(dest_path):
    base, ext = os.path.splitext(dest_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base}_{timestamp}{ext}"

def should_skip_file(file_path):
    file_size_kb = os.path.getsize(file_path) / 1024
    return file_size_kb < CONFIG["MIN_FILE_SIZE_KB"]

def process_file(file_path, dest_base):
    try:
        if should_skip_file(file_path):
            logging.warning(f"Skipped small file: {os.path.basename(file_path)}")
            return

        filename = os.path.basename(file_path)
        file_extension = os.path.splitext(filename)[1]
        category = get_category(file_extension)
        category_dir = os.path.join(dest_base, category)
        
        os.makedirs(category_dir, exist_ok=True)
        
        dest_path = os.path.join(category_dir, filename)
        
        if os.path.exists(dest_path):
            dest_path = handle_existing_file(dest_path)
        
        shutil.move(file_path, dest_path)
        logging.info(f"Moved: {filename} -> {category_dir}")
        
    except Exception as e:
        logging.error(f"Error processing {file_path}: {str(e)}")

def organize_files(source_dir, dest_base):
    logging.info(f"Starting organization from {source_dir} to {dest_base}")
    
    if not os.path.exists(source_dir):
        logging.error(f"Source directory not found: {source_dir}")
        return
    
    file_count = 0
    start_time = datetime.now()
    
    with ThreadPoolExecutor(max_workers=CONFIG["THREADS"]) as executor:
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    executor.submit(process_file, file_path, dest_base)
                    file_count += 1
    
    elapsed_time = datetime.now() - start_time
    logging.info(f"Organization complete. Processed {file_count} files in {elapsed_time}")

if __name__ == "__main__":
    try:
        organize_files(CONFIG["SOURCE_DIR"], CONFIG["DEST_BASE"])
    except KeyboardInterrupt:
        logging.info("Operation interrupted by user")
    except Exception as e:
        logging.critical(f"Critical error: {str(e)}")
