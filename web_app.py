import os
import io
from flask import Flask, render_template, request, send_file
from PIL import Image
from processor import process_image_data

app = Flask(__name__)

# Config from environment
WHITE_THRESHOLD = int(os.getenv("WHITE_THRESHOLD", 225))
BLACK_THRESHOLD = int(os.getenv("BLACK_THRESHOLD", 150))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    try:
        # Load image
        img = Image.open(file.stream)
        
        # Process image
        processed_img = process_image_data(img, WHITE_THRESHOLD, BLACK_THRESHOLD)
        
        # Save to memory
        img_io = io.BytesIO()
        processed_img.save(img_io, 'PNG')
        img_io.seek(0)
        
        # Set output filename
        base_name = os.path.splitext(file.filename)[0]
        output_filename = f"{base_name}_transparent.png"
        
        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name=output_filename)

    except Exception as e:
        return f"Error processing image: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
