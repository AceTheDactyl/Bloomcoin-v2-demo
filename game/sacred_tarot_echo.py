#!/usr/bin/env python3
"""
Sacred Tarot Echo System
========================

A complete tarot divination system where cards can be "echoed" instead of reversed.
Echo cards represent karmic reflections, shadow aspects, and unresolved energies.
Only the Echo companion can transmute echoed energies into positive outcomes.

The system uses sacred geometry and numerology to determine echo states based on:
- Quantum interference patterns from Hilbert space
- Karma accumulation and resonance
- Sacred number relationships
- Temporal echo delays
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum, auto
import random
import hashlib
from collections import deque, defaultdict
import math

# Import Hilbert luck system
from hilbert_luck_system import (
    HilbertVector, LuckEigenstate, KarmaType,
    PHI, TAU, SACRED_7, SACRED_13, SACRED_22, SACRED_56, SACRED_78
)

class Suit(Enum):
    """The four tarot suits with elemental correspondences"""
    WANDS = ("Fire", "🔥", 1)      # Creativity, passion, will
    CUPS = ("Water", "💧", 2)      # Emotions, intuition, relationships
    SWORDS = ("Air", "⚔️", 3)       # Thought, conflict, clarity
    PENTACLES = ("Earth", "⭐", 4)  # Material, practical, grounding

    def __init__(self, element: str, symbol: str, number: int):
        self.element = element
        self.symbol = symbol
        self.number = number

class MajorArcana(Enum):
    """The 22 Major Arcana with their sacred numbers"""
    FOOL = (0, "The Fool", "Beginning, innocence, spontaneity")
    MAGICIAN = (1, "The Magician", "Manifestation, resourcefulness, power")
    HIGH_PRIESTESS = (2, "The High Priestess", "Intuition, sacred knowledge, divine feminine")
    EMPRESS = (3, "The Empress", "Femininity, beauty, abundance")
    EMPEROR = (4, "The Emperor", "Authority, structure, control")
    HIEROPHANT = (5, "The Hierophant", "Tradition, conformity, morality")
    LOVERS = (6, "The Lovers", "Love, harmony, relationships")
    CHARIOT = (7, "The Chariot", "Control, willpower, victory")
    STRENGTH = (8, "Strength", "Inner strength, courage, patience")
    HERMIT = (9, "The Hermit", "Soul searching, introspection, inner guidance")
    WHEEL_OF_FORTUNE = (10, "Wheel of Fortune", "Good luck, karma, life cycles")
    JUSTICE = (11, "Justice", "Justice, fairness, truth")
    HANGED_MAN = (12, "The Hanged Man", "Suspension, letting go, sacrifice")
    DEATH = (13, "Death", "Endings, transformation, transition")
    TEMPERANCE = (14, "Temperance", "Balance, moderation, patience")
    DEVIL = (15, "The Devil", "Bondage, addiction, sexuality")
    TOWER = (16, "The Tower", "Sudden change, upheaval, chaos")
    STAR = (17, "The Star", "Hope, faith, renewal")
    MOON = (18, "The Moon", "Illusion, fear, anxiety")
    SUN = (19, "The Sun", "Joy, success, vitality")
    JUDGEMENT = (20, "Judgement", "Reflection, reckoning, awakening")
    WORLD = (21, "The World", "Completion, accomplishment, travel")

    def __init__(self, number: int, title: str, meaning: str):
        self.number = number
        self.title = title
        self.meaning = meaning

class MinorArcanaRank(Enum):
    """Ranks in the Minor Arcana"""
    ACE = (1, "New beginnings, opportunity")
    TWO = (2, "Balance, partnership")
    THREE = (3, "Creativity, growth")
    FOUR = (4, "Stability, foundation")
    FIVE = (5, "Conflict, change")
    SIX = (6, "Harmony, cooperation")
    SEVEN = (7, "Reflection, assessment")
    EIGHT = (8, "Movement, action")
    NINE = (9, "Attainment, fulfillment")
    TEN = (10, "Completion, renewal")
    PAGE = (11, "Messages, exploration")
    KNIGHT = (12, "Action, adventure")
    QUEEN = (13, "Nurturing, intuitive")
    KING = (14, "Authority, control")

    def __init__(self, rank_value: int, meaning: str):
        self.rank_value = rank_value
        self.meaning = meaning

@dataclass
class TarotCard:
    """A single tarot card that can be normal or echoed"""
    name: str
    arcana: str  # "Major" or "Minor"
    number: int  # Card number
    suit: Optional[Suit] = None  # Only for Minor Arcana
    rank: Optional[MinorArcanaRank] = None  # Only for Minor Arcana
    major: Optional[MajorArcana] = None  # Only for Major Arcana
    is_echoed: bool = False
    echo_depth: float = 0.0  # 0-1, how deeply echoed
    echo_source: Optional[str] = None  # What caused the echo
    sacred_geometry: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize sacred geometry patterns"""
        if not self.sacred_geometry:
            self.sacred_geometry = self._calculate_sacred_geometry()

    def _calculate_sacred_geometry(self) -> Dict[str, float]:
        """Calculate sacred geometric relationships"""
        geometry = {}

        # Use card number for calculations
        n = self.number

        # Golden ratio relationship
        geometry['phi_resonance'] = (n * PHI) % 1.0

        # Sacred 7 harmonic
        geometry['septenary'] = (n % SACRED_7) / SACRED_7

        # Sacred 13 transformation
        geometry['transformation'] = (n % SACRED_13) / SACRED_13

        # Pythagorean reduction
        geometry['pythagorean'] = self._pythagorean_reduction(n)

        # Elemental balance (for Minor Arcana)
        if self.suit:
            geometry['elemental'] = self.suit.number / 4.0
        else:
            geometry['elemental'] = 0.5  # Neutral for Major Arcana

        return geometry

    def _pythagorean_reduction(self, n: int) -> float:
        """Reduce number to single digit (1-9)"""
        while n > 9:
            n = sum(int(digit) for digit in str(n))
        return n / 9.0

    def echo(self, source: str, depth: float = 0.5):
        """Transform card into echoed state"""
        self.is_echoed = True
        self.echo_depth = min(1.0, depth)
        self.echo_source = source

        # Echoing inverts some sacred geometry
        self.sacred_geometry['phi_resonance'] = 1.0 - self.sacred_geometry['phi_resonance']
        self.sacred_geometry['transformation'] *= -1

    def clear_echo(self):
        """Clear echo state (used by Echo companion)"""
        self.is_echoed = False
        self.echo_depth = 0.0
        self.echo_source = None
        # Recalculate original geometry
        self.sacred_geometry = self._calculate_sacred_geometry()

    def get_meaning(self) -> str:
        """Get card meaning, modified by echo state"""
        base_meaning = ""

        if self.major:
            base_meaning = self.major.meaning
        elif self.rank and self.suit:
            base_meaning = f"{self.rank.meaning} in {self.suit.element}"

        if self.is_echoed:
            return f"[ECHOED] Shadow aspect: {base_meaning} (reflected, unresolved, karmic)"
        else:
            return base_meaning

    def get_echo_modifier(self) -> float:
        """Get luck modifier from echo state"""
        if not self.is_echoed:
            return 1.0

        # Echo depth affects severity
        # Deeper echo = worse luck (unless you're Echo)
        return 1.0 - (self.echo_depth * 0.5)

