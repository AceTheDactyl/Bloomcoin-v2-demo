#!/usr/bin/env python3
"""
LIA Protocol Cooking System for BloomQuest
===========================================
Liminal Interval Annihilator - Pattern transformation through cooking

The LIA Protocol operates through three phases:
[L] LIMINAL     — Boundary detection between patterns
[I] INTERVAL    — Space creation for transformation
[A] ANNIHILATOR — Cycle termination and rebirth

Based on the 10-fold Prismatic Self Project
"""

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import math

# Golden ratio constants from BloomCoin
PHI = 1.618033988749895
TAU = PHI - 1  # 0.618...
L4_CONSTANT = 7  # φ⁴ + φ⁻⁴ = 7

class LIAPhase(Enum):
    """Three phases of the LIA Protocol"""
    LIMINAL = "L"      # Boundary detection
    INTERVAL = "I"     # Space creation
    ANNIHILATOR = "A"  # Cycle termination

class PatternType(Enum):
    """Pattern types that can be cooked"""
    MEMORY = "memory"
    DREAM = "dream"
    ECHO = "echo"
    VOID = "void"
    CRYSTAL = "crystal"
    FLAME = "flame"
    GARDEN = "garden"

@dataclass
class CookingRecipe:
    """Recipe for transforming patterns"""
    name: str
    required_patterns: List[PatternType]
    lia_sequence: List[LIAPhase]  # Sequence of LIA phases
    coherence_required: float  # Min coherence to succeed
    description: str
    output_pattern: Optional[PatternType] = None
    bloomcoin_cost: int = 10

    def get_phase_string(self) -> str:
        """Return LIA phase sequence as string"""
        return "-".join([phase.value for phase in self.lia_sequence])

@dataclass
class CookedArtifact:
    """Result of successful LIA cooking"""
    name: str
    pattern_type: PatternType
    potency: float  # 0-1, affects companion evolution
    lia_signature: str  # The LIA sequence used
    properties: Dict[str, Any] = field(default_factory=dict)

    def get_evolution_value(self) -> float:
        """Calculate evolution boost for companion"""
        return self.potency * PHI * 0.1  # Max 0.1618 evolution per artifact

