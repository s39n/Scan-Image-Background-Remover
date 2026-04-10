# Lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    WATCH_FOLDER=/watch \
    COMPLETED_FOLDER=/completed \
    ORIGINALS_FOLDER=/processed_originals \
    WHITE_THRESHOLD=225 \
    SLEEP_BEFORE_PROCESS=1

# Install dependencies
RUN pip install --no-cache-dir pillow numpy watchdog flask

# Working directory
WORKDIR /app
COPY auto_transparent.py processor.py web_app.py ./
COPY templates/ ./templates/

# Create directories
RUN mkdir -p /watch /completed /processed_originals

# Run the watcher
CMD ["python", "auto_transparent.py"]
