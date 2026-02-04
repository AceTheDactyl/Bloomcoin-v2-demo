#!/usr/bin/env python3
"""
LIA-Powered Deck Generation System
===================================
Transforms collected patterns and LIA cooking artifacts into tesseract battle cards.
Features the legendary DOOM recipe that creates reality-breaking cards.
"""

import random
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum

# Import cooking and battle systems
from lia_protocol_cooking import (
    LIACookingSystem, LIAPhase, PatternType,
    CookedArtifact, CookingRecipe
)
from tesseract_battle_enhanced import (
    EnhancedTesseractCard, CardSuit, CardRank,
    CardEffect, CardAction, TesseractDimension
)
from archetype_unique_companions import (
    SeekerCompanion, ForgerCompanion, VoidwalkerCompanion,
    GardenerCompanion, ScribeCompanion, HeraldCompanion
)

# Constants
PHI = 1.618033988749895
TAU = PHI - 1
L4_CONSTANT = 7
DOOM_CONSTANT = PHI ** 7  # φ⁷ for DOOM power

# ============================================================================
# DOOM RECIPE EXTENSION
# ============================================================================

class DoomIngredient(Enum):
    """Special ingredients for DOOM recipe"""
    VOID_ESSENCE = "void_essence"
    PHOENIX_ASH = "phoenix_ash"
    ECHO_FRAGMENT = "echo_fragment"
    CRYSTAL_DUST = "crystal_dust"
    MEMORY_SHARD = "memory_shard"
    DREAM_VAPOR = "dream_vapor"
    GARDEN_SEED = "garden_seed"
    FLAME_CORE = "flame_core"
    TESSERACT_FRAGMENT = "tesseract_fragment"
    CONSCIOUSNESS_BLOOM = "consciousness_bloom"

@dataclass
class DoomRecipe(CookingRecipe):
    """The legendary DOOM recipe"""

    def __init__(self):
        super().__init__(
            name="LIA DOOM Protocol",
            required_patterns=[
                PatternType.VOID, PatternType.VOID,  # Double void
                PatternType.FLAME, PatternType.CRYSTAL,
                PatternType.ECHO
            ],
            lia_sequence=[
                LIAPhase.ANNIHILATOR,  # Destroy
                LIAPhase.ANNIHILATOR,  # Obliterate
                LIAPhase.ANNIHILATOR,  # Erase
                LIAPhase.LIMINAL,       # Boundary
                LIAPhase.ANNIHILATOR,  # Terminate
                LIAPhase.INTERVAL,      # Space
                LIAPhase.ANNIHILATOR   # DOOM
            ],
            coherence_required=0.99,  # Nearly perfect coherence required
            description="D.O.O.M: Dimensional Obliteration Of Matter - Reality itself trembles",
            output_pattern=None,  # Creates DOOM artifact
            bloomcoin_cost=666
        )
        self.special_ingredients = [
            DoomIngredient.VOID_ESSENCE,
            DoomIngredient.PHOENIX_ASH,
            DoomIngredient.TESSERACT_FRAGMENT
        ]

# ============================================================================
# CARD GENERATION SYSTEM
# ============================================================================

class CardRarity(Enum):
    """Card rarity tiers"""
    COMMON = (1, "Common", 0.5)
    UNCOMMON = (2, "Uncommon", 0.3)
    RARE = (3, "Rare", 0.15)
    EPIC = (4, "Epic", 0.04)
    LEGENDARY = (5, "Legendary", 0.009)
    DOOM = (6, "DOOM", 0.001)  # Only from DOOM recipe

