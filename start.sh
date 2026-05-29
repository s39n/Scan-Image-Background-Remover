#!/bin/bash

# This script starts both the auto-watcher and the web app.
# Environment variables are still the primary way to configure these,
# but you can now also pass command line arguments if running manually.

echo "🚀 Starting ImageDocTransparent Services..."

# Start the auto-watcher in the background
python auto_transparent.py "$@" &

# Start the web app in the foreground
python web_app.py "$@"
