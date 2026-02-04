#!/usr/bin/env python3
"""
BloomQuest Launcher - Universal Game Launcher
==============================================
Launch BloomQuest in terminal or web mode with all modules accessible.
"""

import os
import sys
import subprocess
import time
import webbrowser
from typing import Optional

# ANSI colors for terminal
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    CYAN = '\033[36m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    MAGENTA = '\033[35m'
    RED = '\033[31m'
    BRIGHT_WHITE = '\033[97m'

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Print game banner"""
    banner = f"""
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
║              {Colors.YELLOW}NEXTHASH-256 POWERED CRYPTOCURRENCY MINING GAME{Colors.MAGENTA}               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(banner)

def check_dependencies():
    """Check if required dependencies are installed"""
    missing = []

    # Check Python version
    if sys.version_info < (3, 7):
        print(f"{Colors.RED}Error: Python 3.7+ required (you have {sys.version}){Colors.RESET}")
        return False

    # Check for Flask (for web UI)
    try:
        import flask
        import flask_socketio
    except ImportError:
        missing.append("flask flask-socketio")

    if missing:
        print(f"{Colors.YELLOW}Missing dependencies detected!{Colors.RESET}")
        print(f"Install with: pip install {' '.join(missing)}")
        print(f"\n{Colors.CYAN}Continue without web UI? (y/n): {Colors.RESET}", end="")
        choice = input().strip().lower()
        if choice != 'y':
            return False

    return True

def launch_terminal():
    """Launch terminal interface"""
    print(f"{Colors.CYAN}Launching terminal interface...{Colors.RESET}")
    time.sleep(1)

    try:
        # Import and run terminal game
        from bloomquest_terminal import BloomQuestTerminal
        game = BloomQuestTerminal()
        game.start()
    except ImportError as e:
        print(f"{Colors.RED}Error loading terminal interface: {e}{Colors.RESET}")
        print(f"{Colors.YELLOW}Make sure bloomquest_terminal.py is in the same directory{Colors.RESET}")
        return False
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Game interrupted. Returning to launcher...{Colors.RESET}")
        return True
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        return False

    return True

def launch_web():
    """Launch web interface"""
    print(f"{Colors.CYAN}Starting web server...{Colors.RESET}")

    try:
        # Start Flask server in subprocess
        process = subprocess.Popen(
            [sys.executable, "-c", """
from bloomquest_web_ui import run_server
run_server(host='127.0.0.1', port=5000, debug=False)
"""],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Wait for server to start
        time.sleep(3)

        # Open browser
        url = "http://localhost:5000"
        print(f"{Colors.GREEN}Opening browser at {url}{Colors.RESET}")
        webbrowser.open(url)

        print(f"\n{Colors.YELLOW}Web server running!{Colors.RESET}")
        print(f"Access the game at: {Colors.CYAN}{url}{Colors.RESET}")
        print(f"Press {Colors.RED}Ctrl+C{Colors.RESET} to stop the server\n")

        # Wait for interrupt
        try:
            process.wait()
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Stopping web server...{Colors.RESET}")
            process.terminate()
            time.sleep(1)

    except ImportError:
        print(f"{Colors.RED}Error: Web UI requires Flask and Flask-SocketIO{Colors.RESET}")
        print(f"Install with: pip install flask flask-socketio")
        return False
    except Exception as e:
        print(f"{Colors.RED}Error starting web server: {e}{Colors.RESET}")
        return False

    return True

def quick_test():
    """Quick test of all systems"""
    print(f"{Colors.CYAN}Running system diagnostics...{Colors.RESET}\n")

    tests_passed = 0
    tests_total = 0

    # Test NEXTHASH
    tests_total += 1
    try:
        from nexthash256 import nexthash256_hex
        hash_result = nexthash256_hex("test")
        print(f"{Colors.GREEN}✓{Colors.RESET} NEXTHASH-256 working")
        tests_passed += 1
    except Exception as e:
        print(f"{Colors.RED}✗{Colors.RESET} NEXTHASH-256 failed: {e}")

    # Test Companion System
    tests_total += 1
    try:
        from companion_mining_ultimate import UltimateCompanionMiningManager, CompanionType
        print(f"{Colors.GREEN}✓{Colors.RESET} Companion system loaded")
        tests_passed += 1
    except Exception as e:
        print(f"{Colors.RED}✗{Colors.RESET} Companion system failed: {e}")

    # Test Pattern System
    tests_total += 1
    try:
        from guardian_pattern_recipes import PatternType, GuardianPatternSystem
        print(f"{Colors.GREEN}✓{Colors.RESET} Pattern system loaded")
        tests_passed += 1
    except Exception as e:
        print(f"{Colors.RED}✗{Colors.RESET} Pattern system failed: {e}")

    # Test Economy
    tests_total += 1
    try:
        from unified_mining_economy import UnifiedMiningEconomy
        print(f"{Colors.GREEN}✓{Colors.RESET} Unified economy loaded")
        tests_passed += 1
    except Exception as e:
        print(f"{Colors.RED}✗{Colors.RESET} Unified economy failed: {e}")

    # Test Integration Bridge
    tests_total += 1
    try:
        from economy_integration_bridge import UnifiedGameInterface
        print(f"{Colors.GREEN}✓{Colors.RESET} Integration bridge loaded")
        tests_passed += 1
    except Exception as e:
        print(f"{Colors.RED}✗{Colors.RESET} Integration bridge failed: {e}")

    print(f"\n{Colors.CYAN}Results: {tests_passed}/{tests_total} tests passed{Colors.RESET}")

    if tests_passed == tests_total:
        print(f"{Colors.GREEN}All systems operational!{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}Some systems may not function correctly{Colors.RESET}")

    return tests_passed == tests_total

def show_features():
    """Show available features"""
    print(f"\n{Colors.CYAN}═══ AVAILABLE FEATURES ═══{Colors.RESET}\n")

    features = [
        ("⛏️", "NEXTHASH-256 Mining", "3.3x faster cryptocurrency mining"),
        ("🤝", "7 Companion Types", "Each with unique abilities and specializations"),
        ("🔮", "Pattern Discovery", "Find and trade valuable blockchain patterns"),
        ("📈", "Stock Market", "Real-time pattern stock trading"),
        ("⚗️", "Residue Economy", "Synthesize mining byproducts into rewards"),
        ("🏆", "Progression System", "Level up, unlock skills, earn achievements"),
        ("💼", "Job Specializations", "15+ mining job types with bonuses"),
        ("🛡️", "Guardian Alignments", "4 guardians providing unique benefits"),
        ("💰", "Complete Economy", "Wallets, transactions, market dynamics"),
        ("🎮", "Two Interfaces", "Terminal for power users, Web for modern UI")
    ]

    for icon, title, desc in features:
        print(f"  {icon} {Colors.BOLD}{title}{Colors.RESET}")
        print(f"     {Colors.DIM}{desc}{Colors.RESET}")

    input(f"\n{Colors.DIM}Press ENTER to continue...{Colors.RESET}")

def main_menu():
    """Main launcher menu"""
    while True:
        clear_screen()
        print_banner()

        print(f"\n{Colors.CYAN}═══ MAIN MENU ═══{Colors.RESET}\n")
        print(f"  {Colors.BRIGHT_WHITE}[1]{Colors.RESET} Terminal Interface (Classic)")
        print(f"  {Colors.BRIGHT_WHITE}[2]{Colors.RESET} Web Interface (Modern)")
        print(f"  {Colors.BRIGHT_WHITE}[3]{Colors.RESET} Quick Test Systems")
        print(f"  {Colors.BRIGHT_WHITE}[4]{Colors.RESET} View Features")
        print(f"  {Colors.BRIGHT_WHITE}[5]{Colors.RESET} Documentation")
        print(f"  {Colors.BRIGHT_WHITE}[0]{Colors.RESET} Exit")

        print(f"\n{Colors.YELLOW}Select option: {Colors.RESET}", end="")
        choice = input().strip()

        if choice == "1":
            clear_screen()
            if launch_terminal():
                input(f"\n{Colors.DIM}Press ENTER to return to menu...{Colors.RESET}")
        elif choice == "2":
            clear_screen()
            if launch_web():
                input(f"\n{Colors.DIM}Press ENTER to return to menu...{Colors.RESET}")
        elif choice == "3":
            clear_screen()
            quick_test()
            input(f"\n{Colors.DIM}Press ENTER to continue...{Colors.RESET}")
        elif choice == "4":
            show_features()
        elif choice == "5":
            show_documentation()
        elif choice == "0":
            print(f"\n{Colors.GREEN}Thanks for playing BloomQuest!{Colors.RESET}")
            print(f"{Colors.DIM}May your mining be profitable!{Colors.RESET}\n")
            break
        else:
            print(f"{Colors.RED}Invalid option{Colors.RESET}")
            time.sleep(1)

def show_documentation():
    """Show documentation info"""
    clear_screen()
    print(f"{Colors.CYAN}═══ DOCUMENTATION ═══{Colors.RESET}\n")

    docs = [
        ("README", "NEXTHASH_UPGRADE_COMPLETE.md", "NEXTHASH-256 implementation details"),
        ("Companion Mining", "COMPANION_MINING_NEXTHASH_DOCS.md", "Complete companion system guide"),
        ("Unified Economy", "UNIFIED_ECONOMY_DOCUMENTATION.md", "Economic system integration"),
        ("API Reference", "See code files", "Detailed API documentation in source")
    ]

    print("Available documentation files:\n")
    for title, file, desc in docs:
        print(f"  {Colors.BOLD}{title}{Colors.RESET}")
        print(f"    File: {Colors.CYAN}{file}{Colors.RESET}")
        print(f"    {Colors.DIM}{desc}{Colors.RESET}\n")

    print(f"{Colors.YELLOW}Terminal Commands:{Colors.RESET}")
    print("  In terminal mode, type 'help' for command list")
    print("  Use arrow keys to navigate menus")

    print(f"\n{Colors.YELLOW}Web Interface:{Colors.RESET}")
    print("  Navigate using the sidebar menu")
    print("  All features accessible through UI")

    input(f"\n{Colors.DIM}Press ENTER to return to menu...{Colors.RESET}")

def main():
    """Main entry point"""
    try:
        # Check dependencies
        if not check_dependencies():
            print(f"\n{Colors.RED}Dependency check failed. Exiting...{Colors.RESET}")
            sys.exit(1)

        # Run main menu
        main_menu()

    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Launcher interrupted. Goodbye!{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Fatal error: {e}{Colors.RESET}")
        print(f"{Colors.DIM}Please report this issue{Colors.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()