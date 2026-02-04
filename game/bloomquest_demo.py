#!/usr/bin/env python3
"""
BloomQuest Demo - Simplified Playable Version
==============================================
A demonstration version of BloomQuest that works with minimal dependencies.
Shows the core game concepts and bloomcoin integration.
"""

import sys
import random
import time
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

# Try to import PHI, fallback to hardcoded value if not available
try:
    sys.path.insert(0, str(Path(__file__).parent.parent / "bloomcoin-v0.1.0" / "bloomcoin"))
    from bloomcoin.constants import PHI, Z_C
except:
    print("Note: Using hardcoded constants (bloomcoin module not found)")
    PHI = 1.618033988749895  # Golden ratio
    Z_C = 0.866025403784439  # Critical coherence

# Game Constants
BASE_HEALTH = int(PHI * 61.8)  # ~100
BASE_ENERGY = int(PHI * 30.9)  # ~50
BASE_COINS = int(PHI * 6.18)   # ~10

class GameState(Enum):
    """Game state machine"""
    MENU = "menu"
    EXPLORING = "exploring"
    TRADING = "trading"
    COMBAT = "combat"
    VICTORY = "victory"
    DEATH = "death"

class Archetype(Enum):
    """Player archetypes"""
    QUEST = "The Seeker"
    INSIGHT = "The Sage"
    EMERGENCE = "The Creator"
    DESCENT = "The Delver"

@dataclass
class Player:
    """Simplified player character"""
    name: str
    archetype: Archetype
    health: float = BASE_HEALTH
    energy: float = BASE_ENERGY
    coins: float = BASE_COINS
    coherence: float = 0.5
    inventory: Dict[str, int] = None
    level: int = 1

    def __post_init__(self):
        if self.inventory is None:
            self.inventory = {}

@dataclass
class Location:
    """Game location"""
    name: str
    description: str
    coherence_required: float = 0.0
    danger: float = 0.0

