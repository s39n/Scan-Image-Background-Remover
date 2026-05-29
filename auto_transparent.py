import os
import time
import shutil
import argparse
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from processor import process_image_data

def process_image(file_path, output_path, white_threshold, black_threshold):
    """Make white areas transparent and enhance black contrast."""
    try:
        image = Image.open(file_path)
        processed_image = process_image_data(image, white_threshold, black_threshold)
        processed_image.save(output_path, format="PNG")
        print(f"✅ Processed: {os.path.basename(file_path)} → {os.path.basename(output_path)}")
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")

def scan_existing_files(watch_folder, completed_folder, originals_folder, white_threshold, black_threshold):
    """Process any images already in the watch folder on startup."""
    print(f"🔍 Scanning for existing files in: {watch_folder}")
    if not os.path.exists(watch_folder):
        os.makedirs(watch_folder, exist_ok=True)
        return

    for file_name in os.listdir(watch_folder):
        file_path = os.path.join(watch_folder, file_name)
        if os.path.isfile(file_path):
            ext = os.path.splitext(file_name)[1].lower()
            if ext in (".png", ".jpg", ".jpeg"):
                try:
                    base_name = os.path.splitext(file_name)[0]
                    output_path = os.path.join(completed_folder, f"{base_name}.png")
                    process_image(file_path, output_path, white_threshold, black_threshold)

                    # Move original to archive folder
                    os.makedirs(originals_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(originals_folder, file_name))
                    print(f"📦 Moved original → {originals_folder}/{file_name}")
                except Exception as e:
                    print(f"❌ Error processing existing file {file_name}: {e}")

class Watcher(FileSystemEventHandler):
    """Handles new image files dropped into the watched folder."""
    def __init__(self, watch_folder, completed_folder, originals_folder, white_threshold, black_threshold, sleep_time):
        self.watch_folder = watch_folder
        self.completed_folder = completed_folder
        self.originals_folder = originals_folder
        self.white_threshold = white_threshold
        self.black_threshold = black_threshold
        self.sleep_time = sleep_time

    def on_created(self, event):
        self._handle_event(event)

    def on_moved(self, event):
        self._handle_event(event, is_move=True)

    def _handle_event(self, event, is_move=False):
        if event.is_directory:
            return

        file_path = event.dest_path if is_move else event.src_path
        file_name = os.path.basename(file_path)
        ext = os.path.splitext(file_name)[1].lower()

        if ext not in (".png", ".jpg", ".jpeg"):
            return

        print(f"✨ New file detected: {file_name}")
        time.sleep(self.sleep_time)

        try:
            base_name = os.path.splitext(file_name)[0]
            output_path = os.path.join(self.completed_folder, f"{base_name}.png")
            process_image(file_path, output_path, self.white_threshold, self.black_threshold)

            # Move original to archive folder
            os.makedirs(self.originals_folder, exist_ok=True)
            shutil.move(file_path, os.path.join(self.originals_folder, file_name))
            print(f"📦 Moved original → {self.originals_folder}/{file_name}")

        except Exception as e:
            print(f"❌ Error processing {file_name}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ImageDocTransparent Auto Watcher")
    parser.add_argument('--watch', default=os.getenv("WATCH_FOLDER", "watch"), help="Folder to watch for new images")
    parser.add_argument('--completed', default=os.getenv("COMPLETED_FOLDER", "completed"), help="Folder to save processed images")
    parser.add_argument('--originals', default=os.getenv("ORIGINALS_FOLDER", "processed_originals"), help="Folder to archive original images")
    parser.add_argument('--white-threshold', type=int, default=int(os.getenv("WHITE_THRESHOLD", 225)), help="White threshold for transparency")
    parser.add_argument('--black-threshold', type=int, default=int(os.getenv("BLACK_THRESHOLD", 150)), help="Black threshold for sharpening")
    parser.add_argument('--sleep', type=float, default=float(os.getenv("SLEEP_BEFORE_PROCESS", 1.0)), help="Seconds to wait before processing a new file")
    
    args = parser.parse_args()

    os.makedirs(args.completed, exist_ok=True)
    os.makedirs(args.originals, exist_ok=True)
    os.makedirs(args.watch, exist_ok=True)

    # Process existing files first
    scan_existing_files(args.watch, args.completed, args.originals, args.white_threshold, args.black_threshold)

    print(f"👀 Watching folder: {args.watch}")
    print(f"⚙️  Settings: White={args.white_threshold}, Black={args.black_threshold}, Sleep={args.sleep}s")
    
    observer = Observer()
    event_handler = Watcher(args.watch, args.completed, args.originals, args.white_threshold, args.black_threshold, args.sleep)
    observer.schedule(event_handler, args.watch, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
