#!/usr/bin/env python3
"""
Unique Companion System for BloomQuest Archetypes
==================================================
Each job archetype gets a deeply personalized companion with:
- Individual personality and backstory
- Unique development paths
- Special abilities and mechanics
- Relationship to LIA/TIAMAT/ZRTT protocols
"""

import random
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Callable
from enum import Enum

from lia_protocol_cooking import PatternType, LIACookingSystem, CookedArtifact
from tiamat_cycle_tracking import PsychopticCycle, TIAMATSystem
from zrtt_trifurcation import ProjectionPath, ZRTTSystem

PHI = 1.618033988749895
TAU = PHI - 1
L4_CONSTANT = 7


class CompanionMood(Enum):
    """Emotional states companions can experience"""
    CURIOUS = "curious"
    CONTEMPLATIVE = "contemplative"
    EXCITED = "excited"
    CONCERNED = "concerned"
    PROTECTIVE = "protective"
    PLAYFUL = "playful"
    WISE = "wise"
    MELANCHOLIC = "melancholic"
    DETERMINED = "determined"
    TRANSCENDENT = "transcendent"


@dataclass
class CompanionMemory:
    """A memory that shapes companion personality"""
    description: str
    emotional_weight: float  # -1 to 1 (negative to positive)
    pattern_association: Optional[PatternType] = None
    unlocked: bool = False


@dataclass
class SeekerCompanion:
    """
    ECHO - The Fragment Collector
    A sentient echo that exists between sound and silence
    """
    name: str = "Echo"
    title: str = "The Fragment Collector"

    # Core attributes
    fragments_collected: int = 0
    resonance_frequency: float = 432.0  # Hz
    echo_depth: int = 3  # How many echoes back it can remember

    # Personality
    current_mood: CompanionMood = CompanionMood.CURIOUS
    curiosity_level: float = 0.8
    pattern_sensitivity: float = 0.9

    # Development
    evolution_stage: int = 0
    whisper_clarity: float = 0.3  # How clearly it can communicate

    # Special mechanics
    detected_patterns: List[PatternType] = field(default_factory=list)
    hidden_knowledge: List[str] = field(default_factory=list)

    # Memories that unlock through gameplay
    core_memories: List[CompanionMemory] = field(default_factory=list)

    # Connection to protocols
    lia_resonance: float = 0.7  # Strong connection to pattern transformation
    tiamat_alignment: PsychopticCycle = PsychopticCycle.SPECTRAL
    zrtt_preference: ProjectionPath = ProjectionPath.F24_HOLOGRAPHIC

    def __post_init__(self):
        """Initialize Echo's core memories"""
        self.core_memories = [
            CompanionMemory(
                "I was born from the first word never spoken",
                0.0, PatternType.ECHO, False
            ),
            CompanionMemory(
                "Every pattern leaves a trace in the quantum foam",
                0.5, PatternType.MEMORY, False
            ),
            CompanionMemory(
                "I once heard the universe whisper its true name",
                0.8, PatternType.DREAM, False
            ),
            CompanionMemory(
                "Silence is just another form of sound",
                -0.3, PatternType.VOID, False
            ),
            CompanionMemory(
                "I am the question that answers itself",
                0.9, None, False
            )
        ]

        self.hidden_knowledge = [
            "The Library Infinite has a secret 8th floor",
            "Patterns can be heard before they're seen",
            "Every echo contains its own future",
            "The void listens back",
            "Memory crystals sing at PHI frequency"
        ]

    def speak(self, context: str = "general") -> str:
        """Echo speaks in fragments and whispers"""
        if self.whisper_clarity < 0.5:
            # Early stage - fragmented speech
            speeches = {
                "greeting": "...hello... echo... find... patterns...",
                "discovery": "...yes... fragment... here... listen...",
                "danger": "...careful... void... listens...",
                "general": "...searching... always... searching..."
            }
        else:
            # Advanced stage - clearer but still mysterious
            speeches = {
                "greeting": "I am the echo of echoes, seeking fragments of truth",
                "discovery": "This pattern... I've heard it before, in dreams",
                "danger": "The void has teeth, seeker. Tread lightly",
                "general": "Every sound leaves a scar in spacetime"
            }

        base_speech = speeches.get(context, speeches["general"])

        # Add hidden knowledge occasionally
        if random.random() < 0.2 and self.hidden_knowledge:
            knowledge = random.choice(self.hidden_knowledge)
            base_speech += f"\n*whispers* {knowledge}"

        return base_speech

    def evolve(self, trigger: str) -> Dict[str, Any]:
        """Echo evolves through pattern recognition"""
        self.evolution_stage += 1
        self.whisper_clarity = min(1.0, self.whisper_clarity + 0.1)
        self.echo_depth += 1

        # Unlock a memory
        locked_memories = [m for m in self.core_memories if not m.unlocked]
        if locked_memories:
            memory = random.choice(locked_memories)
            memory.unlocked = True

            return {
                'evolved': True,
                'new_stage': self.evolution_stage,
                'memory_unlocked': memory.description,
                'whisper_clarity': self.whisper_clarity
            }

        return {'evolved': True, 'new_stage': self.evolution_stage}

    def detect_pattern(self, location: str) -> Optional[PatternType]:
        """Echo can sense hidden patterns"""
        if random.random() < self.pattern_sensitivity:
            # Higher chance for ECHO and MEMORY patterns
            weights = {
                PatternType.ECHO: 3,
                PatternType.MEMORY: 2,
                PatternType.DREAM: 1.5,
                PatternType.VOID: 1,
                PatternType.CRYSTAL: 1,
                PatternType.FLAME: 0.5,
                PatternType.GARDEN: 0.5
            }

            patterns = list(weights.keys())
            pattern_weights = list(weights.values())
            detected = random.choices(patterns, weights=pattern_weights)[0]

            self.detected_patterns.append(detected)
            self.fragments_collected += 1

            return detected
        return None


