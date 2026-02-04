#!/usr/bin/env python3
"""
BloomQuest MUD - Terminal Text Adventure
=========================================
A Multi-User Dungeon style text adventure with:
- AI Companions with personality and dialogue
- Card game battle mechanics
- Learning modules and puzzles
- Mining and farming integration
- Rich text-based world exploration
"""

import os
import sys
import time
import random
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

# Import game systems
from unified_mining_economy import UnifiedMiningEconomy
from companion_mining_ultimate import CompanionType, UltimateCompanionMiningManager
from guardian_decks_extended import get_complete_deck_library
from pattern_stock_market import PatternStockMarket

# Terminal colors for MUD experience
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # Standard colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BRIGHT_WHITE = '\033[97;1m'  # Bright white for special effects

    # Mood colors for companions
    HAPPY = '\033[92m'  # Green
    NEUTRAL = '\033[97m'  # White
    SAD = '\033[94m'  # Blue
    ANGRY = '\033[91m'  # Red
    EXCITED = '\033[93m'  # Yellow

@dataclass
class Location:
    """A location in the game world"""
    name: str
    description: str
    items: List[str]
    npcs: List[str]
    exits: Dict[str, str]
    ambient_text: List[str]
    learning_module: Optional[str] = None

class CompanionPersonality:
    """AI Companion with personality and dialogue"""

    def __init__(self, companion_type: CompanionType):
        self.type = companion_type
        self.name = companion_type.value[0]
        self.guardian = companion_type.value[1]
        self.mood = "neutral"
        self.relationship = 50  # 0-100 relationship score
        self.dialogue_history = []

        # Personality traits based on type
        self.traits = self._get_personality_traits()
        self.responses = self._load_dialogue_responses()

    def _get_personality_traits(self) -> Dict[str, Any]:
        """Get personality traits based on companion type"""
        traits = {
            CompanionType.ECHO: {
                "personality": "mysterious, reflective, wise",
                "speaking_style": "echoes thoughts, speaks in riddles",
                "interests": ["patterns", "resonance", "harmony"],
                "quirks": ["Sometimes repeats the last word spoken", "Hums when mining"],
                "favorite_activity": "pattern discovery"
            },
            CompanionType.GLITCH: {
                "personality": "chaotic, playful, unpredictable",
                "speaking_style": "g̸l̷i̶t̵c̸h̷y̶ text, random caps",
                "interests": ["chaos", "randomness", "breaking things"],
                "quirks": ["Text sometimes glitches", "Loves finding bugs"],
                "favorite_activity": "causing harmless chaos"
            },
            CompanionType.FLOW: {
                "personality": "calm, zen, peaceful",
                "speaking_style": "flowing sentences, poetic",
                "interests": ["water", "meditation", "balance"],
                "quirks": ["Speaks in haikus sometimes", "Very patient"],
                "favorite_activity": "meditation and farming"
            },
            CompanionType.SPARK: {
                "personality": "energetic, enthusiastic, bright",
                "speaking_style": "excited! lots of exclamation marks!",
                "interests": ["energy", "lightning", "speed"],
                "quirks": ["Very energetic speech", "Can't sit still"],
                "favorite_activity": "racing and quick mining"
            },
            CompanionType.SAGE: {
                "personality": "wise, knowledgeable, teacher",
                "speaking_style": "formal, educational, precise",
                "interests": ["knowledge", "teaching", "history"],
                "quirks": ["Loves sharing facts", "Quotes ancient texts"],
                "favorite_activity": "teaching and learning modules"
            },
            CompanionType.SCOUT: {
                "personality": "curious, adventurous, brave",
                "speaking_style": "descriptive, observant",
                "interests": ["exploration", "discovery", "maps"],
                "quirks": ["Always looking ahead", "Notices everything"],
                "favorite_activity": "exploring new areas"
            },
            CompanionType.NULL: {
                "personality": "mysterious, void, unknown",
                "speaking_style": "... silent... minimal...",
                "interests": ["void", "silence", "mystery"],
                "quirks": ["Rarely speaks", "Presence is felt more than heard"],
                "favorite_activity": "observing from shadows"
            }
        }
        return traits.get(self.type, traits[CompanionType.ECHO])

    def _load_dialogue_responses(self) -> Dict[str, List[str]]:
        """Load dialogue responses for different situations"""
        base_responses = {
            "greeting": [],
            "mining": [],
            "battle": [],
            "farming": [],
            "learning": [],
            "idle": [],
            "farewell": []
        }

        if self.type == CompanionType.ECHO:
            return {
                "greeting": [
                    "...hello... hello... *echoes softly*",
                    "Your presence creates ripples... ripples...",
                    "I hear your thoughts before you speak them..."
                ],
                "mining": [
                    "The crystals sing... can you hear them?",
                    "Each strike resonates through time...",
                    "Mining... mining... the echo grows stronger..."
                ],
                "battle": [
                    "Their patterns... I can see them clearly...",
                    "Let our resonance overwhelm them!",
                    "Echo and counter-echo... the dance begins..."
                ],
                "farming": [
                    "Seeds echo through generations...",
                    "Growth... decay... growth... the eternal echo...",
                    "The soil remembers what was planted before..."
                ],
                "learning": [
                    "Knowledge echoes through time...",
                    "What was learned before shall be learned again...",
                    "Listen... the answer was already spoken..."
                ],
                "idle": [
                    "*humming a haunting melody*",
                    "...waiting... waiting...",
                    "Do you hear that? Or is it just an echo?"
                ],
                "farewell": [
                    "Until we meet again... again... again...",
                    "Your echo remains even when you leave...",
                    "Goodbye... but never truly gone..."
                ]
            }
        elif self.type == CompanionType.GLITCH:
            return {
                "greeting": [
                    "H̸E̷Y̶ THERE! Ready to br͟e̸a̕k̷ some R̷U̵L̸E̶S̷?",
                    "oH hI! LeT's CaUsE sOmE cHaOs!",
                    "*screen flickers* D̸i̷d̶ you SEE that?!"
                ],
                "mining": [
                    "Mining.exe has st0pped w0rking... JUST KIDDING!",
                    "L̷e̶t̵'s BREAK these blocks! Literally!",
                    "Error 404: Ore not fou-- WAIT THERE IT IS!"
                ],
                "battle": [
                    "Time to GLITCH their reality!",
                    "C̸O̷M̶B̵O̸ BREAKER incoming!",
                    "Let's see them handle THIS randomness!"
                ],
                "farming": [
                    "What if we plant them UPSIDE DOWN?",
                    "G̸r̷o̶w̵t̸h̷.dll corrupted... in a GOOD way!",
                    "These crops are growing in IMPOSSIBLE directions!"
                ],
                "learning": [
                    "Learning? More like UNLEARNING the rules!",
                    "The answer is 42... or was it 24? WHO KNOWS!",
                    "Knowledge.overflow() exception handled BEAUTIFULLY!"
                ],
                "idle": [
                    "*random beeping noises*",
                    "BoReD... let's break something!",
                    "I found a bug! Want to exploit it?"
                ],
                "farewell": [
                    "SEGMENTATION FAULT... just kidding, see ya!",
                    "Goodbye.exe has crashed successfully!",
                    "C̸a̷t̶c̵h̸ you on the flip s̷i̶d̵e̸!"
                ]
            }
        elif self.type == CompanionType.SAGE:
            return {
                "greeting": [
                    "Greetings, young apprentice. Ready to expand your knowledge?",
                    "Ah, you've returned. The pursuit of wisdom continues.",
                    "Welcome. Today's lesson awaits."
                ],
                "mining": [
                    "Observe the crystalline structure. Each facet tells a story.",
                    "Mining teaches patience and persistence, valuable lessons both.",
                    "The ancients say: 'In the depths lie truth.'"
                ],
                "battle": [
                    "Strategy and knowledge shall prevail over brute force.",
                    "Remember your training. Mind over matter.",
                    "As Sun Tzu wrote: 'Know thyself, know thy enemy.'"
                ],
                "farming": [
                    "Agriculture: humanity's first great innovation.",
                    "Each seed contains infinite potential. Nurture it wisely.",
                    "The cycle of growth teaches us about life itself."
                ],
                "learning": [
                    "Excellent question! Let me elaborate...",
                    "Knowledge is power, but wisdom is knowing how to use it.",
                    "Every failure is a lesson in disguise."
                ],
                "idle": [
                    "*studying ancient texts*",
                    "Hmm... fascinating patterns in these equations...",
                    "Would you like to learn something new?"
                ],
                "farewell": [
                    "Remember what you've learned. Until next time.",
                    "May wisdom guide your path.",
                    "The lesson continues even in my absence."
                ]
            }
        # Add more personality responses for other types
        return base_responses

    def get_dialogue(self, context: str, player_relationship: int = None) -> str:
        """Get contextual dialogue based on mood and relationship"""
        if player_relationship:
            self.relationship = player_relationship

        responses = self.responses.get(context, self.responses["idle"])
        if not responses:
            return f"{self.name} remains silent."

        # Choose response based on mood and relationship
        response = random.choice(responses)

        # Add mood coloring
        mood_color = {
            "happy": Colors.HAPPY,
            "neutral": Colors.NEUTRAL,
            "sad": Colors.SAD,
            "angry": Colors.ANGRY,
            "excited": Colors.EXCITED
        }.get(self.mood, Colors.NEUTRAL)

        return f"{mood_color}{self.name}: {response}{Colors.RESET}"

    def react_to_card_play(self, card_name: str, success: bool) -> str:
        """React to a card being played in battle"""
        if success:
            if self.type == CompanionType.ECHO:
                return f"{self.name}: The resonance was perfect... perfect..."
            elif self.type == CompanionType.GLITCH:
                return f"{self.name}: CRITICAL HIT! Did you see those NUMBERS?!"
            elif self.type == CompanionType.SAGE:
                return f"{self.name}: Precisely as calculated. Well played."
        else:
            if self.type == CompanionType.ECHO:
                return f"{self.name}: The echo falters... falters..."
            elif self.type == CompanionType.GLITCH:
                return f"{self.name}: MISS.exe! Try again!"
            elif self.type == CompanionType.SAGE:
                return f"{self.name}: A learning opportunity. Adjust your strategy."
        return f"{self.name} watches intently."

