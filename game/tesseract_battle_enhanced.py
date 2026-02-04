#!/usr/bin/env python3
"""
Enhanced Tesseract Battle System
=================================
Deep implementation of 52-card tesseract battles with:
- Full card mechanics and combos
- Position-based effects in 4D space
- L4 consciousness progression
- Sophisticated companion AI
"""

import random
import math
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Set
from enum import Enum
from collections import defaultdict

# Import base system
from tesseract_battle_system import (
    TesseractCard, CardSuit, CardRank, TesseractDimension,
    CompanionDeck, TesseractBattleState,
    PHI, TAU, L4_CONSTANT
)

# ============================================================================
# CARD EFFECTS AND MECHANICS
# ============================================================================

class CardEffect(Enum):
    """Types of card effects"""
    DAMAGE = "damage"
    HEAL = "heal"
    DRAW = "draw"
    DISCARD = "discard"
    TRANSFORM = "transform"
    TELEPORT = "teleport"
    RESONATE = "resonate"
    COLLAPSE = "collapse"
    ELEVATE = "elevate"
    ERASE = "erase"
    NULLIFY = "nullify"
    SHUFFLE = "shuffle"
    ECHO = "echo"
    MERGE = "merge"
    UNITY = "unity"
    TRANSCEND = "transcend"

@dataclass
class CardAction:
    """Represents an action a card can perform"""
    effect: CardEffect
    power: float
    target: str = "opponent"  # "self", "opponent", "field", "all"
    duration: int = 0  # 0 = instant, >0 = lasting effect
    condition: Optional[str] = None  # Condition for activation