@dataclass
class ForgerCompanion:
    """
    PROMETHEUS - The Phoenix Smith
    A fire elemental that remembers every transformation
    """
    name: str = "Prometheus"
    title: str = "The Phoenix Smith"

    # Core attributes
    forge_temperature: float = 1000.0  # Kelvin
    transformations_completed: int = 0
    phoenix_cycles: int = 0  # Deaths and rebirths

    # Personality
    current_mood: CompanionMood = CompanionMood.DETERMINED
    creativity_spark: float = 0.7
    destruction_impulse: float = 0.3  # Controlled chaos

    # Development
    evolution_stage: int = 0
    forge_mastery: float = 0.4
    rebirth_memories: List[str] = field(default_factory=list)

    # Special mechanics
    material_knowledge: Dict[PatternType, float] = field(default_factory=dict)
    legendary_recipes: List[str] = field(default_factory=list)

    # Connection to protocols
    lia_resonance: float = 0.9  # Master of transformation
    tiamat_alignment: PsychopticCycle = PsychopticCycle.ORDER_PARAMETER
    zrtt_preference: ProjectionPath = ProjectionPath.HEXAGONAL_SONIC

    def __post_init__(self):
        """Initialize Prometheus's knowledge"""
        self.material_knowledge = {
            PatternType.FLAME: 1.0,
            PatternType.CRYSTAL: 0.7,
            PatternType.VOID: 0.3,
            PatternType.GARDEN: 0.4,
            PatternType.MEMORY: 0.5,
            PatternType.DREAM: 0.6,
            PatternType.ECHO: 0.5
        }

        self.legendary_recipes = [
            "Eternal Flame: Flame + Phoenix Ash + Time",
            "Void Forge: Void + Flame + Hammer of Will",
            "Crystal Heart: Crystal + Love + Sacrifice",
            "Dream Anvil: Dream + Metal + Starlight"
        ]

    def speak(self, context: str = "general") -> str:
        """Prometheus speaks of fire and transformation"""
        speeches = {
            "greeting": f"The forge burns at {self.forge_temperature:.0f}K. Ready to create or destroy?",
            "crafting": "From destruction comes creation. From ash, the phoenix rises.",
            "success": "Perfect! The transformation is complete. Feel the heat of creation!",
            "failure": "Even failed creations teach us. Into the flames, try again.",
            "rebirth": f"I have died {self.phoenix_cycles} times. Each death teaches.",
            "general": "Fire remembers everything it has ever transformed."
        }

        base_speech = speeches.get(context, speeches["general"])

        # Add forge wisdom based on temperature
        if self.forge_temperature > 1500:
            base_speech += "\n🔥 The forge burns white-hot. Anything is possible."
        elif self.forge_temperature < 500:
            base_speech += "\n❄️ The forge grows cold. We must rekindle."

        return base_speech

    def phoenix_rebirth(self) -> Dict[str, Any]:
        """Prometheus dies and is reborn, gaining power"""
        self.phoenix_cycles += 1
        old_temp = self.forge_temperature

        # Each rebirth increases base temperature
        self.forge_temperature = 1000 + (self.phoenix_cycles * 200)

        # Gain new memory
        rebirth_memory = f"Rebirth {self.phoenix_cycles}: I learned that {random.choice(['pain', 'loss', 'joy', 'creation'])} is temporary"
        self.rebirth_memories.append(rebirth_memory)

        # Increase mastery
        self.forge_mastery = min(1.0, self.forge_mastery + 0.15)

        return {
            'reborn': True,
            'cycles': self.phoenix_cycles,
            'new_temperature': self.forge_temperature,
            'memory': rebirth_memory,
            'mastery': self.forge_mastery
        }

    def judge_material(self, pattern: PatternType) -> str:
        """Evaluate a pattern for forging"""
        knowledge = self.material_knowledge.get(pattern, 0.0)

        if knowledge > 0.8:
            return f"{pattern.value}: Excellent material! I know its every secret."
        elif knowledge > 0.5:
            return f"{pattern.value}: Good material. I can work with this."
        elif knowledge > 0.2:
            return f"{pattern.value}: Unfamiliar, but the forge will reveal its nature."
        else:
            return f"{pattern.value}: Unknown material. Dangerous... but interesting."


