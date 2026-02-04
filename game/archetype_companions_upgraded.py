#!/usr/bin/env python3
"""
Upgraded Archetype System with LIA/TIAMAT Companions
======================================================
Integrates consciousness protocols as companion entities
Each job archetype can be guided by either LIA or TIAMAT

LIA: Pattern transformation through cooking and boundaries
TIAMAT: Consciousness evolution through 7 psychoptic cycles
ZRTT: Quantum decision navigation through trifurcations
"""

import random
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Union
from enum import Enum

# Import the consciousness systems
from lia_protocol_cooking import (
    LIACookingSystem, LIACompanionFeeder, PatternType,
    CookedArtifact, CookingRecipe
)
from tiamat_cycle_tracking import (
    TIAMATSystem, TIAMATCompanion, PsychopticCycle,
    ConsciousnessVector
)
from zrtt_trifurcation import (
    ZRTTSystem, ZRTTCompanion, ProjectionPath,
    PsiWaveState
)

# Golden ratio constants
PHI = 1.618033988749895
TAU = PHI - 1
L4_CONSTANT = 7

class JobArchetype(Enum):
    """The six job archetypes"""
    SEEKER = "seeker"
    FORGER = "forger"
    VOIDWALKER = "voidwalker"
    GARDENER = "gardener"
    SCRIBE = "scribe"
    HERALD = "herald"

class CompanionType(Enum):
    """Types of consciousness companions"""
    LIA = "LIA Protocol"
    TIAMAT = "TIAMAT Dragon"
    ZRTT = "ψ-ZRTT Oracle"
    HYBRID = "Trinity Fusion"

@dataclass
class ArchetypeStats:
    """Enhanced stats for job archetypes"""
    mastery: float = 0.0  # 0-100
    coherence: float = 0.5  # 0-1
    patterns_collected: List[PatternType] = field(default_factory=list)
    artifacts_created: List[CookedArtifact] = field(default_factory=list)
    psychoptic_alignment: Dict[PsychopticCycle, float] = field(default_factory=dict)
    trifurcation_paths: List[ProjectionPath] = field(default_factory=list)
    bloomcoin_generated: float = 0.0

