import os
import time
import shutil
import numpy as np
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from processor import process_image_data

# --- CONFIG ---
WATCH_FOLDER = os.getenv("WATCH_FOLDER", "/watch")
COMPLETED_FOLDER = os.getenv("COMPLETED_FOLDER", "/completed")
ORIGINALS_FOLDER = os.getenv("ORIGINALS_FOLDER", "/processed_originals")
WHITE_THRESHOLD = int(os.getenv("WHITE_THRESHOLD", 225))
BLACK_THRESHOLD = int(os.getenv("BLACK_THRESHOLD", 150))
SLEEP_BEFORE_PROCESS = float(os.getenv("SLEEP_BEFORE_PROCESS", 1.0))


def process_image(file_path, output_path):
    """Make white areas transparent and enhance black contrast."""
    image = Image.open(file_path)
    processed_image = process_image_data(image, WHITE_THRESHOLD, BLACK_THRESHOLD)
    processed_image.save(output_path, format="PNG")
    print(f"✅ Processed: {os.path.basename(file_path)} → {os.path.basename(output_path)}")


class Watcher(FileSystemEventHandler):
    """Handles new image files dropped into the watched folder."""

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        file_name = os.path.basename(file_path)
        ext = os.path.splitext(file_name)[1].lower()

        if ext not in (".png", ".jpg", ".jpeg"):
            return

        time.sleep(SLEEP_BEFORE_PROCESS)

        try:
            base_name = os.path.splitext(file_name)[0]
            output_path = os.path.join(COMPLETED_FOLDER, f"{base_name}.png")
            process_image(file_path, output_path)

            # Move original to archive folder
            os.makedirs(ORIGINALS_FOLDER, exist_ok=True)
            shutil.move(file_path, os.path.join(ORIGINALS_FOLDER, file_name))
            print(f"📦 Moved original → {ORIGINALS_FOLDER}/{file_name}")

        except Exception as e:
            print(f"❌ Error processing {file_name}: {e}")


if __name__ == "__main__":
    os.makedirs(COMPLETED_FOLDER, exist_ok=True)
    os.makedirs(ORIGINALS_FOLDER, exist_ok=True)

    print(f"👀 Watching folder: {WATCH_FOLDER}")
    observer = Observer()
    event_handler = Watcher()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
