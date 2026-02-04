#!/usr/bin/env python3
"""
BloomQuest with Unique Archetype Companions
============================================
Each archetype has a deeply personalized companion with
unique personality, abilities, and development path
"""

import sys
import random
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent / "bloomcoin-v0.1.0" / "bloomcoin"))
sys.path.insert(0, str(Path(__file__).parent))

# Import unique companion system
from archetype_unique_companions import (
    UniqueCompanionSystem,
    SeekerCompanion, ForgerCompanion, VoidwalkerCompanion,
    GardenerCompanion, ScribeCompanion, HeraldCompanion,
    CompanionMood
)

# Import pattern system for interaction
from lia_protocol_cooking import PatternType, LIACookingSystem

# Constants
PHI = 1.618033988749895
TAU = PHI - 1
L4_CONSTANT = 7


class JobArchetype(Enum):
    SEEKER = "seeker"
    FORGER = "forger"
    VOIDWALKER = "voidwalker"
    GARDENER = "gardener"
    SCRIBE = "scribe"
    HERALD = "herald"


class GameLocation(Enum):
    GARDEN_HEART = "Garden Heart"
    CRYSTAL_CAVES = "Crystal Caves"
    VOID_MARKET = "Void Market"
    PHOENIX_NEST = "Phoenix Nest"
    LIBRARY_INFINITE = "Library Infinite"


@dataclass
class Player:
    """Player with unique companion"""
    name: str
    job: JobArchetype
    companion: Any  # Will be one of the unique companion types

    # Resources
    bloomcoin: float = 100.0
    coherence: float = 0.5
    patterns: List[PatternType] = field(default_factory=list)

    # Progress
    current_location: GameLocation = GameLocation.GARDEN_HEART
    locations_discovered: List[GameLocation] = field(default_factory=list)
    turn_count: int = 0