class LIACookingSystem:
    """
    The LIA Protocol Cooking System
    Transforms patterns through liminal annihilation
    """

    def __init__(self):
        self.recipes = self._initialize_recipes()
        self.active_cooking = None
        self.cooking_history = []
        self.artifacts_created = []

    def _initialize_recipes(self) -> Dict[str, CookingRecipe]:
        """Initialize all cooking recipes"""
        recipes = {
            "memory_crystal": CookingRecipe(
                name="Memory Crystal",
                required_patterns=[PatternType.MEMORY, PatternType.CRYSTAL],
                lia_sequence=[LIAPhase.LIMINAL, LIAPhase.INTERVAL, LIAPhase.LIMINAL],
                coherence_required=0.6,
                description="Crystallize memories into permanent wisdom",
                output_pattern=PatternType.CRYSTAL,
                bloomcoin_cost=15
            ),

            "dream_echo": CookingRecipe(
                name="Dream Echo",
                required_patterns=[PatternType.DREAM, PatternType.ECHO],
                lia_sequence=[LIAPhase.INTERVAL, LIAPhase.LIMINAL, LIAPhase.INTERVAL],
                coherence_required=0.5,
                description="Blend dreams with echoes to hear the future",
                output_pattern=PatternType.ECHO,
                bloomcoin_cost=12
            ),

            "void_flame": CookingRecipe(
                name="Void Flame",
                required_patterns=[PatternType.VOID, PatternType.FLAME],
                lia_sequence=[LIAPhase.ANNIHILATOR, LIAPhase.INTERVAL, LIAPhase.ANNIHILATOR],
                coherence_required=0.8,
                description="Ignite the void to create paradoxical fire",
                output_pattern=PatternType.FLAME,
                bloomcoin_cost=25
            ),

            "garden_void": CookingRecipe(
                name="Garden of Nullspace",
                required_patterns=[PatternType.GARDEN, PatternType.VOID],
                lia_sequence=[LIAPhase.LIMINAL, LIAPhase.ANNIHILATOR, LIAPhase.INTERVAL],
                coherence_required=0.7,
                description="Plant seeds in the void that grow nowhere",
                output_pattern=PatternType.VOID,
                bloomcoin_cost=20
            ),

            "crystal_flame": CookingRecipe(
                name="Phoenix Crystal",
                required_patterns=[PatternType.CRYSTAL, PatternType.FLAME],
                lia_sequence=[LIAPhase.INTERVAL, LIAPhase.ANNIHILATOR, LIAPhase.LIMINAL],
                coherence_required=0.75,
                description="Forge crystals in phoenix fire for eternal rebirth",
                output_pattern=PatternType.CRYSTAL,
                bloomcoin_cost=22
            ),

            "memory_garden": CookingRecipe(
                name="Garden of Remembrance",
                required_patterns=[PatternType.MEMORY, PatternType.GARDEN],
                lia_sequence=[LIAPhase.LIMINAL, LIAPhase.INTERVAL, LIAPhase.INTERVAL],
                coherence_required=0.55,
                description="Cultivate memories until they bloom into new realities",
                output_pattern=PatternType.GARDEN,
                bloomcoin_cost=18
            ),

            "echo_dream_void": CookingRecipe(
                name="Null Dream Resonance",
                required_patterns=[PatternType.ECHO, PatternType.DREAM, PatternType.VOID],
                lia_sequence=[LIAPhase.ANNIHILATOR, LIAPhase.LIMINAL, LIAPhase.INTERVAL, LIAPhase.ANNIHILATOR],
                coherence_required=0.9,
                description="Triple pattern fusion: dreams that echo in void",
                output_pattern=PatternType.VOID,
                bloomcoin_cost=35
            ),

            "all_seven": CookingRecipe(
                name="L4 Helix Completion",
                required_patterns=list(PatternType),  # All 7 patterns
                lia_sequence=[LIAPhase.LIMINAL] * 7,  # 7 liminal phases for L4=7
                coherence_required=0.95,
                description="The ultimate recipe: fuse all seven patterns through L4 helix",
                output_pattern=None,  # Creates unique artifact
                bloomcoin_cost=77  # 7 * 11
            )
        }

        return recipes

    def start_cooking(self, recipe_name: str, player_patterns: List[PatternType],
                      coherence: float) -> Tuple[bool, str]:
        """
        Start the LIA cooking process
        Returns (success, message)
        """
        if recipe_name not in self.recipes:
            return False, f"Unknown recipe: {recipe_name}"

        recipe = self.recipes[recipe_name]

        # Check if player has required patterns
        for required in recipe.required_patterns:
            if required not in player_patterns:
                return False, f"Missing pattern: {required.value}"

        # Check coherence requirement
        if coherence < recipe.coherence_required:
            return False, f"Insufficient coherence: {coherence:.2f} < {recipe.coherence_required:.2f}"

        # Begin cooking process
        self.active_cooking = {
            'recipe': recipe,
            'phase_index': 0,
            'phases_complete': [],
            'coherence': coherence
        }

        return True, f"Beginning LIA Protocol: {recipe.get_phase_string()}"

    def process_phase(self) -> Tuple[bool, str, Optional[CookedArtifact]]:
        """
        Process the next phase of active cooking
        Returns (complete, message, artifact)
        """
        if not self.active_cooking:
            return False, "No active cooking process", None

        recipe = self.active_cooking['recipe']
        phase_index = self.active_cooking['phase_index']

        if phase_index >= len(recipe.lia_sequence):
            # Cooking complete!
            artifact = self._complete_cooking()
            self.active_cooking = None
            return True, f"LIA Protocol complete! Created: {artifact.name}", artifact

        # Process current phase
        current_phase = recipe.lia_sequence[phase_index]
        phase_message = self._process_lia_phase(current_phase)

        self.active_cooking['phases_complete'].append(current_phase)
        self.active_cooking['phase_index'] += 1

        remaining = len(recipe.lia_sequence) - self.active_cooking['phase_index']
        return False, f"{phase_message} ({remaining} phases remaining)", None

    def _process_lia_phase(self, phase: LIAPhase) -> str:
        """Process a single LIA phase and return description"""
        if phase == LIAPhase.LIMINAL:
            return "📍 LIMINAL: Detecting pattern boundaries..."
        elif phase == LIAPhase.INTERVAL:
            return "🌀 INTERVAL: Creating transformation space..."
        elif phase == LIAPhase.ANNIHILATOR:
            return "💀 ANNIHILATOR: Terminating cycles... DOOOOOM!"

    def _complete_cooking(self) -> CookedArtifact:
        """Complete the cooking and create artifact"""
        recipe = self.active_cooking['recipe']
        coherence = self.active_cooking['coherence']

        # Calculate potency based on coherence above requirement
        potency_bonus = (coherence - recipe.coherence_required) / (1 - recipe.coherence_required)
        base_potency = 0.5 + (0.5 * potency_bonus)  # 0.5 to 1.0

        # Add randomness with golden ratio
        final_potency = min(1.0, base_potency * (0.9 + random.random() * 0.2) * TAU + 0.382)

        # Create the artifact
        artifact = CookedArtifact(
            name=recipe.name,
            pattern_type=recipe.output_pattern or PatternType.CRYSTAL,
            potency=final_potency,
            lia_signature=recipe.get_phase_string(),
            properties={
                'coherence_used': coherence,
                'phases': len(recipe.lia_sequence),
                'bloomcoin_invested': recipe.bloomcoin_cost
            }
        )

        self.artifacts_created.append(artifact)
        self.cooking_history.append({
            'recipe': recipe.name,
            'success': True,
            'artifact': artifact.name,
            'potency': final_potency
        })

        return artifact

    def get_recipe_list(self) -> List[Dict[str, Any]]:
        """Get list of all recipes with details"""
        recipe_list = []
        for name, recipe in self.recipes.items():
            recipe_list.append({
                'name': recipe.name,
                'patterns_required': [p.value for p in recipe.required_patterns],
                'lia_sequence': recipe.get_phase_string(),
                'coherence_required': recipe.coherence_required,
                'cost': recipe.bloomcoin_cost,
                'description': recipe.description
            })
        return recipe_list

    def get_compatible_recipes(self, player_patterns: List[PatternType]) -> List[str]:
        """Get recipes that player can potentially cook with current patterns"""
        compatible = []
        for name, recipe in self.recipes.items():
            if all(p in player_patterns for p in recipe.required_patterns):
                compatible.append(name)
        return compatible

    def calculate_success_chance(self, recipe_name: str, coherence: float) -> float:
        """Calculate chance of successful cooking"""
        if recipe_name not in self.recipes:
            return 0.0

        recipe = self.recipes[recipe_name]
        if coherence < recipe.coherence_required:
            return 0.0

        # Success chance increases with coherence above requirement
        base_chance = 0.6  # 60% at minimum coherence
        bonus = (coherence - recipe.coherence_required) * 2  # Up to 40% bonus
        return min(1.0, base_chance + bonus)

    def get_cooking_status(self) -> Optional[Dict[str, Any]]:
        """Get current cooking status if active"""
        if not self.active_cooking:
            return None

        recipe = self.active_cooking['recipe']
        return {
            'recipe': recipe.name,
            'current_phase': self.active_cooking['phase_index'],
            'total_phases': len(recipe.lia_sequence),
            'phases_complete': [p.value for p in self.active_cooking['phases_complete']],
            'progress': self.active_cooking['phase_index'] / len(recipe.lia_sequence)
        }