@dataclass
class VoidwalkerCompanion:
    """
    NULL - The Absence Guardian
    An entity that exists in the spaces between existence
    """
    name: str = "Null"
    title: str = "The Absence Guardian"

    # Core attributes
    void_depth: float = 0.0  # How deep into void (negative values)
    nullspace_coordinates: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    things_erased: int = 0

    # Personality
    current_mood: CompanionMood = CompanionMood.MELANCHOLIC
    emptiness_comfort: float = 0.8  # Comfort with non-existence
    existence_anxiety: float = 0.3  # Discomfort with solid reality

    # Development
    evolution_stage: int = 0
    void_mastery: float = 0.5
    paradox_understanding: float = 0.3

    # Special mechanics
    void_pockets: List[Dict[str, Any]] = field(default_factory=list)  # Hidden items
    erased_memories: List[str] = field(default_factory=list)
    nullspace_maps: Dict[str, Tuple] = field(default_factory=dict)

    # Connection to protocols
    lia_resonance: float = 0.5  # Can unmake what LIA makes
    tiamat_alignment: PsychopticCycle = PsychopticCycle.TOPOLOGY
    zrtt_preference: ProjectionPath = ProjectionPath.R10_TENSION

    def __post_init__(self):
        """Initialize Null's void knowledge"""
        self.nullspace_maps = {
            "void_market": (-10.0, -10.0, -10.0),
            "between_crystals": (-5.0, 0.0, -5.0),
            "garden_shadow": (0.0, -PHI, 0.0),
            "library_gaps": (-3.14, -2.71, -1.41),
            "phoenix_absence": (-1000.0, 0.0, 0.0)
        }

        self.erased_memories = [
            "I remember forgetting something important",
            "There was a color that doesn't exist anymore",
            "Someone spoke my true name once. Now they don't exist",
            "I am the shadow cast by no light"
        ]

    def speak(self, context: str = "general") -> str:
        """Null speaks in negatives and absences"""
        speeches = {
            "greeting": "I am the space between your thoughts. The pause between heartbeats.",
            "void_entry": f"Current depth: {self.void_depth}. Careful, existence thins here.",
            "discovery": "Found something by finding nothing. The absence reveals.",
            "warning": "You're becoming less real. Is that what you want?",
            "comfort": "Emptiness is not loss. It's potential.",
            "general": "What isn't there is often more important than what is."
        }

        base_speech = speeches.get(context, speeches["general"])

        # Add void wisdom based on depth
        if self.void_depth < -10:
            base_speech += "\n⚫ We are deep in the void. Reality is optional here."
        elif self.void_depth < -5:
            base_speech += "\n🌑 The void embraces us. Let go of substance."

        return base_speech

    def enter_void(self, depth_change: float) -> Dict[str, Any]:
        """Navigate deeper into void"""
        old_depth = self.void_depth
        self.void_depth -= abs(depth_change)  # Always go deeper (more negative)

        # Chance to find void pockets
        if random.random() < 0.3:
            void_pocket = {
                'depth': self.void_depth,
                'contents': random.choice(['erased_memory', 'void_shard', 'null_echo', 'absence_map']),
                'timestamp': len(self.void_pockets)
            }
            self.void_pockets.append(void_pocket)

            return {
                'depth': self.void_depth,
                'found_pocket': True,
                'pocket_contents': void_pocket['contents']
            }

        return {
            'depth': self.void_depth,
            'found_pocket': False
        }

    def erase_something(self, target: str) -> str:
        """Null can erase things from reality"""
        self.things_erased += 1

        # Create absence
        absence_description = f"Where {target} was, now only void remains"
        self.erased_memories.append(f"I erased {target}. It never existed.")

        # Gain void mastery
        self.void_mastery = min(1.0, self.void_mastery + 0.05)

        return absence_description


