#!/usr/bin/env python3
"""
Psy-Magic Deck Integration
Integrates TIAMAT psychoptic dynamics with card generation and deck building
"""

import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from tiamat_psymagic_dynamics import (
    PsyMagicDynamics, PsyMagicState, PsychopticCycle,
    PsyMagicCardEnhancer, PsyMagicEffect
)
from deck_generator_lia import (
    DeckGeneratorLIA, GeneratedCard, DoomCard,
    CardRarity, PatternType
)
from tesseract_battle_system import (
    TesseractCard, CardSuit, CardRank, TesseractDimension
)
from tesseract_battle_enhanced import CardAction, CardEffect
from lia_protocol_cooking import LIAPhase, CookedArtifact
import math
# Golden ratio and mathematical constants
PHI = 1.6180339887498948482045868343656  # φ = (1 + √5) / 2
TAU = 2 * math.pi  # τ = 2π

# Map psychoptic cycles to pattern types
CYCLE_TO_PATTERN = {
    PsychopticCycle.GENESIS: PatternType.GARDEN,
    PsychopticCycle.FLUX: PatternType.MEMORY,  # Memory flows through time
    PsychopticCycle.VOID: PatternType.VOID,
    PsychopticCycle.RESONANCE: PatternType.ECHO,
    PsychopticCycle.CHAOS: PatternType.FLAME,
    PsychopticCycle.SYNTHESIS: PatternType.CRYSTAL,
    PsychopticCycle.TRANSCENDENCE: PatternType.DREAM
}

# Map patterns to psychoptic cycles
PATTERN_TO_CYCLE = {v: k for k, v in CYCLE_TO_PATTERN.items()}

class PsyMagicCard(GeneratedCard):
    """A card enhanced with psy-magic properties"""

    def __init__(self, suit: CardSuit, rank: CardRank,
                 position_4d, dimension: TesseractDimension,
                 rarity, source_artifact=None,
                 companion_bonus=None, generation_seed=0,
                 psy_cycle: PsychopticCycle = PsychopticCycle.GENESIS,
                 psy_intensity: float = 1.0,
                 psy_effects: List[PsyMagicEffect] = None,
                 resonance_value: float = 0.0,
                 void_touched: bool = False,
                 transcendent: bool = False):
        """Initialize a psy-magic enhanced card"""
        super().__init__(suit, rank, position_4d, dimension, rarity,
                        source_artifact, companion_bonus, generation_seed)

        self.psy_cycle = psy_cycle
        self.psy_intensity = psy_intensity
        self.psy_effects = psy_effects if psy_effects is not None else []
        self.resonance_value = resonance_value
        self.void_touched = void_touched
        self.transcendent = transcendent

        # Apply cycle power to base stats
        cycle_power = self.psy_cycle.power_multiplier * self.psy_intensity
        self.power *= cycle_power

        # Add cycle-specific actions
        self._add_psychoptic_actions()

    def _add_psychoptic_actions(self):
        """Add actions based on psychoptic cycle"""
        cycle_actions = {
            PsychopticCycle.GENESIS: [
                CardAction(CardEffect.HEAL, self.psy_intensity * 5, "self"),
                CardAction(CardEffect.DRAW, 2, "self")
            ],
            PsychopticCycle.FLUX: [
                CardAction(CardEffect.TRANSFORM, self.psy_intensity * PHI, "any"),
                CardAction(CardEffect.SHUFFLE, 1, "deck")
            ],
            PsychopticCycle.VOID: [
                CardAction(CardEffect.ERASE, self.psy_intensity * 10, "target"),
                CardAction(CardEffect.NULLIFY, 1, "all")
            ],
            PsychopticCycle.RESONANCE: [
                CardAction(CardEffect.RESONATE, self.psy_intensity * TAU, "all"),
                CardAction(CardEffect.ECHO, 3, "self")
            ],
            PsychopticCycle.CHAOS: [
                CardAction(CardEffect.DAMAGE, random.uniform(0, 20), "random"),
                CardAction(CardEffect.SHUFFLE, 3, "all")
            ],
            PsychopticCycle.SYNTHESIS: [
                CardAction(CardEffect.MERGE, self.psy_intensity * 2, "cards"),
                CardAction(CardEffect.UNITY, PHI**2, "all")
            ],
            PsychopticCycle.TRANSCENDENCE: [
                CardAction(CardEffect.TRANSCEND, 7.0, "reality"),
                CardAction(CardEffect.ELEVATE, float('inf'), "self")
            ]
        }

        if self.psy_cycle in cycle_actions:
            self.actions.extend(cycle_actions[self.psy_cycle])