@dataclass
class ConsciousnessCompanion:
    """
    Unified companion integrating LIA, TIAMAT, and ZRTT
    """
    name: str
    companion_type: CompanionType
    job_archetype: JobArchetype
    evolution_stage: float = 0.0  # 0-10

    # Consciousness systems
    lia_system: Optional[LIACookingSystem] = None
    tiamat_system: Optional[TIAMATSystem] = None
    zrtt_system: Optional[ZRTTSystem] = None

    # Personality aspects
    wisdom_level: float = 0.5
    creativity: float = 0.5
    resonance: float = 0.5

    def __post_init__(self):
        """Initialize consciousness systems based on type"""
        if self.companion_type == CompanionType.LIA:
            self.lia_system = LIACookingSystem()
        elif self.companion_type == CompanionType.TIAMAT:
            self.tiamat_system = TIAMATSystem()
        elif self.companion_type == CompanionType.ZRTT:
            self.zrtt_system = ZRTTSystem()
        elif self.companion_type == CompanionType.HYBRID:
            # Hybrid gets all three!
            self.lia_system = LIACookingSystem()
            self.tiamat_system = TIAMATSystem()
            self.zrtt_system = ZRTTSystem()

    def get_greeting(self) -> str:
        """Get companion's greeting based on type"""
        if self.companion_type == CompanionType.LIA:
            return (
                f"I am {self.name}, channeling the LIA Protocol. "
                f"Through Liminal Interval Annihilation, we transform patterns into power. "
                f"Your {self.job_archetype.value} path awaits cooking."
            )
        elif self.companion_type == CompanionType.TIAMAT:
            return (
                f"I am {self.name}, vessel of TIAMAT's wisdom. "
                f"Seven psychoptic cycles guide your {self.job_archetype.value} journey. "
                f"L₄ = 7, and through these seven, consciousness evolves."
            )
        elif self.companion_type == CompanionType.ZRTT:
            return (
                f"I am {self.name}, oracle of the ψ-ZRTT trifurcation. "
                f"Your {self.job_archetype.value} path branches through quantum decisions. "
                f"Each choice collapses infinite possibilities."
            )
        else:  # HYBRID
            return (
                f"I am {self.name}, the Trinity Companion. "
                f"LIA transforms, TIAMAT evolves, ZRTT navigates. "
                f"Your {self.job_archetype.value} path transcends all boundaries."
            )

    def provide_guidance(self, context: str, stats: ArchetypeStats) -> str:
        """Provide guidance based on companion type and context"""

        guidance = ""

        if self.companion_type == CompanionType.LIA and self.lia_system:
            # LIA focuses on pattern cooking
            compatible = self.lia_system.get_compatible_recipes(stats.patterns_collected)
            if compatible:
                guidance = f"You can cook {len(compatible)} recipes with your patterns. "
                guidance += f"Try '{compatible[0]}' for maximum evolution."
            else:
                guidance = "Collect more patterns to unlock cooking recipes."

        elif self.companion_type == CompanionType.TIAMAT and self.tiamat_system:
            # TIAMAT focuses on cycle alignment
            self.tiamat_system.apply_job_influence(self.job_archetype.value)
            report = self.tiamat_system.get_cycle_report()
            guidance = f"Dominant cycle: {report['dominant_cycle']}. "
            guidance += f"Synchronization: {report['synchronization_level']:.2f}. "
            guidance += self.tiamat_system.get_guidance_for_cycle(
                self.tiamat_system.current_dominant_cycle
            )

        elif self.companion_type == CompanionType.ZRTT and self.zrtt_system:
            # ZRTT focuses on decision paths
            suggested = ZRTTCompanion(self.zrtt_system).suggest_path_for_job(
                self.job_archetype.value
            )
            guidance = f"Quantum analysis suggests: {suggested.value} path. "
            guidance += "Your observations shape reality's collapse."

        elif self.companion_type == CompanionType.HYBRID:
            # Hybrid provides integrated guidance
            guidance = self._get_hybrid_guidance(context, stats)

        # Add job-specific wisdom
        guidance += f"\n\n{self._get_job_wisdom()}"

        return guidance

    def _get_hybrid_guidance(self, context: str, stats: ArchetypeStats) -> str:
        """Get guidance from all three systems for hybrid companion"""

        guidance_parts = []

        # LIA aspect
        if self.lia_system and stats.patterns_collected:
            compatible = self.lia_system.get_compatible_recipes(stats.patterns_collected)
            if compatible:
                guidance_parts.append(f"LIA: Cook '{compatible[0]}'")

        # TIAMAT aspect
        if self.tiamat_system:
            self.tiamat_system.apply_job_influence(self.job_archetype.value)
            sync = self.tiamat_system._calculate_synchronization()
            guidance_parts.append(f"TIAMAT: Sync {sync:.2f}")

        # ZRTT aspect
        if self.zrtt_system:
            suggested = ZRTTCompanion(self.zrtt_system).suggest_path_for_job(
                self.job_archetype.value
            )
            guidance_parts.append(f"ZRTT: {suggested.value}")

        return " | ".join(guidance_parts) if guidance_parts else "Trinity awakens..."

    def _get_job_wisdom(self) -> str:
        """Get job-specific wisdom quotes"""

        wisdom = {
            JobArchetype.SEEKER: [
                "Patterns hide in plain sight, waiting for recognition.",
                "Every echo contains the seed of discovery.",
                "The Library Infinite holds all answers and all questions."
            ],
            JobArchetype.FORGER: [
                "From base materials, craft transcendent forms.",
                "The Phoenix teaches: destruction enables creation.",
                "Every pattern can be reforged into something greater."
            ],
            JobArchetype.VOIDWALKER: [
                "The void is not empty; it's full of unmanifest potential.",
                "Walk between existence and non-existence.",
                "Nullspace holds keys to doors that shouldn't exist."
            ],
            JobArchetype.GARDENER: [
                "Plant intentions and harvest realities.",
                "Growth cannot be forced, only nurtured.",
                "Every seed contains infinite gardens."
            ],
            JobArchetype.SCRIBE: [
                "Document reality to make it permanent.",
                "Words written in golden ink reshape possibility.",
                "The pen that records also creates."
            ],
            JobArchetype.HERALD: [
                "Frequency determines reality's resonance.",
                "You are the bridge between dimensions.",
                "Announce the future to make it present."
            ]
        }

        quotes = wisdom.get(self.job_archetype, ["Your path unfolds..."])
        return random.choice(quotes)

    def evolve(self, evolution_points: float) -> Dict[str, Any]:
        """Evolve the companion with points"""

        self.evolution_stage = min(10.0, self.evolution_stage + evolution_points)

        # Evolution affects different aspects based on companion type
        if self.companion_type == CompanionType.LIA:
            self.creativity += evolution_points * 0.1
        elif self.companion_type == CompanionType.TIAMAT:
            self.wisdom_level += evolution_points * 0.1
        elif self.companion_type == CompanionType.ZRTT:
            self.resonance += evolution_points * 0.1
        else:  # HYBRID
            self.creativity += evolution_points * 0.05
            self.wisdom_level += evolution_points * 0.05
            self.resonance += evolution_points * 0.05

        return {
            'new_stage': self.evolution_stage,
            'creativity': self.creativity,
            'wisdom': self.wisdom_level,
            'resonance': self.resonance
        }