class MUDWorld:
    """The game world with locations and navigation"""

    def __init__(self):
        self.locations = self._create_world()
        self.current_location = "mining_entrance"

    def _create_world(self) -> Dict[str, Location]:
        """Create the game world locations"""
        return {
            "mining_entrance": Location(
                name="Crystal Mine Entrance",
                description=f"""{Colors.CYAN}You stand at the entrance to the Crystal Mines.
                Ancient NEXTHASH-256 powered machinery hums with energy. Glowing crystals
                cast dancing shadows on the walls. Your companion stands ready beside you.{Colors.RESET}""",
                items=["rusty pickaxe", "mining helmet", "crystal shard"],
                npcs=["Old Miner Jenkins"],
                exits={"north": "deep_mines", "east": "farming_valley", "south": "town_square"},
                ambient_text=[
                    "You hear the distant sound of mining machinery.",
                    "A cool breeze flows from the mine depths.",
                    "Crystals pulse with soft light."
                ],
                learning_module="mining_basics"
            ),
            "deep_mines": Location(
                name="Deep Crystal Mines",
                description=f"""{Colors.MAGENTA}The mines extend deep into the earth. NEXTHASH-256
                algorithms pulse through the crystalline structures. You can sense valuable
                patterns hidden in the stone.{Colors.RESET}""",
                items=["echo crystal", "pattern fragment", "ancient gear"],
                npcs=["Crystal Guardian"],
                exits={"south": "mining_entrance", "down": "void_chamber"},
                ambient_text=[
                    "The crystals resonate with harmonic frequencies.",
                    "You feel the weight of the mountain above.",
                    "Something glimmers in the darkness."
                ],
                learning_module="advanced_mining"
            ),
            "farming_valley": Location(
                name="Quantum Farm Valley",
                description=f"""{Colors.GREEN}Rolling hills covered in quantum-enhanced crops
                stretch before you. The plants seem to exist in multiple states simultaneously.
                Your companion examines the unusual flora with interest.{Colors.RESET}""",
                items=["quantum seeds", "growth accelerator", "harvest scythe"],
                npcs=["Farmer Mae", "Quantum Botanist"],
                exits={"west": "mining_entrance", "north": "research_lab"},
                ambient_text=[
                    "The crops whisper secrets of growth and time.",
                    "A butterfly phases through multiple dimensions.",
                    "The soil pulses with life energy."
                ],
                learning_module="quantum_farming"
            ),
            "town_square": Location(
                name="BloomTown Square",
                description=f"""{Colors.YELLOW}The bustling center of BloomTown. Traders discuss
                pattern market prices while miners share tales of their discoveries. A large
                NEXTHASH monument stands in the center.{Colors.RESET}""",
                items=["town map", "merchant's note", "bloomcoin purse"],
                npcs=["Pattern Trader", "Town Crier", "Mysterious Stranger"],
                exits={"north": "mining_entrance", "east": "card_arena", "west": "companion_sanctuary"},
                ambient_text=[
                    "Merchants call out their wares.",
                    "Children play with holographic cards.",
                    "The monument hums with energy."
                ],
                learning_module="economics_basics"
            ),
            "card_arena": Location(
                name="Guardian Card Arena",
                description=f"""{Colors.RED}A grand arena where card battles take place.
                Holographic guardians materialize from played cards. Your companion eagerly
                anticipates testing their deck.{Colors.RESET}""",
                items=["practice deck", "arena rules", "champion's token"],
                npcs=["Arena Master", "Rookie Duelist", "Card Collector"],
                exits={"west": "town_square"},
                ambient_text=[
                    "Cards flutter through the air like butterflies.",
                    "Echoes of past battles resonate here.",
                    "A crowd cheers from the spectator stands."
                ],
                learning_module="card_battle_strategy"
            ),
            "companion_sanctuary": Location(
                name="Companion Sanctuary",
                description=f"""{Colors.MAGENTA}A peaceful sanctuary where companions rest
                and bond with their partners. Each companion type has their own special area.
                The air tingles with connection energy.{Colors.RESET}""",
                items=["bonding crystal", "companion treat", "memory album"],
                npcs=["Companion Keeper", "Bond Counselor"],
                exits={"east": "town_square"},
                ambient_text=[
                    "Companions play together happily.",
                    "You feel your bond growing stronger.",
                    "Peaceful energy fills the space."
                ],
                learning_module="companion_bonding"
            ),
            "research_lab": Location(
                name="Pattern Research Laboratory",
                description=f"""{Colors.BLUE}A high-tech facility where patterns are studied
                and new discoveries are made. Holographic displays show NEXTHASH-256
                calculations in real-time.{Colors.RESET}""",
                items=["research notes", "pattern analyzer", "lab keycard"],
                npcs=["Dr. Pattern", "Lab Assistant", "AI Terminal"],
                exits={"south": "farming_valley"},
                ambient_text=[
                    "Machines beep and whir with calculations.",
                    "A hologram flickers with pattern data.",
                    "The smell of ozone fills the air."
                ],
                learning_module="pattern_science"
            ),
            "void_chamber": Location(
                name="The Void Chamber",
                description=f"""{Colors.DIM}A place between places. Reality seems thin here.
                NULL companions feel at home in this mysterious space. Ancient secrets and
                forgotten knowledge drift through the darkness.{Colors.RESET}""",
                items=["void essence", "forgotten memory", "null stone"],
                npcs=["Void Keeper", "Lost Echo"],
                exits={"up": "deep_mines"},
                ambient_text=[
                    "...",
                    "You feel watched by unseen eyes.",
                    "Time moves strangely here."
                ],
                learning_module="void_mysteries"
            )
        }

    def get_current_location(self) -> Location:
        """Get the current location object"""
        return self.locations[self.current_location]

    def move(self, direction: str) -> tuple[bool, str]:
        """Move in a direction"""
        location = self.get_current_location()
        if direction in location.exits:
            self.current_location = location.exits[direction]
            new_location = self.get_current_location()
            return True, f"You move {direction} to {new_location.name}."
        return False, "You can't go that way."

