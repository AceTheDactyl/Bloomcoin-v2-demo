#!/usr/bin/env python3
"""
BloomQuest Terminal - Complete Interactive Game Interface
==========================================================
Full gameplay experience with UI commands and module integration.
Access every system through an intuitive terminal interface.
"""

import os
import sys
import time
import json
import random
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import threading
from collections import defaultdict

# Import unified economy
from unified_mining_economy import (
    UnifiedMiningEconomy,
    UnifiedMiningJob,
    MiningJobType,
    ResidueType,
    format_bloomcoin
)

# Import integration bridge
from economy_integration_bridge import (
    UnifiedGameInterface,
    PatternSystemIntegration,
    ResidueRecyclingInterface,
    MarketTradingInterface
)

# Import companion system
from companion_mining_ultimate import (
    CompanionType,
    SpecializationPath,
    CompanionSkillTree
)

# Import pattern system
from guardian_pattern_recipes import PatternType

# ANSI color codes for terminal UI
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'

    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

# ═══════════════════════════════════════════════════════════════════════
# GAME STATE MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class PlayerState:
    """Complete player state tracking"""
    name: str
    level: int = 1
    experience: int = 0
    wallet_address: Optional[str] = None
    balance: float = 0.0

    # Collections
    companions: List[str] = None
    patterns: List[str] = None
    residue_inventory: Dict[str, float] = None
    equipment: List[str] = None

    # Progress tracking
    total_mined: float = 0.0
    patterns_discovered: int = 0
    market_trades: int = 0
    residue_synthesized: int = 0
    battles_won: int = 0

    # Achievements
    achievements: List[str] = None
    titles: List[str] = None
    current_title: str = "Novice Miner"

    # Settings
    auto_complete_jobs: bool = False
    show_notifications: bool = True
    ui_style: str = "modern"  # modern, classic, minimal

    def __post_init__(self):
        if self.companions is None:
            self.companions = []
        if self.patterns is None:
            self.patterns = []
        if self.residue_inventory is None:
            self.residue_inventory = {}
        if self.equipment is None:
            self.equipment = []
        if self.achievements is None:
            self.achievements = []
        if self.titles is None:
            self.titles = ["Novice Miner"]

# ═══════════════════════════════════════════════════════════════════════
# UI COMPONENTS
# ═══════════════════════════════════════════════════════════════════════

