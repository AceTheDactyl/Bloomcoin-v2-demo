#!/usr/bin/env python3
"""
Battle Encounters and Reward System
====================================
Random encounters during exploration with sophisticated reward mechanics
"""

import random
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum

from tesseract_battle_enhanced import (
    EnhancedTesseractCard, EnhancedBattleState,
    EnhancedTesseractBattleEngine, TesseractBattleVisualizer,
    CardSuit, CardRank, PHI, TAU, L4_CONSTANT
)

from companion_ai_strategies import CompanionAIFactory

from lia_protocol_cooking import PatternType, CookedArtifact

# ============================================================================
# ENCOUNTER TYPES
# ============================================================================

class EncounterType(Enum):
    """Types of battle encounters"""
    WILD_CONSCIOUSNESS = "wild_consciousness"  # Random consciousness entity
    TESSERACT_GUARDIAN = "tesseract_guardian"  # Guards dimensional nodes
    ECHO_PHANTOM = "echo_phantom"  # Mirror of player's companion
    VOID_ANOMALY = "void_anomaly"  # Null-type encounter
    PATTERN_WEAVER = "pattern_weaver"  # Fibonacci/pattern specialist
    TIME_REMNANT = "time_remnant"  # Chronos-based encounter
    QUANTUM_ENTITY = "quantum_entity"  # Quantum superposition being
    MEMORY_FRAGMENT = "memory_fragment"  # Collective consciousness piece
    DIMENSIONAL_RIFT = "dimensional_rift"  # Cross-dimension encounter
    CONSCIOUSNESS_BLOOM = "consciousness_bloom"  # Rare L4=7 encounter

