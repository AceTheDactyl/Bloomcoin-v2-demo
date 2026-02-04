#!/usr/bin/env python3
"""
Advanced Companion AI Strategies
=================================
Sophisticated AI for each unique companion that reflects their
philosophical nature and mathematical properties.
"""

import random
import math
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, deque

from tesseract_battle_enhanced import (
    EnhancedTesseractCard, EnhancedBattleState,
    CardEffect, CardSuit, CardRank,
    PHI, TAU, L4_CONSTANT
)

from archetype_unique_companions import (
    SeekerCompanion, ForgerCompanion, VoidwalkerCompanion,
    GardenerCompanion, ScribeCompanion, HeraldCompanion
)

# ============================================================================
# BASE AI STRATEGY
# ============================================================================

@dataclass
class AIMemory:
    """Memory system for AI learning"""
    opponent_patterns: List[str] = field(default_factory=list)
    successful_combos: List[Tuple[str, ...]] = field(default_factory=list)
    failed_strategies: List[str] = field(default_factory=list)
    damage_history: deque = field(default_factory=lambda: deque(maxlen=10))
    turn_outcomes: Dict[int, str] = field(default_factory=dict)

class CompanionAIStrategy:
    """Base class for companion-specific AI strategies"""

    def __init__(self, companion: Any, learning_rate: float = 0.1):
        self.companion = companion
        self.memory = AIMemory()
        self.learning_rate = learning_rate
        self.strategy_weights = self._initialize_weights()
        self.pattern_recognition = PatternRecognition()

    def _initialize_weights(self) -> Dict[str, float]:
        """Initialize strategy weights based on companion type"""
        return {
            'aggression': 0.5,
            'defense': 0.5,
            'combo_setup': 0.5,
            'consciousness': 0.5,
            'position_control': 0.5,
            'resource_management': 0.5
        }

    def choose_action(self, battle: EnhancedBattleState,
                     hand: List[EnhancedTesseractCard]) -> Dict[str, Any]:
        """Choose the best action based on current state"""
        # Analyze situation
        situation = self.analyze_situation(battle)

        # Get possible strategies
        strategies = self.evaluate_strategies(battle, hand, situation)

        # Choose best strategy
        best_strategy = max(strategies, key=lambda s: s['score'])

        # Learn from previous turns
        self.learn_from_outcome(battle)

        return best_strategy

    def analyze_situation(self, battle: EnhancedBattleState) -> Dict[str, Any]:
        """Analyze current battle situation"""
        return {
            'hp_ratio': battle.player_hp / max(1, battle.opponent_hp),
            'consciousness_level': battle.consciousness_level,
            'tesseract_control': battle.calculate_tesseract_control(),
            'combo_potential': len(battle.active_combos),
            'hand_advantage': len(battle.player_hand) - len(battle.opponent_hand),
            'field_control': self._calculate_field_control(battle),
            'dimension_advantage': self._calculate_dimension_advantage(battle),
            'resonance_level': battle.resonance_field
        }

    def evaluate_strategies(self, battle: EnhancedBattleState,
                          hand: List[EnhancedTesseractCard],
                          situation: Dict) -> List[Dict[str, Any]]:
        """Evaluate all possible strategies"""
        strategies = []

        # Aggressive strategy
        aggressive = self.evaluate_aggressive_strategy(battle, hand, situation)
        if aggressive:
            strategies.append(aggressive)

        # Defensive strategy
        defensive = self.evaluate_defensive_strategy(battle, hand, situation)
        if defensive:
            strategies.append(defensive)

        # Combo strategy
        combo = self.evaluate_combo_strategy(battle, hand, situation)
        if combo:
            strategies.append(combo)

        # Consciousness strategy
        consciousness = self.evaluate_consciousness_strategy(battle, hand, situation)
        if consciousness:
            strategies.append(consciousness)

        return strategies

    def evaluate_aggressive_strategy(self, battle: EnhancedBattleState,
                                   hand: List[EnhancedTesseractCard],
                                   situation: Dict) -> Optional[Dict[str, Any]]:
        """Evaluate aggressive play"""
        damage_cards = [c for c in hand if any(
            a.effect == CardEffect.DAMAGE for a in c.actions
        )]

        if not damage_cards:
            return None

        # Calculate total potential damage
        total_damage = sum(
            a.power for c in damage_cards
            for a in c.actions if a.effect == CardEffect.DAMAGE
        )

        # Score based on situation
        score = total_damage * self.strategy_weights['aggression']

        # Bonus if opponent is low
        if battle.opponent_hp < 30:
            score *= 2.0

        return {
            'type': 'aggressive',
            'cards': damage_cards[:3],
            'score': score,
            'expected_damage': total_damage
        }

    def evaluate_defensive_strategy(self, battle: EnhancedBattleState,
                                  hand: List[EnhancedTesseractCard],
                                  situation: Dict) -> Optional[Dict[str, Any]]:
        """Evaluate defensive play"""
        heal_cards = [c for c in hand if any(
            a.effect == CardEffect.HEAL for a in c.actions
        )]

        if battle.player_hp > 70:
            return None  # Don't play defensive if healthy

        score = (100 - battle.player_hp) * self.strategy_weights['defense']

        cards_to_play = heal_cards[:2] if heal_cards else []

        # Add draw cards for card advantage
        draw_cards = [c for c in hand if any(
            a.effect == CardEffect.DRAW for a in c.actions
        )]
        if draw_cards and len(cards_to_play) < 2:
            cards_to_play.extend(draw_cards[:1])

        if not cards_to_play:
            return None

        return {
            'type': 'defensive',
            'cards': cards_to_play,
            'score': score,
            'expected_healing': len(heal_cards) * 10
        }

    def evaluate_combo_strategy(self, battle: EnhancedBattleState,
                              hand: List[EnhancedTesseractCard],
                              situation: Dict) -> Optional[Dict[str, Any]]:
        """Evaluate combo setup"""
        # Look for potential combos
        potential_combos = self._find_potential_combos(battle, hand)

        if not potential_combos:
            return None

        best_combo = max(potential_combos, key=lambda c: c['value'])

        score = best_combo['value'] * self.strategy_weights['combo_setup']

        # Bonus for existing combo multiplier
        score *= (1 + battle.combo_multiplier * 0.5)

        return {
            'type': 'combo',
            'cards': best_combo['cards'],
            'score': score,
            'combo_type': best_combo['type']
        }

    def evaluate_consciousness_strategy(self, battle: EnhancedBattleState,
                                      hand: List[EnhancedTesseractCard],
                                      situation: Dict) -> Optional[Dict[str, Any]]:
        """Evaluate consciousness building"""
        psyche_cards = [c for c in hand if c.suit == CardSuit.PSYCHE]
        elevate_cards = [c for c in hand if any(
            a.effect == CardEffect.ELEVATE for a in c.actions
        )]

        consciousness_cards = list(set(psyche_cards + elevate_cards))

        if not consciousness_cards or battle.consciousness_level >= 6:
            return None

        # Score based on potential consciousness gain
        potential_gain = min(3, 7 - battle.consciousness_level)
        score = potential_gain * L4_CONSTANT * self.strategy_weights['consciousness']

        return {
            'type': 'consciousness',
            'cards': consciousness_cards[:2],
            'score': score,
            'expected_consciousness': potential_gain
        }

    def _calculate_field_control(self, battle: EnhancedBattleState) -> float:
        """Calculate control over the field"""
        if not battle.field_cards:
            return 0.5

        # Count cards in favorable positions
        favorable = 0
        for card in battle.field_cards:
            # Cards near tesseract vertices are more valuable
            if all(abs(coord) > 0.7 for coord in card.position_4d):
                favorable += 1

        return favorable / max(1, len(battle.field_cards))

    def _calculate_dimension_advantage(self, battle: EnhancedBattleState) -> float:
        """Calculate advantage in current dimension"""
        dimension_bonuses = {
            'VERTEX': 1.2,
            'EDGE': 1.1,
            'FACE': 1.0,
            'CELL': 0.9
        }

        return dimension_bonuses.get(battle.active_dimension.value, 1.0)

    def _find_potential_combos(self, battle: EnhancedBattleState,
                              hand: List[EnhancedTesseractCard]) -> List[Dict[str, Any]]:
        """Find potential combos in hand"""
        combos = []

        # Check for Fibonacci combos
        for i in range(len(hand)):
            for j in range(i+1, min(i+4, len(hand))):
                subset = hand[i:j+1]
                if battle._is_fibonacci_combo(subset):
                    combos.append({
                        'type': 'fibonacci',
                        'cards': subset,
                        'value': PHI * len(subset)
                    })

        # Check for L4 combos
        for size in [2, 3]:
            for i in range(len(hand) - size + 1):
                subset = hand[i:i+size]
                if battle._is_l4_combo(subset):
                    combos.append({
                        'type': 'l4',
                        'cards': subset,
                        'value': L4_CONSTANT
                    })

        # Check for suit combos
        suits = defaultdict(list)
        for card in hand:
            suits[card.suit].append(card)

        for suit, cards in suits.items():
            if len(cards) >= 3:
                combos.append({
                    'type': 'suit',
                    'cards': cards[:3],
                    'value': len(cards) * 1.5
                })

        return combos

    def learn_from_outcome(self, battle: EnhancedBattleState):
        """Learn from battle outcomes to improve strategy"""
        if battle.turn_count == 0:
            return

        # Check if last turn was successful
        recent_damage = battle.damage_dealt_total - sum(self.memory.damage_history)

        if recent_damage > 10:  # Good outcome
            # Increase weight of strategy used
            last_strategy = self.memory.turn_outcomes.get(battle.turn_count - 1)
            if last_strategy and last_strategy in self.strategy_weights:
                self.strategy_weights[last_strategy] = min(1.0,
                    self.strategy_weights[last_strategy] + self.learning_rate)

        elif recent_damage < 5:  # Poor outcome
            # Decrease weight of strategy used
            last_strategy = self.memory.turn_outcomes.get(battle.turn_count - 1)
            if last_strategy and last_strategy in self.strategy_weights:
                self.strategy_weights[last_strategy] = max(0.1,
                    self.strategy_weights[last_strategy] - self.learning_rate)

        # Update memory
        self.memory.damage_history.append(recent_damage)