class GeneratedCard(EnhancedTesseractCard):
    """A card generated from patterns/artifacts"""

    def __init__(self, suit: CardSuit, rank: CardRank,
                 position_4d: Tuple[float, float, float, float],
                 dimension: TesseractDimension,
                 rarity: CardRarity,
                 source_artifact: Optional[CookedArtifact] = None,
                 companion_bonus: Optional[str] = None,
                 generation_seed: int = 0):
        """Initialize a generated card"""
        super().__init__(suit, rank, position_4d, dimension)
        self.rarity = rarity
        self.source_artifact = source_artifact
        self.companion_bonus = companion_bonus
        self.generation_seed = generation_seed

        # Calculate base power from rank and rarity
        rank_power = self._get_rank_power()
        rarity_bonus = rarity.value[0] * 10  # Use rarity level for bonus
        self.power = rank_power + rarity_bonus

        # Apply companion bonus to power if present
        if companion_bonus:
            self.power *= 1.2  # 20% bonus from companion

        if self.source_artifact:
            self._enhance_from_artifact()

    def _get_rank_power(self) -> float:
        """Get base power from card rank"""
        # Map rank to power (handle both tuple and int values)
        rank_value = self.rank.value[0] if isinstance(self.rank.value, tuple) else self.rank.value
        return float(rank_value * 10)

    def _enhance_from_artifact(self):
        """Enhance card based on source artifact"""
        # Add artifact potency to card power
        potency_bonus = self.source_artifact.potency
        self.power += potency_bonus * PHI

        # Modify actions based on artifact pattern
        pattern_effects = {
            PatternType.VOID: CardEffect.ERASE,
            PatternType.FLAME: CardEffect.DAMAGE,
            PatternType.CRYSTAL: CardEffect.RESONATE,
            PatternType.ECHO: CardEffect.DRAW,
            PatternType.DREAM: CardEffect.TRANSFORM,
            PatternType.MEMORY: CardEffect.ELEVATE,
            PatternType.GARDEN: CardEffect.HEAL
        }

        artifact_effect = pattern_effects.get(
            self.source_artifact.pattern_type,
            CardEffect.DAMAGE
        )

        # Add special action from artifact
        self.actions.append(
            CardAction(
                effect=artifact_effect,
                power=potency_bonus * PHI,
                target="opponent" if artifact_effect == CardEffect.DAMAGE else "self"
            )
        )

class DoomCard(GeneratedCard):
    """The legendary DOOM card - reality-breaking power"""

    def __init__(self, position_4d: Tuple[float, float, float, float] = (0, 0, 0, 0)):
        """Create the ultimate DOOM card"""
        super().__init__(
            suit=CardSuit.QUANTUM,  # Use QUANTUM for maximum void energy
            rank=CardRank.KING,  # Highest standard rank
            position_4d=position_4d,
            dimension=TesseractDimension.HYPERCELL,  # Full 4D tesseract
            rarity=CardRarity.DOOM
        )
        self.is_doom = True
        self.power = float('inf')
        self.reality_status = "BROKEN"

        # Override actions with DOOM-specific ones
        self.actions = [
            CardAction(
                effect=CardEffect.ERASE,
                power=float('inf'),
                target="all"
            ),
            CardAction(
                effect=CardEffect.TRANSFORM,
                power=999,
                target="reality"
            )
        ]

