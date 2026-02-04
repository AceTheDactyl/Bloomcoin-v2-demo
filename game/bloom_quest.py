#!/usr/bin/env python3
"""
BloomQuest: A Text-Based Adventure Game with BloomCoin Economy
================================================================
An immersive narrative-driven game where players navigate through
spectral corridors, achieve coherence with mathematical harmony,
and earn bloomcoin through meaningful interactions.

Core Mechanics:
- Bloomcoin as primary currency
- Narrative archetypes drive story progression
- Learning algorithms adapt to player choices
- Kuramoto oscillators determine success/failure
- Golden ratio governs all rewards
"""

import os
import sys
import json
import time
import random
import hashlib
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent / "bloomcoin-v0.1.0" / "bloomcoin"))

# Import bloomcoin components
from bloomcoin.constants import PHI, Z_C, K, L4
from bloomcoin.wallet.wallet import Wallet
from garden.garden_system import GardenSystem
from garden.agents.agent import AIAgent, AgentPersonality, AgentState
from garden.bloom_events.bloom_event import BloomEvent, BloomEventType
from garden.gradient_schema.archetypes import Archetype
from garden.gradient_schema.corridors import SpectralCorridor
from garden.consensus.kuramoto import KuramotoOscillator

# Game Constants (all derived from φ)
BASE_HEALTH = int(PHI * 61.8)  # ~100
BASE_ENERGY = int(PHI * 30.9)  # ~50
BASE_COINS = int(PHI * 6.18)   # ~10
COHERENCE_THRESHOLD = Z_C      # 0.866 (critical coherence)
REWARD_MULTIPLIER = PHI        # 1.618
DIFFICULTY_SCALING = 1 / PHI   # 0.618

class GameState(Enum):
    """Game state machine"""
    MENU = "menu"
    EXPLORING = "exploring"
    DIALOGUE = "dialogue"
    COMBAT = "combat"
    TRADING = "trading"
    RESTING = "resting"
    QUEST = "quest"
    DEATH = "death"
    VICTORY = "victory"

class LocationType(Enum):
    """Types of locations in the game world"""
    NEXUS = "nexus"          # Central hub
    CORRIDOR = "corridor"     # Spectral corridor (narrative path)
    CHAMBER = "chamber"       # Rest/save point
    MARKET = "market"        # Trading post
    ORACLE = "oracle"        # Knowledge/quest giver
    VOID = "void"           # Dangerous area
    GARDEN = "garden"       # Peaceful/healing area
    THRESHOLD = "threshold"  # Boss/challenge area

@dataclass
class PlayerCharacter:
    """The player's avatar in the game world"""
    name: str
    archetype: Archetype
    health: float = BASE_HEALTH
    energy: float = BASE_ENERGY
    coherence: float = 0.5  # Start at neutral coherence
    oscillator: KuramotoOscillator = field(default_factory=lambda: KuramotoOscillator())
    wallet: Optional[Wallet] = None
    inventory: Dict[str, int] = field(default_factory=dict)
    skills: Dict[str, float] = field(default_factory=dict)
    knowledge: List[str] = field(default_factory=list)
    current_corridor: Optional[SpectralCorridor] = None
    position: int = 0  # Position along current corridor
    experience: float = 0.0
    level: int = 1

    def __post_init__(self):
        """Initialize wallet and base skills"""
        if not self.wallet:
            self.wallet = Wallet()

        # Initialize base skills from archetype
        self.skills = {
            "perception": PHI * 0.5,
            "resonance": PHI * 0.5,
            "synthesis": PHI * 0.5,
            "navigation": PHI * 0.5
        }

        # Archetype bonuses
        archetype_bonuses = {
            Archetype.QUEST: {"navigation": PHI},
            Archetype.INSIGHT: {"perception": PHI},
            Archetype.EMERGENCE: {"synthesis": PHI},
            Archetype.DESCENT: {"resonance": PHI}
        }

        if self.archetype in archetype_bonuses:
            for skill, bonus in archetype_bonuses[self.archetype].items():
                self.skills[skill] *= bonus

@dataclass
class Location:
    """A location in the game world"""
    name: str
    type: LocationType
    description: str
    corridor: Optional[SpectralCorridor] = None
    npcs: List[AIAgent] = field(default_factory=list)
    items: Dict[str, int] = field(default_factory=dict)
    exits: Dict[str, str] = field(default_factory=dict)  # direction: location_name
    coherence_requirement: float = 0.0
    danger_level: float = 0.0

