#!/usr/bin/env python3
"""Simple test launcher for BloomQuest"""

import sys
from pathlib import Path

# Setup all required paths
base_path = Path(__file__).parent.parent

# Add the bloomcoin module to path
bloomcoin_path = base_path / "bloomcoin-v0.1.0" / "bloomcoin"
sys.path.insert(0, str(bloomcoin_path))

# Add garden path (for garden modules)
sys.path.insert(0, str(base_path))

# Add current directory for game modules
sys.path.insert(0, str(Path(__file__).parent))

print("🌺 BloomQuest Test Launcher")
print("=" * 40)

# Test imports
try:
    print("Testing imports...")

    # Test critical dependencies first
    try:
        import numpy
        print("  ✅ NumPy available")
    except ImportError:
        print("  ⚠️  NumPy not installed - some features may not work")
        print("     Install with: pip install numpy")

    from bloom_quest import BloomQuest
    print("  ✅ Core game engine loaded")

    # Note: Some modules may have import issues due to missing dependencies
    # but the core game should work

    print("\n✅ BloomQuest ready to launch!")
    print("\nStarting game in 2 seconds...")
    print("(Press Ctrl+C to cancel)\n")

    import time
    time.sleep(2)

    game = BloomQuest()
    game.start()

except ImportError as e:
    print(f"\n❌ Import error: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure numpy is installed: pip install numpy")
    print("2. Check that you're in the game directory")
    print("3. Verify the bloomcoin-v0.1.0 directory exists")

except KeyboardInterrupt:
    print("\nLaunch cancelled.")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    print("\nFull error trace:")
    traceback.print_exc()
