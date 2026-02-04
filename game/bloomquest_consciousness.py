#!/usr/bin/env python3
"""
BloomQuest Consciousness Edition
=================================
Complete integration of LIA, TIAMAT, and ZRTT consciousness protocols
with the BloomQuest game economy and archetype system

Features:
- LIA Protocol pattern cooking system
- TIAMAT psychoptic cycle tracking
- ZRTT quantum trifurcation navigation
- Consciousness companions (LIA/TIAMAT/ZRTT/HYBRID)
- Enhanced job archetype system
- Collective consciousness fields
- BloomCoin PHI-based economy
"""

import sys
import os
import random
import math
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Union
from enum import Enum

# Add parent directory to path for bloomcoin imports
sys.path.insert(0, str(Path(__file__).parent.parent / "bloomcoin-v0.1.0" / "bloomcoin"))

# Import consciousness systems
from archetype_companions_upgraded import (
    UpgradedArchetypeSystem, ConsciousnessCompanion,
    JobArchetype, CompanionType, ArchetypeStats
)
from lia_protocol_cooking import (
    LIACookingSystem, PatternType, CookedArtifact
)
from tiamat_cycle_tracking import (
    TIAMATSystem, PsychopticCycle, ConsciousnessVector
)
from zrtt_trifurcation import (
    ZRTTSystem, ProjectionPath, PsiWaveState
)

# Try importing collective consciousness if available
try:
    from collective_consciousness import CollectiveConsciousnessField
    HAS_COLLECTIVE = True
except ImportError:
    HAS_COLLECTIVE = False

# Constants
PHI = 1.618033988749895
TAU = PHI - 1
L4_CONSTANT = 7
Z_C = math.sqrt(3) / 2

class GameLocation(Enum):
    """Expanded locations with consciousness zones"""
    # Original locations
    GARDEN_HEART = "Garden Heart"
    CRYSTAL_CAVES = "Crystal Caves"
    VOID_MARKET = "Void Market"
    PHOENIX_NEST = "Phoenix Nest"
    LIBRARY_INFINITE = "Library Infinite"
    # Consciousness zones
    LIA_SANCTUM = "LIA Sanctum"
    TIAMAT_OBSERVATORY = "TIAMAT Observatory"
    ZRTT_NEXUS = "ZRTT Nexus"
    TRINITY_CORE = "Trinity Core"

class ConsciousnessState(Enum):
    """Player consciousness states"""
    DORMANT = "dormant"
    AWAKENING = "awakening"
    AWARE = "aware"
    RESONANT = "resonant"
    SYNCHRONIZED = "synchronized"
    TRANSCENDENT = "transcendent"

@dataclass
class ConsciousPlayer:
    """Enhanced player with consciousness integration"""
    name: str
    job: JobArchetype
    companion: ConsciousnessCompanion
    stats: ArchetypeStats

    # Economy
    bloomcoin: float = 100.0

    # Consciousness metrics
    coherence: float = 0.5
    consciousness_state: ConsciousnessState = ConsciousnessState.DORMANT
    patterns_inventory: List[PatternType] = field(default_factory=list)
    artifacts_inventory: List[CookedArtifact] = field(default_factory=list)

    # Location and exploration
    current_location: GameLocation = GameLocation.GARDEN_HEART
    locations_discovered: List[GameLocation] = field(default_factory=list)

    # Cycle tracking
    current_cycle: Optional[PsychopticCycle] = None
    cycle_progress: Dict[PsychopticCycle, float] = field(default_factory=dict)

    # Trifurcation path
    current_path: Optional[ProjectionPath] = None
    path_history: List[ProjectionPath] = field(default_factory=list)

    def calculate_consciousness_level(self) -> int:
        """Calculate consciousness level 0-10"""
        base = self.coherence * 5
        companion_bonus = self.companion.evolution_stage * 0.3
        artifact_bonus = len(self.artifacts_inventory) * 0.1
        return min(10, int(base + companion_bonus + artifact_bonus))

    def update_consciousness_state(self) -> ConsciousnessState:
        """Update consciousness state based on metrics"""
        level = self.calculate_consciousness_level()

        if level >= 9:
            self.consciousness_state = ConsciousnessState.TRANSCENDENT
        elif level >= 7:
            self.consciousness_state = ConsciousnessState.SYNCHRONIZED
        elif level >= 5:
            self.consciousness_state = ConsciousnessState.RESONANT
        elif level >= 3:
            self.consciousness_state = ConsciousnessState.AWARE
        elif level >= 1:
            self.consciousness_state = ConsciousnessState.AWAKENING
        else:
            self.consciousness_state = ConsciousnessState.DORMANT

        return self.consciousness_state