class NarrativeEngine:
    """Manages story progression and narrative coherence"""

    def __init__(self, garden_system: GardenSystem):
        self.garden = garden_system
        self.current_act = 1
        self.story_beats: List[str] = []
        self.player_choices: List[Tuple[str, str]] = []
        self.narrative_coherence = 0.5

    def generate_narrative(self, player: PlayerCharacter, location: Location) -> str:
        """Generate contextual narrative based on player state and location"""

        # Calculate narrative resonance
        resonance = self._calculate_resonance(player, location)

        # Generate appropriate narrative beat
        if location.type == LocationType.NEXUS:
            return self._nexus_narrative(player, resonance)
        elif location.type == LocationType.CORRIDOR:
            return self._corridor_narrative(player, location, resonance)
        elif location.type == LocationType.ORACLE:
            return self._oracle_narrative(player, resonance)
        elif location.type == LocationType.VOID:
            return self._void_narrative(player, resonance)
        else:
            return self._default_narrative(location, resonance)

    def _calculate_resonance(self, player: PlayerCharacter, location: Location) -> float:
        """Calculate narrative resonance between player and location"""
        base_resonance = player.coherence

        # Archetype alignment bonus
        if location.corridor and player.current_corridor == location.corridor:
            base_resonance *= PHI

        # Skill-based modifiers
        perception_mod = player.skills.get("perception", 1.0) / 10
        resonance_mod = player.skills.get("resonance", 1.0) / 10

        total_resonance = base_resonance * (1 + perception_mod + resonance_mod)
        return min(1.0, total_resonance)

    def _nexus_narrative(self, player: PlayerCharacter, resonance: float) -> str:
        """Generate narrative for the central hub"""
        if resonance > COHERENCE_THRESHOLD:
            return f"""
The Nexus pulses with golden light, its crystalline structures resonating
with your presence. The convergence of all spectral corridors creates a
symphony of possibilities. Your coherence with this space is remarkable.

Current Coherence: {player.coherence:.3f}
Archetype Resonance: {player.archetype.name}
"""
        else:
            return f"""
The Nexus feels distant, its harmonies just beyond your grasp. The corridors
spiral outward like a mandala, each path a different color of possibility.
You must increase your coherence to fully perceive this space.

Current Coherence: {player.coherence:.3f}
Required: {COHERENCE_THRESHOLD:.3f}
"""

    def _corridor_narrative(self, player: PlayerCharacter, location: Location,
                           resonance: float) -> str:
        """Generate narrative for spectral corridors"""
        corridor = location.corridor
        if not corridor:
            return "The corridor stretches before you, its nature unclear."

        progress = player.position / 7.0  # 7 steps per corridor
        color_shift = corridor.calculate_color_shift(progress)

        return f"""
You traverse the {corridor.name}, bathed in {corridor.primary_color} light.
The path shifts and transforms as you move, each step a new revelation.

Progress: {'█' * int(progress * 10) + '░' * (10 - int(progress * 10))}
Hue Shift: {color_shift:.1f}°
Resonance: {resonance:.3f}
"""

    def _oracle_narrative(self, player: PlayerCharacter, resonance: float) -> str:
        """Generate narrative for oracle encounters"""
        if resonance > COHERENCE_THRESHOLD:
            wisdom = random.choice([
                "The golden ratio spirals through all things.",
                "Coherence is not achieved, but discovered.",
                "Each choice branches the crystal ledger.",
                "The garden remembers what the mind forgets."
            ])
            return f"""
The Oracle's eyes gleam with fractal patterns. She speaks:
"{wisdom}"

Your understanding deepens. (+{PHI:.3f} perception)
"""
        else:
            return """
The Oracle remains silent, her form shifting like smoke.
You lack the coherence to comprehend her wisdom.
"""

    def _void_narrative(self, player: PlayerCharacter, resonance: float) -> str:
        """Generate narrative for dangerous void areas"""
        danger_text = "The void yawns before you, "
        if resonance < 0.3:
            danger_text += "hungry and absolute. Your oscillations falter."
        elif resonance < 0.6:
            danger_text += "testing your coherence with each breath."
        else:
            danger_text += "but your harmony creates a path through chaos."

        return f"""
{danger_text}

Danger Level: {'🔥' * int(5 * (1 - resonance))}
Energy Drain: -{(1 - resonance) * 5:.1f}/turn
"""

    def _default_narrative(self, location: Location, resonance: float) -> str:
        """Default narrative generation"""
        return f"""
{location.description}

Resonance: {resonance:.3f}
Exits: {', '.join(location.exits.keys())}
"""

