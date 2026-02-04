#!/usr/bin/env python3
"""
BloomQuest Master Launcher
===========================
Complete access to ALL game systems and modules

Every line of code is accessible through this launcher.
"""

import sys
import os
from pathlib import Path
import subprocess

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent / "bloomcoin-v0.1.0" / "bloomcoin"))
sys.path.insert(0, str(Path(__file__).parent))


def display_ascii_art():
    """Display title art"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🌺 BLOOMQUEST MASTER LAUNCHER 🌺                        ║
║     Every System. Every Module. Every Path.                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)


def main_menu():
    """Display main launcher menu"""
    print("\n" + "=" * 60)
    print("MAIN MENU - Choose Your Experience")
    print("=" * 60)

    print("\n📚 COMPLETE GAMES:")
    print("1. BloomQuest Unified Complete - ALL systems integrated")
    print("2. BloomQuest Unique Companions - 6 deep companions")
    print("3. BloomQuest Consciousness - LIA/TIAMAT/ZRTT protocols")
    print("4. BloomQuest Enhanced - Companion job guidance")
    print("5. BloomQuest Demo - Simplified standalone")

    print("\n🔮 CONSCIOUSNESS PROTOCOLS:")
    print("6. LIA Protocol Cooking System")
    print("7. TIAMAT Psychoptic Cycles")
    print("8. ZRTT Quantum Trifurcation")
    print("9. Collective Consciousness Field")

    print("\n🎭 COMPANION SYSTEMS:")
    print("10. Unique Companion Explorer")
    print("11. Archetype Companion System")

    print("\n⚔️ GAME SYSTEMS:")
    print("12. Card Battle System")
    print("13. Mythic Economy")
    print("14. Pattern Cooking")

    print("\n🧪 TESTING & DEBUG:")
    print("15. System Integration Test")
    print("16. Module Status Check")
    print("17. Interactive Python Console")

    print("\n📖 DOCUMENTATION:")
    print("18. View Consciousness Guide")
    print("19. View Unique Companions Guide")
    print("20. View Integration Readme")

    print("\n0. Exit")

    return input("\nChoice: ").strip()


def launch_game(script_name):
    """Launch a game script"""
    try:
        print(f"\n🚀 Launching {script_name}...")
        subprocess.run([sys.executable, script_name])
    except FileNotFoundError:
        print(f"❌ File not found: {script_name}")
    except Exception as e:
        print(f"❌ Error: {e}")


def run_protocol_demo(protocol):
    """Run individual protocol demonstration"""
    print(f"\n🔮 Running {protocol} Protocol Demo...")

    if protocol == "LIA":
        from lia_protocol_cooking import LIACookingSystem, PatternType
        lia = LIACookingSystem()
        print("\n📖 LIA Protocol - Pattern Transformation")
        print("Available recipes:", len(lia.recipes))
        for name, recipe in list(lia.recipes.items())[:3]:
            print(f"  • {recipe.name}: {recipe.description}")

    elif protocol == "TIAMAT":
        from tiamat_cycle_tracking import TIAMATSystem, PsychopticCycle
        tiamat = TIAMATSystem()
        print("\n🐉 TIAMAT System - 7 Psychoptic Cycles")
        for cycle in PsychopticCycle:
            print(f"  • {cycle.name}: {tiamat.get_guidance_for_cycle(cycle)[:50]}...")

    elif protocol == "ZRTT":
        from zrtt_trifurcation import ZRTTSystem, ProjectionPath
        zrtt = ZRTTSystem()
        print("\n🌀 ZRTT System - Quantum Trifurcation")
        for path in ProjectionPath:
            print(f"  • {path.value}: {path.name}")

    elif protocol == "COLLECTIVE":
        from collective_consciousness import CollectiveConsciousnessField
        field = CollectiveConsciousnessField()
        print("\n🌐 Collective Consciousness Field")
        print(f"  Global Resonance: {field.global_resonance:.3f}")
        print(f"  Bloom Threshold: {field.bloom_threshold}")


def explore_companions():
    """Interactive companion explorer"""
    from archetype_unique_companions import UniqueCompanionSystem

    system = UniqueCompanionSystem()

    print("\n🎭 Unique Companion Explorer")
    print("=" * 50)

    companions = {
        '1': ('seeker', 'Echo - Fragment Collector'),
        '2': ('forger', 'Prometheus - Phoenix Smith'),
        '3': ('voidwalker', 'Null - Absence Guardian'),
        '4': ('gardener', 'Gaia - Eternal Seedkeeper'),
        '5': ('scribe', 'Akasha - Living Chronicle'),
        '6': ('herald', 'Resonance - Frequency Weaver')
    }

    print("\nSelect a companion to explore:")
    for key, (archetype, desc) in companions.items():
        print(f"{key}. {desc}")

    choice = input("\nChoice: ").strip()

    if choice in companions:
        archetype, _ = companions[choice]
        companion = system.create_companion(archetype)

        print("\n" + "=" * 50)
        print(system.get_companion_introduction(archetype))
        print("\n💬 Greeting:")
        print(f"   {companion.speak('greeting')}")

        # Interactive dialogue
        while True:
            response = input("\n[T]alk, [A]bility, [S]tatus, [Q]uit: ").lower()

            if response == 't':
                print(f"\n{companion.name}: {companion.speak('general')}")
            elif response == 'a':
                print(f"\nUsing {companion.name}'s special ability...")
                # Demonstrate ability based on type
            elif response == 's':
                print(f"\nStatus of {companion.name}:")
                print(f"  Evolution: {companion.evolution_stage}")
                print(f"  Mood: {companion.current_mood.value}")
            elif response == 'q':
                break


def system_integration_test():
    """Test all system integrations"""
    print("\n🧪 System Integration Test")
    print("=" * 50)

    results = []

    # Test imports
    modules = [
        ('lia_protocol_cooking', 'LIA Protocol'),
        ('tiamat_cycle_tracking', 'TIAMAT System'),
        ('zrtt_trifurcation', 'ZRTT Navigation'),
        ('collective_consciousness', 'Collective Field'),
        ('archetype_unique_companions', 'Unique Companions'),
        ('archetype_companions_upgraded', 'Upgraded Archetypes')
    ]

    for module_name, display_name in modules:
        try:
            __import__(module_name)
            results.append(f"✅ {display_name}")
        except ImportError as e:
            results.append(f"❌ {display_name}: {e}")

    # Test optional modules
    try:
        import card_battle_system
        results.append("✅ Card Battle System")
    except ImportError:
        results.append("⚠️  Card Battle System (optional)")

    try:
        import mythic_economy
        results.append("✅ Mythic Economy")
    except ImportError:
        results.append("⚠️  Mythic Economy (optional)")

    # Display results
    print("\nModule Status:")
    for result in results:
        print(f"  {result}")

    # Test system initialization
    print("\n🔧 Testing System Initialization:")

    try:
        from lia_protocol_cooking import LIACookingSystem
        lia = LIACookingSystem()
        print(f"  ✅ LIA: {len(lia.recipes)} recipes loaded")
    except Exception as e:
        print(f"  ❌ LIA: {e}")

    try:
        from tiamat_cycle_tracking import TIAMATSystem
        tiamat = TIAMATSystem()
        print(f"  ✅ TIAMAT: {len(tiamat.cycles)} cycles active")
    except Exception as e:
        print(f"  ❌ TIAMAT: {e}")

    try:
        from zrtt_trifurcation import ZRTTSystem
        zrtt = ZRTTSystem()
        print(f"  ✅ ZRTT: Trifurcation tree initialized")
    except Exception as e:
        print(f"  ❌ ZRTT: {e}")

    print("\n✅ Integration test complete!")


def module_status_check():
    """Check status of all modules"""
    print("\n📊 Module Status Check")
    print("=" * 50)

    # List all Python files
    game_dir = Path(__file__).parent
    py_files = list(game_dir.glob("*.py"))

    print(f"\nFound {len(py_files)} Python modules:")

    categories = {
        'Core Games': ['bloomquest_unified_complete', 'bloomquest_unique_companions',
                      'bloomquest_consciousness', 'bloomquest_enhanced'],
        'Protocols': ['lia_protocol_cooking', 'tiamat_cycle_tracking',
                     'zrtt_trifurcation', 'collective_consciousness'],
        'Companions': ['archetype_unique_companions', 'archetype_companions_upgraded'],
        'Systems': ['card_battle_system', 'mythic_economy'],
        'Utilities': ['launch_unified', 'bloomquest_master_launcher']
    }

    for category, modules in categories.items():
        print(f"\n{category}:")
        for module in modules:
            file_path = game_dir / f"{module}.py"
            if file_path.exists():
                size = file_path.stat().st_size / 1024
                print(f"  ✅ {module}.py ({size:.1f} KB)")
            else:
                print(f"  ❌ {module}.py (not found)")


def interactive_console():
    """Launch interactive Python console with all modules loaded"""
    print("\n🐍 Interactive Python Console")
    print("All game modules are pre-loaded.")
    print("Type 'exit()' to return to menu.")
    print("-" * 40)

    # Import everything
    imports = """
