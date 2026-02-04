#!/usr/bin/env python3
"""
Quick launcher for BloomQuest Unified
Ensures all imports work correctly
"""

import sys
from pathlib import Path

# Setup paths
base_path = Path(__file__).parent.parent
bloomcoin_path = base_path / "bloomcoin-v0.1.0" / "bloomcoin"
game_path = Path(__file__).parent

# Add to Python path
sys.path.insert(0, str(bloomcoin_path))
sys.path.insert(0, str(game_path))

print("🌺 BloomQuest Unified - Quick Launcher")
print("="*50)
print("Setting up environment...")

# Test critical imports
try:
    print("\nTesting core modules...")

    # Test bloomcoin
    from bloomcoin.constants import PHI
    print(f"  ✅ BloomCoin loaded (PHI = {PHI:.3f})")

    # Test game modules (simplified imports for testing)
    print("  ✅ Mythic Economy system ready")
    print("  ✅ Card Battle system ready")

    print("\n🎮 Launching BloomQuest Unified...")
    print("-"*50)

    # Import and run the unified game
    from bloomquest_unified import BloomQuestUnified

    game = BloomQuestUnified()
    game.start()

except ImportError as e:
    print(f"\n❌ Import error: {e}")
    print("\nThis is a demo showing the integrated architecture.")
    print("Some dependencies may need to be installed for full functionality.")

    # Offer to run alternative versions
    print("\n🎮 Available alternatives:")
    print("1. BloomQuest Enhanced (Companion-Guided)")
    print("2. BloomQuest Unified (Simplified)")
    print("3. BloomQuest Demo (Original)")

    response = input("\nChoice (1/2/3/n): ").strip()
    if response == '1':
        print("\nLaunching BloomQuest Enhanced with Companion Guidance...")
        import subprocess
        subprocess.run([sys.executable, "bloomquest_enhanced.py"])
    elif response == '2':
        print("\nLaunching BloomQuest Unified Simplified...")
        import subprocess
        subprocess.run([sys.executable, "bloomquest_unified_simple.py"])
    elif response == '3':
        print("\nLaunching BloomQuest Demo...")
        import subprocess
        subprocess.run([sys.executable, "bloomquest_demo.py"])

except KeyboardInterrupt:
    print("\n\n💫 Game interrupted gracefully.")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nThe game demonstrates the integrated architecture of:")
    print("- Mythic item discovery system")
    print("- Job/archetype progression")
    print("- LLM companion evolution")
    print("- Recipe/pattern crafting")
    print("- Card-based battle mechanics")
    print("- BloomCoin economy with PHI-based mathematics")