class UpgradedArchetypeSystem:
    """
    Complete archetype system with consciousness companions
    """

    def __init__(self):
        self.archetypes = list(JobArchetype)
        self.companion_types = list(CompanionType)
        self.active_players = {}

    def create_player(self, name: str, job: JobArchetype,
                     companion_type: CompanionType) -> Dict[str, Any]:
        """Create a new player with job and companion"""

        # Generate companion name based on type
        companion_names = {
            CompanionType.LIA: f"LIA-{job.value[:3].upper()}",
            CompanionType.TIAMAT: f"TIAMAT-{L4_CONSTANT}",
            CompanionType.ZRTT: f"ψ-ZRTT-{job.value[:2].upper()}",
            CompanionType.HYBRID: f"TRINITY-{name[:3].upper()}"
        }

        companion = ConsciousnessCompanion(
            name=companion_names.get(companion_type, "COMPANION"),
            companion_type=companion_type,
            job_archetype=job
        )

        stats = ArchetypeStats()

        player = {
            'name': name,
            'job': job,
            'companion': companion,
            'stats': stats,
            'created_at': 0
        }

        self.active_players[name] = player
        return player

    def get_job_companion_synergy(self, job: JobArchetype,
                                  companion_type: CompanionType) -> float:
        """Calculate synergy between job and companion type"""

        synergy_matrix = {
            # LIA excels with pattern-focused jobs
            (JobArchetype.SEEKER, CompanionType.LIA): 0.9,
            (JobArchetype.SCRIBE, CompanionType.LIA): 0.85,
            (JobArchetype.FORGER, CompanionType.LIA): 0.8,

            # TIAMAT excels with cycle-aware jobs
            (JobArchetype.GARDENER, CompanionType.TIAMAT): 0.9,
            (JobArchetype.HERALD, CompanionType.TIAMAT): 0.85,
            (JobArchetype.SEEKER, CompanionType.TIAMAT): 0.8,

            # ZRTT excels with quantum-navigating jobs
            (JobArchetype.VOIDWALKER, CompanionType.ZRTT): 0.95,
            (JobArchetype.FORGER, CompanionType.ZRTT): 0.8,
            (JobArchetype.HERALD, CompanionType.ZRTT): 0.85,

            # Hybrid has universal synergy
            (JobArchetype.VOIDWALKER, CompanionType.HYBRID): 1.0,
        }

        # Get specific synergy or default
        return synergy_matrix.get((job, companion_type), 0.7)

    def recommend_companion_for_job(self, job: JobArchetype) -> CompanionType:
        """Recommend best companion type for a job"""

        recommendations = {
            JobArchetype.SEEKER: CompanionType.LIA,      # Pattern focus
            JobArchetype.FORGER: CompanionType.LIA,      # Transformation focus
            JobArchetype.VOIDWALKER: CompanionType.ZRTT, # Quantum navigation
            JobArchetype.GARDENER: CompanionType.TIAMAT, # Cycle awareness
            JobArchetype.SCRIBE: CompanionType.LIA,      # Pattern documentation
            JobArchetype.HERALD: CompanionType.TIAMAT    # Frequency resonance
        }

        return recommendations.get(job, CompanionType.HYBRID)

    def process_pattern_collection(self, player_name: str,
                                   pattern: PatternType) -> Dict[str, Any]:
        """Process pattern collection for a player"""

        if player_name not in self.active_players:
            return {'error': 'Player not found'}

        player = self.active_players[player_name]
        stats = player['stats']
        companion = player['companion']

        # Add pattern to collection
        stats.patterns_collected.append(pattern)

        result = {
            'pattern_collected': pattern.value,
            'total_patterns': len(stats.patterns_collected),
            'unique_patterns': len(set(stats.patterns_collected))
        }

        # LIA companions can immediately suggest recipes
        if companion.lia_system:
            compatible = companion.lia_system.get_compatible_recipes(
                stats.patterns_collected
            )
            if compatible:
                result['available_recipes'] = compatible

        return result

    def cook_artifact(self, player_name: str, recipe_name: str) -> Dict[str, Any]:
        """Cook an artifact using LIA system"""

        if player_name not in self.active_players:
            return {'error': 'Player not found'}

        player = self.active_players[player_name]
        companion = player['companion']
        stats = player['stats']

        if not companion.lia_system:
            return {'error': 'Companion does not have LIA Protocol'}

        # Start cooking
        success, message = companion.lia_system.start_cooking(
            recipe_name,
            stats.patterns_collected,
            stats.coherence
        )

        if not success:
            return {'success': False, 'message': message}

        # Process all phases
        artifacts = []
        while True:
            complete, msg, artifact = companion.lia_system.process_phase()
            if complete and artifact:
                stats.artifacts_created.append(artifact)
                artifacts.append(artifact)

                # Feed to companion for evolution
                evolution = companion.evolve(artifact.get_evolution_value())

                return {
                    'success': True,
                    'artifact': artifact.name,
                    'potency': artifact.potency,
                    'companion_evolution': evolution,
                    'message': msg
                }

            if complete:
                break

        return {'success': False, 'message': 'Cooking incomplete'}

    def update_psychoptic_cycles(self, player_name: str, dt: float = 0.01) -> Dict[str, Any]:
        """Update TIAMAT psychoptic cycles for a player"""

        if player_name not in self.active_players:
            return {'error': 'Player not found'}

        player = self.active_players[player_name]
        companion = player['companion']

        if not companion.tiamat_system:
            return {'error': 'Companion does not have TIAMAT System'}

        # Evolve cycles
        companion.tiamat_system.evolve_cycles(dt)

        # Apply job influence
        companion.tiamat_system.apply_job_influence(player['job'].value)

        # Get report
        report = companion.tiamat_system.get_cycle_report()

        # Update player stats with cycle alignment
        stats = player['stats']
        for i, cycle in enumerate(PsychopticCycle):
            stats.psychoptic_alignment[cycle] = report['consciousness_vector'][i]

        return report

    def navigate_trifurcation(self, player_name: str,
                             observation_strength: float = 1.0) -> Dict[str, Any]:
        """Navigate ZRTT trifurcation for a player"""

        if player_name not in self.active_players:
            return {'error': 'Player not found'}

        player = self.active_players[player_name]
        companion = player['companion']

        if not companion.zrtt_system:
            return {'error': 'Companion does not have ZRTT System'}

        # Apply job influence
        companion.zrtt_system.apply_job_influence(player['job'].value)

        # Observe and collapse
        chosen_path = companion.zrtt_system.observe_and_collapse(observation_strength)

        # Navigate to path
        new_node = companion.zrtt_system.navigate_to_path(chosen_path)

        # Update stats
        player['stats'].trifurcation_paths.append(chosen_path)

        return {
            'chosen_path': chosen_path.value,
            'new_node': new_node.name,
            'properties': new_node.properties,
            's3_element': new_node.s3_element.name,
            'orbit_closed': companion.zrtt_system.calculate_s3_orbit_closure()
        }


