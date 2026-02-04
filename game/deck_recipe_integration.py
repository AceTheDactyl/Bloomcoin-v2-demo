"""
Deck and Recipe Integration System
===================================
Connects guardian decks with the recipe crafting system
Allows recipes to unlock cards and deck mechanics
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set, Tuple
from enum import Enum
import random
from datetime import datetime, timedelta
from collections import defaultdict

from guardian_deck_system import (
    GuardianCard, CardType, CardEffect, MathConcept, Architecture,
    DeckManager, ComboSystem
)
from guardian_decks_extended import get_complete_deck_library, DeckStrategies
from guardian_pattern_recipes import (
    GuardianPatternSystem, GuardianRecipe, PatternType,
    RecipeComplexity, GUARDIAN_RECIPES
)
from mythic_economy import GUARDIANS

# ═══════════════════════════════════════════════════════════════════════
#   CARD CRAFTING RECIPES
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class CardRecipe:
    """Recipe for crafting a specific card"""
    card_name: str
    guardian_key: str
    required_patterns: Dict[str, int]  # Pattern name -> quantity
    required_recipe: Optional[str] = None  # Recipe that must be completed first
    bloomcoin_cost: int = 100
    craft_time: int = 60  # seconds
    unlock_condition: Optional[str] = None

class CardCraftingSystem:
    """System for crafting cards through recipes"""

    def __init__(self):
        self.deck_library = get_complete_deck_library()
        self.card_recipes: Dict[str, CardRecipe] = self._generate_card_recipes()
        self.unlocked_cards: Dict[str, Set[str]] = defaultdict(set)  # player_id -> card names
        self.crafting_queue: List[Tuple[str, str, datetime]] = []  # player_id, card_name, completion

    def _generate_card_recipes(self) -> Dict[str, CardRecipe]:
        """Generate crafting recipes for all cards"""
        recipes = {}

        for guardian_key, deck in self.deck_library.items():
            for card in deck:
                # Generate recipe based on card properties
                recipe = self._create_card_recipe(card, guardian_key)
                recipes[f"{guardian_key}:{card.name}"] = recipe

        return recipes

    def _create_card_recipe(self, card: GuardianCard, guardian_key: str) -> CardRecipe:
        """Create a recipe for a specific card"""
        # Base patterns required
        patterns = {}

        # Determine patterns based on card type
        if card.card_type == CardType.ATTACK:
            patterns["Kinetic Energy"] = max(1, card.attack // 2)
            patterns["Force Pattern"] = 1
        elif card.card_type == CardType.DEFENSE:
            patterns["Shield Matrix"] = max(1, card.defense // 2)
            patterns["Stability Pattern"] = 1
        elif card.card_type == CardType.QUANTUM:
            patterns["Quantum Thread"] = 3
            patterns["Probability Wave"] = 2
        elif card.card_type == CardType.VOID:
            patterns["Void Echo"] = card.void_depth + 1
            patterns["Nullspace Fragment"] = 2
        elif card.card_type == CardType.CHAOS:
            patterns["Chaos Seed"] = int(card.chaos_factor) + 1
            patterns["Entropy Crystal"] = 2
        elif card.card_type == CardType.PATTERN:
            patterns["Pattern Template"] = 2
            patterns["Mathematical Proof"] = 1
        elif card.card_type == CardType.TRANSFORMATION:
            patterns["Metamorphic Essence"] = 2
            patterns["Change Catalyst"] = 3
        else:
            patterns["Universal Pattern"] = 2

        # Add patterns for mathematical concepts
        for concept in card.math_concepts:
            if concept == MathConcept.HILBERT_SPACE:
                patterns["Dimensional Fragment"] = 2
            elif concept == MathConcept.FRACTAL:
                patterns["Recursive Pattern"] = 3
            elif concept == MathConcept.GOLDEN_RATIO:
                patterns["Golden Spiral"] = 1
            elif concept == MathConcept.FIBONACCI:
                patterns["Fibonacci Sequence"] = 2

        # Add patterns for architecture
        if card.architecture:
            if card.architecture == Architecture.NETWORK:
                patterns["Network Node"] = 3
            elif card.architecture == Architecture.CRYSTALLINE:
                patterns["Crystal Lattice"] = 2
            elif card.architecture == Architecture.VOID_SPACE:
                patterns["Void Architecture"] = 2
            elif card.architecture == Architecture.ORGANIC:
                patterns["Organic Blueprint"] = 2

        # Calculate cost based on card power
        base_cost = card.cost * 100
        if card.combo_with:
            base_cost += len(card.combo_with) * 200
        if card.requires_pattern or card.requires_state:
            base_cost += 500

        return CardRecipe(
            card_name=card.name,
            guardian_key=guardian_key,
            required_patterns=patterns,
            required_recipe=None,  # Will be set based on combo relationships
            bloomcoin_cost=base_cost,
            craft_time=card.cost * 30,  # 30 seconds per cost
            unlock_condition=card.requires_pattern or card.requires_state
        )

    def can_craft_card(self, player_id: str, card_key: str,
                       pattern_system: GuardianPatternSystem) -> Tuple[bool, List[str]]:
        """Check if player can craft a card"""
        recipe = self.card_recipes.get(card_key)
        if not recipe:
            return False, ["Card recipe not found"]

        missing = []

        # Check patterns
        player_patterns = pattern_system.player_patterns[player_id]
        for pattern, quantity in recipe.required_patterns.items():
            if player_patterns.get(pattern, 0) < quantity:
                missing.append(f"Need {quantity} {pattern}, have {player_patterns.get(pattern, 0)}")

        # Check bloomcoin
        balance = pattern_system.get_player_balance(player_id)
        if balance < recipe.bloomcoin_cost:
            missing.append(f"Need {recipe.bloomcoin_cost} BloomCoin, have {balance}")

        # Check unlock condition
        if recipe.unlock_condition and recipe.unlock_condition not in self.unlocked_cards[player_id]:
            missing.append(f"Requires: {recipe.unlock_condition}")

        return len(missing) == 0, missing

    def craft_card(self, player_id: str, card_key: str,
                  pattern_system: GuardianPatternSystem) -> Dict[str, Any]:
        """Craft a card using patterns"""
        can_craft, missing = self.can_craft_card(player_id, card_key, pattern_system)

        if not can_craft:
            return {
                "success": False,
                "error": "Cannot craft card",
                "missing": missing
            }

        recipe = self.card_recipes[card_key]

        # Consume patterns
        for pattern, quantity in recipe.required_patterns.items():
            pattern_system.player_patterns[player_id][pattern] -= quantity

        # Deduct bloomcoin
        pattern_system.deduct_bloomcoin(player_id, recipe.bloomcoin_cost)

        # Add to crafting queue
        completion_time = datetime.now() + timedelta(seconds=recipe.craft_time)
        self.crafting_queue.append((player_id, card_key, completion_time))

        # Unlock the card
        self.unlocked_cards[player_id].add(card_key)

        return {
            "success": True,
            "card": recipe.card_name,
            "guardian": recipe.guardian_key,
            "completion_time": completion_time.isoformat()
        }

# ═══════════════════════════════════════════════════════════════════════
#   DECK BUILDING WITH RECIPES
# ═══════════════════════════════════════════════════════════════════════

class DeckRecipeBuilder:
    """Build and enhance decks using recipes"""

    def __init__(self, pattern_system: GuardianPatternSystem):
        self.pattern_system = pattern_system
        self.card_crafting = CardCraftingSystem()
        self.deck_manager = DeckManager()
        self.player_custom_decks: Dict[str, List[GuardianCard]] = {}
        self.deck_bonuses: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))

    def create_custom_deck(self, player_id: str, guardian_key: str,
                          selected_cards: Optional[List[str]] = None) -> Dict[str, Any]:
        """Create a custom deck using unlocked cards"""
        all_cards = self.deck_manager.all_decks.get(guardian_key, [])
        unlocked = self.card_crafting.unlocked_cards[player_id]

        # Filter to unlocked cards
        available_cards = []
        for card in all_cards:
            card_key = f"{guardian_key}:{card.name}"
            if not selected_cards or card.name in selected_cards:
                if card_key in unlocked or card.cost <= 2:  # Basic cards always available
                    available_cards.append(card)

        # Ensure minimum deck size
        if len(available_cards) < 8:
            # Add basic cards to fill
            for card in all_cards:
                if card.cost <= 2 and card not in available_cards:
                    available_cards.append(card)
                if len(available_cards) >= 8:
                    break

        self.player_custom_decks[player_id] = available_cards

        # Calculate deck synergy
        synergy = DeckStrategies.calculate_deck_synergy(available_cards)

        return {
            "success": True,
            "guardian": guardian_key,
            "deck_size": len(available_cards),
            "synergy_score": synergy,
            "cards": [card.name for card in available_cards]
        }

    def apply_recipe_bonus_to_deck(self, player_id: str, recipe: GuardianRecipe) -> Dict[str, Any]:
        """Apply recipe bonuses to player's deck"""
        bonuses = self.deck_bonuses[player_id]

        # Apply bonuses based on recipe type
        if recipe.pattern_type == PatternType.RESONANCE:
            bonuses["echo_multiplier"] += 0.2
        elif recipe.pattern_type == PatternType.QUANTUM:
            bonuses["quantum_states"] += 1
        elif recipe.pattern_type == PatternType.VOID:
            bonuses["void_depth"] += 1
        elif recipe.pattern_type == PatternType.CHAOS:
            bonuses["chaos_factor"] += 0.5
        elif recipe.pattern_type == PatternType.ORGANIC:
            bonuses["growth_rate"] += 0.3

        # Special ability bonuses
        for ability in recipe.special_abilities:
            if "Echo" in ability:
                bonuses["echo_power"] += 0.1
            if "Void" in ability:
                bonuses["void_power"] += 0.1
            if "Transform" in ability:
                bonuses["transform_speed"] += 0.2

        # Battle strategy bonuses
        if "damage over time" in recipe.battle_strategy:
            bonuses["dot_damage"] += 0.3
        if "defense" in recipe.battle_strategy.lower():
            bonuses["defense_multiplier"] += 0.2
        if "amplif" in recipe.battle_strategy.lower():
            bonuses["amplification"] += 0.25

        return {
            "success": True,
            "recipe": recipe.name,
            "bonuses_applied": dict(bonuses),
            "total_bonus": sum(bonuses.values())
        }

    def enhance_card_with_pattern(self, player_id: str, card_key: str,
                                  pattern_name: str, quantity: int = 1) -> Dict[str, Any]:
        """Enhance a card using patterns"""
        # Check if player has the pattern
        player_patterns = self.pattern_system.player_patterns[player_id]
        if player_patterns.get(pattern_name, 0) < quantity:
            return {
                "success": False,
                "error": f"Insufficient {pattern_name}"
            }

        # Find the card
        guardian_key, card_name = card_key.split(":")
        deck = self.deck_manager.all_decks.get(guardian_key, [])
        card = next((c for c in deck if c.name == card_name), None)

        if not card:
            return {"success": False, "error": "Card not found"}

        # Consume pattern
        player_patterns[pattern_name] -= quantity

        # Apply enhancement based on pattern type
        enhancement_applied = {}

        if "Kinetic" in pattern_name:
            card.attack += quantity
            enhancement_applied["attack"] = quantity
        elif "Shield" in pattern_name:
            card.defense += quantity
            enhancement_applied["defense"] = quantity
        elif "Quantum" in pattern_name:
            card.quantum_states += 1
            enhancement_applied["quantum_states"] = 1
        elif "Void" in pattern_name:
            card.void_depth += 1
            enhancement_applied["void_depth"] = 1
        elif "Chaos" in pattern_name:
            card.chaos_factor += 0.5
            enhancement_applied["chaos_factor"] = 0.5

        return {
            "success": True,
            "card": card_name,
            "pattern_used": pattern_name,
            "enhancements": enhancement_applied,
            "new_stats": {
                "attack": card.attack,
                "defense": card.defense,
                "cost": card.cost
            }
        }