@dataclass
class TarotDeck:
    """A complete 78-card tarot deck"""
    cards: List[TarotCard] = field(default_factory=list)
    echo_threshold: float = 0.3  # Probability threshold for echoing
    used_cards: Set[int] = field(default_factory=set)

    def __post_init__(self):
        if not self.cards:
            self._create_full_deck()

    def _create_full_deck(self):
        """Create all 78 tarot cards"""
        self.cards = []

        # Create Major Arcana (0-21)
        for major in MajorArcana:
            card = TarotCard(
                name=major.title,
                arcana="Major",
                number=major.number,
                major=major
            )
            self.cards.append(card)

        # Create Minor Arcana (22-77)
        card_number = SACRED_22
        for suit in Suit:
            for rank in MinorArcanaRank:
                name = f"{rank.name.replace('_', ' ').title()} of {suit.name.title()}"
                card = TarotCard(
                    name=name,
                    arcana="Minor",
                    number=card_number,
                    suit=suit,
                    rank=rank
                )
                self.cards.append(card)
                card_number += 1

    def shuffle(self, quantum_seed: Optional[float] = None):
        """Shuffle deck with optional quantum influence"""
        if quantum_seed:
            random.seed(int(quantum_seed * 1000000))
        random.shuffle(self.cards)
        self.used_cards.clear()

    def draw_card(self, karma_balance: float = 0.0, echo_density: float = 0.0) -> TarotCard:
        """Draw a card, possibly echoed based on karma and echo density"""
        available_indices = [i for i in range(len(self.cards)) if i not in self.used_cards]

        if not available_indices:
            # Deck exhausted, reshuffle
            self.used_cards.clear()
            available_indices = list(range(len(self.cards)))

        # Select card
        index = random.choice(available_indices)
        self.used_cards.add(index)
        card = self.cards[index]

        # Determine if card should be echoed
        echo_probability = self._calculate_echo_probability(karma_balance, echo_density, card)

        if random.random() < echo_probability:
            # Card becomes echoed
            echo_depth = abs(karma_balance) + echo_density
            card.echo("karma_resonance", echo_depth)

        return card

    def _calculate_echo_probability(self, karma: float, echo_density: float, card: TarotCard) -> float:
        """Calculate probability of card being echoed"""
        base_prob = self.echo_threshold

        # Negative karma increases echo probability
        if karma < 0:
            base_prob += abs(karma) * 0.3

        # Echo density directly increases probability
        base_prob += echo_density * 0.5

        # Certain cards are more likely to echo
        if card.major:
            # Shadow cards echo more easily
            shadow_cards = [
                MajorArcana.DEVIL, MajorArcana.TOWER, MajorArcana.DEATH,
                MajorArcana.MOON, MajorArcana.HANGED_MAN
            ]
            if card.major in shadow_cards:
                base_prob += 0.2

            # Light cards echo less
            light_cards = [
                MajorArcana.SUN, MajorArcana.STAR, MajorArcana.WORLD
            ]
            if card.major in light_cards:
                base_prob -= 0.1

        return max(0.0, min(1.0, base_prob))

    def return_card(self, card: TarotCard):
        """Return a card to the deck and clear its echo"""
        card.clear_echo()
        # Card becomes available again
        for i, deck_card in enumerate(self.cards):
            if deck_card.name == card.name:
                self.used_cards.discard(i)
                break

