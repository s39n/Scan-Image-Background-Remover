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

1. **Configure Settings:** 
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` to set your desired `APP_PORT` and host folder paths (`WATCH_DIR`, etc.).

2. **Build and Start:**
   ```bash
   docker-compose up -d --build
   ```

3. **Access the Web App:**
   Open your browser and go to `http://localhost:5000` (or the port you configured).

4. **Use the Auto Watcher:**
   Drop images into your configured watch directory. The processed files will appear in the completed directory.

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

You can configure the application using either a **.env file**, **Environment Variables**, or **Command Line Arguments**.

### Environment Variables (.env)

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_PORT` | `5000` | Host port for the web application (Docker only). |
| `WATCH_DIR` | `./watch` | Host directory to monitor (Docker only). |
| `COMPLETED_DIR` | `./completed` | Host directory for results (Docker only). |
| `ORIGINALS_DIR` | `./processed_originals` | Host directory for archives (Docker only). |
| `WHITE_THRESHOLD` | `225` | Pixels brighter than this become transparent (0-255). |
| `BLACK_THRESHOLD` | `150` | Pixels darker than this are sharpened to pure black. |
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
