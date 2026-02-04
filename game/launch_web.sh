#!/bin/bash
# Launch BloomQuest Web UI

echo "🚀 Starting BloomQuest Web UI..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Start the web server (using working version)
python bloomquest_web_working.py

echo ""
echo "Web UI stopped."