# ═══════════════════════════════════════════════════════════════════════
#   PATTERN TO CARD CONVERSION
# ═══════════════════════════════════════════════════════════════════════

class PatternCardConverter:
    """Convert patterns into cards through special processes"""

    def __init__(self):
        self.conversion_rates = {
            PatternType.RESONANCE: 3,  # 3 patterns -> 1 card
            PatternType.QUANTUM: 5,
            PatternType.VOID: 4,
            PatternType.CHAOS: 3,
            PatternType.ORGANIC: 2,
            PatternType.CRYSTALLINE: 4,
            PatternType.TEMPORAL: 5,
            PatternType.ELEMENTAL: 3,
            PatternType.HARMONIC: 3,
            PatternType.MEMORY: 4
        }

    def convert_patterns_to_card_pack(self, player_id: str, pattern_type: PatternType,
                                      pattern_quantity: int,
                                      pattern_system: GuardianPatternSystem) -> Dict[str, Any]:
        """Convert patterns into a card pack"""
        rate = self.conversion_rates.get(pattern_type, 5)
        packs_available = pattern_quantity // rate

        if packs_available == 0:
            return {
                "success": False,
                "error": f"Need {rate} patterns of type {pattern_type.value}",
                "have": pattern_quantity
            }

        # Generate cards based on pattern type
        cards = self._generate_cards_from_pattern(pattern_type, packs_available)

        return {
            "success": True,
            "packs_created": packs_available,
            "patterns_consumed": packs_available * rate,
            "cards_received": cards
        }

    def _generate_cards_from_pattern(self, pattern_type: PatternType,
                                     num_packs: int) -> List[Dict[str, Any]]:
        """Generate cards based on pattern type"""
        cards = []
        library = get_complete_deck_library()

        for _ in range(num_packs):
            # Find cards that match the pattern type
            matching_cards = []

            for guardian_key, deck in library.items():
                for card in deck:
                    # Check if card matches pattern theme
                    if self._card_matches_pattern(card, pattern_type):
                        matching_cards.append({
                            "guardian": guardian_key,
                            "card": card.name,
                            "type": card.card_type.value,
                            "cost": card.cost
                        })

            # Select random cards from matching pool
            if matching_cards:
                num_cards = min(3, len(matching_cards))
                selected = random.sample(matching_cards, num_cards)
                cards.extend(selected)

        return cards

    def _card_matches_pattern(self, card: GuardianCard, pattern_type: PatternType) -> bool:
        """Check if a card matches a pattern type"""
        if pattern_type == PatternType.RESONANCE:
            return card.card_type == CardType.RESONANCE or "echo" in card.name.lower()
        elif pattern_type == PatternType.QUANTUM:
            return card.card_type == CardType.QUANTUM or card.quantum_states > 1
        elif pattern_type == PatternType.VOID:
            return card.card_type == CardType.VOID or card.void_depth > 0
        elif pattern_type == PatternType.CHAOS:
            return card.card_type == CardType.CHAOS or card.chaos_factor > 0
        elif pattern_type == PatternType.ORGANIC:
            return card.architecture == Architecture.ORGANIC
        elif pattern_type == PatternType.TEMPORAL:
            return card.card_type == CardType.TEMPORAL
        elif pattern_type == PatternType.CRYSTALLINE:
            return card.architecture == Architecture.CRYSTALLINE
        else:
            return random.random() < 0.3  # 30% chance for other types

