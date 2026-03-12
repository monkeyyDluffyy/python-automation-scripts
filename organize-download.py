import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

# Set your downloads path
DOWNLOADS_PATH = os.path.expanduser("~/Downloads")

# File type mapping
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Documents": [".pdf", ".docx", ".doc", ".pptx", ".xlsx", ".txt"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Code": [".py", ".js", ".java", ".cpp", ".html", ".css", ".json"],
    "Installers": [".exe", ".deb", ".msi", ".dmg", ".appimage"]
}


def get_folder(extension):
    for folder, extensions in FILE_TYPES.items():
        if extension.lower() in extensions:
            return folder
    return "Others"


def move_file(file_path):
    if not os.path.isfile(file_path):
        return

    filename = os.path.basename(file_path)
    extension = os.path.splitext(filename)[1]

    folder_name = get_folder(extension)
    destination_folder = os.path.join(DOWNLOADS_PATH, folder_name)

    # Create folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    destination_path = os.path.join(destination_folder, filename)

    try:
        shutil.move(file_path, destination_path)
        print(f"Moved {filename} → {folder_name}")
    except Exception as e:
        print(f"Error moving {filename}: {e}")


class DownloadHandler(FileSystemEventHandler):

    def on_created(self, event):
        if not event.is_directory:
            time.sleep(4)  # wait for download to finish
            move_file(event.src_path)


if __name__ == "__main__":
    print("Monitoring Downloads folder...")

    event_handler = DownloadHandler()
    observer = Observer()
    observer.schedule(event_handler, DOWNLOADS_PATH, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()