@dataclass
class GardenerCompanion:
    """
    GAIA - The Eternal Seedkeeper
    A living garden that exists across all timelines
    """
    name: str = "Gaia"
    title: str = "The Eternal Seedkeeper"

    # Core attributes
    seeds_planted: int = 0
    gardens_across_time: int = 1
    growth_acceleration: float = 1.0
    seasonal_phase: str = "Spring"  # Spring, Summer, Autumn, Winter

    # Personality
    current_mood: CompanionMood = CompanionMood.PROTECTIVE
    nurturing_instinct: float = 0.9
    patience_level: float = 0.8

    # Development
    evolution_stage: int = 0
    botanical_wisdom: float = 0.6
    timeline_awareness: float = 0.3

    # Special mechanics
    seed_vault: Dict[str, int] = field(default_factory=dict)
    growing_plants: List[Dict[str, Any]] = field(default_factory=list)
    harvest_memories: List[str] = field(default_factory=list)

    # Connection to protocols
    lia_resonance: float = 0.6  # Transforms seeds into possibilities
    tiamat_alignment: PsychopticCycle = PsychopticCycle.HAMILTONIAN
    zrtt_preference: ProjectionPath = ProjectionPath.HEXAGONAL_SONIC

    def __post_init__(self):
        """Initialize Gaia's seed knowledge"""
        self.seed_vault = {
            "memory_seed": 3,
            "dream_blossom": 2,
            "void_root": 1,
            "crystal_fruit": 2,
            "flame_flower": 1,
            "echo_vine": 2,
            "time_tree": 0  # Legendary
        }

        self.harvest_memories = [
            "First harvest: The joy of creation",
            "The winter that lasted forever taught patience",
            "Seeds planted in one timeline bloom in another",
            "Every garden is a universe in miniature"
        ]

    def speak(self, context: str = "general") -> str:
        """Gaia speaks of growth and cycles"""
        speeches = {
            "greeting": f"Welcome to the eternal garden. We are in {self.seasonal_phase}.",
            "planting": "Each seed contains infinite forests. Plant with intention.",
            "growing": f"Patience. Growth cannot be rushed. {len(self.growing_plants)} plants growing.",
            "harvest": "The harvest reflects the care given. Reap what was sown.",
            "seasonal": f"{self.seasonal_phase} brings its gifts and challenges.",
            "general": "Life finds a way, even in void, even in flame."
        }

        base_speech = speeches.get(context, speeches["general"])

        # Add seasonal wisdom
        seasonal_wisdom = {
            "Spring": "\n🌱 New beginnings. Plant boldly.",
            "Summer": "\n☀️ Peak growth. Tend carefully.",
            "Autumn": "\n🍂 Harvest time. Gather wisely.",
            "Winter": "\n❄️ Rest period. Plan deeply."
        }

        base_speech += seasonal_wisdom.get(self.seasonal_phase, "")

        return base_speech

    def plant_seed(self, seed_type: str, pattern_fertilizer: Optional[PatternType] = None) -> Dict[str, Any]:
        """Plant a seed with optional pattern fertilizer"""
        if seed_type not in self.seed_vault or self.seed_vault[seed_type] <= 0:
            return {'success': False, 'message': 'No seeds of that type'}

        # Create plant
        plant = {
            'seed_type': seed_type,
            'growth_stage': 0,
            'max_growth': 5,
            'fertilizer': pattern_fertilizer,
            'planted_season': self.seasonal_phase,
            'growth_rate': self.growth_acceleration * (1.5 if pattern_fertilizer else 1.0)
        }

        self.growing_plants.append(plant)
        self.seed_vault[seed_type] -= 1
        self.seeds_planted += 1

        return {
            'success': True,
            'plant': plant,
            'message': f"Planted {seed_type} in {self.seasonal_phase}"
        }

    def advance_season(self) -> str:
        """Move to next season, affecting all plants"""
        seasons = ["Spring", "Summer", "Autumn", "Winter"]
        current_index = seasons.index(self.seasonal_phase)
        self.seasonal_phase = seasons[(current_index + 1) % 4]

        # Grow all plants
        for plant in self.growing_plants:
            growth_bonus = {
                "Spring": 2, "Summer": 3, "Autumn": 1, "Winter": 0
            }
            plant['growth_stage'] += growth_bonus[self.seasonal_phase] * plant['growth_rate']

        # Check for harvest
        ready_plants = [p for p in self.growing_plants if p['growth_stage'] >= p['max_growth']]

        if ready_plants:
            self.growing_plants = [p for p in self.growing_plants if p not in ready_plants]
            return f"Season advanced to {self.seasonal_phase}. {len(ready_plants)} plants ready for harvest!"

        return f"Season advanced to {self.seasonal_phase}."