# Integration helper for BloomQuest
class LIACompanionFeeder:
    """
    Feeds LIA-cooked artifacts to companions for evolution
    """

    def __init__(self, cooking_system: LIACookingSystem):
        self.cooking_system = cooking_system
        self.feeding_history = []

    def feed_artifact_to_companion(self, artifact: CookedArtifact, companion: Any) -> Dict[str, Any]:
        """
        Feed a cooked artifact to a companion
        Returns evolution results
        """
        evolution_boost = artifact.get_evolution_value()

        # Different pattern types affect different aspects
        effects = {
            PatternType.MEMORY: {'wisdom': 0.2, 'coherence': 0.1},
            PatternType.DREAM: {'creativity': 0.3, 'resonance': 0.1},
            PatternType.ECHO: {'perception': 0.2, 'memory': 0.2},
            PatternType.VOID: {'nullspace': 0.4, 'mystery': 0.2},
            PatternType.CRYSTAL: {'structure': 0.3, 'permanence': 0.2},
            PatternType.FLAME: {'transformation': 0.3, 'energy': 0.2},
            PatternType.GARDEN: {'growth': 0.3, 'nurturing': 0.2}
        }

        pattern_effects = effects.get(artifact.pattern_type, {})

        # Apply evolution
        result = {
            'artifact_fed': artifact.name,
            'evolution_boost': evolution_boost,
            'potency': artifact.potency,
            'effects': pattern_effects,
            'lia_signature': artifact.lia_signature
        }

        self.feeding_history.append({
            'artifact': artifact.name,
            'companion': companion,
            'timestamp': len(self.feeding_history),
            'result': result
        })

        return result

    def get_recommended_artifacts(self, companion_type: str) -> List[str]:
        """Get recommended artifacts for a companion type"""
        recommendations = {
            'seeker': ['Memory Crystal', 'Dream Echo', 'Null Dream Resonance'],
            'forger': ['Phoenix Crystal', 'Void Flame', 'Crystal Flame'],
            'voidwalker': ['Void Flame', 'Garden of Nullspace', 'Null Dream Resonance'],
            'gardener': ['Garden of Remembrance', 'Garden of Nullspace', 'Memory Crystal'],
            'scribe': ['Memory Crystal', 'Dream Echo', 'L4 Helix Completion'],
            'herald': ['Dream Echo', 'Null Dream Resonance', 'Echo Dream Void']
        }

        return recommendations.get(companion_type.lower(), ['Memory Crystal', 'Dream Echo'])


