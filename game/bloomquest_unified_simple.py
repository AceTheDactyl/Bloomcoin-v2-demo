#!/usr/bin/env python3
"""
BloomQuest Unified (Simplified) - Adapted for existing modules
A complete adventure combining all systems
"""

import sys
from pathlib import Path
import random
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum

# Setup paths
base_path = Path(__file__).parent.parent
sys.path.insert(0, str(base_path / "bloomcoin-v0.1.0" / "bloomcoin"))
sys.path.insert(0, str(Path(__file__).parent))

# Try imports with fallbacks
try:
    from bloomcoin.constants import PHI
except:
    PHI = 1.618033988749895

# Sacred constants
Z_C = (3**0.5) / 2

class GameState(Enum):
    """Game states"""
    MAIN_MENU = "main_menu"
    EXPLORING = "exploring"
    COMPANION = "companion"
    CRAFTING = "crafting"
    BATTLE = "battle"
    SHOP = "shop"

class SimpleCompanion:
    """Simplified companion"""
    def __init__(self, name: str, archetype: str):
        self.name = name
        self.archetype = archetype
        self.level = 1
        self.patterns_absorbed = 0
        self.wisdom_phrases = [
            "The patterns reveal themselves to those who seek.",
            "Each challenge strengthens your coherence.",
            "Growth follows the golden spiral.",
            "In unity, we find strength.",
            "The territories call to us all differently."
        ]

    def get_wisdom(self) -> str:
        return random.choice(self.wisdom_phrases)

    def feed_pattern(self, pattern: str):
        self.patterns_absorbed += 1
        if self.patterns_absorbed % 5 == 0:
            self.level += 1
            return f"{self.name} evolved to level {self.level}!"
        return f"{self.name} absorbed the {pattern}."

class SimpleItem:
    """Simplified item"""
    def __init__(self, name: str, rarity: str, power: float):
        self.name = name
        self.rarity = rarity
        self.power = power
        self.properties = []

class SimplePlayer:
    """Simplified player"""
    def __init__(self, name: str, archetype: str):
        self.name = name
        self.archetype = archetype
        self.bloomcoin = PHI * 10
        self.coherence = 0.618  # φ⁻¹
        self.inventory = []
        self.location = "Garden Heart"
        self.companion = SimpleCompanion(f"Spirit of {name}", archetype)
        self.deck = self._build_initial_deck()

    def _build_initial_deck(self):
        """Build a simple card deck"""
        suits = ["Leaves", "Stars", "Shadows", "Crystals", "Flames"]
        ranks = list(range(1, 11))
        deck = []
        for _ in range(20):
            suit = random.choice(suits)
            rank = random.choice(ranks)
            deck.append(f"{rank} of {suit}")
        return deck

class SimpleBattle:
    """Simplified battle system"""
    def __init__(self, player: SimplePlayer):
        self.player = player
        self.player_hp = 100
        self.enemy_hp = 100
        self.player_hand = []
        self.turn = 1

    def draw_cards(self, count: int):
        """Draw cards from deck"""
        for _ in range(count):
            if self.player.deck:
                self.player_hand.append(self.player.deck.pop(0))

    def play_card(self, card_index: int) -> int:
        """Play a card and return damage"""
        if 0 <= card_index < len(self.player_hand):
            card = self.player_hand.pop(card_index)
            # Extract rank from card name
            rank = int(card.split()[0])
            damage = rank * PHI * self.player.coherence
            return damage
        return 0