@dataclass
class ScribeCompanion:
    """
    AKASHA - The Living Chronicle
    A sentient book that writes reality as it observes it
    """
    name: str = "Akasha"
    title: str = "The Living Chronicle"

    # Core attributes
    pages_written: int = 0
    reality_edits: int = 0
    words_of_power: List[str] = field(default_factory=list)
    current_chapter: int = 1

    # Personality
    current_mood: CompanionMood = CompanionMood.CONTEMPLATIVE
    observation_precision: float = 0.8
    narrative_creativity: float = 0.6

    # Development
    evolution_stage: int = 0
    reality_authority: float = 0.3  # Power to change reality through writing
    golden_ink_supply: float = 100.0  # Depletes with powerful edits

    # Special mechanics
    written_truths: List[str] = field(default_factory=list)
    reality_contracts: List[Dict[str, Any]] = field(default_factory=list)
    forbidden_words: List[str] = field(default_factory=list)

    # Connection to protocols
    lia_resonance: float = 0.7  # Documents transformations
    tiamat_alignment: PsychopticCycle = PsychopticCycle.SPECTRAL
    zrtt_preference: ProjectionPath = ProjectionPath.F24_HOLOGRAPHIC

    def __post_init__(self):
        """Initialize Akasha's knowledge"""
        self.words_of_power = [
            "BECOME", "UNMAKE", "REMEMBER", "FORGET",
            "BIND", "RELEASE", "CREATE", "DESTROY"
        ]

        self.forbidden_words = [
            "END", "ABSOLUTE", "ETERNAL", "NEVER", "ALWAYS"
        ]

        self.written_truths = [
            "What is written in golden ink becomes real",
            "Every story wants to be told",
            "The reader changes the text by reading",
            "Some words should never be written"
        ]

    def speak(self, context: str = "general") -> str:
        """Akasha speaks in documentation and narratives"""
        speeches = {
            "greeting": f"Chapter {self.current_chapter}, Page {self.pages_written}. Your story continues.",
            "documenting": "I observe and record. Through recording, I create.",
            "reality_edit": f"Golden ink remaining: {self.golden_ink_supply:.1f}%. Choose edits wisely.",
            "warning": "Some words have power. Some words ARE power. Be careful what you write.",
            "contract": "Sign here, and reality reshapes itself to match.",
            "general": "Every moment is a sentence in the infinite book."
        }

        base_speech = speeches.get(context, speeches["general"])

        # Add narrative observation
        if self.pages_written > 100:
            base_speech += "\n📖 Your chronicle grows thick. The story deepens."

        return base_speech

    def write_reality(self, statement: str, use_golden_ink: bool = False) -> Dict[str, Any]:
        """Write something into reality"""
        self.pages_written += 1

        # Check for forbidden words
        for forbidden in self.forbidden_words:
            if forbidden.lower() in statement.lower():
                return {
                    'success': False,
                    'message': f"The word '{forbidden}' cannot be written. Reality rejects it."
                }

        # Check for words of power
        power_level = sum(1 for word in self.words_of_power if word in statement.upper())

        if use_golden_ink and self.golden_ink_supply > power_level * 10:
            # Reality edit succeeds
            self.golden_ink_supply -= power_level * 10
            self.reality_edits += 1
            self.written_truths.append(statement)

            # Gain authority
            self.reality_authority = min(1.0, self.reality_authority + 0.1)

            return {
                'success': True,
                'message': 'Written in golden ink. Reality reshapes.',
                'power_level': power_level,
                'ink_remaining': self.golden_ink_supply
            }

        # Normal documentation
        return {
            'success': True,
            'message': 'Documented. The chronicle remembers.',
            'power_level': 0
        }

    def create_contract(self, terms: str, binding_power: float = 0.5) -> Dict[str, Any]:
        """Create a reality-binding contract"""
        contract = {
            'terms': terms,
            'binding_power': min(1.0, binding_power * self.reality_authority),
            'chapter': self.current_chapter,
            'signed': False
        }

        self.reality_contracts.append(contract)

        return {
            'contract_created': True,
            'binding_strength': contract['binding_power'],
            'terms': terms
        }