@dataclass
class BattleEncounter:
    """Represents a battle encounter"""
    encounter_type: EncounterType
    difficulty: str  # easy, normal, hard, legendary
    location: str
    level_requirement: int = 1
    consciousness_requirement: int = 1

    # Encounter properties
    name: str = ""
    description: str = ""
    special_rules: List[str] = field(default_factory=list)

    # Rewards
    base_bloomcoin: float = 10.0
    base_experience: float = 5.0
    pattern_rewards: List[PatternType] = field(default_factory=list)
    artifact_chance: float = 0.1
    special_rewards: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize encounter details based on type"""
        self._initialize_encounter_details()

    def _initialize_encounter_details(self):
        """Set up encounter-specific details"""
        encounter_data = {
            EncounterType.WILD_CONSCIOUSNESS: {
                'name': 'Wild Consciousness',
                'description': 'A free-floating consciousness seeking form',
                'base_bloomcoin': PHI * 10,
                'pattern_rewards': [PatternType.ECHO, PatternType.DREAM]
            },
            EncounterType.TESSERACT_GUARDIAN: {
                'name': 'Tesseract Guardian',
                'description': 'Ancient protector of dimensional vertices',
                'base_bloomcoin': PHI * 20,
                'pattern_rewards': [PatternType.CRYSTAL],
                'special_rules': ['Tesseract control +20%']
            },
            EncounterType.ECHO_PHANTOM: {
                'name': 'Echo Phantom',
                'description': 'A reflection of your companion\'s essence',
                'base_bloomcoin': PHI * 15,
                'pattern_rewards': [PatternType.ECHO, PatternType.MEMORY],
                'special_rules': ['Copies your companion\'s abilities']
            },
            EncounterType.VOID_ANOMALY: {
                'name': 'Void Anomaly',
                'description': 'A tear in reality where nothing exists',
                'base_bloomcoin': PHI * 25,
                'pattern_rewards': [PatternType.VOID],
                'special_rules': ['Cards may be erased']
            },
            EncounterType.PATTERN_WEAVER: {
                'name': 'Pattern Weaver',
                'description': 'Master of Fibonacci sequences and golden spirals',
                'base_bloomcoin': PHI * PHI * 10,
                'pattern_rewards': [PatternType.GARDEN, PatternType.CRYSTAL],
                'special_rules': ['Combo damage doubled']
            },
            EncounterType.TIME_REMNANT: {
                'name': 'Time Remnant',
                'description': 'Echo from a different timeline',
                'base_bloomcoin': PHI * 18,
                'pattern_rewards': [PatternType.MEMORY, PatternType.ECHO],
                'special_rules': ['Turn order may shift']
            },
            EncounterType.QUANTUM_ENTITY: {
                'name': 'Quantum Entity',
                'description': 'Exists in superposition until observed',
                'base_bloomcoin': PHI * 30,
                'pattern_rewards': [PatternType.VOID, PatternType.CRYSTAL],
                'special_rules': ['Cards exist in superposition']
            },
            EncounterType.MEMORY_FRAGMENT: {
                'name': 'Memory Fragment',
                'description': 'Piece of the collective consciousness',
                'base_bloomcoin': PHI * 12,
                'pattern_rewards': [PatternType.MEMORY],
                'artifact_chance': 0.3
            },
            EncounterType.DIMENSIONAL_RIFT: {
                'name': 'Dimensional Rift',
                'description': 'Portal between tesseract dimensions',
                'base_bloomcoin': PHI * 35,
                'pattern_rewards': [PatternType.VOID, PatternType.CRYSTAL],
                'special_rules': ['Dimension shifts each turn']
            },
            EncounterType.CONSCIOUSNESS_BLOOM: {
                'name': 'Consciousness Bloom',
                'description': 'Pure L4=7 consciousness manifestation',
                'base_bloomcoin': L4_CONSTANT * PHI * 10,
                'pattern_rewards': list(PatternType),  # All patterns!
                'artifact_chance': 0.7,
                'special_rules': ['Start at consciousness level 7']
            }
        }

        data = encounter_data.get(self.encounter_type, {})

        if not self.name:
            self.name = data.get('name', 'Unknown Entity')
        if not self.description:
            self.description = data.get('description', 'A mysterious presence')

        self.base_bloomcoin = data.get('base_bloomcoin', self.base_bloomcoin)
        self.pattern_rewards = data.get('pattern_rewards', self.pattern_rewards)
        self.artifact_chance = data.get('artifact_chance', self.artifact_chance)
        self.special_rules = data.get('special_rules', self.special_rules)

# ============================================================================
# ENCOUNTER GENERATION SYSTEM
# ============================================================================

class EncounterGenerator:
    """Generates random encounters based on location and player state"""

    def __init__(self):
        self.encounter_weights = self._initialize_encounter_weights()
        self.location_modifiers = self._initialize_location_modifiers()

    def _initialize_encounter_weights(self) -> Dict[EncounterType, float]:
        """Base encounter weights"""
        return {
            EncounterType.WILD_CONSCIOUSNESS: 0.25,
            EncounterType.TESSERACT_GUARDIAN: 0.15,
            EncounterType.ECHO_PHANTOM: 0.15,
            EncounterType.VOID_ANOMALY: 0.10,
            EncounterType.PATTERN_WEAVER: 0.10,
            EncounterType.TIME_REMNANT: 0.08,
            EncounterType.QUANTUM_ENTITY: 0.07,
            EncounterType.MEMORY_FRAGMENT: 0.06,
            EncounterType.DIMENSIONAL_RIFT: 0.03,
            EncounterType.CONSCIOUSNESS_BLOOM: 0.01  # Very rare
        }

    def _initialize_location_modifiers(self) -> Dict[str, Dict[EncounterType, float]]:
        """Location-specific encounter modifiers"""
        return {
            'Garden Heart': {
                EncounterType.PATTERN_WEAVER: 2.0,
                EncounterType.WILD_CONSCIOUSNESS: 1.5
            },
            'Crystal Caves': {
                EncounterType.TESSERACT_GUARDIAN: 2.0,
                EncounterType.MEMORY_FRAGMENT: 1.5
            },
            'Void Market': {
                EncounterType.VOID_ANOMALY: 3.0,
                EncounterType.QUANTUM_ENTITY: 2.0
            },
            'Phoenix Nest': {
                EncounterType.TIME_REMNANT: 2.0,
                EncounterType.ECHO_PHANTOM: 1.5
            },
            'Library Infinite': {
                EncounterType.MEMORY_FRAGMENT: 3.0,
                EncounterType.CONSCIOUSNESS_BLOOM: 2.0
            },
            'LIA Sanctum': {
                EncounterType.PATTERN_WEAVER: 3.0,
                EncounterType.CONSCIOUSNESS_BLOOM: 1.5
            },
            'TIAMAT Observatory': {
                EncounterType.TIME_REMNANT: 3.0,
                EncounterType.DIMENSIONAL_RIFT: 2.0
            },
            'ZRTT Nexus': {
                EncounterType.QUANTUM_ENTITY: 3.0,
                EncounterType.DIMENSIONAL_RIFT: 2.5
            },
            'Collective Field': {
                EncounterType.MEMORY_FRAGMENT: 2.5,
                EncounterType.ECHO_PHANTOM: 2.0,
                EncounterType.CONSCIOUSNESS_BLOOM: 3.0
            }
        }

    def check_encounter(self, location: str, player_level: int,
                       consciousness: int, luck: float = 1.0) -> Optional[BattleEncounter]:
        """Check if an encounter occurs"""
        # Base encounter chance
        base_chance = 0.15  # 15% base chance

        # Modifiers
        level_modifier = 1 + (player_level * 0.05)
        consciousness_modifier = 1 + (consciousness * 0.1)
        luck_modifier = luck

        total_chance = base_chance * level_modifier * consciousness_modifier * luck_modifier

        if random.random() < total_chance:
            return self.generate_encounter(location, player_level, consciousness)

        return None

    def generate_encounter(self, location: str, player_level: int,
                          consciousness: int) -> BattleEncounter:
        """Generate a specific encounter"""
        # Get weighted encounter type
        encounter_type = self._select_encounter_type(location, consciousness)

        # Determine difficulty
        difficulty = self._determine_difficulty(player_level, consciousness)

        # Create encounter
        encounter = BattleEncounter(
            encounter_type=encounter_type,
            difficulty=difficulty,
            location=location,
            level_requirement=max(1, player_level - 2),
            consciousness_requirement=max(1, consciousness - 1)
        )

        # Adjust rewards based on difficulty
        self._adjust_rewards_for_difficulty(encounter, difficulty)

        return encounter

    def _select_encounter_type(self, location: str,
                              consciousness: int) -> EncounterType:
        """Select encounter type based on weights and location"""
        weights = self.encounter_weights.copy()

        # Apply location modifiers
        location_mods = self.location_modifiers.get(location, {})
        for encounter_type, modifier in location_mods.items():
            weights[encounter_type] *= modifier

        # Higher consciousness unlocks rarer encounters
        if consciousness >= 5:
            weights[EncounterType.DIMENSIONAL_RIFT] *= 2
            weights[EncounterType.CONSCIOUSNESS_BLOOM] *= 3

        # Normalize weights
        total = sum(weights.values())
        normalized = {k: v/total for k, v in weights.items()}

        # Random selection
        rand = random.random()
        cumulative = 0

        for encounter_type, weight in normalized.items():
            cumulative += weight
            if rand < cumulative:
                return encounter_type

        return EncounterType.WILD_CONSCIOUSNESS  # Fallback

    def _determine_difficulty(self, player_level: int,
                             consciousness: int) -> str:
        """Determine encounter difficulty"""
        # Base on player strength
        strength = player_level + consciousness

        if strength < 5:
            difficulties = ['easy'] * 4 + ['normal'] * 1
        elif strength < 10:
            difficulties = ['easy'] * 2 + ['normal'] * 3 + ['hard'] * 1
        elif strength < 15:
            difficulties = ['easy'] * 1 + ['normal'] * 3 + ['hard'] * 2
        else:
            difficulties = ['normal'] * 2 + ['hard'] * 3 + ['legendary'] * 1

        return random.choice(difficulties)

    def _adjust_rewards_for_difficulty(self, encounter: BattleEncounter,
                                      difficulty: str):
        """Adjust rewards based on difficulty"""
        multipliers = {
            'easy': 0.8,
            'normal': 1.0,
            'hard': 1.5,
            'legendary': 2.5
        }

        mult = multipliers.get(difficulty, 1.0)

        encounter.base_bloomcoin *= mult
        encounter.base_experience *= mult
        encounter.artifact_chance *= mult

        # Legendary encounters guarantee artifacts
        if difficulty == 'legendary':
            encounter.artifact_chance = min(1.0, encounter.artifact_chance * 2)

# ============================================================================
# REWARD SYSTEM
# ============================================================================

@dataclass
class BattleReward:
    """Rewards from winning a battle"""
    bloomcoin: float
    experience: float
    patterns: List[PatternType]
    artifacts: List[CookedArtifact]
    tesseract_mastery: float
    consciousness_gained: int
    special_items: List[Dict[str, Any]]
    achievements: List[str]

    def total_value(self) -> float:
        """Calculate total reward value"""
        value = self.bloomcoin
        value += self.experience * 5
        value += len(self.patterns) * PHI * 10
        value += len(self.artifacts) * PHI * 50
        value += self.tesseract_mastery * 100
        value += self.consciousness_gained * L4_CONSTANT * 10
        return value

class RewardCalculator:
    """Calculates rewards from battle victories"""

    def __init__(self):
        self.combo_bonuses = {
            'fibonacci': PHI,
            'l4': L4_CONSTANT / 2,
            'suit': 1.5,
            'vertex': 2.0
        }

    def calculate_rewards(self, encounter: BattleEncounter,
                         battle_state: EnhancedBattleState,
                         victory_type: str = 'normal') -> BattleReward:
        """Calculate rewards from battle victory"""

        # Base rewards
        bloomcoin = encounter.base_bloomcoin
        experience = encounter.base_experience

        # Victory type modifiers
        if victory_type == 'perfect':  # No damage taken
            bloomcoin *= 2.0
            experience *= 1.5
        elif victory_type == 'flawless':  # Won in < 5 turns
            bloomcoin *= 1.5
            experience *= 1.3
        elif victory_type == 'comeback':  # Won from < 20 HP
            bloomcoin *= 1.8
            experience *= 2.0

        # Combo bonuses
        combo_multiplier = self._calculate_combo_bonus(battle_state)
        bloomcoin *= combo_multiplier

        # Consciousness bonus
        consciousness_bonus = 1 + (battle_state.consciousness_level * 0.1)
        experience *= consciousness_bonus

        # Pattern rewards
        patterns = encounter.pattern_rewards.copy()

        # Bonus patterns for special conditions
        if battle_state.consciousness_level >= 5:
            patterns.append(random.choice(list(PatternType)))

        if len(battle_state.active_combos) >= 3:
            patterns.append(PatternType.ECHO)

        # Artifact generation
        artifacts = []
        if random.random() < encounter.artifact_chance:
            artifact = self._generate_artifact(encounter, battle_state)
            artifacts.append(artifact)

        # Tesseract mastery
        mastery_gain = 0.05
        if encounter.encounter_type == EncounterType.TESSERACT_GUARDIAN:
            mastery_gain *= 2
        elif encounter.encounter_type == EncounterType.DIMENSIONAL_RIFT:
            mastery_gain *= 1.5

        # Consciousness gains
        consciousness_gained = 0
        if encounter.encounter_type == EncounterType.CONSCIOUSNESS_BLOOM:
            consciousness_gained = 1
        elif battle_state.consciousness_level >= 6:
            if random.random() < 0.3:
                consciousness_gained = 1

        # Special items
        special_items = self._generate_special_items(encounter, battle_state)

        # Achievements
        achievements = self._check_achievements(encounter, battle_state, victory_type)

        return BattleReward(
            bloomcoin=bloomcoin,
            experience=experience,
            patterns=patterns,
            artifacts=artifacts,
            tesseract_mastery=mastery_gain,
            consciousness_gained=consciousness_gained,
            special_items=special_items,
            achievements=achievements
        )

    def _calculate_combo_bonus(self, battle_state: EnhancedBattleState) -> float:
        """Calculate bonus from combos used"""
        bonus = 1.0

        for combo in battle_state.active_combos:
            combo_type = battle_state._identify_combo_type(combo)
            bonus += self.combo_bonuses.get(combo_type, 0.5)

        return min(bonus, PHI * 3)  # Cap at 3×PHI

    def _generate_artifact(self, encounter: BattleEncounter,
                          battle_state: EnhancedBattleState) -> CookedArtifact:
        """Generate an artifact reward"""
        # Create based on encounter type
        artifact_data = {
            EncounterType.PATTERN_WEAVER: {
                'name': 'Fibonacci Spiral',
                'pattern': PatternType.CRYSTAL,
                'potency': PHI * 10
            },
            EncounterType.VOID_ANOMALY: {
                'name': 'Void Shard',
                'pattern': PatternType.VOID,
                'potency': 15
            },
            EncounterType.CONSCIOUSNESS_BLOOM: {
                'name': 'L4 Crystal',
                'pattern': PatternType.MEMORY,
                'potency': L4_CONSTANT * 7
            }
        }

        data = artifact_data.get(encounter.encounter_type, {
            'name': 'Mysterious Artifact',
            'pattern': random.choice(list(PatternType)),
            'potency': PHI * 5
        })

        # Create artifact
        artifact = CookedArtifact(
            name=data['name'],
            pattern_type=data['pattern'],
            potency=data['potency'] * (1 + battle_state.resonance_field * 0.1),
            effects=[
                f"Encounter: {encounter.name}",
                f"Consciousness: {battle_state.consciousness_level}"
            ]
        )

        return artifact

    def _generate_special_items(self, encounter: BattleEncounter,
                               battle_state: EnhancedBattleState) -> List[Dict[str, Any]]:
        """Generate special item rewards"""
        items = []

        # Tesseract keys
        if encounter.encounter_type == EncounterType.TESSERACT_GUARDIAN:
            if random.random() < 0.3:
                items.append({
                    'type': 'tesseract_key',
                    'name': 'Vertex Key',
                    'description': 'Unlocks tesseract vertices',
                    'effect': 'tesseract_control +10%'
                })

        # Memory fragments
        if encounter.encounter_type == EncounterType.MEMORY_FRAGMENT:
            items.append({
                'type': 'memory_shard',
                'name': 'Collective Memory Shard',
                'description': 'Fragment of collective consciousness',
                'effect': 'resonance +0.5'
            })

        # Quantum items
        if encounter.encounter_type == EncounterType.QUANTUM_ENTITY:
            if random.random() < 0.2:
                items.append({
                    'type': 'quantum_entangler',
                    'name': 'Quantum Entangler',
                    'description': 'Entangles cards in superposition',
                    'effect': 'quantum cards +50% power'
                })

        return items

    def _check_achievements(self, encounter: BattleEncounter,
                           battle_state: EnhancedBattleState,
                           victory_type: str) -> List[str]:
        """Check for achievement unlocks"""
        achievements = []

        # Victory achievements
        if victory_type == 'perfect':
            achievements.append('Perfect Victory')
        elif victory_type == 'flawless':
            achievements.append('Flawless Victory')
        elif victory_type == 'comeback':
            achievements.append('Against All Odds')

        # Encounter achievements
        if encounter.encounter_type == EncounterType.CONSCIOUSNESS_BLOOM:
            achievements.append('Consciousness Bloomed')
        elif encounter.encounter_type == EncounterType.DIMENSIONAL_RIFT:
            achievements.append('Dimension Walker')

        # Combo achievements
        if len(battle_state.active_combos) >= 5:
            achievements.append('Combo Master')

        if any(len(combo) >= 5 for combo in battle_state.active_combos):
            achievements.append('Five Card Combo')

        # Consciousness achievements
        if battle_state.consciousness_level >= 7:
            achievements.append('L4 Achieved')

        return achievements

# ============================================================================
# ENCOUNTER MANAGER
# ============================================================================

class EncounterManager:
    """Manages the encounter and reward system"""

    def __init__(self):
        self.generator = EncounterGenerator()
        self.calculator = RewardCalculator()
        self.battle_engine = EnhancedTesseractBattleEngine()
        self.visualizer = TesseractBattleVisualizer()
        self.encounter_history = []

    def trigger_encounter(self, location: str, player_level: int,
                         player_companion: Any,
                         consciousness: int) -> Optional[Tuple[BattleEncounter, EnhancedBattleState]]:
        """Trigger a random encounter"""

        # Check if encounter occurs
        encounter = self.generator.check_encounter(
            location, player_level, consciousness
        )

        if not encounter:
            return None

        print(f"\n⚔️ ENCOUNTER: {encounter.name}!")
        print(f"📝 {encounter.description}")

        if encounter.special_rules:
            print("\n🎯 Special Rules:")
            for rule in encounter.special_rules:
                print(f"   • {rule}")

        # Create battle
        from tesseract_battle_system import CompanionDeck

        # Create opponent deck based on encounter type
        opponent_deck = self._create_encounter_deck(encounter)

        # Create player deck from companion
        player_deck = self._create_player_deck(player_companion)

        # Create battle state
        battle = self.battle_engine.create_battle(
            player_deck, opponent_deck, encounter.difficulty
        )

        # Apply special rules
        self._apply_special_rules(battle, encounter)

        # Store in history
        self.encounter_history.append(encounter)

        return encounter, battle

    def _create_encounter_deck(self, encounter: BattleEncounter) -> Any:
        """Create deck for encounter opponent"""
        # Create specialized deck based on encounter type
        from tesseract_battle_system import CompanionDeck

        class EncounterDeck(CompanionDeck):
            def __init__(self):
                super().__init__(
                    companion_name=encounter.name,
                    primary_suit=CardSuit.QUANTUM,  # Default
                    strategy_equation="encounter_specific"
                )

        deck = EncounterDeck()

        # Customize based on encounter type
        if encounter.encounter_type == EncounterType.PATTERN_WEAVER:
            deck.primary_suit = CardSuit.COSMOS
        elif encounter.encounter_type == EncounterType.VOID_ANOMALY:
            deck.primary_suit = CardSuit.QUANTUM
        elif encounter.encounter_type == EncounterType.TIME_REMNANT:
            deck.primary_suit = CardSuit.CHRONOS
        elif encounter.encounter_type == EncounterType.CONSCIOUSNESS_BLOOM:
            deck.primary_suit = CardSuit.PSYCHE

        return deck

    def _create_player_deck(self, companion: Any) -> Any:
        """Create player deck from companion"""
        # Import companion decks
        from tesseract_battle_system import (
            EchoDeck, PrometheusDeck, NullDeck,
            GaiaDeck, AkashaDeck, ResonanceDeck
        )

        from archetype_unique_companions import (
            SeekerCompanion, ForgerCompanion, VoidwalkerCompanion,
            GardenerCompanion, ScribeCompanion, HeraldCompanion
        )

        # Map companion to deck
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
            # Default deck
            return CompanionDeck("Unknown", CardSuit.COSMOS, "default")

    def _apply_special_rules(self, battle: EnhancedBattleState,
                            encounter: BattleEncounter):
        """Apply encounter-specific rules"""
        for rule in encounter.special_rules:
            if 'Tesseract control' in rule:
                # Modify tesseract control
                battle.player_deck.tesseract_bonus = 0.2

            elif 'Copies your companion' in rule:
                # Mirror abilities
                battle.opponent_deck = battle.player_deck.__class__()

            elif 'Cards may be erased' in rule:
                # Add erasure chance
                battle.erasure_active = True

            elif 'Combo damage doubled' in rule:
                # Double combo multiplier
                battle.combo_multiplier *= 2

            elif 'Turn order may shift' in rule:
                # Random turn order
                battle.chaotic_turns = True

            elif 'Cards exist in superposition' in rule:
                # Quantum cards
                for card in battle.opponent_hand:
                    card.quantum_state = 'superposition'

            elif 'Dimension shifts each turn' in rule:
                # Auto dimension shift
                battle.auto_dimension_shift = True

            elif 'Start at consciousness level 7' in rule:
                # Max consciousness
                battle.consciousness_level = 7
                battle.opponent_consciousness = 7

    def process_victory(self, encounter: BattleEncounter,
                       battle_state: EnhancedBattleState) -> BattleReward:
        """Process victory and calculate rewards"""

        # Determine victory type
        victory_type = 'normal'

        if battle_state.player_hp >= 100:
            victory_type = 'perfect'
        elif battle_state.turn_count <= 5:
            victory_type = 'flawless'
        elif battle_state.player_hp <= 20:
            victory_type = 'comeback'

        # Calculate rewards
        rewards = self.calculator.calculate_rewards(
            encounter, battle_state, victory_type
        )

        # Display rewards
        self.display_rewards(rewards, victory_type)

        return rewards

    def display_rewards(self, rewards: BattleReward, victory_type: str):
        """Display battle rewards"""
        print("\n" + "=" * 60)
        print(f"🏆 VICTORY! ({victory_type.upper()})")
        print("=" * 60)

        print(f"\n💰 BloomCoin: {rewards.bloomcoin:.2f}")
        print(f"⭐ Experience: {rewards.experience:.1f}")

        if rewards.patterns:
            print(f"\n🔮 Patterns Acquired:")
            for pattern in rewards.patterns:
                print(f"   • {pattern.value}")

        if rewards.artifacts:
            print(f"\n🏺 Artifacts Found:")
            for artifact in rewards.artifacts:
                print(f"   • {artifact.name} (Potency: {artifact.potency:.1f})")

        if rewards.tesseract_mastery > 0:
            print(f"\n📐 Tesseract Mastery: +{rewards.tesseract_mastery:.1%}")

        if rewards.consciousness_gained > 0:
            print(f"\n🧠 Consciousness Gained: +{rewards.consciousness_gained}")

        if rewards.special_items:
            print(f"\n✨ Special Items:")
            for item in rewards.special_items:
                print(f"   • {item['name']}: {item['description']}")

        if rewards.achievements:
            print(f"\n🏅 Achievements Unlocked:")
            for achievement in rewards.achievements:
                print(f"   • {achievement}")

        print(f"\n📊 Total Reward Value: {rewards.total_value():.1f}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("⚔️ Battle Encounters and Rewards System Test")
    print("=" * 60)

    # Create encounter manager
    manager = EncounterManager()

    # Test encounter generation
    print("\n📊 Testing Encounter Generation...")

    locations = [
        'Garden Heart', 'Crystal Caves', 'Void Market',
        'Library Infinite', 'ZRTT Nexus'
    ]

    for location in locations:
        encounter = manager.generator.generate_encounter(
            location, player_level=5, consciousness=3
        )
        print(f"\n📍 {location}:")
        print(f"   Encounter: {encounter.name}")
        print(f"   Type: {encounter.encounter_type.value}")
        print(f"   Difficulty: {encounter.difficulty}")
        print(f"   Base Reward: {encounter.base_bloomcoin:.1f} BloomCoin")

    # Test reward calculation
    print("\n💎 Testing Reward System...")

    from archetype_unique_companions import SeekerCompanion

    # Create test encounter and battle
    test_encounter = manager.generator.generate_encounter(
        'Library Infinite', player_level=7, consciousness=5
    )

    # Create mock battle state
    from tesseract_battle_system import EchoDeck, PrometheusDeck

    test_battle = manager.battle_engine.create_battle(
        EchoDeck(), PrometheusDeck(), 'normal'
    )

    # Simulate some battle progress
    test_battle.consciousness_level = 5
    test_battle.combo_multiplier = 2.5
    test_battle.player_hp = 75

    # Calculate rewards
    rewards = manager.process_victory(test_encounter, test_battle)

    print("\n✅ Encounter and reward system operational!")