# ═══════════════════════════════════════════════════════════════════════
#   INTEGRATED DECK-RECIPE SYSTEM
# ═══════════════════════════════════════════════════════════════════════

class IntegratedDeckRecipeSystem:
    """Complete integration of decks and recipes"""

    def __init__(self):
        self.pattern_system = GuardianPatternSystem()
        self.deck_builder = DeckRecipeBuilder(self.pattern_system)
        self.pattern_converter = PatternCardConverter()
        self.card_crafting = CardCraftingSystem()

        # Track player progress
        self.player_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "cards_crafted": 0,
            "recipes_completed": 0,
            "patterns_converted": 0,
            "deck_synergy": 0.0,
            "battle_wins": 0
        })

    def complete_recipe_unlock_cards(self, player_id: str, recipe: GuardianRecipe) -> Dict[str, Any]:
        """Complete a recipe and unlock related cards"""
        guardian_key = recipe.guardian_key
        deck = self.deck_builder.deck_manager.all_decks.get(guardian_key, [])

        # Find cards that synergize with this recipe
        unlocked_cards = []
        for card in deck:
            # Check if card relates to recipe abilities
            for ability in recipe.special_abilities:
                if ability.lower() in card.name.lower() or \
                   any(ability.lower() in tag for tag in card.synergy_tags):
                    card_key = f"{guardian_key}:{card.name}"
                    self.card_crafting.unlocked_cards[player_id].add(card_key)
                    unlocked_cards.append(card.name)
                    break

        # Apply deck bonuses
        bonus_result = self.deck_builder.apply_recipe_bonus_to_deck(player_id, recipe)

        # Update stats
        self.player_stats[player_id]["recipes_completed"] += 1

        return {
            "success": True,
            "recipe": recipe.name,
            "cards_unlocked": unlocked_cards,
            "deck_bonuses": bonus_result["bonuses_applied"],
            "total_cards_unlocked": len(self.card_crafting.unlocked_cards[player_id])
        }

    def farm_patterns_get_cards(self, player_id: str, farm_yield: Dict[str, int]) -> Dict[str, Any]:
        """Convert farmed patterns into cards"""
        cards_received = []

        for pattern_name, quantity in farm_yield.items():
            # Determine pattern type
            pattern_type = self._determine_pattern_type(pattern_name)

            # Try to convert to cards
            conversion_result = self.pattern_converter.convert_patterns_to_card_pack(
                player_id, pattern_type, quantity, self.pattern_system
            )

            if conversion_result["success"]:
                cards_received.extend(conversion_result["cards_received"])
                self.player_stats[player_id]["patterns_converted"] += conversion_result["patterns_consumed"]

        return {
            "success": True,
            "patterns_farmed": farm_yield,
            "cards_received": cards_received,
            "total_conversions": self.player_stats[player_id]["patterns_converted"]
        }

    def _determine_pattern_type(self, pattern_name: str) -> PatternType:
        """Determine pattern type from name"""
        name_lower = pattern_name.lower()

        if "echo" in name_lower or "signal" in name_lower:
            return PatternType.RESONANCE
        elif "quantum" in name_lower or "probability" in name_lower:
            return PatternType.QUANTUM
        elif "void" in name_lower or "null" in name_lower:
            return PatternType.VOID
        elif "chaos" in name_lower or "random" in name_lower:
            return PatternType.CHAOS
        elif "organic" in name_lower or "seed" in name_lower:
            return PatternType.ORGANIC
        elif "crystal" in name_lower or "lattice" in name_lower:
            return PatternType.CRYSTALLINE
        elif "time" in name_lower or "temporal" in name_lower:
            return PatternType.TEMPORAL
        elif "memory" in name_lower or "data" in name_lower:
            return PatternType.MEMORY
        else:
            return PatternType.ELEMENTAL

    def get_player_deck_summary(self, player_id: str, guardian_key: str) -> Dict[str, Any]:
        """Get summary of player's deck progress"""
        unlocked_cards = self.card_crafting.unlocked_cards[player_id]
        deck = self.deck_builder.deck_manager.all_decks.get(guardian_key, [])

        # Calculate unlock percentage
        total_cards = len(deck)
        unlocked_count = sum(1 for card in deck
                           if f"{guardian_key}:{card.name}" in unlocked_cards)

        # Get deck bonuses
        bonuses = self.deck_builder.deck_bonuses[player_id]

        # Get custom deck if exists
        custom_deck = self.deck_builder.player_custom_decks.get(player_id, [])
        synergy = DeckStrategies.calculate_deck_synergy(custom_deck) if custom_deck else 0

        return {
            "guardian": guardian_key,
            "total_cards": total_cards,
            "unlocked_cards": unlocked_count,
            "unlock_percentage": (unlocked_count / total_cards * 100) if total_cards > 0 else 0,
            "deck_bonuses": dict(bonuses),
            "deck_synergy": synergy,
            "player_stats": dict(self.player_stats[player_id])
        }