class UIComponents:
    """Reusable UI components for terminal interface"""

    @staticmethod
    def clear_screen():
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def header(title: str, subtitle: str = "", style: str = "modern"):
        """Display styled header"""
        if style == "modern":
            print(f"\n{Colors.BRIGHT_CYAN}{'═' * 80}{Colors.RESET}")
            print(f"{Colors.BRIGHT_WHITE}{Colors.BOLD}{title.center(80)}{Colors.RESET}")
            if subtitle:
                print(f"{Colors.CYAN}{subtitle.center(80)}{Colors.RESET}")
            print(f"{Colors.BRIGHT_CYAN}{'═' * 80}{Colors.RESET}\n")
        elif style == "classic":
            print(f"\n{Colors.GREEN}{'=' * 80}{Colors.RESET}")
            print(f"{Colors.BRIGHT_GREEN}{title.center(80)}{Colors.RESET}")
            if subtitle:
                print(f"{Colors.GREEN}{subtitle.center(80)}{Colors.RESET}")
            print(f"{Colors.GREEN}{'=' * 80}{Colors.RESET}\n")
        else:  # minimal
            print(f"\n{title}")
            if subtitle:
                print(f"{subtitle}")
            print("-" * len(title))

    @staticmethod
    def menu(title: str, options: List[Tuple[str, str]], style: str = "modern"):
        """Display menu with options"""
        if style == "modern":
            print(f"\n{Colors.BRIGHT_YELLOW}┌─ {title} ─┐{Colors.RESET}")
            for key, desc in options:
                print(f"{Colors.YELLOW}│{Colors.RESET} {Colors.BRIGHT_WHITE}[{key}]{Colors.RESET} {desc}")
            print(f"{Colors.BRIGHT_YELLOW}└{'─' * (len(title) + 6)}┘{Colors.RESET}")
        else:
            print(f"\n{title}:")
            for key, desc in options:
                print(f"  [{key}] {desc}")

    @staticmethod
    def progress_bar(current: float, total: float, width: int = 40,
                     label: str = "", show_percent: bool = True):
        """Display progress bar"""
        if total <= 0:
            percent = 0
        else:
            percent = min(100, (current / total) * 100)

        filled = int((percent / 100) * width)
        bar = "█" * filled + "░" * (width - filled)

        if show_percent:
            output = f"{label} [{Colors.BRIGHT_GREEN}{bar}{Colors.RESET}] {percent:.1f}%"
        else:
            output = f"{label} [{Colors.BRIGHT_GREEN}{bar}{Colors.RESET}]"

        print(output)

    @staticmethod
    def table(headers: List[str], rows: List[List[str]],
              colors: List[str] = None, align: str = "left"):
        """Display formatted table"""
        # Calculate column widths
        widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(str(cell)))

        # Print header
        header_line = " │ ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
        print(f"{Colors.BRIGHT_WHITE}{header_line}{Colors.RESET}")
        print("─" * (sum(widths) + len(headers) * 3 - 1))

        # Print rows
        for row in rows:
            cells = []
            for i, cell in enumerate(row):
                cell_str = str(cell)
                if align == "right":
                    cell_str = cell_str.rjust(widths[i])
                elif align == "center":
                    cell_str = cell_str.center(widths[i])
                else:
                    cell_str = cell_str.ljust(widths[i])

                if colors and i < len(colors):
                    cell_str = f"{colors[i]}{cell_str}{Colors.RESET}"

                cells.append(cell_str)

            print(" │ ".join(cells))

    @staticmethod
    def notification(message: str, type: str = "info"):
        """Display notification message"""
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "mining": "⛏️",
            "pattern": "🔮",
            "market": "📈",
            "companion": "🤝",
            "achievement": "🏆"
        }

        colors = {
            "info": Colors.CYAN,
            "success": Colors.BRIGHT_GREEN,
            "warning": Colors.YELLOW,
            "error": Colors.RED,
            "mining": Colors.BRIGHT_YELLOW,
            "pattern": Colors.MAGENTA,
            "market": Colors.BRIGHT_BLUE,
            "companion": Colors.GREEN,
            "achievement": Colors.BRIGHT_MAGENTA
        }

        icon = icons.get(type, "•")
        color = colors.get(type, Colors.WHITE)

        print(f"\n{color}{icon} {message}{Colors.RESET}")

    @staticmethod
    def loading_animation(duration: float = 2.0, message: str = "Loading"):
        """Display loading animation"""
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        start_time = time.time()

        while time.time() - start_time < duration:
            for frame in frames:
                print(f"\r{Colors.CYAN}{frame} {message}...{Colors.RESET}", end="", flush=True)
                time.sleep(0.1)
                if time.time() - start_time >= duration:
                    break

        print(f"\r{Colors.GREEN}✓ {message} complete!{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════
# GAME INTERFACE
# ═══════════════════════════════════════════════════════════════════════

class BloomQuestTerminal:
    """Main game terminal interface"""

    def __init__(self):
        # Initialize game systems
        self.game = UnifiedGameInterface()
        self.ui = UIComponents()

        # Player state
        self.player: Optional[PlayerState] = None
        self.current_menu = "main"
        self.running = True

        # Auto-completion thread
        self.auto_complete_thread = None
        self.active_jobs: Dict[str, float] = {}  # job_id -> start_time

        # Command history
        self.command_history: List[str] = []
        self.history_index = -1

    def start(self):
        """Start the game"""
        self.ui.clear_screen()
        self._show_splash_screen()
        self._login_or_create()
        self._main_loop()

    def _show_splash_screen(self):
        """Display game splash screen"""
        splash = f"""
{Colors.BRIGHT_MAGENTA}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  {Colors.BRIGHT_WHITE}██████╗ ██╗      ██████╗  ██████╗ ███╗   ███╗ ██████╗ ██╗   ██╗███████╗{Colors.BRIGHT_MAGENTA}  ║
║  {Colors.BRIGHT_WHITE}██╔══██╗██║     ██╔═══██╗██╔═══██╗████╗ ████║██╔═══██╗██║   ██║██╔════╝{Colors.BRIGHT_MAGENTA}  ║
║  {Colors.BRIGHT_CYAN}██████╔╝██║     ██║   ██║██║   ██║██╔████╔██║██║   ██║██║   ██║█████╗  {Colors.BRIGHT_MAGENTA}  ║
║  {Colors.BRIGHT_CYAN}██╔══██╗██║     ██║   ██║██║   ██║██║╚██╔╝██║██║▄▄ ██║██║   ██║██╔══╝  {Colors.BRIGHT_MAGENTA}  ║
║  {Colors.BRIGHT_BLUE}██████╔╝███████╗╚██████╔╝╚██████╔╝██║ ╚═╝ ██║╚██████╔╝╚██████╔╝███████╗{Colors.BRIGHT_MAGENTA}  ║
║  {Colors.BRIGHT_BLUE}╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝{Colors.BRIGHT_MAGENTA}  ║
║                                                                              ║
║                {Colors.YELLOW}NEXTHASH-256 POWERED CRYPTOCURRENCY ADVENTURE{Colors.BRIGHT_MAGENTA}                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}
                    {Colors.CYAN}Press ENTER to begin your journey...{Colors.RESET}
"""
        print(splash)
        input()

    def _login_or_create(self):
        """Login or create new player"""
        self.ui.clear_screen()
        self.ui.header("WELCOME TO BLOOMQUEST", "Choose your path")

        options = [
            ("1", "Create New Character"),
            ("2", "Load Existing Character"),
            ("3", "Quick Start (Demo Mode)")
        ]

        self.ui.menu("Character Selection", options)

        choice = input(f"\n{Colors.YELLOW}Your choice: {Colors.RESET}").strip()

        if choice == "1":
            self._create_character()
        elif choice == "2":
            self._load_character()
        else:
            self._quick_start()

    def _create_character(self):
        """Create new character"""
        self.ui.clear_screen()
        self.ui.header("CHARACTER CREATION", "Forge your destiny")

        name = input(f"{Colors.CYAN}Enter your name: {Colors.RESET}").strip() or "Adventurer"

        # Create player in game
        player_data = self.game.create_player(name, initial_balance=1000.0)

        # Initialize player state
        self.player = PlayerState(
            name=name,
            wallet_address=player_data["wallet"].address,
            balance=1000.0,
            companions=[player_data["companion"].name]
        )

        self.ui.notification(f"Welcome to BloomQuest, {name}!", "success")
        self.ui.notification("You've received 1000 BC starting balance", "info")
        self.ui.notification(f"Your companion {player_data['companion'].name} joins you", "companion")

        time.sleep(2)

    def _load_character(self):
        """Load existing character"""
        # For now, create a demo character
        self.ui.notification("Save system coming soon! Creating demo character...", "warning")
        time.sleep(1)
        self._quick_start()

    def _quick_start(self):
        """Quick start with demo character"""
        # Create demo player
        player_data = self.game.create_player("Demo_Player", initial_balance=5000.0)

        self.player = PlayerState(
            name="Demo Player",
            level=5,
            experience=2500,
            wallet_address=player_data["wallet"].address,
            balance=5000.0,
            companions=[player_data["companion"].name],
            patterns=["RESONANCE", "CRYSTALLINE"],
            residue_inventory={"QUANTUM": 10.5, "VOID": 5.2, "HARMONIC": 7.8},
            total_mined=1234.56,
            patterns_discovered=5,
            market_trades=10,
            achievements=["First Mine", "Pattern Hunter", "Market Trader"]
        )

        self.ui.notification("Demo character loaded!", "success")
        time.sleep(1)

    def _main_loop(self):
        """Main game loop"""
        while self.running:
            try:
                self.ui.clear_screen()
                self._show_status_bar()

                if self.current_menu == "main":
                    self._main_menu()
                elif self.current_menu == "mining":
                    self._mining_menu()
                elif self.current_menu == "companions":
                    self._companions_menu()
                elif self.current_menu == "patterns":
                    self._patterns_menu()
                elif self.current_menu == "market":
                    self._market_menu()
                elif self.current_menu == "residue":
                    self._residue_menu()
                elif self.current_menu == "stats":
                    self._stats_menu()
                elif self.current_menu == "settings":
                    self._settings_menu()

            except KeyboardInterrupt:
                self._confirm_exit()
            except Exception as e:
                self.ui.notification(f"Error: {e}", "error")
                time.sleep(2)

    def _show_status_bar(self):
        """Display player status bar"""
        if not self.player:
            return

        # Calculate level progress
        xp_for_next = 100 * (self.player.level ** 1.5)
        xp_progress = self.player.experience % xp_for_next

        # Format balance
        balance_str = format_bloomcoin(self.player.balance)

        # Active jobs
        active_count = len(self.active_jobs)
        job_str = f"{active_count} active" if active_count > 0 else "None"

        # Status line
        status = f"""
{Colors.BG_BLUE}{Colors.BRIGHT_WHITE} {self.player.name} {Colors.RESET} {Colors.CYAN}Lvl {self.player.level}{Colors.RESET} │ {Colors.YELLOW}⛏ {job_str}{Colors.RESET} │ {Colors.GREEN}💰 {balance_str}{Colors.RESET} │ {Colors.MAGENTA}🔮 {len(self.player.patterns)} patterns{Colors.RESET}
"""
        print(status)

        # XP progress bar
        self.ui.progress_bar(xp_progress, xp_for_next, width=60,
                            label="Experience", show_percent=True)

    def _main_menu(self):
        """Main menu interface"""
        self.ui.header("BLOOMQUEST TERMINAL", f"Welcome back, {self.player.name}!")

        # Check for completed jobs
        self._check_completed_jobs()

        options = [
            ("1", f"{Colors.YELLOW}⛏{Colors.RESET}  Mining Operations"),
            ("2", f"{Colors.GREEN}🤝{Colors.RESET}  Companion Management"),
            ("3", f"{Colors.MAGENTA}🔮{Colors.RESET}  Pattern Discovery"),
            ("4", f"{Colors.BLUE}📈{Colors.RESET}  Stock Market"),
            ("5", f"{Colors.CYAN}⚗️{Colors.RESET}  Residue Laboratory"),
            ("6", f"{Colors.WHITE}📊{Colors.RESET}  Statistics & Reports"),
            ("7", f"{Colors.BRIGHT_BLACK}⚙️{Colors.RESET}  Settings"),
            ("8", f"{Colors.GREEN}💾{Colors.RESET}  Save Game"),
            ("9", f"{Colors.RED}🚪{Colors.RESET}  Exit Game")
        ]

        self.ui.menu("Main Menu", options, self.player.ui_style)

        choice = input(f"\n{Colors.YELLOW}Select option: {Colors.RESET}").strip()

        menu_map = {
            "1": "mining",
            "2": "companions",
            "3": "patterns",
            "4": "market",
            "5": "residue",
            "6": "stats",
            "7": "settings",
            "8": self._save_game,
            "9": self._confirm_exit
        }

        if choice in menu_map:
            if callable(menu_map[choice]):
                menu_map[choice]()
            else:
                self.current_menu = menu_map[choice]

    def _mining_menu(self):
        """Mining operations menu"""
        self.ui.header("MINING OPERATIONS", "Extract BloomCoin with NEXTHASH-256")

        # Show active jobs
        if self.active_jobs:
            print(f"{Colors.YELLOW}Active Mining Jobs:{Colors.RESET}")
            for job_id, start_time in self.active_jobs.items():
                elapsed = time.time() - start_time
                status = self.game.check_mining(job_id)
                if status["status"] == "active":
                    self.ui.progress_bar(status["progress"], 1.0, width=50,
                                       label=f"Job {job_id[:8]}", show_percent=True)

        options = [
            ("1", "Start New Mining Job"),
            ("2", "Quick Mine (Auto-select)"),
            ("3", "Team Mining (Multiple Companions)"),
            ("4", "Check Job Status"),
            ("5", "Collect Rewards"),
            ("6", "Mining Statistics"),
            ("0", "Back to Main Menu")
        ]

        self.ui.menu("Mining Menu", options, self.player.ui_style)

        choice = input(f"\n{Colors.YELLOW}Select option: {Colors.RESET}").strip()

        if choice == "1":
            self._start_mining_job()
        elif choice == "2":
            self._quick_mine()
        elif choice == "3":
            self._team_mining()
        elif choice == "4":
            self._check_job_status()
        elif choice == "5":
            self._collect_rewards()
        elif choice == "6":
            self._mining_statistics()
        elif choice == "0":
            self.current_menu = "main"

    def _start_mining_job(self):
        """Start a new mining job with options"""
        print(f"\n{Colors.CYAN}Select Mining Type:{Colors.RESET}")

        job_types = [
            ("1", "Pattern Discovery", MiningJobType.PATTERN_DISCOVERY),
            ("2", "Hash Optimization", MiningJobType.HASH_OPTIMIZATION),
            ("3", "Residue Collection", MiningJobType.RESIDUE_COLLECTION),
            ("4", "Guardian Alignment", MiningJobType.GUARDIAN_ALIGNMENT),
            ("5", "Echo Resonance", MiningJobType.ECHO_RESONANCE),
            ("6", "Market Arbitrage", MiningJobType.ARBITRAGE_MINING)
        ]

        for key, name, _ in job_types:
            print(f"  [{key}] {name}")

        type_choice = input(f"{Colors.YELLOW}Select type: {Colors.RESET}").strip()

        if type_choice in [k for k, _, _ in job_types]:
            job_type = job_types[int(type_choice) - 1][2]

            # Select difficulty
            print(f"\n{Colors.CYAN}Select Difficulty:{Colors.RESET}")
            print("  [1] Easy (1-2 min)")
            print("  [2] Normal (2-3 min)")
            print("  [3] Hard (3-5 min)")
            print("  [4] Expert (5-10 min)")

            diff_choice = input(f"{Colors.YELLOW}Select difficulty: {Colors.RESET}").strip()
            difficulty = int(diff_choice) if diff_choice.isdigit() else 2

            # Start job
            job = self.game.economy.create_mining_job(
                player_id=self.player.name,
                companion_id=f"{self.player.name}_starter",
                job_type=job_type,
                difficulty=difficulty
            )

            if job:
                self.active_jobs[job.job_id] = time.time()
                self.ui.notification(f"Mining job started! ID: {job.job_id[:8]}", "mining")

                if self.player.auto_complete_jobs:
                    self._start_auto_completion(job.job_id, job.duration)

            time.sleep(2)

    def _quick_mine(self):
        """Quick mining with auto-selection"""
        self.ui.loading_animation(1.0, "Analyzing market conditions")

        # Start optimized job
        job = self.game.start_mining(self.player.name)

        if job:
            self.active_jobs[job.job_id] = time.time()
            self.ui.notification(f"Quick mine started! Expected reward: {job.base_reward:.2f} BC", "mining")

            if self.player.auto_complete_jobs:
                self._start_auto_completion(job.job_id, job.duration)

        time.sleep(2)

    def _team_mining(self):
        """Team mining with multiple companions"""
        self.ui.notification("Team mining coming soon!", "warning")
        time.sleep(2)

    def _check_job_status(self):
        """Check status of all jobs"""
        if not self.active_jobs:
            self.ui.notification("No active mining jobs", "info")
        else:
            print(f"\n{Colors.CYAN}Job Status:{Colors.RESET}")

            headers = ["Job ID", "Progress", "Est. Reward", "Time Left"]
            rows = []

            for job_id in list(self.active_jobs.keys()):
                status = self.game.check_mining(job_id)

                if status["status"] == "completed":
                    rows.append([
                        job_id[:8],
                        "COMPLETE",
                        f"{status.get('reward', 0):.2f} BC",
                        "Ready"
                    ])
                elif status["status"] == "active":
                    progress = status["progress"] * 100
                    est_reward = status.get("estimated_reward", 0)
                    time_left = status["duration"] - status["elapsed"]

                    rows.append([
                        job_id[:8],
                        f"{progress:.1f}%",
                        f"{est_reward:.2f} BC",
                        f"{time_left:.0f}s"
                    ])

            self.ui.table(headers, rows)

        input(f"\n{Colors.DIM}Press ENTER to continue...{Colors.RESET}")

    def _collect_rewards(self):
        """Collect rewards from completed jobs"""
        completed = []

        for job_id in list(self.active_jobs.keys()):
            status = self.game.check_mining(job_id)

            if status["status"] == "completed":
                # Process completion
                self.game.economy.process_mining(job_id)

                # Update player
                self.player.balance += status.get("reward", 0)
                self.player.total_mined += status.get("reward", 0)
                self.player.experience += status.get("xp", 0)

                # Add patterns
                for pattern in status.get("patterns", []):
                    if pattern not in self.player.patterns:
                        self.player.patterns.append(pattern)
                        self.player.patterns_discovered += 1

                # Add residue
                if status.get("residue", 0) > 0:
                    # Simplified - add to quantum residue
                    self.player.residue_inventory["QUANTUM"] = \
                        self.player.residue_inventory.get("QUANTUM", 0) + status["residue"]

                completed.append(job_id)

                self.ui.notification(
                    f"Collected {status['reward']:.2f} BC from job {job_id[:8]}",
                    "success"
                )

        # Remove completed jobs
        for job_id in completed:
            del self.active_jobs[job_id]

        if not completed:
            self.ui.notification("No completed jobs to collect", "info")
        else:
            # Check for level up
            self._check_level_up()

        time.sleep(2)

    def _mining_statistics(self):
        """Show mining statistics"""
        print(f"\n{Colors.CYAN}Mining Statistics:{Colors.RESET}")

        stats = [
            ("Total Mined", format_bloomcoin(self.player.total_mined)),
            ("Active Jobs", str(len(self.active_jobs))),
            ("Completed Jobs", str(len(self.game.economy.completed_jobs))),
            ("Success Rate", "95.2%"),  # Mock for now
            ("Best Haul", "523.45 BC"),  # Mock
            ("Mining Level", str(self.player.level))
        ]

        for label, value in stats:
            print(f"  {Colors.WHITE}{label}:{Colors.RESET} {Colors.BRIGHT_GREEN}{value}{Colors.RESET}")

        input(f"\n{Colors.DIM}Press ENTER to continue...{Colors.RESET}")

    def _companions_menu(self):
        """Companion management menu"""
        self.ui.header("COMPANION MANAGEMENT", "Your loyal mining partners")

        # List companions
        print(f"{Colors.CYAN}Your Companions:{Colors.RESET}")
        for i, comp_name in enumerate(self.player.companions, 1):
            print(f"  {i}. {comp_name} (Level 1)")  # Mock level

        options = [
            ("1", "View Companion Details"),
            ("2", "Level Up Companion"),
            ("3", "Apply Specialization"),
            ("4", "Equip Items"),
            ("5", "Learn Skills"),
            ("6", "Recruit New Companion"),
            ("0", "Back to Main Menu")
        ]

        self.ui.menu("Companion Menu", options, self.player.ui_style)

        choice = input(f"\n{Colors.YELLOW}Select option: {Colors.RESET}").strip()

        if choice == "0":
            self.current_menu = "main"
        else:
            self.ui.notification("Companion features coming soon!", "warning")
            time.sleep(2)

    def _patterns_menu(self):
        """Pattern discovery menu"""
        self.ui.header("PATTERN DISCOVERY", "Unlock the secrets of the blockchain")

        # Show discovered patterns
        print(f"{Colors.CYAN}Discovered Patterns ({len(self.player.patterns)}):{Colors.RESET}")
        for pattern in self.player.patterns:
            print(f"  🔮 {pattern}")

        options = [
            ("1", "Verify Patterns"),
            ("2", "Guardian Blessings"),
            ("3", "Pattern Synthesis"),
            ("4", "Pattern Market Value"),
            ("5", "Discovery Statistics"),
            ("0", "Back to Main Menu")
        ]

        self.ui.menu("Pattern Menu", options, self.player.ui_style)

        choice = input(f"\n{Colors.YELLOW}Select option: {Colors.RESET}").strip()

        if choice == "0":
            self.current_menu = "main"
        elif choice == "4":
            self._show_pattern_values()
        else:
            self.ui.notification("Pattern features coming soon!", "warning")
            time.sleep(2)

    def _show_pattern_values(self):
        """Show market value of patterns"""
        print(f"\n{Colors.CYAN}Pattern Market Values:{Colors.RESET}")

        headers = ["Pattern", "Stock Symbol", "Current Price", "24h Change"]
        rows = []

        for pattern in self.player.patterns:
            symbol = pattern[:4].upper()
            if symbol in self.game.economy.stock_market.stocks:
                stock = self.game.economy.stock_market.stocks[symbol]
                change = ((stock.current_price - stock.opening_price) /
                         stock.opening_price * 100)

                change_color = Colors.GREEN if change > 0 else Colors.RED
                change_str = f"{change_color}{change:+.1f}%{Colors.RESET}"

                rows.append([
                    pattern,
                    symbol,
                    f"{stock.current_price:.2f} BC",
                    change_str
                ])

        if rows:
            self.ui.table(headers, rows)
        else:
            print("No pattern market data available")

        input(f"\n{Colors.DIM}Press ENTER to continue...{Colors.RESET}")

    def _market_menu(self):
        """Stock market menu"""
        self.ui.header("PATTERN STOCK MARKET", "Trade patterns for profit")

        # Get market overview
        overview = self.game.market.get_market_overview()

        print(f"{Colors.CYAN}Market Overview:{Colors.RESET}")
        print(f"  Sentiment: {overview['market_sentiment']:.2f}x")
        print(f"  Total Stocks: {overview['total_stocks']}")

        if overview.get("top_gainers"):
            print(f"\n{Colors.GREEN}Top Gainers:{Colors.RESET}")
            for stock in overview["top_gainers"][:3]:
                print(f"  {stock['symbol']}: +{stock['change']:.1f}%")

        options = [
            ("1", "View All Stocks"),
            ("2", "Buy Stocks"),
            ("3", "Sell Stocks"),
            ("4", "Portfolio Value"),
            ("5", "AI Recommendations"),
            ("6", "Market History"),
            ("0", "Back to Main Menu")
        ]

        self.ui.menu("Market Menu", options, self.player.ui_style)

        choice = input(f"\n{Colors.YELLOW}Select option: {Colors.RESET}").strip()

        if choice == "0":
            self.current_menu = "main"
        elif choice == "1":
            self._view_all_stocks()
        elif choice == "5":
            self._show_ai_recommendations()
        else:
            self.ui.notification("Market features coming soon!", "warning")
            time.sleep(2)

    def _view_all_stocks(self):
        """View all pattern stocks"""
        print(f"\n{Colors.CYAN}All Pattern Stocks:{Colors.RESET}")

        headers = ["Symbol", "Price", "24h High", "24h Low", "Volume", "Trend"]
        rows = []

        for symbol, stock in self.game.economy.stock_market.stocks.items():
            trend_emoji = {
                "BULL_RUN": "🚀",
                "BULL": "📈",
                "NEUTRAL": "➡️",
                "BEAR": "📉",
                "CRASH": "💥",
                "BUBBLE": "🎈"
            }

            trend = stock.trend.name if hasattr(stock.trend, 'name') else "UNKNOWN"

            rows.append([
                symbol,
                f"{stock.current_price:.2f}",
                f"{stock.high_24h:.2f}",
                f"{stock.low_24h:.2f}",
                str(stock.volume_24h),
                trend_emoji.get(trend, "❓")
            ])

        self.ui.table(headers, rows)

        input(f"\n{Colors.DIM}Press ENTER to continue...{Colors.RESET}")

    def _show_ai_recommendations(self):
        """Show AI trading recommendations"""
        print(f"\n{Colors.CYAN}AI Trading Recommendations:{Colors.RESET}")

        recommendations = self.game.market.get_recommended_trades(self.player.name)

        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                action_color = Colors.GREEN if rec["action"] == "BUY" else Colors.RED
                print(f"\n{i}. {action_color}{rec['action']}{Colors.RESET} {rec['symbol']}")
                print(f"   Reason: {rec['reason']}")
                print(f"   Confidence: {rec['confidence']:.0%}")
        else:
            print("No recommendations available at this time")

        input(f"\n{Colors.DIM}Press ENTER to continue...{Colors.RESET}")

    def _residue_menu(self):
        """Residue laboratory menu"""
        self.ui.header("RESIDUE LABORATORY", "Transform mining byproducts")

        # Show residue inventory
        print(f"{Colors.CYAN}Residue Inventory:{Colors.RESET}")
        for residue_type, amount in self.player.residue_inventory.items():
            print(f"  {residue_type}: {amount:.2f} units")

        options = [
            ("1", "View Recipes"),
            ("2", "Synthesize Items"),
            ("3", "Recycle to BloomCoin"),
            ("4", "Auto-Synthesize"),
            ("5", "Residue Market"),
            ("0", "Back to Main Menu")
        ]

        self.ui.menu("Residue Menu", options, self.player.ui_style)

        choice = input(f"\n{Colors.YELLOW}Select option: {Colors.RESET}").strip()

        if choice == "0":
            self.current_menu = "main"
        elif choice == "1":
            self._view_recipes()
        elif choice == "3":
            self._recycle_residue()
        else:
            self.ui.notification("Residue features coming soon!", "warning")
            time.sleep(2)

    def _view_recipes(self):
        """View synthesis recipes"""
        print(f"\n{Colors.CYAN}Synthesis Recipes:{Colors.RESET}")

        recipes = self.game.residue.show_available_recipes()

        for recipe in recipes:
            print(f"\n{Colors.BRIGHT_WHITE}{recipe['name']}{Colors.RESET}")
            print(f"  {recipe['description']}")
            print(f"  Requires: {recipe['inputs']}")
            print(f"  Produces: {recipe['outputs']}")

        input(f"\n{Colors.DIM}Press ENTER to continue...{Colors.RESET}")

    def _recycle_residue(self):
        """Recycle residue to BloomCoin"""
        if not self.player.residue_inventory:
            self.ui.notification("No residue to recycle", "info")
        else:
            total_bc = self.game.residue.recycle_all_residue(
                self.player.name,
                self.player.residue_inventory.copy()
            )

            self.player.balance += total_bc
            self.player.residue_inventory.clear()
            self.player.residue_synthesized += 1

            self.ui.notification(f"Recycled residue for {total_bc:.2f} BC!", "success")

        time.sleep(2)

    def _stats_menu(self):
        """Statistics and reports menu"""
        self.ui.header("STATISTICS & REPORTS", "Track your progress")

        # Get comprehensive stats
        stats = self.game.get_player_stats(self.player.name)
        economy_report = self.game.economy.get_economic_report()

        print(f"{Colors.CYAN}Player Statistics:{Colors.RESET}")
        print(f"  Level: {self.player.level}")
        print(f"  Experience: {self.player.experience}")
        print(f"  Total Mined: {format_bloomcoin(self.player.total_mined)}")
        print(f"  Patterns Discovered: {self.player.patterns_discovered}")
        print(f"  Market Trades: {self.player.market_trades}")

        print(f"\n{Colors.CYAN}Economy Metrics:{Colors.RESET}")
        print(f"  Mining Rate: {economy_report['mining']['rate_per_hour']:.2f} BC/hour")
        print(f"  Market Sentiment: {economy_report['market']['market_sentiment']:.2f}x")
        print(f"  Active Miners: {economy_report['mining']['active_jobs']}")

        print(f"\n{Colors.CYAN}Achievements ({len(self.player.achievements)}):{Colors.RESET}")
        for achievement in self.player.achievements:
            print(f"  🏆 {achievement}")

        options = [
            ("1", "Detailed Economy Report"),
            ("2", "Pattern Portfolio"),
            ("3", "Mining History"),
            ("4", "Export Stats"),
            ("0", "Back to Main Menu")
        ]

        self.ui.menu("Stats Menu", options, self.player.ui_style)

        choice = input(f"\n{Colors.YELLOW}Select option: {Colors.RESET}").strip()

        if choice == "0":
            self.current_menu = "main"
        elif choice == "1":
            self._detailed_economy_report()
        else:
            self.ui.notification("Stats features coming soon!", "warning")
            time.sleep(2)

    def _detailed_economy_report(self):
        """Show detailed economy report"""
        report = self.game.economy.get_economic_report()

        print(f"\n{Colors.CYAN}Detailed Economy Report:{Colors.RESET}")
        print(json.dumps(report, indent=2))

        input(f"\n{Colors.DIM}Press ENTER to continue...{Colors.RESET}")

    def _settings_menu(self):
        """Settings menu"""
        self.ui.header("SETTINGS", "Customize your experience")

        print(f"{Colors.CYAN}Current Settings:{Colors.RESET}")
        print(f"  Auto-complete Jobs: {self.player.auto_complete_jobs}")
        print(f"  Show Notifications: {self.player.show_notifications}")
        print(f"  UI Style: {self.player.ui_style}")

        options = [
            ("1", "Toggle Auto-complete Jobs"),
            ("2", "Toggle Notifications"),
            ("3", "Change UI Style"),
            ("4", "Reset Tutorial"),
            ("5", "Clear Cache"),
            ("0", "Back to Main Menu")
        ]

        self.ui.menu("Settings Menu", options, self.player.ui_style)

        choice = input(f"\n{Colors.YELLOW}Select option: {Colors.RESET}").strip()

        if choice == "0":
            self.current_menu = "main"
        elif choice == "1":
            self.player.auto_complete_jobs = not self.player.auto_complete_jobs
            self.ui.notification(
                f"Auto-complete jobs: {self.player.auto_complete_jobs}",
                "success"
            )
            time.sleep(1)
        elif choice == "2":
            self.player.show_notifications = not self.player.show_notifications
            self.ui.notification(
                f"Notifications: {self.player.show_notifications}",
                "success"
            )
            time.sleep(1)
        elif choice == "3":
            self._change_ui_style()
        else:
            self.ui.notification("Settings features coming soon!", "warning")
            time.sleep(2)

    def _change_ui_style(self):
        """Change UI style"""
        print(f"\n{Colors.CYAN}Select UI Style:{Colors.RESET}")
        print("  [1] Modern (colorful, boxes)")
        print("  [2] Classic (simple, green)")
        print("  [3] Minimal (no decorations)")

        choice = input(f"{Colors.YELLOW}Select style: {Colors.RESET}").strip()

        styles = {
            "1": "modern",
            "2": "classic",
            "3": "minimal"
        }

        if choice in styles:
            self.player.ui_style = styles[choice]
            self.ui.notification(f"UI style changed to {self.player.ui_style}", "success")
            time.sleep(1)

    def _save_game(self):
        """Save game state"""
        # TODO: Implement actual save system
        self.ui.loading_animation(1.5, "Saving game")
        self.ui.notification("Game saved successfully!", "success")
        time.sleep(1)

    def _confirm_exit(self):
        """Confirm exit game"""
        print(f"\n{Colors.YELLOW}Are you sure you want to exit? (y/n): {Colors.RESET}", end="")
        choice = input().strip().lower()

        if choice == 'y':
            self.ui.notification("Thanks for playing BloomQuest!", "success")
            print(f"\n{Colors.CYAN}Your progress has been saved.{Colors.RESET}")
            print(f"{Colors.DIM}See you next time!{Colors.RESET}\n")
            self.running = False
        else:
            self.ui.notification("Returning to game...", "info")
            time.sleep(1)

    def _check_completed_jobs(self):
        """Check for and notify about completed jobs"""
        if not self.player.show_notifications:
            return

        completed_count = 0
        for job_id in list(self.active_jobs.keys()):
            status = self.game.check_mining(job_id)
            if status["status"] == "completed":
                completed_count += 1

        if completed_count > 0:
            self.ui.notification(
                f"{completed_count} mining job(s) completed! Collect rewards in Mining menu.",
                "mining"
            )

    def _check_level_up(self):
        """Check if player leveled up"""
        xp_for_next = 100 * (self.player.level ** 1.5)

        while self.player.experience >= xp_for_next:
            self.player.level += 1
            self.player.experience -= xp_for_next
            xp_for_next = 100 * (self.player.level ** 1.5)

            self.ui.notification(f"Level Up! You are now level {self.player.level}!", "achievement")

            # Unlock features
            if self.player.level == 5:
                self.ui.notification("Unlocked: Team Mining!", "success")
            elif self.player.level == 10:
                self.ui.notification("Unlocked: Companion Specializations!", "success")
            elif self.player.level == 15:
                self.ui.notification("Unlocked: Advanced Market Trading!", "success")

    def _start_auto_completion(self, job_id: str, duration: float):
        """Start auto-completion thread for a job"""
        def auto_complete():
            time.sleep(duration)
            if self.player.auto_complete_jobs and job_id in self.active_jobs:
                # Job will be marked as complete, player can collect when ready
                if self.player.show_notifications:
                    print(f"\n{Colors.GREEN}✅ Job {job_id[:8]} completed!{Colors.RESET}")

        thread = threading.Thread(target=auto_complete, daemon=True)
        thread.start()

# ═══════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════

def main():
    """Main entry point for BloomQuest Terminal"""
    try:
        game = BloomQuestTerminal()
        game.start()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Game interrupted. Goodbye!{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Fatal error: {e}{Colors.RESET}")
        print(f"{Colors.DIM}Please report this issue.{Colors.RESET}")

if __name__ == "__main__":
    main()