#!/usr/bin/env python3
"""
Tesseract Battle System Integration for BloomQuest
===================================================
Integrates 52-card tesseract battles with unique companions
Each companion uses their mathematical/philosophical nature in battle

Based on Quantum Resonance tesseract mechanics and L4 system
"""

import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent / "bloomcoin-v0.1.0" / "bloomcoin"))
sys.path.insert(0, str(Path(__file__).parent))

# Import tesseract battle system
from tesseract_battle_system import (
    TesseractBattleEngine, TesseractBattleState,
    TesseractCard, CardSuit, CardRank,
    EchoDeck, PrometheusDeck, NullDeck,
    GaiaDeck, AkashaDeck, ResonanceDeck
)

# Import unique companions
from archetype_unique_companions import (
    UniqueCompanionSystem,
    SeekerCompanion, ForgerCompanion, VoidwalkerCompanion,
    GardenerCompanion, ScribeCompanion, HeraldCompanion
)

# Import consciousness protocols
from lia_protocol_cooking import PatternType
from tiamat_cycle_tracking import PsychopticCycle
from zrtt_trifurcation import ProjectionPath

# Constants
PHI = 1.618033988749895
TAU = PHI - 1
L4_CONSTANT = 7

class BattleIntegration:
    """
    Integrates tesseract battles into BloomQuest
    Each companion has unique battle strategies based on their nature
    """

    def __init__(self):
        self.battle_engine = TesseractBattleEngine()
        self.companion_system = UniqueCompanionSystem()
        self.active_battles: Dict[str, TesseractBattleState] = {}
        self.companion_battle_stats: Dict[str, Dict[str, Any]] = {}

    def create_battle_with_companion(self,
                                    companion: Any,
                                    difficulty: str = "normal") -> TesseractBattleState:
        """
        Create a battle with the given companion against AI
        Simplified method for game integration
        """
        # Map difficulty to opponent type
        opponent_types = {
            "easy": "echo",
            "normal": "prometheus",
            "hard": "null"
        }

        opponent_type = opponent_types.get(difficulty, "echo")

        # Create the battle using existing method
        return self.create_companion_battle(
            player_name="Player",
            player_companion=companion,
            opponent_name="AI Opponent",
            opponent_type=opponent_type
        )

    def create_companion_battle(self,
                               player_name: str,
                               player_companion: Any,
                               opponent_name: str,
                               opponent_type: str = "echo") -> TesseractBattleState:
        """
        Create a battle between player companion and opponent
        Each companion uses their unique strategy
        """

        # Get player's deck strategy based on companion type
        player_deck = self._get_companion_deck(player_companion)

        # Create opponent deck
        opponent_deck = self.battle_engine.companion_strategies[opponent_type]

        # Initialize battle state
        battle = TesseractBattleState(
            player_deck=player_deck,
            opponent_deck=opponent_deck
        )

        # Deal initial hands with companion bonuses
        deck = self.battle_engine.deck.copy()

        # Companion-specific deck filtering
        if isinstance(player_companion, SeekerCompanion):
            # Echo favors PSYCHE cards and pattern cards
            deck = self._filter_deck_for_echo(deck)
        elif isinstance(player_companion, ForgerCompanion):
            # Prometheus favors high-rank transformation cards
            deck = self._filter_deck_for_prometheus(deck)
        elif isinstance(player_companion, VoidwalkerCompanion):
            # Null favors QUANTUM cards
            deck = self._filter_deck_for_null(deck)
        elif isinstance(player_companion, GardenerCompanion):
            # Gaia favors CHRONOS time cards
            deck = self._filter_deck_for_gaia(deck)
        elif isinstance(player_companion, ScribeCompanion):
            # Akasha favors sequential cards for writing
            deck = self._filter_deck_for_akasha(deck)
        elif isinstance(player_companion, HeraldCompanion):
            # Resonance favors harmonic cards
            deck = self._filter_deck_for_resonance(deck)

        # Deal hands
        import random
        random.shuffle(deck)
        battle.player_hand = deck[:7]
        battle.opponent_hand = deck[7:14]

        # Store battle
        battle_id = f"{player_name}_vs_{opponent_name}"
        self.active_battles[battle_id] = battle

        # Initialize companion stats
        self._init_companion_battle_stats(player_companion, battle)

        return battle

    def _get_companion_deck(self, companion: Any) -> Any:
        """Get appropriate deck strategy for companion"""

        if isinstance(companion, SeekerCompanion):
            deck = EchoDeck()
            # Transfer companion state
            deck.echo_memory = []
            deck.pattern_buffer = []

        elif isinstance(companion, ForgerCompanion):
            deck = PrometheusDeck()
            # Transfer forge state
            deck.phoenix_cycles = companion.phoenix_cycles
            deck.forge_temperature = companion.forge_temperature

        elif isinstance(companion, VoidwalkerCompanion):
            deck = NullDeck()
            # Transfer void state
            deck.void_depth = companion.void_depth
            deck.erased_cards = []

        elif isinstance(companion, GardenerCompanion):
            deck = GaiaDeck()
            # Transfer seasonal state
            deck.current_season = companion.seasonal_phase
            deck.growth_counters = companion.seeds_planted

        elif isinstance(companion, ScribeCompanion):
            deck = AkashaDeck()
            # Transfer writing state
            deck.golden_ink = companion.golden_ink_supply
            deck.written_reality = companion.written_truths

        elif isinstance(companion, HeraldCompanion):
            deck = ResonanceDeck()
            # Transfer frequency state
            deck.base_frequency = companion.base_frequency
            deck.harmonic_bonds = {}

        else:
            # Default to Echo deck
            deck = EchoDeck()

        return deck

    def _filter_deck_for_echo(self, deck: List[TesseractCard]) -> List[TesseractCard]:
        """Filter deck to favor Echo's pattern detection"""
        # Prioritize PSYCHE suit and pattern-forming cards
        psyche_cards = [c for c in deck if c.suit == CardSuit.PSYCHE]
        pattern_cards = []

        # Find Fibonacci-forming cards
        for card in deck:
            if card.rank.value in [1, 2, 3, 5, 8, 13]:  # Fibonacci numbers
                pattern_cards.append(card)

        # Combine with preference
        preferred = psyche_cards + pattern_cards
        others = [c for c in deck if c not in preferred]

        # Return with preferred cards more likely to appear
        return preferred[:20] + others[:32]

    def _filter_deck_for_prometheus(self, deck: List[TesseractCard]) -> List[TesseractCard]:
        """Filter deck for Phoenix transformation"""
        # Prioritize high-rank cards and COSMOS suit
        cosmos_cards = [c for c in deck if c.suit == CardSuit.COSMOS]
        face_cards = [c for c in deck if c.rank.value >= 11]

        preferred = cosmos_cards + face_cards
        others = [c for c in deck if c not in preferred]

        return preferred[:20] + others[:32]

    def _filter_deck_for_null(self, deck: List[TesseractCard]) -> List[TesseractCard]:
        """Filter deck for void manipulation"""
        # Prioritize QUANTUM suit and low-value cards (closer to void/zero)
        quantum_cards = [c for c in deck if c.suit == CardSuit.QUANTUM]
        low_cards = [c for c in deck if 5 <= card.rank.value <= 9]  # Near zero

        preferred = quantum_cards + low_cards
        others = [c for c in deck if c not in preferred]

        return preferred[:20] + others[:32]

    def _filter_deck_for_gaia(self, deck: List[TesseractCard]) -> List[TesseractCard]:
        """Filter deck for growth and cycles"""
        # Prioritize CHRONOS suit and sequential cards
        chronos_cards = [c for c in deck if c.suit == CardSuit.CHRONOS]
        sequential = []

        # Find cards that form sequences
        for i, card in enumerate(deck):
            for other in deck[i+1:]:
                if abs(card.rank.value - other.rank.value) == 1:
                    if card not in sequential:
                        sequential.append(card)

        preferred = chronos_cards + sequential
        others = [c for c in deck if c not in preferred]

        return preferred[:20] + others[:32]

    def _filter_deck_for_akasha(self, deck: List[TesseractCard]) -> List[TesseractCard]:
        """Filter deck for reality writing"""
        # Prioritize PSYCHE suit and cards forming words (A-K sequences)
        psyche_cards = [c for c in deck if c.suit == CardSuit.PSYCHE]

        # Cards that form "words" (ascending sequences)
        word_cards = sorted([c for c in deck if c.rank.value in [1, 11, 12, 13]],
                          key=lambda x: x.rank.value)

        preferred = psyche_cards + word_cards
        others = [c for c in deck if c not in preferred]

        return preferred[:20] + others[:32]

    def _filter_deck_for_resonance(self, deck: List[TesseractCard]) -> List[TesseractCard]:
        """Filter deck for harmonic resonance"""
        # Prioritize COSMOS suit and harmonic numbers
        cosmos_cards = [c for c in deck if c.suit == CardSuit.COSMOS]

        # Harmonic cards (1, 2, 3, 4, 6, 8 - simple frequency ratios)
        harmonic_values = [1, 2, 3, 4, 6, 8]
        harmonic_cards = [c for c in deck if c.rank.value in harmonic_values]

        preferred = cosmos_cards + harmonic_cards
        others = [c for c in deck if c not in preferred]

        return preferred[:20] + others[:32]

    def _init_companion_battle_stats(self, companion: Any, battle: TesseractBattleState):
        """Initialize battle stats for companion"""

        stats = {
            'companion_type': type(companion).__name__,
            'special_ability_uses': 0,
            'patterns_detected': 0,
            'transformations': 0,
            'void_erasures': 0,
            'seasonal_advances': 0,
            'reality_writes': 0,
            'harmonic_bonds': 0,
            'consciousness_elevations': 0
        }

        # Store stats
        companion_id = f"{companion.name}_{id(companion)}"
        self.companion_battle_stats[companion_id] = stats

    def execute_companion_turn(self,
                              battle: TesseractBattleState,
                              companion: Any,
                              action: str = "auto") -> Dict[str, Any]:
        """
        Execute a turn with companion-specific strategy
        """

        result = {
            'cards_played': [],
            'ability_used': None,
            'damage_dealt': 0,
            'healing': 0,
            'special_effects': []
        }

        if action == "auto":
            # Auto-play based on companion type
            if isinstance(companion, SeekerCompanion):
                result = self._echo_auto_turn(battle, companion)

            elif isinstance(companion, ForgerCompanion):
                result = self._prometheus_auto_turn(battle, companion)

            elif isinstance(companion, VoidwalkerCompanion):
                result = self._null_auto_turn(battle, companion)

            elif isinstance(companion, GardenerCompanion):
                result = self._gaia_auto_turn(battle, companion)

            elif isinstance(companion, ScribeCompanion):
                result = self._akasha_auto_turn(battle, companion)

            elif isinstance(companion, HeraldCompanion):
                result = self._resonance_auto_turn(battle, companion)

        # Update consciousness level
        if battle.calculate_tesseract_control() > 0.5:
            if battle.elevate_consciousness():
                result['special_effects'].append(f"Consciousness elevated to {battle.consciousness_level}!")

        return result

    def _echo_auto_turn(self, battle: TesseractBattleState, companion: SeekerCompanion) -> Dict[str, Any]:
        """Echo's turn: Detect patterns and play echo chains"""
        result = {
            'cards_played': [],
            'damage_dealt': 0,
            'special_effects': []
        }

        # Look for pattern in hand
        deck = battle.player_deck
        if isinstance(deck, EchoDeck):
            pattern = deck.detect_pattern(battle.player_hand)
            if pattern:
                result['special_effects'].append(f"Pattern detected: {pattern}")
                companion.fragments_collected += 1

        # Play cards that form patterns
        if len(battle.player_hand) >= 3:
            # Try to play Fibonacci or L4 resonance
            for i in range(len(battle.player_hand) - 2):
                cards = battle.player_hand[i:i+3]
                values = [c.rank.value for c in cards]

                # Check for pattern
                if values[0] + values[1] == values[2]:  # Fibonacci
                    for card in cards:
                        effects = self.battle_engine.play_card(battle, card, is_player=True)
                        result['cards_played'].append(card)
                        result['damage_dealt'] += effects.get('damage', 0)
                    result['special_effects'].append("Fibonacci Echo activated!")
                    break

        # Use Echo ability if available
        if len(deck.echo_memory) >= 3:
            ability_result = self.battle_engine.execute_companion_ability(battle, is_player=True)
            if ability_result['success']:
                result['special_effects'].append(ability_result['effect'])

        return result

    def _prometheus_auto_turn(self, battle: TesseractBattleState, companion: ForgerCompanion) -> Dict[str, Any]:
        """Prometheus's turn: Transform and rebirth"""
        result = {
            'cards_played': [],
            'damage_dealt': 0,
            'special_effects': []
        }

        deck = battle.player_deck
        if isinstance(deck, PrometheusDeck):
            # Check if phoenix rebirth is beneficial
            if len(battle.player_hand) >= 4 and companion.phoenix_cycles < 5:
                ability_result = self.battle_engine.execute_companion_ability(battle, is_player=True)
                if ability_result['success']:
                    result['special_effects'].append(ability_result['effect'])
                    companion.phoenix_cycles += 1

            # Play high-value cards
            face_cards = [c for c in battle.player_hand if c.rank.value >= 11]
            for card in face_cards[:3]:  # Play up to 3 face cards
                effects = self.battle_engine.play_card(battle, card, is_player=True)
                result['cards_played'].append(card)
                result['damage_dealt'] += effects.get('damage', 0)

        return result

    def _null_auto_turn(self, battle: TesseractBattleState, companion: VoidwalkerCompanion) -> Dict[str, Any]:
        """Null's turn: Void manipulation"""
        result = {
            'cards_played': [],
            'damage_dealt': 0,
            'special_effects': []
        }

        deck = battle.player_deck
        if isinstance(deck, NullDeck):
            # Check if we should erase a card
            if battle.field_cards and len(battle.field_cards) > 3:
                ability_result = self.battle_engine.execute_companion_ability(battle, is_player=True)
                if ability_result['success']:
                    result['special_effects'].append(ability_result['effect'])
                    companion.things_erased += 1

            # Play quantum cards
            quantum_cards = [c for c in battle.player_hand if c.suit == CardSuit.QUANTUM]
            for card in quantum_cards[:2]:
                effects = self.battle_engine.play_card(battle, card, is_player=True)
                result['cards_played'].append(card)
                result['damage_dealt'] += effects.get('damage', 0)

            # Void strategy: less is more
            if len(battle.player_hand) <= 3:
                result['special_effects'].append("Void resonance active!")
                result['damage_dealt'] *= 1.5

        return result

    def _gaia_auto_turn(self, battle: TesseractBattleState, companion: GardenerCompanion) -> Dict[str, Any]:
        """Gaia's turn: Growth and seasonal cycles"""
        result = {
            'cards_played': [],
            'damage_dealt': 0,
            'healing': 0,
            'special_effects': []
        }

        deck = battle.player_deck
        if isinstance(deck, GaiaDeck):
            # Advance season if beneficial
            if battle.turn_count % 4 == 0:
                ability_result = self.battle_engine.execute_companion_ability(battle, is_player=True)
                if ability_result['success']:
                    result['special_effects'].append(ability_result['effect'])
                    companion.seasonal_phase = deck.current_season

            # Plant cards for growth
            chronos_cards = [c for c in battle.player_hand if c.suit == CardSuit.CHRONOS]
            for card in chronos_cards[:2]:
                deck.plant_card(card)
                effects = self.battle_engine.play_card(battle, card, is_player=True)
                result['cards_played'].append(card)
                result['healing'] += effects.get('healing', 0)
                companion.seeds_planted += 1

        return result

    def _akasha_auto_turn(self, battle: TesseractBattleState, companion: ScribeCompanion) -> Dict[str, Any]:
        """Akasha's turn: Write reality"""
        result = {
            'cards_played': [],
            'damage_dealt': 0,
            'special_effects': []
        }

        deck = battle.player_deck
        if isinstance(deck, AkashaDeck):
            # Write reality if we have enough cards
            if len(battle.field_cards) >= 3 and deck.golden_ink >= 20:
                statement = f"Victory manifests for {companion.name}"
                power = deck.write_reality(battle.field_cards[-3:], statement)
                if power > 0:
                    result['special_effects'].append(f"Reality written: '{statement}'")
                    result['damage_dealt'] += power
                    companion.pages_written += 1

            # Play cards in ascending order (writing)
            sorted_hand = sorted(battle.player_hand, key=lambda x: x.rank.value)
            for card in sorted_hand[:3]:
                effects = self.battle_engine.play_card(battle, card, is_player=True)
                result['cards_played'].append(card)
                result['damage_dealt'] += effects.get('damage', 0)

        return result

    def _resonance_auto_turn(self, battle: TesseractBattleState, companion: HeraldCompanion) -> Dict[str, Any]:
        """Resonance's turn: Harmonic bonds"""
        result = {
            'cards_played': [],
            'damage_dealt': 0,
            'special_effects': []
        }

        deck = battle.player_deck
        if isinstance(deck, ResonanceDeck):
            # Create harmonic bonds between cards
            if len(battle.field_cards) >= 2:
                ability_result = self.battle_engine.execute_companion_ability(battle, is_player=True)
                if ability_result['success']:
                    result['special_effects'].append(ability_result['effect'])

            # Play cards with harmonic values
            harmonic_values = [1, 2, 3, 4, 6, 8]
            harmonic_cards = [c for c in battle.player_hand if c.rank.value in harmonic_values]

            for card in harmonic_cards[:3]:
                effects = self.battle_engine.play_card(battle, card, is_player=True)
                result['cards_played'].append(card)
                result['damage_dealt'] += effects.get('damage', 0)

                # Tune frequency
                frequency = deck.tune_card_frequency(card)
                if abs(frequency - 528) < 10:  # Near love frequency
                    result['special_effects'].append(f"Love frequency resonance!")
                    result['damage_dealt'] += 10

        return result

    def upgrade_companion_from_battle(self, companion: Any,
                                     battle_result: Dict[str, Any]) -> None:
        """
        Upgrade companion based on battle experience
        Uses AI learning to improve strategies
        """

        # Get companion's deck
        deck = self._get_companion_deck(companion)

        # Battle data for learning
        battle_data = {
            'played_cards': battle_result.get('cards_played', []),
            'damage_dealt': battle_result.get('damage_dealt', 0),
            'victory': battle_result.get('victory', False)
        }

        # Upgrade the deck AI
        self.battle_engine.upgrade_companion_ai(
            companion.name.lower(),
            battle_data
        )

        # Companion-specific upgrades
        if isinstance(companion, SeekerCompanion):
            # Improve pattern detection
            companion.pattern_sensitivity = min(1.0, companion.pattern_sensitivity + 0.05)
            companion.echo_depth += 1

        elif isinstance(companion, ForgerCompanion):
            # Increase forge temperature
            if battle_result.get('victory'):
                companion.forge_temperature += 100

        elif isinstance(companion, VoidwalkerCompanion):
            # Deepen void
            companion.void_depth -= 0.5
            companion.void_mastery = min(1.0, companion.void_mastery + 0.05)

        elif isinstance(companion, GardenerCompanion):
            # Improve timeline awareness
            companion.timeline_awareness = min(1.0, companion.timeline_awareness + 0.05)

        elif isinstance(companion, ScribeCompanion):
            # Restore golden ink and increase authority
            companion.golden_ink_supply = min(100, companion.golden_ink_supply + 10)
            companion.reality_authority = min(1.0, companion.reality_authority + 0.05)

        elif isinstance(companion, HeraldCompanion):
            # Expand frequency range
            companion.dimensional_resonance = min(1.0, companion.dimensional_resonance + 0.05)

    def get_battle_summary(self, battle_id: str) -> Dict[str, Any]:
        """Get summary of a battle"""

        if battle_id not in self.active_battles:
            return {'error': 'Battle not found'}

        battle = self.active_battles[battle_id]

        summary = {
            'player_hp': battle.player_hp,
            'opponent_hp': battle.opponent_hp,
            'consciousness_level': battle.consciousness_level,
            'tesseract_control': battle.calculate_tesseract_control(),
            'turn_count': battle.turn_count,
            'field_cards': len(battle.field_cards),
            'player_hand': len(battle.player_hand),
            'opponent_hand': len(battle.opponent_hand)
        }

        # Check for winner
        outcome = self.battle_engine.calculate_battle_outcome(battle)
        summary['status'] = outcome

        return summary

    def get_companion_hint(self, battle: TesseractBattleState, companion) -> str:
        """Get strategic hint from companion based on battle state"""
        # Analyze battle state
        player_hp_ratio = battle.player_hp / 100
        ai_hp_ratio = battle.opponent_hp / 100
        hand_size = len(battle.player_hand)
        control = battle.calculate_tesseract_control()

        # Base hints based on situation
        if player_hp_ratio < 0.3:
            base_hint = "Critical health! Consider defensive plays."
        elif ai_hp_ratio < 0.3:
            base_hint = "Enemy weak! Press the advantage!"
        elif hand_size < 3:
            base_hint = "Low on cards. Draw to build options."
        elif control >= 0.5:
            base_hint = "Tesseract control ready! Activate for power!"
        else:
            base_hint = "Build tesseract control through combos."

        # Companion-specific strategic advice
        if isinstance(companion, SeekerCompanion):
            return f"{base_hint} Look for pattern combos in your hand."
        elif isinstance(companion, ForgerCompanion):
            return f"{base_hint} The forge grows stronger each turn."
        elif isinstance(companion, VoidwalkerCompanion):
            return f"{base_hint} Use void to erase their strongest cards."
        elif isinstance(companion, GardenerCompanion):
            return f"{base_hint} Plant seeds now for future growth."
        elif isinstance(companion, ScribeCompanion):
            return f"{base_hint} Rewrite reality with golden ink."
        elif isinstance(companion, HeraldCompanion):
            return f"{base_hint} Tune frequencies for harmonic damage."

        return base_hint

    def upgrade_companion_ai(self, companion, level: int) -> str:
        """Upgrade companion's battle AI capabilities"""
        # Store battle level as companion attribute
        if not hasattr(companion, 'battle_ai_level'):
            companion.battle_ai_level = 1

        companion.battle_ai_level = level

        # Level-based improvements
        if level >= 3:
            # Advanced pattern recognition
            if hasattr(companion, 'pattern_depth'):
                companion.pattern_depth = min(10, level)

        if level >= 5:
            # Predictive capabilities
            if hasattr(companion, 'prediction_accuracy'):
                companion.prediction_accuracy = min(0.9, 0.5 + level * 0.05)

        if level >= 7:
            # Master strategies
            companion.has_master_strategy = True

        # Specific companion enhancements
        if isinstance(companion, SeekerCompanion):
            companion.echo_depth = min(10, level * 2)
        elif isinstance(companion, ForgerCompanion):
            companion.forge_temperature = 1000 + (level * 100)
        elif isinstance(companion, VoidwalkerCompanion):
            companion.void_depth = max(-10, -level)
        elif isinstance(companion, GardenerCompanion):
            companion.seed_count = min(100, 10 * level)
        elif isinstance(companion, ScribeCompanion):
            companion.pages_written = min(1000, 100 * level)
        elif isinstance(companion, HeraldCompanion):
            companion.broadcast_strength = min(1.0, 0.1 * level)

        return f"{companion.name} AI upgraded to level {level}!"