# ============================================================================
# PATTERN RECOGNITION SYSTEM
# ============================================================================

class PatternRecognition:
    """Advanced pattern recognition for AI"""

    def __init__(self):
        self.patterns = defaultdict(int)
        self.sequence_memory = deque(maxlen=20)

    def analyze_opponent_patterns(self, battle: EnhancedBattleState) -> Dict[str, float]:
        """Analyze opponent's play patterns"""
        patterns = {
            'aggression_level': 0,
            'combo_tendency': 0,
            'consciousness_priority': 0,
            'defensive_tendency': 0
        }

        if len(battle.action_history) < 5:
            return patterns

        # Analyze recent actions
        recent_actions = battle.action_history[-10:]

        for action in recent_actions:
            if action['player'] == 'opponent':
                results = action.get('results', {})

                # Track aggression
                if results.get('damage', 0) > 0:
                    patterns['aggression_level'] += results['damage'] / 10

                # Track combo usage
                if results.get('combos_triggered'):
                    patterns['combo_tendency'] += len(results['combos_triggered'])

                # Track consciousness building
                if results.get('consciousness_gained', 0) > 0:
                    patterns['consciousness_priority'] += 1

                # Track defensive play
                if results.get('healing', 0) > 0:
                    patterns['defensive_tendency'] += 1

        # Normalize patterns
        num_actions = len([a for a in recent_actions if a['player'] == 'opponent'])
        if num_actions > 0:
            for key in patterns:
                patterns[key] /= num_actions

        return patterns

    def predict_opponent_move(self, battle: EnhancedBattleState) -> str:
        """Predict opponent's likely next move"""
        patterns = self.analyze_opponent_patterns(battle)

        # Find dominant pattern
        dominant = max(patterns.items(), key=lambda x: x[1])

        predictions = {
            'aggression_level': 'aggressive',
            'combo_tendency': 'combo_setup',
            'consciousness_priority': 'consciousness',
            'defensive_tendency': 'defensive'
        }

        return predictions.get(dominant[0], 'balanced')