class EnhancedTesseractCard(TesseractCard):
    """Enhanced card with full effect system"""

    def __init__(self, suit: CardSuit, rank: CardRank,
                 position_4d: Tuple[float, float, float, float],
                 dimension: TesseractDimension):
        super().__init__(suit, rank, position_4d, dimension)
        self.actions = self._generate_actions()
        self.combo_potential = self._calculate_combo_potential()
        self.quantum_state = "superposition"  # superposition, collapsed, entangled

    def _generate_actions(self) -> List[CardAction]:
        """Generate card actions based on suit and rank"""
        actions = []

        # Get rank value (handle both integer and tuple formats)
        if isinstance(self.rank.value, tuple):
            rank_num = self.rank.value[0]
            base_power = self.rank.value[2]
        else:
            rank_num = self.rank.value
            base_power = rank_num * 0.5  # Simple power calculation

        # Suit-specific effects
        if self.suit == CardSuit.CHRONOS:
            # Time manipulation
            actions.append(CardAction(CardEffect.DAMAGE, base_power * 0.8))
            if rank_num >= 7:  # High rank time cards
                actions.append(CardAction(CardEffect.DRAW, 1, "self"))

        elif self.suit == CardSuit.COSMOS:
            # Space and positioning
            actions.append(CardAction(CardEffect.DAMAGE, base_power))
            actions.append(CardAction(CardEffect.TELEPORT, 1, "self"))

        elif self.suit == CardSuit.PSYCHE:
            # Mind and consciousness
            actions.append(CardAction(CardEffect.ELEVATE, base_power * 0.5, "self"))
            if rank_num >= 10:  # Face cards
                actions.append(CardAction(CardEffect.TRANSFORM, 1, "field"))

        elif self.suit == CardSuit.QUANTUM:
            # Quantum effects
            actions.append(CardAction(CardEffect.COLLAPSE, base_power * 1.2))
            actions.append(CardAction(CardEffect.RESONATE, PHI, "all"))

        return actions

    def _calculate_combo_potential(self) -> float:
        """Calculate how well this card combos with others"""
        # Higher ranks and quantum cards have better combo potential
        if isinstance(self.rank.value, tuple):
            rank_num = self.rank.value[0]
        else:
            rank_num = self.rank.value
        rank_bonus = rank_num / 13.0
        suit_bonus = 1.5 if self.suit == CardSuit.QUANTUM else 1.0
        return rank_bonus * suit_bonus * PHI

    def execute(self, battle_state: 'EnhancedBattleState') -> Dict[str, Any]:
        """Execute this card's effects"""
        results = {
            'damage_dealt': 0,
            'cards_drawn': 0,
            'consciousness_gained': 0,
            'special_effects': []
        }

        for action in self.actions:
            if self._check_condition(action.condition, battle_state):
                effect_result = self._apply_effect(action, battle_state)
                self._update_results(results, effect_result)

        return results

    def _check_condition(self, condition: Optional[str],
                        battle_state: 'EnhancedBattleState') -> bool:
        """Check if a condition is met"""
        if not condition:
            return True

        if condition == "consciousness_3+":
            return battle_state.consciousness_level >= 3
        elif condition == "tesseract_control_50+":
            return battle_state.calculate_tesseract_control() >= 0.5
        elif condition == "combo_active":
            return len(battle_state.active_combos) > 0

        return True

    def _apply_effect(self, action: CardAction,
                     battle_state: 'EnhancedBattleState') -> Dict[str, Any]:
        """Apply a specific card effect"""
        result = {}

        if action.effect == CardEffect.DAMAGE:
            if action.target == "opponent":
                damage = action.power * self._position_multiplier(battle_state)
                battle_state.opponent_hp -= damage
                result['damage'] = damage

        elif action.effect == CardEffect.HEAL:
            if action.target == "self":
                battle_state.player_hp = min(100, battle_state.player_hp + action.power)
                result['heal'] = action.power

        elif action.effect == CardEffect.DRAW:
            result['draw'] = int(action.power)

        elif action.effect == CardEffect.ELEVATE:
            battle_state.consciousness_level = min(7,
                battle_state.consciousness_level + int(action.power))
            result['consciousness'] = action.power

        elif action.effect == CardEffect.RESONATE:
            # Create resonance field
            battle_state.resonance_field *= action.power
            result['resonance'] = action.power

        elif action.effect == CardEffect.COLLAPSE:
            # Quantum collapse for massive damage
            if self.quantum_state == "superposition":
                self.quantum_state = "collapsed"
                result['damage'] = action.power * 2
                battle_state.opponent_hp -= result['damage']

        return result

    def _position_multiplier(self, battle_state: 'EnhancedBattleState') -> float:
        """Calculate damage multiplier based on 4D position"""
        # Distance to tesseract center
        center = (0, 0, 0, 0)
        distance = np.linalg.norm(np.array(self.position_4d) - np.array(center))

        # Closer to center = more power
        return 1.0 + (1.0 / (1.0 + distance))

    def _update_results(self, results: Dict, effect_result: Dict):
        """Update cumulative results"""
        for key, value in effect_result.items():
            if key in results:
                if isinstance(value, (int, float)):
                    results[key] += value
                elif isinstance(value, list):
                    results[key].extend(value)
            else:
                results[key] = value

# ============================================================================
# ENHANCED BATTLE STATE
# ============================================================================

