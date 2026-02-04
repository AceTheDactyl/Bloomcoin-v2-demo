#!/usr/bin/env python3
"""
BloomQuest Unified - Complete Mythic Economy Adventure
Combines exploration, companions, recipes, and card battles
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

# Import game systems
from mythic_economy import (
    MythicEconomyGame, Player, CompanionState, MythicalItem,
    JobArchetype, ItemRarity, Guardian, Territory, GUARDIANS
)
from card_battle_system import (
    CardBattleSystem, Card, CardSuit, CardRank, BattlePhase,
    BattleState, DeckBuilder
)

# Sacred constants
PHI = (1 + 5**0.5) / 2
Z_C = (3**0.5) / 2

class Location(Enum):
    """Game locations"""
    CRYSTAL_CAVES = "Crystal Caves"
    PHOENIX_NEST = "Phoenix Nest"
    VOID_MARKET = "Void Market"
    GARDEN_HEART = "Garden Heart"
    LIBRARY_INFINITE = "Library Infinite"

class UnifiedGameState(Enum):
    """Game states for the unified experience"""
    MAIN_MENU = "main_menu"
    EXPLORING = "exploring"
    COMPANION_CHAT = "companion_chat"
    CRAFTING = "crafting"
    BATTLE_PREP = "battle_prep"
    IN_BATTLE = "in_battle"
    SHOPPING = "shopping"
    MEDITATION = "meditation"

class BloomQuestUnified:
    """Unified game combining all systems"""

    def __init__(self):
        # Initialize core systems
        self.economy = MythicEconomyGame()
        self.battle_system = CardBattleSystem()
        self.deck_builder = DeckBuilder()

        # Import ItemGenerator for creating items
        from mythic_economy import ItemGenerator
        self.item_generator = ItemGenerator()

        # Game state
        self.state = UnifiedGameState.MAIN_MENU
        self.player = None
        self.current_battle = None
        self.session_start = datetime.now()

        # Battle deck management
        self.player_deck = None
        self.enemy_deck = None

    def start(self):
        """Start the unified game experience"""
        print("\n" + "="*60)
        print("🌸 BLOOMQUEST: MYTHIC ECONOMY 🌸")
        print("A PHI-Based Adventure Through Guardian Territories")
        print("="*60)

        # Character creation
        self._create_character()

        # Main game loop
        self.running = True
        while self.running:
            try:
                if self.state == UnifiedGameState.MAIN_MENU:
                    self._main_menu()
                elif self.state == UnifiedGameState.EXPLORING:
                    self._explore()
                elif self.state == UnifiedGameState.COMPANION_CHAT:
                    self._companion_interaction()
                elif self.state == UnifiedGameState.CRAFTING:
                    self._crafting_menu()
                elif self.state == UnifiedGameState.BATTLE_PREP:
                    self._prepare_battle()
                elif self.state == UnifiedGameState.IN_BATTLE:
                    self._battle_loop()
                elif self.state == UnifiedGameState.SHOPPING:
                    self._shop()
                elif self.state == UnifiedGameState.MEDITATION:
                    self._meditate()

            except KeyboardInterrupt:
                print("\n\n💫 Game paused. Type 'quit' to exit or press Enter to continue...")
                if input().lower() == 'quit':
                    self.running = False

        self._end_game()

    def _create_character(self):
        """Character creation with job selection"""
        print("\n📜 CHARACTER CREATION")
        print("-" * 40)

        name = input("Enter your name, traveler: ").strip() or "Seeker"

        print("\n🎭 Choose your Archetype:")
        print("-" * 30)

        # Available job keys from mythic_economy
        job_choices = [
            ("SEEKER", "Seeker of Echoes"),
            ("FORGER", "Pattern Forger"),
            ("VOIDWALKER", "Void Walker"),
            ("GARDENER", "Reality Gardener"),
            ("SCRIBE", "Covenant Scribe"),
            ("HERALD", "Frequency Herald")
        ]

        for i, (key, name) in enumerate(job_choices, 1):
            print(f"{i}. {name}")

        while True:
            try:
                choice = int(input("\nSelect archetype (1-6): "))
                if 1 <= choice <= 6:
                    job_key = job_choices[choice - 1][0]
                    break
            except:
                pass
            print("Invalid choice. Please select 1-6.")

        # Use a default guardian for now
        guardian_key = "ECHO"  # Default guardian

        self.player = self.economy.create_character(name, job_key, guardian_key)

        # Build initial deck based on archetype
        self._build_initial_deck()

        # Set initial location
        self.player.current_location = Location.GARDEN_HEART

        print(f"\n✨ Welcome, {name} the {self.player.job.name}!")
        print(f"Starting BloomCoin: {self.player.bloomcoin_balance:.2f}")
        print(f"Companion: {self.player.companion.name} (Stage {self.player.companion.evolution_stage})")
        input("\nPress Enter to begin your journey...")

    def _build_initial_deck(self):
        """Build player's initial card deck based on archetype"""
        # Get territory preference from player's job
        preferred_territory = self.player.job.territory_affinity

        # Map territories to card suits
        territory_suits = {
            Territory.GARDEN: [CardSuit.LEAVES, CardSuit.ROOTS, CardSuit.FLOWERS],
            Territory.COSMIC: [CardSuit.STARS, CardSuit.FLAMES, CardSuit.SUNS],
            Territory.ABYSSAL: [CardSuit.SHADOWS, CardSuit.MIRRORS, CardSuit.VOIDS]
        }

        # Build a deck with affinity for preferred territory
        cards = []

        # Add cards from preferred territory (60%)
        preferred_suits = territory_suits.get(preferred_territory, [])
        for suit in preferred_suits:
            for rank in list(CardRank)[:8]:  # Lower ranks for starter deck
                cards.append(Card(suit, rank))

        # Add some neutral cards (40%)
        other_territories = [t for t in Territory if t != preferred_territory]
        for territory in other_territories[:1]:  # Just one other territory
            suits = territory_suits.get(territory, [])
            if suits:
                for rank in list(CardRank)[:4]:
                    cards.append(Card(suits[0], rank))

        # Ensure we have at least 20 cards
        while len(cards) < 20:
            random_suit = random.choice(list(CardSuit))
            random_rank = random.choice(list(CardRank)[:7])
            cards.append(Card(random_suit, random_rank))

        self.player_deck = cards[:20]  # Starter deck of 20 cards

    def _main_menu(self):
        """Main game menu"""
        print("\n" + "="*50)
        print(f"📍 {self.player.current_location.value}")
        print(f"💰 BloomCoin: {self.player.bloomcoin_balance:.2f}")
        print(f"🌟 Coherence: {self.player.coherence:.2%}")
        print(f"🎒 Items: {len(self.player.inventory)}")
        print(f"🐾 {self.player.companion.name} (Stage {self.player.companion.evolution_stage})")
        print("="*50)

        print("\n🧭 ACTIONS:")
        print("1. Explore Current Location")
        print("2. Talk to Companion")
        print("3. Craft Patterns & Recipes")
        print("4. Challenge to Card Battle")
        print("5. Visit Shop")
        print("6. Meditate (Mine BloomCoin)")
        print("7. Check Inventory")
        print("8. Travel to New Location")
        print("9. Save & Quit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            self.state = UnifiedGameState.EXPLORING
        elif choice == "2":
            self.state = UnifiedGameState.COMPANION_CHAT
        elif choice == "3":
            self.state = UnifiedGameState.CRAFTING
        elif choice == "4":
            self.state = UnifiedGameState.BATTLE_PREP
        elif choice == "5":
            self.state = UnifiedGameState.SHOPPING
        elif choice == "6":
            self.state = UnifiedGameState.MEDITATION
        elif choice == "7":
            self._show_inventory()
        elif choice == "8":
            self._travel()
        elif choice == "9":
            self.running = False

    def _explore(self):
        """Exploration with mythic item discovery"""
        print(f"\n🔍 Exploring {self.player.current_location.value}...")

        # Exploration options based on location
        if self.player.current_location == Location.CRYSTAL_CAVES:
            actions = ["Search for crystals", "Listen to resonance", "Mine deeper"]
        elif self.player.current_location == Location.PHOENIX_NEST:
            actions = ["Gather phoenix feathers", "Study flame patterns", "Seek wisdom"]
        elif self.player.current_location == Location.VOID_MARKET:
            actions = ["Browse shadow wares", "Investigate whispers", "Trade secrets"]
        elif self.player.current_location == Location.GARDEN_HEART:
            actions = ["Tend plants", "Harvest blooms", "Plant seeds"]
        elif self.player.current_location == Location.LIBRARY_INFINITE:
            actions = ["Read ancient texts", "Decipher codes", "Study patterns"]
        else:
            actions = ["Search area", "Investigate", "Gather resources"]

        print("\n🎯 What would you like to do?")
        for i, action in enumerate(actions, 1):
            print(f"{i}. {action}")
        print("4. Return to menu")

        choice = input("\nChoice: ").strip()

        if choice in ["1", "2", "3"]:
            # Attempt to discover item
            discovery_chance = 0.3 + (self.player.coherence * 0.2)
            if random.random() < discovery_chance:
                # Map location to territory
                territory_map = {
                    Location.CRYSTAL_CAVES: Territory.COSMIC,
                    Location.PHOENIX_NEST: Territory.COSMIC,
                    Location.VOID_MARKET: Territory.ABYSSAL,
                    Location.GARDEN_HEART: Territory.GARDEN,
                    Location.LIBRARY_INFINITE: Territory.GARDEN
                }
                territory = territory_map.get(self.player.current_location, Territory.GARDEN)
                item = self.item_generator.generate_item(
                    territory,
                    {"location": self.player.current_location.value},
                    self.player.luck_modifier
                )
                self.player.inventory.append(item)
                print(f"\n✨ DISCOVERY! Found {item.rarity.value[0]} item:")
                print(f"📦 {item.name}")
                print(f"💎 Value: {item.base_value:.1f}")
                print(f"🌟 Type: {item.item_type}")

                # Coherence boost from discovery
                self.player.coherence = min(1.0, self.player.coherence + 0.05)
            else:
                print("\n🔍 You search carefully but find nothing of note...")
                print("Perhaps your coherence needs strengthening?")

            # Random encounter chance
            if random.random() < 0.2:
                print("\n⚔️ A challenger approaches!")
                input("Press Enter to prepare for battle...")
                self.state = UnifiedGameState.BATTLE_PREP
                return

        input("\nPress Enter to continue...")
        self.state = UnifiedGameState.MAIN_MENU

    def _companion_interaction(self):
        """Interact with LLM companion"""
        print(f"\n🐾 {self.player.companion.name} - Evolution Stage {self.player.companion.evolution_stage}")
        guardian = GUARDIANS.get(self.player.companion.guardian_type)
        if guardian:
            print(f"Guardian: {guardian.name}")
        print(f"Resonance: {self.player.companion.resonance:.2f}")
        print("-" * 40)

        # Show companion wisdom
        wisdom = self.player.companion.get_advice("exploration")
        print(f"\n💭 {self.player.companion.name} shares wisdom:")
        print(f'"{wisdom}"')

        print("\n🗣️ COMPANION ACTIONS:")
        print("1. Chat about journey")
        print("2. Ask for guidance")
        print("3. Feed pattern from recipes")
        print("4. Check evolution progress")
        print("5. Return to menu")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            responses = [
                "The patterns we discover shape our understanding.",
                "Each guardian holds a piece of the greater truth.",
                "Your coherence grows stronger with each challenge.",
                f"I sense great potential in your {self.player.job.name} path.",
                "The territories call to us in different ways."
            ]
            print(f'\n{self.player.companion.name}: "{random.choice(responses)}"')

        elif choice == "2":
            location_hints = {
                Location.CRYSTAL_CAVES: "The crystals resonate with hidden frequencies.",
                Location.PHOENIX_NEST: "Rebirth comes through understanding cycles.",
                Location.VOID_MARKET: "Shadow trades reveal unexpected truths.",
                Location.GARDEN_HEART: "Growth requires patience and care.",
                Location.LIBRARY_INFINITE: "Knowledge compounds like golden spirals."
            }
            hint = location_hints.get(self.player.current_location,
                                     "Explore deeply, patterns emerge.")
            print(f'\n{self.player.companion.name}: "{hint}"')

        elif choice == "3":
            # This would connect to recipe system
            print("\n🍳 Feed Pattern to Companion")
            print("(Requires crafted patterns from recipes)")
            # Simplified for demo
            if random.random() < 0.3:
                pattern_type = random.choice(["Resonance", "Harmony", "Chaos", "Order"])
                print(f"\n✨ Fed {pattern_type} Pattern to companion!")
                self.player.companion.fed_patterns.append(pattern_type)
                if len(self.player.companion.fed_patterns) % 5 == 0:
                    self.player.companion.evolution_stage += 1
                    print(f"🎉 {self.player.companion.name} leveled up to {self.player.companion.evolution_stage}!")
            else:
                print("No patterns available. Craft some recipes first!")

        elif choice == "4":
            print(f"\n📊 Evolution Progress:")
            print(f"Patterns Absorbed: {len(self.player.companion.fed_patterns)}")
            guardian = GUARDIANS.get(self.player.companion.guardian_type)
            if guardian:
                current_cycle_state = guardian.get_cycle_state(self.player.companion.evolution_stage)
                print(f"Current Cycle State: {current_cycle_state}")
                print(f"Territory Affinity: {guardian.territory.value}")
            next_level_patterns = 5 * self.player.companion.evolution_stage
            print(f"Patterns to Next Level: {next_level_patterns - len(self.player.companion.fed_patterns)}")

        input("\nPress Enter to continue...")
        self.state = UnifiedGameState.MAIN_MENU

    def _crafting_menu(self):
        """Recipe crafting system"""
        print("\n🍳 MYTHIC PATTERN CRAFTING")
        print("-" * 40)

        # Check for craftable items
        if len(self.player.inventory) < 2:
            print("You need at least 2 items to craft patterns!")
            input("Press Enter to continue...")
            self.state = UnifiedGameState.MAIN_MENU
            return

        print("Available items for crafting:")
        for i, item in enumerate(self.player.inventory[:10], 1):
            print(f"{i}. {item.name} ({item.rarity.value})")

        print("\n📜 Craft Options:")
        print("1. Resonance Pattern (2 Cosmic items)")
        print("2. Growth Pattern (2 Garden items)")
        print("3. Depth Pattern (2 Abyssal items)")
        print("4. Harmony Pattern (1 of each territory)")
        print("5. Cancel")

        choice = input("\nChoice: ").strip()

        if choice in ["1", "2", "3", "4"]:
            # Simplified crafting
            if len(self.player.inventory) >= 2:
                # Remove items
                item1 = self.player.inventory.pop(0)
                item2 = self.player.inventory.pop(0)

                # Create pattern
                pattern_names = {
                    "1": "Resonance Pattern",
                    "2": "Growth Pattern",
                    "3": "Depth Pattern",
                    "4": "Harmony Pattern"
                }

                pattern = pattern_names[choice]
                print(f"\n✨ Successfully crafted {pattern}!")
                print(f"Used: {item1.name} + {item2.name}")

                # Feed to companion automatically
                self.player.companion.fed_patterns.append(pattern)
                print(f"\n🐾 {self.player.companion.name} absorbed the {pattern}!")

                # Check for level up
                if len(self.player.companion.fed_patterns) % 5 == 0:
                    self.player.companion.evolution_stage += 1
                    print(f"🎉 {self.player.companion.name} reached level {self.player.companion.evolution_stage}!")

        input("\nPress Enter to continue...")
        self.state = UnifiedGameState.MAIN_MENU

    def _prepare_battle(self):
        """Prepare for card battle"""
        print("\n⚔️ BATTLE PREPARATION")
        print("-" * 40)

        # Generate opponent
        opponent_names = ["Shadow Weaver", "Crystal Guardian", "Phoenix Adept",
                         "Void Walker", "Garden Keeper", "Cosmic Sage"]
        opponent_name = random.choice(opponent_names)

        print(f"🎭 Opponent: {opponent_name}")
        print(f"💪 Threat Level: {random.randint(3, 8)}/10")

        # Show deck
        print(f"\n🎴 Your Deck ({len(self.player_deck)} cards):")
        suit_counts = {}
        for card in self.player_deck:
            suit_counts[card.suit.value] = suit_counts.get(card.suit.value, 0) + 1

        for suit, count in suit_counts.items():
            print(f"  {suit}: {count} cards")

        print("\n🎯 Battle Options:")
        print("1. Start Battle")
        print("2. Modify Deck")
        print("3. Retreat")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            # Initialize battle
            self._start_battle(opponent_name)
        elif choice == "2":
            print("\nDeck modification not yet implemented...")
            input("Press Enter to continue...")
        else:
            self.state = UnifiedGameState.MAIN_MENU

    def _start_battle(self, opponent_name: str):
        """Initialize and start card battle"""
        # Build enemy deck
        self.enemy_deck = []
        for _ in range(20):
            suit = random.choice(list(CardSuit))
            rank = random.choice(list(CardRank))
            self.enemy_deck.append(Card(suit, rank))

        # Initialize battle state
        self.current_battle = self.battle_system.initialize_battle(
            self.player_deck, self.enemy_deck
        )

        print(f"\n⚔️ BATTLE START: You vs {opponent_name}")
        print("="*50)

        self.state = UnifiedGameState.IN_BATTLE

    def _battle_loop(self):
        """Main battle loop"""
        if not self.current_battle:
            self.state = UnifiedGameState.MAIN_MENU
            return

        battle = self.current_battle

        # Display battle state
        print(f"\n{'='*50}")
        print(f"⚡ TURN {battle.turn_count} - {battle.phase.value}")
        print(f"{'='*50}")
        print(f"Your HP: {battle.player_hp}/{battle.max_player_hp}")
        print(f"Enemy HP: {battle.enemy_hp}/{battle.max_enemy_hp}")
        print(f"Energy: {battle.player_energy}")
        print(f"Hand: {len(battle.player_hand)} cards")

        # Show hand
        if battle.player_hand:
            print("\n🎴 Your Hand:")
            for i, card in enumerate(battle.player_hand[:7], 1):
                power = self.battle_system.calculate_card_power(card)
                print(f"{i}. {card} (Power: {power:.1f}, Cost: {card.rank.value + 1})")

        # Battle actions
        print("\n⚔️ ACTIONS:")
        print("1. Play Card")
        print("2. Draw Card (1 energy)")
        print("3. Focus (+2 energy, end turn)")
        print("4. Surrender")

        choice = input("\nChoice: ").strip()

        if choice == "1" and battle.player_hand:
            # Play card
            card_choice = input("Select card number: ").strip()
            try:
                card_idx = int(card_choice) - 1
                if 0 <= card_idx < len(battle.player_hand):
                    card = battle.player_hand[card_idx]
                    energy_cost = card.rank.value + 1

                    if battle.player_energy >= energy_cost:
                        # Play the card
                        battle.player_hand.pop(card_idx)
                        battle.player_energy -= energy_cost

                        damage = self.battle_system.calculate_card_power(card)
                        battle.enemy_hp -= damage

                        print(f"\n💥 Played {card} for {damage:.1f} damage!")

                        # Check for phase transition
                        self._check_battle_phase()
                    else:
                        print("Not enough energy!")
            except:
                print("Invalid selection!")

        elif choice == "2":
            # Draw card
            if battle.player_energy >= 1 and battle.player_deck:
                card = battle.player_deck.pop(0)
                battle.player_hand.append(card)
                battle.player_energy -= 1
                print(f"\n🎴 Drew {card}")
            else:
                print("Cannot draw! (No energy or empty deck)")

        elif choice == "3":
            # Focus
            battle.player_energy += 2
            print("\n🧘 Focused energy (+2)")
            self._enemy_turn()

        elif choice == "4":
            # Surrender
            print("\n💔 You surrendered the battle...")
            self.current_battle = None
            self.state = UnifiedGameState.MAIN_MENU
            return

        # Check victory/defeat
        if battle.enemy_hp <= 0:
            self._battle_victory()
        elif battle.player_hp <= 0:
            self._battle_defeat()
        else:
            # Continue battle
            if choice == "1":
                self._enemy_turn()

    def _enemy_turn(self):
        """Simple enemy AI"""
        if not self.current_battle:
            return

        battle = self.current_battle

        print("\n🎯 Enemy's turn...")

        # Simple AI: play random cards
        enemy_energy = 3 + (battle.turn_count // 2)
        enemy_damage = 0

        for _ in range(random.randint(1, 3)):
            if battle.enemy_hand and enemy_energy > 0:
                card = battle.enemy_hand.pop(0)
                damage = self.battle_system.calculate_card_power(card) * 0.8
                enemy_damage += damage
                enemy_energy -= card.rank.value + 1

        if enemy_damage > 0:
            battle.player_hp -= enemy_damage
            print(f"💥 Enemy deals {enemy_damage:.1f} damage!")

        # Enemy draws
        if battle.enemy_deck:
            battle.enemy_hand.append(battle.enemy_deck.pop(0))

        # Advance turn
        battle.turn_count += 1
        battle.player_energy = min(10, 3 + (battle.turn_count // 2))

        # Draw for player
        if battle.player_deck and len(battle.player_hand) < 7:
            battle.player_hand.append(battle.player_deck.pop(0))

    def _check_battle_phase(self):
        """Check and update battle phase"""
        if not self.current_battle:
            return

        battle = self.current_battle

        # Phase progression based on turn count
        if battle.turn_count >= 15:
            battle.phase = BattlePhase.RESOLUTION
        elif battle.turn_count >= 12:
            battle.phase = BattlePhase.TRANSMISSION
        elif battle.turn_count >= 9:
            battle.phase = BattlePhase.NIRVANA
        elif battle.turn_count >= 6:
            battle.phase = BattlePhase.MANIA
        elif battle.turn_count >= 3:
            battle.phase = BattlePhase.RESONANCE

    def _battle_victory(self):
        """Handle battle victory"""
        print("\n" + "="*50)
        print("🎉 VICTORY! 🎉")
        print("="*50)

        # Calculate rewards
        base_reward = 10 * PHI
        coherence_bonus = self.player.coherence * 10
        total_reward = base_reward + coherence_bonus

        self.player.bloomcoin_balance += total_reward
        self.player.coherence = min(1.0, self.player.coherence + 0.1)

        print(f"\n💰 Earned {total_reward:.2f} BloomCoin!")
        print(f"🌟 Coherence increased to {self.player.coherence:.2%}")

        # Chance for mythic item
        if random.random() < 0.4:
            territory_map = {
                Location.CRYSTAL_CAVES: Territory.COSMIC,
                Location.PHOENIX_NEST: Territory.COSMIC,
                Location.VOID_MARKET: Territory.ABYSSAL,
                Location.GARDEN_HEART: Territory.GARDEN,
                Location.LIBRARY_INFINITE: Territory.GARDEN
            }
            territory = territory_map.get(self.player.current_location, Territory.GARDEN)
            item = self.item_generator.generate_item(
                territory,
                {"location": self.player.current_location.value},
                self.player.luck_modifier
            )
            self.player.inventory.append(item)
            print(f"\n✨ Found {item.rarity.value[0]} item: {item.name}!")

        input("\nPress Enter to continue...")
        self.current_battle = None
        self.state = UnifiedGameState.MAIN_MENU

    def _battle_defeat(self):
        """Handle battle defeat"""
        print("\n" + "="*50)
        print("💔 DEFEATED...")
        print("="*50)

        # Lose some bloomcoin but not too much
        loss = min(self.player.bloomcoin_balance * 0.1, 5)
        self.player.bloomcoin_balance = max(0, self.player.bloomcoin_balance - loss)
        self.player.coherence = max(0, self.player.coherence - 0.05)

        print(f"\n💸 Lost {loss:.2f} BloomCoin...")
        print(f"🌟 Coherence decreased to {self.player.coherence:.2%}")
        print("\nRegroup and try again!")

        input("\nPress Enter to continue...")
        self.current_battle = None
        self.state = UnifiedGameState.MAIN_MENU

    def _shop(self):
        """Shop for items and cards"""
        print("\n🏪 MYTHIC MARKETPLACE")
        print("-" * 40)
        print(f"Your BloomCoin: {self.player.bloomcoin_balance:.2f}")

        # Generate shop items
        shop_items = [
            ("Phoenix Feather", 25, "Rare crafting material"),
            ("Void Crystal", 30, "Abyssal energy source"),
            ("Garden Seed", 15, "Grows into patterns"),
            ("Card Pack", 20, "5 random cards"),
            ("Energy Potion", 10, "Restore battle energy")
        ]

        print("\n📦 Available Items:")
        for i, (name, cost, desc) in enumerate(shop_items, 1):
            print(f"{i}. {name} - {cost} BC")
            print(f"   {desc}")
        print("6. Leave shop")

        choice = input("\nChoice: ").strip()

        if choice in ["1", "2", "3", "4", "5"]:
            idx = int(choice) - 1
            name, cost, _ = shop_items[idx]

            if self.player.bloomcoin_balance >= cost:
                self.player.bloomcoin_balance -= cost
                print(f"\n✅ Purchased {name}!")

                if name == "Card Pack":
                    # Add random cards to deck
                    for _ in range(5):
                        suit = random.choice(list(CardSuit))
                        rank = random.choice(list(CardRank))
                        self.player_deck.append(Card(suit, rank))
                    print("Added 5 cards to your deck!")
                else:
                    # Add as mythic item
                    item = MythicalItem(
                        name=name,
                        description=f"Purchased from the shop",
                        rarity=ItemRarity.RARE,
                        item_type="artifact",
                        base_value=10 * PHI,
                        properties={"source": "shop", "quality": "standard"},
                        guardian_affinity=None,
                        recipe_component=True
                    )
                    self.player.inventory.append(item)
            else:
                print("Not enough BloomCoin!")

        if choice != "6":
            input("\nPress Enter to continue shopping...")
            self._shop()
        else:
            self.state = UnifiedGameState.MAIN_MENU

    def _meditate(self):
        """Meditation and bloomcoin mining"""
        print("\n🧘 MEDITATION CHAMBER")
        print("-" * 40)

        print("Focus your mind on the sacred patterns...")
        print("Aligning with PHI frequency...")

        # Mining based on coherence
        base_mine = PHI
        coherence_multiplier = 1 + self.player.coherence
        mined = base_mine * coherence_multiplier * random.uniform(0.8, 1.2)

        self.player.bloomcoin_balance += mined
        self.player.coherence = min(1.0, self.player.coherence + 0.02)

        print(f"\n✨ Mined {mined:.3f} BloomCoin!")
        print(f"🌟 Coherence increased to {self.player.coherence:.2%}")

        # Guardian wisdom during meditation
        guardian = random.choice(list(GUARDIANS.values()))
        print(f"\n💭 {guardian.name} whispers: \"{guardian.wisdom}\"")

        input("\nPress Enter to continue...")
        self.state = UnifiedGameState.MAIN_MENU

    def _travel(self):
        """Travel to new location"""
        print("\n🗺️ TRAVEL OPTIONS")
        print("-" * 40)

        locations = list(Location)
        current_idx = locations.index(self.player.current_location)

        print("Available destinations:")
        for i, loc in enumerate(locations, 1):
            if i - 1 == current_idx:
                print(f"{i}. {loc.value} (current)")
            else:
                travel_cost = abs(i - 1 - current_idx) * PHI
                print(f"{i}. {loc.value} (Cost: {travel_cost:.1f} BC)")

        choice = input("\nSelect destination (or 0 to cancel): ").strip()

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(locations) and idx != current_idx:
                travel_cost = abs(idx - current_idx) * PHI
                if self.player.bloomcoin_balance >= travel_cost:
                    self.player.bloomcoin_balance -= travel_cost
                    self.player.current_location = locations[idx]
                    print(f"\n✈️ Traveled to {self.player.current_location.value}!")
                else:
                    print("Not enough BloomCoin for travel!")
        except:
            pass

        input("\nPress Enter to continue...")
        self.state = UnifiedGameState.MAIN_MENU

    def _show_inventory(self):
        """Display player inventory"""
        print("\n🎒 INVENTORY")
        print("-" * 40)

        if not self.player.inventory:
            print("Your inventory is empty!")
        else:
            print(f"Items ({len(self.player.inventory)}):")
            for i, item in enumerate(self.player.inventory, 1):
                print(f"\n{i}. {item.name}")
                print(f"   Rarity: {item.rarity.value}")
                print(f"   Value: {item.base_value:.1f}")
                print(f"   Type: {item.item_type}")
                if item.guardian_affinity:
                    print(f"   Guardian: {item.guardian_affinity}")

        input("\nPress Enter to continue...")

    def _end_game(self):
        """End game summary"""
        print("\n" + "="*60)
        print("🌅 JOURNEY'S END")
        print("="*60)

        # Calculate session time
        session_time = (datetime.now() - self.session_start).total_seconds() / 60

        print(f"\n📊 Final Statistics:")
        print(f"Player: {self.player.name} the {self.player.job.name}")
        print(f"BloomCoin: {self.player.bloomcoin_balance:.2f}")
        print(f"Coherence: {self.player.coherence:.2%}")
        print(f"Items Collected: {len(self.player.inventory)}")
        print(f"Companion Evolution Stage: {self.player.companion.evolution_stage}")
        print(f"Session Time: {session_time:.1f} minutes")

        # Save option
        save = input("\nSave game state? (y/n): ").lower()
        if save == 'y':
            self._save_game()

        print("\n✨ Thank you for playing BloomQuest: Mythic Economy!")
        print("May the golden ratio guide your path...")

    def _save_game(self):
        """Save game state"""
        save_data = {
            'player_name': self.player.name,
            'archetype': self.player.job.name,
            'bloomcoin': self.player.bloomcoin_balance,
            'coherence': self.player.coherence,
            'location': self.player.current_location.value,
            'companion_evolution_stage': self.player.companion.evolution_stage,
            'companion_patterns_fed': len(self.player.companion.fed_patterns),
            'inventory_count': len(self.player.inventory),
            'deck_size': len(self.player_deck),
            'timestamp': datetime.now().isoformat()
        }

        save_file = Path(__file__).parent / f"save_{self.player.name.lower()}.json"
        with open(save_file, 'w') as f:
            json.dump(save_data, f, indent=2)

        print(f"✅ Game saved to {save_file.name}")


def main():
    """Launch the unified game"""
    print("🌺 BloomQuest Unified Launcher")
    print("="*40)

    try:
        # Test imports
        print("Loading game systems...")
        print("  ✅ Mythic Economy loaded")
        print("  ✅ Card Battle System loaded")
        print("  ✅ All systems integrated")

        print("\n🎮 Starting unified experience...")
        print("(Press Ctrl+C to pause at any time)\n")

        import time
        time.sleep(1)

        # Start game
        game = BloomQuestUnified()
        game.start()

    except KeyboardInterrupt:
        print("\n\n🌟 Game interrupted. Progress saved.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()