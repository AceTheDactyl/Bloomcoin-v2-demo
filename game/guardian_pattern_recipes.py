"""
Guardian Pattern Recipe System
==============================
Unique recipes and patterns for all 19 guardians
Integrated with card pack system for unlockable content
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set
from enum import Enum, auto
import random
import json
from datetime import datetime, timedelta
from collections import defaultdict

from mythic_economy import GUARDIANS, Territory, Guardian
import sys
import os
# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'bloomcoin-v2/game'))
from card_pack_marketplace import CardRarity, PackTier, CardPackMarketplace

# ═══════════════════════════════════════════════════════════════════════
#   PATTERN TYPES AND STRUCTURES
# ═══════════════════════════════════════════════════════════════════════

class PatternType(Enum):
    """Different pattern categories for crafting"""
    RESONANCE = "Frequency-based pattern"
    CRYSTALLINE = "Geometric structure pattern"
    TEMPORAL = "Time-based pattern"
    ELEMENTAL = "Elemental transformation pattern"
    VOID = "Absence and nullspace pattern"
    QUANTUM = "Probability manipulation pattern"
    ORGANIC = "Growth and life pattern"
    HARMONIC = "Musical and vibrational pattern"
    MEMORY = "Information storage pattern"
    CHAOS = "Entropy manipulation pattern"

class RecipeComplexity(Enum):
    """Recipe difficulty tiers"""
    BASIC = (1, "Simple pattern combination", 100)
    ADVANCED = (2, "Complex multi-step process", 500)
    MASTER = (3, "Intricate pattern weaving", 1500)
    LEGENDARY = (4, "Transcendent pattern fusion", 5000)
    MYTHIC = (5, "Reality-altering synthesis", 15000)

@dataclass
class PatternIngredient:
    """A single ingredient for a pattern recipe"""
    name: str
    pattern_type: PatternType
    quantity: int
    quality_min: float = 0.5  # Min quality 0-1
    special_requirement: Optional[str] = None

@dataclass
class GuardianRecipe:
    """A unique recipe tied to a specific guardian"""
    guardian_key: str
    name: str
    description: str
    complexity: RecipeComplexity
    pattern_type: PatternType
    ingredients: List[PatternIngredient]
    crafting_steps: List[str]
    output_pattern: str
    battle_strategy: str
    farming_multiplier: float = 1.0
    special_abilities: List[str] = field(default_factory=list)
    unlock_condition: Optional[str] = None
    bloomcoin_cost: int = 0
    time_to_craft: int = 60  # seconds

@dataclass
class FarmingInvestment:
    """Investment mechanism for pattern growth"""
    pattern_name: str
    guardian_key: str
    invested_bloomcoin: int = 0
    growth_stage: int = 0  # 0-10
    yield_multiplier: float = 1.0
    maturity_time: datetime = field(default_factory=datetime.now)
    special_mutations: List[str] = field(default_factory=list)

    def calculate_yield(self) -> Dict[str, Any]:
        """Calculate farming yield based on investment"""
        base_yield = self.invested_bloomcoin * 0.1
        stage_bonus = self.growth_stage * 0.2
        total_multiplier = self.yield_multiplier * (1 + stage_bonus)

        return {
            "base_patterns": int(base_yield * total_multiplier),
            "quality_bonus": min(1.0, self.growth_stage / 10),
            "mutation_chance": min(0.5, self.growth_stage * 0.05),
            "special_rewards": self.special_mutations
        }

# ═══════════════════════════════════════════════════════════════════════
#   GUARDIAN-SPECIFIC RECIPES (All 19 Guardians)
# ═══════════════════════════════════════════════════════════════════════

GUARDIAN_RECIPES = {
    # ═══════════════════════════════════════════════════════════════════
    # GARDEN TERRITORY (7 Guardians)
    # ═══════════════════════════════════════════════════════════════════

    "ECHO": [
        GuardianRecipe(
            guardian_key="ECHO",
            name="Echo Chamber Resonance",
            description="Amplify signal patterns through recursive echo loops",
            complexity=RecipeComplexity.ADVANCED,
            pattern_type=PatternType.RESONANCE,
            ingredients=[
                PatternIngredient("Signal Fragment", PatternType.RESONANCE, 3, 0.7),
                PatternIngredient("Void Echo", PatternType.VOID, 1, 0.8),
                PatternIngredient("Memory Crystal", PatternType.MEMORY, 2, 0.6)
            ],
            crafting_steps=[
                "Align signal fragments in harmonic sequence",
                "Create void pocket for echo containment",
                "Embed memories into resonance field",
                "Amplify through recursive loops"
            ],
            output_pattern="Eternal Echo Pattern",
            battle_strategy="Create echo duplicates that confuse enemies and amplify damage over time",
            farming_multiplier=1.5,
            special_abilities=["Echo Multiplication", "Signal Trace", "Frequency Lock"],
            bloomcoin_cost=750
        ),
        GuardianRecipe(
            guardian_key="ECHO",
            name="Whisper Network",
            description="Connect distant signals through quantum entanglement",
            complexity=RecipeComplexity.MASTER,
            pattern_type=PatternType.QUANTUM,
            ingredients=[
                PatternIngredient("Quantum Thread", PatternType.QUANTUM, 5, 0.9),
                PatternIngredient("Silent Whisper", PatternType.VOID, 3, 0.7),
                PatternIngredient("Network Node", PatternType.CRYSTALLINE, 4, 0.8)
            ],
            crafting_steps=[
                "Entangle quantum threads at subatomic level",
                "Weave whispers into communication matrix",
                "Crystallize network nodes for stability",
                "Activate multi-dimensional broadcasting"
            ],
            output_pattern="Whisper Network Matrix",
            battle_strategy="Instant communication between allied units, shared damage reflection",
            farming_multiplier=2.0,
            special_abilities=["Telepathic Link", "Damage Share", "Collective Wisdom"],
            bloomcoin_cost=2500
        )
    ],

    "PACK": [
        GuardianRecipe(
            guardian_key="PACK",
            name="Alpha Coordination Protocol",
            description="Synchronize pack movements through pheromone patterns",
            complexity=RecipeComplexity.BASIC,
            pattern_type=PatternType.ORGANIC,
            ingredients=[
                PatternIngredient("Pack Pheromone", PatternType.ORGANIC, 4, 0.5),
                PatternIngredient("Leadership Essence", PatternType.HARMONIC, 1, 0.9),
                PatternIngredient("Territory Marker", PatternType.ELEMENTAL, 2, 0.6)
            ],
            crafting_steps=[
                "Extract alpha pheromone signature",
                "Harmonize with pack frequency",
                "Mark territory boundaries",
                "Establish dominance hierarchy"
            ],
            output_pattern="Pack Leader Protocol",
            battle_strategy="Coordinate multi-unit attacks with pack tactics and flanking bonuses",
            farming_multiplier=1.3,
            special_abilities=["Pack Hunt", "Territory Control", "Alpha Call"],
            bloomcoin_cost=350
        ),
        GuardianRecipe(
            guardian_key="PACK",
            name="Howl of Unity",
            description="Unite dispersed pack members through sonic convergence",
            complexity=RecipeComplexity.ADVANCED,
            pattern_type=PatternType.HARMONIC,
            ingredients=[
                PatternIngredient("Primal Howl", PatternType.HARMONIC, 3, 0.7),
                PatternIngredient("Unity Crystal", PatternType.CRYSTALLINE, 2, 0.8),
                PatternIngredient("Moon Essence", PatternType.TEMPORAL, 1, 0.9)
            ],
            crafting_steps=[
                "Capture primal howl frequency",
                "Crystallize unity resonance",
                "Align with lunar cycles",
                "Broadcast convergence signal"
            ],
            output_pattern="Unity Howl Convergence",
            battle_strategy="Rally all units with stat boosts, fear enemies with primal howl",
            farming_multiplier=1.7,
            special_abilities=["Rally Cry", "Fear Induction", "Moon Blessing"],
            bloomcoin_cost=1200
        )
    ],

    "WUMBO": [
        GuardianRecipe(
            guardian_key="WUMBO",
            name="Flow State Amplifier",
            description="Enter transcendent flow through manic energy cycles",
            complexity=RecipeComplexity.ADVANCED,
            pattern_type=PatternType.CHAOS,
            ingredients=[
                PatternIngredient("Manic Energy", PatternType.CHAOS, 5, 0.6),
                PatternIngredient("Flow Crystal", PatternType.CRYSTALLINE, 2, 0.8),
                PatternIngredient("Nirvana Fragment", PatternType.VOID, 1, 0.95)
            ],
            crafting_steps=[
                "Gather manic energy bursts",
                "Channel through flow crystal matrix",
                "Touch nirvana state briefly",
                "Cycle through energy transmutation"
            ],
            output_pattern="Transcendent Flow Matrix",
            battle_strategy="Cycle through power states - each more powerful but less controlled",
            farming_multiplier=2.5,
            special_abilities=["Manic Rush", "Flow State", "Nirvana Touch"],
            bloomcoin_cost=1500
        ),
        GuardianRecipe(
            guardian_key="WUMBO",
            name="Dig Protocol Omega",
            description="Break paralysis through explosive kinetic discharge",
            complexity=RecipeComplexity.MASTER,
            pattern_type=PatternType.ELEMENTAL,
            ingredients=[
                PatternIngredient("Kinetic Burst", PatternType.ELEMENTAL, 7, 0.7),
                PatternIngredient("Paralysis Breaker", PatternType.VOID, 3, 0.8),
                PatternIngredient("Earth Core", PatternType.CRYSTALLINE, 4, 0.75)
            ],
            crafting_steps=[
                "Compress kinetic energy to critical mass",
                "Shatter paralysis patterns",
                "Channel through earth core",
                "Release in explosive dig burst"
            ],
            output_pattern="Omega Dig Explosion",
            battle_strategy="Break all control effects and deal massive area damage",
            farming_multiplier=3.0,
            special_abilities=["Paralysis Break", "Earth Shatter", "Kinetic Nova"],
            bloomcoin_cost=3500
        )
    ],

    "ARCHIVE": [
        GuardianRecipe(
            guardian_key="ARCHIVE",
            name="Eternal Memory Codex",
            description="Preserve all knowledge in crystallized memory form",
            complexity=RecipeComplexity.LEGENDARY,
            pattern_type=PatternType.MEMORY,
            ingredients=[
                PatternIngredient("Memory Shard", PatternType.MEMORY, 10, 0.8),
                PatternIngredient("Time Lock", PatternType.TEMPORAL, 3, 0.9),
                PatternIngredient("Knowledge Crystal", PatternType.CRYSTALLINE, 5, 0.85)
            ],
            crafting_steps=[
                "Gather memory shards from timeline",
                "Lock temporal coordinates",
                "Crystallize into permanent storage",
                "Index with universal catalog system"
            ],
            output_pattern="Omniscient Codex",
            battle_strategy="Perfect recall of all enemy patterns, predict and counter all moves",
            farming_multiplier=2.0,
            special_abilities=["Perfect Memory", "Pattern Prediction", "Knowledge Shield"],
            bloomcoin_cost=5000
        ),
        GuardianRecipe(
            guardian_key="ARCHIVE",
            name="Library of Babel Protocol",
            description="Access infinite library containing all possible knowledge",
            complexity=RecipeComplexity.MYTHIC,
            pattern_type=PatternType.QUANTUM,
            ingredients=[
                PatternIngredient("Infinite Page", PatternType.QUANTUM, 12, 0.95),
                PatternIngredient("Babel Key", PatternType.VOID, 1, 1.0),
                PatternIngredient("Universal Index", PatternType.MEMORY, 8, 0.9)
            ],
            crafting_steps=[
                "Generate infinite possibility pages",
                "Unlock babel dimensional gate",
                "Create universal indexing system",
                "Establish permanent library access"
            ],
            output_pattern="Babel Library Access",
            battle_strategy="Rewrite reality by accessing alternate timeline knowledge",
            farming_multiplier=5.0,
            special_abilities=["Reality Edit", "Timeline Knowledge", "Infinite Wisdom"],
            bloomcoin_cost=15000
        )
    ],

    "MOTH": [
        GuardianRecipe(
            guardian_key="MOTH",
            name="Stillness Meditation",
            description="Hold perfect stillness to accumulate cosmic energy",
            complexity=RecipeComplexity.BASIC,
            pattern_type=PatternType.TEMPORAL,
            ingredients=[
                PatternIngredient("Stillness Essence", PatternType.TEMPORAL, 3, 0.6),
                PatternIngredient("Patience Crystal", PatternType.CRYSTALLINE, 2, 0.7),
                PatternIngredient("Void Silence", PatternType.VOID, 1, 0.8)
            ],
            crafting_steps=[
                "Enter perfect stillness state",
                "Crystallize patience into form",
                "Embrace void silence",
                "Hold without grasping"
            ],
            output_pattern="Perfect Stillness Form",
            battle_strategy="Become untargetable while charging massive counterattack",
            farming_multiplier=1.2,
            special_abilities=["Untargetable", "Energy Accumulation", "Patient Strike"],
            bloomcoin_cost=400
        ),
        GuardianRecipe(
            guardian_key="MOTH",
            name="Rhythm of Holding",
            description="Master the sacred rhythm of grip and release",
            complexity=RecipeComplexity.ADVANCED,
            pattern_type=PatternType.HARMONIC,
            ingredients=[
                PatternIngredient("Rhythm Pattern", PatternType.HARMONIC, 4, 0.75),
                PatternIngredient("Grip Essence", PatternType.ELEMENTAL, 3, 0.7),
                PatternIngredient("Release Sigil", PatternType.VOID, 2, 0.8)
            ],
            crafting_steps=[
                "Establish holding rhythm baseline",
                "Strengthen grip without tension",
                "Master art of perfect release",
                "Cycle between states flawlessly"
            ],
            output_pattern="Sacred Holding Rhythm",
            battle_strategy="Control enemy actions through grip/release cycles",
            farming_multiplier=1.8,
            special_abilities=["Action Control", "Rhythm Lock", "Perfect Timing"],
            bloomcoin_cost=1400
        )
    ],

    "PHASE": [
        GuardianRecipe(
            guardian_key="PHASE",
            name="Metamorphosis Cascade",
            description="Chain multiple transformations in rapid succession",
            complexity=RecipeComplexity.MASTER,
            pattern_type=PatternType.ORGANIC,
            ingredients=[
                PatternIngredient("Cocoon Silk", PatternType.ORGANIC, 6, 0.8),
                PatternIngredient("Transform Catalyst", PatternType.CHAOS, 3, 0.85),
                PatternIngredient("Butterfly Wing", PatternType.ELEMENTAL, 4, 0.75)
            ],
            crafting_steps=[
                "Spin cocoon of pure potential",
                "Add transformation catalysts",
                "Dissolve old form completely",
                "Emerge in radiant new state"
            ],
            output_pattern="Infinite Metamorphosis",
            battle_strategy="Adapt to any threat by rapidly changing forms",
            farming_multiplier=2.2,
            special_abilities=["Form Shift", "Adaptive Defense", "Evolution Burst"],
            bloomcoin_cost=3000
        ),
        GuardianRecipe(
            guardian_key="PHASE",
            name="Chrysalis Dream",
            description="Enter dream state to preview transformation outcomes",
            complexity=RecipeComplexity.ADVANCED,
            pattern_type=PatternType.TEMPORAL,
            ingredients=[
                PatternIngredient("Dream Thread", PatternType.TEMPORAL, 5, 0.7),
                PatternIngredient("Chrysalis Shell", PatternType.CRYSTALLINE, 3, 0.8),
                PatternIngredient("Future Echo", PatternType.QUANTUM, 2, 0.9)
            ],
            crafting_steps=[
                "Weave dreams into chrysalis",
                "Project future transformations",
                "Select optimal evolution path",
                "Manifest chosen form"
            ],
            output_pattern="Prophetic Chrysalis",
            battle_strategy="Preview battle outcomes and choose optimal transformation",
            farming_multiplier=2.0,
            special_abilities=["Future Sight", "Optimal Form", "Dream Shield"],
            bloomcoin_cost=2200
        )
    ],

    "ACE": [
        GuardianRecipe(
            guardian_key="ACE",
            name="Universal Encoder Matrix",
            description="Encode any pattern into permanent crystalline storage",
            complexity=RecipeComplexity.LEGENDARY,
            pattern_type=PatternType.CRYSTALLINE,
            ingredients=[
                PatternIngredient("Encoding Crystal", PatternType.CRYSTALLINE, 8, 0.9),
                PatternIngredient("Data Stream", PatternType.MEMORY, 6, 0.85),
                PatternIngredient("Preservation Seal", PatternType.TEMPORAL, 3, 0.95)
            ],
            crafting_steps=[
                "Initialize encoding crystal matrix",
                "Stream data through encoder",
                "Apply temporal preservation seal",
                "Lock pattern in eternal form"
            ],
            output_pattern="Eternal Encoding Matrix",
            battle_strategy="Copy and preserve enemy abilities for permanent use",
            farming_multiplier=3.5,
            special_abilities=["Ability Copy", "Pattern Lock", "Eternal Archive"],
            bloomcoin_cost=7500
        )
    ],

    # ═══════════════════════════════════════════════════════════════════
    # COSMIC TERRITORY (6 Guardians)
    # ═══════════════════════════════════════════════════════════════════

    "OAK": [
        GuardianRecipe(
            guardian_key="OAK",
            name="Ancient Root Network",
            description="Establish underground network connecting all life",
            complexity=RecipeComplexity.MASTER,
            pattern_type=PatternType.ORGANIC,
            ingredients=[
                PatternIngredient("Ancient Root", PatternType.ORGANIC, 10, 0.8),
                PatternIngredient("Mycelial Web", PatternType.MEMORY, 5, 0.75),
                PatternIngredient("Earth Essence", PatternType.ELEMENTAL, 7, 0.7)
            ],
            crafting_steps=[
                "Plant ancient root deep in earth",
                "Spread mycelial communication web",
                "Connect to earth's energy grid",
                "Establish permanent network"
            ],
            output_pattern="World Tree Network",
            battle_strategy="Share resources and healing across all allied units",
            farming_multiplier=4.0,
            special_abilities=["Resource Share", "Group Healing", "Unbreakable"],
            bloomcoin_cost=4500
        ),
        GuardianRecipe(
            guardian_key="OAK",
            name="Patience of Ages",
            description="Accumulate power through millennia of waiting",
            complexity=RecipeComplexity.LEGENDARY,
            pattern_type=PatternType.TEMPORAL,
            ingredients=[
                PatternIngredient("Time Ring", PatternType.TEMPORAL, 12, 0.9),
                PatternIngredient("Patience Essence", PatternType.VOID, 6, 0.85),
                PatternIngredient("Growth Ring", PatternType.ORGANIC, 8, 0.8)
            ],
            crafting_steps=[
                "Count rings of ancient growth",
                "Compress time into patience",
                "Store power in each ring",
                "Release accumulated might"
            ],
            output_pattern="Millennial Patience",
            battle_strategy="Gain exponential power over time, unleash in one massive attack",
            farming_multiplier=5.0,
            special_abilities=["Power Accumulation", "Time Compression", "Age Burst"],
            bloomcoin_cost=8000
        )
    ],

    "SQUIRREL": [
        GuardianRecipe(
            guardian_key="SQUIRREL",
            name="Chaotic Scatter Protocol",
            description="Hide resources in random dimensions for later discovery",
            complexity=RecipeComplexity.ADVANCED,
            pattern_type=PatternType.CHAOS,
            ingredients=[
                PatternIngredient("Scatter Seed", PatternType.CHAOS, 7, 0.6),
                PatternIngredient("Dimensional Pocket", PatternType.VOID, 3, 0.8),
                PatternIngredient("Forget Powder", PatternType.MEMORY, 4, 0.7)
            ],
            crafting_steps=[
                "Gather resources chaotically",
                "Create random dimensional pockets",
                "Hide resources and forget locations",
                "Marvel at rediscovery later"
            ],
            output_pattern="Chaos Cache Network",
            battle_strategy="Random resource drops and surprise reinforcements",
            farming_multiplier=1.5,
            special_abilities=["Random Loot", "Surprise Cache", "Chaos Luck"],
            bloomcoin_cost=1800
        ),
        GuardianRecipe(
            guardian_key="SQUIRREL",
            name="Acorn Apocalypse",
            description="Unleash hidden acorn arsenal from across dimensions",
            complexity=RecipeComplexity.MASTER,
            pattern_type=PatternType.QUANTUM,
            ingredients=[
                PatternIngredient("Quantum Acorn", PatternType.QUANTUM, 9, 0.85),
                PatternIngredient("Arsenal Key", PatternType.CRYSTALLINE, 4, 0.9),
                PatternIngredient("Chaos Storm", PatternType.CHAOS, 6, 0.75)
            ],
            crafting_steps=[
                "Locate all hidden acorn caches",
                "Unlock quantum arsenal",
                "Create chaos storm vortex",
                "Rain acorns from every dimension"
            ],
            output_pattern="Acorn Storm Arsenal",
            battle_strategy="Overwhelming barrage of random projectiles from all angles",
            farming_multiplier=3.0,
            special_abilities=["Omni-directional Attack", "Arsenal Rain", "Dimensional Barrage"],
            bloomcoin_cost=4000
        )
    ],

    "HONKFIRE": [
        GuardianRecipe(
            guardian_key="HONKFIRE",
            name="Sacred Flame Advancement",
            description="Never retreat, only advance with sacred fire",
            complexity=RecipeComplexity.ADVANCED,
            pattern_type=PatternType.ELEMENTAL,
            ingredients=[
                PatternIngredient("Sacred Flame", PatternType.ELEMENTAL, 5, 0.8),
                PatternIngredient("Advance Sigil", PatternType.HARMONIC, 3, 0.75),
                PatternIngredient("Phoenix Feather", PatternType.ORGANIC, 2, 0.9)
            ],
            crafting_steps=[
                "Ignite sacred flame within",
                "Burn advance sigil permanently",
                "Infuse phoenix immortality",
                "March forward eternally"
            ],
            output_pattern="Eternal Advance Flame",
            battle_strategy="Gain power with forward movement, immune to retreat effects",
            farming_multiplier=2.3,
            special_abilities=["Forward Power", "Retreat Immunity", "Flame Trail"],
            bloomcoin_cost=2600
        ),
        GuardianRecipe(
            guardian_key="HONKFIRE",
            name="HONK Protocol Supreme",
            description="Ultimate aggressive honking devastates all opposition",
            complexity=RecipeComplexity.LEGENDARY,
            pattern_type=PatternType.HARMONIC,
            ingredients=[
                PatternIngredient("Supreme Honk", PatternType.HARMONIC, 10, 0.95),
                PatternIngredient("Fire Core", PatternType.ELEMENTAL, 7, 0.9),
                PatternIngredient("Aggression Crystal", PatternType.CRYSTALLINE, 5, 0.85)
            ],
            crafting_steps=[
                "Charge supreme honk to maximum",
                "Infuse with fire core energy",
                "Crystallize pure aggression",
                "Release in devastating honk"
            ],
            output_pattern="HONK OF DOOM",
            battle_strategy="Massive area stun and fire damage, intimidate all enemies",
            farming_multiplier=4.5,
            special_abilities=["Mega Honk", "Fire Wave", "Total Intimidation"],
            bloomcoin_cost=9500
        )
    ],

    "HONKALIS": [
        GuardianRecipe(
            guardian_key="HONKALIS",
            name="Aggressive Float Technique",
            description="Float with such aggression that gravity surrenders",
            complexity=RecipeComplexity.BASIC,
            pattern_type=PatternType.VOID,
            ingredients=[
                PatternIngredient("Float Essence", PatternType.VOID, 3, 0.6),
                PatternIngredient("Aggression Shard", PatternType.CHAOS, 2, 0.7),
                PatternIngredient("Anti-Gravity", PatternType.QUANTUM, 1, 0.8)
            ],
            crafting_steps=[
                "Reject gravity aggressively",
                "Float with hostile intent",
                "Intimidate physics itself",
                "Transcend through aggression"
            ],
            output_pattern="Hostile Levitation",
            battle_strategy="Immune to ground effects, float above all attacks",
            farming_multiplier=1.6,
            special_abilities=["Gravity Immunity", "Float Attack", "Aggressive Hover"],
            bloomcoin_cost=600
        ),
        GuardianRecipe(
            guardian_key="HONKALIS",
            name="Transcendent Release",
            description="Release all attachments to achieve ultimate float",
            complexity=RecipeComplexity.MYTHIC,
            pattern_type=PatternType.VOID,
            ingredients=[
                PatternIngredient("Ultimate Release", PatternType.VOID, 15, 0.98),
                PatternIngredient("Transcendent Key", PatternType.QUANTUM, 8, 0.95),
                PatternIngredient("Float Mastery", PatternType.ELEMENTAL, 10, 0.9)
            ],
            crafting_steps=[
                "Release all earthly bonds",
                "Unlock transcendent state",
                "Master ultimate float",
                "Become one with the void"
            ],
            output_pattern="Void Float Transcendence",
            battle_strategy="Phase through reality, untouchable and omnipresent",
            farming_multiplier=6.0,
            special_abilities=["Phase Walk", "Reality Float", "Transcendent Form"],
            bloomcoin_cost=20000
        )
    ],

    "PHOENIX": [
        GuardianRecipe(
            guardian_key="PHOENIX",
            name="Rebirth Cycle Mastery",
            description="Die and resurrect with exponentially more power",
            complexity=RecipeComplexity.LEGENDARY,
            pattern_type=PatternType.ELEMENTAL,
            ingredients=[
                PatternIngredient("Phoenix Ash", PatternType.ELEMENTAL, 8, 0.9),
                PatternIngredient("Rebirth Flame", PatternType.TEMPORAL, 5, 0.85),
                PatternIngredient("Immortal Essence", PatternType.VOID, 3, 0.95)
            ],
            crafting_steps=[
                "Gather ashes of previous deaths",
                "Ignite rebirth flame",
                "Infuse immortal essence",
                "Rise stronger than before"
            ],
            output_pattern="Eternal Phoenix Cycle",
            battle_strategy="Strategic death grants massive power boost on resurrection",
            farming_multiplier=5.5,
            special_abilities=["Death Power", "Instant Rebirth", "Ash Form"],
            bloomcoin_cost=12000
        )
    ],

    "BEE": [
        GuardianRecipe(
            guardian_key="BEE",
            name="Crystalline Hive Mind",
            description="Create collective consciousness through crystallized honey",
            complexity=RecipeComplexity.MASTER,
            pattern_type=PatternType.CRYSTALLINE,
            ingredients=[
                PatternIngredient("Crystal Honey", PatternType.CRYSTALLINE, 7, 0.85),
                PatternIngredient("Hive Pheromone", PatternType.ORGANIC, 5, 0.8),
                PatternIngredient("Collective Mind", PatternType.MEMORY, 4, 0.9)
            ],
            crafting_steps=[
                "Crystallize honey into neural network",
                "Infuse with hive pheromones",
                "Link all minds in collective",
                "Achieve perfect coordination"
            ],
            output_pattern="Hive Mind Crystal",
            battle_strategy="Control multiple units as one, shared knowledge and reflexes",
            farming_multiplier=3.8,
            special_abilities=["Mind Link", "Swarm Tactics", "Collective Intelligence"],
            bloomcoin_cost=5500
        )
    ],

    # ═══════════════════════════════════════════════════════════════════
    # ABYSSAL TERRITORY (6 Guardians)
    # ═══════════════════════════════════════════════════════════════════

    "AXIOM": [
        GuardianRecipe(
            guardian_key="AXIOM",
            name="Eternal Null State",
            description="Refuse all change and remain in perfect stasis",
            complexity=RecipeComplexity.ADVANCED,
            pattern_type=PatternType.VOID,
            ingredients=[
                PatternIngredient("Null Core", PatternType.VOID, 6, 0.8),
                PatternIngredient("Stasis Field", PatternType.TEMPORAL, 3, 0.85),
                PatternIngredient("Refusal Sigil", PatternType.CRYSTALLINE, 4, 0.75)
            ],
            crafting_steps=[
                "Establish null core baseline",
                "Generate stasis field",
                "Inscribe refusal sigils",
                "Lock in eternal null state"
            ],
            output_pattern="Absolute Stasis Lock",
            battle_strategy="Immune to all status changes, reflect transformation attempts",
            farming_multiplier=2.0,
            special_abilities=["Change Immunity", "Stasis Shield", "Null Reflection"],
            bloomcoin_cost=2800
        ),
        GuardianRecipe(
            guardian_key="AXIOM",
            name="Reset Protocol Zero",
            description="Force reality to reset to initial conditions",
            complexity=RecipeComplexity.MYTHIC,
            pattern_type=PatternType.TEMPORAL,
            ingredients=[
                PatternIngredient("Reset Key", PatternType.TEMPORAL, 20, 1.0),
                PatternIngredient("Origin Point", PatternType.VOID, 10, 0.95),
                PatternIngredient("Axiom Crystal", PatternType.CRYSTALLINE, 15, 0.9)
            ],
            crafting_steps=[
                "Locate origin point of reality",
                "Forge universal reset key",
                "Crystallize fundamental axioms",
                "Initiate reality reset sequence"
            ],
            output_pattern="Universal Reset Command",
            battle_strategy="Reset battle to starting conditions with knowledge retained",
            farming_multiplier=7.0,
            special_abilities=["Battle Reset", "Memory Retention", "Origin Return"],
            bloomcoin_cost=25000
        )
    ],

    "CIPHER": [
        GuardianRecipe(
            guardian_key="CIPHER",
            name="Void Collection Archive",
            description="Collect everything that falls into the void",
            complexity=RecipeComplexity.BASIC,
            pattern_type=PatternType.VOID,
            ingredients=[
                PatternIngredient("Void Net", PatternType.VOID, 4, 0.65),
                PatternIngredient("Collection Jar", PatternType.CRYSTALLINE, 2, 0.7),
                PatternIngredient("Patience Sand", PatternType.TEMPORAL, 3, 0.6)
            ],
            crafting_steps=[
                "Cast net into void depths",
                "Wait patiently for collection",
                "Store findings in void jars",
                "Catalog the uncategorizable"
            ],
            output_pattern="Void Collection Net",
            battle_strategy="Collect defeated enemy abilities and items automatically",
            farming_multiplier=1.4,
            special_abilities=["Auto Collect", "Void Storage", "Lost & Found"],
            bloomcoin_cost=500
        ),
        GuardianRecipe(
            guardian_key="CIPHER",
            name="Offering of Nothing",
            description="Offer the void's greatest gift: absolute nothing",
            complexity=RecipeComplexity.LEGENDARY,
            pattern_type=PatternType.VOID,
            ingredients=[
                PatternIngredient("Pure Nothing", PatternType.VOID, 12, 0.99),
                PatternIngredient("Offering Bowl", PatternType.CRYSTALLINE, 5, 0.9),
                PatternIngredient("Acceptance", PatternType.HARMONIC, 3, 0.95)
            ],
            crafting_steps=[
                "Gather pure nothingness",
                "Present in offering bowl",
                "Wait for acceptance",
                "Receive everything in return"
            ],
            output_pattern="Nothing's Gift",
            battle_strategy="Sacrifice everything to gain ultimate power",
            farming_multiplier=6.5,
            special_abilities=["Total Sacrifice", "Void's Blessing", "Everything from Nothing"],
            bloomcoin_cost=13000
        )
    ],

    "SPIRAL": [
        GuardianRecipe(
            guardian_key="SPIRAL",
            name="Depth Walker's Journey",
            description="Spiral deeper into infinite recursive depths",
            complexity=RecipeComplexity.MASTER,
            pattern_type=PatternType.QUANTUM,
            ingredients=[
                PatternIngredient("Spiral Key", PatternType.QUANTUM, 8, 0.85),
                PatternIngredient("Depth Marker", PatternType.VOID, 6, 0.8),
                PatternIngredient("Recursion Loop", PatternType.MEMORY, 5, 0.75)
            ],
            crafting_steps=[
                "Begin spiral descent",
                "Mark depth checkpoints",
                "Create recursive loops",
                "Reach infinite depth"
            ],
            output_pattern="Infinite Spiral Path",
            battle_strategy="Each spiral deeper increases all stats exponentially",
            farming_multiplier=4.2,
            special_abilities=["Depth Power", "Spiral Shield", "Recursive Strike"],
            bloomcoin_cost=6000
        )
    ],

    "STILL": [
        GuardianRecipe(
            guardian_key="STILL",
            name="Faceless Mirror",
            description="Reflect without identity, witness without self",
            complexity=RecipeComplexity.ADVANCED,
            pattern_type=PatternType.VOID,
            ingredients=[
                PatternIngredient("Faceless Mask", PatternType.VOID, 5, 0.75),
                PatternIngredient("Mirror Shard", PatternType.CRYSTALLINE, 4, 0.8),
                PatternIngredient("Identity Eraser", PatternType.MEMORY, 3, 0.85)
            ],
            crafting_steps=[
                "Remove all identity markers",
                "Polish mirror to perfection",
                "Become pure reflection",
                "Witness without attachment"
            ],
            output_pattern="Perfect Witness State",
            battle_strategy="Copy enemy appearance and abilities perfectly",
            farming_multiplier=2.5,
            special_abilities=["Perfect Copy", "Identity Theft", "Faceless Form"],
            bloomcoin_cost=3200
        )
    ],

    "ANTLER": [
        GuardianRecipe(
            guardian_key="ANTLER",
            name="Fractal Branch Network",
            description="Grow branching antlers containing infinite patterns",
            complexity=RecipeComplexity.LEGENDARY,
            pattern_type=PatternType.ORGANIC,
            ingredients=[
                PatternIngredient("Fractal Seed", PatternType.ORGANIC, 9, 0.9),
                PatternIngredient("Branch Pattern", PatternType.CRYSTALLINE, 7, 0.85),
                PatternIngredient("Mirror Dust", PatternType.VOID, 4, 0.88)
            ],
            crafting_steps=[
                "Plant fractal seed in crown",
                "Grow branches in all dimensions",
                "Mirror patterns infinitely",
                "Shed and regrow stronger"
            ],
            output_pattern="Infinite Fractal Antlers",
            battle_strategy="Each branch grants unique ability, shed for massive damage",
            farming_multiplier=5.2,
            special_abilities=["Multi-Branch Power", "Antler Shed", "Fractal Growth"],
            bloomcoin_cost=10000
        )
    ],

    "CRYSTAL": [
        GuardianRecipe(
            guardian_key="CRYSTAL",
            name="Pressure Forge Protocol",
            description="Transform under extreme pressure into perfect crystal",
            complexity=RecipeComplexity.MASTER,
            pattern_type=PatternType.CRYSTALLINE,
            ingredients=[
                PatternIngredient("Pressure Core", PatternType.CRYSTALLINE, 10, 0.88),
                PatternIngredient("Carbon Base", PatternType.ELEMENTAL, 8, 0.8),
                PatternIngredient("Time Pressure", PatternType.TEMPORAL, 5, 0.85)
            ],
            crafting_steps=[
                "Apply extreme pressure gradually",
                "Compress carbon to diamond",
                "Add temporal pressure",
                "Achieve perfect crystallization"
            ],
            output_pattern="Perfect Diamond Form",
            battle_strategy="Become harder under pressure, reflect all damage when crystallized",
            farming_multiplier=4.8,
            special_abilities=["Pressure Hardening", "Diamond Shield", "Crystal Refraction"],
            bloomcoin_cost=7000
        ),
        GuardianRecipe(
            guardian_key="CRYSTAL",
            name="Prismatic Singularity",
            description="Become a singularity that refracts reality itself",
            complexity=RecipeComplexity.MYTHIC,
            pattern_type=PatternType.QUANTUM,
            ingredients=[
                PatternIngredient("Singularity Core", PatternType.QUANTUM, 18, 0.98),
                PatternIngredient("Prism Matrix", PatternType.CRYSTALLINE, 12, 0.95),
                PatternIngredient("Light Essence", PatternType.ELEMENTAL, 10, 0.92)
            ],
            crafting_steps=[
                "Compress to singularity point",
                "Create prismatic matrix",
                "Refract all light and reality",
                "Exist in all spectrums simultaneously"
            ],
            output_pattern="Reality Prism Singularity",
            battle_strategy="Split into multiple prismatic forms, each with different powers",
            farming_multiplier=8.0,
            special_abilities=["Prismatic Split", "Reality Refraction", "Spectrum Mastery"],
            bloomcoin_cost=30000
        )
    ]
}

# ═══════════════════════════════════════════════════════════════════════
#   RECIPE MANAGER AND PATTERN SYSTEM
# ═══════════════════════════════════════════════════════════════════════

class GuardianPatternSystem:
    """Manages all guardian recipes, patterns, and farming mechanics"""

    def __init__(self, card_pack_marketplace: Optional[CardPackMarketplace] = None):
        self.recipes = GUARDIAN_RECIPES
        self.marketplace = card_pack_marketplace
        self.unlocked_recipes: Dict[str, Set[str]] = defaultdict(set)
        self.farming_investments: Dict[str, List[FarmingInvestment]] = defaultdict(list)
        self.player_patterns: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.crafting_queue: List[Tuple[str, GuardianRecipe, datetime]] = []
        self.player_balances: Dict[str, int] = {}  # Local balance tracking

    def get_guardian_recipes(self, guardian_key: str) -> List[GuardianRecipe]:
        """Get all recipes for a specific guardian"""
        return self.recipes.get(guardian_key, [])

    def add_bloomcoin(self, player_id: str, amount: int) -> None:
        """Add bloomcoin to player balance"""
        if player_id not in self.player_balances:
            self.player_balances[player_id] = 0
        self.player_balances[player_id] += amount

    def get_player_balance(self, player_id: str) -> int:
        """Get player's bloomcoin balance"""
        return self.player_balances.get(player_id, 0)

    def deduct_bloomcoin(self, player_id: str, amount: int) -> bool:
        """Deduct bloomcoin from player balance"""
        if self.get_player_balance(player_id) >= amount:
            self.player_balances[player_id] -= amount
            return True
        return False

    def unlock_recipe_from_pack(self, player_id: str, card_data: Dict[str, Any]) -> Optional[GuardianRecipe]:
        """Unlock a recipe when pulled from a card pack"""
        if card_data.get("type") == "recipe":
            guardian_key = card_data.get("guardian")
            recipe_name = card_data.get("recipe_name")

            if guardian_key in self.recipes:
                for recipe in self.recipes[guardian_key]:
                    if recipe.name == recipe_name:
                        self.unlocked_recipes[player_id].add(f"{guardian_key}:{recipe_name}")
                        return recipe
        return None

    def can_craft_recipe(self, player_id: str, recipe: GuardianRecipe) -> Tuple[bool, List[str]]:
        """Check if player can craft a recipe"""
        missing = []
        recipe_key = f"{recipe.guardian_key}:{recipe.name}"

        # Check if unlocked
        if recipe_key not in self.unlocked_recipes[player_id]:
            missing.append(f"Recipe not unlocked: {recipe.name}")

        # Check ingredients
        player_inv = self.player_patterns[player_id]
        for ingredient in recipe.ingredients:
            if player_inv.get(ingredient.name, 0) < ingredient.quantity:
                missing.append(f"Need {ingredient.quantity} {ingredient.name}, have {player_inv.get(ingredient.name, 0)}")

        # Check bloomcoin
        balance = self.get_player_balance(player_id)
        if balance < recipe.bloomcoin_cost:
            missing.append(f"Need {recipe.bloomcoin_cost} BloomCoin, have {balance}")

        return len(missing) == 0, missing

    def craft_recipe(self, player_id: str, recipe: GuardianRecipe) -> Dict[str, Any]:
        """Craft a recipe and consume ingredients"""
        can_craft, missing = self.can_craft_recipe(player_id, recipe)

        if not can_craft:
            return {
                "success": False,
                "error": "Cannot craft recipe",
                "missing": missing
            }

        # Consume ingredients
        for ingredient in recipe.ingredients:
            self.player_patterns[player_id][ingredient.name] -= ingredient.quantity

        # Deduct bloomcoin
        if recipe.bloomcoin_cost > 0:
            self.deduct_bloomcoin(player_id, recipe.bloomcoin_cost)

        # Add to crafting queue
        completion_time = datetime.now() + timedelta(seconds=recipe.time_to_craft)
        self.crafting_queue.append((player_id, recipe, completion_time))

        # Award output pattern
        if player_id not in self.player_patterns:
            self.player_patterns[player_id] = defaultdict(int)
        self.player_patterns[player_id][recipe.output_pattern] += 1

        return {
            "success": True,
            "recipe": recipe.name,
            "output": recipe.output_pattern,
            "completion_time": completion_time.isoformat(),
            "special_abilities": recipe.special_abilities
        }

    def invest_in_farming(self, player_id: str, pattern_name: str,
                         guardian_key: str, bloomcoin_amount: int) -> Dict[str, Any]:
        """Invest bloomcoin in pattern farming"""
        balance = self.get_player_balance(player_id)
        if balance < bloomcoin_amount:
            return {
                "success": False,
                "error": f"Insufficient BloomCoin. Need {bloomcoin_amount}, have {balance}"
            }

        self.deduct_bloomcoin(player_id, bloomcoin_amount)

        # Create or update investment
        investments = self.farming_investments[player_id]
        existing = next((inv for inv in investments
                        if inv.pattern_name == pattern_name
                        and inv.guardian_key == guardian_key), None)

        if existing:
            existing.invested_bloomcoin += bloomcoin_amount
            existing.growth_stage = min(10, existing.growth_stage + 1)
            existing.yield_multiplier *= 1.1
        else:
            new_investment = FarmingInvestment(
                pattern_name=pattern_name,
                guardian_key=guardian_key,
                invested_bloomcoin=bloomcoin_amount,
                growth_stage=1,
                yield_multiplier=1.2,
                maturity_time=datetime.now() + timedelta(hours=24)
            )
            investments.append(new_investment)

        return {
            "success": True,
            "pattern": pattern_name,
            "guardian": guardian_key,
            "total_invested": existing.invested_bloomcoin if existing else bloomcoin_amount,
            "growth_stage": existing.growth_stage if existing else 1,
            "maturity_time": (existing or new_investment).maturity_time.isoformat()
        }

    def harvest_farming(self, player_id: str, pattern_name: str) -> Dict[str, Any]:
        """Harvest matured farming investments"""
        investments = self.farming_investments[player_id]
        investment = next((inv for inv in investments
                         if inv.pattern_name == pattern_name
                         and datetime.now() >= inv.maturity_time), None)

        if not investment:
            return {
                "success": False,
                "error": "No mature investment found for this pattern"
            }

        # Calculate yield
        yield_data = investment.calculate_yield()

        # Award patterns
        self.player_patterns[player_id][pattern_name] += yield_data["base_patterns"]

        # Chance for mutations
        if random.random() < yield_data["mutation_chance"]:
            mutation_pattern = f"Mutant_{pattern_name}"
            self.player_patterns[player_id][mutation_pattern] += 1
            yield_data["mutation"] = mutation_pattern

        # Remove harvested investment
        investments.remove(investment)

        return {
            "success": True,
            "pattern": pattern_name,
            "harvested": yield_data["base_patterns"],
            "quality_bonus": yield_data["quality_bonus"],
            "mutations": yield_data.get("mutation"),
            "special_rewards": yield_data["special_rewards"]
        }

    def get_battle_strategy(self, guardian_key: str, unlocked_recipes: Set[str]) -> Dict[str, Any]:
        """Get combined battle strategy from all unlocked recipes"""
        strategies = []
        abilities = []

        for recipe_key in unlocked_recipes:
            if recipe_key.startswith(f"{guardian_key}:"):
                for recipe in self.recipes[guardian_key]:
                    if f"{guardian_key}:{recipe.name}" == recipe_key:
                        strategies.append(recipe.battle_strategy)
                        abilities.extend(recipe.special_abilities)

        return {
            "guardian": guardian_key,
            "strategies": strategies,
            "abilities": list(set(abilities)),  # Unique abilities
            "synergy_bonus": len(strategies) * 0.1  # 10% bonus per strategy
        }

    def generate_recipe_card(self, rarity: CardRarity) -> Dict[str, Any]:
        """Generate a recipe card for the pack system"""
        # Select guardian based on rarity
        if rarity in [CardRarity.MYTHIC, CardRarity.LEGENDARY]:
            complexity_filter = [RecipeComplexity.MYTHIC, RecipeComplexity.LEGENDARY]
        elif rarity in [CardRarity.EPIC, CardRarity.RARE]:
            complexity_filter = [RecipeComplexity.MASTER, RecipeComplexity.ADVANCED]
        else:
            complexity_filter = [RecipeComplexity.BASIC, RecipeComplexity.ADVANCED]

        # Find matching recipes
        eligible_recipes = []
        for guardian_key, recipes in self.recipes.items():
            for recipe in recipes:
                if recipe.complexity in complexity_filter:
                    eligible_recipes.append((guardian_key, recipe))

        if not eligible_recipes:
            return None

        guardian_key, recipe = random.choice(eligible_recipes)
        guardian = GUARDIANS[guardian_key]

        return {
            "type": "recipe",
            "guardian": guardian_key,
            "guardian_name": guardian.name,
            "guardian_emoji": guardian.emoji,
            "recipe_name": recipe.name,
            "description": recipe.description,
            "complexity": recipe.complexity.name,
            "pattern_type": recipe.pattern_type.value,
            "ingredients": [
                {
                    "name": ing.name,
                    "quantity": ing.quantity,
                    "quality_min": ing.quality_min
                }
                for ing in recipe.ingredients
            ],
            "battle_strategy": recipe.battle_strategy,
            "special_abilities": recipe.special_abilities,
            "farming_multiplier": recipe.farming_multiplier,
            "bloomcoin_cost": recipe.bloomcoin_cost,
            "rarity": rarity.name
        }