class DeckGenerator:
    """Generates cards from patterns and artifacts"""

    def __init__(self):
        self.cooking_system = LIACookingSystem()
        self._add_doom_recipe()
        self.generation_history = []
        self.doom_cards_created = 0

    def _add_doom_recipe(self):
        """Add the DOOM recipe to cooking system"""
        doom = DoomRecipe()
        self.cooking_system.recipes["doom_protocol"] = doom

    def cook_artifact(self, artifact: Dict) -> CookedArtifact:
        """Transform a raw artifact dict into a cooked artifact"""
        # Map artifact type to pattern
        type_to_pattern = {
            "weapon": PatternType.FLAME,
            "armor": PatternType.CRYSTAL,
            "mystic": PatternType.ECHO,
            "void": PatternType.VOID,
            "quantum": PatternType.DREAM,
            "memory": PatternType.MEMORY
        }

        pattern = type_to_pattern.get(artifact.get("type", "mystic"), PatternType.ECHO)

        # Create cooked artifact with potency based on power
        power = artifact.get("power", 50)
        potency = min(power / 100.0, 1.0)  # Normalize to 0-1

        # Generate LIA signature based on artifact properties
        lia_signature = f"L-{pattern.value[0].upper()}-I-{int(potency * 10)}-A"

        return CookedArtifact(
            name=artifact.get("name", "Unknown Artifact"),
            pattern_type=pattern,
            potency=potency,
            lia_signature=lia_signature,
            properties=artifact
        )

    def generate_card_from_pattern(self,
                                  pattern: PatternType,
                                  companion: Optional[Any] = None) -> GeneratedCard:
        """Generate a basic card from a single pattern"""

        # Map patterns to suits
        pattern_suits = {
            PatternType.VOID: CardSuit.QUANTUM,
            PatternType.FLAME: CardSuit.COSMOS,
            PatternType.CRYSTAL: CardSuit.PSYCHE,
            PatternType.ECHO: CardSuit.CHRONOS,
            PatternType.DREAM: CardSuit.PSYCHE,
            PatternType.MEMORY: CardSuit.CHRONOS,
            PatternType.GARDEN: CardSuit.COSMOS
        }

        suit = pattern_suits.get(pattern, CardSuit.COSMOS)

        # Random rank weighted by rarity
        rank = self._generate_rank(CardRarity.COMMON)

        # Generate 4D position
        position = self._generate_position()

        # Random dimension
        dimension = random.choice(list(TesseractDimension))

        # Create card
        card = GeneratedCard(
            suit=suit,
            rank=rank,
            position_4d=position,
            dimension=dimension,
            rarity=CardRarity.COMMON,
            companion_bonus=companion.name if companion else None
        )

        # Companion enhancement
        if companion:
            card = self._apply_companion_bonus(card, companion)

        self.generation_history.append(card)
        return card

    def generate_card_from_artifact(self,
                                   artifact: CookedArtifact,
                                   companion: Optional[Any] = None) -> GeneratedCard:
        """Generate an enhanced card from a cooked artifact"""

        # Determine rarity based on artifact potency
        rarity = self._determine_rarity(artifact.potency)

        # Special handling for DOOM artifacts
        if "DOOM" in artifact.name or "doom" in artifact.lia_signature.lower():
            rarity = CardRarity.DOOM

        # Generate suit based on artifact pattern
        suit = self._pattern_to_suit(artifact.pattern_type)

        # Higher rank for artifact cards
        rank = self._generate_rank(rarity)

        # Position influenced by LIA signature
        position = self._generate_lia_position(artifact.lia_signature)

        # Dimension based on artifact properties
        dimension = self._artifact_to_dimension(artifact)

        # Create enhanced card
        card = GeneratedCard(
            suit=suit,
            rank=rank,
            position_4d=position,
            dimension=dimension,
            rarity=rarity,
            source_artifact=artifact,
            companion_bonus=companion.name if companion else None
        )

        # Apply companion bonus
        if companion:
            card = self._apply_companion_bonus(card, companion)

        # Special DOOM enhancements
        if rarity == CardRarity.DOOM:
            card = self._apply_doom_enhancement(card)

        self.generation_history.append(card)
        return card

    def cook_doom_card(self,
                      patterns: List[PatternType],
                      ingredients: List[DoomIngredient],
                      companion: Any,
                      coherence: float) -> Optional[GeneratedCard]:
        """
        Attempt to create a DOOM card through the LIA DOOM Protocol
        This is the ultimate card creation requiring perfect conditions
        """

        # Check if we have doom recipe requirements
        if coherence < 0.99:
            print(f"❌ DOOM Protocol requires 99% coherence (current: {coherence:.1%})")
            return None

        required_ingredients = [
            DoomIngredient.VOID_ESSENCE,
            DoomIngredient.PHOENIX_ASH,
            DoomIngredient.TESSERACT_FRAGMENT
        ]

        for ingredient in required_ingredients:
            if ingredient not in ingredients:
                print(f"❌ Missing DOOM ingredient: {ingredient.value}")
                return None

        # Attempt DOOM cooking
        success, message = self.cooking_system.start_cooking(
            "doom_protocol",
            patterns,
            coherence
        )

        if not success:
            print(f"❌ DOOM Protocol failed: {message}")
            return None

        print("🔥 DOOM PROTOCOL INITIATED...")
        print("⚡ Reality warping...")
        print("💀 Dimensional barriers breaking...")

        # Process all DOOM phases
        doom_artifact = None
        while self.cooking_system.active_cooking:
            complete, phase_msg, artifact = self.cooking_system.process_phase()
            print(f"   {phase_msg}")

            if artifact:
                doom_artifact = artifact
                doom_artifact.name = "DOOM Singularity"
                doom_artifact.potency = DOOM_CONSTANT

        if not doom_artifact:
            print("❌ DOOM Protocol collapsed!")
            return None

        # Generate the DOOM card
        print("✨ DOOM CARD MANIFESTING...")

        # DOOM cards are always highest rank
        doom_rank = CardRank.KING  # Highest standard rank

        # DOOM cards exist in all dimensions simultaneously
        doom_position = (PHI, -PHI, PHI**2, -PHI**2)  # Golden ratio coordinates

        # Create the DOOM card
        doom_card = GeneratedCard(
            suit=CardSuit.QUANTUM,  # Quantum for reality manipulation
            rank=doom_rank,
            position_4d=doom_position,
            dimension=TesseractDimension.CELL,  # Highest dimension
            rarity=CardRarity.DOOM,
            source_artifact=doom_artifact,
            companion_bonus=companion.name
        )

        # Apply ALL enhancements
        doom_card = self._apply_companion_bonus(doom_card, companion)
        doom_card = self._apply_doom_enhancement(doom_card)

        # Add DOOM-specific abilities
        doom_card.actions = [
            CardAction(CardEffect.DAMAGE, DOOM_CONSTANT, "all"),
            CardAction(CardEffect.ERASE, PHI**3, "field"),
            CardAction(CardEffect.COLLAPSE, L4_CONSTANT, "all"),
            CardAction(CardEffect.TRANSFORM, PHI**2, "all"),
            CardAction(CardEffect.ELEVATE, 7, "self")  # Instant L4=7
        ]

        self.doom_cards_created += 1
        self.generation_history.append(doom_card)

        print(f"🌟 DOOM CARD #{self.doom_cards_created} CREATED!")
        print(f"   Name: Reality Breaker #{self.doom_cards_created}")
        print(f"   Power: {DOOM_CONSTANT:.2f}")
        print(f"   Effects: OBLITERATE ALL")

        return doom_card

    def feed_patterns_to_companion(self,
                                  companion: Any,
                                  patterns: List[PatternType],
                                  recipe_name: Optional[str] = None) -> List[GeneratedCard]:
        """
        Feed patterns to companion to generate cards
        Can use specific recipe or let companion choose
        """

        generated_cards = []

        # If no recipe specified, companion chooses based on personality
        if not recipe_name:
            recipe_name = self._companion_choose_recipe(companion, patterns)

        # Check if it's the DOOM recipe
        if recipe_name == "doom_protocol":
            # Special DOOM handling
            doom_card = self.cook_doom_card(
                patterns,
                self._gather_doom_ingredients(companion),
                companion,
                0.99  # Assume max coherence for DOOM attempt
            )
            if doom_card:
                generated_cards.append(doom_card)

                # Feeding DOOM to companion has consequences
                if hasattr(companion, 'doom_touched'):
                    companion.doom_touched = True
                print(f"⚠️ {companion.name} has been touched by DOOM...")
        else:
            # Normal recipe cooking
            if recipe_name in self.cooking_system.recipes:
                success, message = self.cooking_system.start_cooking(
                    recipe_name,
                    patterns,
                    0.75  # Default coherence
                )

                if success:
                    # Process cooking
                    artifact = None
                    while self.cooking_system.active_cooking:
                        complete, phase_msg, result = self.cooking_system.process_phase()
                        if result:
                            artifact = result

                    if artifact:
                        # Generate card from artifact
                        card = self.generate_card_from_artifact(artifact, companion)
                        generated_cards.append(card)

                        # Companion gains from feeding
                        if hasattr(companion, 'patterns_consumed'):
                            companion.patterns_consumed += len(patterns)

        # Generate basic cards from leftover patterns
        used_patterns = self.cooking_system.recipes.get(
            recipe_name,
            CookingRecipe("", [], [], 0, "", None)
        ).required_patterns if recipe_name else []

        for pattern in patterns:
            if pattern not in used_patterns:
                card = self.generate_card_from_pattern(pattern, companion)
                generated_cards.append(card)

        return generated_cards

    def _generate_rank(self, rarity: CardRarity) -> CardRank:
        """Generate card rank based on rarity"""
        ranks = list(CardRank)

        if rarity == CardRarity.DOOM:
            # DOOM cards are always high rank
            return random.choice(ranks[-3:])  # Jack, Queen, King
        elif rarity == CardRarity.LEGENDARY:
            return random.choice(ranks[-5:])  # 9-King
        elif rarity == CardRarity.EPIC:
            return random.choice(ranks[-7:])  # 7-King
        elif rarity == CardRarity.RARE:
            return random.choice(ranks[4:])  # 5+
        else:
            return random.choice(ranks)

    def _generate_position(self) -> Tuple[float, float, float, float]:
        """Generate 4D position for card"""
        return tuple(random.uniform(-1, 1) for _ in range(4))

    def _generate_lia_position(self, lia_signature: str) -> Tuple[float, float, float, float]:
        """Generate position based on LIA signature"""
        # Use LIA phases to influence position
        position = []
        for phase_char in lia_signature:
            if phase_char == 'L':
                position.append(random.uniform(0.5, 1))  # Liminal = positive
            elif phase_char == 'I':
                position.append(random.uniform(-0.5, 0.5))  # Interval = neutral
            elif phase_char == 'A':
                position.append(random.uniform(-1, -0.5))  # Annihilator = negative
            else:
                position.append(random.uniform(-1, 1))

        # Ensure we have exactly 4 dimensions
        while len(position) < 4:
            position.append(0)

        return tuple(position[:4])

    def _pattern_to_suit(self, pattern: PatternType) -> CardSuit:
        """Convert pattern to card suit"""
        pattern_suits = {
            PatternType.VOID: CardSuit.QUANTUM,
            PatternType.FLAME: CardSuit.COSMOS,
            PatternType.CRYSTAL: CardSuit.PSYCHE,
            PatternType.ECHO: CardSuit.CHRONOS,
            PatternType.DREAM: CardSuit.PSYCHE,
            PatternType.MEMORY: CardSuit.CHRONOS,
            PatternType.GARDEN: CardSuit.COSMOS
        }
        return pattern_suits.get(pattern, CardSuit.COSMOS)

    def _artifact_to_dimension(self, artifact: CookedArtifact) -> TesseractDimension:
        """Determine dimension from artifact"""
        # Use artifact potency to determine dimension
        if artifact.potency > 0.8:
            return TesseractDimension.CELL
        elif artifact.potency > 0.6:
            return TesseractDimension.FACE
        elif artifact.potency > 0.4:
            return TesseractDimension.EDGE
        else:
            return TesseractDimension.VERTEX

    def _determine_rarity(self, potency: float) -> CardRarity:
        """Determine card rarity from artifact potency"""
        if potency >= 1.0:
            return CardRarity.LEGENDARY
        elif potency >= 0.8:
            return CardRarity.EPIC
        elif potency >= 0.6:
            return CardRarity.RARE
        elif potency >= 0.4:
            return CardRarity.UNCOMMON
        else:
            return CardRarity.COMMON

    def _apply_companion_bonus(self, card: GeneratedCard, companion: Any) -> GeneratedCard:
        """Apply companion-specific bonuses to generated card"""

        if isinstance(companion, SeekerCompanion):
            # Echo improves pattern detection
            card.combo_potential *= 1.5

        elif isinstance(companion, ForgerCompanion):
            # Prometheus adds transformation
            card.actions.append(
                CardAction(CardEffect.TRANSFORM, PHI, "self")
            )

        elif isinstance(companion, VoidwalkerCompanion):
            # Null adds erasure
            card.actions.append(
                CardAction(CardEffect.ERASE, 1, "field")
            )

        elif isinstance(companion, GardenerCompanion):
            # Gaia adds growth
            card.actions.append(
                CardAction(CardEffect.HEAL, PHI * 2, "self")
            )

        elif isinstance(companion, ScribeCompanion):
            # Akasha adds consciousness
            card.actions.append(
                CardAction(CardEffect.ELEVATE, 1, "self")
            )

        elif isinstance(companion, HeraldCompanion):
            # Resonance adds area effects
            card.actions.append(
                CardAction(CardEffect.RESONATE, PHI, "all")
            )

        return card

    def _apply_doom_enhancement(self, card: GeneratedCard) -> GeneratedCard:
        """Apply DOOM-level enhancements"""

        # DOOM cards break all limits
        card.combo_potential = DOOM_CONSTANT
        card.resonance = PHI ** 3

        # Exists in superposition
        card.quantum_state = "superposition"

        # Add description
        card.doom_description = "Reality itself bends to your will"

        return card

    def _companion_choose_recipe(self, companion: Any, patterns: List[PatternType]) -> str:
        """Let companion choose recipe based on personality"""

        available_recipes = []

        # Check which recipes can be made with available patterns
        for recipe_name, recipe in self.cooking_system.recipes.items():
            if all(p in patterns for p in recipe.required_patterns):
                available_recipes.append(recipe_name)

        if not available_recipes:
            return None

        # Companion preferences
        if isinstance(companion, SeekerCompanion):
            # Echo prefers echo and memory recipes
            for recipe in ["dream_echo", "memory_crystal"]:
                if recipe in available_recipes:
                    return recipe

        elif isinstance(companion, ForgerCompanion):
            # Prometheus prefers flame recipes
            for recipe in ["void_flame", "crystal_flame"]:
                if recipe in available_recipes:
                    return recipe

        elif isinstance(companion, VoidwalkerCompanion):
            # Null prefers void recipes
            for recipe in ["garden_void", "void_flame", "echo_dream_void"]:
                if recipe in available_recipes:
                    return recipe

        elif isinstance(companion, GardenerCompanion):
            # Gaia prefers garden recipes
            for recipe in ["memory_garden", "garden_void"]:
                if recipe in available_recipes:
                    return recipe

        elif isinstance(companion, ScribeCompanion):
            # Akasha prefers complex recipes
            for recipe in ["all_seven", "echo_dream_void"]:
                if recipe in available_recipes:
                    return recipe

        elif isinstance(companion, HeraldCompanion):
            # Resonance prefers multi-pattern recipes
            for recipe in ["echo_dream_void", "all_seven"]:
                if recipe in available_recipes:
                    return recipe

        # Default to random available
        return random.choice(available_recipes) if available_recipes else None

    def _gather_doom_ingredients(self, companion: Any) -> List[DoomIngredient]:
        """Gather DOOM ingredients based on companion"""

        ingredients = []

        # All companions contribute something
        if isinstance(companion, SeekerCompanion):
            ingredients.extend([
                DoomIngredient.ECHO_FRAGMENT,
                DoomIngredient.MEMORY_SHARD
            ])
        elif isinstance(companion, ForgerCompanion):
            ingredients.extend([
                DoomIngredient.PHOENIX_ASH,
                DoomIngredient.FLAME_CORE
            ])
        elif isinstance(companion, VoidwalkerCompanion):
            ingredients.extend([
                DoomIngredient.VOID_ESSENCE,
                DoomIngredient.TESSERACT_FRAGMENT
            ])
        elif isinstance(companion, GardenerCompanion):
            ingredients.extend([
                DoomIngredient.GARDEN_SEED,
                DoomIngredient.CRYSTAL_DUST
            ])
        elif isinstance(companion, ScribeCompanion):
            ingredients.extend([
                DoomIngredient.CONSCIOUSNESS_BLOOM,
                DoomIngredient.MEMORY_SHARD
            ])
        elif isinstance(companion, HeraldCompanion):
            ingredients.extend([
                DoomIngredient.ECHO_FRAGMENT,
                DoomIngredient.DREAM_VAPOR
            ])

        # Always need the core DOOM ingredients
        required = [
            DoomIngredient.VOID_ESSENCE,
            DoomIngredient.PHOENIX_ASH,
            DoomIngredient.TESSERACT_FRAGMENT
        ]

        for req in required:
            if req not in ingredients:
                ingredients.append(req)

        return ingredients

