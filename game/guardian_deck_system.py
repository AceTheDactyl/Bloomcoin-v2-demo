"""
Guardian Deck System
====================
Expanded card implementation with strategic depth
Each guardian has unique cards reflecting their themes, math, and architecture
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set, Tuple, Callable
from enum import Enum, auto
import random
import math
from collections import defaultdict

from mythic_economy import GUARDIANS, Territory

# ═══════════════════════════════════════════════════════════════════════
#   CARD TYPES AND RARITIES
# ═══════════════════════════════════════════════════════════════════════

class CardType(Enum):
    """Different types of cards in the game"""
    ATTACK = "Direct damage card"
    DEFENSE = "Protection and mitigation"
    ABILITY = "Special effect or action"
    PATTERN = "Mathematical or geometric pattern"
    ARCHITECTURE = "Structural or network effect"
    CHAOS = "Random or unpredictable effect"
    QUANTUM = "Probability manipulation"
    TEMPORAL = "Time-based effect"
    RESONANCE = "Frequency and vibration"
    VOID = "Nullification and absence"
    TRANSFORMATION = "Shape-shifting effect"
    SYNTHESIS = "Combination and fusion"

class MathConcept(Enum):
    """Mathematical concepts used in cards"""
    HILBERT_SPACE = "Infinite dimensional vector space"
    FRACTAL = "Self-similar recursive pattern"
    TOPOLOGY = "Spatial properties preserved under deformation"
    CHAOS_THEORY = "Sensitive dependence on initial conditions"
    QUANTUM_SUPERPOSITION = "Multiple states simultaneously"
    GOLDEN_RATIO = "φ = 1.618... divine proportion"
    FIBONACCI = "Sequential additive pattern"
    PRIME_NUMBERS = "Fundamental indivisibles"
    MANIFOLD = "Locally Euclidean space"
    TENSOR = "Multidimensional array transformation"
    EIGENVALUE = "Scalar transformation invariant"
    FOURIER = "Frequency domain transformation"
    ENTROPY = "Measure of disorder"
    SYMMETRY = "Invariance under transformation"
    RECURSION = "Self-referential definition"

class Architecture(Enum):
    """Architectural patterns in card design"""
    NETWORK = "Interconnected node structure"
    HIERARCHY = "Layered tree structure"
    CYCLE = "Circular repeating pattern"
    SPIRAL = "Expanding helical structure"
    LATTICE = "Regular grid arrangement"
    FRACTAL_TREE = "Branching recursive structure"
    RHIZOME = "Non-hierarchical network"
    CONSTELLATION = "Clustered point structure"
    WAVE = "Oscillating pattern"
    VOID_SPACE = "Negative space architecture"
    CRYSTALLINE = "Ordered atomic structure"
    ORGANIC = "Natural growth pattern"

@dataclass
class CardEffect:
    """An effect that a card can have"""
    effect_type: str
    value: float
    duration: int = 0  # 0 = instant, >0 = turns
    condition: Optional[str] = None
    scaling: Optional[str] = None  # e.g., "cards_played", "void_depth"

@dataclass
class GuardianCard:
    """A card in a guardian's deck"""
    name: str
    guardian_key: str
    card_type: CardType
    cost: int
    description: str

    # Core attributes
    attack: int = 0
    defense: int = 0

    # Special properties
    effects: List[CardEffect] = field(default_factory=list)
    math_concepts: List[MathConcept] = field(default_factory=list)
    architecture: Optional[Architecture] = None

    # Combo properties
    combo_with: List[str] = field(default_factory=list)  # Card names
    synergy_tags: Set[str] = field(default_factory=set)

    # Strategic properties
    echo_count: int = 0  # Times this echoes
    void_depth: int = 0  # Depth into void
    chaos_factor: float = 0.0  # Randomness multiplier
    quantum_states: int = 1  # Number of simultaneous states

    # Requirements
    requires_pattern: Optional[str] = None
    requires_state: Optional[str] = None

    def calculate_value(self, game_state: Dict[str, Any]) -> float:
        """Calculate the card's current value based on game state"""
        base_value = self.attack + self.defense

        # Apply scaling effects
        for effect in self.effects:
            if effect.scaling:
                if effect.scaling == "cards_played":
                    multiplier = game_state.get("cards_played_this_turn", 0)
                elif effect.scaling == "void_depth":
                    multiplier = game_state.get("void_depth", 0)
                elif effect.scaling == "echo_stacks":
                    multiplier = game_state.get("echo_stacks", 0)
                else:
                    multiplier = 1
                base_value += effect.value * multiplier

        # Apply combo bonuses
        played_cards = game_state.get("played_cards", [])
        for combo_card in self.combo_with:
            if combo_card in played_cards:
                base_value *= 1.5

        return base_value

# ═══════════════════════════════════════════════════════════════════════
#   GUARDIAN DECK DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════