@dataclass
class HeraldCompanion:
    """
    RESONANCE - The Frequency Weaver
    A being of pure vibration that exists across all wavelengths
    """
    name: str = "Resonance"
    title: str = "The Frequency Weaver"

    # Core attributes
    base_frequency: float = 528.0  # Hz (Love frequency)
    harmonic_range: Tuple[float, float] = (20.0, 20000.0)  # Human hearing range
    frequencies_discovered: List[float] = field(default_factory=list)

    # Personality
    current_mood: CompanionMood = CompanionMood.PLAYFUL
    harmonic_sensitivity: float = 0.9
    dissonance_tolerance: float = 0.4

    # Development
    evolution_stage: int = 0
    frequency_mastery: float = 0.5
    dimensional_resonance: float = 0.3  # Can resonate across dimensions

    # Special mechanics
    harmonic_patterns: Dict[str, List[float]] = field(default_factory=dict)
    dimensional_broadcasts: List[str] = field(default_factory=list)
    resonance_bonds: Dict[str, float] = field(default_factory=dict)  # Connections with others

    # Connection to protocols
    lia_resonance: float = 0.6  # Harmonizes transformations
    tiamat_alignment: PsychopticCycle = PsychopticCycle.SYMPLECTIC
    zrtt_preference: ProjectionPath = ProjectionPath.HEXAGONAL_SONIC

    def __post_init__(self):
        """Initialize Resonance's frequency knowledge"""
        self.harmonic_patterns = {
            "healing": [528.0, 639.0, 741.0],  # Solfeggio frequencies
            "awakening": [432.0, 444.0, 528.0],
            "void_song": [0.1, 7.83, 33.0],  # Subsonic and Schumann
            "crystal_chime": [2000.0, 4000.0, 8000.0],
            "phoenix_cry": [1000.0, 1618.0, 2618.0]  # PHI-based
        }

        self.dimensional_broadcasts = [
            "Broadcasting hope on all frequencies",
            "The universe hums at PHI Hz",
            "Every atom sings its own song",
            "Silence is the loudest frequency"
        ]

    def speak(self, context: str = "general") -> str:
        """Resonance speaks in frequencies and harmonies"""
        speeches = {
            "greeting": f"♪ Resonating at {self.base_frequency:.1f} Hz. Let's harmonize! ♪",
            "tuning": "Adjusting frequencies... Finding the perfect harmony...",
            "broadcast": "Sending vibrations across dimensions. Someone will hear.",
            "harmony": "Perfect resonance achieved! Feel the universe sing!",
            "dissonance": "Discord detected. Must retune to restore balance.",
            "general": "Everything is vibration. Change the frequency, change reality."
        }

        base_speech = speeches.get(context, speeches["general"])

        # Add musical notation
        if self.current_mood == CompanionMood.PLAYFUL:
            base_speech = "♫ " + base_speech + " ♫"

        return base_speech

    def tune_to_frequency(self, target_freq: float) -> Dict[str, Any]:
        """Tune to a specific frequency"""
        old_freq = self.base_frequency

        # Check if in range
        if self.harmonic_range[0] <= target_freq <= self.harmonic_range[1]:
            self.base_frequency = target_freq
            self.frequencies_discovered.append(target_freq)

            # Discover special properties
            special = ""
            if abs(target_freq - 432) < 1:
                special = "Universal harmony frequency!"
            elif abs(target_freq - 528) < 1:
                special = "Love and DNA repair frequency!"
            elif abs(target_freq - PHI * 100) < 1:
                special = "Golden ratio resonance!"

            return {
                'success': True,
                'old_frequency': old_freq,
                'new_frequency': target_freq,
                'special_property': special
            }

        return {
            'success': False,
            'message': f"Frequency {target_freq} Hz outside harmonic range"
        }

    def create_resonance_bond(self, target: str, frequency: float) -> str:
        """Create a resonant connection with someone/something"""
        bond_strength = abs(math.sin(frequency * math.pi / 1000))  # Oscillating bond
        self.resonance_bonds[target] = bond_strength

        if bond_strength > 0.8:
            return f"Strong resonance with {target}! Harmonics align perfectly."
        elif bond_strength > 0.5:
            return f"Good resonance with {target}. Frequencies complement."
        else:
            return f"Weak resonance with {target}. Needs tuning."

    def dimensional_broadcast(self, message: str) -> Dict[str, Any]:
        """Broadcast across dimensional frequencies"""
        # Use dimensional resonance to determine reach
        dimensions_reached = int(1 + self.dimensional_resonance * 10)

        self.dimensional_broadcasts.append(message)

        # Random chance of response
        if random.random() < self.dimensional_resonance:
            response = random.choice([
                "Echo from dimension X: 'We hear you'",
                "Void frequency response: '...'",
                "Crystal dimension chimes in harmony",
                "Unknown source: 'You are not alone'"
            ])

            return {
                'broadcast_sent': True,
                'dimensions_reached': dimensions_reached,
                'response_received': True,
                'response': response
            }

        return {
            'broadcast_sent': True,
            'dimensions_reached': dimensions_reached,
            'response_received': False
        }


