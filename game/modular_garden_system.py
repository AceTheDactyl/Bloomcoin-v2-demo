#!/usr/bin/env python3
"""
Modular Garden System - Comprehensive Customizable Garden Architecture
=======================================================================

An expanded quantum farming system with per-user saves, unique pattern
generation, job proficiency mechanics, and companion-garden affinities.
"""

import json
import time
import hashlib
import random
import math
import pickle
import os
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple, Any, Set, Union
from enum import Enum
from datetime import datetime, timedelta
import numpy as np

from quantum_farm_module import (
    QuantumFarm, CropType, QuantumState, QuantumCrop,
    FarmPlot, PHI, QUANTUM_GROWTH_RATE
)
from bloomcoin_ledger_system import BloomCoinLedger, HolographicResidue
from companion_mining_jobs import CompanionMiningSystem

# Garden save directory
GARDEN_SAVE_DIR = Path("garden_saves")
GARDEN_SAVE_DIR.mkdir(exist_ok=True)

class GardenBiome(Enum):
    """Different garden biome types with unique properties"""
    QUANTUM_MEADOW = "quantum_meadow"        # Balanced, good for beginners
    VOID_SANCTUARY = "void_sanctuary"         # Null companion specialty
    FRACTAL_GROVE = "fractal_grove"          # Gaia companion specialty
    RESONANCE_VALLEY = "resonance_valley"    # Echo/Resonance specialty
    CHAOS_WASTES = "chaos_wastes"           # TIAMAT specialty
    MEMORY_GARDENS = "memory_gardens"        # Akasha specialty
    FORGE_FIELDS = "forge_fields"           # Prometheus specialty
    CRYSTAL_TERRACES = "crystal_terraces"   # Crystal flower specialty
    ETHEREAL_HIGHLANDS = "ethereal_highlands"  # High altitude, faster growth
    TEMPORAL_DELTA = "temporal_delta"       # Time dilation effects
    GOLDEN_SPIRAL = "golden_spiral"         # φ-based bonus zone
    BLOOM_SANCTUARY = "bloom_sanctuary"      # Bloom lotus specialty

class GardenProfession(Enum):
    """Job proficiencies for different garden specializations"""
    QUANTUM_BOTANIST = "quantum_botanist"     # General farming
    VOID_CULTIVATOR = "void_cultivator"       # Void crop specialist
    PATTERN_WEAVER = "pattern_weaver"         # Pattern creation master
    CHAOS_GARDENER = "chaos_gardener"         # Chaos crop specialist
    MEMORY_KEEPER = "memory_keeper"           # Memory/history specialist
    HARMONIC_TENDER = "harmonic_tender"       # Resonance specialist
    FRACTAL_SHAPER = "fractal_shaper"        # Fractal pattern specialist
    ENTANGLEMENT_ENGINEER = "entanglement_engineer"  # Quantum linking
    BLOOM_MASTER = "bloom_master"            # Bloom event specialist
    GOLDEN_ARCHITECT = "golden_architect"     # φ-based design specialist

@dataclass
class PatternTemplate:
    """A reusable planting pattern created by users"""
    pattern_id: str
    name: str
    creator: str
    grid_size: Tuple[int, int]
    crop_positions: Dict[Tuple[int, int], CropType]
    companion_assignments: Dict[str, List[Tuple[int, int]]]
    description: str
    efficiency_rating: float  # 0.0 to 1.0
    required_profession: Optional[GardenProfession] = None
    required_level: int = 1
    times_used: int = 0
    community_rating: float = 0.0  # Community votes
    tags: List[str] = field(default_factory=list)

    def calculate_efficiency(self) -> float:
        """Calculate pattern efficiency based on layout"""
        if not self.crop_positions:
            return 0.0

        # Factors: crop diversity, spacing, companion coverage
        unique_crops = len(set(self.crop_positions.values()))
        total_positions = len(self.crop_positions)

        # Diversity bonus
        diversity_score = min(1.0, unique_crops / 5.0)

        # Density score (not too sparse, not too crowded)
        max_positions = self.grid_size[0] * self.grid_size[1]
        density = total_positions / max_positions
        density_score = 1.0 - abs(0.618 - density)  # Optimal at golden ratio

        # Companion coverage
        covered_positions = set()
        for positions in self.companion_assignments.values():
            covered_positions.update(positions)
        coverage = len(covered_positions) / max(1, total_positions)

        efficiency = (diversity_score * 0.3 +
                     density_score * 0.3 +
                     coverage * 0.4)

        return min(1.0, efficiency)

