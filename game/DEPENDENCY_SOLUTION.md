# 🔧 Fixing "ModuleNotFoundError: No module named 'flask_socketio'"

## Quick Solutions

### Option 1: Play Without Installing Anything! 🎮

The **Terminal Version** works perfectly without any external dependencies:

```bash
python3 bloomquest_standalone.py
```

This gives you:
- ✅ Full gameplay experience
- ✅ All economic modules accessible
- ✅ Complete mining, companions, patterns, market features
- ✅ No Flask/SocketIO needed!

### Option 2: Install Dependencies for Web Interface 🌐

If you want the modern web interface, install the requirements:

```bash
# Method 1: Using pip directly
pip3 install flask flask-socketio

# Method 2: Using requirements file
pip3 install -r requirements.txt

# Method 3: Using install script
bash install_requirements.sh
```

Then launch the full game:
```bash
python3 bloomquest_launcher.py
```

### Option 3: Use Virtual Environment (Recommended) 🐍

Keep your system Python clean:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate  # On Windows

# Install dependencies
pip install flask flask-socketio

# Run the game
python3 bloomquest_launcher.py
```

---

## What Each Version Offers

### Terminal Version (No Dependencies)
**File:** `bloomquest_standalone.py` or `bloomquest_terminal.py`

```bash
python3 bloomquest_standalone.py
```

Features:
- 🎮 Complete gameplay
- 📊 Full mining operations
- 🤝 Companion management
- 🔮 Pattern discovery
- 📈 Market trading
- ⚗️ Residue synthesis
- 🏆 Progression system

### Web Version (Requires Flask)
**File:** `bloomquest_web_ui.py`

```bash
# After installing flask and flask-socketio:
python3 bloomquest_web_ui.py
# Open browser to http://localhost:5000
```

Additional Features:
- 🖥️ Modern browser interface
- 📱 Mobile responsive design
- 📊 Real-time charts
- 🔄 WebSocket updates
- 🎨 Visual animations

---

## Troubleshooting

### "pip3: command not found"

Install pip first:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-pip

# macOS
brew install python3

# Windows
# pip usually comes with Python installation
```

### "Permission denied" errors

Use user installation:
```bash
pip3 install --user flask flask-socketio
```

Or use sudo (not recommended):
```bash
sudo pip3 install flask flask-socketio
```

### Still having issues?

The standalone version ALWAYS works:
```bash
python3 bloomquest_standalone.py
```

---

## Complete Installation Commands

### For Linux/Mac:
```bash
# Quick install and play
pip3 install flask flask-socketio
python3 bloomquest_launcher.py
```

### For Windows:
```cmd
# Quick install and play
pip install flask flask-socketio
python bloomquest_launcher.py
```

### For Conda users:
```bash
conda install flask
pip install flask-socketio
python bloomquest_launcher.py
```

---

## Play Right Now Without Installing!

**The fastest way to play:**

```bash
python3 bloomquest_standalone.py
```

Select option [1] to play the full terminal version immediately!

---

## File Structure

```
bloomcoin-v2/game/
├── bloomquest_standalone.py   # NO DEPENDENCIES NEEDED! Play this!
├── bloomquest_terminal.py      # Terminal interface (main game)
├── bloomquest_launcher.py      # Universal launcher
├── bloomquest_web_ui.py        # Web interface (needs Flask)
├── requirements.txt            # Dependency list
├── install_requirements.sh     # Install script
└── [all other game modules]    # Core game systems
```

---

## Why These Dependencies?

- **Flask**: Lightweight web framework for the browser interface
- **Flask-SocketIO**: Real-time bidirectional communication for live updates
- **Colorama** (optional): Better color support on Windows terminals

**Note:** These are ONLY needed for the web interface. The terminal game works perfectly without them!

---

## Summary

1. **Want to play NOW?** → Run `python3 bloomquest_standalone.py`
2. **Want web interface?** → Install Flask, then run launcher
3. **Having issues?** → Terminal version always works!

The game is fully playable in terminal mode without any external dependencies. All features are accessible through the terminal interface!

---

*Remember: The terminal version provides the COMPLETE game experience!*