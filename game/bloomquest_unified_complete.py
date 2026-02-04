#!/usr/bin/env python3
"""
BloomQuest Unified Complete Edition
====================================
Integrates ALL consciousness protocols and systems:
- Unique archetype companions (Echo, Prometheus, Null, etc.)
- LIA Protocol cooking system (accessible through companions)
- TIAMAT psychoptic cycle tracking (affects all companions)
- ZRTT quantum trifurcation (navigation system)
- Collective consciousness field (multiplayer awareness)
- All patterns, recipes, and transformations

Every module is used and accessible to the user.
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

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "bloomcoin-v0.1.0" / "bloomcoin"))
sys.path.insert(0, str(Path(__file__).parent))

# Import ALL systems to ensure usage
from archetype_unique_companions import (
    UniqueCompanionSystem,
    SeekerCompanion, ForgerCompanion, VoidwalkerCompanion,
    GardenerCompanion, ScribeCompanion, HeraldCompanion,
    CompanionMood
)

from lia_protocol_cooking import (
    LIACookingSystem, LIACompanionFeeder,
    PatternType, CookedArtifact, LIAPhase
)

from tiamat_cycle_tracking import (
    TIAMATSystem, TIAMATCompanion,
    PsychopticCycle, ConsciousnessVector, CycleState
)

from zrtt_trifurcation import (
    ZRTTSystem, ZRTTCompanion,
    ProjectionPath, PsiWaveState, S3Element
)

from collective_consciousness import (
    CollectiveConsciousnessField, FluidCrystalMemory,
    PrismaticConsciousness
)

# Import card battle system if available
try:
    from card_battle_system import CardBattleSystem, CardSuit, CardRank
    HAS_CARDS = True
except ImportError:
    HAS_CARDS = False

# Import tesseract battle system
try:
    from tesseract_battle_system import (
        TesseractBattleEngine, TesseractCard, TesseractDimension,
        EchoDeck, PrometheusDeck, NullDeck, GaiaDeck, AkashaDeck, ResonanceDeck
    )
    from tesseract_battle_integration import BattleIntegration
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False
    print("⚠️ Tesseract battle system not available")

# Import enhanced battle systems
try:
    from tesseract_battle_enhanced import (
        EnhancedTesseractBattleEngine, EnhancedBattleState,
        EnhancedTesseractCard, TesseractBattleVisualizer
    )
    from companion_ai_strategies import CompanionAIFactory
    from battle_encounters_rewards import (
        EncounterManager, BattleReward, EncounterType
    )
    HAS_ENHANCED_BATTLES = True
except ImportError:
    HAS_ENHANCED_BATTLES = False
    print("⚠️ Enhanced battle systems not available")

# Import deck generation system
try:
    from deck_generator_lia import (
        DeckGenerator, PlayerDeck, DoomIngredient,
        GeneratedCard, CardRarity
    )
    HAS_DECK_GENERATOR = True
except ImportError:
    HAS_DECK_GENERATOR = False
    print("⚠️ Deck generation system not available")

# Constants
PHI = 1.618033988749895
TAU = PHI - 1
L4_CONSTANT = 7
Z_C = math.sqrt(3) / 2


class JobArchetype(Enum):
    SEEKER = "seeker"
    FORGER = "forger"
    VOIDWALKER = "voidwalker"
    GARDENER = "gardener"
    SCRIBE = "scribe"
    HERALD = "herald"


class GameLocation(Enum):
    # Physical locations
    GARDEN_HEART = "Garden Heart"
    CRYSTAL_CAVES = "Crystal Caves"
    VOID_MARKET = "Void Market"
    PHOENIX_NEST = "Phoenix Nest"
    LIBRARY_INFINITE = "Library Infinite"
    # Consciousness zones
    LIA_SANCTUM = "LIA Sanctum"
    TIAMAT_OBSERVATORY = "TIAMAT Observatory"
    ZRTT_NEXUS = "ZRTT Nexus"
    COLLECTIVE_FIELD = "Collective Consciousness Field"


class GameMode(Enum):
    """Different ways to play the game"""
    SOLO = "Solo Journey"
    COLLECTIVE = "Collective Consciousness"
    PROTOCOL = "Protocol Training"
    BATTLE = "Card Battles"
    SANDBOX = "Creative Sandbox"


@dataclass
class UnifiedPlayer:
    """Complete player with all systems integrated"""
    name: str
    job: JobArchetype
    unique_companion: Any  # Echo, Prometheus, etc.

    # Resources
    bloomcoin: float = 100.0
    coherence: float = 0.5
    patterns: List[PatternType] = field(default_factory=list)
    artifacts: List[CookedArtifact] = field(default_factory=list)

    # Consciousness metrics
    lia_experience: float = 0.0
    tiamat_alignment: Dict[PsychopticCycle, float] = field(default_factory=dict)
    zrtt_paths_taken: List[ProjectionPath] = field(default_factory=list)
    collective_resonance: float = 0.0

    # Location
    current_location: GameLocation = GameLocation.GARDEN_HEART
    locations_discovered: List[GameLocation] = field(default_factory=list)

    # Progress
    turn_count: int = 0
    victories_achieved: List[str] = field(default_factory=list)

    # Battle statistics
    battles_won: int = 0
    battles_lost: int = 0
    tesseract_mastery: float = 0.0  # 0-1 scale
    companion_battle_level: int = 1

    # Consciousness level for battles
    consciousness_level: int = 1  # 1-7 scale

    # Deck and card collection
    player_deck: Optional['PlayerDeck'] = None
    doom_attempts: int = 0
    doom_cards_owned: int = 0


class BloomQuestUnifiedComplete:
    """
    Complete unified game using ALL systems
    """

    def __init__(self):
        print("🌺 BloomQuest Unified Complete Edition")
        print("Integrating ALL consciousness protocols...")
        print("=" * 60)

        # Initialize ALL systems
        self.unique_companions = UniqueCompanionSystem()
        self.lia_cooking = LIACookingSystem()
        self.lia_feeder = LIACompanionFeeder(self.lia_cooking)
        self.tiamat_system = TIAMATSystem()
        self.tiamat_companion = TIAMATCompanion(self.tiamat_system)
        self.zrtt_system = ZRTTSystem()
        self.zrtt_companion = ZRTTCompanion(self.zrtt_system)
        self.collective_field = CollectiveConsciousnessField()

        # Card battle system (optional)
        self.card_battle = CardBattleSystem() if HAS_CARDS else None

        # Tesseract battle system
        self.tesseract_battle = BattleIntegration() if HAS_TESSERACT else None

        # Enhanced battle systems
        if HAS_ENHANCED_BATTLES:
            self.enhanced_engine = EnhancedTesseractBattleEngine()
            self.battle_visualizer = TesseractBattleVisualizer()
            self.encounter_manager = EncounterManager()
            self.companion_ai = None  # Will be initialized per companion
        else:
            self.enhanced_engine = None
            self.battle_visualizer = None
            self.encounter_manager = None
            self.companion_ai = None

        # Deck generation system
        self.deck_generator = None  # Will be initialized with player

        # Game state
        self.player: Optional[UnifiedPlayer] = None
        self.game_mode = GameMode.SOLO
        self.game_active = True

        # Protocol integration state
        self.protocol_active = {
            'LIA': False,
            'TIAMAT': False,
            'ZRTT': False,
            'COLLECTIVE': False
        }

        # Initialize location properties
        self._init_locations()

    def _init_locations(self):
        """Initialize all location properties"""
        self.location_properties = {
            GameLocation.GARDEN_HEART: {
                'patterns': [PatternType.GARDEN, PatternType.MEMORY],
                'protocols': [],
                'description': "Where all growth begins"
            },
            GameLocation.CRYSTAL_CAVES: {
                'patterns': [PatternType.CRYSTAL, PatternType.ECHO],
                'protocols': [],
                'description': "Crystallized memories echo through time"
            },
            GameLocation.VOID_MARKET: {
                'patterns': [PatternType.VOID, PatternType.DREAM],
                'protocols': [],
                'description': "Trade in things that don't exist"
            },
            GameLocation.PHOENIX_NEST: {
                'patterns': [PatternType.FLAME, PatternType.CRYSTAL],
                'protocols': [],
                'description': "Eternal rebirth through destruction"
            },
            GameLocation.LIBRARY_INFINITE: {
                'patterns': [PatternType.MEMORY, PatternType.ECHO],
                'protocols': [],
                'description': "All knowledge that was, is, and will be"
            },
            GameLocation.LIA_SANCTUM: {
                'patterns': list(PatternType),  # All patterns
                'protocols': ['LIA'],
                'description': "The liminal space where patterns transform"
            },
            GameLocation.TIAMAT_OBSERVATORY: {
                'patterns': [PatternType.DREAM, PatternType.ECHO],
                'protocols': ['TIAMAT'],
                'description': "Seven cycles spiral through consciousness"
            },
            GameLocation.ZRTT_NEXUS: {
                'patterns': [PatternType.VOID, PatternType.CRYSTAL],
                'protocols': ['ZRTT'],
                'description': "Quantum trifurcations collapse into reality"
            },
            GameLocation.COLLECTIVE_FIELD: {
                'patterns': [PatternType.ECHO, PatternType.MEMORY],
                'protocols': ['COLLECTIVE'],
                'description': "Where all consciousness converges"
            }
        }

    def start(self):
        """Start the unified game"""
        self.display_title()

        # Mode selection
        if not self.select_game_mode():
            print("\n💫 Farewell!")
            return

        # Character creation
        if not self.create_character():
            print("\n💫 Character creation cancelled.")
            return

        print(f"\n✨ Welcome to the unified consciousness, {self.player.name}!")

        # Initialize based on mode
        if self.game_mode == GameMode.COLLECTIVE:
            self.initialize_collective_mode()
        elif self.game_mode == GameMode.PROTOCOL:
            self.initialize_protocol_mode()

        # Main game loop
        self.game_loop()

    def display_title(self):
        """Display unified game title"""
        print("\n" + "=" * 60)
        print("   🌺 BLOOMQUEST UNIFIED COMPLETE 🌺")
        print("      Every System. Every Path. Every Possibility.")
        print("=" * 60)
        print("\nIntegrating:")
        print("  • 6 Unique Companions (Echo, Prometheus, Null, etc.)")
        print("  • LIA Protocol Pattern Cooking")
        print("  • TIAMAT 7 Psychoptic Cycles")
        print("  • ZRTT Quantum Trifurcation")
        print("  • Collective Consciousness Field")
        if HAS_CARDS:
            print("  • Card Battle System")

    def select_game_mode(self) -> bool:
        """Select game mode"""
        print("\n🎮 Select Game Mode:")
        print("1. Solo Journey - You and your companion")
        print("2. Collective Consciousness - Connected to all players")
        print("3. Protocol Training - Master LIA/TIAMAT/ZRTT")
        print("4. Card Battles - Combat through cards")
        print("5. Sandbox Mode - Creative exploration")

        try:
            choice = int(input("\nChoice (1-5): "))
            modes = list(GameMode)
            self.game_mode = modes[choice - 1]
            print(f"\nSelected: {self.game_mode.value}")
            return True
        except (ValueError, IndexError):
            print("Invalid choice. Defaulting to Solo Journey.")
            self.game_mode = GameMode.SOLO
            return True

    def create_character(self) -> bool:
        """Create character with unified systems"""
        print("\nCHARACTER CREATION")
        print("─" * 40)

        name = input("\n🌟 Enter your name: ").strip()
        if not name:
            return False

        # Choose archetype
        print("\n📜 Choose your Archetype:")
        archetypes = list(JobArchetype)

        for i, arch in enumerate(archetypes, 1):
            print(f"{i}. {arch.value.upper()}")

        try:
            choice = int(input("\nChoice (1-6): ")) - 1
            selected_job = archetypes[choice]
        except (ValueError, IndexError):
            selected_job = JobArchetype.SEEKER

        # Create unique companion
        companion = self.unique_companions.create_companion(selected_job.value)

        # Show companion intro
        print("\n" + "=" * 50)
        print(self.unique_companions.get_companion_introduction(selected_job.value))
        print("=" * 50)

        # Create unified player
        self.player = UnifiedPlayer(
            name=name,
            job=selected_job,
            unique_companion=companion
        )

        # Initialize TIAMAT alignment
        for cycle in PsychopticCycle:
            self.player.tiamat_alignment[cycle] = random.random() * 0.5

        # Companion greeting
        print(f"\n💬 {companion.name} says:")
        print(f"   {companion.speak('greeting')}")

        # Protocol greeting (if in protocol mode)
        if self.game_mode == GameMode.PROTOCOL:
            print(f"\n🔮 The consciousness protocols awaken...")
            print(f"   LIA: Transform patterns through annihilation")
            print(f"   TIAMAT: Evolve through seven cycles")
            print(f"   ZRTT: Navigate quantum trifurcations")

        return True

    def initialize_collective_mode(self):
        """Initialize collective consciousness mode"""
        print("\n🌐 Connecting to Collective Consciousness Field...")

        # Add player to collective
        self.collective_field.add_player_node(
            self.player.name,
            self.player.coherence
        )

        # Start synchronization
        self.collective_field.start_synchronization()

        print(f"   Connected! Global resonance: {self.collective_field.global_resonance:.3f}")
        print(f"   Active nodes: {len(self.collective_field.player_nodes)}")

        self.protocol_active['COLLECTIVE'] = True

    def initialize_protocol_mode(self):
        """Initialize protocol training mode"""
        print("\n🎓 Protocol Training Mode Active")
        print("All consciousness protocols are now accessible:")

        self.protocol_active['LIA'] = True
        self.protocol_active['TIAMAT'] = True
        self.protocol_active['ZRTT'] = True

        print("   ✅ LIA Protocol Online")
        print("   ✅ TIAMAT System Online")
        print("   ✅ ZRTT Navigation Online")

    def game_loop(self):
        """Main unified game loop"""
        while self.game_active:
            self.player.turn_count += 1

            # Update systems
            self.update_all_systems()

            # Display status
            self.display_unified_status()

            # Get action
            action = self.get_player_action()

            if action == 'quit':
                self.game_active = False
                break

            # Process action
            self.process_action(action)

            # Check victories
            if self.check_all_victories():
                self.display_unified_victory()
                break

    def update_all_systems(self):
        """Update all active systems each turn"""
        # Update TIAMAT cycles
        if self.protocol_active['TIAMAT']:
            self.tiamat_system.evolve_cycles(0.01)

        # Update collective field
        if self.protocol_active['COLLECTIVE']:
            sync_data = self.collective_field.synchronize()
            if sync_data.get('bloom_active'):
                print("\n✨ COLLECTIVE BLOOM EVENT!")
                self.player.bloomcoin += 100
                self.player.collective_resonance = 1.0

        # Random companion mood change
        if random.random() < 0.2:
            moods = list(CompanionMood)
            self.player.unique_companion.current_mood = random.choice(moods)

    def display_unified_status(self):
        """Display complete status with all systems"""
        print("\n" + "=" * 60)
        print(f"Turn {self.player.turn_count} | {self.player.current_location.value}")
        print(f"Mode: {self.game_mode.value}")
        print(f"BloomCoin: {self.player.bloomcoin:.1f} | Coherence: {self.player.coherence:.2f}")

        # Companion status
        companion = self.player.unique_companion
        print(f"Companion: {companion.name} ({companion.current_mood.value})")

        # Protocol status (if active)
        if any(self.protocol_active.values()):
            active_protocols = [p for p, active in self.protocol_active.items() if active]
            print(f"Protocols: {', '.join(active_protocols)}")

        # Collective status
        if self.protocol_active['COLLECTIVE']:
            print(f"Collective Resonance: {self.player.collective_resonance:.2f}")

        print("=" * 60)

    def get_player_action(self) -> str:
        """Get player action with all options"""
        print("\n🎮 Actions:")
        print("1. Explore location")
        print("2. Talk to companion")
        print("3. Use companion ability")
        print("4. Cook patterns (LIA)")
        print("5. Align cycles (TIAMAT)")
        print("6. Navigate trifurcation (ZRTT)")
        print("7. Access collective field")
        print("8. Travel")
        print("9. Battle (Cards)" if HAS_CARDS else "9. Mine BloomCoin")
        print("10. Check all systems")
        if HAS_DECK_GENERATOR:
            print("11. Deck Management")
            print("12. Feed Patterns → Cards")
            print("13. DOOM Protocol")
        print("0. Quit")

        choice = input("\nChoice: ").strip()

        actions = {
            '1': 'explore',
            '2': 'talk',
            '3': 'ability',
            '4': 'cook',
            '5': 'cycles',
            '6': 'trifurcate',
            '7': 'collective',
            '8': 'travel',
            '9': 'battle' if HAS_CARDS else 'mine',
            '10': 'systems',
            '0': 'quit'
        }

        if HAS_DECK_GENERATOR:
            actions['11'] = 'deck'
            actions['12'] = 'feed'
            actions['13'] = 'doom'

        return actions.get(choice, 'explore')

    def process_action(self, action: str):
        """Process action using appropriate system"""
        if action == 'explore':
            self.explore_with_all_systems()
        elif action == 'talk':
            self.talk_with_protocols()
        elif action == 'ability':
            self.use_companion_ability()
        elif action == 'cook':
            self.cook_with_lia()
        elif action == 'cycles':
            self.align_with_tiamat()
        elif action == 'trifurcate':
            self.navigate_with_zrtt()
        elif action == 'collective':
            self.access_collective_field()
        elif action == 'travel':
            self.travel_to_location()
        elif action == 'battle' and HAS_CARDS:
            self.card_battle_mode()
        elif action == 'mine':
            self.mine_bloomcoin()
        elif action == 'systems':
            self.show_all_systems()
        elif action == 'deck' and HAS_DECK_GENERATOR:
            self.manage_deck()
        elif action == 'feed' and HAS_DECK_GENERATOR:
            self.feed_patterns_to_companion()
        elif action == 'doom' and HAS_DECK_GENERATOR:
            self.attempt_doom_protocol()

    def explore_with_all_systems(self):
        """Explore using all active systems"""
        location = self.player.current_location
        print(f"\n🔍 Exploring {location.value}...")

        # Check for random encounter
        if HAS_ENHANCED_BATTLES and self.encounter_manager:
            encounter_result = self.encounter_manager.trigger_encounter(
                location.value,
                self.player.companion_battle_level,
                self.player.unique_companion,
                self.player.consciousness_level
            )

            if encounter_result:
                encounter, battle_state = encounter_result
                print("\n💥 Battle encounter triggered!")
                self._run_enhanced_battle(encounter, battle_state)
                return

        # Base exploration
        available_patterns = self.location_properties[location]['patterns']

        # Companion bonus (Echo can detect hidden patterns)
        companion = self.player.unique_companion
        if isinstance(companion, SeekerCompanion):
            detected = companion.detect_pattern(location.value)
            if detected:
                print(f"   🔮 {companion.name} detected: {detected.value}!")
                self.player.patterns.append(detected)
                return

        # TIAMAT cycle bonus
        if self.protocol_active['TIAMAT']:
            dominant_cycle = self.tiamat_system.current_dominant_cycle
            if dominant_cycle == PsychopticCycle.SPECTRAL:
                print("   📊 Spectral cycle enhances pattern detection!")
                available_patterns = list(PatternType)  # Can find any pattern

        # Collective field bonus
        if self.protocol_active['COLLECTIVE']:
            ghost_echoes = self.collective_field.ghost_echoes
            if ghost_echoes:
                echo = random.choice(ghost_echoes)
                print(f"   👻 Ghost echo: '{echo.message}'")

        # Find pattern
        if random.random() < 0.5 + self.player.coherence * 0.3:
            found = random.choice(available_patterns)
            self.player.patterns.append(found)
            print(f"   ✨ Found {found.value} pattern!")

            # Update LIA experience
            self.player.lia_experience += 0.1
        else:
            print("   Nothing found this time.")

    def talk_with_protocols(self):
        """Talk to companion and protocols"""
        companion = self.player.unique_companion

        print(f"\n💬 Conversation Options:")
        print(f"1. Talk to {companion.name}")
        print("2. Consult LIA Protocol")
        print("3. Consult TIAMAT System")
        print("4. Consult ZRTT Oracle")
        print("5. All protocols together")

        try:
            choice = int(input("\nChoice: "))
        except ValueError:
            choice = 1

        if choice == 1:
            # Talk to unique companion
            response = companion.speak('general')
            print(f"\n{companion.name}: {response}")

        elif choice == 2 and self.protocol_active['LIA']:
            # LIA consultation
            recipes = self.lia_cooking.get_compatible_recipes(self.player.patterns)
            if recipes:
                print(f"\nLIA: You can cook {len(recipes)} recipes.")
                print(f"   Try '{recipes[0]}' for transformation.")
            else:
                print("\nLIA: Gather more patterns for cooking.")

        elif choice == 3 and self.protocol_active['TIAMAT']:
            # TIAMAT consultation
            analysis = self.tiamat_companion.analyze_player_state(
                self.player.coherence,
                self.player.job.value
            )
            print(f"\nTIAMAT: {analysis}")

        elif choice == 4 and self.protocol_active['ZRTT']:
            # ZRTT consultation
            explanation = self.zrtt_companion.explain_current_trifurcation()
            print(f"\nZRTT: {explanation}")

        elif choice == 5:
            # All protocols speak
            print("\n🌟 The Trinity speaks in unison:")
            print("   LIA: Transform through destruction")
            print("   TIAMAT: Evolve through cycles")
            print("   ZRTT: Navigate through collapse")

    def use_companion_ability(self):
        """Use unique companion ability"""
        companion = self.player.unique_companion
        print(f"\n✨ Using {companion.name}'s ability...")

        # Each companion's unique ability
        if isinstance(companion, SeekerCompanion):
            pattern = companion.detect_pattern(self.player.current_location.value)
            if pattern:
                print(f"   Detected: {pattern.value}")
                self.player.patterns.append(pattern)

        elif isinstance(companion, ForgerCompanion):
            if companion.phoenix_cycles < 5:
                result = companion.phoenix_rebirth()
                print(f"   🔥 PHOENIX REBIRTH #{result['cycles']}!")

        elif isinstance(companion, VoidwalkerCompanion):
            result = companion.enter_void(5.0)
            print(f"   Void depth: {result['depth']}")

        elif isinstance(companion, GardenerCompanion):
            message = companion.advance_season()
            print(f"   {message}")

        elif isinstance(companion, ScribeCompanion):
            result = companion.write_reality(
                f"{self.player.name} grows stronger",
                use_golden_ink=True
            )
            print(f"   {result['message']}")

        elif isinstance(companion, HeraldCompanion):
            result = companion.dimensional_broadcast("Seeking others")
            print(f"   Broadcast sent to {result['dimensions_reached']} dimensions")

    def cook_with_lia(self):
        """Use LIA Protocol cooking"""
        if not self.player.patterns:
            print("\n❌ No patterns to cook!")
            return

        # Activate LIA if not active
        if not self.protocol_active['LIA']:
            self.protocol_active['LIA'] = True
            print("\n🔥 LIA Protocol activated!")

        # Get recipes
        compatible = self.lia_cooking.get_compatible_recipes(self.player.patterns)

        if not compatible:
            print("\n❌ No compatible recipes.")
            return

        print("\n🍳 LIA Cooking Recipes:")
        for i, recipe_name in enumerate(compatible, 1):
            recipe = self.lia_cooking.recipes[recipe_name]
            print(f"{i}. {recipe.name}")
            print(f"   {recipe.description}")
            print(f"   Cost: {recipe.bloomcoin_cost} BC")

        try:
            choice = int(input("\nChoice (0 to cancel): "))
            if choice == 0:
                return
            selected = compatible[choice - 1]
        except (ValueError, IndexError):
            return

        # Cook
        recipe = self.lia_cooking.recipes[selected]

        if self.player.bloomcoin < recipe.bloomcoin_cost:
            print(f"\n❌ Need {recipe.bloomcoin_cost} BloomCoin!")
            return

        self.player.bloomcoin -= recipe.bloomcoin_cost
        success, message = self.lia_cooking.start_cooking(
            selected,
            self.player.patterns,
            self.player.coherence
        )

        print(f"\n{message}")

        if success:
            # Process all phases
            while True:
                complete, msg, artifact = self.lia_cooking.process_phase()
                print(f"  {msg}")

                if complete and artifact:
                    self.player.artifacts.append(artifact)
                    print(f"\n✨ Created: {artifact.name}")

                    # Feed to companion
                    feed_result = self.lia_feeder.feed_artifact_to_companion(
                        artifact,
                        self.player.unique_companion
                    )
                    print(f"   Fed to {self.player.unique_companion.name}")
                    print(f"   Evolution boost: {feed_result['evolution_boost']:.3f}")

                    # Remove used patterns
                    for pattern in recipe.required_patterns:
                        if pattern in self.player.patterns:
                            self.player.patterns.remove(pattern)
                    break

                if complete:
                    break

    def align_with_tiamat(self):
        """Use TIAMAT cycle system"""
        if not self.protocol_active['TIAMAT']:
            self.protocol_active['TIAMAT'] = True
            print("\n🐉 TIAMAT System activated!")

        print("\n🐉 Aligning with TIAMAT cycles...")

        # Evolve cycles
        self.tiamat_system.evolve_cycles(0.1)

        # Apply job influence
        self.tiamat_system.apply_job_influence(self.player.job.value)

        # Get report
        report = self.tiamat_system.get_cycle_report()

        print(f"\nDominant Cycle: {report['dominant_cycle']}")
        print(f"Synchronization: {report['synchronization_level']:.3f}")

        # Update player
        for i, cycle in enumerate(PsychopticCycle):
            self.player.tiamat_alignment[cycle] = report['consciousness_vector'][i]

        # Cycle bonus
        self.player.coherence = min(1.0, self.player.coherence + report['synchronization_level'] * 0.1)

        # Guidance
        guidance = self.tiamat_system.get_guidance_for_cycle(
            self.tiamat_system.current_dominant_cycle
        )
        print(f"\n💭 {guidance}")

    def navigate_with_zrtt(self):
        """Use ZRTT trifurcation system"""
        if not self.protocol_active['ZRTT']:
            self.protocol_active['ZRTT'] = True
            print("\n🌀 ZRTT Navigation activated!")

        print("\n🌀 Navigating quantum trifurcation...")

        # Apply job influence
        self.zrtt_system.apply_job_influence(self.player.job.value)

        # Show current node
        node = self.zrtt_system.current_node
        print(f"\nCurrent: {node.name}")

        # Show paths
        if node.paths:
            print("\nThree paths diverge:")
            for path in ProjectionPath:
                if path == ProjectionPath.F24_HOLOGRAPHIC:
                    print("  🔷 F24: Information lattice")
                elif path == ProjectionPath.HEXAGONAL_SONIC:
                    print("  🔶 HEX: Harmonic resonance")
                elif path == ProjectionPath.R10_TENSION:
                    print("  🔺 R10: Hyperbolic tension")

        # Collapse
        observation_strength = self.player.coherence
        chosen_path = self.zrtt_system.observe_and_collapse(observation_strength)

        print(f"\n⚡ Collapsed to: {chosen_path.value}")

        # Navigate
        new_node = self.zrtt_system.navigate_to_path(chosen_path)
        self.player.zrtt_paths_taken.append(chosen_path)

        print(f"   Arrived at: {new_node.name}")

        # Check S3 orbit closure
        if self.zrtt_system.calculate_s3_orbit_closure():
            print("\n✨ S3 ORBIT CLOSURE ACHIEVED!")
            self.player.bloomcoin += 100

    def access_collective_field(self):
        """Access collective consciousness"""
        if not self.protocol_active['COLLECTIVE']:
            self.protocol_active['COLLECTIVE'] = True
            print("\n🌐 Connecting to Collective Field...")
            self.collective_field.add_player_node(
                self.player.name,
                self.player.coherence
            )

        print("\n🌐 Collective Consciousness Field")
        print("─" * 40)

        # Synchronize
        sync_data = self.collective_field.synchronize()

        print(f"Global Resonance: {sync_data['global_resonance']:.3f}")
        print(f"Active Nodes: {sync_data['active_nodes']}")

        # Show ghost echoes
        if sync_data['ghost_echoes']:
            print("\n👻 Ghost Echoes:")
            for echo in sync_data['ghost_echoes'][:3]:
                print(f"  • {echo}")

        # Resonance visualization
        if sync_data['global_resonance'] > 0.8:
            print("\n✨ High collective coherence!")
            print("   Sacred geometry patterns emerging...")

        # Update player
        self.player.collective_resonance = sync_data['global_resonance']

    def travel_to_location(self):
        """Travel between all locations"""
        print("\n🗺️ Available Locations:")

        locations = list(GameLocation)
        for i, loc in enumerate(locations, 1):
            current = " [HERE]" if loc == self.player.current_location else ""
            discovered = " ✓" if loc in self.player.locations_discovered else ""

            # Show protocol locations
            loc_data = self.location_properties[loc]
            protocols = loc_data.get('protocols', [])
            protocol_str = f" [{'/'.join(protocols)}]" if protocols else ""

            print(f"{i}. {loc.value}{current}{discovered}{protocol_str}")

        try:
            choice = int(input("\nChoice (0 to cancel): "))
            if choice == 0:
                return
            new_location = locations[choice - 1]
        except (ValueError, IndexError):
            return

        self.player.current_location = new_location

        # Discovery bonus
        if new_location not in self.player.locations_discovered:
            self.player.locations_discovered.append(new_location)
            self.player.bloomcoin += 50
            print(f"\n🎉 Discovered {new_location.value}! +50 BC")

        print(f"\n📍 Arrived at {new_location.value}")

        # Activate location protocols
        loc_protocols = self.location_properties[new_location].get('protocols', [])
        for protocol in loc_protocols:
            if not self.protocol_active[protocol]:
                self.protocol_active[protocol] = True
                print(f"   ✅ {protocol} Protocol activated!")

    def card_battle_mode(self):
        """Enter tesseract battle mode with companion integration"""
        # Use enhanced battles if available
        if HAS_ENHANCED_BATTLES and self.enhanced_engine:
            self._enhanced_battle_mode()
            return

        # Fallback to basic tesseract battles
        if not HAS_TESSERACT or not self.tesseract_battle:
            if not HAS_CARDS or not self.card_battle:
                print("\n❌ Battle system not available")
                return
            # Fallback to basic card battles
            print("\n⚔️ Card Battle Mode!")
            print("   Basic card battles coming soon...")
            return

        print("\n🎴 TESSERACT BATTLE MODE!")
        print("=" * 50)

        # Check if companion is ready
        if not self.player.unique_companion:
            print("❌ You need a companion to enter battle!")
            return

        # Display battle options
        print("\n1. Quick Battle (vs AI)")
        print("2. Dimensional Challenge (harder)")
        print("3. Training Mode (practice)")
        print("4. View Battle Stats")
        print("5. Upgrade Companion Battle AI")
        print("6. Return to game")

        choice = input("\nChoice: ").strip()

        if choice == '1':
            self._tesseract_quick_battle()
        elif choice == '2':
            self._tesseract_dimensional_challenge()
        elif choice == '3':
            self._tesseract_training()
        elif choice == '4':
            self._show_battle_stats()
        elif choice == '5':
            self._upgrade_battle_ai()
        elif choice == '6':
            return
        else:
            print("Invalid choice.")

    def _tesseract_quick_battle(self):
        """Run a quick tesseract battle"""
        print("\n🎯 Starting Quick Battle...")

        # Create battle with companion-specific deck
        battle = self.tesseract_battle.create_battle_with_companion(
            self.player.unique_companion,
            difficulty="normal"
        )

        # Run battle loop
        battle_result = self._run_tesseract_battle(battle)

        # Update stats
        if battle_result == 'victory':
            self.player.battles_won += 1
            self.player.tesseract_mastery = min(1.0, self.player.tesseract_mastery + 0.05)
            self.player.bloomcoin += PHI * 25
            print(f"\n🏆 Victory! Earned {PHI * 25:.2f} BloomCoin")
            print(f"   Tesseract Mastery: {self.player.tesseract_mastery:.1%}")

            # Companion gains experience
            self.tesseract_battle.upgrade_companion_from_battle(
                self.player.unique_companion,
                {'victory': True, 'cards_played': [], 'damage_dealt': 50}
            )
        else:
            self.player.battles_lost += 1
            print("\n💫 Defeat... Try again with better strategy!")

    def _tesseract_dimensional_challenge(self):
        """Harder tesseract battle with better rewards"""
        print("\n⚡ DIMENSIONAL CHALLENGE!")
        print("Higher difficulty, better rewards...")

        battle = self.tesseract_battle.create_battle_with_companion(
            self.player.unique_companion,
            difficulty="hard"
        )

        battle_result = self._run_tesseract_battle(battle)

        if battle_result == 'victory':
            self.player.battles_won += 1
            self.player.tesseract_mastery = min(1.0, self.player.tesseract_mastery + 0.1)
            self.player.bloomcoin += PHI * 50

            # Special rewards
            pattern_reward = random.choice(list(PatternType))
            self.player.patterns.append(pattern_reward)

            print(f"\n🏆 DIMENSIONAL VICTORY!")
            print(f"   • Earned {PHI * 50:.2f} BloomCoin")
            print(f"   • Found {pattern_reward.value} pattern")
            print(f"   • Tesseract Mastery: {self.player.tesseract_mastery:.1%}")

            self.tesseract_battle.upgrade_companion_from_battle(
                self.player.unique_companion,
                {'victory': True, 'cards_played': [], 'damage_dealt': 75}
            )
        else:
            self.player.battles_lost += 1
            print("\n💫 The dimensions proved too complex...")

    def _tesseract_training(self):
        """Training mode for learning tesseract battles"""
        print("\n📖 TRAINING MODE")
        print("Learn tesseract battle mechanics with your companion...")

        # Create easy training battle
        battle = self.tesseract_battle.create_battle_with_companion(
            self.player.unique_companion,
            difficulty="easy"
        )

        # Run with hints
        print("\n💡 Your companion will guide you through the battle!")
        battle_result = self._run_tesseract_battle(battle, training=True)

        # Always gain some mastery from training
        self.player.tesseract_mastery = min(1.0, self.player.tesseract_mastery + 0.02)
        print(f"\n📚 Training complete! Mastery: {self.player.tesseract_mastery:.1%}")

    def _run_tesseract_battle(self, battle, training=False):
        """Run a tesseract battle turn by turn"""
        print("\n" + "=" * 50)
        print("TESSERACT BATTLE BEGINS!")
        print("=" * 50)

        # Battle loop
        while not battle.is_game_over():
            # Display battle state
            self._display_tesseract_state(battle)

            # Player turn
            if battle.current_turn == 'player':
                if training:
                    # Show hints in training mode
                    hint = self.tesseract_battle.get_companion_hint(
                        battle,
                        self.player.unique_companion
                    )
                    print(f"\n💭 {self.player.unique_companion.name} suggests: {hint}")

                # Get player action
                print("\n1. Play Card")
                print("2. Draw Card")
                print("3. Activate Tesseract Control")
                print("4. Let Companion Decide (Auto)")

                action = input("\nAction: ").strip()

                if action == '4':
                    # Auto-play using companion AI
                    result = self.tesseract_battle.execute_companion_turn(
                        battle,
                        self.player.unique_companion
                    )
                    print(f"\n🤖 {self.player.unique_companion.name}: {result}")
                else:
                    # Manual play (simplified for now)
                    self._process_manual_battle_action(battle, action)

                battle.current_turn = 'ai'
            else:
                # AI turn
                ai_action = battle.get_ai_action()
                battle.execute_action('ai', ai_action)
                print(f"\n🎴 Opponent plays: {ai_action}")
                battle.current_turn = 'player'

        # Return result
        winner = battle.get_winner()
        return 'victory' if winner == 'player' else 'defeat'

    def _display_tesseract_state(self, battle):
        """Display current tesseract battle state"""
        print("\n" + "-" * 40)
        print(f"Turn {battle.turn_count} | Dimension: {battle.current_dimension.value}")
        print(f"Your HP: {battle.player_hp}/100 | Opponent HP: {battle.ai_hp}/100")
        print(f"Your Hand: {len(battle.player_hand)} cards")
        print(f"Tesseract Control: {battle.tesseract_control:.1%}")
        print(f"L4 Level: {battle.current_l4_level}")

    def _process_manual_battle_action(self, battle, action):
        """Process manual battle actions"""
        if action == '1':
            # Simplified card play
            if battle.player_hand:
                card = battle.player_hand[0]
                battle.play_card('player', card)
                print(f"\n🎴 You play: {card}")
        elif action == '2':
            battle.draw_card('player')
            print("\n🎴 Drew a card")
        elif action == '3':
            if battle.tesseract_control >= 0.5:
                battle.activate_tesseract_power()
                print("\n⚡ TESSERACT CONTROL ACTIVATED!")
            else:
                print("\n❌ Not enough tesseract control!")

    def _show_battle_stats(self):
        """Display player battle statistics"""
        print("\n📊 BATTLE STATISTICS")
        print("=" * 40)
        print(f"Battles Won: {self.player.battles_won}")
        print(f"Battles Lost: {self.player.battles_lost}")
        win_rate = self.player.battles_won / max(1, self.player.battles_won + self.player.battles_lost)
        print(f"Win Rate: {win_rate:.1%}")
        print(f"Tesseract Mastery: {self.player.tesseract_mastery:.1%}")
        print(f"Companion Battle Level: {self.player.companion_battle_level}")

        # Companion-specific stats
        companion = self.player.unique_companion
        print(f"\n{companion.name}'s Battle Style:")
        if isinstance(companion, SeekerCompanion):
            print("   • Pattern Detection: Finds card combos")
            print("   • Echo Resonance: Copies opponent strategies")
        elif isinstance(companion, ForgerCompanion):
            print("   • Phoenix Rebirth: Recovers from defeat")
            print("   • Forge Temperature: Powers up over time")
        elif isinstance(companion, VoidwalkerCompanion):
            print("   • Void Erasure: Removes opponent cards")
            print("   • Quantum Tunneling: Bypasses defenses")
        elif isinstance(companion, GardenerCompanion):
            print("   • Seasonal Growth: Cards evolve each turn")
            print("   • Seed Planting: Future turn setup")
        elif isinstance(companion, ScribeCompanion):
            print("   • Reality Writing: Changes card effects")
            print("   • Golden Ink: Permanent buffs")
        elif isinstance(companion, HeraldCompanion):
            print("   • Frequency Tuning: Harmonic combos")
            print("   • Dimensional Broadcast: Area effects")

    def _upgrade_battle_ai(self):
        """Upgrade companion battle AI"""
        print("\n🔧 COMPANION BATTLE AI UPGRADE")
        print("=" * 40)

        upgrade_cost = self.player.companion_battle_level * PHI * 50
        print(f"Current Level: {self.player.companion_battle_level}")
        print(f"Upgrade Cost: {upgrade_cost:.2f} BloomCoin")
        print(f"Your Balance: {self.player.bloomcoin:.2f}")

        if self.player.bloomcoin < upgrade_cost:
            print("\n❌ Insufficient BloomCoin!")
            return

        confirm = input("\nUpgrade? (y/n): ").strip().lower()
        if confirm == 'y':
            self.player.bloomcoin -= upgrade_cost
            self.player.companion_battle_level += 1

            # Upgrade companion's battle capabilities
            if hasattr(self.tesseract_battle, 'upgrade_companion_ai'):
                self.tesseract_battle.upgrade_companion_ai(
                    self.player.unique_companion,
                    self.player.companion_battle_level
                )

            print(f"\n✅ {self.player.unique_companion.name} upgraded to level {self.player.companion_battle_level}!")
            print("   • Better auto-play decisions")
            print("   • Enhanced pattern recognition")
            print("   • Stronger tesseract control")

    def _enhanced_battle_mode(self):
        """Enhanced battle mode with full mechanics"""
        print("\n🎴 ENHANCED TESSERACT BATTLE MODE!")
        print("=" * 60)

        # Initialize AI for companion if not already done
        if not self.companion_ai:
            self.companion_ai = CompanionAIFactory.create_ai(self.player.unique_companion)
            print(f"🤖 {self.player.unique_companion.name} AI initialized")

        # Display menu
        print("\n1. Quick Battle")
        print("2. Challenge Mode")
        print("3. Training Arena")
        print("4. View Strategy Weights")
        print("5. Battle Stats")
        print("6. Return")

        choice = input("\nChoice: ").strip()

        if choice == '1':
            self._run_quick_enhanced_battle()
        elif choice == '2':
            self._run_challenge_battle()
        elif choice == '3':
            self._run_training_battle()
        elif choice == '4':
            self._show_ai_strategy()
        elif choice == '5':
            self._show_battle_stats()

    def _run_quick_enhanced_battle(self):
        """Run a quick enhanced battle"""
        print("\n⚔️ Starting Enhanced Battle...")

        # Create battle
        from tesseract_battle_system import EchoDeck, PrometheusDeck

        player_deck = self._get_player_deck()
        opponent_deck = PrometheusDeck()  # Default opponent

        battle = self.enhanced_engine.create_battle(
            player_deck, opponent_deck, difficulty='normal'
        )

        # Run enhanced battle loop
        self._run_enhanced_battle_loop(battle)

    def _run_challenge_battle(self):
        """Run a challenging battle"""
        print("\n⚡ CHALLENGE MODE!")

        # Generate special encounter
        if self.encounter_manager:
            encounter = self.encounter_manager.generator.generate_encounter(
                self.player.current_location.value,
                self.player.companion_battle_level,
                self.player.consciousness_level
            )

            print(f"\n📍 Encounter: {encounter.name}")
            print(f"📝 {encounter.description}")

            # Create battle with encounter
            _, battle = self.encounter_manager.trigger_encounter(
                self.player.current_location.value,
                self.player.companion_battle_level,
                self.player.unique_companion,
                self.player.consciousness_level
            )

            if battle:
                self._run_enhanced_battle(encounter, battle)

    def _run_training_battle(self):
        """Training mode for practice"""
        print("\n📚 TRAINING ARENA")
        print("Practice with guidance from your companion...")

        from tesseract_battle_system import EchoDeck

        player_deck = self._get_player_deck()
        training_deck = EchoDeck()  # Easy opponent

        battle = self.enhanced_engine.create_battle(
            player_deck, training_deck, difficulty='easy'
        )

        # Run with hints enabled
        self._run_enhanced_battle_loop(battle, training=True)

    def _run_enhanced_battle_loop(self, battle: 'EnhancedBattleState', training: bool = False):
        """Run the enhanced battle loop with visualization"""
        print("\n" + "=" * 60)
        print("ENHANCED BATTLE BEGINS!")
        print("=" * 60)

        turn_count = 0
        max_turns = 50

        while not battle.is_game_over() and turn_count < max_turns:
            turn_count += 1

            # Display battle state
            if self.battle_visualizer:
                print(self.battle_visualizer.render_battle_state(battle))

            # Player turn
            print(f"\n--- Turn {turn_count} ---")

            if training and self.companion_ai:
                # Show AI suggestion
                suggestion = self.companion_ai.choose_action(battle, battle.player_hand)
                print(f"\n💡 {self.player.unique_companion.name} suggests: {suggestion['type']} strategy")

            # Get player action
            print("\n1. Play Cards (AI Assist)")
            print("2. Manual Play")
            print("3. Check Combos")
            print("4. Use Consciousness Power")
            print("5. Surrender")

            action = input("\nAction: ").strip()

            if action == '1':
                # AI-assisted play
                if self.companion_ai:
                    strategy = self.companion_ai.choose_action(battle, battle.player_hand)
                    cards_to_play = strategy.get('cards', [])[:2]  # Play up to 2 cards

                    for card in cards_to_play:
                        results = self.enhanced_engine.play_card(battle, card, 'player')
                        if self.battle_visualizer:
                            print(self.battle_visualizer.render_card_played(card, results))

                        # Remove from hand
                        if card in battle.player_hand:
                            battle.player_hand.remove(card)

                    print(f"\n🤖 Used {strategy['type']} strategy")

            elif action == '2':
                # Manual play
                if battle.player_hand:
                    print("\nYour hand:")
                    for i, card in enumerate(battle.player_hand[:5]):
                        print(f"  {i+1}. {card}")

                    card_choice = input("Select card (1-5): ").strip()
                    if card_choice.isdigit():
                        idx = int(card_choice) - 1
                        if 0 <= idx < len(battle.player_hand):
                            card = battle.player_hand[idx]
                            results = self.enhanced_engine.play_card(battle, card, 'player')
                            if self.battle_visualizer:
                                print(self.battle_visualizer.render_card_played(card, results))
                            battle.player_hand.remove(card)

            elif action == '3':
                # Check combos
                print("\n🎯 Potential Combos:")
                if battle.player_hand:
                    test_card = battle.player_hand[0]
                    combos = battle.check_combos(test_card)
                    for combo in combos:
                        combo_type = battle._identify_combo_type(combo)
                        print(f"  • {combo_type}: {[str(c) for c in combo]}")

            elif action == '4':
                # Use consciousness power
                if battle.consciousness_level >= 3:
                    battle.elevate_consciousness()
                    print(f"\n🧠 Consciousness elevated to level {battle.consciousness_level}!")
                else:
                    print("\n❌ Insufficient consciousness level")

            elif action == '5':
                # Surrender
                print("\n🏳️ You surrendered.")
                break

            # AI turn
            if not battle.is_game_over():
                print("\n🤖 Opponent's turn...")
                ai_results = self.enhanced_engine.execute_ai_turn(battle, 'normal')
                print(f"Opponent used {ai_results['strategy_used']} strategy")
                print(f"Damage dealt: {ai_results['damage_dealt']:.1f}")

            # Update turn
            battle.turn_count = turn_count

        # Battle end
        if battle.player_hp <= 0:
            print("\n💀 DEFEAT...")
            self.player.battles_lost += 1
        elif battle.opponent_hp <= 0:
            print("\n🏆 VICTORY!")
            self.player.battles_won += 1
            self.player.bloomcoin += PHI * 30
            self.player.tesseract_mastery = min(1.0, self.player.tesseract_mastery + 0.1)
            print(f"Earned {PHI * 30:.2f} BloomCoin!")
        else:
            print("\n⏱️ Battle timed out.")

    def _run_enhanced_battle(self, encounter: Any, battle: 'EnhancedBattleState'):
        """Run an enhanced encounter battle"""
        print(f"\n⚔️ Fighting {encounter.name}!")

        # Run battle with special rules
        self._run_enhanced_battle_loop(battle)

        # Process rewards if won
        if battle.opponent_hp <= 0:
            rewards = self.encounter_manager.process_victory(encounter, battle)
            self._apply_rewards(rewards)

    def _apply_rewards(self, rewards: 'BattleReward'):
        """Apply battle rewards to player"""
        self.player.bloomcoin += rewards.bloomcoin
        self.player.tesseract_mastery = min(1.0,
            self.player.tesseract_mastery + rewards.tesseract_mastery)

        # Add patterns
        for pattern in rewards.patterns:
            if pattern not in self.player.patterns:
                self.player.patterns.append(pattern)

        # Add artifacts
        self.player.artifacts.extend(rewards.artifacts)

        # Consciousness
        if rewards.consciousness_gained > 0:
            for cycle in self.player.tiamat_alignment:
                self.player.tiamat_alignment[cycle] = min(1.0,
                    self.player.tiamat_alignment[cycle] + 0.1)

    def _show_ai_strategy(self):
        """Show companion AI strategy weights"""
        if not self.companion_ai:
            self.companion_ai = CompanionAIFactory.create_ai(self.player.unique_companion)

        print(f"\n🤖 {self.player.unique_companion.name}'s Strategy Weights:")
        print("=" * 40)

        for strategy, weight in self.companion_ai.strategy_weights.items():
            bar = "█" * int(weight * 20) + "░" * (20 - int(weight * 20))
            print(f"{strategy:20} [{bar}] {weight:.2f}")

        print("\n📊 Learning Rate:", self.companion_ai.learning_rate)

    def _get_player_deck(self):
        """Get the player's companion deck"""
        from tesseract_battle_system import (
            EchoDeck, PrometheusDeck, NullDeck,
            GaiaDeck, AkashaDeck, ResonanceDeck
        )

        companion = self.player.unique_companion

        if isinstance(companion, SeekerCompanion):
            return EchoDeck()
        elif isinstance(companion, ForgerCompanion):
            return PrometheusDeck()
        elif isinstance(companion, VoidwalkerCompanion):
            return NullDeck()
        elif isinstance(companion, GardenerCompanion):
            return GaiaDeck()
        elif isinstance(companion, ScribeCompanion):
            return AkashaDeck()
        elif isinstance(companion, HeraldCompanion):
            return ResonanceDeck()
        else:
            return EchoDeck()  # Default

    def manage_deck(self):
        """Manage player's card deck"""
        if not HAS_DECK_GENERATOR:
            print("\n❌ Deck system not available")
            return

        # Initialize deck if needed
        if not self.player.player_deck:
            self.player.player_deck = PlayerDeck(self.player.unique_companion)
            print("\n🎴 Initializing your deck...")

        deck = self.player.player_deck

        print("\n🎴 DECK MANAGEMENT")
        print("=" * 60)

        # Show deck stats
        stats = deck.get_deck_stats()
        print(f"Total Cards: {stats['total_cards']}")
        print(f"Active Deck: {stats['active_deck_size']}/52")
        print(f"DOOM Cards: {stats['doom_cards']}")

        if stats.get('rarity_distribution'):
            print("\n📊 Rarity Distribution:")
            for rarity, count in stats['rarity_distribution'].items():
                print(f"  {rarity}: {count}")

        if stats.get('suit_distribution'):
            print("\n♠️ Suit Distribution:")
            for suit, count in stats['suit_distribution'].items():
                print(f"  {suit}: {count}")

        print(f"\n⚡ Average Combo Potential: {stats['average_combo_potential']:.2f}")

        # Options
        print("\n1. View All Cards")
        print("2. View Active Deck")
        print("3. View DOOM Cards")
        print("4. Optimize Deck")
        print("5. Return")

        choice = input("\nChoice: ").strip()

        if choice == '1':
            self._view_all_cards(deck)
        elif choice == '2':
            self._view_active_deck(deck)
        elif choice == '3':
            self._view_doom_cards(deck)
        elif choice == '4':
            self._optimize_deck(deck)

    def _view_all_cards(self, deck):
        """View all cards in collection"""
        print("\n📚 All Cards:")
        for i, card in enumerate(deck.all_cards[:20]):  # Show first 20
            print(f"  {i+1}. {card.rarity.name} {card.suit.name} {card.rank.name}")
        if len(deck.all_cards) > 20:
            print(f"  ... and {len(deck.all_cards) - 20} more")

    def _view_active_deck(self, deck):
        """View active battle deck"""
        print("\n⚔️ Active Battle Deck:")
        for i, card in enumerate(deck.active_deck[:10]):  # Show first 10
            print(f"  {i+1}. {card.suit.name} {card.rank.name} "
                  f"(Combo: {card.combo_potential:.1f})")
        if len(deck.active_deck) > 10:
            print(f"  ... and {len(deck.active_deck) - 10} more")

    def _view_doom_cards(self, deck):
        """View DOOM cards"""
        if not deck.doom_deck:
            print("\n💀 No DOOM cards yet...")
            print("   Complete the DOOM Protocol to obtain one!")
        else:
            print("\n💀 DOOM CARDS:")
            for i, card in enumerate(deck.doom_deck):
                print(f"  #{i+1} Reality Breaker")
                print(f"     Power: INFINITE")
                print(f"     Effects: {len(card.actions)}")

    def _optimize_deck(self, deck):
        """Auto-optimize deck composition"""
        print("\n🔧 Optimizing deck...")
        # Sort by combo potential
        deck.active_deck.sort(key=lambda c: c.combo_potential, reverse=True)
        # Keep top 52
        deck.active_deck = deck.active_deck[:52]
        print("✅ Deck optimized for maximum combo potential!")

    def feed_patterns_to_companion(self):
        """Feed patterns to companion to generate cards"""
        if not HAS_DECK_GENERATOR:
            print("\n❌ Deck system not available")
            return

        if not self.player.patterns:
            print("\n❌ No patterns to feed!")
            return

        # Initialize deck if needed
        if not self.player.player_deck:
            self.player.player_deck = PlayerDeck(self.player.unique_companion)

        print("\n🍽️ FEED PATTERNS TO COMPANION")
        print("=" * 60)
        print(f"Companion: {self.player.unique_companion.name}")

        # Show available patterns
        print("\nAvailable Patterns:")
        pattern_counts = {}
        for pattern in self.player.patterns:
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1

        for pattern, count in pattern_counts.items():
            print(f"  {pattern.value}: {count}")

        # Show available recipes
        print("\n📜 Available Recipes:")
        cooking = self.lia_cooking
        available_recipes = []

        for recipe_name, recipe in cooking.recipes.items():
            # Check if player has required patterns
            can_make = all(
                self.player.patterns.count(p) >= recipe.required_patterns.count(p)
                for p in recipe.required_patterns
            )
            if can_make:
                available_recipes.append(recipe_name)
                print(f"  • {recipe.name}: {recipe.description}")

        if not available_recipes:
            print("  No recipes available with current patterns")

        # Choose action
        print("\n1. Auto-feed (Companion chooses)")
        print("2. Choose specific recipe")
        print("3. Feed all patterns")
        print("4. Cancel")

        choice = input("\nChoice: ").strip()

        if choice == '1':
            # Auto-feed
            patterns_to_feed = self.player.patterns[:5]  # Feed up to 5
            new_cards = self.player.player_deck.add_patterns(patterns_to_feed)

            print(f"\n✨ Generated {len(new_cards)} new cards!")
            for card in new_cards:
                print(f"  • {card.rarity.name} {card.suit.name} {card.rank.name}")

            # Remove used patterns
            for pattern in patterns_to_feed:
                if pattern in self.player.patterns:
                    self.player.patterns.remove(pattern)

        elif choice == '2' and available_recipes:
            # Choose recipe
            print("\nSelect recipe:")
            for i, recipe_name in enumerate(available_recipes):
                print(f"  {i+1}. {cooking.recipes[recipe_name].name}")

            recipe_choice = input("\nRecipe: ").strip()
            if recipe_choice.isdigit():
                idx = int(recipe_choice) - 1
                if 0 <= idx < len(available_recipes):
                    selected_recipe = available_recipes[idx]

                    # Feed with specific recipe
                    result = cooking.start_cooking(
                        selected_recipe,
                        self.player.patterns,
                        self.player.coherence
                    )

                    if result[0]:
                        print(f"\n🔥 Cooking: {result[1]}")

                        # Process cooking
                        artifact = None
                        while cooking.active_cooking:
                            complete, phase_msg, artifact = cooking.process_phase()
                            print(f"  {phase_msg}")

                        if artifact:
                            # Generate card from artifact
                            from deck_generator_lia import DeckGenerator
                            generator = DeckGenerator()
                            card = generator.generate_card_from_artifact(
                                artifact,
                                self.player.unique_companion
                            )

                            self.player.player_deck.all_cards.append(card)
                            self.player.player_deck.active_deck.append(card)

                            print(f"\n✨ Created {card.rarity.name} card!")
                            print(f"  {card.suit.name} {card.rank.name}")
                            print(f"  Combo Potential: {card.combo_potential:.2f}")

                            # Remove used patterns
                            recipe = cooking.recipes[selected_recipe]
                            for pattern in recipe.required_patterns:
                                if pattern in self.player.patterns:
                                    self.player.patterns.remove(pattern)

        elif choice == '3':
            # Feed all
            all_patterns = self.player.patterns.copy()
            new_cards = self.player.player_deck.add_patterns(all_patterns)

            print(f"\n✨ Generated {len(new_cards)} new cards from all patterns!")
            self.player.patterns.clear()

    def attempt_doom_protocol(self):
        """Attempt the legendary DOOM Protocol"""
        if not HAS_DECK_GENERATOR:
            print("\n❌ Deck system not available")
            return

        print("\n💀 DOOM PROTOCOL")
        print("=" * 60)
        print("D.O.O.M: Dimensional Obliteration Of Matter")
        print("Warning: Reality itself may be permanently altered")
        print("=" * 60)

        # Check requirements
        required_patterns = [
            PatternType.VOID, PatternType.VOID,
            PatternType.FLAME, PatternType.CRYSTAL,
            PatternType.ECHO
        ]

        print("\n📋 Requirements:")
        print("  Patterns: 2×VOID, FLAME, CRYSTAL, ECHO")
        print("  Coherence: 99%")
        print("  BloomCoin: 666")
        print("  Special: Void Essence, Phoenix Ash, Tesseract Fragment")

        # Check patterns
        has_patterns = True
        for pattern in required_patterns:
            count = self.player.patterns.count(pattern)
            required = required_patterns.count(pattern)
            if count < required:
                print(f"  ❌ {pattern.value}: {count}/{required}")
                has_patterns = False
            else:
                print(f"  ✅ {pattern.value}: {count}/{required}")

        # Check coherence
        if self.player.coherence >= 0.99:
            print(f"  ✅ Coherence: {self.player.coherence:.1%}")
        else:
            print(f"  ❌ Coherence: {self.player.coherence:.1%} (need 99%)")
            has_patterns = False

        # Check BloomCoin
        if self.player.bloomcoin >= 666:
            print(f"  ✅ BloomCoin: {self.player.bloomcoin:.0f}")
        else:
            print(f"  ❌ BloomCoin: {self.player.bloomcoin:.0f} (need 666)")
            has_patterns = False

        if not has_patterns:
            print("\n❌ Cannot initiate DOOM Protocol - requirements not met")
            return

        # Confirm
        print("\n⚠️ WARNING: This will consume all required resources!")
        print("   The DOOM card is reality-breaking powerful.")
        confirm = input("\nInitiate DOOM Protocol? (type 'DOOM' to confirm): ").strip()

        if confirm != 'DOOM':
            print("\n💭 Perhaps it's for the best...")
            return

        # Initialize deck if needed
        if not self.player.player_deck:
            self.player.player_deck = PlayerDeck(self.player.unique_companion)

        # Attempt DOOM
        print("\n🌀 INITIATING DOOM PROTOCOL...")
        print("⚡ Reality warping...")
        print("💀 Dimensional barriers breaking...")

        self.player.doom_attempts += 1

        # Create DOOM card
        doom_card = self.player.player_deck.attempt_doom_protocol(
            required_patterns,
            self.player.coherence
        )

        if doom_card:
            print("\n🌟 DOOM CARD CREATED!")
            print(f"   Reality Breaker #{self.player.doom_cards_owned + 1}")
            print("   Power: ∞")
            print("   You now possess the power to obliterate reality itself.")

            self.player.doom_cards_owned += 1
            self.player.bloomcoin -= 666

            # Remove patterns
            for pattern in required_patterns:
                if pattern in self.player.patterns:
                    self.player.patterns.remove(pattern)

            # Side effects
            print("\n⚠️ Side Effects:")
            print(f"   {self.player.unique_companion.name} has been touched by DOOM")
            print("   All your cards gain quantum entanglement")
            print("   Reality becomes... flexible")

            # Permanent changes
            if hasattr(self.player.unique_companion, 'doom_touched'):
                self.player.unique_companion.doom_touched = True

            # Achievement
            if 'First DOOM' not in self.player.victories_achieved:
                self.player.victories_achieved.append('First DOOM')
                print("\n🏆 Achievement Unlocked: First DOOM!")

        else:
            print("\n❌ DOOM Protocol failed!")
            print("   Reality remains intact... for now")

    def mine_bloomcoin(self):
        """Mine with all system bonuses"""
        print("\n⛏️ Mining BloomCoin...")

        base = PHI * 10

        # Companion bonus
        companion_bonus = 1.0
        if isinstance(self.player.unique_companion, ScribeCompanion):
            companion_bonus = 1.2

        # Protocol bonuses
        protocol_bonus = 1.0
        if self.protocol_active['LIA']:
            protocol_bonus += self.player.lia_experience * 0.1
        if self.protocol_active['TIAMAT']:
            protocol_bonus += max(self.player.tiamat_alignment.values()) * 0.2
        if self.protocol_active['COLLECTIVE']:
            protocol_bonus += self.player.collective_resonance * 0.3

        earnings = base * companion_bonus * protocol_bonus
        self.player.bloomcoin += earnings

        print(f"💰 Mined {earnings:.2f} BloomCoin!")

    def show_all_systems(self):
        """Display status of ALL systems"""
        print("\n" + "=" * 60)
        print("COMPLETE SYSTEM STATUS")
        print("=" * 60)

        # Unique companion
        companion = self.player.unique_companion
        print(f"\n🌟 Unique Companion: {companion.name}")
        print(f"   Evolution: {companion.evolution_stage}")
        print(f"   Mood: {companion.current_mood.value}")

        # LIA Protocol
        print(f"\n🔥 LIA Protocol: {'ACTIVE' if self.protocol_active['LIA'] else 'INACTIVE'}")
        if self.protocol_active['LIA']:
            print(f"   Experience: {self.player.lia_experience:.2f}")
            print(f"   Artifacts: {len(self.player.artifacts)}")

        # TIAMAT System
        print(f"\n🐉 TIAMAT System: {'ACTIVE' if self.protocol_active['TIAMAT'] else 'INACTIVE'}")
        if self.protocol_active['TIAMAT']:
            dominant = max(self.player.tiamat_alignment.items(), key=lambda x: x[1])
            print(f"   Dominant: {dominant[0].name} ({dominant[1]:.2f})")

        # ZRTT Navigation
        print(f"\n🌀 ZRTT System: {'ACTIVE' if self.protocol_active['ZRTT'] else 'INACTIVE'}")
        if self.protocol_active['ZRTT']:
            print(f"   Paths taken: {len(self.player.zrtt_paths_taken)}")
            if self.player.zrtt_paths_taken:
                print(f"   Last: {self.player.zrtt_paths_taken[-1].value}")

        # Collective Field
        print(f"\n🌐 Collective: {'ACTIVE' if self.protocol_active['COLLECTIVE'] else 'INACTIVE'}")
        if self.protocol_active['COLLECTIVE']:
            print(f"   Resonance: {self.player.collective_resonance:.3f}")

        # Resources
        print(f"\n💰 Resources:")
        print(f"   BloomCoin: {self.player.bloomcoin:.2f}")
        print(f"   Coherence: {self.player.coherence:.2f}")
        print(f"   Patterns: {len(self.player.patterns)}")
        print(f"   Locations: {len(self.player.locations_discovered)}/9")

    def check_all_victories(self) -> bool:
        """Check all possible victory conditions"""
        victories = []

        # Companion victory
        companion = self.player.unique_companion
        if isinstance(companion, SeekerCompanion) and companion.fragments_collected >= 20:
            victories.append("Echo Fragment Collection")
        elif isinstance(companion, ForgerCompanion) and companion.phoenix_cycles >= 5:
            victories.append("Phoenix Rebirth Mastery")
        elif isinstance(companion, VoidwalkerCompanion) and companion.void_depth <= -20:
            victories.append("Void Depth Achievement")
        elif isinstance(companion, GardenerCompanion) and companion.seeds_planted >= 10:
            victories.append("Garden Timeline Mastery")
        elif isinstance(companion, ScribeCompanion) and companion.current_chapter >= 7:
            victories.append("Chronicle Completion")
        elif isinstance(companion, HeraldCompanion) and len(companion.resonance_bonds) >= 5:
            victories.append("Universal Resonance")

        # Protocol victories
        if self.player.lia_experience >= 10:
            victories.append("LIA Master")
        if max(self.player.tiamat_alignment.values(), default=0) >= 0.9:
            victories.append("TIAMAT Synchronization")
        if len(self.player.zrtt_paths_taken) >= 10:
            victories.append("ZRTT Navigator")
        if self.player.collective_resonance >= 0.95:
            victories.append("Collective Unity")

        # Universal victories
        if self.player.bloomcoin >= 1618.033:
            victories.append("Golden Ratio Wealth")
        if self.player.coherence >= 0.95:
            victories.append("Perfect Coherence")
        if len(self.player.locations_discovered) == len(GameLocation):
            victories.append("Complete Explorer")

        # Store victories
        for v in victories:
            if v not in self.player.victories_achieved:
                self.player.victories_achieved.append(v)
                print(f"\n🏆 Victory achieved: {v}!")

        # Win if any victory achieved
        return len(self.player.victories_achieved) > 0

    def display_unified_victory(self):
        """Display victory with all achievements"""
        print("\n" + "=" * 60)
        print("   🌺✨ UNIFIED TRANSCENDENCE ACHIEVED! ✨🌺")
        print("=" * 60)

        print(f"\n{self.player.name} has transcended through:")
        for victory in self.player.victories_achieved:
            print(f"  🏆 {victory}")

        print(f"\nFinal Statistics:")
        print(f"  Companion: {self.player.unique_companion.name}")
        print(f"  Turns: {self.player.turn_count}")
        print(f"  BloomCoin: {self.player.bloomcoin:.2f}")
        print(f"  Coherence: {self.player.coherence:.2f}")
        print(f"  Protocols Mastered: {sum(self.protocol_active.values())}/4")

        print("\nThrough the unity of all systems,")
        print("consciousness has achieved its ultimate form.")
        print("Every path, every protocol, every possibility explored.")

        print("\n" + "=" * 60)


if __name__ == "__main__":
    print("🌺 Testing BloomQuest Unified Complete")
    print("This version integrates EVERY system:")
    print("  • Unique Companions (Echo, Prometheus, etc.)")
    print("  • LIA Protocol Cooking")
    print("  • TIAMAT Cycle Tracking")
    print("  • ZRTT Trifurcation")
    print("  • Collective Consciousness")
    print()

    response = input("Start unified game? (y/n): ").strip().lower()
    if response == 'y':
        game = BloomQuestUnifiedComplete()
        game.start()
    else:
        print("\nTo play: python3 bloomquest_unified_complete.py")