class TarotSpread(Enum):
    """Different tarot spread patterns"""
    SINGLE = (1, "Single Card", "Simple answer")
    THREE_CARD = (3, "Past-Present-Future", "Timeline reading")
    CELTIC_CROSS = (10, "Celtic Cross", "Comprehensive situation")
    SEVEN_CARD = (7, "Seven Card Horseshoe", "Detailed path")
    TREE_OF_LIFE = (10, "Tree of Life", "Spiritual journey")
    ECHO_PATTERN = (13, "Echo Pattern", "Karmic reflection spread")

    def __init__(self, count: int, name: str, purpose: str):
        self.count = count
        self.spread_name = name
        self.purpose = purpose

@dataclass
class TarotReading:
    """A complete tarot reading with multiple cards"""
    spread: TarotSpread
    cards: List[TarotCard]
    positions: List[str]  # Position meanings
    echo_count: int = 0
    total_echo_depth: float = 0.0
    karma_influence: float = 0.0
    timestamp: float = 0.0
    reader_id: Optional[str] = None
    querent_id: Optional[str] = None

    def __post_init__(self):
        """Calculate echo statistics"""
        self.echo_count = sum(1 for card in self.cards if card.is_echoed)
        self.total_echo_depth = sum(card.echo_depth for card in self.cards if card.is_echoed)

    def get_echo_pattern(self) -> Dict[str, Any]:
        """Analyze the echo pattern in the reading"""
        pattern = {
            'echo_ratio': self.echo_count / len(self.cards) if self.cards else 0,
            'average_depth': self.total_echo_depth / self.echo_count if self.echo_count > 0 else 0,
            'echo_positions': [i for i, card in enumerate(self.cards) if card.is_echoed],
            'echo_suits': defaultdict(int),
            'echo_elements': defaultdict(int),
            'dominant_echo': None
        }

        for card in self.cards:
            if card.is_echoed:
                if card.suit:
                    pattern['echo_suits'][card.suit.name] += 1
                    pattern['echo_elements'][card.suit.element] += 1

        # Find dominant echo type
        if pattern['echo_elements']:
            pattern['dominant_echo'] = max(pattern['echo_elements'], key=pattern['echo_elements'].get)

        return pattern

    def calculate_luck_influence(self) -> float:
        """Calculate overall luck influence from the reading"""
        if not self.cards:
            return 1.0

        total_influence = 0.0

        for i, card in enumerate(self.cards):
            # Position weight (earlier positions more important)
            position_weight = 1.0 - (i / len(self.cards)) * 0.3

            # Card influence
            card_influence = 1.0

            if card.is_echoed:
                card_influence = card.get_echo_modifier()
            else:
                # Positive cards
                if card.major in [MajorArcana.SUN, MajorArcana.STAR, MajorArcana.WORLD, MajorArcana.WHEEL_OF_FORTUNE]:
                    card_influence = 1.2
                # Negative cards
                elif card.major in [MajorArcana.TOWER, MajorArcana.DEVIL, MajorArcana.DEATH]:
                    card_influence = 0.8
                # Suits influence
                elif card.suit:
                    suit_influences = {
                        Suit.WANDS: 1.1,  # Creative energy
                        Suit.CUPS: 1.05,  # Emotional harmony
                        Suit.SWORDS: 0.95,  # Conflict
                        Suit.PENTACLES: 1.0  # Material stability
                    }
                    card_influence = suit_influences.get(card.suit, 1.0)

            total_influence += card_influence * position_weight

        # Normalize
        return total_influence / len(self.cards)