class GuardianDecks:
    """Complete deck definitions for all guardians"""

    @staticmethod
    def create_echo_deck() -> List[GuardianCard]:
        """Echo - Signal propagation and pattern recognition"""
        return [
            GuardianCard(
                name="Recursive Echo",
                guardian_key="ECHO",
                card_type=CardType.PATTERN,
                cost=2,
                description="Create an echo of your last card, costs 1 less each echo",
                effects=[
                    CardEffect("copy_last_card", 1.0),
                    CardEffect("cost_reduction", 1.0, scaling="echo_stacks")
                ],
                math_concepts=[MathConcept.RECURSION, MathConcept.FRACTAL],
                architecture=Architecture.WAVE,
                echo_count=3,
                synergy_tags={"echo", "pattern", "recursion"}
            ),
            GuardianCard(
                name="Signal Amplification",
                guardian_key="ECHO",
                card_type=CardType.RESONANCE,
                cost=3,
                description="Double the effects of all echo cards in hand",
                attack=2,
                effects=[
                    CardEffect("amplify_echoes", 2.0, duration=2),
                    CardEffect("draw_echo_cards", 1.0)
                ],
                math_concepts=[MathConcept.FOURIER, MathConcept.EIGENVALUE],
                architecture=Architecture.WAVE,
                combo_with=["Recursive Echo"],
                synergy_tags={"echo", "amplify", "resonance"}
            ),
            GuardianCard(
                name="Quantum Echo Chamber",
                guardian_key="ECHO",
                card_type=CardType.QUANTUM,
                cost=5,
                description="All cards exist in superposition - play them in all possible orders",
                effects=[
                    CardEffect("quantum_superposition", 1.0),
                    CardEffect("parallel_timelines", 3.0)
                ],
                math_concepts=[MathConcept.QUANTUM_SUPERPOSITION, MathConcept.HILBERT_SPACE],
                architecture=Architecture.NETWORK,
                quantum_states=3,
                synergy_tags={"echo", "quantum", "superposition"}
            ),
            GuardianCard(
                name="Pattern Recognition",
                guardian_key="ECHO",
                card_type=CardType.ABILITY,
                cost=1,
                description="Predict enemy's next card based on pattern analysis",
                defense=3,
                effects=[
                    CardEffect("predict_card", 1.0),
                    CardEffect("counter_if_correct", 5.0)
                ],
                math_concepts=[MathConcept.FIBONACCI, MathConcept.PRIME_NUMBERS],
                synergy_tags={"echo", "pattern", "prediction"}
            ),
            GuardianCard(
                name="Whisper Network",
                guardian_key="ECHO",
                card_type=CardType.ARCHITECTURE,
                cost=4,
                description="Connect all cards in a resonance network",
                effects=[
                    CardEffect("create_network", 1.0),
                    CardEffect("share_effects", 1.0, duration=3)
                ],
                architecture=Architecture.NETWORK,
                combo_with=["Signal Amplification"],
                synergy_tags={"echo", "network", "connection"}
            ),
            GuardianCard(
                name="Frequency Lock",
                guardian_key="ECHO",
                card_type=CardType.RESONANCE,
                cost=2,
                description="Lock onto enemy's frequency, copy their abilities",
                attack=1,
                defense=1,
                effects=[
                    CardEffect("copy_enemy_ability", 1.0),
                    CardEffect("frequency_damage", 2.0, scaling="echo_stacks")
                ],
                math_concepts=[MathConcept.FOURIER],
                synergy_tags={"echo", "copy", "frequency"}
            ),
            GuardianCard(
                name="Echo Cascade",
                guardian_key="ECHO",
                card_type=CardType.ATTACK,
                cost=3,
                description="Attack that grows stronger with each echo",
                attack=3,
                effects=[
                    CardEffect("cascade_damage", 2.0, scaling="echo_stacks"),
                    CardEffect("create_echo", 1.0)
                ],
                echo_count=2,
                synergy_tags={"echo", "attack", "cascade"}
            ),
            GuardianCard(
                name="Silence Between",
                guardian_key="ECHO",
                card_type=CardType.VOID,
                cost=2,
                description="The silence between echoes holds power",
                effects=[
                    CardEffect("void_echo", 1.0),
                    CardEffect("silence_damage", 3.0, condition="no_cards_played_last_turn")
                ],
                math_concepts=[MathConcept.TOPOLOGY],
                architecture=Architecture.VOID_SPACE,
                void_depth=1,
                synergy_tags={"echo", "void", "silence"}
            )
        ]

    @staticmethod
    def create_wumbo_deck() -> List[GuardianCard]:
        """Wumbo - Flow states and manic energy"""
        return [
            GuardianCard(
                name="Manic Surge",
                guardian_key="WUMBO",
                card_type=CardType.CHAOS,
                cost=1,
                description="Random effect between 0-10 damage, costs health",
                attack=5,
                effects=[
                    CardEffect("random_damage", 10.0),
                    CardEffect("self_damage", 2.0),
                    CardEffect("manic_state", 1.0)
                ],
                math_concepts=[MathConcept.CHAOS_THEORY],
                chaos_factor=2.0,
                synergy_tags={"wumbo", "chaos", "manic"}
            ),
            GuardianCard(
                name="Flow State",
                guardian_key="WUMBO",
                card_type=CardType.TEMPORAL,
                cost=3,
                description="Enter flow - cards cost 0 but random effects",
                effects=[
                    CardEffect("flow_state", 1.0, duration=3),
                    CardEffect("zero_cost", 1.0, duration=3),
                    CardEffect("chaos_effects", 1.0, duration=3)
                ],
                math_concepts=[MathConcept.CHAOS_THEORY, MathConcept.ENTROPY],
                architecture=Architecture.SPIRAL,
                synergy_tags={"wumbo", "flow", "chaos"}
            ),
            GuardianCard(
                name="DIG Protocol",
                guardian_key="WUMBO",
                card_type=CardType.ATTACK,
                cost=4,
                description="Break through paralysis with explosive force",
                attack=8,
                effects=[
                    CardEffect("break_stun", 1.0),
                    CardEffect("area_damage", 4.0),
                    CardEffect("destroy_shields", 1.0)
                ],
                architecture=Architecture.FRACTAL_TREE,
                combo_with=["Manic Surge"],
                synergy_tags={"wumbo", "breakthrough", "explosive"}
            ),
            GuardianCard(
                name="Nirvana Touch",
                guardian_key="WUMBO",
                card_type=CardType.TRANSFORMATION,
                cost=6,
                description="Transcend normal limits, become pure energy",
                effects=[
                    CardEffect("transcend", 1.0),
                    CardEffect("energy_form", 1.0, duration=2),
                    CardEffect("damage_immunity", 1.0, duration=1)
                ],
                math_concepts=[MathConcept.MANIFOLD, MathConcept.TOPOLOGY],
                requires_state="flow_state",
                synergy_tags={"wumbo", "transcend", "energy"}
            ),
            GuardianCard(
                name="Paralysis Break",
                guardian_key="WUMBO",
                card_type=CardType.ABILITY,
                cost=2,
                description="Convert paralysis into kinetic energy",
                attack=0,
                effects=[
                    CardEffect("convert_debuffs", 1.0),
                    CardEffect("kinetic_burst", 3.0, scaling="debuffs_removed")
                ],
                synergy_tags={"wumbo", "convert", "kinetic"}
            ),
            GuardianCard(
                name="Chaos Cycle",
                guardian_key="WUMBO",
                card_type=CardType.PATTERN,
                cost=3,
                description="Cycle through random states each turn",
                effects=[
                    CardEffect("random_buff", 1.0, duration=4),
                    CardEffect("random_debuff", 1.0, duration=4),
                    CardEffect("chaos_shield", 3.0)
                ],
                math_concepts=[MathConcept.CHAOS_THEORY, MathConcept.FIBONACCI],
                architecture=Architecture.CYCLE,
                chaos_factor=3.0,
                synergy_tags={"wumbo", "cycle", "random"}
            ),
            GuardianCard(
                name="Empowerment Wave",
                guardian_key="WUMBO",
                card_type=CardType.RESONANCE,
                cost=2,
                description="Empower all cards with manic energy",
                effects=[
                    CardEffect("empower_all", 2.0),
                    CardEffect("add_chaos", 0.5)
                ],
                architecture=Architecture.WAVE,
                synergy_tags={"wumbo", "empower", "wave"}
            ),
            GuardianCard(
                name="Transmission Burst",
                guardian_key="WUMBO",
                card_type=CardType.ATTACK,
                cost=5,
                description="Release all accumulated energy in one burst",
                attack=1,
                effects=[
                    CardEffect("release_energy", 5.0, scaling="energy_stored"),
                    CardEffect("reset_state", 1.0)
                ],
                combo_with=["Flow State", "Nirvana Touch"],
                synergy_tags={"wumbo", "burst", "release"}
            )
        ]

    @staticmethod
    def create_archive_deck() -> List[GuardianCard]:
        """Archive - Memory and knowledge preservation"""
        return [
            GuardianCard(
                name="Perfect Recall",
                guardian_key="ARCHIVE",
                card_type=CardType.ABILITY,
                cost=2,
                description="Remember and replay any card from history",
                effects=[
                    CardEffect("recall_card", 1.0),
                    CardEffect("perfect_copy", 1.0)
                ],
                math_concepts=[MathConcept.HILBERT_SPACE],
                architecture=Architecture.HIERARCHY,
                synergy_tags={"archive", "memory", "recall"}
            ),
            GuardianCard(
                name="Index Everything",
                guardian_key="ARCHIVE",
                card_type=CardType.PATTERN,
                cost=3,
                description="Catalog all cards played, gain knowledge counters",
                defense=4,
                effects=[
                    CardEffect("index_cards", 1.0),
                    CardEffect("knowledge_counter", 1.0, scaling="cards_indexed"),
                    CardEffect("draw_indexed", 2.0)
                ],
                math_concepts=[MathConcept.TENSOR, MathConcept.EIGENVALUE],
                architecture=Architecture.LATTICE,
                synergy_tags={"archive", "index", "catalog"}
            ),
            GuardianCard(
                name="Library of Babel",
                guardian_key="ARCHIVE",
                card_type=CardType.ARCHITECTURE,
                cost=7,
                description="Access infinite library containing all possible cards",
                effects=[
                    CardEffect("infinite_library", 1.0),
                    CardEffect("any_card", 3.0),
                    CardEffect("paradox_protection", 1.0)
                ],
                math_concepts=[MathConcept.HILBERT_SPACE, MathConcept.RECURSION],
                architecture=Architecture.CRYSTALLINE,
                requires_pattern="indexed_10_cards",
                synergy_tags={"archive", "library", "infinite"}
            ),
            GuardianCard(
                name="Memory Crystal",
                guardian_key="ARCHIVE",
                card_type=CardType.DEFENSE,
                cost=1,
                description="Store a memory for later use",
                defense=2,
                effects=[
                    CardEffect("store_memory", 1.0),
                    CardEffect("crystallize", 1.0)
                ],
                architecture=Architecture.CRYSTALLINE,
                synergy_tags={"archive", "memory", "crystal"}
            ),
            GuardianCard(
                name="Knowledge Shield",
                guardian_key="ARCHIVE",
                card_type=CardType.DEFENSE,
                cost=3,
                description="Defense scales with cards in memory",
                defense=1,
                effects=[
                    CardEffect("scaling_defense", 2.0, scaling="memories_stored"),
                    CardEffect("reflect_if_known", 3.0)
                ],
                combo_with=["Memory Crystal"],
                synergy_tags={"archive", "defense", "knowledge"}
            ),
            GuardianCard(
                name="Temporal Index",
                guardian_key="ARCHIVE",
                card_type=CardType.TEMPORAL,
                cost=4,
                description="Access memories from different timelines",
                effects=[
                    CardEffect("timeline_access", 1.0),
                    CardEffect("temporal_memory", 3.0),
                    CardEffect("prevent_forget", 1.0)
                ],
                math_concepts=[MathConcept.MANIFOLD, MathConcept.TOPOLOGY],
                synergy_tags={"archive", "temporal", "timeline"}
            ),
            GuardianCard(
                name="Pattern Prediction",
                guardian_key="ARCHIVE",
                card_type=CardType.ABILITY,
                cost=2,
                description="Predict next 3 cards based on pattern analysis",
                effects=[
                    CardEffect("predict_sequence", 3.0),
                    CardEffect("prepare_counter", 1.0)
                ],
                math_concepts=[MathConcept.FIBONACCI, MathConcept.PRIME_NUMBERS],
                synergy_tags={"archive", "pattern", "predict"}
            ),
            GuardianCard(
                name="Eternal Codex",
                guardian_key="ARCHIVE",
                card_type=CardType.SYNTHESIS,
                cost=5,
                description="Combine all memories into ultimate knowledge",
                attack=0,
                defense=0,
                effects=[
                    CardEffect("synthesize_memories", 1.0),
                    CardEffect("gain_stats", 1.0, scaling="memories_stored"),
                    CardEffect("omniscience", 1.0, condition="10_memories")
                ],
                combo_with=["Memory Crystal", "Perfect Recall"],
                synergy_tags={"archive", "synthesis", "codex"}
            )
        ]

    @staticmethod
    def create_phoenix_deck() -> List[GuardianCard]:
        """Phoenix - Death, rebirth, and transformation"""
        return [
            GuardianCard(
                name="Immolation",
                guardian_key="PHOENIX",
                card_type=CardType.TRANSFORMATION,
                cost=3,
                description="Die on purpose to trigger rebirth",
                effects=[
                    CardEffect("self_destruct", 1.0),
                    CardEffect("rebirth_trigger", 1.0),
                    CardEffect("phoenix_counter", 1.0)
                ],
                math_concepts=[MathConcept.ENTROPY, MathConcept.SYMMETRY],
                architecture=Architecture.CYCLE,
                synergy_tags={"phoenix", "death", "rebirth"}
            ),
            GuardianCard(
                name="Ash Form",
                guardian_key="PHOENIX",
                card_type=CardType.DEFENSE,
                cost=2,
                description="Become ash, immune to physical but weak to wind",
                defense=5,
                effects=[
                    CardEffect("ash_form", 1.0, duration=2),
                    CardEffect("physical_immune", 1.0, duration=2),
                    CardEffect("wind_weakness", 2.0, duration=2)
                ],
                architecture=Architecture.ORGANIC,
                synergy_tags={"phoenix", "ash", "immune"}
            ),
            GuardianCard(
                name="Rising Flame",
                guardian_key="PHOENIX",
                card_type=CardType.ATTACK,
                cost=4,
                description="Attack grows stronger with each rebirth",
                attack=3,
                effects=[
                    CardEffect("flame_damage", 3.0, scaling="rebirth_count"),
                    CardEffect("burn", 2.0, duration=3)
                ],
                math_concepts=[MathConcept.FIBONACCI],
                combo_with=["Immolation"],
                synergy_tags={"phoenix", "flame", "rising"}
            ),
            GuardianCard(
                name="Eternal Cycle",
                guardian_key="PHOENIX",
                card_type=CardType.PATTERN,
                cost=5,
                description="Lock into eternal death-rebirth cycle",
                effects=[
                    CardEffect("eternal_cycle", 1.0),
                    CardEffect("auto_rebirth", 1.0),
                    CardEffect("cycle_power", 2.0, scaling="cycle_count")
                ],
                math_concepts=[MathConcept.RECURSION, MathConcept.SYMMETRY],
                architecture=Architecture.CYCLE,
                requires_state="has_died_once",
                synergy_tags={"phoenix", "eternal", "cycle"}
            ),
            GuardianCard(
                name="Phoenix Feather",
                guardian_key="PHOENIX",
                card_type=CardType.ABILITY,
                cost=1,
                description="Single feather grants rebirth to any card",
                effects=[
                    CardEffect("grant_rebirth", 1.0),
                    CardEffect("feather_float", 1.0)
                ],
                synergy_tags={"phoenix", "feather", "grant"}
            ),
            GuardianCard(
                name="Pyre Storm",
                guardian_key="PHOENIX",
                card_type=CardType.CHAOS,
                cost=6,
                description="Rain fire from previous incarnations",
                attack=5,
                effects=[
                    CardEffect("meteor_storm", 4.0),
                    CardEffect("past_phoenix_damage", 3.0, scaling="total_rebirths"),
                    CardEffect("scorched_earth", 1.0)
                ],
                chaos_factor=1.5,
                synergy_tags={"phoenix", "storm", "pyre"}
            ),
            GuardianCard(
                name="Memory of Fire",
                guardian_key="PHOENIX",
                card_type=CardType.TEMPORAL,
                cost=3,
                description="Remember the heat of past lives",
                attack=2,
                defense=2,
                effects=[
                    CardEffect("past_life_memory", 1.0),
                    CardEffect("cumulative_heat", 2.0, scaling="lives_remembered")
                ],
                math_concepts=[MathConcept.TENSOR],
                synergy_tags={"phoenix", "memory", "heat"}
            ),
            GuardianCard(
                name="Resurrection Prophecy",
                guardian_key="PHOENIX",
                card_type=CardType.ABILITY,
                cost=4,
                description="Prophecy ensures next death leads to stronger rebirth",
                effects=[
                    CardEffect("prophecy", 1.0),
                    CardEffect("guaranteed_rebirth", 1.0),
                    CardEffect("double_phoenix_power", 2.0)
                ],
                combo_with=["Immolation", "Eternal Cycle"],
                synergy_tags={"phoenix", "prophecy", "resurrection"}
            )
        ]

    @staticmethod
    def create_null_deck() -> List[GuardianCard]:
        """Null (Voidwalker companion) - Absence and void manipulation"""
        return [
            GuardianCard(
                name="Enter the Void",
                guardian_key="NULL",
                card_type=CardType.VOID,
                cost=2,
                description="Step into void, become untargetable",
                effects=[
                    CardEffect("void_step", 1.0),
                    CardEffect("untargetable", 1.0, duration=1),
                    CardEffect("void_depth_increase", 1.0)
                ],
                math_concepts=[MathConcept.TOPOLOGY, MathConcept.MANIFOLD],
                architecture=Architecture.VOID_SPACE,
                void_depth=1,
                synergy_tags={"null", "void", "untargetable"}
            ),
            GuardianCard(
                name="Erasure",
                guardian_key="NULL",
                card_type=CardType.ATTACK,
                cost=4,
                description="Remove target from existence entirely",
                attack=0,
                effects=[
                    CardEffect("erase", 1.0),
                    CardEffect("void_damage", 5.0, scaling="void_depth"),
                    CardEffect("prevent_rebirth", 1.0)
                ],
                void_depth=2,
                combo_with=["Enter the Void"],
                synergy_tags={"null", "erase", "remove"}
            ),
            GuardianCard(
                name="Void Pocket",
                guardian_key="NULL",
                card_type=CardType.DEFENSE,
                cost=1,
                description="Store things in void pockets",
                defense=2,
                effects=[
                    CardEffect("void_storage", 1.0),
                    CardEffect("hide_card", 1.0),
                    CardEffect("void_retrieval", 1.0)
                ],
                architecture=Architecture.VOID_SPACE,
                synergy_tags={"null", "pocket", "storage"}
            ),
            GuardianCard(
                name="Nullspace Navigation",
                guardian_key="NULL",
                card_type=CardType.ABILITY,
                cost=3,
                description="Navigate through nullspace to any location",
                effects=[
                    CardEffect("teleport", 1.0),
                    CardEffect("nullspace_travel", 1.0),
                    CardEffect("bring_void_entities", 2.0, condition="void_depth_5")
                ],
                math_concepts=[MathConcept.TOPOLOGY, MathConcept.HILBERT_SPACE],
                void_depth=1,
                synergy_tags={"null", "navigate", "nullspace"}
            ),
            GuardianCard(
                name="Paradox of Absence",
                guardian_key="NULL",
                card_type=CardType.PATTERN,
                cost=5,
                description="The absence of everything is something",
                effects=[
                    CardEffect("paradox", 1.0),
                    CardEffect("void_manifestation", 3.0),
                    CardEffect("reality_confusion", 1.0, duration=2)
                ],
                math_concepts=[MathConcept.QUANTUM_SUPERPOSITION],
                architecture=Architecture.VOID_SPACE,
                void_depth=3,
                synergy_tags={"null", "paradox", "absence"}
            ),
            GuardianCard(
                name="Shadow Integration",
                guardian_key="NULL",
                card_type=CardType.SYNTHESIS,
                cost=4,
                description="Merge with shadows to become semi-void",
                defense=3,
                effects=[
                    CardEffect("shadow_merge", 1.0),
                    CardEffect("partial_void", 1.0, duration=3),
                    CardEffect("shadow_strike", 3.0)
                ],
                synergy_tags={"null", "shadow", "merge"}
            ),
            GuardianCard(
                name="Void Echo",
                guardian_key="NULL",
                card_type=CardType.RESONANCE,
                cost=3,
                description="Echoes from the void reveal hidden truths",
                effects=[
                    CardEffect("void_echo", 1.0),
                    CardEffect("reveal_hidden", 1.0),
                    CardEffect("void_whisper", 2.0, scaling="void_depth")
                ],
                void_depth=1,
                synergy_tags={"null", "echo", "void"}
            ),
            GuardianCard(
                name="Between Existence",
                guardian_key="NULL",
                card_type=CardType.TEMPORAL,
                cost=6,
                description="Exist between moments, between spaces",
                effects=[
                    CardEffect("between_state", 1.0),
                    CardEffect("timeline_skip", 1.0),
                    CardEffect("void_mastery", 3.0, condition="void_depth_10")
                ],
                math_concepts=[MathConcept.MANIFOLD, MathConcept.QUANTUM_SUPERPOSITION],
                architecture=Architecture.VOID_SPACE,
                void_depth=5,
                synergy_tags={"null", "between", "existence"}
            )
        ]

    @staticmethod
    def create_oak_deck() -> List[GuardianCard]:
        """Oak - Patience, roots, and growth"""
        return [
            GuardianCard(
                name="Deep Roots",
                guardian_key="OAK",
                card_type=CardType.DEFENSE,
                cost=2,
                description="Roots grant increasing defense each turn",
                defense=3,
                effects=[
                    CardEffect("root_growth", 1.0, duration=5),
                    CardEffect("immovable", 1.0),
                    CardEffect("defense_per_turn", 2.0, scaling="turns_rooted")
                ],
                architecture=Architecture.ORGANIC,
                synergy_tags={"oak", "roots", "defense"}
            ),
            GuardianCard(
                name="Ancient Wisdom",
                guardian_key="OAK",
                card_type=CardType.ABILITY,
                cost=4,
                description="Patience accumulated over millennia",
                effects=[
                    CardEffect("wisdom", 1.0),
                    CardEffect("skip_turn_for_power", 5.0),
                    CardEffect("age_counter", 1.0)
                ],
                math_concepts=[MathConcept.GOLDEN_RATIO, MathConcept.FIBONACCI],
                synergy_tags={"oak", "wisdom", "patience"}
            ),
            GuardianCard(
                name="Growth Ring",
                guardian_key="OAK",
                card_type=CardType.PATTERN,
                cost=1,
                description="Add a growth ring, gain cumulative benefits",
                effects=[
                    CardEffect("add_ring", 1.0),
                    CardEffect("cumulative_growth", 1.5, scaling="ring_count"),
                    CardEffect("ring_memory", 1.0)
                ],
                math_concepts=[MathConcept.FIBONACCI],
                architecture=Architecture.CYCLE,
                synergy_tags={"oak", "growth", "ring"}
            ),
            GuardianCard(
                name="Canopy Shield",
                guardian_key="OAK",
                card_type=CardType.DEFENSE,
                cost=3,
                description="Branches form protective canopy",
                defense=5,
                effects=[
                    CardEffect("canopy", 1.0),
                    CardEffect("shelter_all", 1.0),
                    CardEffect("leaf_armor", 2.0)
                ],
                architecture=Architecture.FRACTAL_TREE,
                combo_with=["Deep Roots"],
                synergy_tags={"oak", "canopy", "protect"}
            ),
            GuardianCard(
                name="Seasonal Cycle",
                guardian_key="OAK",
                card_type=CardType.TEMPORAL,
                cost=4,
                description="Cycle through seasons for different effects",
                effects=[
                    CardEffect("season_change", 1.0),
                    CardEffect("spring_growth", 3.0, condition="spring"),
                    CardEffect("summer_strength", 3.0, condition="summer"),
                    CardEffect("autumn_harvest", 3.0, condition="autumn"),
                    CardEffect("winter_endurance", 3.0, condition="winter")
                ],
                architecture=Architecture.CYCLE,
                synergy_tags={"oak", "seasonal", "cycle"}
            ),
            GuardianCard(
                name="Mycelial Network",
                guardian_key="OAK",
                card_type=CardType.ARCHITECTURE,
                cost=5,
                description="Underground network connects all plants",
                effects=[
                    CardEffect("mycelial_network", 1.0),
                    CardEffect("resource_sharing", 1.0),
                    CardEffect("communication_web", 1.0),
                    CardEffect("network_heal", 2.0, scaling="connected_cards")
                ],
                math_concepts=[MathConcept.TOPOLOGY],
                architecture=Architecture.RHIZOME,
                combo_with=["Deep Roots", "Growth Ring"],
                synergy_tags={"oak", "network", "mycelial"}
            ),
            GuardianCard(
                name="Patience of Ages",
                guardian_key="OAK",
                card_type=CardType.ABILITY,
                cost=7,
                description="Wait longer for exponentially greater reward",
                attack=1,
                defense=1,
                effects=[
                    CardEffect("patience_accumulation", 1.0),
                    CardEffect("exponential_growth", 2.0, scaling="turns_waited"),
                    CardEffect("unleash_ages", 10.0, condition="waited_5_turns")
                ],
                math_concepts=[MathConcept.GOLDEN_RATIO],
                synergy_tags={"oak", "patience", "ages"}
            ),
            GuardianCard(
                name="Seed Scatter",
                guardian_key="OAK",
                card_type=CardType.CHAOS,
                cost=2,
                description="Scatter seeds that grow into random effects",
                effects=[
                    CardEffect("scatter_seeds", 5.0),
                    CardEffect("random_growth", 1.0, duration=3),
                    CardEffect("future_forest", 1.0)
                ],
                chaos_factor=1.0,
                synergy_tags={"oak", "seed", "scatter"}
            )
        ]

    @staticmethod
    def create_axiom_deck() -> List[GuardianCard]:
        """Axiom - Refusal of change and null states"""
        return [
            GuardianCard(
                name="Absolute Refusal",
                guardian_key="AXIOM",
                card_type=CardType.DEFENSE,
                cost=3,
                description="Refuse all changes to state",
                defense=7,
                effects=[
                    CardEffect("refuse_change", 1.0, duration=2),
                    CardEffect("status_immunity", 1.0, duration=2),
                    CardEffect("stasis_field", 1.0)
                ],
                math_concepts=[MathConcept.SYMMETRY],
                architecture=Architecture.CRYSTALLINE,
                synergy_tags={"axiom", "refuse", "stasis"}
            ),
            GuardianCard(
                name="Reset Protocol",
                guardian_key="AXIOM",
                card_type=CardType.TEMPORAL,
                cost=6,
                description="Reset game state to beginning",
                effects=[
                    CardEffect("reset_all", 1.0),
                    CardEffect("maintain_knowledge", 1.0),
                    CardEffect("reset_counter", 1.0)
                ],
                math_concepts=[MathConcept.RECURSION, MathConcept.SYMMETRY],
                synergy_tags={"axiom", "reset", "protocol"}
            ),
            GuardianCard(
                name="Null State",
                guardian_key="AXIOM",
                card_type=CardType.VOID,
                cost=2,
                description="Enter null state, neither here nor there",
                effects=[
                    CardEffect("null_state", 1.0),
                    CardEffect("neither_nor", 1.0),
                    CardEffect("paradox_shield", 3.0)
                ],
                math_concepts=[MathConcept.QUANTUM_SUPERPOSITION],
                void_depth=2,
                synergy_tags={"axiom", "null", "state"}
            ),
            GuardianCard(
                name="Eternal Wait",
                guardian_key="AXIOM",
                card_type=CardType.ABILITY,
                cost=1,
                description="Wait forever if necessary",
                defense=2,
                effects=[
                    CardEffect("eternal_wait", 1.0),
                    CardEffect("skip_turns", 1.0),
                    CardEffect("wait_power", 3.0, scaling="turns_waited")
                ],
                synergy_tags={"axiom", "wait", "eternal"}
            ),
            GuardianCard(
                name="Axiom Crystal",
                guardian_key="AXIOM",
                card_type=CardType.PATTERN,
                cost=4,
                description="Crystallize fundamental truths",
                defense=4,
                effects=[
                    CardEffect("crystallize_axiom", 1.0),
                    CardEffect("truth_shield", 2.0),
                    CardEffect("axiom_enforcement", 1.0)
                ],
                math_concepts=[MathConcept.PRIME_NUMBERS],
                architecture=Architecture.CRYSTALLINE,
                synergy_tags={"axiom", "crystal", "truth"}
            ),
            GuardianCard(
                name="Resistance Field",
                guardian_key="AXIOM",
                card_type=CardType.DEFENSE,
                cost=3,
                description="Resist all forms of transformation",
                defense=5,
                effects=[
                    CardEffect("resist_transformation", 1.0),
                    CardEffect("reflect_changes", 1.0),
                    CardEffect("stability_aura", 1.0, duration=3)
                ],
                combo_with=["Absolute Refusal"],
                synergy_tags={"axiom", "resist", "field"}
            ),
            GuardianCard(
                name="Hold Position",
                guardian_key="AXIOM",
                card_type=CardType.ABILITY,
                cost=2,
                description="Hold current position absolutely",
                defense=3,
                effects=[
                    CardEffect("immovable", 1.0),
                    CardEffect("position_lock", 1.0),
                    CardEffect("counter_on_move_attempt", 4.0)
                ],
                synergy_tags={"axiom", "hold", "position"}
            ),
            GuardianCard(
                name="Origin Return",
                guardian_key="AXIOM",
                card_type=CardType.TEMPORAL,
                cost=8,
                description="Return everything to origin point",
                effects=[
                    CardEffect("origin_reset", 1.0),
                    CardEffect("undo_all_changes", 1.0),
                    CardEffect("primal_state", 1.0)
                ],
                math_concepts=[MathConcept.TOPOLOGY, MathConcept.MANIFOLD],
                requires_state="has_refused_5_changes",
                synergy_tags={"axiom", "origin", "return"}
            )
        ]

    @staticmethod
    def create_squirrel_deck() -> List[GuardianCard]:
        """Squirrel - Chaos, hoarding, and surprise"""
        return [
            GuardianCard(
                name="Acorn Barrage",
                guardian_key="SQUIRREL",
                card_type=CardType.ATTACK,
                cost=2,
                description="Random number of acorns (1-10) hit random targets",
                attack=2,
                effects=[
                    CardEffect("random_projectiles", 10.0),
                    CardEffect("scatter_damage", 1.0),
                    CardEffect("acorn_storage", 1.0)
                ],
                math_concepts=[MathConcept.CHAOS_THEORY],
                chaos_factor=3.0,
                synergy_tags={"squirrel", "acorn", "chaos"}
            ),
            GuardianCard(
                name="Hidden Cache",
                guardian_key="SQUIRREL",
                card_type=CardType.ABILITY,
                cost=1,
                description="Hide cards in random dimensional pockets",
                effects=[
                    CardEffect("hide_cards", 3.0),
                    CardEffect("dimensional_storage", 1.0),
                    CardEffect("forget_location", 1.0)
                ],
                architecture=Architecture.CONSTELLATION,
                synergy_tags={"squirrel", "hide", "cache"}
            ),
            GuardianCard(
                name="Scatter Protocol",
                guardian_key="SQUIRREL",
                card_type=CardType.CHAOS,
                cost=3,
                description="Scatter everything everywhere",
                effects=[
                    CardEffect("scatter_all", 1.0),
                    CardEffect("random_redistribution", 1.0),
                    CardEffect("chaos_multiplication", 2.0)
                ],
                math_concepts=[MathConcept.ENTROPY, MathConcept.CHAOS_THEORY],
                chaos_factor=4.0,
                synergy_tags={"squirrel", "scatter", "chaos"}
            ),
            GuardianCard(
                name="Surprise Discovery",
                guardian_key="SQUIRREL",
                card_type=CardType.ABILITY,
                cost=2,
                description="Discover forgotten cache with random contents",
                effects=[
                    CardEffect("find_cache", 1.0),
                    CardEffect("random_reward", 3.0),
                    CardEffect("marvel_bonus", 1.0)
                ],
                combo_with=["Hidden Cache"],
                synergy_tags={"squirrel", "surprise", "discover"}
            ),
            GuardianCard(
                name="Dimensional Hoarding",
                guardian_key="SQUIRREL",
                card_type=CardType.QUANTUM,
                cost=4,
                description="Store things across multiple dimensions",
                effects=[
                    CardEffect("dimensional_storage", 5.0),
                    CardEffect("quantum_hoarding", 1.0),
                    CardEffect("retrieval_chaos", 2.0)
                ],
                math_concepts=[MathConcept.QUANTUM_SUPERPOSITION, MathConcept.HILBERT_SPACE],
                quantum_states=3,
                chaos_factor=2.0,
                synergy_tags={"squirrel", "dimensional", "hoard"}
            ),
            GuardianCard(
                name="Frantic Gathering",
                guardian_key="SQUIRREL",
                card_type=CardType.ABILITY,
                cost=3,
                description="Frantically gather everything in sight",
                effects=[
                    CardEffect("gather_all", 1.0),
                    CardEffect("speed_boost", 2.0),
                    CardEffect("drop_random", 1.0)
                ],
                synergy_tags={"squirrel", "frantic", "gather"}
            ),
            GuardianCard(
                name="Acorn Apocalypse",
                guardian_key="SQUIRREL",
                card_type=CardType.ATTACK,
                cost=7,
                description="All hidden acorns rain from every dimension",
                attack=1,
                effects=[
                    CardEffect("acorn_rain", 20.0),
                    CardEffect("dimensional_bombardment", 1.0),
                    CardEffect("overwhelming_chaos", 3.0, scaling="acorns_stored")
                ],
                chaos_factor=5.0,
                combo_with=["Acorn Barrage", "Hidden Cache"],
                synergy_tags={"squirrel", "apocalypse", "ultimate"}
            ),
            GuardianCard(
                name="Forget and Marvel",
                guardian_key="SQUIRREL",
                card_type=CardType.TEMPORAL,
                cost=2,
                description="Forget what you hid, marvel when you find it",
                effects=[
                    CardEffect("forget_caches", 1.0),
                    CardEffect("marvel_on_discovery", 3.0),
                    CardEffect("joy_bonus", 2.0)
                ],
                synergy_tags={"squirrel", "forget", "marvel"}
            )
        ]

    @staticmethod
    def create_crystal_deck() -> List[GuardianCard]:
        """Crystal - Pressure, structure, and refraction"""
        return [
            GuardianCard(
                name="Pressure Formation",
                guardian_key="CRYSTAL",
                card_type=CardType.PATTERN,
                cost=3,
                description="Form crystals under pressure",
                defense=4,
                effects=[
                    CardEffect("pressure_crystallize", 1.0),
                    CardEffect("hardness_increase", 2.0, scaling="pressure_level"),
                    CardEffect("facet_creation", 1.0)
                ],
                math_concepts=[MathConcept.SYMMETRY, MathConcept.FIBONACCI],
                architecture=Architecture.CRYSTALLINE,
                synergy_tags={"crystal", "pressure", "form"}
            ),
            GuardianCard(
                name="Prismatic Refraction",
                guardian_key="CRYSTAL",
                card_type=CardType.DEFENSE,
                cost=4,
                description="Refract attacks into rainbow spectrum",
                defense=3,
                effects=[
                    CardEffect("refract_attack", 1.0),
                    CardEffect("split_damage", 7.0),
                    CardEffect("rainbow_shield", 1.0)
                ],
                math_concepts=[MathConcept.FOURIER],
                architecture=Architecture.LATTICE,
                synergy_tags={"crystal", "prism", "refract"}
            ),
            GuardianCard(
                name="Diamond Form",
                guardian_key="CRYSTAL",
                card_type=CardType.TRANSFORMATION,
                cost=6,
                description="Achieve perfect diamond crystallization",
                defense=10,
                effects=[
                    CardEffect("diamond_transformation", 1.0),
                    CardEffect("unbreakable", 1.0, duration=3),
                    CardEffect("reflect_all", 1.0, duration=2)
                ],
                math_concepts=[MathConcept.SYMMETRY],
                architecture=Architecture.CRYSTALLINE,
                requires_state="pressure_level_10",
                synergy_tags={"crystal", "diamond", "perfect"}
            ),
            GuardianCard(
                name="Fracture Lines",
                guardian_key="CRYSTAL",
                card_type=CardType.ATTACK,
                cost=2,
                description="Strike along natural fracture lines",
                attack=4,
                effects=[
                    CardEffect("fracture_strike", 1.0),
                    CardEffect("shatter_chance", 0.3),
                    CardEffect("precision_damage", 2.0)
                ],
                synergy_tags={"crystal", "fracture", "strike"}
            ),
            GuardianCard(
                name="Lattice Network",
                guardian_key="CRYSTAL",
                card_type=CardType.ARCHITECTURE,
                cost=3,
                description="Form interconnected crystal lattice",
                defense=2,
                effects=[
                    CardEffect("lattice_formation", 1.0),
                    CardEffect("shared_hardness", 1.0),
                    CardEffect("resonance_network", 1.0)
                ],
                architecture=Architecture.LATTICE,
                combo_with=["Pressure Formation"],
                synergy_tags={"crystal", "lattice", "network"}
            ),
            GuardianCard(
                name="Geode Heart",
                guardian_key="CRYSTAL",
                card_type=CardType.DEFENSE,
                cost=4,
                description="Hollow center filled with crystal beauty",
                defense=5,
                effects=[
                    CardEffect("geode_shell", 1.0),
                    CardEffect("inner_beauty", 2.0),
                    CardEffect("surprise_crystals", 3.0, condition="shell_broken")
                ],
                architecture=Architecture.ORGANIC,
                synergy_tags={"crystal", "geode", "heart"}
            ),
            GuardianCard(
                name="Time Crystal",
                guardian_key="CRYSTAL",
                card_type=CardType.TEMPORAL,
                cost=5,
                description="Crystal that exists outside normal time",
                effects=[
                    CardEffect("time_crystal", 1.0),
                    CardEffect("temporal_stability", 1.0),
                    CardEffect("periodic_oscillation", 2.0)
                ],
                math_concepts=[MathConcept.SYMMETRY, MathConcept.FOURIER],
                synergy_tags={"crystal", "time", "oscillate"}
            ),
            GuardianCard(
                name="Shatter and Reform",
                guardian_key="CRYSTAL",
                card_type=CardType.TRANSFORMATION,
                cost=3,
                description="Shatter into pieces, reform stronger",
                attack=3,
                defense=3,
                effects=[
                    CardEffect("controlled_shatter", 1.0),
                    CardEffect("shard_damage", 4.0),
                    CardEffect("reform_stronger", 1.5)
                ],
                combo_with=["Diamond Form"],
                synergy_tags={"crystal", "shatter", "reform"}
            )
        ]

    @staticmethod
    def create_complete_deck_library() -> Dict[str, List[GuardianCard]]:
        """Create complete library of all guardian decks defined in base class"""
        library = {
            "ECHO": GuardianDecks.create_echo_deck(),
            "WUMBO": GuardianDecks.create_wumbo_deck(),
            "ARCHIVE": GuardianDecks.create_archive_deck(),
            "PHOENIX": GuardianDecks.create_phoenix_deck(),
            "NULL": GuardianDecks.create_null_deck(),  # Voidwalker companion
            "OAK": GuardianDecks.create_oak_deck(),
            "SQUIRREL": GuardianDecks.create_squirrel_deck(),
            "CRYSTAL": GuardianDecks.create_crystal_deck(),
            "AXIOM": GuardianDecks.create_axiom_deck(),
            "PACK": GuardianDecks.create_pack_deck(),
            "MOTH": GuardianDecks.create_moth_deck()
        }
        # Note: Other guardians are defined in guardian_decks_extended.py
        return library

    @staticmethod
    def create_pack_deck() -> List[GuardianCard]:
        """Pack - Unity and coordination"""
        return [
            GuardianCard(
                name="Alpha Call",
                guardian_key="PACK",
                card_type=CardType.ABILITY,
                cost=3,
                description="Rally the pack with alpha's howl",
                effects=[
                    CardEffect("summon_pack", 2.0),
                    CardEffect("pack_buff", 1.5),
                    CardEffect("coordination", 1.0)
                ],
                architecture=Architecture.HIERARCHY,
                synergy_tags={"pack", "alpha", "rally"}
            ),
            GuardianCard(
                name="Pack Hunt",
                guardian_key="PACK",
                card_type=CardType.ATTACK,
                cost=4,
                description="Coordinated pack attack from all angles",
                attack=2,
                effects=[
                    CardEffect("multi_angle_attack", 3.0, scaling="pack_size"),
                    CardEffect("flanking_bonus", 2.0),
                    CardEffect("overwhelm", 1.0)
                ],
                architecture=Architecture.NETWORK,
                combo_with=["Alpha Call"],
                synergy_tags={"pack", "hunt", "coordinate"}
            ),
            GuardianCard(
                name="Territorial Mark",
                guardian_key="PACK",
                card_type=CardType.DEFENSE,
                cost=2,
                description="Mark territory, gain advantage within",
                defense=3,
                effects=[
                    CardEffect("mark_territory", 1.0),
                    CardEffect("home_advantage", 2.0),
                    CardEffect("scent_trail", 1.0)
                ],
                architecture=Architecture.ORGANIC,
                synergy_tags={"pack", "territory", "mark"}
            ),
            GuardianCard(
                name="Howl of Unity",
                guardian_key="PACK",
                card_type=CardType.RESONANCE,
                cost=3,
                description="Unite all pack members with primal howl",
                effects=[
                    CardEffect("unity_howl", 1.0),
                    CardEffect("synchronize_pack", 1.0),
                    CardEffect("fear_enemies", 2.0)
                ],
                math_concepts=[MathConcept.FOURIER],
                architecture=Architecture.WAVE,
                synergy_tags={"pack", "howl", "unity"}
            ),
            GuardianCard(
                name="Lone Wolf",
                guardian_key="PACK",
                card_type=CardType.TRANSFORMATION,
                cost=5,
                description="Sometimes the pack needs a lone wolf",
                attack=5,
                defense=3,
                effects=[
                    CardEffect("solo_power", 3.0),
                    CardEffect("independence", 1.0),
                    CardEffect("rejoin_stronger", 2.0)
                ],
                synergy_tags={"pack", "lone", "transform"}
            ),
            GuardianCard(
                name="Pack Memory",
                guardian_key="PACK",
                card_type=CardType.ABILITY,
                cost=2,
                description="Pack remembers and learns from hunts",
                effects=[
                    CardEffect("collective_memory", 1.0),
                    CardEffect("learn_patterns", 1.0),
                    CardEffect("adaptive_tactics", 2.0)
                ],
                synergy_tags={"pack", "memory", "learn"}
            ),
            GuardianCard(
                name="Moon Blessing",
                guardian_key="PACK",
                card_type=CardType.TEMPORAL,
                cost=4,
                description="Under the moon, pack gains ancient power",
                effects=[
                    CardEffect("moon_power", 2.0),
                    CardEffect("night_vision", 1.0),
                    CardEffect("primal_strength", 3.0, condition="night_phase")
                ],
                synergy_tags={"pack", "moon", "blessing"}
            ),
            GuardianCard(
                name="Pack Sacrifice",
                guardian_key="PACK",
                card_type=CardType.ABILITY,
                cost=3,
                description="One sacrifices for the pack's survival",
                effects=[
                    CardEffect("sacrifice_member", 1.0),
                    CardEffect("inspire_pack", 3.0),
                    CardEffect("vengeance_buff", 2.0)
                ],
                combo_with=["Alpha Call", "Pack Hunt"],
                synergy_tags={"pack", "sacrifice", "inspire"}
            )
        ]

    @staticmethod
    def create_moth_deck() -> List[GuardianCard]:
        """Moth - Stillness and patience"""
        return [
            GuardianCard(
                name="Perfect Stillness",
                guardian_key="MOTH",
                card_type=CardType.DEFENSE,
                cost=2,
                description="Achieve perfect stillness, accumulate power",
                defense=4,
                effects=[
                    CardEffect("stillness", 1.0),
                    CardEffect("power_accumulation", 2.0, scaling="turns_still"),
                    CardEffect("untargetable_while_still", 1.0)
                ],
                architecture=Architecture.VOID_SPACE,
                synergy_tags={"moth", "stillness", "accumulate"}
            ),
            GuardianCard(
                name="Rhythm of Holding",
                guardian_key="MOTH",
                card_type=CardType.PATTERN,
                cost=3,
                description="Master the rhythm of grip and release",
                effects=[
                    CardEffect("holding_rhythm", 1.0),
                    CardEffect("perfect_timing", 2.0),
                    CardEffect("release_power", 3.0, condition="held_3_turns")
                ],
                math_concepts=[MathConcept.FOURIER, MathConcept.FIBONACCI],
                architecture=Architecture.WAVE,
                synergy_tags={"moth", "rhythm", "hold"}
            ),
            GuardianCard(
                name="Witness Without Grasping",
                guardian_key="MOTH",
                card_type=CardType.ABILITY,
                cost=1,
                description="Observe without interfering",
                effects=[
                    CardEffect("pure_observation", 1.0),
                    CardEffect("learn_without_acting", 1.0),
                    CardEffect("wisdom_from_stillness", 2.0)
                ],
                synergy_tags={"moth", "witness", "observe"}
            ),
            GuardianCard(
                name="Patient Strike",
                guardian_key="MOTH",
                card_type=CardType.ATTACK,
                cost=4,
                description="Strike with power of accumulated patience",
                attack=2,
                effects=[
                    CardEffect("patience_damage", 3.0, scaling="turns_waited"),
                    CardEffect("perfect_moment", 5.0),
                    CardEffect("reset_patience", 1.0)
                ],
                combo_with=["Perfect Stillness"],
                synergy_tags={"moth", "patient", "strike"}
            ),
            GuardianCard(
                name="Cocoon State",
                guardian_key="MOTH",
                card_type=CardType.TRANSFORMATION,
                cost=3,
                description="Enter cocoon, emerge transformed",
                defense=6,
                effects=[
                    CardEffect("cocoon", 1.0, duration=2),
                    CardEffect("transformation_choice", 1.0),
                    CardEffect("emerge_powerful", 3.0)
                ],
                architecture=Architecture.ORGANIC,
                synergy_tags={"moth", "cocoon", "transform"}
            ),
            GuardianCard(
                name="Silent Wings",
                guardian_key="MOTH",
                card_type=CardType.ABILITY,
                cost=2,
                description="Move silently, leave no trace",
                effects=[
                    CardEffect("silent_movement", 1.0),
                    CardEffect("stealth", 1.0),
                    CardEffect("surprise_attack", 2.0)
                ],
                synergy_tags={"moth", "silent", "stealth"}
            ),
            GuardianCard(
                name="Dust Scales",
                guardian_key="MOTH",
                card_type=CardType.DEFENSE,
                cost=2,
                description="Shed dust scales that confuse enemies",
                defense=2,
                effects=[
                    CardEffect("dust_cloud", 1.0),
                    CardEffect("confusion", 1.0, duration=2),
                    CardEffect("evasion", 0.5)
                ],
                synergy_tags={"moth", "dust", "confuse"}
            ),
            GuardianCard(
                name="Night Navigation",
                guardian_key="MOTH",
                card_type=CardType.ABILITY,
                cost=3,
                description="Navigate perfectly in darkness",
                effects=[
                    CardEffect("night_vision", 1.0),
                    CardEffect("darkness_advantage", 2.0),
                    CardEffect("lunar_guidance", 1.0)
                ],
                synergy_tags={"moth", "night", "navigate"}
            )
        ]