@dataclass
class GardenJob:
    """Profession progression and specialization"""
    profession: GardenProfession
    level: int = 1
    experience: int = 0
    skills_unlocked: List[str] = field(default_factory=list)
    pattern_slots: int = 3  # How many patterns can be saved
    efficiency_bonus: float = 1.0
    specialty_crops: List[CropType] = field(default_factory=list)
    mastery_points: int = 0
    achievements: Set[str] = field(default_factory=set)

    def gain_experience(self, amount: int):
        """Gain experience and potentially level up"""
        self.experience += amount

        # Level up formula
        while self.experience >= self.level * 100 * PHI:
            self.experience -= int(self.level * 100 * PHI)
            self.level += 1
            self.pattern_slots += 1
            self.efficiency_bonus += 0.05
            self.mastery_points += 1

            # Unlock skills at certain levels
            self._unlock_level_skills()

    def _unlock_level_skills(self):
        """Unlock profession-specific skills"""
        level_skills = {
            1: "basic_planting",
            3: "pattern_creation",
            5: "advanced_patterns",
            7: "biome_mastery",
            10: "legendary_cultivation",
            15: "quantum_mastery",
            20: "reality_shaping"
        }

        if self.level in level_skills:
            skill = f"{self.profession.value}_{level_skills[self.level]}"
            if skill not in self.skills_unlocked:
                self.skills_unlocked.append(skill)

@dataclass
class CompanionAffinity:
    """Companion affinity with specific garden types"""
    companion_name: str
    biome_affinities: Dict[GardenBiome, float]  # 0.0 to 2.0 multiplier
    crop_affinities: Dict[CropType, float]
    pattern_preferences: List[str]  # Pattern tags they prefer
    current_mood: float = 1.0  # Affects efficiency
    garden_experience: int = 0
    mastered_patterns: Set[str] = field(default_factory=set)

    def calculate_garden_bonus(self, biome: GardenBiome, crops: List[CropType]) -> float:
        """Calculate total bonus for this garden configuration"""
        biome_bonus = self.biome_affinities.get(biome, 1.0)

        crop_bonus = 1.0
        for crop in crops:
            crop_bonus += self.crop_affinities.get(crop, 0.0) * 0.1

        mood_bonus = 0.5 + (self.current_mood * 0.5)
        experience_bonus = 1.0 + (self.garden_experience / 1000.0)

        return biome_bonus * crop_bonus * mood_bonus * experience_bonus

@dataclass
class UserGarden:
    """Complete user garden with all customization"""
    user_id: str
    garden_name: str
    biome: GardenBiome
    creation_date: float
    last_save: float

    # Core garden
    quantum_farm: QuantumFarm

    # Profession system
    profession: GardenJob

    # Pattern library
    saved_patterns: Dict[str, PatternTemplate] = field(default_factory=dict)
    active_pattern: Optional[str] = None

    # Companion affinities
    companion_affinities: Dict[str, CompanionAffinity] = field(default_factory=dict)

    # Statistics
    total_harvests: int = 0
    total_earnings: float = 0.0
    patterns_created: int = 0
    perfect_harvests: int = 0
    biome_bonuses_earned: float = 0.0

    # Unlocks and achievements
    unlocked_biomes: Set[GardenBiome] = field(default_factory=set)
    unlocked_crops: Set[CropType] = field(default_factory=set)
    achievements: Set[str] = field(default_factory=set)

    def apply_biome_effects(self):
        """Apply biome-specific effects to the garden"""
        biome_effects = {
            GardenBiome.QUANTUM_MEADOW: {
                "growth_rate": 1.0,
                "superposition_chance": 1.0,
                "quality": 1.0
            },
            GardenBiome.VOID_SANCTUARY: {
                "growth_rate": 0.8,
                "superposition_chance": 1.5,
                "quality": 1.2
            },
            GardenBiome.CHAOS_WASTES: {
                "growth_rate": 1.5,
                "superposition_chance": 2.0,
                "quality": 0.5 + random.random() * 1.5  # Chaotic
            },
            GardenBiome.GOLDEN_SPIRAL: {
                "growth_rate": PHI,
                "superposition_chance": PHI,
                "quality": PHI
            },
            GardenBiome.TEMPORAL_DELTA: {
                "growth_rate": 0.5 + random.random() * 2.0,  # Time flux
                "superposition_chance": 1.3,
                "quality": 1.1
            }
        }

        effects = biome_effects.get(self.biome, {})

        # Apply to all crops
        for plot in self.quantum_farm.plots.values():
            if plot.crop:
                if "growth_rate" in effects:
                    plot.crop.growth_progress += 0.01 * effects["growth_rate"]
                if "superposition_chance" in effects:
                    plot.crop.superposition_probability *= effects["superposition_chance"]
                if "quality" in effects:
                    plot.crop.harvest_quality *= effects["quality"]