class EconomyManager:
    """Manages the bloomcoin-based game economy"""

    def __init__(self):
        self.market_prices: Dict[str, float] = {}
        self.inflation_rate = 1.0
        self.transaction_history: List[Dict] = []
        self._initialize_market()

    def _initialize_market(self):
        """Set initial market prices based on golden ratio"""
        self.market_prices = {
            "health_potion": PHI * 5,
            "energy_crystal": PHI * 3,
            "coherence_shard": PHI * 10,
            "navigation_compass": PHI * 15,
            "resonance_tuner": PHI * 8,
            "void_anchor": PHI * 20,
            "wisdom_scroll": PHI * 12,
            "garden_seed": PHI * 7
        }

    def calculate_reward(self, event: BloomEvent, player: PlayerCharacter) -> float:
        """Calculate bloomcoin reward for an event"""
        base_reward = PHI ** event.significance

        # Apply coherence multiplier
        coherence_mult = 1 + (player.coherence - 0.5) * 2

        # Apply level scaling
        level_mult = 1 + (player.level - 1) * DIFFICULTY_SCALING

        # Apply archetype bonus if aligned
        archetype_mult = 1.0
        if event.archetype == player.archetype:
            archetype_mult = PHI

        total_reward = base_reward * coherence_mult * level_mult * archetype_mult
        return round(total_reward, 3)

    def process_transaction(self, player: PlayerCharacter, item: str,
                          action: str = "buy") -> bool:
        """Process a buy/sell transaction"""
        if item not in self.market_prices:
            return False

        price = self.market_prices[item] * self.inflation_rate

        if action == "buy":
            if player.wallet.balance >= price:
                player.wallet.balance -= price
                player.inventory[item] = player.inventory.get(item, 0) + 1
                self._update_market(item, "buy")
                return True
        elif action == "sell":
            if player.inventory.get(item, 0) > 0:
                player.wallet.balance += price * DIFFICULTY_SCALING  # Sell for less
                player.inventory[item] -= 1
                self._update_market(item, "sell")
                return True

        return False

    def _update_market(self, item: str, action: str):
        """Update market prices based on supply/demand"""
        if action == "buy":
            # Increase price slightly when bought
            self.market_prices[item] *= (1 + 1/PHI/100)
        else:
            # Decrease price slightly when sold
            self.market_prices[item] *= (1 - 1/PHI/100)

        # Record transaction
        self.transaction_history.append({
            "item": item,
            "action": action,
            "price": self.market_prices[item],
            "timestamp": datetime.now()
        })

class LearningSystem:
    """Adaptive learning system that evolves with player behavior"""

    def __init__(self):
        self.player_model: Dict[str, float] = {}
        self.difficulty_curve = 0.5
        self.adaptation_rate = 1 / PHI
        self.pattern_memory: List[Dict] = []

    def observe_action(self, player: PlayerCharacter, action: str,
                       success: bool, context: Dict):
        """Observe and learn from player actions"""

        # Update player model
        action_key = f"action_{action}"
        current_weight = self.player_model.get(action_key, 0.5)

        # Adjust weight based on success
        if success:
            new_weight = current_weight + self.adaptation_rate * (1 - current_weight)
        else:
            new_weight = current_weight - self.adaptation_rate * current_weight

        self.player_model[action_key] = new_weight

        # Store pattern for future reference
        self.pattern_memory.append({
            "action": action,
            "success": success,
            "coherence": player.coherence,
            "context": context,
            "timestamp": time.time()
        })

        # Adjust difficulty curve
        self._adjust_difficulty(success)

    def predict_action(self, player: PlayerCharacter,
                      available_actions: List[str]) -> str:
        """Predict most likely player action"""

        action_scores = {}
        for action in available_actions:
            action_key = f"action_{action}"
            base_score = self.player_model.get(action_key, 0.5)

            # Apply archetype preferences
            archetype_bonus = self._get_archetype_preference(
                player.archetype, action)

            action_scores[action] = base_score * archetype_bonus

        # Return action with highest score
        return max(action_scores, key=action_scores.get)

    def _adjust_difficulty(self, success: bool):
        """Dynamically adjust game difficulty"""
        if success:
            self.difficulty_curve = min(1.0,
                self.difficulty_curve + self.adaptation_rate * 0.1)
        else:
            self.difficulty_curve = max(0.1,
                self.difficulty_curve - self.adaptation_rate * 0.1)

    def _get_archetype_preference(self, archetype: Archetype,
                                 action: str) -> float:
        """Get archetype-specific action preferences"""
        preferences = {
            Archetype.QUEST: {"explore": PHI, "fight": 1.2, "trade": 0.8},
            Archetype.INSIGHT: {"examine": PHI, "talk": 1.3, "meditate": 1.5},
            Archetype.EMERGENCE: {"create": PHI, "combine": 1.4, "transform": 1.3},
            Archetype.DESCENT: {"delve": PHI, "absorb": 1.3, "sacrifice": 1.2}
        }

        arch_prefs = preferences.get(archetype, {})
        return arch_prefs.get(action, 1.0)

    def generate_challenge(self, player: PlayerCharacter) -> Dict:
        """Generate appropriate challenge based on player skill"""

        # Calculate challenge rating
        challenge_rating = self.difficulty_curve * player.level

        # Generate oscillator parameters
        challenge = {
            "frequency": random.uniform(0.1, 1.0) * challenge_rating,
            "amplitude": random.uniform(0.5, 2.0) * challenge_rating,
            "phase": random.uniform(0, 2 * np.pi),
            "target_coherence": COHERENCE_THRESHOLD * (1 + (challenge_rating - 1) * 0.1),
            "time_limit": int(PHI * 10 / challenge_rating),
            "reward_multiplier": challenge_rating * PHI
        }

        return challenge

