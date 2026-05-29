import os
import io
import re
import argparse
from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image
from processor import process_image_data

app = Flask(__name__)

# Config - will be updated by main()
WHITE_THRESHOLD = 225
BLACK_THRESHOLD = 150

# --- Page Routes ---

@app.get('/')
def index():
    """Serves the unified Utility Dashboard."""
    return render_template('index.html')

# --- API Routes ---

@app.post('/api/image/process')
@app.post('/upload') # Support both for backward compatibility
def upload():
    """Handles image background removal and detail sharpening."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        img = Image.open(file.stream)
        processed_img = process_image_data(img, WHITE_THRESHOLD, BLACK_THRESHOLD)

        img_io = io.BytesIO()
        processed_img.save(img_io, 'PNG')
        img_io.seek(0)

        base_name = os.path.splitext(file.filename)[0]
        output_filename = f"{base_name}_transparent.png"

        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name=output_filename)       
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.post('/api/text/clean')
def clean_text():
    """Handles text cleaning and artifact counting."""
    text = request.form.get('text', '')
    mode = request.form.get('cleaning_mode', 'standard')

    # Artifact count: non-ASCII or 2+ spaces
    artifacts = len(re.findall(r'[^\x00-\x7F]+|\s{2,}', text))

    # Clean non-ASCII
    cleaned = re.sub(r'[^\x00-\x7F]+', '', text)

    if mode == 'one_line':
        # Replace carriage returns and newlines with a space
        cleaned = re.sub(r'[\r\n]+', ' ', cleaned)
        cleaned = " ".join(cleaned.split())
    else:
        # Standard normalization
        cleaned = re.sub(r'\r\n|\r', '\n', cleaned)
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        cleaned = re.sub(r'[ \t]+', ' ', cleaned).strip()

    return jsonify({
        "cleaned_text": cleaned,
        "artifacts_removed": artifacts
    })

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="ImageDocTransparent Web App")
    parser.add_argument('--port', type=int, default=int(os.getenv("PORT", 5000)), help="Port to run the server on")
    parser.add_argument('--host', default=os.getenv("HOST", "0.0.0.0"), help="Host to bind the server to")
    parser.add_argument('--white-threshold', type=int, default=int(os.getenv("WHITE_THRESHOLD", 225)), help="White threshold for transparency")
    parser.add_argument('--black-threshold', type=int, default=int(os.getenv("BLACK_THRESHOLD", 150)), help="Black threshold for sharpening")
    args = parser.parse_args()

    WHITE_THRESHOLD = args.white_threshold
    BLACK_THRESHOLD = args.black_threshold

    print(f"🚀 Starting Web App on {args.host}:{args.port}")
    print(f"⚙️  Thresholds: White={WHITE_THRESHOLD}, Black={BLACK_THRESHOLD}")
    
    app.run(host=args.host, port=args.port)