# ═══════════════════════════════════════════════════════════════════════
#   DEMONSTRATION
# ═══════════════════════════════════════════════════════════════════════

def demonstrate_integration():
    """Demonstrate the deck-recipe integration"""
    print("\n" + "=" * 70)
    print("DECK-RECIPE INTEGRATION DEMONSTRATION")
    print("=" * 70)

    system = IntegratedDeckRecipeSystem()
    player_id = "test_player"

    # Initialize player
    system.pattern_system.add_bloomcoin(player_id, 10000)
    system.pattern_system.player_patterns[player_id] = {
        "Kinetic Energy": 10,
        "Shield Matrix": 8,
        "Quantum Thread": 15,
        "Void Echo": 12,
        "Signal Fragment": 20
    }

    print("\n1. CRAFTING CARDS FROM PATTERNS")
    print("-" * 40)

    # Try to craft an Echo card
    echo_card = "ECHO:Recursive Echo"
    can_craft, missing = system.card_crafting.can_craft_card(
        player_id, echo_card, system.pattern_system
    )

    print(f"Attempting to craft: Recursive Echo (ECHO)")
    if can_craft:
        result = system.card_crafting.craft_card(player_id, echo_card, system.pattern_system)
        print(f"  ✓ Crafted successfully!")
        print(f"    Completion time: {result['completion_time']}")
    else:
        print(f"  ✗ Cannot craft:")
        for miss in missing[:3]:
            print(f"    - {miss}")

    print("\n2. RECIPE COMPLETION UNLOCKS CARDS")
    print("-" * 40)

    # Complete a recipe and unlock cards
    echo_recipe = GUARDIAN_RECIPES["ECHO"][0]  # First Echo recipe
    unlock_result = system.complete_recipe_unlock_cards(player_id, echo_recipe)

    print(f"Completed Recipe: {echo_recipe.name}")
    print(f"  Cards Unlocked: {len(unlock_result['cards_unlocked'])}")
    for card in unlock_result['cards_unlocked'][:3]:
        print(f"    - {card}")
    print(f"  Deck Bonuses Applied:")
    for bonus, value in list(unlock_result['deck_bonuses'].items())[:3]:
        print(f"    - {bonus}: +{value:.2f}")

    print("\n3. PATTERN TO CARD CONVERSION")
    print("-" * 40)

    # Convert patterns to cards
    conversion_result = system.pattern_converter.convert_patterns_to_card_pack(
        player_id, PatternType.RESONANCE, 15, system.pattern_system
    )

    if conversion_result["success"]:
        print(f"Converted {conversion_result['patterns_consumed']} Resonance patterns")
        print(f"  Packs Created: {conversion_result['packs_created']}")
        print(f"  Cards Received: {len(conversion_result['cards_received'])}")
        for card_info in conversion_result['cards_received'][:3]:
            print(f"    - {card_info['card']} ({card_info['guardian']})")

    print("\n4. CUSTOM DECK BUILDING")
    print("-" * 40)

    # Create custom deck
    deck_result = system.deck_builder.create_custom_deck(player_id, "ECHO")

    print(f"Created Custom Deck for ECHO:")
    print(f"  Deck Size: {deck_result['deck_size']} cards")
    print(f"  Synergy Score: {deck_result['synergy_score']:.1f}")
    print(f"  Cards in Deck:")
    for card_name in deck_result['cards'][:5]:
        print(f"    - {card_name}")

    print("\n5. FARMING YIELDS CARDS")
    print("-" * 40)

    # Simulate farming yield
    farm_yield = {
        "Echo Pattern": 10,
        "Signal Fragment": 15,
        "Void Echo": 8
    }

    farm_result = system.farm_patterns_get_cards(player_id, farm_yield)

    print(f"Farm Harvest Results:")
    print(f"  Patterns Farmed: {sum(farm_yield.values())}")
    print(f"  Cards Received: {len(farm_result['cards_received'])}")
    print(f"  Total Patterns Converted: {farm_result['total_conversions']}")

    print("\n6. PLAYER PROGRESS SUMMARY")
    print("-" * 40)

    summary = system.get_player_deck_summary(player_id, "ECHO")

    print(f"Player Deck Progress (ECHO):")
    print(f"  Cards Unlocked: {summary['unlocked_cards']}/{summary['total_cards']} ({summary['unlock_percentage']:.1f}%)")
    print(f"  Deck Synergy: {summary['deck_synergy']:.1f}")
    print(f"  Player Stats:")
    for stat, value in summary['player_stats'].items():
        print(f"    - {stat}: {value}")

    print("\n" + "=" * 70)
    print("INTEGRATION FEATURES:")
    print("  ✓ Cards craftable from patterns")
    print("  ✓ Recipes unlock related cards")
    print("  ✓ Pattern farming yields cards")
    print("  ✓ Deck bonuses from recipes")
    print("  ✓ Card enhancement with patterns")
    print("  ✓ Custom deck building")
    print("  ✓ Progress tracking")
    print("=" * 70)

if __name__ == "__main__":
    demonstrate_integration()