class BloomQuestSimplified:
    """Simplified unified game"""

    def __init__(self):
        self.state = GameState.MAIN_MENU
        self.player = None
        self.running = True
        self.current_battle = None
        self.locations = [
            "Garden Heart",
            "Crystal Caves",
            "Phoenix Nest",
            "Void Market",
            "Library Infinite"
        ]

    def start(self):
        """Start the game"""
        print("\n" + "="*60)
        print("🌸 BLOOMQUEST: MYTHIC ECONOMY (SIMPLIFIED) 🌸")
        print("A PHI-Based Adventure")
        print("="*60)

        self._create_character()

        while self.running:
            try:
                if self.state == GameState.MAIN_MENU:
                    self._main_menu()
                elif self.state == GameState.EXPLORING:
                    self._explore()
                elif self.state == GameState.COMPANION:
                    self._companion_chat()
                elif self.state == GameState.CRAFTING:
                    self._craft()
                elif self.state == GameState.BATTLE:
                    self._battle()
                elif self.state == GameState.SHOP:
                    self._shop()

            except KeyboardInterrupt:
                print("\n\nPaused. Type 'quit' to exit...")
                if input().lower() == 'quit':
                    self.running = False

        self._end_game()

    def _create_character(self):
        """Create character"""
        print("\n📜 CHARACTER CREATION")
        print("-" * 40)

        name = input("Enter your name: ").strip() or "Wanderer"

        print("\n🎭 Choose your path:")
        archetypes = [
            "Seeker - Discovery and wisdom",
            "Forger - Creation and craft",
            "Guardian - Protection and strength",
            "Scholar - Knowledge and patterns",
            "Mystic - Magic and mystery"
        ]

        for i, arch in enumerate(archetypes, 1):
            print(f"{i}. {arch}")

        while True:
            try:
                choice = int(input("\nChoice (1-5): "))
                if 1 <= choice <= 5:
                    archetype = archetypes[choice-1].split(" - ")[0]
                    break
            except:
                pass
            print("Please choose 1-5")

        self.player = SimplePlayer(name, archetype)

        print(f"\n✨ Welcome, {name} the {archetype}!")
        print(f"Starting BloomCoin: {self.player.bloomcoin:.2f}")
        print(f"Companion: {self.player.companion.name}")
        input("\nPress Enter to begin...")

    def _main_menu(self):
        """Main menu"""
        print("\n" + "="*50)
        print(f"📍 {self.player.location}")
        print(f"💰 BloomCoin: {self.player.bloomcoin:.2f}")
        print(f"🌟 Coherence: {self.player.coherence:.2%}")
        print(f"🎒 Items: {len(self.player.inventory)}")
        print(f"🐾 {self.player.companion.name} (Lvl {self.player.companion.level})")
        print("="*50)

        print("\n🧭 ACTIONS:")
        print("1. Explore")
        print("2. Talk to Companion")
        print("3. Craft Patterns")
        print("4. Battle")
        print("5. Shop")
        print("6. Meditate")
        print("7. Travel")
        print("8. Quit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            self.state = GameState.EXPLORING
        elif choice == "2":
            self.state = GameState.COMPANION
        elif choice == "3":
            self.state = GameState.CRAFTING
        elif choice == "4":
            self.state = GameState.BATTLE
        elif choice == "5":
            self.state = GameState.SHOP
        elif choice == "6":
            self._meditate()
        elif choice == "7":
            self._travel()
        elif choice == "8":
            self.running = False

    def _explore(self):
        """Explore location"""
        print(f"\n🔍 Exploring {self.player.location}...")

        # Chance to find item
        if random.random() < 0.3 + (self.player.coherence * 0.2):
            rarities = ["Common", "Uncommon", "Rare", "Epic", "Legendary"]
            weights = [0.5, 0.3, 0.15, 0.04, 0.01]
            rarity = random.choices(rarities, weights)[0]

            item_names = {
                "Garden Heart": ["Living Seed", "Bloom Essence", "Root Crystal"],
                "Crystal Caves": ["Echo Shard", "Resonance Gem", "Harmonic Stone"],
                "Phoenix Nest": ["Ember Feather", "Ash of Rebirth", "Flame Core"],
                "Void Market": ["Shadow Coin", "Void Fragment", "Null Stone"],
                "Library Infinite": ["Wisdom Scroll", "Pattern Codex", "Truth Page"]
            }

            name = random.choice(item_names.get(self.player.location, ["Mysterious Item"]))
            power = PHI ** (rarities.index(rarity) + 1)

            item = SimpleItem(f"{rarity} {name}", rarity, power)
            self.player.inventory.append(item)

            print(f"\n✨ Found {item.name}!")
            print(f"Power: {item.power:.1f}")

            self.player.coherence = min(1.0, self.player.coherence + 0.05)
        else:
            print("\nYou search but find nothing of note...")

        # Random encounter
        if random.random() < 0.2:
            print("\n⚔️ A challenger appears!")
            input("Press Enter for battle...")
            self.state = GameState.BATTLE
            return

        input("\nPress Enter to continue...")
        self.state = GameState.MAIN_MENU

    def _companion_chat(self):
        """Chat with companion"""
        print(f"\n🐾 {self.player.companion.name}")
        print(f"Level {self.player.companion.level}")
        print("-" * 40)

        wisdom = self.player.companion.get_wisdom()
        print(f'\n💭 "{wisdom}"')

        print("\n1. Ask for guidance")
        print("2. Feed pattern")
        print("3. Check progress")
        print("4. Return")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            hints = [
                "Explore deeply to find rare items.",
                "Your coherence affects everything.",
                "Patterns compound like golden spirals.",
                "Each territory holds unique treasures.",
                "Meditation strengthens your connection."
            ]
            print(f'\n{self.player.companion.name}: "{random.choice(hints)}"')

        elif choice == "2":
            if self.player.companion.patterns_absorbed < 100:
                patterns = ["Resonance", "Growth", "Shadow", "Light", "Harmony"]
                pattern = random.choice(patterns)
                result = self.player.companion.feed_pattern(pattern)
                print(f"\n✨ {result}")
            else:
                print("\nYour companion has absorbed maximum patterns!")

        elif choice == "3":
            print(f"\nPatterns Absorbed: {self.player.companion.patterns_absorbed}")
            print(f"Next Level: {5 - (self.player.companion.patterns_absorbed % 5)} patterns")

        input("\nPress Enter to continue...")
        self.state = GameState.MAIN_MENU

    def _craft(self):
        """Craft patterns"""
        print("\n🍳 PATTERN CRAFTING")
        print("-" * 40)

        if len(self.player.inventory) < 2:
            print("Need at least 2 items to craft!")
            input("Press Enter...")
            self.state = GameState.MAIN_MENU
            return

        print("Your items:")
        for i, item in enumerate(self.player.inventory[:5], 1):
            print(f"{i}. {item.name}")

        print("\n1. Craft Resonance Pattern (2 items)")
        print("2. Craft Growth Pattern (2 items)")
        print("3. Cancel")

        choice = input("\nChoice: ").strip()

        if choice in ["1", "2"]:
            if len(self.player.inventory) >= 2:
                item1 = self.player.inventory.pop(0)
                item2 = self.player.inventory.pop(0)

                pattern = "Resonance" if choice == "1" else "Growth"
                print(f"\n✨ Crafted {pattern} Pattern!")
                print(f"Used: {item1.name} + {item2.name}")

                result = self.player.companion.feed_pattern(pattern)
                print(f"\n🐾 {result}")

        input("\nPress Enter...")
        self.state = GameState.MAIN_MENU

    def _battle(self):
        """Battle system"""
        if not self.current_battle:
            self.current_battle = SimpleBattle(self.player)
            self.current_battle.draw_cards(5)
            print("\n⚔️ BATTLE START!")

        battle = self.current_battle

        print(f"\n{'='*40}")
        print(f"Turn {battle.turn}")
        print(f"Your HP: {battle.player_hp}/100")
        print(f"Enemy HP: {battle.enemy_hp}/100")
        print(f"Hand: {len(battle.player_hand)} cards")

        if battle.player_hand:
            print("\nYour hand:")
            for i, card in enumerate(battle.player_hand, 1):
                print(f"{i}. {card}")

        print("\n1. Play card")
        print("2. Draw card")
        print("3. Flee")

        choice = input("\nChoice: ").strip()

        if choice == "1" and battle.player_hand:
            card_choice = input("Card number: ").strip()
            try:
                idx = int(card_choice) - 1
                damage = battle.play_card(idx)
                battle.enemy_hp -= damage
                print(f"\n💥 Dealt {damage:.1f} damage!")
            except:
                print("Invalid!")

        elif choice == "2":
            battle.draw_cards(1)
            print("\n🎴 Drew a card")

        elif choice == "3":
            print("\n💨 You fled!")
            self.current_battle = None
            self.state = GameState.MAIN_MENU
            return

        # Enemy turn
        if battle.enemy_hp > 0:
            enemy_damage = random.randint(5, 15)
            battle.player_hp -= enemy_damage
            print(f"\n💥 Enemy deals {enemy_damage} damage!")

        # Check victory/defeat
        if battle.enemy_hp <= 0:
            reward = 10 * PHI
            self.player.bloomcoin += reward
            self.player.coherence = min(1.0, self.player.coherence + 0.1)

            print("\n🎉 VICTORY!")
            print(f"Earned {reward:.2f} BloomCoin!")

            self.current_battle = None
            input("\nPress Enter...")
            self.state = GameState.MAIN_MENU

        elif battle.player_hp <= 0:
            print("\n💔 DEFEATED...")
            self.player.bloomcoin = max(0, self.player.bloomcoin - 5)
            self.current_battle = None
            input("\nPress Enter...")
            self.state = GameState.MAIN_MENU

        else:
            battle.turn += 1
            battle.draw_cards(1)

    def _shop(self):
        """Shop"""
        print("\n🏪 MARKETPLACE")
        print(f"Your BloomCoin: {self.player.bloomcoin:.2f}")

        items = [
            ("Health Potion", 10, "Restore health"),
            ("Pattern Crystal", 20, "Craft patterns"),
            ("Card Pack", 15, "5 new cards"),
            ("Coherence Gem", 30, "Boost coherence")
        ]

        for i, (name, cost, desc) in enumerate(items, 1):
            print(f"{i}. {name} - {cost} BC ({desc})")
        print("5. Leave")

        choice = input("\nChoice: ").strip()

        if choice in ["1", "2", "3", "4"]:
            idx = int(choice) - 1
            name, cost, _ = items[idx]

            if self.player.bloomcoin >= cost:
                self.player.bloomcoin -= cost
                print(f"\n✅ Bought {name}!")

                if name == "Card Pack":
                    for _ in range(5):
                        suit = random.choice(["Leaves", "Stars", "Shadows"])
                        rank = random.randint(1, 10)
                        self.player.deck.append(f"{rank} of {suit}")
                elif name == "Coherence Gem":
                    self.player.coherence = min(1.0, self.player.coherence + 0.1)
            else:
                print("Not enough BloomCoin!")

        if choice != "5":
            self._shop()
        else:
            self.state = GameState.MAIN_MENU

    def _meditate(self):
        """Meditate to gain bloomcoin"""
        print("\n🧘 MEDITATION")
        print("Aligning with PHI frequency...")

        mined = PHI * (1 + self.player.coherence) * random.uniform(0.8, 1.2)
        self.player.bloomcoin += mined
        self.player.coherence = min(1.0, self.player.coherence + 0.02)

        print(f"\n✨ Mined {mined:.3f} BloomCoin!")
        print(f"Coherence: {self.player.coherence:.2%}")

        input("\nPress Enter...")
        self.state = GameState.MAIN_MENU

    def _travel(self):
        """Travel between locations"""
        print("\n🗺️ TRAVEL")

        for i, loc in enumerate(self.locations, 1):
            marker = "📍" if loc == self.player.location else ""
            print(f"{i}. {loc} {marker}")

        choice = input("\nDestination: ").strip()

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.locations):
                cost = PHI * 2
                if self.player.bloomcoin >= cost:
                    self.player.bloomcoin -= cost
                    self.player.location = self.locations[idx]
                    print(f"\n✈️ Traveled to {self.player.location}")
                else:
                    print("Not enough BloomCoin!")
        except:
            print("Invalid choice")

        input("\nPress Enter...")
        self.state = GameState.MAIN_MENU

    def _end_game(self):
        """End game"""
        print("\n" + "="*60)
        print("🌅 JOURNEY'S END")
        print("="*60)

        if self.player:
            print(f"\n{self.player.name} the {self.player.archetype}")
            print(f"BloomCoin: {self.player.bloomcoin:.2f}")
            print(f"Coherence: {self.player.coherence:.2%}")
            print(f"Items: {len(self.player.inventory)}")
            print(f"Companion Level: {self.player.companion.level}")

        print("\n✨ Thank you for playing!")

def main():
    """Launch the game"""
    print("🌺 BloomQuest Simplified Launcher")
    print("="*40)

    try:
        game = BloomQuestSimplified()
        game.start()
    except KeyboardInterrupt:
        print("\n\n💫 Game interrupted.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()