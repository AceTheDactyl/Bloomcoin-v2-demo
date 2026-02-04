#!/bin/bash
# Launch BloomQuest Web UI - WORKING VERSION

echo "🚀 Starting BloomQuest Web UI (Working Version)..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip install flask flask-socketio python-socketio[client] --quiet
fi

# Start the web server
echo "Starting server on http://localhost:5000"
echo ""
python3 bloomquest_web_working.py --port 5000

echo ""
echo "Web UI stopped."