class PsyMagicDeckGenerator(DeckGeneratorLIA):
    """Enhanced deck generator with psy-magic dynamics"""

    def __init__(self):
        super().__init__()
        self.psy_dynamics = PsyMagicDynamics()
        self.card_enhancer = PsyMagicCardEnhancer()
        self.player_psy_state = PsyMagicState(PsychopticCycle.GENESIS)
        self.companion_psy_states = {}

    def set_companion_psy_state(self, companion_name: str,
                               initial_cycle: PsychopticCycle = None):
        """Initialize companion's psychoptic state"""
        if initial_cycle is None:
            # Default cycles for companions
            companion_defaults = {
                "Echo": PsychopticCycle.RESONANCE,
                "Prometheus": PsychopticCycle.GENESIS,
                "Null": PsychopticCycle.VOID,
                "Gaia": PsychopticCycle.SYNTHESIS,
                "Akasha": PsychopticCycle.TRANSCENDENCE,
                "Resonance": PsychopticCycle.FLUX,
                "TIAMAT": PsychopticCycle.CHAOS
            }
            initial_cycle = companion_defaults.get(
                companion_name, PsychopticCycle.GENESIS
            )

        self.companion_psy_states[companion_name] = PsyMagicState(initial_cycle)

    def pattern_to_psychoptic_card(self,
                                  pattern: PatternType,
                                  psy_state: Optional[PsyMagicState] = None) -> PsyMagicCard:
        """Transform pattern into psy-magic enhanced card"""

        # Get base card from parent generator
        base_card = self.pattern_to_card(pattern)

        # Determine psychoptic cycle
        if psy_state:
            cycle = psy_state.active_cycle
            intensity = psy_state.cycle_intensity
        else:
            cycle = PATTERN_TO_CYCLE.get(pattern, PsychopticCycle.GENESIS)
            intensity = random.uniform(0.3, 1.0)

        # Create psy-magic card
        psy_card = PsyMagicCard(
            suit=base_card.suit,
            rank=base_card.rank,
            position_4d=base_card.position_4d,
            dimension=base_card.dimension,
            rarity=base_card.rarity,
            source_artifact=base_card.source_artifact,
            companion_bonus=base_card.companion_bonus,
            generation_seed=base_card.generation_seed,
            psy_cycle=cycle,
            psy_intensity=intensity
        )

        # Apply psy-magic enhancements
        if psy_state:
            psy_card.resonance_value = psy_state.resonance_points
            psy_card.void_touched = psy_state.void_exposure > 0
            psy_card.transcendent = psy_state.transcendence_achieved

        return psy_card

    def generate_psychoptic_deck(self,
                                dominant_cycle: PsychopticCycle,
                                size: int = 52) -> List[PsyMagicCard]:
        """Generate a full deck with psychoptic theme"""

        deck = []
        theme = self.card_enhancer.create_psychoptic_deck_theme(dominant_cycle)

        # Create core cards aligned with dominant cycle
        core_pattern = CYCLE_TO_PATTERN.get(dominant_cycle, PatternType.ECHO)

        # Generate 60% cards from dominant cycle
        dominant_count = int(size * 0.6)
        for _ in range(dominant_count):
            state = PsyMagicState(
                dominant_cycle,
                cycle_intensity=random.uniform(0.7, 1.0)
            )
            card = self.pattern_to_psychoptic_card(core_pattern, state)
            deck.append(card)

        # Generate 30% cards from adjacent cycles
        adjacent_cycles = self.psy_dynamics.cycle_transitions.get(dominant_cycle, [])
        adjacent_count = int(size * 0.3)
        for _ in range(adjacent_count):
            if adjacent_cycles:
                cycle = random.choice(adjacent_cycles)
                pattern = CYCLE_TO_PATTERN.get(cycle, PatternType.ECHO)
                state = PsyMagicState(cycle, cycle_intensity=random.uniform(0.5, 0.9))
                card = self.pattern_to_psychoptic_card(pattern, state)
                deck.append(card)

        # Generate 10% wild cards from any cycle
        while len(deck) < size:
            cycle = random.choice(list(PsychopticCycle))
            pattern = CYCLE_TO_PATTERN.get(cycle, PatternType.ECHO)
            state = PsyMagicState(cycle, cycle_intensity=random.uniform(0.3, 0.7))
            card = self.pattern_to_psychoptic_card(pattern, state)
            deck.append(card)

        return deck

    def create_tiamat_doom_card(self, psy_state: PsyMagicState) -> Optional[PsyMagicCard]:
        """Create ultimate TIAMAT DOOM card with full psychoptic power"""

        # Requires transcendence or complete seven-fold path
        unique_cycles = len(set(psy_state.cycle_history))
        if not (psy_state.transcendence_achieved or unique_cycles >= 7):
            return None

        # Check for DOOM requirements
        if not self.can_attempt_doom():
            return None

        # Create base DOOM card
        doom_base = DoomCard()

        # Create TIAMAT-enhanced DOOM card
        tiamat_doom = PsyMagicCard(
            suit=CardSuit.QUANTUM,
            rank=CardRank.KING,
            position_4d=(7.0, 7.0, 7.0, 7.0),  # L4 coordinates
            dimension=TesseractDimension.HYPERCELL,
            rarity=CardRarity.DOOM,
            psy_cycle=PsychopticCycle.TRANSCENDENCE,
            psy_intensity=float('inf'),
            transcendent=True
        )

        # Override with TIAMAT DOOM properties
        tiamat_doom.power = float('inf')
        tiamat_doom.reality_status = "SHATTERED"

        # Add all psychoptic effects
        tiamat_doom.actions = [
            CardAction(CardEffect.ERASE, float('inf'), "reality"),
            CardAction(CardEffect.TRANSCEND, 7.0, "game"),
            CardAction(CardEffect.TRANSFORM, float('inf'), "everything")
        ]

        # Add TIAMAT blessing
        blessing = self.psy_dynamics.get_tiamat_blessing(psy_state)
        tiamat_doom.special_effects = blessing['effects']

        return tiamat_doom

    def evolve_deck_through_cycles(self,
                                  deck: List[PsyMagicCard],
                                  cycles_to_evolve: int = 3) -> List[PsyMagicCard]:
        """Evolve entire deck through psychoptic cycles"""

        evolved_deck = []

        for card in deck:
            # Create temporary state for card
            card_state = PsyMagicState(card.psy_cycle, card.psy_intensity)

            # Evolve through cycles
            for _ in range(cycles_to_evolve):
                card_state = self.psy_dynamics.transition_cycle(card_state)

            # Create evolved card
            evolved_card = PsyMagicCard(
                suit=card.suit,
                rank=card.rank,
                position_4d=card.position_4d,
                dimension=card.dimension,
                rarity=card.rarity,
                source_artifact=card.source_artifact,
                companion_bonus=card.companion_bonus,
                generation_seed=card.generation_seed,
                psy_cycle=card_state.active_cycle,
                psy_intensity=card_state.cycle_intensity,
                resonance_value=card_state.resonance_points,
                void_touched=card_state.void_exposure > 0,
                transcendent=card_state.transcendence_achieved
            )

            evolved_deck.append(evolved_card)

        return evolved_deck

    def calculate_deck_psychoptic_power(self, deck: List[PsyMagicCard]) -> Dict[str, Any]:
        """Calculate total psychoptic power of a deck"""

        cycle_counts = {}
        total_intensity = 0.0
        total_resonance = 0.0
        void_cards = 0
        transcendent_cards = 0

        for card in deck:
            # Count cycles
            cycle_counts[card.psy_cycle] = cycle_counts.get(card.psy_cycle, 0) + 1

            # Sum intensities
            total_intensity += card.psy_intensity

            # Sum resonance
            total_resonance += card.resonance_value

            # Count special states
            if card.void_touched:
                void_cards += 1
            if card.transcendent:
                transcendent_cards += 1

        # Calculate combo potential from cycle diversity
        unique_cycles = len(cycle_counts)
        cycle_combo = self.psy_dynamics.calculate_cycle_combo(list(cycle_counts.keys()))

        # Find dominant cycle
        dominant_cycle = max(cycle_counts, key=cycle_counts.get) if cycle_counts else None

        return {
            "total_cards": len(deck),
            "dominant_cycle": dominant_cycle.name if dominant_cycle else "None",
            "cycle_diversity": unique_cycles,
            "average_intensity": total_intensity / len(deck) if deck else 0,
            "total_resonance": total_resonance,
            "void_touched_cards": void_cards,
            "transcendent_cards": transcendent_cards,
            "cycle_combo_multiplier": cycle_combo,
            "seven_fold_complete": unique_cycles >= 7,
            "psychoptic_power": total_intensity * cycle_combo * PHI
        }