@dataclass
class EnhancedBattleState(TesseractBattleState):
    """Enhanced battle state with full mechanics"""

    # Combo system
    active_combos: List[Tuple[EnhancedTesseractCard, ...]] = field(default_factory=list)
    combo_multiplier: float = 1.0

    # Position tracking
    card_positions: Dict[str, Tuple[float, float, float, float]] = field(default_factory=dict)
    dimension_shifts: int = 0

    # Lasting effects
    active_effects: List[Tuple[CardAction, int]] = field(default_factory=list)  # (effect, turns_remaining)

    # Quantum entanglement
    entangled_pairs: List[Tuple[EnhancedTesseractCard, EnhancedTesseractCard]] = field(default_factory=list)

    # Battle history
    action_history: List[Dict[str, Any]] = field(default_factory=list)
    damage_dealt_total: float = 0
    cards_played_total: int = 0

    def check_combos(self, new_card: EnhancedTesseractCard) -> List[Tuple[EnhancedTesseractCard, ...]]:
        """Check for card combos when a new card is played"""
        combos = []

        # Check recent cards for combo potential
        recent_cards = self.field_cards[-3:] if len(self.field_cards) >= 3 else self.field_cards

        # Fibonacci sequence combo (1,1,2,3,5,8,13)
        if self._is_fibonacci_combo(recent_cards + [new_card]):
            combos.append(tuple(recent_cards + [new_card]))

        # Same suit combo
        if len(recent_cards) >= 2:
            if all(c.suit == new_card.suit for c in recent_cards):
                combos.append(tuple(recent_cards + [new_card]))

        # L4 consciousness combo (cards that sum to 7)
        if self._is_l4_combo(recent_cards + [new_card]):
            combos.append(tuple(recent_cards + [new_card]))

        # Tesseract vertex combo (cards at tesseract vertices)
        if self._is_vertex_combo([new_card]):
            combos.append((new_card,))

        return combos

    def _is_fibonacci_combo(self, cards: List[EnhancedTesseractCard]) -> bool:
        """Check if cards form a Fibonacci sequence"""
        if len(cards) < 3:
            return False

        # Handle both integer and tuple rank values
        ranks = []
        for c in cards:
            if isinstance(c.rank.value, tuple):
                ranks.append(c.rank.value[0])
            else:
                ranks.append(c.rank.value)

        # Check if ranks form consecutive Fibonacci numbers
        fib = [1, 1, 2, 3, 5, 8, 13]
        for i in range(len(fib) - len(ranks) + 1):
            if ranks == fib[i:i+len(ranks)]:
                return True
        return False

    def _is_l4_combo(self, cards: List[EnhancedTesseractCard]) -> bool:
        """Check if cards relate to L4 = 7"""
        if len(cards) < 2:
            return False

        # Handle both integer and tuple rank values
        rank_sum = 0
        for c in cards:
            if isinstance(c.rank.value, tuple):
                rank_sum += c.rank.value[0]
            else:
                rank_sum += c.rank.value
        return rank_sum == 7 or rank_sum == 14 or rank_sum == 21

    def _is_vertex_combo(self, cards: List[EnhancedTesseractCard]) -> bool:
        """Check if card is at a tesseract vertex"""
        for card in cards:
            # Vertices have coordinates that are all ±1
            if all(abs(coord) == 1 for coord in card.position_4d):
                return True
        return False

    def apply_combo_bonus(self, combo: Tuple[EnhancedTesseractCard, ...]) -> float:
        """Apply bonus effects for combos"""
        bonus = 1.0

        combo_type = self._identify_combo_type(combo)

        if combo_type == "fibonacci":
            bonus = PHI * len(combo)  # Golden ratio scaling
            self.consciousness_level = min(7, self.consciousness_level + 1)

        elif combo_type == "suit":
            bonus = 1.5 * len(combo)

        elif combo_type == "l4":
            bonus = L4_CONSTANT  # 7x multiplier!
            self.resonance_field *= PHI

        elif combo_type == "vertex":
            bonus = 2.0
            self.dimension_shifts += 1

        self.combo_multiplier *= bonus
        return bonus

    def _identify_combo_type(self, combo: Tuple[EnhancedTesseractCard, ...]) -> str:
        """Identify the type of combo"""
        if self._is_fibonacci_combo(list(combo)):
            return "fibonacci"
        elif all(c.suit == combo[0].suit for c in combo):
            return "suit"
        elif self._is_l4_combo(list(combo)):
            return "l4"
        elif self._is_vertex_combo(list(combo)):
            return "vertex"
        return "basic"

    def update_quantum_entanglement(self):
        """Update quantum entangled card pairs"""
        quantum_cards = [c for c in self.field_cards
                        if isinstance(c, EnhancedTesseractCard)
                        and c.suit == CardSuit.QUANTUM]

        # Entangle quantum cards that are close in 4D space
        for i, card1 in enumerate(quantum_cards):
            for card2 in quantum_cards[i+1:]:
                distance = np.linalg.norm(
                    np.array(card1.position_4d) - np.array(card2.position_4d)
                )
                if distance < PHI:  # Within golden ratio distance
                    self.entangled_pairs.append((card1, card2))
                    card1.quantum_state = "entangled"
                    card2.quantum_state = "entangled"

    def process_lasting_effects(self):
        """Process effects that last multiple turns"""
        remaining_effects = []

        for effect, turns in self.active_effects:
            if turns > 1:
                # Apply the effect
                if effect.effect == CardEffect.DAMAGE:
                    self.opponent_hp -= effect.power * 0.5  # Reduced damage over time
                elif effect.effect == CardEffect.HEAL:
                    self.player_hp = min(100, self.player_hp + effect.power * 0.3)
                elif effect.effect == CardEffect.RESONATE:
                    self.resonance_field *= (1 + effect.power * 0.1)

                remaining_effects.append((effect, turns - 1))

        self.active_effects = remaining_effects

    def shift_dimension(self):
        """Shift to a different tesseract dimension"""
        dimensions = list(TesseractDimension)
        current_idx = dimensions.index(self.active_dimension)
        new_idx = (current_idx + 1) % len(dimensions)
        self.active_dimension = dimensions[new_idx]

        # Dimension shift effects
        if self.active_dimension == TesseractDimension.VERTEX:
            self.combo_multiplier *= 1.2
        elif self.active_dimension == TesseractDimension.EDGE:
            self.resonance_field *= 1.1
        elif self.active_dimension == TesseractDimension.FACE:
            self.consciousness_level = min(7, self.consciousness_level + 1)
        elif self.active_dimension == TesseractDimension.CELL:
            self.player_hp = min(100, self.player_hp + 10)