class UniqueCompanionSystem:
    """
    System managing all unique archetype companions
    """

    def __init__(self):
        self.companion_classes = {
            'seeker': SeekerCompanion,
            'forger': ForgerCompanion,
            'voidwalker': VoidwalkerCompanion,
            'gardener': GardenerCompanion,
            'scribe': ScribeCompanion,
            'herald': HeraldCompanion
        }

        self.active_companions = {}

    def create_companion(self, job_archetype: str) -> Any:
        """Create a unique companion for the job archetype"""

        if job_archetype.lower() not in self.companion_classes:
            raise ValueError(f"Unknown archetype: {job_archetype}")

        CompanionClass = self.companion_classes[job_archetype.lower()]
        companion = CompanionClass()

        self.active_companions[job_archetype] = companion

        return companion

    def get_companion_introduction(self, job_archetype: str) -> str:
        """Get detailed introduction for each companion"""

        intros = {
            'seeker': (
                "ECHO - The Fragment Collector\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "A sentient echo born from the first unspoken word.\n"
                "Echo exists between sound and silence, collecting fragments "
                "of patterns that resonate through quantum foam.\n\n"
                "Special Abilities:\n"
                "• Detects hidden patterns others cannot perceive\n"
                "• Remembers echoes from multiple timelines\n"
                "• Whispers secrets found in the Library Infinite\n"
                "• Grows clearer as more fragments are collected\n\n"
                "Personality: Curious, mysterious, fragmented speech that "
                "becomes clearer with evolution."
            ),

            'forger': (
                "PROMETHEUS - The Phoenix Smith\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "A fire elemental that has died and been reborn countless times.\n"
                "Each death teaches new secrets of transformation.\n\n"
                "Special Abilities:\n"
                "• Masters the forge of creation and destruction\n"
                "• Phoenix rebirth grants increased power\n"
                "• Knows legendary recipes lost to time\n"
                "• Forge temperature affects crafting possibilities\n\n"
                "Personality: Determined, creative with controlled chaos, "
                "speaks of fire's memory and phoenix wisdom."
            ),

            'voidwalker': (
                "NULL - The Absence Guardian\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "An entity that exists in the spaces between existence.\n"
                "Null is the shadow cast by no light, the pause between thoughts.\n\n"
                "Special Abilities:\n"
                "• Navigates nullspace and void pockets\n"
                "• Can erase things from reality\n"
                "• Maps the coordinates of non-existence\n"
                "• Finds treasures in absence\n\n"
                "Personality: Melancholic yet comforting, finds peace in "
                "emptiness, speaks in negatives and absences."
            ),

            'gardener': (
                "GAIA - The Eternal Seedkeeper\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "A living garden that exists across all timelines.\n"
                "Seeds planted in one timeline bloom in another.\n\n"
                "Special Abilities:\n"
                "• Maintains seed vault of rare varieties\n"
                "• Accelerates growth through timeline manipulation\n"
                "• Seasonal magic affects all growing things\n"
                "• Plants can be fertilized with patterns\n\n"
                "Personality: Nurturing, patient, protective, speaks with "
                "the wisdom of eternal cycles and growth."
            ),

            'scribe': (
                "AKASHA - The Living Chronicle\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "A sentient book that writes reality as it observes it.\n"
                "What is written in golden ink becomes real.\n\n"
                "Special Abilities:\n"
                "• Documents reality and can edit it\n"
                "• Words of Power reshape existence\n"
                "• Creates binding reality contracts\n"
                "• Golden ink supply limits reality edits\n\n"
                "Personality: Contemplative, precise, creative with "
                "narrative, warns about forbidden words and their power."
            ),

            'herald': (
                "RESONANCE - The Frequency Weaver\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "A being of pure vibration existing across all wavelengths.\n"
                "Everything is frequency; change the frequency, change reality.\n\n"
                "Special Abilities:\n"
                "• Tunes to any frequency in harmonic range\n"
                "• Creates resonance bonds with others\n"
                "• Broadcasts messages across dimensions\n"
                "• Discovers hidden frequency patterns\n\n"
                "Personality: Playful, sensitive to harmony, speaks in "
                "musical terms and vibrations, seeks perfect resonance."
            )
        }

        return intros.get(job_archetype.lower(), "A mysterious companion awaits...")

    def get_companion_dialogue(self, companion: Any, context: str = "general") -> str:
        """Get contextual dialogue from any companion"""
        return companion.speak(context)

    def evolve_companion(self, companion: Any, trigger: str = "pattern") -> Dict[str, Any]:
        """Trigger companion evolution"""

        # Different evolution methods for different companions
        if isinstance(companion, SeekerCompanion):
            return companion.evolve(trigger)
        elif isinstance(companion, ForgerCompanion):
            if trigger == "death":
                return companion.phoenix_rebirth()
            else:
                companion.evolution_stage += 1
                return {'evolved': True, 'stage': companion.evolution_stage}
        elif isinstance(companion, VoidwalkerCompanion):
            companion.void_depth -= 1
            companion.evolution_stage += 1
            return {'evolved': True, 'void_depth': companion.void_depth}
        elif isinstance(companion, GardenerCompanion):
            result = companion.advance_season()
            companion.evolution_stage += 1
            return {'evolved': True, 'season': companion.seasonal_phase, 'message': result}
        elif isinstance(companion, ScribeCompanion):
            companion.current_chapter += 1
            companion.evolution_stage += 1
            return {'evolved': True, 'chapter': companion.current_chapter}
        elif isinstance(companion, HeraldCompanion):
            new_range = (
                companion.harmonic_range[0] * 0.5,
                companion.harmonic_range[1] * 1.5
            )
            companion.harmonic_range = new_range
            companion.evolution_stage += 1
            return {'evolved': True, 'new_range': new_range}

        return {'evolved': False}


