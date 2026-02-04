#!/usr/bin/env python3
"""
Fix import paths for the game modules
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(filepath):
    """Fix import statements in a single file"""
    with open(filepath, 'r') as f:
        content = f.read()

    # Fix the import paths
    replacements = [
        # Fix bloomcoin imports
        (r'from bloomcoin_v0_1_0\.bloomcoin\.bloomcoin\.',
         'from bloomcoin.'),
        (r'from bloomcoin_v0_1_0\.bloomcoin\.',
         'from '),

        # Update sys.path additions
        (r"sys\.path\.append\(str\(Path\(__file__\)\.parent\.parent\)\)",
         'sys.path.append(str(Path(__file__).parent.parent / "bloomcoin-v0.1.0" / "bloomcoin"))'),
    ]

    modified = False
    for pattern, replacement in replacements:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            modified = True
            content = new_content

    if modified:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✅ Fixed imports in {filepath.name}")
        return True
    return False

def main():
    """Fix imports in all game files"""
    game_dir = Path(__file__).parent

    # Files to fix
    game_files = [
        'bloom_quest.py',
        'narrative_generator.py',
        'learning_ai.py',
        'blockchain_integration.py',
        'launch_bloomquest.py'
    ]

    print("Fixing import paths...")
    print("-" * 40)

    fixed_count = 0
    for filename in game_files:
        filepath = game_dir / filename
        if filepath.exists():
            if fix_imports_in_file(filepath):
                fixed_count += 1
        else:
            print(f"⚠️  File not found: {filename}")

    print("-" * 40)
    print(f"Fixed {fixed_count} files")

    # Create a simple test launcher
    test_launcher = game_dir / "test_launch.py"
    with open(test_launcher, 'w') as f:
        f.write('''#!/usr/bin/env python3
"""Simple test launcher for BloomQuest"""

import sys
from pathlib import Path

# Add the bloomcoin module to path
bloomcoin_path = Path(__file__).parent.parent / "bloomcoin-v0.1.0" / "bloomcoin"
sys.path.insert(0, str(bloomcoin_path))

# Add garden path
garden_path = Path(__file__).parent.parent
sys.path.insert(0, str(garden_path))

# Try to import and run
try:
    from bloom_quest import BloomQuest
    print("✅ BloomQuest loaded successfully!")
    print("Starting game...")
    print()

    game = BloomQuest()
    game.start()
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all dependencies are installed")
except Exception as e:
    print(f"❌ Error: {e}")
''')

    os.chmod(test_launcher, 0o755)
    print(f"\n✅ Created test launcher: test_launch.py")
    print("\nTo start the game, run:")
    print("  python3 test_launch.py")

if __name__ == "__main__":
    main()