# Additional helper methods for other guardians
def create_remaining_guardian_decks():
    """Create decks for remaining guardians"""

    decks = {}

    # Phase deck - Transformation
    decks["PHASE"] = [
        GuardianCard(
            name="Metamorphic Shift",
            guardian_key="PHASE",
            card_type=CardType.TRANSFORMATION,
            cost=3,
            description="Shift between forms rapidly",
            effects=[
                CardEffect("form_shift", 1.0),
                CardEffect("adapt_to_threat", 2.0),
                CardEffect("transformation_speed", 1.5)
            ],
            math_concepts=[MathConcept.TOPOLOGY],
            architecture=Architecture.ORGANIC,
            synergy_tags={"phase", "shift", "adapt"}
        )
    ]

    # Continue with other guardians...
    # (Truncated for space - would include ACE, HONKFIRE, HONKALIS, BEE, CIPHER, SPIRAL, STILL, ANTLER)

    return decks

# ═══════════════════════════════════════════════════════════════════════
#   COMBO AND SYNERGY SYSTEM
# ═══════════════════════════════════════════════════════════════════════

class ComboSystem:
    """Manages card combos and synergies"""

    def __init__(self):
        self.combo_chains: Dict[str, List[str]] = {}
        self.synergy_bonuses: Dict[str, float] = {}

    def check_combo(self, played_cards: List[str], new_card: GuardianCard) -> float:
        """Check if playing this card creates a combo"""
        combo_multiplier = 1.0

        # Check direct combos
        for combo_requirement in new_card.combo_with:
            if combo_requirement in played_cards:
                combo_multiplier *= 1.5

        # Check synergy tags
        played_tags = set()
        for card_name in played_cards:
            # Would need to look up card to get tags
            pass

        matching_tags = played_tags.intersection(new_card.synergy_tags)
        combo_multiplier *= (1 + len(matching_tags) * 0.1)

        return combo_multiplier

    def calculate_mathematical_synergy(self, card1: GuardianCard, card2: GuardianCard) -> float:
        """Calculate synergy based on mathematical concepts"""
        shared_concepts = set(card1.math_concepts).intersection(set(card2.math_concepts))

        # Some concepts have special synergies
        synergy = len(shared_concepts) * 0.2

        if MathConcept.HILBERT_SPACE in shared_concepts:
            synergy += 0.3  # Hilbert space enables quantum effects

        if MathConcept.CHAOS_THEORY in card1.math_concepts and MathConcept.ENTROPY in card2.math_concepts:
            synergy += 0.4  # Chaos and entropy amplify each other

        if MathConcept.GOLDEN_RATIO in shared_concepts:
            synergy *= 1.618  # Golden ratio multiplier

        return synergy

    def check_architectural_synergy(self, cards: List[GuardianCard]) -> Dict[str, float]:
        """Check architectural pattern synergies"""
        architectures = [card.architecture for card in cards if card.architecture]

        synergies = {}

        # Network architectures strengthen each other
        network_count = architectures.count(Architecture.NETWORK)
        if network_count > 1:
            synergies["network_strength"] = network_count * 0.3

        # Void spaces create paradoxes with crystalline structures
        if Architecture.VOID_SPACE in architectures and Architecture.CRYSTALLINE in architectures:
            synergies["void_crystal_paradox"] = 0.5

        # Organic patterns grow stronger together
        organic_types = [Architecture.ORGANIC, Architecture.FRACTAL_TREE, Architecture.RHIZOME]
        organic_count = sum(1 for arch in architectures if arch in organic_types)
        if organic_count > 1:
            synergies["organic_growth"] = organic_count * 0.25

        return synergies