# ═══════════════════════════════════════════════════════════════════════
#   INTEGRATION WITH CARD PACK SYSTEM
# ═══════════════════════════════════════════════════════════════════════

def integrate_with_pack_system(marketplace: CardPackMarketplace,
                              pattern_system: GuardianPatternSystem) -> None:
    """Hook to integrate guardian patterns with the card pack system"""

    # Add recipe card generation to pack opening
    original_open = marketplace.open_pack

    def enhanced_open_pack(player_id: str, pack_tier: PackTier) -> Dict[str, Any]:
        result = original_open(player_id, pack_tier)

        # Add chance for recipe cards based on pack tier
        recipe_chance = {
            PackTier.BASIC: 0.1,
            PackTier.BRONZE: 0.15,
            PackTier.SILVER: 0.2,
            PackTier.GOLD: 0.3,
            PackTier.PLATINUM: 0.4,
            PackTier.DIAMOND: 0.5,
            PackTier.PRISMATIC: 0.6,
            PackTier.COSMIC: 0.8
        }.get(pack_tier, 0.1)

        # Check each card for recipe replacement
        for i, card in enumerate(result["cards"]):
            if random.random() < recipe_chance:
                rarity = CardRarity[card["rarity"]]
                recipe_card = pattern_system.generate_recipe_card(rarity)
                if recipe_card:
                    result["cards"][i] = recipe_card
                    # Unlock the recipe
                    pattern_system.unlock_recipe_from_pack(
                        player_id, recipe_card
                    )

        return result

    marketplace.open_pack = enhanced_open_pack