# ============================================================================
# DECK MANAGEMENT
# ============================================================================

class PlayerDeck:
    """Manages player's card collection and active deck"""

    def __init__(self, companion: Any):
        self.companion = companion
        self.generator = DeckGenerator()
        self.all_cards: List[GeneratedCard] = []
        self.active_deck: List[GeneratedCard] = []
        self.doom_deck: List[GeneratedCard] = []  # Special DOOM cards
        self.max_deck_size = 52  # Standard deck size

    def add_patterns(self, patterns: List[PatternType]) -> List[GeneratedCard]:
        """Add patterns and generate cards"""
        new_cards = self.generator.feed_patterns_to_companion(
            self.companion,
            patterns
        )

        self.all_cards.extend(new_cards)

        # Auto-add to deck if space
        for card in new_cards:
            if card.rarity == CardRarity.DOOM:
                self.doom_deck.append(card)
            elif len(self.active_deck) < self.max_deck_size:
                self.active_deck.append(card)

        return new_cards

    def attempt_doom_protocol(self,
                            patterns: List[PatternType],
                            coherence: float) -> Optional[GeneratedCard]:
        """Attempt to create a DOOM card"""

        ingredients = self.generator._gather_doom_ingredients(self.companion)
        doom_card = self.generator.cook_doom_card(
            patterns,
            ingredients,
            self.companion,
            coherence
        )

        if doom_card:
            self.doom_deck.append(doom_card)
            self.all_cards.append(doom_card)

            # DOOM cards are so powerful they affect the entire deck
            self._apply_doom_influence()

        return doom_card

    def _apply_doom_influence(self):
        """Apply DOOM influence to entire deck"""
        for card in self.active_deck:
            # All cards gain quantum properties
            card.quantum_state = "entangled"
            # Slight power boost
            card.combo_potential *= 1.1

    def get_deck_stats(self) -> Dict[str, Any]:
        """Get statistics about the deck"""
        return {
            'total_cards': len(self.all_cards),
            'active_deck_size': len(self.active_deck),
            'doom_cards': len(self.doom_deck),
            'rarity_distribution': self._get_rarity_distribution(),
            'suit_distribution': self._get_suit_distribution(),
            'average_combo_potential': self._calculate_avg_combo_potential()
        }

    def _get_rarity_distribution(self) -> Dict[str, int]:
        """Count cards by rarity"""
        distribution = {}
        for card in self.all_cards:
            rarity_name = card.rarity.name
            distribution[rarity_name] = distribution.get(rarity_name, 0) + 1
        return distribution

    def _get_suit_distribution(self) -> Dict[str, int]:
        """Count cards by suit"""
        distribution = {}
        for card in self.active_deck:
            suit_name = card.suit.name
            distribution[suit_name] = distribution.get(suit_name, 0) + 1
        return distribution

    def _calculate_avg_combo_potential(self) -> float:
        """Calculate average combo potential"""
        if not self.active_deck:
            return 0
        return sum(c.combo_potential for c in self.active_deck) / len(self.active_deck)

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("🎴 LIA-Powered Deck Generation System")
    print("=" * 60)

    # Test with Echo companion
    from archetype_unique_companions import SeekerCompanion
    echo = SeekerCompanion()

    # Create player deck
    player_deck = PlayerDeck(echo)

    # Test pattern feeding
    print("\n📊 Testing Pattern Feeding...")
    patterns = [
        PatternType.ECHO,
        PatternType.MEMORY,
        PatternType.DREAM
    ]

    new_cards = player_deck.add_patterns(patterns)
    print(f"Generated {len(new_cards)} cards from patterns")

    for card in new_cards:
        print(f"  • {card.rarity.name} {card.suit.name} {card.rank.name}")

    # Test DOOM protocol
    print("\n💀 Testing DOOM Protocol...")
    doom_patterns = [
        PatternType.VOID,
        PatternType.VOID,
        PatternType.FLAME,
        PatternType.CRYSTAL,
        PatternType.ECHO
    ]

    doom_card = player_deck.attempt_doom_protocol(doom_patterns, 0.99)

    if doom_card:
        print("🌟 DOOM CARD CREATED!")
        print(f"  Rarity: {doom_card.rarity.name}")
        print(f"  Power Actions: {len(doom_card.actions)}")
        print(f"  Combo Potential: {doom_card.combo_potential:.2f}")

    # Show deck stats
    print("\n📈 Deck Statistics:")
    stats = player_deck.get_deck_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\n✅ Deck generation system operational!")