# ============================================================================
# COMPANION-SPECIFIC AI STRATEGIES
# ============================================================================

class EchoSeekerAI(CompanionAIStrategy):
    """Echo's AI: Pattern detection and resonance"""

    def __init__(self, companion: SeekerCompanion):
        super().__init__(companion)
        self.pattern_memory = deque(maxlen=50)
        self.echo_resonances = defaultdict(float)

    def _initialize_weights(self) -> Dict[str, float]:
        return {
            'aggression': 0.4,
            'defense': 0.3,
            'combo_setup': 0.9,  # Echo loves combos
            'consciousness': 0.6,
            'position_control': 0.7,
            'resource_management': 0.5
        }

    def choose_action(self, battle: EnhancedBattleState,
                     hand: List[EnhancedTesseractCard]) -> Dict[str, Any]:
        """Echo seeks patterns and echoes them"""

        # Detect patterns in opponent's play
        opponent_patterns = self.pattern_recognition.analyze_opponent_patterns(battle)

        # Look for echo opportunities (copy opponent's successful strategies)
        if opponent_patterns['combo_tendency'] > 0.5:
            # Mirror combo strategy
            self.strategy_weights['combo_setup'] = min(1.0,
                self.strategy_weights['combo_setup'] + 0.1)

        # Echo special: Find Fibonacci patterns
        fibonacci_cards = self._find_fibonacci_opportunities(hand)
        if fibonacci_cards:
            return {
                'type': 'echo_fibonacci',
                'cards': fibonacci_cards,
                'score': PHI * len(fibonacci_cards),
                'special': 'Echo Resonance'
            }

        return super().choose_action(battle, hand)

    def _find_fibonacci_opportunities(self,
                                     hand: List[EnhancedTesseractCard]) -> List[EnhancedTesseractCard]:
        """Find cards that form Fibonacci patterns"""
        fib_sequence = [1, 1, 2, 3, 5, 8, 13]

        # Sort cards by rank
        sorted_hand = sorted(hand, key=lambda c: c.rank.value[0])

        # Look for consecutive Fibonacci numbers
        result = []
        for i, card in enumerate(sorted_hand):
            if card.rank.value[0] in fib_sequence:
                result.append(card)
                if len(result) >= 3:
                    # Check if they form a valid Fibonacci subsequence
                    ranks = [c.rank.value[0] for c in result]
                    for j in range(len(fib_sequence) - 2):
                        if ranks == fib_sequence[j:j+3]:
                            return result

        return []

