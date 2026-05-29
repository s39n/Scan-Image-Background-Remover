# Lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    WATCH_FOLDER=/watch \
    COMPLETED_FOLDER=/completed \
    ORIGINALS_FOLDER=/processed_originals \
    WHITE_THRESHOLD=225 \
    BLACK_THRESHOLD=150 \
    SLEEP_BEFORE_PROCESS=1 \
    FLASK_APP=web_app.py

# Working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY auto_transparent.py processor.py web_app.py start.sh ./
COPY templates/ ./templates/

# Create directories and set permissions
RUN mkdir -p /watch /completed /processed_originals && \
    chmod +x start.sh

# Expose the Flask port
EXPOSE 5000

# Run the startup script
CMD ["./start.sh"]
