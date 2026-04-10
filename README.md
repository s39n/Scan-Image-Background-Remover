# Image Background Remover & Enhancer (Dual-Mode)

A dual-mode Python application that makes image backgrounds transparent and enhances black contrast (perfect for sheet music, sketches, or text).

## 🚀 Features
- **Mode 1: Folder Watcher** - Automatically processes any image dropped into a specific folder.
- **Mode 2: Web App** - Drag and drop images into your browser for instant processing and download.
- **Smart Transparency** - Automatically removes near-white backgrounds.
- **Contrast Boost** - Forces dark/gray pixels to pure black to make details "stand out."
- **No Zipping** - Delivers individual PNG files directly.

## 🛠️ Installation & Setup

### Using Docker (Recommended)
1.  **Configure Volumes:** Open `docker-compose.yml` and update the volume paths to match your local folders (e.g., replace `/volume1/Docker/app/` with your actual path).
2.  **Run the App:**
    ```bash
    docker-compose up -d --build
    ```
3.  **Access the Web App:** Go to `http://localhost:5000` in your browser.
4.  **Use the Watcher:** Drop images into your local `/watch` folder; the results will appear in `/completed`.

### Manual Setup (Without Docker)
1.  **Install Requirements:**
    ```bash
    pip install pillow numpy watchdog flask
    ```
2.  **Run the Web App:**
    ```bash
    python web_app.py
    ```
3.  **Run the Folder Watcher:**
    ```bash
    python auto_transparent.py
    ```

## ⚙️ Configuration
You can tune the sensitivity using environment variables in `docker-compose.yml`:

| Variable | Default | Description |
| :--- | :--- | :--- |
| `WHITE_THRESHOLD` | `230` | Higher = stricter (only pure white becomes transparent). Lower = more aggressive. |
| `BLACK_THRESHOLD` | `150` | Higher = more aggressive (makes dark grays pure black). |
| `WATCH_FOLDER` | `/watch` | The folder to monitor for new images. |
| `COMPLETED_FOLDER` | `/completed` | Where the processed PNGs are saved. |

## 📁 Project Structure
- `web_app.py`: Flask server for the browser interface.
- `auto_transparent.py`: Watchdog script for folder automation.
- `processor.py`: Core logic for transparency and contrast enhancement.
- `templates/`: HTML/JS for the web interface.
- `docker-compose.yml` & `dockerfile`: Containerization setup.

## 📄 License
MIT