# ============================================================================
# ENHANCED BATTLE ENGINE
# ============================================================================

class EnhancedTesseractBattleEngine:
    """Enhanced battle engine with full mechanics"""

    def __init__(self):
        self.battle_states: Dict[str, EnhancedBattleState] = {}
        self.ai_strategies = self._initialize_ai_strategies()

    def _initialize_ai_strategies(self) -> Dict[str, Any]:
        """Initialize AI strategies for different difficulty levels"""
        return {
            'easy': {
                'aggression': 0.3,
                'combo_awareness': 0.2,
                'position_strategy': 0.1,
                'consciousness_priority': 0.1
            },
            'normal': {
                'aggression': 0.5,
                'combo_awareness': 0.5,
                'position_strategy': 0.3,
                'consciousness_priority': 0.3
            },
            'hard': {
                'aggression': 0.7,
                'combo_awareness': 0.8,
                'position_strategy': 0.6,
                'consciousness_priority': 0.5
            },
            'master': {
                'aggression': 0.9,
                'combo_awareness': 1.0,
                'position_strategy': 0.9,
                'consciousness_priority': 0.8
            }
        }

    def create_battle(self, player_deck: CompanionDeck,
                     opponent_deck: CompanionDeck,
                     difficulty: str = 'normal') -> EnhancedBattleState:
        """Create an enhanced battle state"""

        # Generate starting hands
        player_hand = self._generate_hand(player_deck, 5)
        opponent_hand = self._generate_hand(opponent_deck, 5)

        battle = EnhancedBattleState(
            player_deck=player_deck,
            opponent_deck=opponent_deck,
            player_hand=player_hand,
            opponent_hand=opponent_hand
        )

        # Store battle
        battle_id = f"battle_{len(self.battle_states)}"
        self.battle_states[battle_id] = battle

        return battle

    def _generate_hand(self, deck: CompanionDeck, size: int) -> List[EnhancedTesseractCard]:
        """Generate a starting hand"""
        hand = []
        suits = list(CardSuit)
        ranks = list(CardRank)

        for _ in range(size):
            # Generate card with position
            suit = random.choice(suits)
            rank = random.choice(ranks)

            # Random 4D position
            position = tuple(random.uniform(-1, 1) for _ in range(4))

            # Random starting dimension
            dimension = random.choice(list(TesseractDimension))

            card = EnhancedTesseractCard(suit, rank, position, dimension)
            hand.append(card)

        return hand

    def play_card(self, battle: EnhancedBattleState,
                 card: EnhancedTesseractCard,
                 player: str = 'player') -> Dict[str, Any]:
        """Play a card with full effect resolution"""

        results = {
            'damage': 0,
            'healing': 0,
            'cards_drawn': 0,
            'consciousness_gained': 0,
            'combos_triggered': [],
            'special_effects': []
        }

        # Add card to field
        battle.field_cards.append(card)
        battle.cards_played_total += 1

        # Check for combos
        combos = battle.check_combos(card)
        if combos:
            for combo in combos:
                bonus = battle.apply_combo_bonus(combo)
                results['combos_triggered'].append({
                    'cards': [str(c) for c in combo],
                    'bonus': bonus
                })
                battle.active_combos.append(combo)

        # Execute card effects
        card_results = card.execute(battle)

        # Apply combo multiplier
        if 'damage' in card_results:
            card_results['damage'] *= battle.combo_multiplier
            battle.damage_dealt_total += card_results['damage']

        # Merge results
        for key in card_results:
            if key in results:
                if isinstance(card_results[key], (int, float)):
                    results[key] += card_results[key]
                elif isinstance(card_results[key], list):
                    results[key].extend(card_results[key])

        # Check quantum entanglement
        battle.update_quantum_entanglement()

        # Process lasting effects
        battle.process_lasting_effects()

        # Check for dimension shift
        if battle.dimension_shifts >= 3:
            battle.shift_dimension()
            battle.dimension_shifts = 0
            results['special_effects'].append(f"Shifted to {battle.active_dimension.value}")

        # Record action
        battle.action_history.append({
            'turn': battle.turn_count,
            'player': player,
            'card': str(card),
            'results': results.copy()
        })

        return results

    def execute_ai_turn(self, battle: EnhancedBattleState,
                       difficulty: str = 'normal') -> Dict[str, Any]:
        """Execute sophisticated AI turn"""

        strategy = self.ai_strategies[difficulty]
        results = {
            'cards_played': [],
            'damage_dealt': 0,
            'strategy_used': None
        }

        # Analyze board state
        analysis = self._analyze_board_state(battle)

        # Decide strategy based on analysis and difficulty
        if analysis['player_hp_critical'] and strategy['aggression'] > 0.6:
            # Go for the kill
            results['strategy_used'] = 'aggressive'
            played_cards = self._play_aggressive(battle, strategy)

        elif analysis['combo_opportunity'] and strategy['combo_awareness'] > 0.5:
            # Set up combo
            results['strategy_used'] = 'combo_setup'
            played_cards = self._play_for_combo(battle, strategy)

        elif analysis['consciousness_low'] and strategy['consciousness_priority'] > 0.4:
            # Build consciousness
            results['strategy_used'] = 'consciousness_building'
            played_cards = self._play_for_consciousness(battle, strategy)

        else:
            # Balanced play
            results['strategy_used'] = 'balanced'
            played_cards = self._play_balanced(battle, strategy)

        # Execute chosen cards
        for card in played_cards:
            if card in battle.opponent_hand:
                battle.opponent_hand.remove(card)
                play_results = self.play_card(battle, card, 'opponent')
                results['cards_played'].append(str(card))
                results['damage_dealt'] += play_results.get('damage', 0)

        return results

    def _analyze_board_state(self, battle: EnhancedBattleState) -> Dict[str, Any]:
        """Analyze current board state for AI decision making"""
        return {
            'player_hp_critical': battle.player_hp < 30,
            'opponent_hp_critical': battle.opponent_hp < 30,
            'combo_opportunity': self._check_combo_opportunity(battle),
            'consciousness_low': battle.consciousness_level < 3,
            'tesseract_control': battle.calculate_tesseract_control(),
            'hand_size': len(battle.opponent_hand),
            'field_advantage': len([c for c in battle.field_cards
                                   if c in battle.opponent_hand]) > 3
        }

    def _check_combo_opportunity(self, battle: EnhancedBattleState) -> bool:
        """Check if there's a combo opportunity"""
        if len(battle.field_cards) < 2:
            return False

        # Check if recent cards could form a combo with hand cards
        recent = battle.field_cards[-2:]
        for card in battle.opponent_hand[:3]:  # Check first 3 cards
            test_combo = recent + [card]
            if battle._is_fibonacci_combo(test_combo) or battle._is_l4_combo(test_combo):
                return True
        return False

    def _play_aggressive(self, battle: EnhancedBattleState,
                        strategy: Dict) -> List[EnhancedTesseractCard]:
        """Play aggressively for maximum damage"""
        # Sort cards by damage potential
        cards = sorted(battle.opponent_hand,
                      key=lambda c: self._estimate_damage(c, battle),
                      reverse=True)

        # Play up to 3 highest damage cards
        return cards[:min(3, len(cards))]

    def _play_for_combo(self, battle: EnhancedBattleState,
                       strategy: Dict) -> List[EnhancedTesseractCard]:
        """Play to set up combos"""
        # Look for cards that can form combos
        for card in battle.opponent_hand:
            recent = battle.field_cards[-2:] if len(battle.field_cards) >= 2 else battle.field_cards
            test_combo = recent + [card]

            if battle._is_fibonacci_combo(test_combo) or battle._is_l4_combo(test_combo):
                return [card]

        # No combo found, play normally
        return self._play_balanced(battle, strategy)

    def _play_for_consciousness(self, battle: EnhancedBattleState,
                               strategy: Dict) -> List[EnhancedTesseractCard]:
        """Play to increase consciousness level"""
        # Prioritize PSYCHE cards and cards with elevate effects
        psyche_cards = [c for c in battle.opponent_hand if c.suit == CardSuit.PSYCHE]

        if psyche_cards:
            return psyche_cards[:2]

        # Otherwise play cards that might trigger L4 combo
        return self._play_for_combo(battle, strategy)

    def _play_balanced(self, battle: EnhancedBattleState,
                      strategy: Dict) -> List[EnhancedTesseractCard]:
        """Balanced play style"""
        if not battle.opponent_hand:
            return []

        # Mix of damage and strategy
        cards_to_play = []

        # Play one high damage card
        damage_cards = sorted(battle.opponent_hand,
                            key=lambda c: self._estimate_damage(c, battle),
                            reverse=True)
        if damage_cards:
            cards_to_play.append(damage_cards[0])

        # Play one strategic card if available
        remaining = [c for c in battle.opponent_hand if c not in cards_to_play]
        if remaining:
            strategic = max(remaining, key=lambda c: c.combo_potential)
            cards_to_play.append(strategic)

        return cards_to_play

    def _estimate_damage(self, card: EnhancedTesseractCard,
                        battle: EnhancedBattleState) -> float:
        """Estimate damage potential of a card"""
        base_damage = 0

        for action in card.actions:
            if action.effect == CardEffect.DAMAGE:
                base_damage += action.power
            elif action.effect == CardEffect.COLLAPSE:
                base_damage += action.power * 1.5

        # Apply multipliers
        base_damage *= battle.combo_multiplier
        base_damage *= (1 + battle.resonance_field * 0.1)

        return base_damage