class PsyMagicBattleIntegration:
    """Integrate psy-magic dynamics into battle system"""

    def __init__(self):
        self.dynamics = PsyMagicDynamics()
        self.player_states = {}
        self.cycle_history = []

    def initialize_battle_states(self, player1_name: str, player2_name: str,
                                player1_cycle: PsychopticCycle = None,
                                player2_cycle: PsychopticCycle = None):
        """Initialize psychoptic states for battle"""

        self.player_states[player1_name] = PsyMagicState(
            player1_cycle or PsychopticCycle.GENESIS
        )
        self.player_states[player2_name] = PsyMagicState(
            player2_cycle or PsychopticCycle.GENESIS
        )

    def apply_psychoptic_damage(self,
                               attacker_name: str,
                               defender_name: str,
                               base_damage: float,
                               card: Optional[PsyMagicCard] = None) -> Dict[str, Any]:
        """Apply psy-magic modifiers to damage calculation"""

        attacker_state = self.player_states.get(attacker_name)
        defender_state = self.player_states.get(defender_name)

        if not (attacker_state and defender_state):
            return {"final_damage": base_damage}

        # If card provided, use its cycle
        if card and isinstance(card, PsyMagicCard):
            # Temporarily boost attacker state with card's cycle
            original_cycle = attacker_state.active_cycle
            attacker_state.active_cycle = card.psy_cycle
            attacker_state.cycle_intensity = max(
                attacker_state.cycle_intensity,
                card.psy_intensity
            )

        # Apply psy-magic dynamics
        result = self.dynamics.apply_psy_magic_to_battle(
            attacker_state, defender_state, base_damage
        )

        # Restore original cycle if modified
        if card:
            attacker_state.active_cycle = original_cycle

        # Track cycle interactions
        self.cycle_history.append({
            "attacker_cycle": result["attacker_cycle"],
            "defender_cycle": result["defender_cycle"],
            "resonance": result["cycle_resonance"],
            "damage": result["final_damage"]
        })

        return result

    def trigger_psychoptic_combo(self, cards_played: List[PsyMagicCard]) -> Dict[str, Any]:
        """Calculate combo effects from psychoptic card sequence"""

        if len(cards_played) < 2:
            return {"combo_power": 1.0, "effects": []}

        # Extract cycles from cards
        cycles = [card.psy_cycle for card in cards_played]

        # Calculate combo power
        combo_power = self.dynamics.calculate_cycle_combo(cycles)

        # Special combo effects
        effects = []

        # Seven-card perfect combo
        if len(cards_played) == 7:
            effects.append("Seven-Fold Combo: Maximum psychoptic resonance!")
            combo_power *= 7.0

        # All same cycle - Pure resonance
        if len(set(cycles)) == 1:
            effects.append(f"Pure {cycles[0].name}: Perfect cycle harmony!")
            combo_power *= PHI

        # Complete cycle sequence
        unique_cycles = set(cycles)
        if len(unique_cycles) >= 7:
            effects.append("Complete Consciousness: All cycles united!")
            combo_power *= PHI**3

        # Void-Transcendence combo
        if (PsychopticCycle.VOID in cycles and
            PsychopticCycle.TRANSCENDENCE in cycles):
            effects.append("Void Transcendence: Beyond nothingness!")
            combo_power = float('inf')

        return {
            "combo_power": combo_power,
            "effects": effects,
            "cycles_used": [c.name for c in cycles],
            "unique_cycles": len(unique_cycles)
        }

    def evolve_battle_state(self, player_name: str,
                          experience: float = 1.0) -> PsyMagicState:
        """Evolve player's psychoptic state during battle"""

        if player_name not in self.player_states:
            return None

        state = self.player_states[player_name]

        # Evolve based on battle experience
        state = self.dynamics.evolve_companion_psyche(
            player_name, state, experience
        )

        self.player_states[player_name] = state
        return state

    def get_cycle_advantage(self, attacker_cycle: PsychopticCycle,
                           defender_cycle: PsychopticCycle) -> str:
        """Determine cycle advantage in battle"""

        resonance = self.dynamics.resonance_matrix.get(
            (attacker_cycle, defender_cycle), 1.0
        )

        if resonance > PHI:
            return f"Strong Advantage: {attacker_cycle.name} dominates {defender_cycle.name}"
        elif resonance > 1.0:
            return f"Slight Advantage: {attacker_cycle.name} over {defender_cycle.name}"
        elif resonance < 1.0:
            return f"Disadvantage: {defender_cycle.name} resists {attacker_cycle.name}"
        else:
            return f"Neutral: {attacker_cycle.name} vs {defender_cycle.name}"