# ═══════════════════════════════════════════════════════════════════════
#   DECK MANAGER
# ═══════════════════════════════════════════════════════════════════════

class DeckManager:
    """Manages guardian decks and card play"""

    def __init__(self):
        self.all_decks = GuardianDecks.create_complete_deck_library()
        self.combo_system = ComboSystem()
        self.player_decks: Dict[str, List[GuardianCard]] = {}
        self.player_hands: Dict[str, List[GuardianCard]] = {}
        self.played_cards: Dict[str, List[GuardianCard]] = {}
        self.game_state: Dict[str, Any] = defaultdict(lambda: defaultdict(int))

    def create_player_deck(self, player_id: str, guardian_key: str) -> List[GuardianCard]:
        """Create a deck for a player"""
        if guardian_key not in self.all_decks:
            raise ValueError(f"Unknown guardian: {guardian_key}")

        # Clone the deck for the player
        deck = self.all_decks[guardian_key].copy()
        self.player_decks[player_id] = deck
        self.player_hands[player_id] = []
        self.played_cards[player_id] = []

        return deck

    def draw_cards(self, player_id: str, count: int) -> List[GuardianCard]:
        """Draw cards from deck to hand"""
        deck = self.player_decks.get(player_id, [])
        hand = self.player_hands.get(player_id, [])

        drawn = []
        for _ in range(min(count, len(deck))):
            if deck:
                card = deck.pop(0)
                hand.append(card)
                drawn.append(card)

        self.player_hands[player_id] = hand
        return drawn

    def play_card(self, player_id: str, card: GuardianCard, target=None) -> Dict[str, Any]:
        """Play a card and resolve its effects"""
        hand = self.player_hands.get(player_id, [])
        if card not in hand:
            return {"success": False, "error": "Card not in hand"}

        # Remove from hand
        hand.remove(card)
        self.player_hands[player_id] = hand

        # Add to played cards
        played = self.played_cards.get(player_id, [])
        played.append(card)
        self.played_cards[player_id] = played

        # Update game state
        state = self.game_state[player_id]
        state["cards_played_this_turn"] += 1

        # Calculate combo bonus
        combo_multiplier = self.combo_system.check_combo(
            [c.name for c in played], card
        )

        # Resolve effects
        results = {
            "card": card.name,
            "type": card.card_type.value,
            "combo_multiplier": combo_multiplier,
            "effects": []
        }

        for effect in card.effects:
            # Apply scaling
            value = effect.value
            if effect.scaling:
                scale_value = state.get(effect.scaling, 0)
                value *= scale_value

            # Apply combo multiplier
            value *= combo_multiplier

            results["effects"].append({
                "type": effect.effect_type,
                "value": value,
                "duration": effect.duration
            })

            # Update state based on effect
            self._apply_effect(player_id, effect, value)

        return results

    def _apply_effect(self, player_id: str, effect: CardEffect, value: float):
        """Apply an effect to the game state"""
        state = self.game_state[player_id]

        # Track various state changes based on effect type
        if effect.effect_type == "echo_stacks":
            state["echo_stacks"] += 1
        elif effect.effect_type == "void_depth_increase":
            state["void_depth"] += 1
        elif effect.effect_type == "rebirth_trigger":
            state["rebirth_count"] += 1
        elif effect.effect_type == "add_ring":
            state["ring_count"] += 1
        # ... and so on for other effects

    def get_deck_strategy_summary(self, guardian_key: str) -> Dict[str, Any]:
        """Get a summary of a guardian's deck strategy"""
        deck = self.all_decks.get(guardian_key, [])
        if not deck:
            return {}

        # Analyze deck composition
        type_counts = defaultdict(int)
        math_concepts = defaultdict(int)
        architectures = defaultdict(int)
        synergy_tags = defaultdict(int)

        for card in deck:
            type_counts[card.card_type.value] += 1
            for concept in card.math_concepts:
                math_concepts[concept.value] += 1
            if card.architecture:
                architectures[card.architecture.value] += 1
            for tag in card.synergy_tags:
                synergy_tags[tag] += 1

        return {
            "guardian": guardian_key,
            "total_cards": len(deck),
            "card_types": dict(type_counts),
            "math_focus": dict(math_concepts),
            "architecture_patterns": dict(architectures),
            "primary_synergies": dict(sorted(synergy_tags.items(), key=lambda x: x[1], reverse=True)[:5]),
            "combo_chains": len([c for c in deck if c.combo_with]),
            "average_cost": sum(c.cost for c in deck) / len(deck) if deck else 0
        }