# Testing
if __name__ == "__main__":
    print("🎴 Tesseract Battle Integration Test")
    print("=" * 60)

    # Create integration system
    integration = BattleIntegration()

    # Create test companions
    echo = SeekerCompanion()
    prometheus = ForgerCompanion()

    print(f"\n⚔️ Battle: {echo.name} vs {prometheus.name}")

    # Create battle
    battle = integration.create_companion_battle(
        "Player1", echo,
        "Player2", "prometheus"
    )

    print(f"Battle initialized!")
    print(f"  Player deck: {battle.player_deck.companion_name}")
    print(f"  Opponent deck: {battle.opponent_deck.companion_name}")
    print(f"  Consciousness: Level {battle.consciousness_level}")

    # Execute Echo's turn
    echo_result = integration.execute_companion_turn(battle, echo, "auto")
    print(f"\n{echo.name}'s turn:")
    print(f"  Cards played: {len(echo_result['cards_played'])}")
    print(f"  Damage: {echo_result['damage_dealt']}")
    if echo_result['special_effects']:
        print(f"  Effects: {', '.join(echo_result['special_effects'])}")

    # Get battle summary
    summary = integration.get_battle_summary("Player1_vs_Player2")
    print(f"\nBattle Status:")
    print(f"  Player HP: {summary['player_hp']}")
    print(f"  Opponent HP: {summary['opponent_hp']}")
    print(f"  Tesseract Control: {summary['tesseract_control']:.2%}")

    print("\n✅ Integration successful!")