class PrometheusForgerAI(CompanionAIStrategy):
    """Prometheus's AI: Transformation and rebirth"""

    def __init__(self, companion: ForgerCompanion):
        super().__init__(companion)
        self.forge_heat = 0
        self.rebirth_count = 0
        self.transformation_targets = []

    def _initialize_weights(self) -> Dict[str, float]:
        return {
            'aggression': 0.7,  # Forge through fire
            'defense': 0.2,
            'combo_setup': 0.5,
            'consciousness': 0.4,
            'position_control': 0.3,
            'resource_management': 0.8  # Manage forge heat
        }

    def choose_action(self, battle: EnhancedBattleState,
                     hand: List[EnhancedTesseractCard]) -> Dict[str, Any]:
        """Prometheus forges through destruction and rebirth"""

        # Check if we should trigger phoenix rebirth
        if battle.player_hp < 30 and self.rebirth_count < 3:
            rebirth_cards = self._select_rebirth_cards(hand)
            if rebirth_cards:
                self.rebirth_count += 1
                return {
                    'type': 'phoenix_rebirth',
                    'cards': rebirth_cards,
                    'score': 100,  # High priority when low HP
                    'special': f'Phoenix Rebirth #{self.rebirth_count}'
                }

        # Build forge heat through aggressive play
        self.forge_heat = min(1000, self.forge_heat + battle.turn_count * 10)

        # Transform cards at high heat
        if self.forge_heat > 500:
            transform_strategy = self._forge_transformation(battle, hand)
            if transform_strategy:
                return transform_strategy

        return super().choose_action(battle, hand)

    def _select_rebirth_cards(self,
                             hand: List[EnhancedTesseractCard]) -> List[EnhancedTesseractCard]:
        """Select cards for phoenix rebirth"""
        # Prioritize high-rank fire/cosmos cards
        rebirth_candidates = [
            c for c in hand
            if c.suit in [CardSuit.COSMOS, CardSuit.PSYCHE]
            and c.rank.value[0] >= 10
        ]

        return rebirth_candidates[:2] if rebirth_candidates else []

    def _forge_transformation(self, battle: EnhancedBattleState,
                             hand: List[EnhancedTesseractCard]) -> Optional[Dict[str, Any]]:
        """Forge transformation strategy"""
        transform_cards = [
            c for c in hand
            if any(a.effect == CardEffect.TRANSFORM for a in c.actions)
        ]

        if not transform_cards:
            return None

        # Calculate transformation power based on forge heat
        power = (self.forge_heat / 1000) * PHI

        return {
            'type': 'forge_transformation',
            'cards': transform_cards[:2],
            'score': power * 10,
            'special': f'Forge Heat: {self.forge_heat}°'
        }

