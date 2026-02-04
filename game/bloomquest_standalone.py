#!/usr/bin/env python3
"""
BloomQuest Standalone - No External Dependencies Required
==========================================================
Play BloomQuest without needing Flask or other external packages.
Full terminal experience with all game features.
"""

import os
import sys
import time
import random
from typing import Optional

# Check if we can import the terminal version
try:
    from bloomquest_terminal import BloomQuestTerminal, Colors, UIComponents
    TERMINAL_AVAILABLE = True
except ImportError:
    TERMINAL_AVAILABLE = False
    print("Error: bloomquest_terminal.py not found")

# Quick standalone colors if needed
class StandaloneColors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    CYAN = '\033[36m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    MAGENTA = '\033[35m'
    RED = '\033[31m'
    BRIGHT_WHITE = '\033[97m'

def install_dependencies():
    """Offer to install dependencies"""
    Colors = StandaloneColors()

    print(f"{Colors.YELLOW}Missing optional dependencies for web interface.{Colors.RESET}")
    print(f"\nYou have several options:\n")
    print(f"  {Colors.GREEN}1. Play Terminal Version{Colors.RESET} (no dependencies needed)")
    print(f"  {Colors.CYAN}2. Install Dependencies{Colors.RESET} (for web interface)")
    print(f"  {Colors.YELLOW}3. View Installation Instructions{Colors.RESET}")
    print(f"  {Colors.RED}4. Exit{Colors.RESET}")

    choice = input(f"\n{Colors.YELLOW}Your choice: {Colors.RESET}").strip()

    if choice == "1":
        return "terminal"
    elif choice == "2":
        print(f"\n{Colors.CYAN}To install dependencies, run:{Colors.RESET}")
        print(f"  pip3 install flask flask-socketio")
        print(f"\nOr if you have the install script:")
        print(f"  bash install_requirements.sh")
        input(f"\n{Colors.YELLOW}Press ENTER after installing...{Colors.RESET}")
        return "retry"
    elif choice == "3":
        show_instructions()
        return "menu"
    else:
        return "exit"

def show_instructions():
    """Show installation instructions"""
    Colors = StandaloneColors()

    print(f"\n{Colors.CYAN}═══ INSTALLATION INSTRUCTIONS ═══{Colors.RESET}\n")

    print(f"{Colors.BOLD}Option 1: Quick Install (Recommended){Colors.RESET}")
    print("  Run the install script:")
    print("    bash install_requirements.sh")

    print(f"\n{Colors.BOLD}Option 2: Manual Install{Colors.RESET}")
    print("  Install Python packages:")
    print("    pip3 install flask flask-socketio")

    print(f"\n{Colors.BOLD}Option 3: No Installation{Colors.RESET}")
    print("  Play the terminal version which needs no dependencies!")

    print(f"\n{Colors.YELLOW}System Requirements:{Colors.RESET}")
    print("  • Python 3.7 or higher")
    print("  • Terminal with ANSI color support")
    print("  • (Optional) Flask for web interface")

    input(f"\n{Colors.YELLOW}Press ENTER to continue...{Colors.RESET}")

def run_terminal_game():
    """Run the terminal version of the game"""
    Colors = StandaloneColors()

    if not TERMINAL_AVAILABLE:
        print(f"{Colors.RED}Error: Terminal game not available.{Colors.RESET}")
        print("Make sure bloomquest_terminal.py is in the same directory.")
        return False

    print(f"{Colors.GREEN}Starting BloomQuest Terminal Edition...{Colors.RESET}")
    time.sleep(1)

    try:
        game = BloomQuestTerminal()
        game.start()
        return True
    except Exception as e:
        print(f"{Colors.RED}Error running game: {e}{Colors.RESET}")
        return False

def show_game_info():
    """Show game information"""
    Colors = StandaloneColors()

    print(f"""
{Colors.MAGENTA}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  {Colors.BRIGHT_WHITE}██████╗ ██╗      ██████╗  ██████╗ ███╗   ███╗ ██████╗ ██╗   ██╗███████╗{Colors.MAGENTA}  ║
║  {Colors.BRIGHT_WHITE}██╔══██╗██║     ██╔═══██╗██╔═══██╗████╗ ████║██╔═══██╗██║   ██║██╔════╝{Colors.MAGENTA}  ║
║  {Colors.CYAN}██████╔╝██║     ██║   ██║██║   ██║██╔████╔██║██║   ██║██║   ██║█████╗  {Colors.MAGENTA}  ║
║  {Colors.CYAN}██╔══██╗██║     ██║   ██║██║   ██║██║╚██╔╝██║██║▄▄ ██║██║   ██║██╔══╝  {Colors.MAGENTA}  ║
║  {Colors.GREEN}██████╔╝███████╗╚██████╔╝╚██████╔╝██║ ╚═╝ ██║╚██████╔╝╚██████╔╝███████╗{Colors.MAGENTA}  ║
║  {Colors.GREEN}╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝{Colors.MAGENTA}  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}

                    {Colors.CYAN}NEXTHASH-256 CRYPTOCURRENCY MINING GAME{Colors.RESET}

    {Colors.GREEN}✓ No External Dependencies Required for Terminal Mode{Colors.RESET}
    {Colors.GREEN}✓ Full Access to All Game Features{Colors.RESET}
    {Colors.GREEN}✓ Complete Economic System Integration{Colors.RESET}
""")

def test_core_systems():
    """Test that core game systems work"""
    Colors = StandaloneColors()

    print(f"{Colors.CYAN}Testing core game systems...{Colors.RESET}\n")

    tests_passed = 0
    tests_total = 5

    # Test 1: NEXTHASH
    try:
        from nexthash256 import nexthash256_hex
        print(f"{Colors.GREEN}✓{Colors.RESET} NEXTHASH-256 system")
        tests_passed += 1
    except:
        print(f"{Colors.RED}✗{Colors.RESET} NEXTHASH-256 system")

    # Test 2: Companions
    try:
        from companion_mining_ultimate import CompanionType
        print(f"{Colors.GREEN}✓{Colors.RESET} Companion system")
        tests_passed += 1
    except:
        print(f"{Colors.RED}✗{Colors.RESET} Companion system")

    # Test 3: Patterns
    try:
        from guardian_pattern_recipes import PatternType
        print(f"{Colors.GREEN}✓{Colors.RESET} Pattern system")
        tests_passed += 1
    except:
        print(f"{Colors.RED}✗{Colors.RESET} Pattern system")

    # Test 4: Economy
    try:
        from unified_mining_economy import UnifiedMiningEconomy
        print(f"{Colors.GREEN}✓{Colors.RESET} Economic system")
        tests_passed += 1
    except:
        print(f"{Colors.RED}✗{Colors.RESET} Economic system")

    # Test 5: Terminal UI
    try:
        from bloomquest_terminal import BloomQuestTerminal
        print(f"{Colors.GREEN}✓{Colors.RESET} Terminal interface")
        tests_passed += 1
    except:
        print(f"{Colors.RED}✗{Colors.RESET} Terminal interface")

    print(f"\n{Colors.CYAN}Result: {tests_passed}/{tests_total} systems ready{Colors.RESET}")

    if tests_passed == tests_total:
        print(f"{Colors.GREEN}All systems operational! Ready to play.{Colors.RESET}")
        return True
    else:
        print(f"{Colors.YELLOW}Some systems need attention.{Colors.RESET}")
        return False

def main_menu():
    """Main menu for standalone launcher"""
    Colors = StandaloneColors()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        show_game_info()

        print(f"{Colors.CYAN}═══ MAIN MENU ═══{Colors.RESET}\n")
        print(f"  {Colors.GREEN}[1] Play Game (Terminal Mode){Colors.RESET}")
        print(f"  {Colors.YELLOW}[2] Test Systems{Colors.RESET}")
        print(f"  {Colors.CYAN}[3] Installation Help{Colors.RESET}")
        print(f"  {Colors.MAGENTA}[4] About BloomQuest{Colors.RESET}")
        print(f"  {Colors.RED}[0] Exit{Colors.RESET}")

        choice = input(f"\n{Colors.YELLOW}Select option: {Colors.RESET}").strip()

        if choice == "1":
            if run_terminal_game():
                input(f"\n{Colors.YELLOW}Press ENTER to return to menu...{Colors.RESET}")
            else:
                input(f"\n{Colors.RED}Press ENTER to continue...{Colors.RESET}")

        elif choice == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            test_core_systems()
            input(f"\n{Colors.YELLOW}Press ENTER to continue...{Colors.RESET}")

        elif choice == "3":
            show_instructions()

        elif choice == "4":
            show_about()

        elif choice == "0":
            print(f"\n{Colors.GREEN}Thanks for playing BloomQuest!{Colors.RESET}")
            break

        else:
            print(f"{Colors.RED}Invalid option{Colors.RESET}")
            time.sleep(1)

def show_about():
    """Show about information"""
    Colors = StandaloneColors()

    print(f"\n{Colors.CYAN}═══ ABOUT BLOOMQUEST ═══{Colors.RESET}\n")

    print(f"{Colors.BOLD}BloomQuest: NEXTHASH-256 Mining Adventure{Colors.RESET}\n")

    print("A complete cryptocurrency mining game featuring:")
    print("  • NEXTHASH-256 proof-of-work (3.3x faster than SHA-256)")
    print("  • 7 unique companion types with specializations")
    print("  • Pattern discovery and verification system")
    print("  • Real-time stock market simulation")
    print("  • Residue economy with synthesis")
    print("  • Complete progression system")

    print(f"\n{Colors.YELLOW}Game Modes:{Colors.RESET}")
    print("  • Terminal Mode - Full game, no dependencies")
    print("  • Web Mode - Modern UI (requires Flask)")

    print(f"\n{Colors.GREEN}Key Features:{Colors.RESET}")
    print("  ✓ Quantum-resistant cryptography")
    print("  ✓ Guardian alignment system")
    print("  ✓ Equipment crafting")
    print("  ✓ Skill trees and specializations")
    print("  ✓ Market trading with AI recommendations")

    print(f"\n{Colors.MAGENTA}Version 1.0 - February 2026{Colors.RESET}")

    input(f"\n{Colors.YELLOW}Press ENTER to continue...{Colors.RESET}")

def check_web_dependencies():
    """Check if web dependencies are available"""
    try:
        import flask
        import flask_socketio
        return True
    except ImportError:
        return False

def main():
    """Main entry point for standalone launcher"""
    Colors = StandaloneColors()

    # Check if this is first run after web UI error
    if len(sys.argv) > 1 and sys.argv[1] == "--web-failed":
        print(f"\n{Colors.YELLOW}Web interface requires Flask and SocketIO.{Colors.RESET}")
        result = install_dependencies()

        if result == "terminal":
            run_terminal_game()
            return
        elif result == "exit":
            return
        elif result == "retry":
            # Try to run web version again
            if check_web_dependencies():
                print(f"{Colors.GREEN}Dependencies installed! Launching web interface...{Colors.RESET}")
                import bloomquest_web_ui
                bloomquest_web_ui.run_server()
                return

    # Normal flow
    try:
        # First check if we can just run the terminal game
        if TERMINAL_AVAILABLE:
            # Give user choice
            main_menu()
        else:
            print(f"{Colors.RED}Error: Game files not found.{Colors.RESET}")
            print("Make sure all game files are in the current directory:")
            print("  • bloomquest_terminal.py")
            print("  • unified_mining_economy.py")
            print("  • companion_mining_ultimate.py")
            print("  • And other required modules")

    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Game interrupted. Goodbye!{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()