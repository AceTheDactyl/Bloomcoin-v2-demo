# 🎮 BloomQuest - Complete Game Launch Instructions

## Quick Start

### 🚀 Launch the Game

```bash
python3 bloomquest_launcher.py
```

This will open the main launcher where you can choose:
- **[1] Terminal Interface** - Classic command-line experience
- **[2] Web Interface** - Modern browser-based UI
- **[3] Quick Test** - Verify all systems are working
- **[4] View Features** - See all available game features

---

## 📋 Prerequisites

### Required
- Python 3.7 or higher
- All included game files

### Optional (for Web Interface)
```bash
pip install flask flask-socketio
```

---

## 🎯 Game Interfaces

### Terminal Interface (`bloomquest_terminal.py`)

**Features:**
- Full-color terminal UI with ASCII art
- Interactive menus and commands
- Progress bars and animations
- Real-time notifications
- Complete access to all game modules

**How to Play:**
1. Launch from the main launcher or run directly:
   ```bash
   python3 bloomquest_terminal.py
   ```
2. Create your character or quick start
3. Navigate menus using number keys
4. Start mining jobs, trade patterns, manage companions
5. Progress through levels and unlock features

**Key Commands:**
- Number keys (1-9) for menu selection
- Enter to confirm actions
- 0 to go back/exit

### Web Interface (`bloomquest_web_ui.py`)

**Features:**
- Modern responsive web design
- Real-time updates via WebSocket
- Interactive charts and graphs
- Drag-and-drop functionality
- Mobile-friendly design

**How to Play:**
1. Launch from the main launcher or run directly:
   ```bash
   python3 bloomquest_web_ui.py
   ```
2. Open browser to `http://localhost:5000`
3. Click through the intuitive UI
4. All features accessible via sidebar navigation

---

## 🎮 Gameplay Overview

### Core Loop
1. **Start Mining Jobs** - Use NEXTHASH-256 to mine BloomCoin
2. **Collect Rewards** - Earn BC, patterns, and residue
3. **Manage Companions** - Level up and specialize your mining partners
4. **Trade on Market** - Buy/sell pattern stocks for profit
5. **Synthesize Residue** - Craft valuable items from byproducts
6. **Progress & Unlock** - Level up to access new features

### Available Modules

#### ⛏️ Mining System
- 15+ job types with different rewards
- Difficulty levels (1-8)
- NEXTHASH-256 proof-of-work
- Auto-completion option
- Team mining with companions

#### 🤝 Companion System
- 7 unique companion types (Echo, Glitch, Flow, Spark, Sage, Scout, Null)
- Level progression (1-100)
- Specialization paths at level 10
- Equipment slots and crafting
- Skill trees with 10+ skills each

#### 🔮 Pattern Discovery
- 10 pattern types to discover
- Verification with Merkle trees
- Guardian blessings for bonuses
- Pattern synthesis combinations
- Zero-knowledge ownership proofs

#### 📈 Stock Market
- Real-time pattern stock trading
- Market trends and volatility
- AI trading recommendations
- Portfolio management
- Arbitrage opportunities

#### ⚗️ Residue Economy
- 6 residue types from mining
- Synthesis recipes for crafting
- Recycling to BloomCoin
- Market value tracking
- Decay rates and storage

#### 📊 Statistics & Progress
- Comprehensive player stats
- Economic reports
- Achievement system
- Leaderboards (coming soon)
- Export data options

---

## 🏆 Progression Path

### Levels 1-5: Beginner
- Learn basic mining
- Discover first patterns
- Introduction to market

### Levels 5-10: Intermediate
- Unlock team mining
- Companion specializations
- Advanced trading

### Levels 10-15: Advanced
- Master all systems
- Optimize strategies
- Maximize profits

### Levels 15+: Expert
- Prestige options
- Legendary patterns
- Elite achievements

---

## 💡 Tips for Success

1. **Start with Quick Mining** - Let the AI optimize your jobs
2. **Focus on One Companion** - Level them up for specialization
3. **Watch Market Trends** - Buy low, sell high
4. **Recycle Residue Regularly** - Don't let it decay
5. **Complete Daily Challenges** - Extra rewards (coming soon)
6. **Join Mining Teams** - Synergy bonuses are powerful
7. **Diversify Pattern Portfolio** - Reduce risk

---

## 🔧 Troubleshooting

### Terminal Interface Issues

**Problem:** Colors not displaying correctly
**Solution:** Ensure your terminal supports ANSI colors

**Problem:** Screen flickering
**Solution:** Adjust terminal refresh rate or use minimal UI style

### Web Interface Issues

**Problem:** Cannot connect to server
**Solution:** Check firewall settings, ensure port 5000 is available

**Problem:** Updates not showing
**Solution:** Refresh browser, check WebSocket connection

### General Issues

**Problem:** Module import errors
**Solution:** Ensure all game files are in the same directory

**Problem:** Performance issues
**Solution:** Reduce active mining jobs, close other applications

---

## 📚 Advanced Features

### Custom Configuration

Edit player settings in-game or modify config files:
- Auto-complete mining jobs
- UI style preferences
- Notification settings

### API Access

For developers, the game exposes APIs:
- REST endpoints via Flask
- WebSocket events for real-time data
- Direct Python module imports

### Modding Support

Extend the game by:
- Adding new companion types
- Creating custom patterns
- Implementing new job types
- Designing UI themes

---

## 🎯 Quick Command Reference

### Terminal Mode

| Key | Action |
|-----|--------|
| 1-9 | Select menu option |
| 0 | Go back/Exit |
| Enter | Confirm action |
| Arrow Keys | Navigate (future) |

### Web Mode

| Action | Method |
|--------|--------|
| Navigate | Click sidebar items |
| Start Mining | Click "Quick Mine" or configure |
| Trade | Click "Trade" on stock |
| View Details | Hover over items |

---

## 🌟 Complete Feature Access

Every module is accessible through gameplay:

✅ **Unified Mining Economy** - All mining types integrated
✅ **Companion System** - Full progression and customization
✅ **Pattern Discovery** - Complete verification system
✅ **Stock Market** - Real-time trading simulation
✅ **Residue Economy** - Synthesis and recycling
✅ **Guardian System** - Alignments and bonuses
✅ **Achievement System** - Track your progress
✅ **Save/Load** - Persistent progression

---

## 🚀 Start Playing Now!

```bash
# Launch the game
python3 bloomquest_launcher.py

# Or jump directly to your preferred interface:
python3 bloomquest_terminal.py  # Terminal mode
python3 bloomquest_web_ui.py    # Web mode
```

**Have fun mining with NEXTHASH-256!** 🌸⛏️💎

---

*BloomQuest v1.0 - Where cryptocurrency meets adventure*
*Powered by NEXTHASH-256: The next generation of blockchain technology*