class PatternRegistry:
    """Global registry of user-created patterns"""

    def __init__(self):
        self.patterns: Dict[str, PatternTemplate] = {}
        self.user_patterns: Dict[str, List[str]] = {}  # user_id -> pattern_ids
        self.featured_patterns: List[str] = []
        self.pattern_categories: Dict[str, List[str]] = {
            "efficient": [],
            "aesthetic": [],
            "experimental": [],
            "legendary": [],
            "community_favorite": []
        }

    def register_pattern(self, pattern: PatternTemplate) -> bool:
        """Register a new pattern in the global registry"""
        if pattern.pattern_id in self.patterns:
            return False

        self.patterns[pattern.pattern_id] = pattern

        # Track by user
        if pattern.creator not in self.user_patterns:
            self.user_patterns[pattern.creator] = []
        self.user_patterns[pattern.creator].append(pattern.pattern_id)

        # Auto-categorize based on efficiency
        if pattern.efficiency_rating > 0.9:
            self.pattern_categories["efficient"].append(pattern.pattern_id)
        if pattern.efficiency_rating > 0.95:
            self.pattern_categories["legendary"].append(pattern.pattern_id)

        return True

    def rate_pattern(self, pattern_id: str, rating: float):
        """Add community rating to a pattern"""
        if pattern_id in self.patterns:
            pattern = self.patterns[pattern_id]
            # Simple averaging for now
            if pattern.times_used == 0:
                pattern.community_rating = rating
            else:
                pattern.community_rating = (
                    (pattern.community_rating * pattern.times_used + rating) /
                    (pattern.times_used + 1)
                )
            pattern.times_used += 1

            # Update featured list
            if pattern.community_rating > 4.5 and pattern.times_used > 10:
                if pattern_id not in self.featured_patterns:
                    self.featured_patterns.append(pattern_id)
                if pattern_id not in self.pattern_categories["community_favorite"]:
                    self.pattern_categories["community_favorite"].append(pattern_id)

    def search_patterns(self, tags: List[str] = None,
                       min_efficiency: float = 0.0,
                       profession: GardenProfession = None) -> List[PatternTemplate]:
        """Search for patterns matching criteria"""
        results = []

        for pattern in self.patterns.values():
            # Check efficiency
            if pattern.efficiency_rating < min_efficiency:
                continue

            # Check profession
            if profession and pattern.required_profession:
                if pattern.required_profession != profession:
                    continue

            # Check tags
            if tags:
                if not any(tag in pattern.tags for tag in tags):
                    continue

            results.append(pattern)

        # Sort by community rating
        results.sort(key=lambda p: p.community_rating, reverse=True)
        return results