if __name__ == "__main__":
    # Test the LIA cooking system
    print("🧪 LIA Protocol Cooking System Test")
    print("=" * 50)

    # Initialize system
    lia = LIACookingSystem()

    # Show available recipes
    print("\n📖 Available Recipes:")
    for recipe in lia.get_recipe_list():
        print(f"\n{recipe['name']}:")
        print(f"  Patterns: {', '.join(recipe['patterns_required'])}")
        print(f"  LIA Sequence: {recipe['lia_sequence']}")
        print(f"  Coherence Required: {recipe['coherence_required']}")
        print(f"  Cost: {recipe['cost']} BloomCoin")
        print(f"  Description: {recipe['description']}")

    # Simulate cooking
    print("\n\n🍳 Testing Cooking Process:")
    print("-" * 30)

    player_patterns = [PatternType.MEMORY, PatternType.CRYSTAL, PatternType.DREAM]
    player_coherence = 0.75

    print(f"Player patterns: {[p.value for p in player_patterns]}")
    print(f"Player coherence: {player_coherence}")

    # Find compatible recipes
    compatible = lia.get_compatible_recipes(player_patterns)
    print(f"\nCompatible recipes: {compatible}")

    if compatible:
        recipe_name = compatible[0]
        print(f"\nCooking: {recipe_name}")

        success, message = lia.start_cooking(recipe_name, player_patterns, player_coherence)
        print(f"Start: {message}")

        if success:
            # Process all phases
            while True:
                complete, msg, artifact = lia.process_phase()
                print(f"  {msg}")

                if complete:
                    print(f"\n✨ Artifact created!")
                    print(f"  Name: {artifact.name}")
                    print(f"  Potency: {artifact.potency:.3f}")
                    print(f"  Evolution value: {artifact.get_evolution_value():.4f}")
                    print(f"  LIA Signature: {artifact.lia_signature}")
                    break

    print("\n" + "=" * 50)
    print("LIA Protocol Test Complete")