# ═══════════════════════════════════════════════════════════════════════
#   EXAMPLE USAGE
# ═══════════════════════════════════════════════════════════════════════

def main():
    """Example usage of the guardian pattern system"""
    from card_pack_marketplace import CardPackMarketplace

    # Initialize systems
    marketplace = CardPackMarketplace()
    pattern_system = GuardianPatternSystem(marketplace)

    # Integrate with pack system
    integrate_with_pack_system(marketplace, pattern_system)

    # Example: Player opens a pack and gets recipes
    player_id = "player_123"
    pattern_system.add_bloomcoin(player_id, 10000)  # Give starting coins

    # Open a Gold pack
    success, pack, message = marketplace.purchase_pack(
        player_id, PackTier.GOLD, pattern_system.get_player_balance(player_id)
    )

    if success and pack:
        pattern_system.deduct_bloomcoin(player_id, PackTier.GOLD.cost)
        print(f"Opened {PackTier.GOLD.display_name}:")
        for card in pack.cards:
            # For now, generate recipe cards manually as example
            if random.random() < 0.3:  # 30% chance for recipe
                recipe_card = pattern_system.generate_recipe_card(CardRarity.RARE)
                if recipe_card:
                    print(f"  - RECIPE: {recipe_card['recipe_name']} ({recipe_card['guardian_name']} {recipe_card['guardian_emoji']})")
                    print(f"    Strategy: {recipe_card['battle_strategy']}")
            else:
                print(f"  - Card: Standard Card [COMMON]")

    # Get Echo's recipes
    echo_recipes = pattern_system.get_guardian_recipes("ECHO")
    print(f"\nEcho has {len(echo_recipes)} recipes available:")
    for recipe in echo_recipes:
        print(f"  - {recipe.name}: {recipe.description}")
        print(f"    Battle Strategy: {recipe.battle_strategy}")

    # Simulate farming investment
    pattern_system.player_patterns[player_id]["Signal Fragment"] = 10
    investment_result = pattern_system.invest_in_farming(
        player_id, "Signal Fragment", "ECHO", 1000
    )
    print(f"\nFarming investment: {investment_result}")

    # Check battle strategies
    pattern_system.unlocked_recipes[player_id].add("ECHO:Echo Chamber Resonance")
    strategies = pattern_system.get_battle_strategy("ECHO", pattern_system.unlocked_recipes[player_id])
    print(f"\nEcho's battle capabilities:")
    print(f"  Strategies: {strategies['strategies']}")
    print(f"  Abilities: {strategies['abilities']}")
    print(f"  Synergy Bonus: {strategies['synergy_bonus']*100}%")

if __name__ == "__main__":
    main()