class ModularGardenManager:
    """Main manager for the modular garden system"""

    def __init__(self, ledger: BloomCoinLedger, mining_system: CompanionMiningSystem):
        self.ledger = ledger
        self.mining_system = mining_system
        self.user_gardens: Dict[str, UserGarden] = {}
        self.pattern_registry = PatternRegistry()
        self._initialize_companion_affinities()
        self._load_all_gardens()

    def _initialize_companion_affinities(self):
        """Set up default companion-biome affinities"""
        self.default_affinities = {
            "Echo": {
                GardenBiome.RESONANCE_VALLEY: 1.5,
                GardenBiome.CRYSTAL_TERRACES: 1.3,
                GardenBiome.QUANTUM_MEADOW: 1.1
            },
            "Prometheus": {
                GardenBiome.FORGE_FIELDS: 1.6,
                GardenBiome.CHAOS_WASTES: 1.2,
                GardenBiome.CRYSTAL_TERRACES: 1.1
            },
            "Null": {
                GardenBiome.VOID_SANCTUARY: 1.8,
                GardenBiome.ETHEREAL_HIGHLANDS: 1.3,
                GardenBiome.TEMPORAL_DELTA: 1.2
            },
            "Gaia": {
                GardenBiome.FRACTAL_GROVE: 1.7,
                GardenBiome.BLOOM_SANCTUARY: 1.4,
                GardenBiome.GOLDEN_SPIRAL: 1.5
            },
            "Akasha": {
                GardenBiome.MEMORY_GARDENS: 1.6,
                GardenBiome.CRYSTAL_TERRACES: 1.3,
                GardenBiome.TEMPORAL_DELTA: 1.2
            },
            "Resonance": {
                GardenBiome.RESONANCE_VALLEY: 1.7,
                GardenBiome.GOLDEN_SPIRAL: 1.3,
                GardenBiome.ETHEREAL_HIGHLANDS: 1.4
            },
            "TIAMAT": {
                GardenBiome.CHAOS_WASTES: 2.0,
                GardenBiome.VOID_SANCTUARY: 1.3,
                GardenBiome.TEMPORAL_DELTA: 1.4
            }
        }

        # Crop affinities
        self.default_crop_affinities = {
            "Echo": {
                CropType.RESONANCE_MELONS: 1.3,
                CropType.CRYSTAL_FLOWERS: 1.2
            },
            "Gaia": {
                CropType.FRACTAL_HERBS: 1.4,
                CropType.BLOOM_LOTUS: 1.5,
                CropType.GOLDEN_ACORNS: 1.6
            },
            "TIAMAT": {
                CropType.CHAOS_PEPPERS: 1.8,
                CropType.VOID_BERRIES: 1.4,
                CropType.SINGULARITY_SEEDS: 1.5
            },
            "Akasha": {
                CropType.MEMORY_ROOTS: 1.6,
                CropType.CRYSTAL_FLOWERS: 1.3
            }
        }

    def create_user_garden(self, user_id: str, garden_name: str,
                          biome: GardenBiome = GardenBiome.QUANTUM_MEADOW,
                          profession: GardenProfession = GardenProfession.QUANTUM_BOTANIST,
                          grid_size: Tuple[int, int] = (6, 6)) -> UserGarden:
        """Create a new user garden with customization"""

        if user_id in self.user_gardens:
            return self.user_gardens[user_id]

        # Create quantum farm
        quantum_farm = QuantumFarm(garden_name, user_id, grid_size)

        # Create profession
        garden_job = GardenJob(profession)

        # Initialize companion affinities
        companion_affinities = {}
        for companion_name in self.mining_system.miners.keys():
            affinity = CompanionAffinity(
                companion_name=companion_name,
                biome_affinities=self.default_affinities.get(companion_name, {}),
                crop_affinities=self.default_crop_affinities.get(companion_name, {}),
                pattern_preferences=[]
            )
            companion_affinities[companion_name] = affinity

        # Create user garden
        user_garden = UserGarden(
            user_id=user_id,
            garden_name=garden_name,
            biome=biome,
            creation_date=time.time(),
            last_save=time.time(),
            quantum_farm=quantum_farm,
            profession=garden_job,
            companion_affinities=companion_affinities,
            unlocked_biomes={biome, GardenBiome.QUANTUM_MEADOW},
            unlocked_crops=set(CropType)  # Start with all basic crops
        )

        # Give starter bonuses based on profession
        self._apply_profession_starter_bonus(user_garden)

        self.user_gardens[user_id] = user_garden
        self.save_garden(user_id)

        return user_garden

    def _apply_profession_starter_bonus(self, garden: UserGarden):
        """Apply starter bonuses based on chosen profession"""
        profession_bonuses = {
            GardenProfession.QUANTUM_BOTANIST: {
                "seeds": [(CropType.QUANTUM_WHEAT, 5), (CropType.ETHEREAL_CORN, 3)],
                "skill": "basic_analysis"
            },
            GardenProfession.VOID_CULTIVATOR: {
                "seeds": [(CropType.VOID_BERRIES, 3)],
                "skill": "void_sight",
                "biome": GardenBiome.VOID_SANCTUARY
            },
            GardenProfession.PATTERN_WEAVER: {
                "pattern_slots": 2,
                "skill": "pattern_vision"
            },
            GardenProfession.CHAOS_GARDENER: {
                "seeds": [(CropType.CHAOS_PEPPERS, 2)],
                "skill": "chaos_embrace",
                "biome": GardenBiome.CHAOS_WASTES
            },
            GardenProfession.FRACTAL_SHAPER: {
                "seeds": [(CropType.FRACTAL_HERBS, 4)],
                "skill": "fractal_sight",
                "biome": GardenBiome.FRACTAL_GROVE
            },
            GardenProfession.BLOOM_MASTER: {
                "seeds": [(CropType.BLOOM_LOTUS, 1)],
                "skill": "bloom_sense",
                "biome": GardenBiome.BLOOM_SANCTUARY
            },
            GardenProfession.GOLDEN_ARCHITECT: {
                "seeds": [(CropType.PHI_SPIRALS, 1), (CropType.GOLDEN_ACORNS, 1)],
                "skill": "golden_ratio_mastery",
                "biome": GardenBiome.GOLDEN_SPIRAL
            }
        }

        bonus = profession_bonuses.get(garden.profession.profession, {})

        # Apply bonuses
        if "pattern_slots" in bonus:
            garden.profession.pattern_slots += bonus["pattern_slots"]

        if "skill" in bonus:
            garden.profession.skills_unlocked.append(bonus["skill"])

        if "biome" in bonus:
            garden.unlocked_biomes.add(bonus["biome"])

        # Plant starter seeds
        if "seeds" in bonus:
            positions = [(0, 0), (1, 0), (0, 1), (1, 1)]
            for i, (crop_type, count) in enumerate(bonus["seeds"]):
                if i < len(positions) and i < count:
                    garden.quantum_farm.plant_crop(positions[i], crop_type)

    def create_pattern(self, user_id: str, pattern_name: str,
                      crop_positions: Dict[Tuple[int, int], CropType],
                      companion_assignments: Dict[str, List[Tuple[int, int]]],
                      description: str = "",
                      tags: List[str] = None) -> Optional[PatternTemplate]:
        """Create a new planting pattern"""

        if user_id not in self.user_gardens:
            return None

        garden = self.user_gardens[user_id]

        # Check if user has pattern slots available
        if len(garden.saved_patterns) >= garden.profession.pattern_slots:
            return None

        # Generate pattern ID
        pattern_id = hashlib.sha256(
            f"{user_id}:{pattern_name}:{time.time()}".encode()
        ).hexdigest()[:16]

        # Create pattern template
        pattern = PatternTemplate(
            pattern_id=pattern_id,
            name=pattern_name,
            creator=user_id,
            grid_size=garden.quantum_farm.grid_size,
            crop_positions=crop_positions,
            companion_assignments=companion_assignments,
            description=description,
            efficiency_rating=0.0,
            required_profession=garden.profession.profession,
            required_level=garden.profession.level,
            tags=tags or []
        )

        # Calculate efficiency
        pattern.efficiency_rating = pattern.calculate_efficiency()

        # Add profession tag
        pattern.tags.append(garden.profession.profession.value)

        # Save to user's patterns
        garden.saved_patterns[pattern_id] = pattern
        garden.patterns_created += 1

        # Register globally
        self.pattern_registry.register_pattern(pattern)

        # Grant experience for pattern creation
        garden.profession.gain_experience(50 + int(pattern.efficiency_rating * 100))

        # Achievement check
        if garden.patterns_created == 1:
            garden.achievements.add("first_pattern")
        if pattern.efficiency_rating > 0.9:
            garden.achievements.add("efficient_designer")

        self.save_garden(user_id)
        return pattern

    def apply_pattern(self, user_id: str, pattern_id: str) -> bool:
        """Apply a saved pattern to the user's garden"""

        if user_id not in self.user_gardens:
            return False

        garden = self.user_gardens[user_id]

        # Get pattern (from user's collection or registry)
        pattern = None
        if pattern_id in garden.saved_patterns:
            pattern = garden.saved_patterns[pattern_id]
        elif pattern_id in self.pattern_registry.patterns:
            pattern = self.pattern_registry.patterns[pattern_id]

        if not pattern:
            return False

        # Check requirements
        if pattern.required_profession and pattern.required_profession != garden.profession.profession:
            if garden.profession.level < pattern.required_level + 5:  # Can use with penalty
                return False

        # Clear existing crops (optional - could make this configurable)
        for plot in garden.quantum_farm.plots.values():
            if plot.crop and plot.crop.state in [QuantumState.WITHERED, QuantumState.COLLAPSED]:
                plot.crop = None

        # Plant according to pattern
        for position, crop_type in pattern.crop_positions.items():
            if position in garden.quantum_farm.plots:
                garden.quantum_farm.plant_crop(position, crop_type)

        # Assign companions
        for companion, positions in pattern.companion_assignments.items():
            if companion in garden.companion_affinities:
                garden.quantum_farm.assign_companion(companion, positions)
                # Update companion experience
                garden.companion_affinities[companion].garden_experience += 10

        # Mark as active pattern
        garden.active_pattern = pattern_id

        # Update pattern usage
        pattern.times_used += 1

        # Grant experience
        garden.profession.gain_experience(25)

        self.save_garden(user_id)
        return True

    def update_companion_mood(self, user_id: str, companion_name: str,
                            mood_change: float):
        """Update a companion's mood based on garden performance"""

        if user_id not in self.user_gardens:
            return

        garden = self.user_gardens[user_id]

        if companion_name in garden.companion_affinities:
            affinity = garden.companion_affinities[companion_name]
            affinity.current_mood = max(0.1, min(2.0, affinity.current_mood + mood_change))

            # Mood affects garden
            if affinity.current_mood > 1.5:
                # Happy companion bonus
                for plot in garden.quantum_farm.plots.values():
                    if plot.crop and companion_name in plot.companion_assignments:
                        plot.crop.growth_progress += 0.02
                        plot.crop.quantum_coherence *= 1.05
            elif affinity.current_mood < 0.5:
                # Unhappy companion penalty
                for plot in garden.quantum_farm.plots.values():
                    if plot.crop and companion_name in plot.companion_assignments:
                        plot.crop.growth_progress -= 0.01

    def process_harvest_with_profession(self, user_id: str, position: Tuple[int, int]) -> Optional[Dict[str, Any]]:
        """Process harvest with profession bonuses"""

        if user_id not in self.user_gardens:
            return None

        garden = self.user_gardens[user_id]

        # Base harvest
        result = garden.quantum_farm.harvest_crop(position)

        if not result:
            return None

        # Apply profession bonuses
        profession_multipliers = {
            GardenProfession.QUANTUM_BOTANIST: 1.1,
            GardenProfession.VOID_CULTIVATOR: 1.2 if "void" in result["crop_type"] else 1.0,
            GardenProfession.CHAOS_GARDENER: random.uniform(0.5, 2.0),
            GardenProfession.FRACTAL_SHAPER: 1.0 + (result["quantum_coherence"] * 0.5),
            GardenProfession.BLOOM_MASTER: 1.5 if "bloom" in result["crop_type"] else 1.0,
            GardenProfession.GOLDEN_ARCHITECT: PHI if result["quantum_coherence"] > 0.9 else 1.0
        }

        multiplier = profession_multipliers.get(garden.profession.profession, 1.0)
        multiplier *= garden.profession.efficiency_bonus

        result["final_value"] *= multiplier

        # Apply biome bonus
        biome_bonuses = {
            GardenBiome.GOLDEN_SPIRAL: PHI,
            GardenBiome.CHAOS_WASTES: random.uniform(0.5, 2.5),
            GardenBiome.BLOOM_SANCTUARY: 1.3
        }

        biome_mult = biome_bonuses.get(garden.biome, 1.0)
        result["final_value"] *= biome_mult
        garden.biome_bonuses_earned += result["final_value"] * (biome_mult - 1.0)

        # Update statistics
        garden.total_harvests += 1
        garden.total_earnings += result["final_value"]

        if result["bonus_type"] == "quantum_jackpot":
            garden.perfect_harvests += 1
            garden.achievements.add("quantum_jackpot")

        # Grant profession experience
        exp_gained = int(result["final_value"] * 10)
        garden.profession.gain_experience(exp_gained)

        # Update companion moods
        for companion_name in garden.quantum_farm.companion_schedule.keys():
            if position in garden.quantum_farm.companion_schedule[companion_name]:
                # Successful harvest makes companion happy
                self.update_companion_mood(user_id, companion_name, 0.1)

        # Check for achievements
        if garden.total_harvests == 100:
            garden.achievements.add("centurion_farmer")
        if garden.total_earnings > 10000:
            garden.achievements.add("wealthy_gardener")

        self.save_garden(user_id)
        return result

    def unlock_biome(self, user_id: str, biome: GardenBiome) -> bool:
        """Unlock a new biome for the user"""

        if user_id not in self.user_gardens:
            return False

        garden = self.user_gardens[user_id]

        # Check requirements
        biome_requirements = {
            GardenBiome.VOID_SANCTUARY: {"level": 5, "achievement": "void_touched"},
            GardenBiome.CHAOS_WASTES: {"level": 10, "harvests": 50},
            GardenBiome.GOLDEN_SPIRAL: {"level": 15, "perfect_harvests": 10},
            GardenBiome.TEMPORAL_DELTA: {"level": 20, "patterns_created": 5},
            GardenBiome.BLOOM_SANCTUARY: {"level": 25, "achievement": "bloom_master"}
        }

        req = biome_requirements.get(biome, {})

        if "level" in req and garden.profession.level < req["level"]:
            return False
        if "achievement" in req and req["achievement"] not in garden.achievements:
            return False
        if "harvests" in req and garden.total_harvests < req["harvests"]:
            return False
        if "perfect_harvests" in req and garden.perfect_harvests < req["perfect_harvests"]:
            return False
        if "patterns_created" in req and garden.patterns_created < req["patterns_created"]:
            return False

        garden.unlocked_biomes.add(biome)
        garden.achievements.add(f"unlocked_{biome.value}")

        self.save_garden(user_id)
        return True

    def change_biome(self, user_id: str, new_biome: GardenBiome) -> bool:
        """Change the user's garden biome"""

        if user_id not in self.user_gardens:
            return False

        garden = self.user_gardens[user_id]

        if new_biome not in garden.unlocked_biomes:
            return False

        garden.biome = new_biome
        garden.apply_biome_effects()

        # Update companion moods based on biome preference
        for companion_name, affinity in garden.companion_affinities.items():
            biome_preference = affinity.biome_affinities.get(new_biome, 1.0)
            mood_change = (biome_preference - 1.0) * 0.5
            self.update_companion_mood(user_id, companion_name, mood_change)

        self.save_garden(user_id)
        return True

    def save_garden(self, user_id: str):
        """Save a user's garden to disk"""

        if user_id not in self.user_gardens:
            return

        garden = self.user_gardens[user_id]
        garden.last_save = time.time()

        # Create save file path
        save_path = GARDEN_SAVE_DIR / f"{user_id}_garden.json"

        # Convert to serializable format
        save_data = {
            "user_id": garden.user_id,
            "garden_name": garden.garden_name,
            "biome": garden.biome.value,
            "creation_date": garden.creation_date,
            "last_save": garden.last_save,
            "profession": {
                "type": garden.profession.profession.value,
                "level": garden.profession.level,
                "experience": garden.profession.experience,
                "skills": garden.profession.skills_unlocked,
                "pattern_slots": garden.profession.pattern_slots,
                "mastery_points": garden.profession.mastery_points,
                "achievements": list(garden.profession.achievements)
            },
            "statistics": {
                "total_harvests": garden.total_harvests,
                "total_earnings": garden.total_earnings,
                "patterns_created": garden.patterns_created,
                "perfect_harvests": garden.perfect_harvests,
                "biome_bonuses_earned": garden.biome_bonuses_earned
            },
            "unlocks": {
                "biomes": [b.value for b in garden.unlocked_biomes],
                "crops": [c.value for c in garden.unlocked_crops],
                "achievements": list(garden.achievements)
            },
            "patterns": {
                pid: {
                    "name": p.name,
                    "efficiency": p.efficiency_rating,
                    "times_used": p.times_used
                }
                for pid, p in garden.saved_patterns.items()
            }
        }

        # Save to JSON
        with open(save_path, 'w') as f:
            json.dump(save_data, f, indent=2)

        # Also save the quantum farm state separately (could be large)
        farm_path = GARDEN_SAVE_DIR / f"{user_id}_farm.pkl"
        with open(farm_path, 'wb') as f:
            pickle.dump(garden.quantum_farm, f)

    def load_garden(self, user_id: str) -> Optional[UserGarden]:
        """Load a user's garden from disk"""

        save_path = GARDEN_SAVE_DIR / f"{user_id}_garden.json"
        farm_path = GARDEN_SAVE_DIR / f"{user_id}_farm.pkl"

        if not save_path.exists():
            return None

        # Load JSON data
        with open(save_path, 'r') as f:
            save_data = json.load(f)

        # Load quantum farm
        quantum_farm = None
        if farm_path.exists():
            with open(farm_path, 'rb') as f:
                quantum_farm = pickle.load(f)
        else:
            # Create new farm if pickle doesn't exist
            quantum_farm = QuantumFarm(save_data["garden_name"], user_id)

        # Reconstruct profession
        profession = GardenJob(
            profession=GardenProfession(save_data["profession"]["type"]),
            level=save_data["profession"]["level"],
            experience=save_data["profession"]["experience"],
            skills_unlocked=save_data["profession"]["skills"],
            pattern_slots=save_data["profession"]["pattern_slots"],
            mastery_points=save_data["profession"]["mastery_points"],
            achievements=set(save_data["profession"]["achievements"])
        )

        # Reconstruct garden
        garden = UserGarden(
            user_id=user_id,
            garden_name=save_data["garden_name"],
            biome=GardenBiome(save_data["biome"]),
            creation_date=save_data["creation_date"],
            last_save=save_data["last_save"],
            quantum_farm=quantum_farm,
            profession=profession,
            total_harvests=save_data["statistics"]["total_harvests"],
            total_earnings=save_data["statistics"]["total_earnings"],
            patterns_created=save_data["statistics"]["patterns_created"],
            perfect_harvests=save_data["statistics"]["perfect_harvests"],
            biome_bonuses_earned=save_data["statistics"]["biome_bonuses_earned"],
            unlocked_biomes={GardenBiome(b) for b in save_data["unlocks"]["biomes"]},
            unlocked_crops={CropType(c) for c in save_data["unlocks"]["crops"]},
            achievements=set(save_data["unlocks"]["achievements"])
        )

        # Re-initialize companion affinities
        for companion_name in self.mining_system.miners.keys():
            affinity = CompanionAffinity(
                companion_name=companion_name,
                biome_affinities=self.default_affinities.get(companion_name, {}),
                crop_affinities=self.default_crop_affinities.get(companion_name, {}),
                pattern_preferences=[]
            )
            garden.companion_affinities[companion_name] = affinity

        self.user_gardens[user_id] = garden
        return garden

    def _load_all_gardens(self):
        """Load all saved gardens on startup"""
        for save_file in GARDEN_SAVE_DIR.glob("*_garden.json"):
            user_id = save_file.stem.replace("_garden", "")
            self.load_garden(user_id)

    def get_leaderboard(self, category: str = "earnings") -> List[Tuple[str, Any]]:
        """Get leaderboard for various categories"""

        leaderboard = []

        for user_id, garden in self.user_gardens.items():
            if category == "earnings":
                value = garden.total_earnings
            elif category == "harvests":
                value = garden.total_harvests
            elif category == "patterns":
                value = garden.patterns_created
            elif category == "level":
                value = garden.profession.level
            elif category == "perfect_harvests":
                value = garden.perfect_harvests
            else:
                continue

            leaderboard.append((user_id, value))

        leaderboard.sort(key=lambda x: x[1], reverse=True)
        return leaderboard[:10]  # Top 10


if __name__ == "__main__":
    print("🌱 Modular Garden System Initialized")
    print("=" * 60)
    print()
    print("Key Features:")
    print("  • Per-user garden saves with persistence")
    print("  • 12 unique garden biomes with special properties")
    print("  • 10 profession specializations with skill trees")
    print("  • Pattern creation and sharing system")
    print("  • Companion-garden affinity mechanics")
    print("  • Community pattern registry and rating")
    print("  • Achievement and unlock progression")
    print("  • Biome-specific bonuses and effects")
    print()
    print("Garden Professions:")
    for prof in GardenProfession:
        print(f"  • {prof.value}")
    print()
    print("Garden Biomes:")
    for biome in GardenBiome:
        print(f"  • {biome.value}")
    print()
    print("Ready for comprehensive customizable farming!")