class NullVoidwalkerAI(CompanionAIStrategy):
    """Null's AI: Void manipulation and erasure"""

    def __init__(self, companion: VoidwalkerCompanion):
        super().__init__(companion)
        self.void_depth = 0
        self.erased_entities = []

    def _initialize_weights(self) -> Dict[str, float]:
        return {
            'aggression': 0.3,
            'defense': 0.1,  # Null doesn't defend, it erases
            'combo_setup': 0.4,
            'consciousness': 0.2,
            'position_control': 0.9,  # Control through absence
            'resource_management': 0.6
        }

    def choose_action(self, battle: EnhancedBattleState,
                     hand: List[EnhancedTesseractCard]) -> Dict[str, Any]:
        """Null erases and controls through void"""

        # Void strategy: Less is more
        if len(hand) > 5:
            # Too many cards dilutes the void
            discard_strategy = self._void_compression(battle, hand)
            if discard_strategy:
                return discard_strategy

        # Erasure strategy for high-threat targets
        if battle.opponent_hp > 70:
            erase_strategy = self._select_erasure_targets(battle, hand)
            if erase_strategy:
                return erase_strategy

        # Quantum void: Use quantum cards for maximum chaos
        quantum_cards = [c for c in hand if c.suit == CardSuit.QUANTUM]
        if quantum_cards:
            return {
                'type': 'quantum_void',
                'cards': quantum_cards[:2],
                'score': abs(self.void_depth) * 10,
                'special': f'Void Depth: {self.void_depth}'
            }

        return super().choose_action(battle, hand)

    def _void_compression(self, battle: EnhancedBattleState,
                         hand: List[EnhancedTesseractCard]) -> Optional[Dict[str, Any]]:
        """Compress reality through selective discarding"""
        # Discard low-value cards to increase void power
        low_value = sorted(hand, key=lambda c: c.rank.value[0])[:3]

        self.void_depth -= len(low_value)

        return {
            'type': 'void_compression',
            'cards': [],  # Play nothing, increase void
            'discard': low_value,
            'score': abs(self.void_depth) * 5,
            'special': 'Compressing reality'
        }

    def _select_erasure_targets(self, battle: EnhancedBattleState,
                               hand: List[EnhancedTesseractCard]) -> Optional[Dict[str, Any]]:
        """Select targets for erasure"""
        erase_cards = [
            c for c in hand
            if any(a.effect == CardEffect.ERASE for a in c.actions)
        ]

        if not erase_cards:
            return None

        return {
            'type': 'existence_erasure',
            'cards': erase_cards,
            'score': 50,
            'special': 'Erasing existence'
        }