class SimplifiedBloomQuest:
    """Simplified demo version of BloomQuest"""

    def __init__(self):
        self.state = GameState.MENU
        self.player: Optional[Player] = None
        self.current_location: Optional[Location] = None
        self.locations = self._create_locations()
        self.running = True
        self.turn_count = 0

    def _create_locations(self) -> Dict[str, Location]:
        """Create game world"""
        return {
            "nexus": Location(
                "The Nexus",
                "A crystalline chamber where golden light dances. All paths converge here.",
                0.0, 0.0
            ),
            "market": Location(
                "Resonance Market",
                "Traders exchange goods infused with mathematical harmony.",
                0.0, 0.1
            ),
            "garden": Location(
                "Harmony Garden",
                "Living fractals grow in spiral patterns. Peace pervades this space.",
                0.2, 0.0
            ),
            "corridor": Location(
                "Spectral Corridor",
                "Colors shift and blend as you move through this transitional space.",
                0.3, 0.2
            ),
            "oracle": Location(
                "Oracle's Chamber",
                "Ancient wisdom echoes in crystallized thoughts.",
                0.5, 0.1
            ),
            "void": Location(
                "Void Threshold",
                "The boundary between order and chaos. Danger and opportunity dance.",
                Z_C, 0.8
            )
        }

    def start(self):
        """Main game loop"""
        self.display_title()

        while self.running:
            if self.state == GameState.MENU:
                self.main_menu()
            elif self.state == GameState.EXPLORING:
                self.explore()
            elif self.state == GameState.TRADING:
                self.trade()
            elif self.state == GameState.COMBAT:
                self.combat()
            elif self.state == GameState.VICTORY:
                self.victory()
            elif self.state == GameState.DEATH:
                self.death()

    def display_title(self):
        """Display game title"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    B L O O M Q U E S T                      ║
║                         Demo Version                        ║
║                                                              ║
║              A Journey Through Golden Realms                ║
║                  Powered by BloomCoin v2                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

        φ = 1.618... The Golden Thread Connects All

""")

    def main_menu(self):
        """Main menu"""
        print("═══════════════ MAIN MENU ═══════════════\n")
        print("1. New Journey")
        print("2. About BloomQuest")
        print("3. Exit\n")

        choice = input("Choose (1-3): ").strip()

        if choice == "1":
            self.new_game()
        elif choice == "2":
            self.about()
        elif choice == "3":
            print("\nMay your oscillations find coherence...")
            self.running = False
        else:
            print("Invalid choice.")

    def new_game(self):
        """Start new game"""
        print("\n═══════════════ CHARACTER CREATION ═══════════════\n")

        name = input("Enter your name: ").strip() or "Wanderer"

        print("\nChoose your archetype:")
        archetypes = list(Archetype)
        for i, arch in enumerate(archetypes, 1):
            print(f"{i}. {arch.value} ({arch.name})")

        while True:
            try:
                choice = int(input("\nChoose (1-4): "))
                if 1 <= choice <= 4:
                    archetype = archetypes[choice - 1]
                    break
            except:
                pass
            print("Please enter 1-4.")

        self.player = Player(name, archetype)
        self.current_location = self.locations["nexus"]

        print(f"""
═══════════════ JOURNEY BEGINS ═══════════════

Welcome, {name} the {archetype.value}!

Starting Resources:
- Health: {self.player.health:.0f}
- Energy: {self.player.energy:.0f}
- Coins: {self.player.coins:.1f}
- Coherence: {self.player.coherence:.3f}

Press Enter to begin...
""")
        input()
        self.state = GameState.EXPLORING

    def explore(self):
        """Exploration mode"""
        if not self.player or not self.current_location:
            return

        self.turn_count += 1

        # Display location
        print("\n" + "═" * 50)
        print(f"📍 {self.current_location.name}")
        print("═" * 50)
        print(f"\n{self.current_location.description}\n")

        # Display status
        self._display_status()

        # Random events
        if random.random() < 0.2:
            self._random_event()

        # Display actions
        print("\n═══════════════ ACTIONS ═══════════════")
        print("1. Travel to another location")
        print("2. Meditate (increase coherence)")
        print("3. Search area")
        print("4. Trade")
        print("5. Rest (costs 5 coins)")
        print("6. Check inventory")
        print("7. Return to menu")
        print("═" * 40)

        choice = input("\nWhat will you do? ").strip()

        if choice == "1":
            self._travel()
        elif choice == "2":
            self._meditate()
        elif choice == "3":
            self._search()
        elif choice == "4":
            self.state = GameState.TRADING
        elif choice == "5":
            self._rest()
        elif choice == "6":
            self._show_inventory()
        elif choice == "7":
            self.state = GameState.MENU
        else:
            print("Invalid action.")

        # Energy drain
        self.player.energy -= 1 + self.current_location.danger

        # Check game over conditions
        if self.player.health <= 0 or self.player.energy <= 0:
            self.state = GameState.DEATH
        elif self.player.coherence >= 1.0 and self.player.level >= 5:
            self.state = GameState.VICTORY

    def _display_status(self):
        """Display player status"""
        print(f"""╔═══════════════ STATUS ═══════════════╗
║ ❤️  Health: {self.player.health:.0f}/{BASE_HEALTH}
║ ⚡ Energy: {self.player.energy:.0f}/{BASE_ENERGY}
║ 🪙 Coins: {self.player.coins:.1f}
║ 🔮 Coherence: {self.player.coherence:.3f}
║ 📊 Level: {self.player.level}
║ 🔄 Turn: {self.turn_count}
╚═══════════════════════════════════════╝""")

    def _travel(self):
        """Travel to new location"""
        print("\n═══════════════ TRAVEL ═══════════════")
        locations = list(self.locations.keys())

        for i, loc_key in enumerate(locations, 1):
            loc = self.locations[loc_key]
            status = "✅" if self.player.coherence >= loc.coherence_required else "🔒"
            print(f"{i}. {status} {loc.name} (requires {loc.coherence_required:.2f} coherence)")

        try:
            choice = int(input("\nChoose destination (0 to cancel): "))
            if 0 < choice <= len(locations):
                destination = self.locations[locations[choice - 1]]
                if self.player.coherence >= destination.coherence_required:
                    self.current_location = destination
                    self.player.energy -= 5
                    print(f"\n→ Traveled to {destination.name}")
                else:
                    print("\nInsufficient coherence!")
        except:
            print("Travel cancelled.")

    def _meditate(self):
        """Meditation mini-game"""
        print("\n═══════════════ MEDITATION ═══════════════")
        print("Align your oscillations with the universal frequency...")
        print("Choose a number between 0 and 10 to match the hidden frequency.")

        target = random.randint(0, 10)
        attempts = 3

        for attempt in range(attempts):
            try:
                guess = int(input(f"\nAttempt {attempt + 1}/3: "))
                diff = abs(target - guess)

                if diff == 0:
                    gain = 0.1 * PHI
                    self.player.coherence = min(1.0, self.player.coherence + gain)
                    print(f"✨ Perfect alignment! +{gain:.3f} coherence")
                    self.player.energy += 10
                    break
                elif diff <= 2:
                    gain = 0.05
                    self.player.coherence = min(1.0, self.player.coherence + gain)
                    print(f"Close! +{gain:.3f} coherence")
                else:
                    print("Not aligned. Try again.")
            except:
                print("Invalid input.")

        print(f"\nThe target was {target}")
        time.sleep(1)

    def _search(self):
        """Search current area"""
        print("\n═══════════════ SEARCHING ═══════════════")
        print("You search the area carefully...")

        if random.random() < 0.4:
            # Find coins
            coins_found = random.uniform(1, 10) * PHI
            self.player.coins += coins_found
            print(f"💰 Found {coins_found:.1f} BloomCoins!")
        elif random.random() < 0.3:
            # Find item
            items = ["Health Potion", "Energy Crystal", "Coherence Shard"]
            item = random.choice(items)
            self.player.inventory[item] = self.player.inventory.get(item, 0) + 1
            print(f"📦 Found {item}!")
        else:
            print("Nothing found this time.")

        self.player.energy -= 3

    def _rest(self):
        """Rest to restore health and energy"""
        if self.player.coins >= 5:
            self.player.coins -= 5
            health_gain = 20 * self.player.coherence
            energy_gain = 10 * self.player.coherence

            self.player.health = min(BASE_HEALTH, self.player.health + health_gain)
            self.player.energy = min(BASE_ENERGY, self.player.energy + energy_gain)

            print(f"\n✨ Rested well!")
            print(f"Restored {health_gain:.0f} health and {energy_gain:.0f} energy")
        else:
            print("\nNot enough coins to rest (need 5)")

    def _show_inventory(self):
        """Display inventory"""
        print("\n═══════════════ INVENTORY ═══════════════")
        if self.player.inventory:
            for item, count in self.player.inventory.items():
                print(f"  {item}: {count}")
        else:
            print("  Empty")
        print("\nPress Enter to continue...")
        input()

    def _random_event(self):
        """Random events"""
        events = [
            ("💫 Coherence Surge!", 0.05, 0),
            ("⚡ Energy Drain!", 0, -5),
            ("🎁 Gift from the Universe!", 0, 0),
            ("🌀 Oscillation Challenge!", 0, 0)
        ]

        event = random.choice(events)
        print(f"\n*** {event[0]} ***")

        if event[1] != 0:
            self.player.coherence = min(1.0, self.player.coherence + event[1])
            print(f"Coherence {'increased' if event[1] > 0 else 'decreased'} by {abs(event[1]):.2f}")

        if event[2] != 0:
            self.player.energy += event[2]
            print(f"Energy {'gained' if event[2] > 0 else 'lost'}: {abs(event[2])}")

        if "Gift" in event[0]:
            coins = PHI * random.randint(3, 8)
            self.player.coins += coins
            print(f"Received {coins:.1f} BloomCoins!")

        if "Challenge" in event[0]:
            print("Quick! Enter a number (1-5):")
            try:
                choice = int(input())
                if choice == random.randint(1, 5):
                    self.player.level += 1
                    print(f"✨ Success! Advanced to level {self.player.level}")
                else:
                    print("Failed the challenge.")
            except:
                print("Challenge failed.")

    def trade(self):
        """Trading system"""
        print("\n═══════════════ TRADING POST ═══════════════")
        print(f"Your Coins: {self.player.coins:.1f}\n")

        items = {
            "Health Potion": PHI * 5,
            "Energy Crystal": PHI * 3,
            "Coherence Shard": PHI * 10
        }

        print("═══ FOR SALE ═══")
        for i, (item, price) in enumerate(items.items(), 1):
            print(f"{i}. {item}: {price:.1f} BC")

        print("\n1-3: Buy item")
        print("4: Sell items")
        print("5: Leave market")

        choice = input("\nChoice: ").strip()

        try:
            if 1 <= int(choice) <= 3:
                item_list = list(items.keys())
                item = item_list[int(choice) - 1]
                price = items[item]

                if self.player.coins >= price:
                    self.player.coins -= price
                    self.player.inventory[item] = self.player.inventory.get(item, 0) + 1
                    print(f"✅ Purchased {item}")
                else:
                    print("❌ Not enough coins!")
        except:
            pass

        if choice == "4":
            print("\nYour items:")
            for item, count in self.player.inventory.items():
                sell_price = items.get(item, 5) * 0.7  # 70% of buy price
                print(f"  {item} x{count} (sell for {sell_price:.1f} BC each)")

            item_name = input("Item to sell (or cancel): ").strip()
            if item_name in self.player.inventory and self.player.inventory[item_name] > 0:
                sell_price = items.get(item_name, 5) * 0.7
                self.player.inventory[item_name] -= 1
                self.player.coins += sell_price
                print(f"✅ Sold {item_name} for {sell_price:.1f} BC")

        if choice == "5":
            self.state = GameState.EXPLORING

    def combat(self):
        """Simple combat system"""
        print("\n⚔️ COMBAT!")
        enemy_health = 50 * (1 + self.current_location.danger)

        while enemy_health > 0 and self.player.health > 0:
            print(f"\nEnemy Health: {enemy_health:.0f}")
            print(f"Your Health: {self.player.health:.0f}")

            print("\n1. Attack")
            print("2. Defend")
            print("3. Use item")
            print("4. Flee")

            choice = input("Action: ").strip()

            if choice == "1":
                damage = random.uniform(5, 15) * (1 + self.player.coherence)
                enemy_health -= damage
                print(f"You deal {damage:.0f} damage!")

                if enemy_health > 0:
                    enemy_damage = random.uniform(3, 10) * (1 + self.current_location.danger)
                    self.player.health -= enemy_damage
                    print(f"Enemy deals {enemy_damage:.0f} damage!")
            elif choice == "2":
                enemy_damage = random.uniform(1, 5) * (1 + self.current_location.danger)
                self.player.health -= enemy_damage
                print(f"You defend! Enemy deals {enemy_damage:.0f} damage")
            elif choice == "3":
                if "Health Potion" in self.player.inventory and self.player.inventory["Health Potion"] > 0:
                    self.player.inventory["Health Potion"] -= 1
                    self.player.health = min(BASE_HEALTH, self.player.health + 30)
                    print("Used Health Potion! +30 health")
                else:
                    print("No items to use!")
            elif choice == "4":
                if random.random() < 0.5:
                    print("Escaped successfully!")
                    self.state = GameState.EXPLORING
                    return
                else:
                    print("Couldn't escape!")

        if enemy_health <= 0:
            reward = PHI * random.uniform(10, 20)
            self.player.coins += reward
            self.player.level += 1
            print(f"\n✨ VICTORY!")
            print(f"Earned {reward:.1f} BloomCoins!")
            print(f"Advanced to level {self.player.level}!")
        else:
            self.state = GameState.DEATH

        time.sleep(2)
        self.state = GameState.EXPLORING

    def victory(self):
        """Victory screen"""
        print(f"""
═══════════════════════════════════════════════════════
           T R A N S C E N D E N C E   A C H I E V E D
═══════════════════════════════════════════════════════

Congratulations, {self.player.name}!

You have achieved perfect coherence with the universe.
The golden ratio flows through your being.

Final Statistics:
- Coherence: {self.player.coherence:.3f}
- Level: {self.player.level}
- Coins: {self.player.coins:.1f}
- Turns: {self.turn_count}

Your journey is complete, but the spiral continues...

Press Enter to return to menu...
═══════════════════════════════════════════════════════
""")
        input()
        self.state = GameState.MENU

    def death(self):
        """Death screen"""
        print(f"""
═══════════════════════════════════════════════════════
              Y O U   H A V E   F A L L E N
═══════════════════════════════════════════════════════

Your oscillations have lost coherence.
{'Energy depleted.' if self.player.energy <= 0 else 'Health depleted.'}

Final Statistics:
- Level: {self.player.level}
- Coherence: {self.player.coherence:.3f}
- Turns survived: {self.turn_count}

The spiral awaits your return...

Press Enter to return to menu...
═══════════════════════════════════════════════════════
""")
        input()
        self.state = GameState.MENU

    def about(self):
        """About screen"""
        print("""
═══════════════ ABOUT BLOOMQUEST ═══════════════

BloomQuest Demo Version

A text-based adventure game demonstrating the integration
of blockchain concepts, mathematical harmony, and adaptive
gameplay using the BloomCoin v2 ecosystem.

Key Concepts:
• Golden Ratio (φ = 1.618...): All game constants derive from φ
• Coherence: Your synchronization with universal harmony
• BloomCoins: In-game currency following mathematical laws
• Archetypes: Character classes affecting narrative

This demo shows core mechanics. The full version includes:
- Blockchain persistence
- Learning AI that adapts to your playstyle
- Procedural narrative generation
- Multiplayer features
- NFT achievements

Press Enter to continue...
""")
        input()

def main():
    """Main entry point"""
    print("🌺 Welcome to BloomQuest Demo!")
    print("=" * 40)
    print("\nThis is a simplified, playable demo version")
    print("that demonstrates the core game concepts.\n")

    game = SimplifiedBloomQuest()

    try:
        game.start()
    except KeyboardInterrupt:
        print("\n\n🛑 Game interrupted.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
    finally:
        print("\nThank you for playing BloomQuest Demo!")
        print("May your oscillations find eternal coherence! ✨")

if __name__ == "__main__":
    main()