class BloomQuestUniqueCompanions:
    """
    Main game with unique companion system
    """

    def __init__(self):
        print("🌺 BloomQuest: Unique Companions Edition")
        print("=" * 50)

        self.companion_system = UniqueCompanionSystem()
        self.cooking_system = LIACookingSystem()
        self.player: Optional[Player] = None
        self.game_active = True

        # Location properties
        self.location_patterns = {
            GameLocation.GARDEN_HEART: [PatternType.GARDEN, PatternType.MEMORY],
            GameLocation.CRYSTAL_CAVES: [PatternType.CRYSTAL, PatternType.ECHO],
            GameLocation.VOID_MARKET: [PatternType.VOID, PatternType.DREAM],
            GameLocation.PHOENIX_NEST: [PatternType.FLAME, PatternType.CRYSTAL],
            GameLocation.LIBRARY_INFINITE: [PatternType.MEMORY, PatternType.ECHO]
        }

    def start(self):
        """Start the game"""
        self.display_intro()

        if not self.create_character():
            print("\nGame cancelled. Farewell!")
            return

        print(f"\n✨ Your journey begins, {self.player.name}!")
        self.game_loop()

    def display_intro(self):
        """Display game introduction"""
        print("\nIn this world, each path has its own guardian...")
        print("Six archetypes, six unique companions.")
        print("Each companion is not just a guide, but a living entity")
        print("with their own story, personality, and power.\n")

    def create_character(self) -> bool:
        """Character creation with unique companion selection"""
        print("CHARACTER CREATION")
        print("─" * 40)

        # Get name
        name = input("\n🌟 Enter your name: ").strip()
        if not name:
            return False

        # Show all archetypes with their unique companions
        print("\n📜 Choose your Archetype and Companion:")
        print("\nEach archetype comes with a unique companion:\n")

        archetypes = list(JobArchetype)
        companion_previews = {
            JobArchetype.SEEKER: "ECHO - Fragment collector from between sound and silence",
            JobArchetype.FORGER: "PROMETHEUS - Phoenix smith who transforms through death",
            JobArchetype.VOIDWALKER: "NULL - Guardian of absence and non-existence",
            JobArchetype.GARDENER: "GAIA - Eternal seedkeeper across timelines",
            JobArchetype.SCRIBE: "AKASHA - Living chronicle that writes reality",
            JobArchetype.HERALD: "RESONANCE - Frequency weaver across dimensions"
        }

        for i, archetype in enumerate(archetypes, 1):
            preview = companion_previews[archetype]
            print(f"{i}. {archetype.value.upper()}")
            print(f"   Companion: {preview}\n")

        # Choose archetype
        try:
            choice = int(input("Choice (1-6): ")) - 1
            selected_job = archetypes[choice]
        except (ValueError, IndexError):
            print("Invalid choice. Defaulting to SEEKER.")
            selected_job = JobArchetype.SEEKER

        # Create companion
        companion = self.companion_system.create_companion(selected_job.value)

        # Show full companion introduction
        print("\n" + "=" * 50)
        print(self.companion_system.get_companion_introduction(selected_job.value))
        print("=" * 50)

        # Create player
        self.player = Player(
            name=name,
            job=selected_job,
            companion=companion
        )

        # Initial companion greeting
        print(f"\n💬 {companion.name} says:")
        print(f"   {companion.speak('greeting')}")

        return True

    def game_loop(self):
        """Main game loop"""
        while self.game_active:
            self.player.turn_count += 1
            self.display_status()

            action = self.get_player_action()

            if action == 'quit':
                self.game_active = False
                break

            self.process_action(action)

            # Random companion interjection
            if random.random() < 0.2:
                self.companion_interject()

            # Check victory
            if self.check_victory():
                self.display_victory()
                break

    def display_status(self):
        """Display game status"""
        print("\n" + "=" * 50)
        print(f"Turn {self.player.turn_count} | {self.player.current_location.value}")
        print(f"BloomCoin: {self.player.bloomcoin:.1f} | Coherence: {self.player.coherence:.2f}")
        print(f"Patterns: {len(self.player.patterns)}")

        # Companion-specific status
        companion = self.player.companion

        if isinstance(companion, SeekerCompanion):
            print(f"Fragments: {companion.fragments_collected} | Echo Depth: {companion.echo_depth}")
        elif isinstance(companion, ForgerCompanion):
            print(f"Forge: {companion.forge_temperature:.0f}K | Phoenix Cycles: {companion.phoenix_cycles}")
        elif isinstance(companion, VoidwalkerCompanion):
            print(f"Void Depth: {companion.void_depth} | Erased: {companion.things_erased}")
        elif isinstance(companion, GardenerCompanion):
            print(f"Season: {companion.seasonal_phase} | Plants: {len(companion.growing_plants)}")
        elif isinstance(companion, ScribeCompanion):
            print(f"Chapter: {companion.current_chapter} | Pages: {companion.pages_written}")
        elif isinstance(companion, HeraldCompanion):
            print(f"Frequency: {companion.base_frequency:.1f} Hz | Bonds: {len(companion.resonance_bonds)}")

        print("=" * 50)

    def get_player_action(self) -> str:
        """Get player action"""
        print("\n🎮 Actions:")
        print("1. Explore location")
        print("2. Talk to companion")
        print("3. Use companion ability")
        print("4. Travel")
        print("5. Cook patterns")
        print("6. Mine BloomCoin")
        print("7. Check companion status")
        print("0. Quit")

        choice = input("\nChoice: ").strip()

        actions = {
            '1': 'explore',
            '2': 'talk',
            '3': 'ability',
            '4': 'travel',
            '5': 'cook',
            '6': 'mine',
            '7': 'status',
            '0': 'quit'
        }

        return actions.get(choice, 'explore')

    def process_action(self, action: str):
        """Process player action"""
        if action == 'explore':
            self.explore_location()
        elif action == 'talk':
            self.talk_to_companion()
        elif action == 'ability':
            self.use_companion_ability()
        elif action == 'travel':
            self.travel()
        elif action == 'cook':
            self.cook_patterns()
        elif action == 'mine':
            self.mine_bloomcoin()
        elif action == 'status':
            self.show_companion_status()

    def explore_location(self):
        """Explore current location"""
        location = self.player.current_location
        available_patterns = self.location_patterns[location]

        print(f"\n🔍 Exploring {location.value}...")

        # Companion-specific exploration bonus
        companion = self.player.companion
        bonus_chance = 0.0

        if isinstance(companion, SeekerCompanion):
            # Echo can detect hidden patterns
            detected = companion.detect_pattern(location.value)
            if detected:
                print(f"   🔮 {companion.name} detected a hidden {detected.value} pattern!")
                self.player.patterns.append(detected)
                return

        # Normal exploration
        if random.random() < 0.5 + bonus_chance:
            found = random.choice(available_patterns)
            self.player.patterns.append(found)
            print(f"   ✨ Found {found.value} pattern!")

            # Companion reaction
            if isinstance(companion, GardenerCompanion) and found == PatternType.GARDEN:
                print(f"\n💬 {companion.name}: Perfect! This will grow beautifully.")
            elif isinstance(companion, ForgerCompanion) and found == PatternType.FLAME:
                print(f"\n💬 {companion.name}: Fire pattern! The forge burns brighter!")
        else:
            print("   Nothing found this time.")

    def talk_to_companion(self):
        """Have a conversation with companion"""
        companion = self.player.companion

        print(f"\n💬 Talking with {companion.name}...")

        # Context-based dialogue
        contexts = ['general', 'greeting']

        # Add specific contexts based on companion
        if isinstance(companion, ForgerCompanion):
            contexts.extend(['crafting', 'rebirth'])
        elif isinstance(companion, VoidwalkerCompanion):
            contexts.extend(['void_entry', 'comfort'])
        elif isinstance(companion, GardenerCompanion):
            contexts.extend(['planting', 'seasonal'])
        elif isinstance(companion, ScribeCompanion):
            contexts.extend(['documenting', 'contract'])
        elif isinstance(companion, HeraldCompanion):
            contexts.extend(['tuning', 'harmony'])
        elif isinstance(companion, SeekerCompanion):
            contexts.extend(['discovery', 'danger'])

        # Random context
        context = random.choice(contexts)
        response = companion.speak(context)

        print(f"\n{companion.name}: {response}")

        # Chance to unlock memory (Seeker)
        if isinstance(companion, SeekerCompanion):
            locked = [m for m in companion.core_memories if not m.unlocked]
            if locked and random.random() < 0.2:
                memory = random.choice(locked)
                memory.unlocked = True
                print(f"\n✨ Memory unlocked: {memory.description}")

    def use_companion_ability(self):
        """Use companion's special ability"""
        companion = self.player.companion

        print(f"\n✨ Using {companion.name}'s special ability...")

        if isinstance(companion, SeekerCompanion):
            # Echo fragments
            pattern = companion.detect_pattern(self.player.current_location.value)
            if pattern:
                print(f"Echo detected: {pattern.value} pattern!")
                self.player.patterns.append(pattern)
            else:
                print("No patterns detected right now.")

        elif isinstance(companion, ForgerCompanion):
            # Phoenix rebirth
            if companion.phoenix_cycles < 3:
                result = companion.phoenix_rebirth()
                print(f"🔥 PHOENIX REBIRTH! Cycle {result['cycles']}")
                print(f"   New forge temperature: {result['new_temperature']}K")
                print(f"   Memory: {result['memory']}")
            else:
                print("The phoenix has reached maximum cycles for now.")

        elif isinstance(companion, VoidwalkerCompanion):
            # Enter void
            result = companion.enter_void(3.0)
            print(f"Entering void... Depth: {result['depth']}")
            if result.get('found_pocket'):
                print(f"✨ Found void pocket: {result['pocket_contents']}")
                # Give reward
                if result['pocket_contents'] == 'void_shard':
                    self.player.patterns.append(PatternType.VOID)

        elif isinstance(companion, GardenerCompanion):
            # Plant seed
            if companion.seed_vault.get('memory_seed', 0) > 0:
                fertilizer = self.player.patterns[0] if self.player.patterns else None
                result = companion.plant_seed('memory_seed', fertilizer)
                print(result['message'])
                if result['success'] and fertilizer:
                    self.player.patterns.remove(fertilizer)
            else:
                # Advance season
                message = companion.advance_season()
                print(message)

        elif isinstance(companion, ScribeCompanion):
            # Write reality
            statement = f"{self.player.name} gains wisdom"
            result = companion.write_reality(statement, use_golden_ink=True)
            print(f"📝 {result['message']}")
            if result['success'] and result.get('power_level', 0) > 0:
                self.player.coherence = min(1.0, self.player.coherence + 0.1)
                print("   Your coherence increases!")

        elif isinstance(companion, HeraldCompanion):
            # Dimensional broadcast
            message = f"Seeking others at frequency {companion.base_frequency}"
            result = companion.dimensional_broadcast(message)
            print(f"📡 Broadcasting... Reached {result['dimensions_reached']} dimensions")
            if result['response_received']:
                print(f"   Response: {result['response']}")
                self.player.bloomcoin += 50
                print("   +50 BloomCoin from dimensional response!")

    def travel(self):
        """Travel to a new location"""
        print("\n🗺️ Where to travel?")

        locations = list(GameLocation)
        for i, loc in enumerate(locations, 1):
            current = " [CURRENT]" if loc == self.player.current_location else ""
            discovered = " ✓" if loc in self.player.locations_discovered else ""
            print(f"{i}. {loc.value}{current}{discovered}")

        try:
            choice = int(input("\nChoice (0 to cancel): "))
            if choice == 0:
                return
            new_location = locations[choice - 1]
        except (ValueError, IndexError):
            print("Invalid choice.")
            return

        self.player.current_location = new_location

        if new_location not in self.player.locations_discovered:
            self.player.locations_discovered.append(new_location)
            self.player.bloomcoin += 25
            print(f"\n🎉 First visit to {new_location.value}! +25 BloomCoin")

        print(f"\n📍 Arrived at {new_location.value}")

        # Companion location reaction
        companion = self.player.companion
        if isinstance(companion, SeekerCompanion) and new_location == GameLocation.LIBRARY_INFINITE:
            print(f"\n💬 {companion.name}: The Library... I can hear all the unspoken words...")
        elif isinstance(companion, ForgerCompanion) and new_location == GameLocation.PHOENIX_NEST:
            print(f"\n💬 {companion.name}: Home... The eternal flames remember me.")
        elif isinstance(companion, VoidwalkerCompanion) and new_location == GameLocation.VOID_MARKET:
            print(f"\n💬 {companion.name}: The Void Market. Trade in things that don't exist.")
        elif isinstance(companion, GardenerCompanion) and new_location == GameLocation.GARDEN_HEART:
            print(f"\n💬 {companion.name}: The Garden Heart. All growth begins here.")

    def cook_patterns(self):
        """Cook patterns using LIA protocol"""
        if not self.player.patterns:
            print("\n❌ No patterns to cook!")
            return

        # Get compatible recipes
        compatible = self.cooking_system.get_compatible_recipes(self.player.patterns)

        if not compatible:
            print("\n❌ No recipes available with current patterns.")
            return

        print("\n🍳 Available Recipes:")
        for i, recipe_name in enumerate(compatible, 1):
            recipe = self.cooking_system.recipes[recipe_name]
            print(f"{i}. {recipe.name} - {recipe.bloomcoin_cost} BC")

        try:
            choice = int(input("\nChoice (0 to cancel): "))
            if choice == 0:
                return
            selected = compatible[choice - 1]
        except (ValueError, IndexError):
            print("Invalid choice.")
            return

        recipe = self.cooking_system.recipes[selected]

        if self.player.bloomcoin < recipe.bloomcoin_cost:
            print(f"\n❌ Need {recipe.bloomcoin_cost} BloomCoin!")
            return

        # Cook
        self.player.bloomcoin -= recipe.bloomcoin_cost
        success, message = self.cooking_system.start_cooking(
            selected,
            self.player.patterns,
            self.player.coherence
        )

        print(f"\n{message}")

        if success:
            # Process phases
            while True:
                complete, msg, artifact = self.cooking_system.process_phase()
                print(f"  {msg}")

                if complete and artifact:
                    print(f"\n✨ Created: {artifact.name}")

                    # Remove used patterns
                    for pattern in recipe.required_patterns:
                        if pattern in self.player.patterns:
                            self.player.patterns.remove(pattern)

                    # Companion reaction
                    if isinstance(self.player.companion, ForgerCompanion):
                        print(f"\n💬 {self.player.companion.name}: Excellent transformation!")
                    break

                if complete:
                    break

    def mine_bloomcoin(self):
        """Mine BloomCoin"""
        print("\n⛏️ Mining BloomCoin...")

        base = PHI * 10

        # Companion mining bonus
        bonus = 1.0
        companion = self.player.companion

        if isinstance(companion, ScribeCompanion):
            bonus = 1.2  # Scribes document value into existence
        elif isinstance(companion, ForgerCompanion):
            bonus = 1.0 + (companion.forge_temperature / 5000)  # Heat increases yield

        earnings = base * bonus
        self.player.bloomcoin += earnings

        print(f"💰 Mined {earnings:.2f} BloomCoin!")

    def show_companion_status(self):
        """Show detailed companion status"""
        companion = self.player.companion

        print(f"\n{'=' * 50}")
        print(f"COMPANION: {companion.name} - {companion.title}")
        print(f"{'=' * 50}")

        if isinstance(companion, SeekerCompanion):
            print(f"Evolution Stage: {companion.evolution_stage}")
            print(f"Whisper Clarity: {companion.whisper_clarity:.1%}")
            print(f"Fragments Collected: {companion.fragments_collected}")
            print(f"Echo Depth: {companion.echo_depth}")
            print(f"Current Mood: {companion.current_mood.value}")
            print("\nUnlocked Memories:")
            for memory in companion.core_memories:
                if memory.unlocked:
                    print(f"  • {memory.description}")

        elif isinstance(companion, ForgerCompanion):
            print(f"Evolution Stage: {companion.evolution_stage}")
            print(f"Forge Temperature: {companion.forge_temperature}K")
            print(f"Phoenix Cycles: {companion.phoenix_cycles}")
            print(f"Transformations: {companion.transformations_completed}")
            print(f"Forge Mastery: {companion.forge_mastery:.1%}")
            print("\nRebirth Memories:")
            for memory in companion.rebirth_memories:
                print(f"  • {memory}")

        elif isinstance(companion, VoidwalkerCompanion):
            print(f"Evolution Stage: {companion.evolution_stage}")
            print(f"Void Depth: {companion.void_depth}")
            print(f"Things Erased: {companion.things_erased}")
            print(f"Void Mastery: {companion.void_mastery:.1%}")
            print(f"Void Pockets Found: {len(companion.void_pockets)}")

        elif isinstance(companion, GardenerCompanion):
            print(f"Evolution Stage: {companion.evolution_stage}")
            print(f"Current Season: {companion.seasonal_phase}")
            print(f"Seeds Planted: {companion.seeds_planted}")
            print(f"Growing Plants: {len(companion.growing_plants)}")
            print(f"Timeline Awareness: {companion.timeline_awareness:.1%}")
            print("\nSeed Vault:")
            for seed, count in companion.seed_vault.items():
                if count > 0:
                    print(f"  • {seed}: {count}")

        elif isinstance(companion, ScribeCompanion):
            print(f"Evolution Stage: {companion.evolution_stage}")
            print(f"Current Chapter: {companion.current_chapter}")
            print(f"Pages Written: {companion.pages_written}")
            print(f"Reality Edits: {companion.reality_edits}")
            print(f"Golden Ink: {companion.golden_ink_supply:.1f}%")
            print(f"Reality Authority: {companion.reality_authority:.1%}")

        elif isinstance(companion, HeraldCompanion):
            print(f"Evolution Stage: {companion.evolution_stage}")
            print(f"Base Frequency: {companion.base_frequency} Hz")
            print(f"Harmonic Range: {companion.harmonic_range[0]}-{companion.harmonic_range[1]} Hz")
            print(f"Frequencies Discovered: {len(companion.frequencies_discovered)}")
            print(f"Dimensional Resonance: {companion.dimensional_resonance:.1%}")
            print("\nResonance Bonds:")
            for target, strength in companion.resonance_bonds.items():
                print(f"  • {target}: {strength:.1%}")

    def companion_interject(self):
        """Random companion interjection"""
        companion = self.player.companion

        # Change mood occasionally
        if random.random() < 0.3:
            moods = list(CompanionMood)
            companion.current_mood = random.choice(moods)

        # Speak based on mood
        if companion.current_mood == CompanionMood.CURIOUS:
            print(f"\n💭 {companion.name} seems curious about something...")
        elif companion.current_mood == CompanionMood.PROTECTIVE:
            print(f"\n💭 {companion.name} watches over you protectively...")
        elif companion.current_mood == CompanionMood.PLAYFUL:
            print(f"\n💭 {companion.name} seems in a playful mood!")

    def check_victory(self) -> bool:
        """Check victory conditions"""
        companion = self.player.companion

        # Companion-specific victories
        if isinstance(companion, SeekerCompanion):
            if companion.fragments_collected >= 20:
                return True
        elif isinstance(companion, ForgerCompanion):
            if companion.phoenix_cycles >= 5:
                return True
        elif isinstance(companion, VoidwalkerCompanion):
            if companion.void_depth <= -20:
                return True
        elif isinstance(companion, GardenerCompanion):
            if companion.seeds_planted >= 10:
                return True
        elif isinstance(companion, ScribeCompanion):
            if companion.current_chapter >= 7:
                return True
        elif isinstance(companion, HeraldCompanion):
            if len(companion.resonance_bonds) >= 5:
                return True

        # Universal victories
        if self.player.bloomcoin >= 1000:
            return True
        if self.player.coherence >= 0.95:
            return True

        return False

    def display_victory(self):
        """Display victory message"""
        companion = self.player.companion

        print("\n" + "=" * 60)
        print("   🌺✨ VICTORY ACHIEVED! ✨🌺")
        print("=" * 60)
        print(f"\n{self.player.name} and {companion.name} have transcended!")
        print(f"Job: {self.player.job.value}")
        print(f"Companion: {companion.title}")
        print(f"Turns: {self.player.turn_count}")
        print(f"BloomCoin: {self.player.bloomcoin:.2f}")

        # Companion-specific victory message
        if isinstance(companion, SeekerCompanion):
            print(f"\nEcho has collected enough fragments to hear the universe's true song.")
        elif isinstance(companion, ForgerCompanion):
            print(f"\nPrometheus has been reborn enough times to understand eternal fire.")
        elif isinstance(companion, VoidwalkerCompanion):
            print(f"\nNull has reached the deepest void where all possibilities exist.")
        elif isinstance(companion, GardenerCompanion):
            print(f"\nGaia's garden now spans all timelines, eternal and ever-growing.")
        elif isinstance(companion, ScribeCompanion):
            print(f"\nAkasha's chronicle is complete. Reality is now as written.")
        elif isinstance(companion, HeraldCompanion):
            print(f"\nResonance has harmonized with the universe's frequency.")

        print("\nYour unique companion made this journey unlike any other.")
        print("Together, you discovered what it means to transcend.")

        print("\n" + "=" * 60)


if __name__ == "__main__":
    game = BloomQuestUniqueCompanions()
    game.start()