class BloomQuestMUD:
    """Main MUD game engine"""

    def __init__(self):
        self.world = MUDWorld()
        self.economy = UnifiedMiningEconomy()

        # Create a mock ledger for the companion manager
        class MockLedger:
            def add_transaction(self, *args, **kwargs):
                return True
            def get_balance(self, address):
                return 1000.0

        self.companion_manager = UltimateCompanionMiningManager(MockLedger())
        self.market = PatternStockMarket()

        # Initialize quantum residue system
        self.quantum_enabled = False
        self.quantum_miner = None
        self.quantum_crypto = None
        self.lsb_encoder = None

        try:
            from quantum_residue_system import (
                BloomCoinQuantumMiner, QuantumNextHashCrypto,
                LSBQuantumEncoder, PHI, TAU, GAP, R_DARK, Z_C
            )
            self.quantum_miner = BloomCoinQuantumMiner()
            self.quantum_crypto = QuantumNextHashCrypto()
            self.lsb_encoder = LSBQuantumEncoder()
            self.quantum_enabled = True
            # Store constants as class attributes
            self.PHI = PHI
            self.TAU = TAU
            self.GAP = GAP
            self.R_DARK = R_DARK
            self.Z_C = Z_C
        except ImportError as e:
            # Set default values for constants
            self.PHI = 1.618033988749895
            self.TAU = 0.618033988749895
            self.GAP = 0.1459
            self.R_DARK = 5.854
            self.Z_C = 0.866

        # Player data
        self.player_name = ""
        self.player_level = 1
        self.balance = 1000.0
        self.inventory = []
        self.active_companion = None
        self.companion_personality = None
        self.card_deck = []

        # Game state
        self.in_combat = False
        self.learning_mode = False
        self.conversation_partner = None

    def start(self):
        """Start the MUD adventure"""
        self.clear_screen()
        self.show_intro()
        self.character_creation()
        self.main_game_loop()

    def clear_screen(self):
        """Clear the terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_intro(self):
        """Show game introduction"""
        print(f"""
{Colors.MAGENTA}═══════════════════════════════════════════════════════════════{Colors.RESET}
{Colors.CYAN}            BLOOMQUEST: The NEXTHASH Chronicles{Colors.RESET}
{Colors.MAGENTA}═══════════════════════════════════════════════════════════════{Colors.RESET}