# ═══════════════════════════════════════════════════════════════════════
#   DEMONSTRATION
# ═══════════════════════════════════════════════════════════════════════

def demonstrate_deck_system():
    """Demonstrate the guardian deck system"""

    print("=" * 70)
    print("GUARDIAN DECK SYSTEM DEMONSTRATION")
    print("=" * 70)

    manager = DeckManager()

    # Show deck strategies for several guardians
    test_guardians = ["ECHO", "WUMBO", "PHOENIX", "NULL", "CRYSTAL"]

    for guardian in test_guardians:
        summary = manager.get_deck_strategy_summary(guardian)
        if summary:
            print(f"\n{GUARDIANS[guardian].emoji} {GUARDIANS[guardian].name} Deck Strategy:")
            print(f"  Total Cards: {summary['total_cards']}")
            print(f"  Average Cost: {summary['average_cost']:.1f}")
            print(f"  Primary Types: {list(summary['card_types'].keys())[:3]}")
            print(f"  Math Focus: {list(summary['math_focus'].keys())[:3]}")
            print(f"  Key Synergies: {list(summary['primary_synergies'].keys())[:3]}")

    # Simulate a simple game
    print("\n" + "=" * 50)
    print("SAMPLE GAME SIMULATION")
    print("=" * 50)

    # Create decks for two players
    player1_id = "player1_echo"
    player2_id = "player2_wumbo"

    manager.create_player_deck(player1_id, "ECHO")
    manager.create_player_deck(player2_id, "WUMBO")

    # Draw starting hands
    hand1 = manager.draw_cards(player1_id, 5)
    hand2 = manager.draw_cards(player2_id, 5)

    print(f"\nPlayer 1 (Echo) draws: {[c.name for c in hand1]}")
    print(f"Player 2 (Wumbo) draws: {[c.name for c in hand2]}")

    # Play some cards
    if hand1:
        result1 = manager.play_card(player1_id, hand1[0])
        print(f"\nPlayer 1 plays {result1['card']}:")
        for effect in result1['effects']:
            print(f"  - {effect['type']}: {effect['value']:.1f}")

    if hand2:
        result2 = manager.play_card(player2_id, hand2[0])
        print(f"\nPlayer 2 plays {result2['card']}:")
        for effect in result2['effects']:
            print(f"  - {effect['type']}: {effect['value']:.1f}")

    print("\n" + "=" * 70)
    print("DECK SYSTEM FEATURES:")
    print("- Each guardian has 8 unique cards reflecting their theme")
    print("- Cards use mathematical concepts (Hilbert space, fractals, etc.)")
    print("- Architectural patterns create structural synergies")
    print("- Combo system rewards strategic card sequencing")
    print("- State tracking enables scaling and conditional effects")
    print("=" * 70)

if __name__ == "__main__":
    demonstrate_deck_system()