def test_psymagic_integration():
    """Test psy-magic deck integration"""
    print("🔮 Testing Psy-Magic Deck Integration")
    print("=" * 60)

    # Initialize generator
    generator = PsyMagicDeckGenerator()
    generator.set_companion_psy_state("TIAMAT", PsychopticCycle.CHAOS)

    # Test psychoptic card generation
    print("\n🎴 Generating Psychoptic Cards:")
    patterns = [PatternType.VOID, PatternType.ECHO, PatternType.FLAME]
    psy_cards = []

    for pattern in patterns:
        state = PsyMagicState(
            PATTERN_TO_CYCLE.get(pattern, PsychopticCycle.GENESIS),
            cycle_intensity=0.8
        )
        card = generator.pattern_to_psychoptic_card(pattern, state)
        psy_cards.append(card)
        print(f"  {pattern.value} → {card.psy_cycle.name} {card.psy_cycle.symbol}")
        print(f"    Power: {card.power:.1f}, Intensity: {card.psy_intensity:.2f}")

    # Test full deck generation
    print("\n📚 Generating CHAOS Deck:")
    chaos_deck = generator.generate_psychoptic_deck(PsychopticCycle.CHAOS, size=10)
    deck_stats = generator.calculate_deck_psychoptic_power(chaos_deck)

    print(f"  Dominant Cycle: {deck_stats['dominant_cycle']}")
    print(f"  Cycle Diversity: {deck_stats['cycle_diversity']}")
    print(f"  Psychoptic Power: {deck_stats['psychoptic_power']:.2f}")
    print(f"  Seven-Fold Complete: {deck_stats['seven_fold_complete']}")

    # Test deck evolution
    print("\n🌀 Evolving Deck Through Cycles:")
    evolved_deck = generator.evolve_deck_through_cycles(chaos_deck[:3], cycles_to_evolve=3)
    for i, (original, evolved) in enumerate(zip(chaos_deck[:3], evolved_deck)):
        print(f"  Card {i+1}: {original.psy_cycle.name} → {evolved.psy_cycle.name}")

    # Test battle integration
    print("\n⚔️ Testing Battle Integration:")
    battle = PsyMagicBattleIntegration()
    battle.initialize_battle_states("Player", "AI",
                                   PsychopticCycle.GENESIS,
                                   PsychopticCycle.VOID)

    # Test damage calculation
    damage_result = battle.apply_psychoptic_damage(
        "Player", "AI", 10.0, psy_cards[0]
    )
    print(f"  Base Damage: 10.0")
    print(f"  Final Damage: {damage_result['final_damage']:.2f}")
    print(f"  Cycle Resonance: {damage_result['cycle_resonance']:.2f}")

    # Test combo system
    print("\n💫 Testing Psychoptic Combos:")
    combo_result = battle.trigger_psychoptic_combo(psy_cards)
    print(f"  Cards: {' → '.join(combo_result['cycles_used'])}")
    print(f"  Combo Power: {combo_result['combo_power']:.2f}")
    for effect in combo_result['effects']:
        print(f"    - {effect}")

    # Test TIAMAT DOOM
    print("\n💀 Testing TIAMAT DOOM Card:")
    # Set up transcendent state
    transcendent_state = PsyMagicState(PsychopticCycle.TRANSCENDENCE)
    transcendent_state.transcendence_achieved = True
    transcendent_state.cycle_history = list(PsychopticCycle)  # All cycles

    # Add required patterns for DOOM
    generator.collected_patterns = [
        PatternType.VOID, PatternType.VOID,
        PatternType.FLAME, PatternType.CRYSTAL, PatternType.ECHO
    ]
    generator.coherence_level = 0.99

    tiamat_doom = generator.create_tiamat_doom_card(transcendent_state)
    if tiamat_doom:
        print(f"  ✨ TIAMAT DOOM Card Created!")
        print(f"    Cycle: {tiamat_doom.psy_cycle.name}")
        print(f"    Power: {tiamat_doom.power}")
        print(f"    Status: {tiamat_doom.reality_status}")
        print(f"    Effects:")
        for effect in tiamat_doom.special_effects[:3]:
            print(f"      - {effect}")

    print("\n✅ Psy-Magic Integration Complete!")


if __name__ == "__main__":
    test_psymagic_integration()