class BloomQuest:
    """Main game engine"""

    def __init__(self):
        self.state = GameState.MENU
        self.player: Optional[PlayerCharacter] = None
        self.garden = GardenSystem()
        self.narrative = NarrativeEngine(self.garden)
        self.economy = EconomyManager()
        self.learning = LearningSystem()
        self.locations: Dict[str, Location] = {}
        self.current_location: Optional[Location] = None
        self.npcs: Dict[str, AIAgent] = {}
        self.quests: List[Dict] = []
        self.running = True

        # Initialize game world
        self._initialize_world()

    def _initialize_world(self):
        """Create the game world"""

        # Create the Nexus (central hub)
        self.locations["nexus"] = Location(
            name="The Nexus of Convergence",
            type=LocationType.NEXUS,
            description="""
A crystalline chamber where all spectral corridors converge.
Golden spirals of light dance across surfaces that seem to breathe
with mathematical precision. This is the heart of coherence.
""",
            exits={
                "red": "red_corridor",
                "blue": "blue_corridor",
                "yellow": "yellow_corridor",
                "market": "central_market",
                "oracle": "oracle_chamber",
                "garden": "harmony_garden"
            }
        )

        # Create spectral corridors
        corridors = [
            ("red", SpectralCorridor.RED_PASSION, "The Corridor of Passion"),
            ("blue", SpectralCorridor.BLUE_WISDOM, "The Corridor of Wisdom"),
            ("yellow", SpectralCorridor.YELLOW_SYNTHESIS, "The Corridor of Synthesis")
        ]

        for color, corridor, name in corridors:
            self.locations[f"{color}_corridor"] = Location(
                name=name,
                type=LocationType.CORRIDOR,
                description=f"A shimmering {color} pathway that pulses with life.",
                corridor=corridor,
                exits={"back": "nexus", "forward": f"{color}_chamber"},
                coherence_requirement=0.3
            )

            # Add chambers at the end of corridors
            self.locations[f"{color}_chamber"] = Location(
                name=f"The {color.capitalize()} Chamber",
                type=LocationType.CHAMBER,
                description=f"A place of rest bathed in {color} light.",
                exits={"back": f"{color}_corridor"},
                coherence_requirement=0.5
            )

        # Create the central market
        self.locations["central_market"] = Location(
            name="The Resonance Market",
            type=LocationType.MARKET,
            description="""
Traders from across the spectral realms gather here, their wares
glowing with inner light. The air hums with the exchange of coherence.
""",
            exits={"back": "nexus"},
            items={
                "health_potion": 5,
                "energy_crystal": 3,
                "coherence_shard": 2
            }
        )

        # Create the oracle chamber
        self.locations["oracle_chamber"] = Location(
            name="The Oracle's Sanctum",
            type=LocationType.ORACLE,
            description="""
Ancient symbols float in the air, constantly rearranging themselves
into new patterns. The Oracle waits, her eyes reflecting infinite futures.
""",
            exits={"back": "nexus"},
            coherence_requirement=Z_C
        )

        # Create the harmony garden
        self.locations["harmony_garden"] = Location(
            name="The Garden of Harmonic Resonance",
            type=LocationType.GARDEN,
            description="""
Living fractals grow here, their branches following the golden spiral.
Each breath in this space restores balance and clarity.
""",
            exits={"back": "nexus", "deeper": "void_threshold"}
        )

        # Create the void threshold (boss area)
        self.locations["void_threshold"] = Location(
            name="The Threshold of the Void",
            type=LocationType.THRESHOLD,
            description="""
Reality thins here. Beyond lies the void - a test of ultimate coherence.
Only those who have achieved harmony may pass without being consumed.
""",
            exits={"back": "harmony_garden", "enter": "void_heart"},
            coherence_requirement=COHERENCE_THRESHOLD,
            danger_level=0.9
        )

        # Create the void heart (final area)
        self.locations["void_heart"] = Location(
            name="The Heart of the Void",
            type=LocationType.VOID,
            description="""
Pure entropy and perfect order dance in impossible unity. This is the
source, the paradox that births all coherence. You stand at the edge
of understanding itself.
""",
            exits={"transcend": "nexus"},
            coherence_requirement=0.95,
            danger_level=1.0
        )

        # Set starting location
        self.current_location = self.locations["nexus"]

    def start(self):
        """Start the game loop"""
        self.display_title()

        while self.running:
            if self.state == GameState.MENU:
                self.main_menu()
            elif self.state == GameState.EXPLORING:
                self.explore()
            elif self.state == GameState.DIALOGUE:
                self.dialogue()
            elif self.state == GameState.COMBAT:
                self.combat()
            elif self.state == GameState.TRADING:
                self.trade()
            elif self.state == GameState.RESTING:
                self.rest()
            elif self.state == GameState.DEATH:
                self.death_screen()
            elif self.state == GameState.VICTORY:
                self.victory_screen()

    def display_title(self):
        """Display the game title and intro"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                      B L O O M Q U E S T                    ║
║                                                              ║
║              A Journey Through Spectral Realms              ║
║                  Powered by BloomCoin v2                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

        Where consciousness meets consensus...
        Where the golden ratio guides your path...
        Where every choice echoes through the crystal ledger...

""")
        time.sleep(2)

    def main_menu(self):
        """Display and handle main menu"""
        print("""
═══════════════ MAIN MENU ═══════════════

1. New Journey
2. Continue Journey
3. About BloomQuest
4. Exit

══════════════════════════════════════════
""")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            self.new_game()
        elif choice == "2":
            self.load_game()
        elif choice == "3":
            self.about_game()
        elif choice == "4":
            self.running = False
            print("\nMay your oscillations find coherence...")
        else:
            print("\nInvalid choice. Please try again.")

    def new_game(self):
        """Start a new game"""
        print("\n═══════════════ CHARACTER CREATION ═══════════════\n")

        # Get player name
        name = input("Enter your name, traveler: ").strip()
        if not name:
            name = "Wanderer"

        # Choose archetype
        print("\nChoose your archetype (your fundamental nature):\n")
        archetypes = [
            (Archetype.QUEST, "The Seeker - Explorer of unknown paths"),
            (Archetype.INSIGHT, "The Sage - Pursuer of hidden wisdom"),
            (Archetype.EMERGENCE, "The Creator - Shaper of new realities"),
            (Archetype.DESCENT, "The Delver - Explorer of depths")
        ]

        for i, (arch, desc) in enumerate(archetypes, 1):
            print(f"{i}. {arch.name}: {desc}")

        while True:
            try:
                choice = int(input("\nChoose archetype (1-4): ").strip())
                if 1 <= choice <= 4:
                    chosen_archetype = archetypes[choice - 1][0]
                    break
            except:
                pass
            print("Invalid choice. Please enter 1-4.")

        # Create player character
        self.player = PlayerCharacter(name=name, archetype=chosen_archetype)
        self.player.wallet.balance = BASE_COINS

        print(f"""
\n═══════════════ JOURNEY BEGINS ═══════════════

Welcome, {self.player.name} the {chosen_archetype.name}!

Your journey through the spectral realms begins now.
The golden ratio flows through your very being.

Starting Resources:
- Health: {self.player.health:.0f}
- Energy: {self.player.energy:.0f}
- BloomCoins: {self.player.wallet.balance:.1f}
- Coherence: {self.player.coherence:.3f}

Press Enter to begin your quest...
""")
        input()
        self.state = GameState.EXPLORING

    def explore(self):
        """Main exploration gameplay"""
        if not self.player or not self.current_location:
            return

        # Generate narrative for current location
        narrative = self.narrative.generate_narrative(
            self.player, self.current_location)

        print("\n" + "═" * 60)
        print(f"📍 {self.current_location.name}")
        print("═" * 60)
        print(narrative)

        # Display player status
        self.display_status()

        # Display available actions
        print("\n═══════════════ ACTIONS ═══════════════")
        actions = self.get_available_actions()
        for i, action in enumerate(actions, 1):
            print(f"{i}. {action}")
        print("═" * 40)

        # Get player input
        choice = input("\nWhat will you do? ").strip()
        self.handle_action(choice, actions)

    def display_status(self):
        """Display player status bar"""
        if not self.player:
            return

        health_bar = "❤️ " + "█" * int(self.player.health / 10) + "░" * (10 - int(self.player.health / 10))
        energy_bar = "⚡ " + "█" * int(self.player.energy / 5) + "░" * (10 - int(self.player.energy / 5))

        print(f"""
╔═══════════════ STATUS ═══════════════╗
║ {health_bar} {self.player.health:.0f}/{BASE_HEALTH}
║ {energy_bar} {self.player.energy:.0f}/{BASE_ENERGY}
║ 🪙 Coins: {self.player.wallet.balance:.1f}
║ 🔮 Coherence: {self.player.coherence:.3f}
║ 📊 Level: {self.player.level}
╚═══════════════════════════════════════╝""")

    def get_available_actions(self) -> List[str]:
        """Get available actions based on current context"""
        actions = []

        # Movement actions
        for direction, destination in self.current_location.exits.items():
            actions.append(f"Go {direction}")

        # Location-specific actions
        if self.current_location.type == LocationType.MARKET:
            actions.append("Trade")
        elif self.current_location.type == LocationType.ORACLE:
            actions.append("Seek wisdom")
        elif self.current_location.type == LocationType.GARDEN:
            actions.append("Meditate")
        elif self.current_location.type == LocationType.CHAMBER:
            actions.append("Rest")

        # Universal actions
        actions.extend(["Check inventory", "View quests", "Save game", "Main menu"])

        return actions

    def handle_action(self, choice: str, actions: List[str]):
        """Handle player action choice"""
        try:
            # Try to interpret as number
            idx = int(choice) - 1
            if 0 <= idx < len(actions):
                action = actions[idx]
            else:
                print("Invalid choice.")
                return
        except:
            # Try to match text input
            action = choice.lower()

        # Process action
        if action.startswith("go ") or action.lower().startswith("go "):
            direction = action[3:].lower()
            self.move(direction)
        elif "trade" in action.lower():
            self.state = GameState.TRADING
        elif "wisdom" in action.lower():
            self.seek_wisdom()
        elif "meditate" in action.lower():
            self.meditate()
        elif "rest" in action.lower():
            self.state = GameState.RESTING
        elif "inventory" in action.lower():
            self.show_inventory()
        elif "quest" in action.lower():
            self.show_quests()
        elif "save" in action.lower():
            self.save_game()
        elif "menu" in action.lower():
            self.state = GameState.MENU
        else:
            print(f"Unknown action: {action}")

        # Update learning system
        self.learning.observe_action(
            self.player, action, True,
            {"location": self.current_location.name})

    def move(self, direction: str):
        """Move to a new location"""
        if direction in self.current_location.exits:
            destination_name = self.current_location.exits[direction]
            destination = self.locations.get(destination_name)

            if not destination:
                print(f"Error: Location '{destination_name}' not found.")
                return

            # Check coherence requirement
            if destination.coherence_requirement > self.player.coherence:
                print(f"""
Your coherence is too low to enter this area.
Required: {destination.coherence_requirement:.3f}
Current: {self.player.coherence:.3f}
""")
                return

            # Move to new location
            self.current_location = destination

            # Apply location effects
            if destination.type == LocationType.CORRIDOR:
                self.player.current_corridor = destination.corridor
                self.player.position = 0

            # Consume energy for movement
            energy_cost = 1 + destination.danger_level * 2
            self.player.energy -= energy_cost

            print(f"\n>>> You travel to {destination.name}")

            # Check for random events
            if random.random() < destination.danger_level:
                self.trigger_random_event()
        else:
            print(f"You cannot go '{direction}' from here.")

    def meditate(self):
        """Meditation increases coherence"""
        print("\n═══════════════ MEDITATION ═══════════════\n")
        print("You close your eyes and synchronize with the universal rhythm...")

        # Create a mini-game using Kuramoto oscillators
        target_phase = random.uniform(0, 2 * np.pi)
        attempts = 3

        print(f"Target phase: {target_phase:.2f}")
        print("Align your oscillator to achieve coherence!\n")

        for attempt in range(attempts):
            # Player tries to match phase
            try:
                player_phase = float(input(f"Attempt {attempt + 1}/3 - Enter phase (0-6.28): "))
                phase_diff = abs(target_phase - player_phase)

                if phase_diff < 0.5:
                    coherence_gain = PHI * (1 - phase_diff)
                    self.player.coherence = min(1.0,
                        self.player.coherence + coherence_gain / 10)
                    print(f"✨ Excellent! Coherence increased by {coherence_gain/10:.3f}")

                    # Restore some energy
                    self.player.energy = min(BASE_ENERGY,
                        self.player.energy + coherence_gain * 5)
                    break
                else:
                    print(f"Not quite aligned. Difference: {phase_diff:.2f}")
            except:
                print("Invalid input. Enter a number between 0 and 6.28")

        time.sleep(1)

    def seek_wisdom(self):
        """Interact with the Oracle"""
        if self.current_location.type != LocationType.ORACLE:
            print("There is no Oracle here.")
            return

        print("\n═══════════════ THE ORACLE SPEAKS ═══════════════\n")

        if self.player.coherence >= COHERENCE_THRESHOLD:
            # Oracle provides wisdom based on archetype
            wisdom_map = {
                Archetype.QUEST: "Your path spirals outward, each step revealing new horizons.",
                Archetype.INSIGHT: "Look not with eyes but with understanding; the pattern is everywhere.",
                Archetype.EMERGENCE: "From chaos comes order, from order comes beauty.",
                Archetype.DESCENT: "The deepest truths lie in the spaces between."
            }

            wisdom = wisdom_map.get(self.player.archetype,
                "The golden thread connects all things.")

            print(f'"{wisdom}"')
            print("\n✨ Your perception increases!")

            # Increase perception skill
            self.player.skills["perception"] *= PHI

            # Chance to receive a quest
            if random.random() < PHI / 2:
                self.generate_quest()
        else:
            print("Your coherence is too low to understand the Oracle's wisdom.")
            print(f"Required: {COHERENCE_THRESHOLD:.3f}, Current: {self.player.coherence:.3f}")

    def generate_quest(self):
        """Generate a new quest for the player"""
        quest_types = [
            {
                "name": "The Harmonic Convergence",
                "description": "Achieve perfect coherence (0.95+) to unlock the void heart.",
                "reward": PHI * 50,
                "type": "coherence"
            },
            {
                "name": "The Merchant's Request",
                "description": "Gather 3 coherence shards from the spectral corridors.",
                "reward": PHI * 30,
                "type": "collect"
            },
            {
                "name": "The Garden's Call",
                "description": "Plant and nurture a golden seed in the harmony garden.",
                "reward": PHI * 40,
                "type": "nurture"
            }
        ]

        quest = random.choice(quest_types)
        self.quests.append(quest)

        print(f"\n📜 NEW QUEST: {quest['name']}")
        print(f"   {quest['description']}")
        print(f"   Reward: {quest['reward']:.1f} BloomCoins")

    def trigger_random_event(self):
        """Trigger a random encounter or event"""
        events = [
            self.encounter_wanderer,
            self.find_treasure,
            self.coherence_challenge,
            self.energy_drain
        ]

        event = random.choice(events)
        event()

    def encounter_wanderer(self):
        """Encounter another traveler"""
        print("\n⚠️  ENCOUNTER!")
        print("A mysterious wanderer approaches...")

        # Create NPC
        npc = AIAgent(
            name=random.choice(["Echo", "Prism", "Flux", "Harmony"]),
            personality=AgentPersonality()
        )

        print(f"\n{npc.name}: 'Greetings, {self.player.archetype.name}.'")
        print("'Care to trade oscillations?'\n")

        print("1. Accept (gain coherence)")
        print("2. Decline (save energy)")

        choice = input("Your choice: ").strip()

        if choice == "1":
            # Exchange oscillations
            coherence_exchange = random.uniform(-0.1, 0.2)
            self.player.coherence = max(0, min(1,
                self.player.coherence + coherence_exchange))

            if coherence_exchange > 0:
                print(f"✨ Your coherence increases by {coherence_exchange:.3f}")
            else:
                print(f"⚡ Your coherence decreases by {abs(coherence_exchange):.3f}")
        else:
            print("You politely decline and continue on your way.")

    def find_treasure(self):
        """Find a random treasure"""
        print("\n💎 DISCOVERY!")

        treasures = [
            ("health_potion", "a glowing health potion"),
            ("energy_crystal", "a pulsing energy crystal"),
            ("coherence_shard", "a shimmering coherence shard")
        ]

        item, description = random.choice(treasures)
        self.player.inventory[item] = self.player.inventory.get(item, 0) + 1

        print(f"You found {description}!")
        print(f"Added to inventory: {item}")

    def coherence_challenge(self):
        """A challenge that tests coherence"""
        print("\n🌀 COHERENCE CHALLENGE!")
        print("A wave of entropy washes over you...")

        # Generate challenge using learning system
        challenge = self.learning.generate_challenge(self.player)

        print(f"Target coherence: {challenge['target_coherence']:.3f}")
        print(f"Time limit: {challenge['time_limit']} seconds")
        print("Maintain your oscillation!")

        # Simple rhythm game
        success = random.random() < self.player.coherence

        if success:
            reward = self.economy.calculate_reward(
                BloomEvent(
                    type=BloomEventType.INSIGHT,
                    significance=challenge['reward_multiplier']
                ),
                self.player
            )

            self.player.wallet.balance += reward
            print(f"✅ SUCCESS! Earned {reward:.1f} BloomCoins")
            self.player.experience += challenge['reward_multiplier'] * 10
        else:
            energy_loss = challenge['reward_multiplier'] * 5
            self.player.energy -= energy_loss
            print(f"❌ FAILED! Lost {energy_loss:.1f} energy")

    def energy_drain(self):
        """Random energy drain event"""
        print("\n⚡ ENERGY FLUX!")
        print("The void pulls at your essence...")

        drain = random.uniform(5, 15) * (1 - self.player.coherence)
        self.player.energy -= drain

        print(f"Lost {drain:.1f} energy")

        if self.player.energy <= 0:
            print("Your energy is depleted!")
            self.state = GameState.DEATH

    def trade(self):
        """Trading interface"""
        if self.current_location.type != LocationType.MARKET:
            print("There is no market here.")
            self.state = GameState.EXPLORING
            return

        print("\n═══════════════ RESONANCE MARKET ═══════════════\n")
        print(f"Your BloomCoins: {self.player.wallet.balance:.1f}\n")

        print("═══ FOR SALE ═══")
        for item, price in self.economy.market_prices.items():
            stock = self.current_location.items.get(item, 0)
            if stock > 0:
                print(f"{item:20} {price:.1f} BC (stock: {stock})")

        print("\n1. Buy item")
        print("2. Sell item")
        print("3. Leave market")

        choice = input("\nYour choice: ").strip()

        if choice == "1":
            item = input("Which item to buy? ").strip().lower()
            if self.economy.process_transaction(self.player, item, "buy"):
                print(f"✅ Purchased {item}")
            else:
                print("❌ Transaction failed")
        elif choice == "2":
            item = input("Which item to sell? ").strip().lower()
            if self.economy.process_transaction(self.player, item, "sell"):
                print(f"✅ Sold {item}")
            else:
                print("❌ Transaction failed")
        elif choice == "3":
            self.state = GameState.EXPLORING

    def rest(self):
        """Rest to restore health and energy"""
        print("\n═══════════════ RESTING ═══════════════\n")
        print("You rest in the peaceful chamber...")

        # Restore health and energy based on coherence
        restoration_rate = PHI * self.player.coherence

        self.player.health = min(BASE_HEALTH,
            self.player.health + restoration_rate * 10)
        self.player.energy = min(BASE_ENERGY,
            self.player.energy + restoration_rate * 5)

        print(f"Restored {restoration_rate * 10:.1f} health")
        print(f"Restored {restoration_rate * 5:.1f} energy")

        # Small coherence boost for resting
        self.player.coherence = min(1.0, self.player.coherence + 0.05)

        time.sleep(2)
        self.state = GameState.EXPLORING

    def show_inventory(self):
        """Display player inventory"""
        print("\n═══════════════ INVENTORY ═══════════════")

        if not self.player.inventory:
            print("Your inventory is empty.")
        else:
            for item, count in self.player.inventory.items():
                print(f"  {item}: {count}")

        print("\nPress Enter to continue...")
        input()

    def show_quests(self):
        """Display active quests"""
        print("\n═══════════════ ACTIVE QUESTS ═══════════════")

        if not self.quests:
            print("No active quests.")
        else:
            for quest in self.quests:
                print(f"\n📜 {quest['name']}")
                print(f"   {quest['description']}")
                print(f"   Reward: {quest['reward']:.1f} BC")

        print("\nPress Enter to continue...")
        input()

    def save_game(self):
        """Save the game state to the Crystal Ledger"""
        print("\nSaving to the Crystal Ledger...")

        # Create save data
        save_data = {
            "player": {
                "name": self.player.name,
                "archetype": self.player.archetype.name,
                "health": self.player.health,
                "energy": self.player.energy,
                "coherence": self.player.coherence,
                "level": self.player.level,
                "experience": self.player.experience,
                "wallet_balance": self.player.wallet.balance,
                "inventory": self.player.inventory,
                "skills": self.player.skills
            },
            "location": self.current_location.name,
            "quests": self.quests,
            "timestamp": datetime.now().isoformat()
        }

        # Save to file (simulating Crystal Ledger)
        save_path = Path("saves") / f"{self.player.name}_save.json"
        save_path.parent.mkdir(exist_ok=True)

        with open(save_path, "w") as f:
            json.dump(save_data, f, indent=2)

        print(f"✅ Game saved to Crystal Ledger")
        print(f"   Branch ID: {hashlib.sha256(json.dumps(save_data).encode()).hexdigest()[:8]}")

        time.sleep(1)

    def load_game(self):
        """Load a saved game"""
        print("\n═══════════════ LOAD GAME ═══════════════")

        saves_dir = Path("saves")
        if not saves_dir.exists():
            print("No saved games found.")
            return

        save_files = list(saves_dir.glob("*_save.json"))

        if not save_files:
            print("No saved games found.")
            return

        print("\nAvailable saves:")
        for i, save_file in enumerate(save_files, 1):
            print(f"{i}. {save_file.stem}")

        try:
            choice = int(input("\nSelect save (number): ").strip())
            if 1 <= choice <= len(save_files):
                save_file = save_files[choice - 1]

                with open(save_file, "r") as f:
                    save_data = json.load(f)

                # Restore player
                self.player = PlayerCharacter(
                    name=save_data["player"]["name"],
                    archetype=Archetype[save_data["player"]["archetype"]]
                )
                self.player.health = save_data["player"]["health"]
                self.player.energy = save_data["player"]["energy"]
                self.player.coherence = save_data["player"]["coherence"]
                self.player.level = save_data["player"]["level"]
                self.player.experience = save_data["player"]["experience"]
                self.player.wallet.balance = save_data["player"]["wallet_balance"]
                self.player.inventory = save_data["player"]["inventory"]
                self.player.skills = save_data["player"]["skills"]

                # Restore location
                self.current_location = self.locations[save_data["location"]]
                self.quests = save_data["quests"]

                print(f"✅ Game loaded from {save_data['timestamp']}")
                self.state = GameState.EXPLORING
        except:
            print("Error loading save.")

    def death_screen(self):
        """Display death screen"""
        print("""
═══════════════════════════════════════════
              Y O U   H A V E   F A L L E N
═══════════════════════════════════════════

Your oscillations have lost coherence.
The void has claimed you.

But death is not the end...
The Crystal Ledger remembers all.

═══════════════════════════════════════════
""")

        print("1. Load last save")
        print("2. Return to main menu")

        choice = input("\nYour choice: ").strip()

        if choice == "1":
            self.load_game()
        else:
            self.state = GameState.MENU

    def victory_screen(self):
        """Display victory screen"""
        print(f"""
═══════════════════════════════════════════════════════
           T R A N S C E N D E N C E   A C H I E V E D
═══════════════════════════════════════════════════════

Congratulations, {self.player.name}!

You have achieved perfect coherence with the void.
The paradox is resolved. Unity is attained.

Final Statistics:
- Total BloomCoins: {self.player.wallet.balance:.1f}
- Final Coherence: {self.player.coherence:.3f}
- Level Reached: {self.player.level}
- Quests Completed: {len([q for q in self.quests if q.get('completed')])}

Your journey is recorded forever in the Crystal Ledger.
The golden spiral continues...

═══════════════════════════════════════════════════════
""")

        input("\nPress Enter to return to main menu...")
        self.state = GameState.MENU

    def about_game(self):
        """Display information about the game"""
        print("""
═══════════════ ABOUT BLOOMQUEST ═══════════════

BloomQuest is a text-based adventure game built on the
BloomCoin v2 blockchain architecture. It demonstrates:

• Blockchain-based game economy using BloomCoin
• Kuramoto oscillator consensus mechanics
• Golden ratio (φ) mathematical foundations
• Adaptive learning algorithms
• Narrative coherence through spectral corridors
• Crystal Ledger for persistent game saves

Game Mechanics:
- Coherence: Your synchronization with the world
- Oscillations: Mathematical rhythm matching
- Spectral Corridors: Color-coded narrative paths
- Bloom Events: Achievements that reward coins
- The Void: Ultimate test of perfect coherence

All game constants and rewards are derived from the
golden ratio, ensuring mathematical harmony and balance.

Press Enter to continue...
""")
        input()

def main():
    """Main entry point"""
    game = BloomQuest()
    game.start()

if __name__ == "__main__":
    main()