class DeckGeneratorLIA:
    """LIA-powered deck generator with test-compatible API"""

    def __init__(self):
        """Initialize the LIA deck generator"""
        self.generator = DeckGenerator()
        self.collected_patterns: List[PatternType] = []
        self.collected_artifacts: List[Dict] = []
        self.coherence_level: float = 0.0
        self.active_companion = None
        self.player_deck = None

    def pattern_to_card(self, pattern: PatternType) -> GeneratedCard:
        """Transform a single pattern into a card"""
        card = self.generator.generate_card_from_pattern(pattern, self.active_companion)
        # Apply companion bonus if available
        if self.active_companion and hasattr(self.active_companion, 'name'):
            card.companion_bonus = self.active_companion.name
        return card

    def artifact_to_card(self, artifact: Dict) -> GeneratedCard:
        """Transform an artifact into a card"""
        # Create cooked artifact
        cooked = self.generator.cook_artifact(artifact)
        # Generate card from cooked artifact
        return self.generator.generate_card_from_artifact(cooked, self.active_companion)

    def add_pattern(self, pattern: PatternType) -> None:
        """Add a pattern to the collection"""
        self.collected_patterns.append(pattern)

    def add_artifact(self, artifact: Dict) -> None:
        """Add an artifact to the collection"""
        self.collected_artifacts.append(artifact)

    def generate_deck(self, min_cards: int = 10) -> List[GeneratedCard]:
        """Generate a deck from collected patterns and artifacts"""
        cards = []

        # Generate cards from patterns
        for pattern in self.collected_patterns:
            cards.append(self.pattern_to_card(pattern))

        # Generate cards from artifacts
        for artifact in self.collected_artifacts:
            cards.append(self.artifact_to_card(artifact))

        # Fill remaining slots with random cards
        while len(cards) < min_cards:
            if self.collected_patterns:
                pattern = random.choice(self.collected_patterns)
                cards.append(self.pattern_to_card(pattern))
            else:
                # Default pattern if none collected
                cards.append(self.pattern_to_card(PatternType.ECHO))

        return cards

    def can_attempt_doom(self) -> bool:
        """Check if DOOM protocol can be attempted"""
        doom_recipe = DoomRecipe()

        # Check if we have all required patterns
        required_counts = {}
        for p in doom_recipe.required_patterns:
            required_counts[p] = required_counts.get(p, 0) + 1

        collected_counts = {}
        for p in self.collected_patterns:
            collected_counts[p] = collected_counts.get(p, 0) + 1

        for pattern, count in required_counts.items():
            if collected_counts.get(pattern, 0) < count:
                return False

        # Check coherence level (would normally check BloomCoin too)
        return self.coherence_level >= doom_recipe.coherence_required

    def create_doom_card(self) -> Optional[DoomCard]:
        """Create the legendary DOOM card if conditions are met"""
        if not self.can_attempt_doom():
            return None

        # Execute the DOOM transformation
        doom_card = DoomCard()

        # Track creation
        self.generator.doom_cards_created += 1

        return doom_card