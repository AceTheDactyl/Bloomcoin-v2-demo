#!/bin/bash
# Install required dependencies for BloomQuest

echo "Installing BloomQuest dependencies..."

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 not found. Installing pip..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

# Install Flask and extensions for web UI
echo "Installing Flask and SocketIO..."
pip3 install flask flask-socketio

# Optional: Install additional helpful packages
echo "Installing optional packages..."
pip3 install colorama  # For better cross-platform color support

echo "✅ Dependencies installed successfully!"
echo ""
echo "You can now run BloomQuest with:"
echo "  python3 bloomquest_launcher.py"