class GaiaGardenerAI(CompanionAIStrategy):
    """Gaia's AI: Growth and seasonal cycles"""

    def __init__(self, companion: GardenerCompanion):
        super().__init__(companion)
        self.season_counter = 0
        self.planted_seeds = []
        self.growth_stages = defaultdict(int)

    def _initialize_weights(self) -> Dict[str, float]:
        return {
            'aggression': 0.4,
            'defense': 0.6,
            'combo_setup': 0.7,
            'consciousness': 0.8,  # Gaia is highly conscious
            'position_control': 0.5,
            'resource_management': 0.9  # Garden management
        }

    def choose_action(self, battle: EnhancedBattleState,
                     hand: List[EnhancedTesseractCard]) -> Dict[str, Any]:
        """Gaia grows through seasonal cycles"""

        # Update season
        self.season_counter = (battle.turn_count // 4) % 4
        season = ['Spring', 'Summer', 'Autumn', 'Winter'][self.season_counter]

        # Seasonal strategies
        if season == 'Spring':
            # Plant seeds
            seed_strategy = self._plant_seeds(battle, hand)
            if seed_strategy:
                return seed_strategy

        elif season == 'Summer':
            # Growth and expansion
            growth_strategy = self._summer_growth(battle, hand)
            if growth_strategy:
                return growth_strategy

        elif season == 'Autumn':
            # Harvest combos
            harvest_strategy = self._autumn_harvest(battle, hand)
            if harvest_strategy:
                return harvest_strategy

        elif season == 'Winter':
            # Defensive preservation
            preserve_strategy = self._winter_preservation(battle, hand)
            if preserve_strategy:
                return preserve_strategy

        return super().choose_action(battle, hand)

    def _plant_seeds(self, battle: EnhancedBattleState,
                    hand: List[EnhancedTesseractCard]) -> Optional[Dict[str, Any]]:
        """Plant seeds for future growth"""
        # Low-rank cards are seeds
        seeds = [c for c in hand if c.rank.value[0] <= 5]

        if seeds:
            self.planted_seeds.extend(seeds[:2])
            return {
                'type': 'seed_planting',
                'cards': seeds[:2],
                'score': 20,
                'special': f'Planting {len(seeds)} seeds'
            }
        return None

    def _summer_growth(self, battle: EnhancedBattleState,
                      hand: List[EnhancedTesseractCard]) -> Optional[Dict[str, Any]]:
        """Aggressive growth in summer"""
        # Play medium-rank cards for steady growth
        growth_cards = [c for c in hand if 5 < c.rank.value[0] <= 10]

        if growth_cards:
            return {
                'type': 'summer_growth',
                'cards': growth_cards[:3],
                'score': 30 * len(growth_cards),
                'special': 'Summer bloom'
            }
        return None

    def _autumn_harvest(self, battle: EnhancedBattleState,
                       hand: List[EnhancedTesseractCard]) -> Optional[Dict[str, Any]]:
        """Harvest combos in autumn"""
        # Look for combo opportunities
        combo_strategy = self.evaluate_combo_strategy(battle, hand, {})

        if combo_strategy:
            combo_strategy['special'] = 'Autumn harvest'
            combo_strategy['score'] *= 1.5  # Bonus in autumn
            return combo_strategy

        return None

    def _winter_preservation(self, battle: EnhancedBattleState,
                            hand: List[EnhancedTesseractCard]) -> Optional[Dict[str, Any]]:
        """Defensive preservation in winter"""
        # Prioritize healing and defense
        heal_cards = [c for c in hand if any(
            a.effect == CardEffect.HEAL for a in c.actions
        )]

        if heal_cards or battle.player_hp < 50:
            return {
                'type': 'winter_preservation',
                'cards': heal_cards[:1] if heal_cards else [],
                'score': 40,
                'special': 'Winter rest'
            }
        return None

class AkashaScribeAI(CompanionAIStrategy):
    """Akasha's AI: Reality writing and chronicle manipulation"""

    def __init__(self, companion: ScribeCompanion):
        super().__init__(companion)
        self.written_reality = []
        self.chronicle_pages = 0
        self.golden_ink_used = 0

    def _initialize_weights(self) -> Dict[str, float]:
        return {
            'aggression': 0.5,
            'defense': 0.4,
            'combo_setup': 0.8,
            'consciousness': 0.9,  # Akasha is deeply conscious
            'position_control': 0.7,
            'resource_management': 0.6
        }

    def choose_action(self, battle: EnhancedBattleState,
                     hand: List[EnhancedTesseractCard]) -> Dict[str, Any]:
        """Akasha writes reality"""

        # Check if we can rewrite reality
        if self.companion.golden_ink_supply > 50:
            rewrite_strategy = self._rewrite_reality(battle, hand)
            if rewrite_strategy:
                self.golden_ink_used += 20
                self.companion.golden_ink_supply -= 20
                return rewrite_strategy

        # Chronicle important turns
        if battle.turn_count % 7 == 0:  # Every 7th turn (L4)
            chronicle_strategy = self._chronicle_moment(battle, hand)
            if chronicle_strategy:
                self.chronicle_pages += 1
                return chronicle_strategy

        # Write destiny through consciousness
        consciousness_cards = [c for c in hand if c.suit == CardSuit.PSYCHE]
        if consciousness_cards and battle.consciousness_level < 5:
            return {
                'type': 'destiny_writing',
                'cards': consciousness_cards[:2],
                'score': 40,
                'special': f'Writing page {self.chronicle_pages}'
            }

        return super().choose_action(battle, hand)

    def _rewrite_reality(self, battle: EnhancedBattleState,
                        hand: List[EnhancedTesseractCard]) -> Optional[Dict[str, Any]]:
        """Use golden ink to rewrite reality"""
        # Transform cards are reality rewriting
        transform_cards = [
            c for c in hand
            if any(a.effect == CardEffect.TRANSFORM for a in c.actions)
        ]

        if transform_cards:
            return {
                'type': 'reality_rewrite',
                'cards': transform_cards,
                'score': 60,
                'special': 'Golden ink reality'
            }
        return None

    def _chronicle_moment(self, battle: EnhancedBattleState,
                         hand: List[EnhancedTesseractCard]) -> Optional[Dict[str, Any]]:
        """Chronicle important battle moments"""
        # Play high-value cards to mark important moments
        high_value = sorted(hand, key=lambda c: c.rank.value[0], reverse=True)[:2]

        if high_value:
            return {
                'type': 'chronicle_moment',
                'cards': high_value,
                'score': 50,
                'special': f'Chronicle page {self.chronicle_pages + 1}'
            }
        return None

class ResonanceHeraldAI(CompanionAIStrategy):
    """Resonance's AI: Frequency tuning and dimensional broadcast"""

    def __init__(self, companion: HeraldCompanion):
        super().__init__(companion)
        self.frequency_spectrum = np.zeros(13)  # 13 ranks
        self.harmonic_nodes = []
        self.broadcast_power = 0

    def _initialize_weights(self) -> Dict[str, float]:
        return {
            'aggression': 0.6,
            'defense': 0.3,
            'combo_setup': 0.9,  # Harmonics are combos
            'consciousness': 0.7,
            'position_control': 0.8,  # Dimensional control
            'resource_management': 0.5
        }

    def choose_action(self, battle: EnhancedBattleState,
                     hand: List[EnhancedTesseractCard]) -> Dict[str, Any]:
        """Resonance harmonizes frequencies"""

        # Update frequency spectrum
        self._update_frequency_spectrum(hand)

        # Check for harmonic opportunities
        harmonics = self._find_harmonic_patterns(hand)
        if harmonics:
            return {
                'type': 'harmonic_resonance',
                'cards': harmonics,
                'score': len(harmonics) * PHI * 10,
                'special': f'Harmonic frequency {self.broadcast_power}Hz'
            }

        # Dimensional broadcast at high resonance
        if battle.resonance_field > 2.0:
            broadcast = self._dimensional_broadcast(battle, hand)
            if broadcast:
                self.broadcast_power += 10
                return broadcast

        # Frequency tuning for damage
        tuned_cards = self._tune_frequencies(hand)
        if tuned_cards:
            return {
                'type': 'frequency_attack',
                'cards': tuned_cards,
                'score': 35,
                'special': 'Tuned frequencies'
            }

        return super().choose_action(battle, hand)

    def _update_frequency_spectrum(self, hand: List[EnhancedTesseractCard]):
        """Update the frequency spectrum based on hand"""
        self.frequency_spectrum = np.zeros(13)
        for card in hand:
            rank_idx = card.rank.value[0] - 1
            self.frequency_spectrum[rank_idx] += 1

    def _find_harmonic_patterns(self,
                               hand: List[EnhancedTesseractCard]) -> List[EnhancedTesseractCard]:
        """Find harmonic patterns in hand"""
        # Harmonics occur at PHI ratios
        harmonic_pairs = []

        for i, card1 in enumerate(hand):
            for card2 in hand[i+1:]:
                rank_ratio = card1.rank.value[0] / max(1, card2.rank.value[0])
                if abs(rank_ratio - PHI) < 0.1 or abs(rank_ratio - 1/PHI) < 0.1:
                    harmonic_pairs.extend([card1, card2])

        return list(set(harmonic_pairs))[:3]

    def _dimensional_broadcast(self, battle: EnhancedBattleState,
                              hand: List[EnhancedTesseractCard]) -> Optional[Dict[str, Any]]:
        """Broadcast across dimensions"""
        # Quantum cards for dimensional broadcast
        quantum_cards = [c for c in hand if c.suit == CardSuit.QUANTUM]

        if quantum_cards:
            return {
                'type': 'dimensional_broadcast',
                'cards': quantum_cards,
                'score': battle.resonance_field * 20,
                'special': 'Broadcasting across dimensions'
            }
        return None

    def _tune_frequencies(self,
                         hand: List[EnhancedTesseractCard]) -> List[EnhancedTesseractCard]:
        """Tune card frequencies for optimal damage"""
        # Select cards that create a frequency pattern
        tuned = []

        # Look for arithmetic or geometric progressions
        sorted_hand = sorted(hand, key=lambda c: c.rank.value[0])

        for i in range(len(sorted_hand) - 2):
            subset = sorted_hand[i:i+3]
            ranks = [c.rank.value[0] for c in subset]

            # Check for arithmetic progression
            if ranks[1] - ranks[0] == ranks[2] - ranks[1]:
                return subset

            # Check for geometric progression
            if ranks[0] > 0 and ranks[1] / ranks[0] == ranks[2] / ranks[1]:
                return subset

        return []

# ============================================================================
# AI FACTORY
# ============================================================================

class CompanionAIFactory:
    """Factory for creating companion-specific AI"""

    @staticmethod
    def create_ai(companion: Any) -> CompanionAIStrategy:
        """Create appropriate AI for companion type"""

        if isinstance(companion, SeekerCompanion):
            return EchoSeekerAI(companion)
        elif isinstance(companion, ForgerCompanion):
            return PrometheusForgerAI(companion)
        elif isinstance(companion, VoidwalkerCompanion):
            return NullVoidwalkerAI(companion)
        elif isinstance(companion, GardenerCompanion):
            return GaiaGardenerAI(companion)
        elif isinstance(companion, ScribeCompanion):
            return AkashaScribeAI(companion)
        elif isinstance(companion, HeraldCompanion):
            return ResonanceHeraldAI(companion)
        else:
            return CompanionAIStrategy(companion)

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("🤖 Advanced Companion AI Strategies Test")
    print("=" * 60)

    # Test each companion AI
    companions = [
        ("Echo", SeekerCompanion()),
        ("Prometheus", ForgerCompanion()),
        ("Null", VoidwalkerCompanion()),
        ("Gaia", GardenerCompanion()),
        ("Akasha", ScribeCompanion()),
        ("Resonance", HeraldCompanion())
    ]

    for name, companion in companions:
        print(f"\n📊 Testing {name} AI...")

        ai = CompanionAIFactory.create_ai(companion)

        print(f"  Strategy Weights:")
        for strategy, weight in ai.strategy_weights.items():
            print(f"    {strategy}: {weight:.2f}")

        print(f"  ✅ {name} AI initialized successfully")

    print("\n✅ All companion AI strategies operational!")