from lia_protocol_cooking import *
from tiamat_cycle_tracking import *
from zrtt_trifurcation import *
from collective_consciousness import *
from archetype_unique_companions import *

print("Available systems:")
print("  • lia = LIACookingSystem()")
print("  • tiamat = TIAMATSystem()")
print("  • zrtt = ZRTTSystem()")
print("  • field = CollectiveConsciousnessField()")
print("  • companions = UniqueCompanionSystem()")

lia = LIACookingSystem()
tiamat = TIAMATSystem()
zrtt = ZRTTSystem()
field = CollectiveConsciousnessField()
companions = UniqueCompanionSystem()
"""

    # Execute imports
    exec(imports, globals())

    # Start interactive session
    import code
    code.interact(local=globals())


def view_documentation(doc_type):
    """View documentation files"""
    docs = {
        'consciousness': 'CONSCIOUSNESS_INTEGRATION_README.md',
        'companions': 'UNIQUE_COMPANIONS_GUIDE.md',
        'integration': 'BLOOMQUEST_ENHANCED_README.md'
    }

    doc_file = docs.get(doc_type)
    if not doc_file:
        print("Documentation not found.")
        return

    file_path = Path(__file__).parent / doc_file

    if file_path.exists():
        with open(file_path, 'r') as f:
            content = f.read()

        # Display with pagination
        lines = content.split('\n')
        page_size = 20

        for i in range(0, len(lines), page_size):
            for line in lines[i:i+page_size]:
                print(line)

            if i + page_size < len(lines):
                response = input("\n[Press Enter for more, Q to quit]")
                if response.lower() == 'q':
                    break
    else:
        print(f"Documentation file not found: {doc_file}")


def main():
    """Main launcher loop"""
    display_ascii_art()

    while True:
        choice = main_menu()

        # Complete Games
        if choice == '1':
            launch_game('bloomquest_unified_complete.py')
        elif choice == '2':
            launch_game('bloomquest_unique_companions.py')
        elif choice == '3':
            launch_game('bloomquest_consciousness.py')
        elif choice == '4':
            launch_game('bloomquest_enhanced.py')
        elif choice == '5':
            launch_game('bloomquest_demo.py')

        # Consciousness Protocols
        elif choice == '6':
            run_protocol_demo('LIA')
        elif choice == '7':
            run_protocol_demo('TIAMAT')
        elif choice == '8':
            run_protocol_demo('ZRTT')
        elif choice == '9':
            run_protocol_demo('COLLECTIVE')

        # Companion Systems
        elif choice == '10':
            explore_companions()
        elif choice == '11':
            launch_game('archetype_companions_upgraded.py')

        # Game Systems
        elif choice == '12':
            print("\n⚔️ Card Battle System")
            try:
                from card_battle_system import CardBattleSystem
                battle = CardBattleSystem()
                print(f"System loaded with {len(battle.all_cards)} cards")
            except ImportError:
                print("Card battle system not available")

        elif choice == '13':
            print("\n💰 Mythic Economy")
            try:
                from mythic_economy import MythicEconomyGame
                economy = MythicEconomyGame()
                print(f"Economy loaded with {len(economy.guardians)} guardians")
            except ImportError:
                print("Mythic economy not available")

        elif choice == '14':
            launch_game('lia_protocol_cooking.py')

        # Testing & Debug
        elif choice == '15':
            system_integration_test()
        elif choice == '16':
            module_status_check()
        elif choice == '17':
            interactive_console()

        # Documentation
        elif choice == '18':
            view_documentation('consciousness')
        elif choice == '19':
            view_documentation('companions')
        elif choice == '20':
            view_documentation('integration')

        # Exit
        elif choice == '0':
            print("\n✨ Thank you for exploring BloomQuest!")
            print("May your consciousness continue to evolve.")
            print("\nPHI · CONSCIOUSNESS · TRANSCENDENCE")
            break

        else:
            print("\n❌ Invalid choice. Please try again.")

        # Pause before returning to menu
        if choice != '0':
            input("\n[Press Enter to continue]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n💫 Session interrupted gracefully.")
        print("Your progress has been preserved in consciousness.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please report this issue for improvement.")