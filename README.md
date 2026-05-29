# ImageDocTransparent

A dual-purpose utility for automated image transparency processing and text cleaning. This project provides both a user-friendly web interface and a background service for batch processing.

## 🌟 Features

### 1. Image Transparency Processor
- **Web Interface:** Upload PNG/JPG/JPEG files to automatically remove white/near-white backgrounds.
- **Auto Watcher:** Monitors a specific folder and automatically processes any images dropped into it.
- **Contrast Enhancement:** Automatically sharpens black details to ensure high-quality, crisp results for scanned documents or line art.

### 2. Text Cleaner
- Removes non-ASCII characters and artifacts from pasted text.
- Supports "Single Line Mode" for flattening text or "Standard Mode" for preserving structure while cleaning whitespace.

## 🛠️ Project Structure

- `web_app.py`: Flask-based web application.
- `auto_transparent.py`: Background service using `watchdog` to monitor and process images.
- `processor.py`: Core logic for image manipulation.
- `templates/`: HTML templates for the web interface.
- `docker-compose.yml`: Orchestration for running both the web app and watcher simultaneously.

## 🚀 Getting Started

### Using Docker (Recommended)

1. **Build and Start:**
   ```bash
   docker-compose up -d --build
   ```

2. **Access the Web App:**
   Open your browser and go to `http://localhost:5000`.

3. **Use the Auto Watcher:**
   Drop images into the directory mapped to `/watch` (configured in `docker-compose.yml`). The processed files will appear in `/completed`, and the originals will be moved to `/processed_originals`.

### Local Installation

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Web App:**
   ```bash
   python web_app.py --port 5000 --white-threshold 225
   ```

3. **Run the Auto Watcher:**
   ```bash
   python auto_transparent.py --watch my_watch_folder --completed my_output_folder
   ```

## ⚙️ Configuration

You can configure the application using either **Environment Variables** or **Command Line Arguments**.

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `5000` | Port for the web application. |
| `WHITE_THRESHOLD` | `225` | Pixels brighter than this become transparent (0-255). |
| `BLACK_THRESHOLD` | `150` | Pixels darker than this are sharpened to pure black. |
| `WATCH_FOLDER` | `watch` | Directory for the auto-watcher to monitor. |
| `COMPLETED_FOLDER` | `completed` | Directory where processed images are saved. |
| `ORIGINALS_FOLDER` | `processed_originals` | Directory where original files are archived. |
| `SLEEP_BEFORE_PROCESS`| `1.0` | Delay in seconds before processing a new file. |

### Command Line Arguments

#### `web_app.py`
- `--port`: Port to run the server on.
- `--host`: Host to bind to.
- `--white-threshold`: White threshold for transparency.
- `--black-threshold`: Black threshold for sharpening.

#### `auto_transparent.py`
- `--watch`: Folder to watch for new images.
- `--completed`: Folder to save processed images.
- `--originals`: Folder to archive original images.
- `--white-threshold`: White threshold for transparency.
- `--black-threshold`: Black threshold for sharpening.
- `--sleep`: Seconds to wait before processing a new file.

## 🧹 Maintenance

This directory has been cleaned of unused FastAPI prototypes (`main.py`, `main_app.py`) and redundant templates to maintain a lean codebase.