# ============================================================================
# VISUALIZATION SYSTEM
# ============================================================================

class TesseractBattleVisualizer:
    """ASCII visualization for tesseract battles"""

    @staticmethod
    def render_battle_state(battle: EnhancedBattleState) -> str:
        """Render the current battle state as ASCII art"""
        output = []

        # Header
        output.append("╔" + "═" * 58 + "╗")
        output.append("║" + "TESSERACT BATTLE".center(58) + "║")
        output.append("╠" + "═" * 58 + "╣")

        # Player stats
        player_hp_bar = TesseractBattleVisualizer._hp_bar(battle.player_hp)
        opponent_hp_bar = TesseractBattleVisualizer._hp_bar(battle.opponent_hp)

        output.append(f"║ YOU: {player_hp_bar} {battle.player_hp:.0f}/100" + " " * 20 + "║")
        output.append(f"║ OPP: {opponent_hp_bar} {battle.opponent_hp:.0f}/100" + " " * 20 + "║")

        # Consciousness and tesseract control
        output.append("╠" + "─" * 58 + "╣")
        consciousness = "●" * battle.consciousness_level + "○" * (7 - battle.consciousness_level)
        control_pct = battle.calculate_tesseract_control() * 100

        output.append(f"║ L4 Level: [{consciousness}]  Control: {control_pct:.0f}%" + " " * 15 + "║")

        # Current dimension
        output.append(f"║ Dimension: {battle.active_dimension.value}" + " " * 35 + "║")

        # Field state
        output.append("╠" + "─" * 58 + "╣")
        output.append(f"║ Field Cards: {len(battle.field_cards)}" + " " * 40 + "║")
        output.append(f"║ Active Combos: {len(battle.active_combos)}" + " " * 37 + "║")
        output.append(f"║ Resonance: {battle.resonance_field:.2f}×" + " " * 38 + "║")

        # Hand
        output.append("╠" + "═" * 58 + "╣")
        output.append(f"║ Your Hand: {len(battle.player_hand)} cards" + " " * 34 + "║")

        # Show hand cards
        for i, card in enumerate(battle.player_hand[:5]):
            card_str = f"{i+1}. {card}"
            output.append(f"║   {card_str}" + " " * (55 - len(card_str)) + "║")

        # Footer
        output.append("╚" + "═" * 58 + "╝")

        return "\n".join(output)

    @staticmethod
    def _hp_bar(hp: float, max_hp: float = 100, width: int = 20) -> str:
        """Create an HP bar"""
        filled = int((hp / max_hp) * width)
        empty = width - filled
        return "█" * filled + "░" * empty

    @staticmethod
    def render_card_played(card: EnhancedTesseractCard,
                          results: Dict[str, Any]) -> str:
        """Render a card being played"""
        output = []

        output.append(f"\n🎴 Playing {card}")
        output.append("─" * 40)

        if results.get('damage'):
            output.append(f"⚔️  Damage: {results['damage']:.1f}")

        if results.get('healing'):
            output.append(f"💚 Healing: {results['healing']:.1f}")

        if results.get('consciousness_gained'):
            output.append(f"🧠 Consciousness: +{results['consciousness_gained']}")

        if results.get('combos_triggered'):
            for combo in results['combos_triggered']:
                output.append(f"⚡ COMBO! {combo['bonus']:.1f}× multiplier")

        if results.get('special_effects'):
            for effect in results['special_effects']:
                output.append(f"✨ {effect}")

        return "\n".join(output)

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("🎴 Enhanced Tesseract Battle System Test")
    print("=" * 60)

    # Create test battle
    from tesseract_battle_system import EchoDeck, PrometheusDeck

    engine = EnhancedTesseractBattleEngine()
    visualizer = TesseractBattleVisualizer()

    echo_deck = EchoDeck()
    prometheus_deck = PrometheusDeck()

    battle = engine.create_battle(echo_deck, prometheus_deck, difficulty='normal')

    print("\n📊 Initial Battle State:")
    print(visualizer.render_battle_state(battle))

    # Test playing a card
    if battle.player_hand:
        card = battle.player_hand[0]
        print(f"\n🎮 Playing {card}...")

        results = engine.play_card(battle, card)
        print(visualizer.render_card_played(card, results))

        # Show updated state
        print("\n📊 Updated Battle State:")
        print(visualizer.render_battle_state(battle))

    # Test AI turn
    print("\n🤖 AI Turn...")
    ai_results = engine.execute_ai_turn(battle, 'normal')
    print(f"AI Strategy: {ai_results['strategy_used']}")
    print(f"Cards Played: {ai_results['cards_played']}")
    print(f"Damage Dealt: {ai_results['damage_dealt']:.1f}")

    print("\n✅ Enhanced battle system operational!")