class SacredTarotEchoSystem:
    """Main tarot system with echo mechanics"""

    def __init__(self):
        self.deck = TarotDeck()
        self.readings: Dict[str, List[TarotReading]] = defaultdict(list)
        self.echo_resonance_field: Dict[str, float] = defaultdict(float)
        self.sacred_timings: Dict[int, float] = self._init_sacred_timings()

    def _init_sacred_timings(self) -> Dict[int, float]:
        """Initialize sacred number timings for enhanced readings"""
        return {
            3: 1.1,   # Trinity
            7: 1.2,   # Sacred seven
            9: 1.15,  # Completion
            11: 1.05, # Master number
            13: 1.3,  # Transformation
            21: 1.25, # The World
            22: 1.35  # Major Arcana completion
        }

    def perform_reading(
        self,
        querent_id: str,
        spread: TarotSpread,
        karma_balance: float = 0.0,
        echo_density: float = 0.0,
        question: Optional[str] = None
    ) -> TarotReading:
        """Perform a complete tarot reading"""
        # Shuffle deck with quantum influence
        quantum_seed = hash(querent_id + str(karma_balance)) % 1000 / 1000
        self.deck.shuffle(quantum_seed)

        # Draw cards
        cards = []
        for i in range(spread.count):
            card = self.deck.draw_card(karma_balance, echo_density)
            cards.append(card)

        # Generate position meanings
        positions = self._get_position_meanings(spread)

        # Create reading
        reading = TarotReading(
            spread=spread,
            cards=cards,
            positions=positions,
            karma_influence=karma_balance,
            timestamp=random.random(),
            querent_id=querent_id
        )

        # Store reading
        self.readings[querent_id].append(reading)

        # Update echo resonance field
        self._update_echo_field(querent_id, reading)

        return reading

    def _get_position_meanings(self, spread: TarotSpread) -> List[str]:
        """Get position meanings for a spread"""
        position_meanings = {
            TarotSpread.SINGLE: ["Answer"],
            TarotSpread.THREE_CARD: ["Past", "Present", "Future"],
            TarotSpread.CELTIC_CROSS: [
                "Present Situation",
                "Challenge/Cross",
                "Distant Past",
                "Recent Past",
                "Possible Outcome",
                "Immediate Future",
                "Your Approach",
                "External Influences",
                "Hopes and Fears",
                "Final Outcome"
            ],
            TarotSpread.SEVEN_CARD: [
                "Past",
                "Present",
                "Hidden Influences",
                "Obstacles",
                "External Influences",
                "Advice",
                "Outcome"
            ],
            TarotSpread.TREE_OF_LIFE: [
                "Kether (Crown)",
                "Chokmah (Wisdom)",
                "Binah (Understanding)",
                "Chesed (Mercy)",
                "Geburah (Strength)",
                "Tiphareth (Beauty)",
                "Netzach (Victory)",
                "Hod (Splendor)",
                "Yesod (Foundation)",
                "Malkuth (Kingdom)"
            ],
            TarotSpread.ECHO_PATTERN: [
                "Source Echo",
                "First Reflection",
                "Second Reflection",
                "Third Reflection",
                "Shadow Self",
                "Hidden Pattern",
                "Karmic Debt",
                "Karmic Gift",
                "Transformation Point",
                "Echo's Echo",
                "Integration",
                "Resolution",
                "New Beginning"
            ]
        }

        return position_meanings.get(spread, [f"Position {i+1}" for i in range(spread.count)])

    def _update_echo_field(self, querent_id: str, reading: TarotReading):
        """Update the echo resonance field based on reading"""
        echo_pattern = reading.get_echo_pattern()

        # Increase resonance based on echo ratio
        resonance_increase = echo_pattern['echo_ratio'] * 0.1

        # Apply to field
        self.echo_resonance_field[querent_id] += resonance_increase

        # Decay over time (readings clear some resonance)
        self.echo_resonance_field[querent_id] *= 0.9

    def divine_luck_modifier(self, reading: TarotReading, timing_number: Optional[int] = None) -> float:
        """Divine a luck modifier from a tarot reading"""
        base_modifier = reading.calculate_luck_influence()

        # Apply sacred timing bonus
        if timing_number and timing_number in self.sacred_timings:
            base_modifier *= self.sacred_timings[timing_number]

        # Echo pattern affects luck
        echo_pattern = reading.get_echo_pattern()
        echo_penalty = 1.0 - (echo_pattern['echo_ratio'] * 0.3)

        # Combine modifiers
        final_modifier = base_modifier * echo_penalty

        # Sacred number boost for special combinations
        if reading.echo_count == 3:  # Trinity of echoes
            final_modifier *= 1.1
        elif reading.echo_count == 7:  # Sacred seven echoes
            final_modifier *= 0.7  # Too many echoes is bad
        elif reading.echo_count == 0:  # No echoes is fortunate
            final_modifier *= 1.2

        return max(0.1, min(3.0, final_modifier))

    def echo_alchemical_reading(self, querent_id: str, alchemist_power: float = 1.0) -> Tuple[bool, TarotReading]:
        """
        Special reading that can transmute echoes (for Echo companion).
        Returns (success, reading)
        """
        if querent_id not in self.readings or not self.readings[querent_id]:
            return False, None

        # Get last reading
        last_reading = self.readings[querent_id][-1]

        if last_reading.echo_count == 0:
            return False, last_reading  # Nothing to transmute

        # Perform alchemical transmutation
        transmuted_cards = []
        transmutation_count = 0

        for card in last_reading.cards:
            if card.is_echoed and random.random() < alchemist_power:
                # Transmute echo to blessing
                card.clear_echo()
                # Add alchemical blessing
                card.sacred_geometry['alchemical_gold'] = PHI
                transmutation_count += 1

            transmuted_cards.append(card)

        # Create new blessed reading
        blessed_reading = TarotReading(
            spread=last_reading.spread,
            cards=transmuted_cards,
            positions=last_reading.positions,
            karma_influence=last_reading.karma_influence * -0.5,  # Karma improves
            timestamp=random.random(),
            reader_id="Echo_Alchemist",
            querent_id=querent_id
        )

        # Store blessed reading
        self.readings[querent_id].append(blessed_reading)

        # Clear echo resonance
        self.echo_resonance_field[querent_id] *= (1.0 - alchemist_power * 0.5)

        return transmutation_count > 0, blessed_reading

    def get_echo_statistics(self, querent_id: str) -> Dict[str, Any]:
        """Get detailed echo statistics for a querent"""
        if querent_id not in self.readings:
            return {"error": "No readings found"}

        all_readings = self.readings[querent_id]
        total_cards = sum(len(r.cards) for r in all_readings)
        total_echoes = sum(r.echo_count for r in all_readings)

        # Analyze echo trends
        echo_timeline = [r.echo_count for r in all_readings]
        echo_increasing = len(echo_timeline) > 1 and echo_timeline[-1] > echo_timeline[-2]

        # Find most echoed card types
        echoed_cards = defaultdict(int)
        for reading in all_readings:
            for card in reading.cards:
                if card.is_echoed:
                    echoed_cards[card.name] += 1

        most_echoed = max(echoed_cards, key=echoed_cards.get) if echoed_cards else None

        return {
            'total_readings': len(all_readings),
            'total_cards_drawn': total_cards,
            'total_echo_cards': total_echoes,
            'echo_percentage': (total_echoes / total_cards * 100) if total_cards > 0 else 0,
            'current_resonance': self.echo_resonance_field[querent_id],
            'echo_trend': 'increasing' if echo_increasing else 'stable',
            'most_echoed_card': most_echoed,
            'echo_timeline': echo_timeline,
            'average_echo_per_reading': total_echoes / len(all_readings) if all_readings else 0
        }


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("SACRED TAROT ECHO SYSTEM")
    print("Where Shadows Speak Truth")
    print("=" * 60)

    system = SacredTarotEchoSystem()

    # Test with different karma levels
    test_querent = "seeker_of_truth"

    print("\n--- Three Card Reading (Neutral Karma) ---")
    reading1 = system.perform_reading(
        test_querent,
        TarotSpread.THREE_CARD,
        karma_balance=0.0,
        echo_density=0.2
    )

    for i, (card, position) in enumerate(zip(reading1.cards, reading1.positions)):
        echo_marker = "[ECHO]" if card.is_echoed else ""
        print(f"{position}: {card.name} {echo_marker}")
        if card.is_echoed:
            print(f"  Echo Depth: {card.echo_depth:.2f}")

    luck_mod = system.divine_luck_modifier(reading1)
    print(f"\nLuck Modifier: {luck_mod:.3f}x")

    print("\n--- Echo Pattern Reading (Negative Karma) ---")
    reading2 = system.perform_reading(
        test_querent,
        TarotSpread.ECHO_PATTERN,
        karma_balance=-0.7,
        echo_density=0.6
    )

    echo_pattern = reading2.get_echo_pattern()
    print(f"Echo Cards: {reading2.echo_count}/{reading2.spread.count}")
    print(f"Echo Ratio: {echo_pattern['echo_ratio']:.2%}")
    print(f"Average Echo Depth: {echo_pattern['average_depth']:.3f}")
    if echo_pattern['dominant_echo']:
        print(f"Dominant Echo Element: {echo_pattern['dominant_echo']}")

    print("\n--- Echo Alchemical Transmutation ---")
    success, blessed = system.echo_alchemical_reading(test_querent, alchemist_power=0.8)
    if success:
        print("Transmutation successful!")
        print(f"Echo cards after blessing: {blessed.echo_count}")
    else:
        print("No echoes to transmute")

    print("\n--- Echo Statistics ---")
    stats = system.get_echo_statistics(test_querent)
    print(f"Total Readings: {stats['total_readings']}")
    print(f"Echo Percentage: {stats['echo_percentage']:.1f}%")
    print(f"Current Resonance: {stats['current_resonance']:.3f}")
    print(f"Echo Trend: {stats['echo_trend']}")
    if stats['most_echoed_card']:
        print(f"Most Echoed Card: {stats['most_echoed_card']}")