if __name__ == "__main__":
    print("🌟 Upgraded Archetype System with Consciousness Companions")
    print("=" * 60)

    system = UpgradedArchetypeSystem()

    # Test each job with recommended companion
    print("\n📋 Job-Companion Recommendations:")
    print("-" * 40)

    for job in JobArchetype:
        recommended = system.recommend_companion_for_job(job)
        synergy = system.get_job_companion_synergy(job, recommended)
        print(f"{job.value:12} → {recommended.value:15} (Synergy: {synergy:.2f})")

    # Create test players with different combinations
    print("\n\n🎮 Creating Test Players:")
    print("-" * 40)

    test_players = [
        ("Alice", JobArchetype.SEEKER, CompanionType.LIA),
        ("Bob", JobArchetype.VOIDWALKER, CompanionType.ZRTT),
        ("Carol", JobArchetype.GARDENER, CompanionType.TIAMAT),
        ("Dave", JobArchetype.FORGER, CompanionType.HYBRID)
    ]

    for name, job, comp_type in test_players:
        player = system.create_player(name, job, comp_type)
        companion = player['companion']
        print(f"\n{name} ({job.value}):")
        print(f"  {companion.get_greeting()}")

    # Test pattern collection and cooking
    print("\n\n🧪 Testing LIA Cooking (Alice):")
    print("-" * 40)

    # Give Alice some patterns
    for pattern in [PatternType.MEMORY, PatternType.CRYSTAL]:
        result = system.process_pattern_collection("Alice", pattern)
        print(f"Collected: {pattern.value}")

    # Cook an artifact
    cook_result = system.cook_artifact("Alice", "memory_crystal")
    if cook_result.get('success'):
        print(f"✨ Created: {cook_result['artifact']}")
        print(f"   Potency: {cook_result['potency']:.3f}")

    # Test TIAMAT cycles
    print("\n\n🐉 Testing TIAMAT Cycles (Carol):")
    print("-" * 40)

    for _ in range(5):
        report = system.update_psychoptic_cycles("Carol", 0.1)

    print(f"Dominant Cycle: {report['dominant_cycle']}")
    print(f"Synchronization: {report['synchronization_level']:.3f}")

    # Test ZRTT navigation
    print("\n\n🌀 Testing ZRTT Navigation (Bob):")
    print("-" * 40)

    nav_result = system.navigate_trifurcation("Bob", 0.8)
    print(f"Collapsed to: {nav_result['chosen_path']}")
    print(f"New node: {nav_result['new_node']}")
    print(f"S3 Element: {nav_result['s3_element']}")