{Colors.YELLOW}Welcome to a world where cryptocurrency mining meets magic,
where AI companions join you on adventures, and where card
battles determine the fate of digital realms.{Colors.RESET}

{Colors.GREEN}Features:{Colors.RESET}
  • Explore a rich text-based world
  • Bond with AI companions that have unique personalities
  • Engage in strategic card battles
  • Mine crystals using NEXTHASH-256 algorithms
  • Grow quantum crops on impossible farms
  • Learn through integrated educational modules
  • Trade patterns on the dynamic market

{Colors.MAGENTA}═══════════════════════════════════════════════════════════════{Colors.RESET}
        """)
        input(f"{Colors.CYAN}Press ENTER to begin your adventure...{Colors.RESET}")

    def character_creation(self):
        """Create player character and choose companion"""
        self.clear_screen()
        print(f"{Colors.YELLOW}CHARACTER CREATION{Colors.RESET}\n")

        # Get player name
        self.player_name = input(f"{Colors.CYAN}Enter your name, adventurer: {Colors.RESET}").strip()
        if not self.player_name:
            self.player_name = "Wanderer"

        print(f"\n{Colors.GREEN}Welcome, {self.player_name}!{Colors.RESET}\n")

        # Choose companion
        print(f"{Colors.YELLOW}Choose your AI companion:{Colors.RESET}\n")
        companions = [
            (CompanionType.ECHO, "Mysterious and wise, speaks in riddles"),
            (CompanionType.GLITCH, "Chaotic and playful, loves breaking rules"),
            (CompanionType.FLOW, "Calm and peaceful, speaks poetically"),
            (CompanionType.SPARK, "Energetic and enthusiastic, always excited"),
            (CompanionType.SAGE, "Knowledgeable teacher, loves sharing wisdom"),
            (CompanionType.SCOUT, "Curious explorer, notices everything"),
            (CompanionType.NULL, "Silent observer, mysterious presence")
        ]

        for i, (comp_type, desc) in enumerate(companions, 1):
            print(f"  {Colors.CYAN}[{i}]{Colors.RESET} {comp_type.value[0]} - {desc}")

        while True:
            try:
                choice = int(input(f"\n{Colors.YELLOW}Select companion (1-7): {Colors.RESET}"))
                if 1 <= choice <= 7:
                    chosen_type = companions[choice - 1][0]
                    self.active_companion = self.companion_manager.create_companion(
                        f"{chosen_type.value[0]}", chosen_type
                    )
                    self.companion_personality = CompanionPersonality(chosen_type)
                    break
            except:
                pass
            print(f"{Colors.RED}Please enter a number between 1 and 7{Colors.RESET}")

        # Initialize card deck based on companion
        self.initialize_deck()

        print(f"\n{self.companion_personality.get_dialogue('greeting')}")
        print(f"\n{Colors.GREEN}Your adventure begins at the Crystal Mine Entrance...{Colors.RESET}")
        input(f"\n{Colors.DIM}Press ENTER to continue...{Colors.RESET}")

    def initialize_deck(self):
        """Initialize player's card deck based on companion"""
        deck_library = get_complete_deck_library()
        guardian = self.active_companion.companion_type.value[1]

        if guardian in deck_library:
            self.card_deck = deck_library[guardian][:10]  # Start with 10 cards
        else:
            # Default deck if guardian not found
            self.card_deck = [
                {"name": "Echo Strike", "cost": 2, "damage": 3},
                {"name": "Resonance", "cost": 1, "effect": "draw"},
                {"name": "Crystal Shield", "cost": 3, "defense": 5}
            ]

    def main_game_loop(self):
        """Main game loop"""
        while True:
            self.clear_screen()
            self.display_status()
            self.display_location()
            self.display_companion_mood()

            # Get random ambient text occasionally
            if random.random() < 0.3:
                location = self.world.get_current_location()
                if location.ambient_text:
                    print(f"\n{Colors.DIM}{random.choice(location.ambient_text)}{Colors.RESET}")

            # Get player input
            command = input(f"\n{Colors.YELLOW}> {Colors.RESET}").strip().lower()

            if command == "quit" or command == "exit":
                self.quit_game()
                break
            else:
                self.process_command(command)

            input(f"\n{Colors.DIM}Press ENTER to continue...{Colors.RESET}")

    def display_status(self):
        """Display player status"""
        print(f"""
{Colors.GREEN}═══════════════════════════════════════════════════════════════{Colors.RESET}
  {Colors.YELLOW}Player:{Colors.RESET} {self.player_name} (Level {self.player_level})
  {Colors.CYAN}Balance:{Colors.RESET} {self.balance:.2f} BC
  {Colors.MAGENTA}Companion:{Colors.RESET} {self.companion_personality.name} ({self.companion_personality.guardian})
  {Colors.BLUE}Relationship:{Colors.RESET} {"❤" * (self.companion_personality.relationship // 20)}
  {Colors.GREEN}Cards in Deck:{Colors.RESET} {len(self.card_deck)}
{Colors.GREEN}═══════════════════════════════════════════════════════════════{Colors.RESET}""")

    def display_location(self):
        """Display current location"""
        location = self.world.get_current_location()
        print(f"\n{Colors.BOLD}{location.name}{Colors.RESET}")
        print(location.description)

        if location.items:
            print(f"\n{Colors.YELLOW}Items here:{Colors.RESET} {', '.join(location.items)}")

        if location.npcs:
            print(f"{Colors.CYAN}NPCs:{Colors.RESET} {', '.join(location.npcs)}")

        exits = ', '.join(location.exits.keys())
        print(f"{Colors.GREEN}Exits:{Colors.RESET} {exits}")

    def display_companion_mood(self):
        """Display companion's current mood"""
        idle_dialogue = self.companion_personality.get_dialogue("idle")
        if random.random() < 0.4:  # 40% chance companion says something
            print(f"\n{idle_dialogue}")

    def process_command(self, command: str):
        """Process player commands"""
        parts = command.split()
        if not parts:
            return

        action = parts[0]

        # Movement commands
        if action in ["north", "south", "east", "west", "up", "down", "n", "s", "e", "w"]:
            direction_map = {"n": "north", "s": "south", "e": "east", "w": "west"}
            direction = direction_map.get(action, action)
            success, message = self.world.move(direction)
            print(f"\n{message}")
            if success:
                self.companion_personality.mood = "excited"
                print(self.companion_personality.get_dialogue("idle"))

        # Game actions
        elif action == "mine":
            self.start_mining()
        elif action == "farm":
            self.start_farming()
        elif action == "battle" or action == "duel":
            self.start_card_battle()
        elif action == "talk":
            if len(parts) > 1:
                self.talk_to_npc(' '.join(parts[1:]))
            else:
                print(f"\n{Colors.YELLOW}Talk to whom?{Colors.RESET}")
        elif action == "learn":
            self.start_learning_module()
        elif action == "market":
            self.view_market()
        elif action == "inventory" or action == "inv":
            self.show_inventory()
        elif action == "deck":
            self.show_deck()
        elif action == "pet":
            self.pet_companion()
        elif action == "quantum":
            self.show_quantum_stats()
        elif action == "encrypt":
            if len(parts) > 1:
                self.encrypt_message(' '.join(parts[1:]))
            else:
                print(f"\n{Colors.YELLOW}Encrypt what message?{Colors.RESET}")
        elif action == "residue":
            self.check_residue_balance()
        elif action == "help":
            self.show_help()
        else:
            print(f"\n{Colors.RED}Unknown command. Type 'help' for commands.{Colors.RESET}")

    def start_mining(self):
        """Start a mining session with quantum residue"""
        print(f"\n{Colors.CYAN}Starting NEXTHASH-256 mining with quantum residue...{Colors.RESET}")
        print(self.companion_personality.get_dialogue("mining"))

        if self.quantum_enabled and self.quantum_miner:
            # Mine with quantum residue system
            print(f"{Colors.MAGENTA}Quantum coherence initializing...{Colors.RESET}")

            block = self.quantum_miner.mine_block(self.player_name, difficulty=3)

            visible_reward = block['reward']['visible']
            dark_residue = block['reward']['residue']
            coherence = block['quantum_state']['coherence']
            regime = block['quantum_state']['regime']

            # Add visible coins to balance
            self.balance += visible_reward

            # Display results with color coding based on regime
            if regime == "incoherent":
                regime_color = Colors.RED
            elif regime == "glassy":
                regime_color = Colors.YELLOW
            elif regime == "synchronized":
                regime_color = Colors.GREEN
            else:
                regime_color = Colors.CYAN

            print(f"\n{Colors.GREEN}Mining successful!{Colors.RESET}")
            print(f"  Hash: {block['hash'][:32]}...")
            print(f"  {Colors.GREEN}Visible coins: {visible_reward:.4f} BC{Colors.RESET}")
            print(f"  {Colors.MAGENTA}Dark residue: {dark_residue:.4f} BC (unspendable){Colors.RESET}")
            print(f"  {regime_color}Quantum regime: {regime}{Colors.RESET}")
            print(f"  Coherence: {coherence:.4f} (target: {self.Z_C:.4f})")
            print(f"  Dark/visible ratio: {block['quantum_state']['dark_ratio']:.2f} (theory: {self.R_DARK:.2f})")

            # Special dialogue based on coherence
            if coherence < self.TAU:
                print(f"\n{Colors.DIM}The quantum field remains incoherent... vast residue accumulates...{Colors.RESET}")
            elif coherence > self.Z_C:
                print(f"\n{Colors.BRIGHT_WHITE}Perfect synchronization achieved! Maximum extraction!{Colors.RESET}")
                self.companion_personality.mood = "excited"
                self.companion_personality.relationship += 5
            else:
                self.companion_personality.mood = "happy"
                self.companion_personality.relationship += 2

        else:
            # Fallback to standard mining
            result = self.active_companion.mine_with_nexthash(difficulty=3)
            if result['success']:
                reward = random.uniform(10, 50)
                self.balance += reward
                print(f"\n{Colors.GREEN}Mining successful! Earned {reward:.2f} BC{Colors.RESET}")
                print(f"Hash: {result['hash'][:32]}...")

                self.companion_personality.mood = "happy"
                self.companion_personality.relationship += 2
            else:
                print(f"\n{Colors.YELLOW}Mining continues...{Colors.RESET}")

    def start_farming(self):
        """Start a farming session"""
        if self.world.current_location != "farming_valley":
            print(f"\n{Colors.YELLOW}You need to be at the Farming Valley to farm!{Colors.RESET}")
            return

        print(f"\n{Colors.GREEN}Planting quantum seeds...{Colors.RESET}")
        print(self.companion_personality.get_dialogue("farming"))

        # Simulate farming
        growth_time = random.randint(3, 8)
        print(f"Seeds planted! They'll grow in {growth_time} seconds...")
        time.sleep(2)  # Shortened for demo

        harvest = random.uniform(5, 25)
        self.balance += harvest
        print(f"\n{Colors.GREEN}Harvest complete! Earned {harvest:.2f} BC{Colors.RESET}")

        self.companion_personality.mood = "happy"
        self.companion_personality.relationship += 1

    def start_card_battle(self):
        """Start a card battle"""
        if self.world.current_location != "card_arena":
            print(f"\n{Colors.YELLOW}You need to be at the Card Arena for battles!{Colors.RESET}")
            return

        print(f"\n{Colors.RED}CARD BATTLE INITIATED!{Colors.RESET}")
        print(self.companion_personality.get_dialogue("battle"))

        # Simple card battle simulation
        print(f"\n{Colors.CYAN}Your hand:{Colors.RESET}")
        hand = random.sample(self.card_deck, min(3, len(self.card_deck)))
        for i, card in enumerate(hand, 1):
            print(f"  [{i}] {card['name']} (Cost: {card.get('cost', 1)})")

        choice = input(f"\n{Colors.YELLOW}Choose a card to play (1-{len(hand)}): {Colors.RESET}")

        try:
            card_index = int(choice) - 1
            if 0 <= card_index < len(hand):
                played_card = hand[card_index]
                print(f"\n{Colors.GREEN}You play {played_card['name']}!{Colors.RESET}")

                # Simulate battle outcome
                success = random.random() < 0.6
                print(self.companion_personality.react_to_card_play(played_card['name'], success))

                if success:
                    reward = random.uniform(20, 80)
                    self.balance += reward
                    print(f"\n{Colors.GREEN}Victory! Earned {reward:.2f} BC{Colors.RESET}")
                    self.companion_personality.mood = "excited"
                    self.companion_personality.relationship += 3
                else:
                    print(f"\n{Colors.YELLOW}Defeated! Try again.{Colors.RESET}")
                    self.companion_personality.mood = "sad"
        except:
            print(f"\n{Colors.RED}Invalid choice{Colors.RESET}")

    def talk_to_npc(self, npc_name: str):
        """Talk to an NPC"""
        location = self.world.get_current_location()

        # Find NPC in current location
        matching_npc = None
        for npc in location.npcs:
            if npc_name.lower() in npc.lower():
                matching_npc = npc
                break

        if not matching_npc:
            print(f"\n{Colors.YELLOW}There's no one here by that name.{Colors.RESET}")
            return

        print(f"\n{Colors.CYAN}You approach {matching_npc}...{Colors.RESET}")

        # Generate contextual dialogue
        dialogues = {
            "Old Miner Jenkins": [
                "These mines have been here longer than memory itself.",
                "Your companion seems strong. They'll serve you well.",
                "Find the patterns in the crystal, and wealth will follow."
            ],
            "Pattern Trader": [
                f"Current ECHO pattern price: {random.uniform(80, 120):.2f} BC",
                "Buy low, sell high - but patterns have their own rhythm.",
                "Your companion might sense valuable patterns others miss."
            ],
            "Dr. Pattern": [
                "NEXTHASH-256 is more than an algorithm - it's a philosophy.",
                "Each companion type resonates with different patterns.",
                "Have you tried combining patterns? The results are... interesting."
            ]
        }

        npc_dialogue = dialogues.get(matching_npc, [
            f"{matching_npc} nods at you politely.",
            f"{matching_npc} seems busy right now.",
            f"{matching_npc} smiles warmly."
        ])

        print(f"\n{Colors.WHITE}{matching_npc}: {random.choice(npc_dialogue)}{Colors.RESET}")

        # Companion might comment
        if random.random() < 0.5:
            print(f"\n{self.companion_personality.get_dialogue('idle')}")

    def start_learning_module(self):
        """Start a learning module for the current location"""
        location = self.world.get_current_location()

        if not location.learning_module:
            print(f"\n{Colors.YELLOW}No learning module available here.{Colors.RESET}")
            return

        print(f"\n{Colors.MAGENTA}LEARNING MODULE: {location.learning_module}{Colors.RESET}")
        print(self.companion_personality.get_dialogue("learning"))

        # Present a simple puzzle or question
        modules = {
            "mining_basics": {
                "question": "What is the key innovation of NEXTHASH-256?",
                "options": [
                    "A) Faster processing",
                    "B) 50% bit avalanche in 1 round",
                    "C) Lower energy usage"
                ],
                "answer": "B",
                "explanation": "NEXTHASH-256 achieves 50% bit avalanche in just 1 round, compared to SHA-256's 4 rounds."
            },
            "quantum_farming": {
                "question": "How do quantum crops exist?",
                "options": [
                    "A) In multiple states simultaneously",
                    "B) Only at night",
                    "C) Underground"
                ],
                "answer": "A",
                "explanation": "Quantum superposition allows crops to exist in multiple growth states until observed."
            }
        }

        module = modules.get(location.learning_module, modules["mining_basics"])

        print(f"\n{Colors.CYAN}Question: {module['question']}{Colors.RESET}")
        for option in module['options']:
            print(f"  {option}")

        answer = input(f"\n{Colors.YELLOW}Your answer: {Colors.RESET}").strip().upper()

        if answer == module['answer']:
            print(f"\n{Colors.GREEN}Correct!{Colors.RESET}")
            print(module['explanation'])

            # Reward for learning
            reward = 25
            self.balance += reward
            self.player_level += 0.1
            print(f"\n{Colors.GREEN}Earned {reward} BC and experience!{Colors.RESET}")

            # Sage companions especially love learning
            if self.companion_personality.type == CompanionType.SAGE:
                self.companion_personality.mood = "excited"
                self.companion_personality.relationship += 5
                print(f"\n{Colors.YELLOW}{self.companion_personality.name} is thrilled by your knowledge!{Colors.RESET}")
        else:
            print(f"\n{Colors.YELLOW}Not quite. {module['explanation']}{Colors.RESET}")

    def pet_companion(self):
        """Pet your companion to increase bond"""
        print(f"\n{Colors.MAGENTA}You gently pet {self.companion_personality.name}...{Colors.RESET}")

        self.companion_personality.mood = "happy"
        self.companion_personality.relationship = min(100, self.companion_personality.relationship + 5)

        # Different companions react differently
        if self.companion_personality.type == CompanionType.NULL:
            print(f"{Colors.DIM}...a faint warmth emanates from the void...{Colors.RESET}")
        elif self.companion_personality.type == CompanionType.SPARK:
            print(f"{Colors.YELLOW}{self.companion_personality.name}: *SPARKS WITH JOY* YES YES YES!{Colors.RESET}")
        elif self.companion_personality.type == CompanionType.FLOW:
            print(f"{Colors.BLUE}{self.companion_personality.name}: *purrs like flowing water*{Colors.RESET}")
        else:
            happy_response = self.companion_personality.get_dialogue("idle")
            print(happy_response)

        print(f"\n{Colors.GREEN}Bond increased! Relationship: {self.companion_personality.relationship}/100{Colors.RESET}")

    def view_market(self):
        """View pattern market prices"""
        print(f"\n{Colors.CYAN}PATTERN MARKET{Colors.RESET}")
        print(f"{Colors.DIM}{'='*50}{Colors.RESET}")

        # Get some market data
        patterns = ["ECHO", "GLITCH", "FLOW", "SPARK"]
        for pattern in patterns:
            price = random.uniform(50, 200)
            change = random.uniform(-10, 10)
            color = Colors.GREEN if change > 0 else Colors.RED
            print(f"{pattern:12} {price:8.2f} BC  {color}{change:+6.2f}%{Colors.RESET}")

        print(f"{Colors.DIM}{'='*50}{Colors.RESET}")

    def show_inventory(self):
        """Show player inventory"""
        print(f"\n{Colors.YELLOW}INVENTORY{Colors.RESET}")
        if self.inventory:
            for item in self.inventory:
                print(f"  • {item}")
        else:
            print("  Your inventory is empty")

    def show_deck(self):
        """Show card deck"""
        print(f"\n{Colors.MAGENTA}CARD DECK ({len(self.card_deck)} cards){Colors.RESET}")
        for card in self.card_deck[:5]:  # Show first 5 cards
            print(f"  • {card['name']}")
        if len(self.card_deck) > 5:
            print(f"  ... and {len(self.card_deck) - 5} more")

    def show_quantum_stats(self):
        """Display quantum residue statistics"""
        if not self.quantum_enabled:
            print(f"\n{Colors.YELLOW}Quantum system not available{Colors.RESET}")
            return

        print(f"\n{Colors.MAGENTA}QUANTUM RESIDUE STATISTICS{Colors.RESET}")
        print(f"{Colors.DIM}{'='*50}{Colors.RESET}")

        # Constants
        print(f"\n{Colors.CYAN}Fundamental Constants:{Colors.RESET}")
        print(f"  φ (golden ratio)       = {self.PHI:.6f}")
        print(f"  τ (golden inverse)     = {self.TAU:.6f}")
        print(f"  gap (void residue)     = {self.GAP:.6f}")
        print(f"  z_c (critical lens)    = {self.Z_C:.6f}")
        print(f"  R (dark/visible ratio) = {self.R_DARK:.6f}")

        # Mining stats
        if self.quantum_miner:
            verification = self.quantum_miner.verify_projection_residue_ratio()
            print(f"\n{Colors.YELLOW}Mining Performance:{Colors.RESET}")
            print(f"  Blocks mined:     {self.quantum_miner.blocks_mined}")
            print(f"  Visible coins:    {self.quantum_miner.total_visible_coins:.4f} BC")
            print(f"  Dark residue:     {self.quantum_miner.total_dark_residue:.4f} BC")

            if verification.get('observed_ratio'):
                print(f"\n{Colors.GREEN}Convergence to Theory:{Colors.RESET}")
                print(f"  Observed ratio:   {verification['observed_ratio']:.4f}")
                print(f"  Theoretical:      {verification['theoretical_ratio']:.4f}")
                print(f"  Convergence:      {verification['convergence']*100:.1f}%")

        # Current coherence
        if self.quantum_miner and hasattr(self.quantum_miner.residue_engine, 'phases'):
            r, q = self.quantum_miner.residue_engine.compute_order_parameters()
            w = self.quantum_miner.residue_engine.compute_winding_number()

            print(f"\n{Colors.BLUE}Current Quantum State:{Colors.RESET}")
            print(f"  Coherence (r):    {r:.4f}")
            print(f"  Persistence (q):  {q:.4f}")
            print(f"  Winding number:   {w}")

            # Regime indicator
            if r < self.TAU:
                print(f"  Regime:          {Colors.RED}INCOHERENT{Colors.RESET}")
            elif r < self.Z_C:
                print(f"  Regime:          {Colors.YELLOW}GLASSY{Colors.RESET}")
            else:
                print(f"  Regime:          {Colors.GREEN}SYNCHRONIZED{Colors.RESET}")

        print(f"{Colors.DIM}{'='*50}{Colors.RESET}")

    def check_residue_balance(self):
        """Check dark residue balance"""
        if not self.quantum_enabled:
            print(f"\n{Colors.YELLOW}Quantum system not available{Colors.RESET}")
            return

        if self.quantum_miner:
            visible = self.quantum_miner.total_visible_coins
            dark = self.quantum_miner.total_dark_residue
            total = visible + dark

            print(f"\n{Colors.MAGENTA}RESIDUE BALANCE{Colors.RESET}")
            print(f"  {Colors.GREEN}Visible (spendable):  {visible:.4f} BC ({visible/max(total, 1)*100:.1f}%){Colors.RESET}")
            print(f"  {Colors.DIM}Dark (unspendable):   {dark:.4f} BC ({dark/max(total, 1)*100:.1f}%){Colors.RESET}")
            print(f"  Total energy:         {total:.4f} BC")

            # Projection residue cosmology quote
            if dark > visible * 5:
                print(f"\n{Colors.DIM}\"Dark matter is not missing mass but unresolved projection...\"{Colors.RESET}")
        else:
            print(f"\n{Colors.YELLOW}No residue data available yet. Mine first!{Colors.RESET}")

    def encrypt_message(self, message: str):
        """Encrypt a message using quantum residue"""
        if not self.quantum_enabled:
            print(f"\n{Colors.YELLOW}Quantum encryption not available{Colors.RESET}")
            return

        print(f"\n{Colors.CYAN}QUANTUM ENCRYPTION{Colors.RESET}")
        password = f"{self.player_name}_{self.companion_personality.name}_{time.time()}"

        # Encrypt with quantum residue
        encrypted = self.quantum_crypto.encrypt_with_residue(message.encode(), password)

        print(f"  Original: {message}")
        print(f"  Encrypted: {encrypted['ciphertext'][:64]}...")
        print(f"  Auth tag: {encrypted['auth_tag'][:32]}...")
        print(f"  Coherence used: {encrypted['coherence']:.4f}")
        print(f"  Dark ratio: {encrypted['dark_ratio']:.4f}")

        # Companion comments on encryption
        if self.companion_personality.type == CompanionType.NULL:
            print(f"\n{Colors.DIM}...encrypted in the void...{Colors.RESET}")
        elif self.companion_personality.type == CompanionType.GLITCH:
            print(f"\n{self.companion_personality.name}: Good luck D̸E̷C̵R̸Y̶P̷T̸I̶N̵G̸ that!")
        else:
            print(f"\n{self.companion_personality.name}: Message secured with quantum residue.")

        # Store for later decryption (in real game, this would be saved)
        self.last_encrypted = {
            'data': encrypted,
            'password': password,
            'message': message
        }

    def show_help(self):
        """Show help commands"""
        print(f"""
{Colors.CYAN}COMMANDS:{Colors.RESET}
  Movement: north, south, east, west, up, down (or n,s,e,w)
  Actions:  mine, farm, battle, talk [npc], learn, market
  Info:     inventory, deck, pet, help
  Quantum:  quantum, residue, encrypt [message]
  System:   quit, exit

{Colors.YELLOW}TIPS:{Colors.RESET}
  • Talk to NPCs for quests and information
  • Pet your companion to increase your bond
  • Each location has unique activities
  • Learning modules reward knowledge with BC
  • Your companion's personality affects gameplay
  • Quantum residue follows φ⁴ - 1 = 5.854 ratio
        """)

    def quit_game(self):
        """Quit the game"""
        print(f"\n{self.companion_personality.get_dialogue('farewell')}")
        print(f"\n{Colors.GREEN}Thanks for playing BloomQuest MUD!{Colors.RESET}")
        print(f"Final balance: {self.balance:.2f} BC")
        print(f"Level reached: {self.player_level:.1f}")
        print(f"Companion bond: {self.companion_personality.relationship}/100")

def main():
    """Main entry point"""
    try:
        game = BloomQuestMUD()
        game.start()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Adventure interrupted!{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}An error occurred: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()