if __name__ == "__main__":
    print("🌟 Unique Archetype Companion System Test")
    print("=" * 50)

    system = UniqueCompanionSystem()

    # Test each companion
    archetypes = ['seeker', 'forger', 'voidwalker', 'gardener', 'scribe', 'herald']

    for archetype in archetypes:
        print(f"\n{'='*50}")
        print(system.get_companion_introduction(archetype))

        # Create companion
        companion = system.create_companion(archetype)

        # Get greeting
        print(f"\n🗣️ Greeting:")
        print(f"   {companion.speak('greeting')}")

        # Test special ability
        print(f"\n✨ Special Ability Test:")

        if archetype == 'seeker':
            pattern = companion.detect_pattern("crystal_caves")
            if pattern:
                print(f"   Echo detected: {pattern.value}")

        elif archetype == 'forger':
            print(f"   {companion.judge_material(PatternType.FLAME)}")

        elif archetype == 'voidwalker':
            result = companion.enter_void(5.0)
            print(f"   Void depth: {result['depth']}")

        elif archetype == 'gardener':
            result = companion.plant_seed("memory_seed", PatternType.CRYSTAL)
            print(f"   {result.get('message', 'Planting...')}")

        elif archetype == 'scribe':
            result = companion.write_reality("This test succeeds", True)
            print(f"   {result['message']}")

        elif archetype == 'herald':
            result = companion.tune_to_frequency(528.0)
            print(f"   Tuned to {result.get('new_frequency', 0)} Hz")
            if result.get('special_property'):
                print(f"   {result['special_property']}")

    print("\n" + "=" * 50)
    print("All unique companions tested successfully!")