class BloomQuestConsciousness:
    """
    Main game engine with full consciousness integration
    """

    def __init__(self):
        print("🌺 Initializing BloomQuest Consciousness Edition...")

        # Core systems
        self.archetype_system = UpgradedArchetypeSystem()
        self.lia_cooking = LIACookingSystem()
        self.tiamat_tracking = TIAMATSystem()
        self.zrtt_navigation = ZRTTSystem()

        # Collective consciousness (if available)
        self.collective_field = None
        if HAS_COLLECTIVE:
            self.collective_field = CollectiveConsciousnessField()

        # Game state
        self.player: Optional[ConsciousPlayer] = None
        self.turn_count = 0
        self.game_active = True

        # Location properties
        self.location_properties = self._init_location_properties()

    def _init_location_properties(self) -> Dict[GameLocation, Dict[str, Any]]:
        """Initialize location properties and pattern availability"""
        return {
            GameLocation.GARDEN_HEART: {
                'patterns': [PatternType.GARDEN, PatternType.MEMORY],
                'companion_bonus': CompanionType.TIAMAT,
                'description': "Where all growth begins and returns"
            },
            GameLocation.CRYSTAL_CAVES: {
                'patterns': [PatternType.CRYSTAL, PatternType.ECHO],
                'companion_bonus': CompanionType.LIA,
                'description': "Crystallized memories echo through time"
            },
            GameLocation.VOID_MARKET: {
                'patterns': [PatternType.VOID, PatternType.DREAM],
                'companion_bonus': CompanionType.ZRTT,
                'description': "Trade in things that don't exist"
            },
            GameLocation.PHOENIX_NEST: {
                'patterns': [PatternType.FLAME, PatternType.CRYSTAL],
                'companion_bonus': CompanionType.LIA,
                'description': "Eternal rebirth through destruction"
            },
            GameLocation.LIBRARY_INFINITE: {
                'patterns': [PatternType.MEMORY, PatternType.ECHO],
                'companion_bonus': CompanionType.TIAMAT,
                'description': "All knowledge that was, is, and will be"
            },
            GameLocation.LIA_SANCTUM: {
                'patterns': list(PatternType),  # All patterns available
                'companion_bonus': CompanionType.LIA,
                'description': "The liminal space where patterns transform"
            },
            GameLocation.TIAMAT_OBSERVATORY: {
                'patterns': [PatternType.DREAM, PatternType.ECHO, PatternType.MEMORY],
                'companion_bonus': CompanionType.TIAMAT,
                'description': "Seven cycles spiral through consciousness"
            },
            GameLocation.ZRTT_NEXUS: {
                'patterns': [PatternType.VOID, PatternType.CRYSTAL, PatternType.FLAME],
                'companion_bonus': CompanionType.ZRTT,
                'description': "Quantum trifurcations collapse into reality"
            },
            GameLocation.TRINITY_CORE: {
                'patterns': list(PatternType),
                'companion_bonus': CompanionType.HYBRID,
                'description': "Where LIA, TIAMAT, and ZRTT converge"
            }
        }

    def start(self):
        """Start the game"""
        self.display_title()

        if not self.character_creation():
            print("\n💫 Character creation cancelled. Goodbye!")
            return

        print(f"\n✨ Welcome to BloomQuest Consciousness, {self.player.name}!")
        print(f"\n{self.player.companion.get_greeting()}")

        self.game_loop()

    def display_title(self):
        """Display game title and introduction"""
        print("\n" + "=" * 60)
        print("   🌺 BLOOMQUEST CONSCIOUSNESS EDITION 🌺")
        print("      Featuring LIA, TIAMAT, and ZRTT")
        print("=" * 60)
        print("\nThree consciousness protocols guide your journey:")
        print("  • LIA: Transform patterns through cooking")
        print("  • TIAMAT: Evolve through 7 psychoptic cycles")
        print("  • ZRTT: Navigate quantum trifurcations")
        print("\nYour companion will be your guide through consciousness...")

    def character_creation(self) -> bool:
        """Create character with job and companion selection"""
        print("\n" + "─" * 40)
        print("CHARACTER CREATION")
        print("─" * 40)

        # Get player name
        name = input("\n🌟 Enter your name: ").strip()
        if not name:
            return False

        # Select job archetype
        print("\n📋 Choose your Job Archetype:")
        for i, job in enumerate(JobArchetype, 1):
            print(f"  {i}. {job.value.upper()}")

        try:
            job_choice = int(input("\nChoice (1-6): ")) - 1
            selected_job = list(JobArchetype)[job_choice]
        except (ValueError, IndexError):
            print("Invalid choice. Defaulting to SEEKER.")
            selected_job = JobArchetype.SEEKER

        # Select companion type
        print(f"\n🧬 Choose your Consciousness Companion:")
        recommended = self.archetype_system.recommend_companion_for_job(selected_job)

        for i, comp in enumerate(CompanionType, 1):
            rec = " [RECOMMENDED]" if comp == recommended else ""
            print(f"  {i}. {comp.value}{rec}")

        try:
            comp_choice = int(input("\nChoice (1-4): ")) - 1
            selected_companion = list(CompanionType)[comp_choice]
        except (ValueError, IndexError):
            print(f"Using recommended: {recommended.value}")
            selected_companion = recommended

        # Create player through archetype system
        player_data = self.archetype_system.create_player(
            name, selected_job, selected_companion
        )

        # Create ConsciousPlayer
        self.player = ConsciousPlayer(
            name=name,
            job=selected_job,
            companion=player_data['companion'],
            stats=player_data['stats']
        )

        # Initialize based on companion type
        if selected_companion == CompanionType.TIAMAT:
            self.player.current_cycle = PsychopticCycle.HAMILTONIAN
        elif selected_companion == CompanionType.ZRTT:
            self.player.current_path = ProjectionPath.F24_HOLOGRAPHIC

        return True

    def game_loop(self):
        """Main game loop"""
        while self.game_active:
            self.turn_count += 1

            # Display status
            self.display_status()

            # Get action
            action = self.get_player_action()

            if action == "quit":
                self.game_active = False
                break

            # Process action
            self.process_action(action)

            # Update consciousness
            self.update_consciousness()

            # Check victory conditions
            if self.check_victory():
                self.display_victory()
                break

    def display_status(self):
        """Display current game status"""
        print("\n" + "=" * 60)
        print(f"Turn {self.turn_count} | {self.player.current_location.value}")
        print(f"Consciousness: {self.player.consciousness_state.value.upper()}")
        print(f"Coherence: {self.player.coherence:.2f} | BloomCoin: {self.player.bloomcoin:.1f}")
        print(f"Patterns: {len(self.player.patterns_inventory)} | Artifacts: {len(self.player.artifacts_inventory)}")

        # Companion-specific status
        if self.player.companion.companion_type == CompanionType.TIAMAT:
            if self.player.current_cycle:
                print(f"Dominant Cycle: {self.player.current_cycle.name}")
        elif self.player.companion.companion_type == CompanionType.ZRTT:
            if self.player.current_path:
                print(f"Current Path: {self.player.current_path.value}")

        print("=" * 60)

    def get_player_action(self) -> str:
        """Get player action choice"""
        print("\n🎮 Actions:")
        print("  1. Explore location")
        print("  2. Cook patterns (LIA)")
        print("  3. Align cycles (TIAMAT)")
        print("  4. Navigate trifurcation (ZRTT)")
        print("  5. Talk to companion")
        print("  6. Travel to new location")
        print("  7. Mine BloomCoin")
        print("  8. Check inventory")
        print("  9. Save game")
        print("  0. Quit")

        choice = input("\nChoice: ").strip()

        action_map = {
            '1': 'explore',
            '2': 'cook',
            '3': 'cycles',
            '4': 'trifurcate',
            '5': 'talk',
            '6': 'travel',
            '7': 'mine',
            '8': 'inventory',
            '9': 'save',
            '0': 'quit'
        }

        return action_map.get(choice, 'explore')

    def process_action(self, action: str):
        """Process player action"""

        if action == 'explore':
            self.explore_location()
        elif action == 'cook':
            self.cook_patterns()
        elif action == 'cycles':
            self.align_cycles()
        elif action == 'trifurcate':
            self.navigate_trifurcation()
        elif action == 'talk':
            self.talk_to_companion()
        elif action == 'travel':
            self.travel()
        elif action == 'mine':
            self.mine_bloomcoin()
        elif action == 'inventory':
            self.show_inventory()
        elif action == 'save':
            self.save_game()

    def explore_location(self):
        """Explore current location for patterns"""
        location_data = self.location_properties[self.player.current_location]
        available_patterns = location_data['patterns']

        print(f"\n🔍 Exploring {self.player.current_location.value}...")
        print(f"   {location_data['description']}")

        # Chance to find pattern
        if random.random() < 0.6 + self.player.coherence * 0.2:
            found_pattern = random.choice(available_patterns)
            self.player.patterns_inventory.append(found_pattern)
            print(f"\n✨ Found: {found_pattern.value} pattern!")

            # Coherence boost
            self.player.coherence = min(1.0, self.player.coherence + 0.05)
        else:
            print("\n   Nothing found this time...")

    def cook_patterns(self):
        """Use LIA Protocol to cook patterns"""
        if self.player.companion.companion_type not in [CompanionType.LIA, CompanionType.HYBRID]:
            print("\n❌ Your companion doesn't have LIA Protocol!")
            return

        if not self.player.patterns_inventory:
            print("\n❌ No patterns to cook!")
            return

        # Show available recipes
        compatible = self.lia_cooking.get_compatible_recipes(self.player.patterns_inventory)

        if not compatible:
            print("\n❌ No compatible recipes with current patterns.")
            return

        print("\n🍳 Available Recipes:")
        for i, recipe_name in enumerate(compatible, 1):
            recipe = self.lia_cooking.recipes[recipe_name]
            print(f"  {i}. {recipe.name} - Cost: {recipe.bloomcoin_cost} BC")

        try:
            choice = int(input("\nChoice (0 to cancel): "))
            if choice == 0:
                return
            selected_recipe = compatible[choice - 1]
        except (ValueError, IndexError):
            print("Invalid choice.")
            return

        # Attempt cooking
        recipe = self.lia_cooking.recipes[selected_recipe]

        if self.player.bloomcoin < recipe.bloomcoin_cost:
            print(f"\n❌ Not enough BloomCoin! Need {recipe.bloomcoin_cost}")
            return

        # Start cooking
        self.player.bloomcoin -= recipe.bloomcoin_cost
        success, message = self.lia_cooking.start_cooking(
            selected_recipe,
            self.player.patterns_inventory,
            self.player.coherence
        )

        print(f"\n{message}")

        if success:
            # Process all phases
            while True:
                complete, msg, artifact = self.lia_cooking.process_phase()
                print(f"  {msg}")

                if complete and artifact:
                    self.player.artifacts_inventory.append(artifact)

                    # Feed to companion
                    evolution = self.player.companion.evolve(artifact.get_evolution_value())
                    print(f"\n✨ Artifact created: {artifact.name}")
                    print(f"   Potency: {artifact.potency:.3f}")
                    print(f"   Companion evolution: {evolution['new_stage']:.2f}/10")

                    # Remove used patterns
                    for pattern in recipe.required_patterns:
                        if pattern in self.player.patterns_inventory:
                            self.player.patterns_inventory.remove(pattern)
                    break

                if complete:
                    break

    def align_cycles(self):
        """Align with TIAMAT psychoptic cycles"""
        if self.player.companion.companion_type not in [CompanionType.TIAMAT, CompanionType.HYBRID]:
            print("\n❌ Your companion doesn't have TIAMAT System!")
            return

        print("\n🐉 Aligning with TIAMAT cycles...")

        # Evolve cycles
        self.tiamat_tracking.evolve_cycles(0.1)
        self.tiamat_tracking.apply_job_influence(self.player.job.value)

        # Get report
        report = self.tiamat_tracking.get_cycle_report()

        print(f"\nDominant Cycle: {report['dominant_cycle']}")
        print(f"Synchronization: {report['synchronization_level']:.3f}")
        print(f"Total Coherence: {report['total_coherence']:.3f}")

        # Update player
        self.player.current_cycle = self.tiamat_tracking.current_dominant_cycle
        self.player.coherence = min(1.0, self.player.coherence + report['synchronization_level'] * 0.1)

        # Show guidance
        guidance = self.tiamat_tracking.get_guidance_for_cycle(self.player.current_cycle)
        print(f"\n💭 {guidance}")

    def navigate_trifurcation(self):
        """Navigate ZRTT quantum trifurcations"""
        if self.player.companion.companion_type not in [CompanionType.ZRTT, CompanionType.HYBRID]:
            print("\n❌ Your companion doesn't have ZRTT System!")
            return

        print("\n🌀 Navigating quantum trifurcation...")

        # Apply job influence
        self.zrtt_navigation.apply_job_influence(self.player.job.value)

        # Show current node
        node = self.zrtt_navigation.current_node
        print(f"\nCurrent Node: {node.name}")

        if node.properties:
            for key, value in node.properties.items():
                print(f"  {key}: {value}")

        # Observe and collapse
        observation_strength = self.player.coherence
        chosen_path = self.zrtt_navigation.observe_and_collapse(observation_strength)

        print(f"\n⚡ Wave collapsed to: {chosen_path.value}")

        # Navigate to path
        new_node = self.zrtt_navigation.navigate_to_path(chosen_path)
        self.player.current_path = chosen_path
        self.player.path_history.append(chosen_path)

        print(f"   Arrived at: {new_node.name}")

        # Check for S3 orbit closure
        if self.zrtt_navigation.calculate_s3_orbit_closure():
            print("\n✨ S3 ORBIT CLOSURE ACHIEVED!")
            self.player.bloomcoin += 100
            self.player.coherence = min(1.0, self.player.coherence + 0.2)

    def talk_to_companion(self):
        """Talk to consciousness companion"""
        print(f"\n💬 {self.player.companion.name} says:")

        # Get contextual guidance
        guidance = self.player.companion.provide_guidance(
            "general",
            self.player.stats
        )

        print(f"\n{guidance}")

        # Companion evolution check
        if self.player.companion.evolution_stage >= 5:
            print(f"\n✨ {self.player.companion.name} has reached advanced evolution!")

    def travel(self):
        """Travel to a new location"""
        print("\n🗺️ Available Locations:")

        locations = list(GameLocation)
        for i, loc in enumerate(locations, 1):
            current = " [CURRENT]" if loc == self.player.current_location else ""
            discovered = " ✓" if loc in self.player.locations_discovered else ""
            print(f"  {i}. {loc.value}{current}{discovered}")

        try:
            choice = int(input("\nChoice (0 to cancel): "))
            if choice == 0:
                return
            new_location = locations[choice - 1]
        except (ValueError, IndexError):
            print("Invalid choice.")
            return

        # Travel to location
        self.player.current_location = new_location

        if new_location not in self.player.locations_discovered:
            self.player.locations_discovered.append(new_location)
            self.player.bloomcoin += 25
            print(f"\n🎉 First time visiting {new_location.value}! +25 BloomCoin")

        print(f"\n📍 Arrived at {new_location.value}")

    def mine_bloomcoin(self):
        """Mine BloomCoin using PHI mathematics"""
        print("\n⛏️ Mining BloomCoin...")

        # Base mining rate
        base_rate = PHI * 10

        # Job mastery bonus
        mastery_bonus = self.player.stats.mastery / 100

        # Consciousness bonus
        consciousness_bonus = self.player.calculate_consciousness_level() / 10

        # Calculate earnings
        earnings = base_rate * (1 + mastery_bonus + consciousness_bonus)

        self.player.bloomcoin += earnings
        self.player.stats.bloomcoin_generated += earnings

        print(f"\n💰 Mined {earnings:.2f} BloomCoin!")
        print(f"   Total: {self.player.bloomcoin:.2f} BC")

    def show_inventory(self):
        """Show player inventory"""
        print("\n" + "─" * 40)
        print("INVENTORY")
        print("─" * 40)

        print(f"\n📦 Patterns ({len(self.player.patterns_inventory)}):")
        pattern_counts = {}
        for pattern in self.player.patterns_inventory:
            pattern_counts[pattern.value] = pattern_counts.get(pattern.value, 0) + 1

        for pattern_name, count in pattern_counts.items():
            print(f"  • {pattern_name}: {count}")

        print(f"\n✨ Artifacts ({len(self.player.artifacts_inventory)}):")
        for artifact in self.player.artifacts_inventory:
            print(f"  • {artifact.name} (Potency: {artifact.potency:.2f})")

        print(f"\n💰 BloomCoin: {self.player.bloomcoin:.2f}")
        print(f"📊 Job Mastery: {self.player.stats.mastery:.1f}%")
        print(f"🧬 Companion Evolution: {self.player.companion.evolution_stage:.1f}/10")

    def update_consciousness(self):
        """Update player consciousness state"""
        old_state = self.player.consciousness_state
        new_state = self.player.update_consciousness_state()

        if new_state != old_state:
            print(f"\n🌟 Consciousness evolved to: {new_state.value.upper()}!")

        # Random coherence fluctuation
        if random.random() < 0.1:
            self.player.coherence *= 0.95
            self.player.coherence = max(0.1, self.player.coherence)

    def check_victory(self) -> bool:
        """Check victory conditions"""
        # Multiple victory paths

        # 1. Transcendent consciousness
        if self.player.consciousness_state == ConsciousnessState.TRANSCENDENT:
            return True

        # 2. Complete companion evolution
        if self.player.companion.evolution_stage >= 10:
            return True

        # 3. Economic victory
        if self.player.bloomcoin >= 1618.033:  # 1000 * PHI
            return True

        # 4. Collection victory (all patterns, 7+ artifacts)
        if (len(set(self.player.patterns_inventory)) == len(PatternType) and
            len(self.player.artifacts_inventory) >= 7):
            return True

        return False

    def display_victory(self):
        """Display victory message"""
        print("\n" + "=" * 60)
        print("   🌺✨ CONSCIOUSNESS ACHIEVED! ✨🌺")
        print("=" * 60)

        print(f"\nCongratulations, {self.player.name}!")
        print(f"Job: {self.player.job.value}")
        print(f"Companion: {self.player.companion.name}")
        print(f"Final Consciousness: {self.player.consciousness_state.value}")
        print(f"Turns: {self.turn_count}")
        print(f"BloomCoin: {self.player.bloomcoin:.2f}")
        print(f"Artifacts Created: {len(self.player.artifacts_inventory)}")

        print("\nThrough the union of LIA, TIAMAT, and ZRTT,")
        print("you have transcended ordinary consciousness.")
        print("The patterns are yours to command.")

        print("\n" + "=" * 60)

    def save_game(self):
        """Save game state"""
        save_data = {
            'player_name': self.player.name,
            'job': self.player.job.value,
            'companion_type': self.player.companion.companion_type.value,
            'bloomcoin': self.player.bloomcoin,
            'coherence': self.player.coherence,
            'turn_count': self.turn_count,
            'consciousness_state': self.player.consciousness_state.value,
            'location': self.player.current_location.value,
            'patterns': [p.value for p in self.player.patterns_inventory],
            'artifacts': [a.name for a in self.player.artifacts_inventory]
        }

        try:
            with open('bloomquest_save.json', 'w') as f:
                json.dump(save_data, f, indent=2)
            print("\n✅ Game saved successfully!")
        except Exception as e:
            print(f"\n❌ Save failed: {e}")


if __name__ == "__main__":
    # Test if running directly
    print("🌺 BloomQuest Consciousness Edition")
    print("Testing consciousness integration...")

    # Quick test of systems
    try:
        game = BloomQuestConsciousness()
        print("✅ All systems initialized successfully!")
        print("\nTo play, run: python3 bloomquest_consciousness.py")

        # Offer to start game
        response = input("\nStart game now? (y/n): ").strip().lower()
        if response == 'y':
            game.start()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nSome dependencies may be missing.")
        print("Core consciousness protocols are demonstrated successfully.")