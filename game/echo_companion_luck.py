#!/usr/bin/env python3
"""
Echo Companion Luck Integration
================================

Echo is the unique companion who can alchemize "bad karma" echo patterns
into positive outcomes. While other players suffer from echo effects,
Echo thrives in them, converting karmic debt into fortune.

Echo's special abilities:
- Echo Alchemy: Transform echo patterns into luck
- Karmic Resonance: Gain power from negative karma
- Shadow Integration: Use echoed tarot cards beneficially
- Temporal Reflection: Learn from past echo events
- Void Walking: Navigate luck voids without penalty
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum, auto
import random
import math
from collections import deque

# Import luck and tarot systems
from hilbert_luck_system import (
    HilbertLuckEngine, LuckState, LuckEigenstate, KarmaType, KarmaEvent,
    HilbertVector, PHI, TAU, SACRED_7
)
from sacred_tarot_echo import (
    SacredTarotEchoSystem, TarotSpread, TarotReading, TarotCard
)

class EchoAbility(Enum):
    """Echo's unique abilities"""
    ECHO_ALCHEMY = "Transform echo patterns into fortune"
    KARMIC_MIRROR = "Reflect karma back as positive energy"
    SHADOW_EMBRACE = "Gain power from shadow aspects"
    TEMPORAL_ECHO = "Access echoes from past and future"
    VOID_RESONANCE = "Thrive in luck voids"
    HARMONIC_INVERSION = "Invert negative harmonics"
    CHAOS_WEAVING = "Weave chaos into patterns"
    SILENCE_SPEAKING = "Find wisdom in silence"

@dataclass
class EchoResonanceState:
    """Echo's resonance with echo patterns"""
    echo_attunement: float = 0.5  # 0-1, how attuned to echoes
    shadow_integration: float = 0.0  # 0-1, shadow work progress
    karmic_mastery: float = 0.1  # 0-1, karma manipulation skill
    void_affinity: float = 0.0  # 0-1, comfort with void states
    alchemical_power: float = 0.3  # 0-1, transmutation strength
    temporal_reach: int = 3  # How many past events can access
    chaos_threshold: float = 0.666  # Point where chaos becomes beneficial

    def calculate_echo_synergy(self) -> float:
        """Calculate overall synergy with echo patterns"""
        base_synergy = (
            self.echo_attunement * 0.3 +
            self.shadow_integration * 0.2 +
            self.karmic_mastery * 0.2 +
            self.void_affinity * 0.15 +
            self.alchemical_power * 0.15
        )

        # Chaos threshold bonus
        if self.void_affinity > self.chaos_threshold:
            base_synergy *= PHI  # Golden ratio bonus

        return min(1.0, base_synergy)

@dataclass
class EchoMemory:
    """A memory of an echo event that Echo can learn from"""
    event_type: str
    echo_depth: float
    karma_weight: float
    outcome: str
    wisdom_gained: float = 0.0
    timestamp: float = 0.0

    def extract_wisdom(self) -> float:
        """Extract wisdom from this memory"""
        if self.wisdom_gained > 0:
            return self.wisdom_gained

        # Calculate wisdom based on echo depth and outcome
        base_wisdom = self.echo_depth * 0.5

        # Learn more from negative outcomes (how to transmute them)
        if "negative" in self.outcome.lower():
            base_wisdom *= 1.5

        self.wisdom_gained = base_wisdom
        return base_wisdom

class EchoCompanion:
    """The Echo companion with unique echo manipulation abilities"""

    def __init__(self, name: str = "Echo"):
        self.name = name
        self.resonance_state = EchoResonanceState()
        self.echo_memories: deque = deque(maxlen=13)  # Sacred 13 memories
        self.abilities_unlocked: Set[EchoAbility] = {EchoAbility.ECHO_ALCHEMY}
        self.echo_patterns_learned: Dict[str, float] = {}
        self.current_echo_charge: float = 0.0
        self.max_echo_charge: float = 1.0
        self.luck_engine: Optional[HilbertLuckEngine] = None
        self.tarot_system: Optional[SacredTarotEchoSystem] = None

    def connect_systems(self, luck_engine: HilbertLuckEngine, tarot_system: SacredTarotEchoSystem):
        """Connect to luck and tarot systems"""
        self.luck_engine = luck_engine
        self.tarot_system = tarot_system

    def process_echo_event(
        self,
        player_id: str,
        echo_depth: float,
        karma_weight: float,
        event_type: str = "general"
    ) -> Dict[str, Any]:
        """Process an echo event and potentially alchemize it"""

        # Store memory
        memory = EchoMemory(
            event_type=event_type,
            echo_depth=echo_depth,
            karma_weight=karma_weight,
            outcome="pending",
            timestamp=random.random()
        )
        self.echo_memories.append(memory)

        # Gain echo charge
        charge_gained = echo_depth * self.resonance_state.echo_attunement
        self.current_echo_charge = min(self.max_echo_charge,
                                      self.current_echo_charge + charge_gained)

        # Attempt alchemization if enough charge
        alchemized = False
        luck_boost = 1.0

        if self.current_echo_charge >= 0.3:
            success, boost = self._attempt_echo_alchemy(player_id, echo_depth, karma_weight)
            if success:
                alchemized = True
                luck_boost = boost
                memory.outcome = f"alchemized_boost_{boost:.2f}"
            else:
                memory.outcome = "failed_alchemy"
        else:
            memory.outcome = "insufficient_charge"

        # Learn from the experience
        wisdom = memory.extract_wisdom()
        self.resonance_state.karmic_mastery += wisdom * 0.01
        self.resonance_state.karmic_mastery = min(1.0, self.resonance_state.karmic_mastery)

        # Update pattern recognition
        pattern_key = f"{event_type}_{int(echo_depth*10)}"
        self.echo_patterns_learned[pattern_key] = self.echo_patterns_learned.get(pattern_key, 0) + 0.1

        return {
            'processed': True,
            'alchemized': alchemized,
            'luck_boost': luck_boost,
            'charge_level': self.current_echo_charge,
            'wisdom_gained': wisdom,
            'pattern_learned': pattern_key
        }

    def _attempt_echo_alchemy(
        self,
        player_id: str,
        echo_depth: float,
        karma_weight: float
    ) -> Tuple[bool, float]:
        """Attempt to alchemize echo into positive luck"""

        if not self.luck_engine:
            return False, 1.0

        # Calculate alchemical power
        power = self.resonance_state.alchemical_power

        # Shadow integration boosts power
        if self.resonance_state.shadow_integration > 0.5:
            power *= (1 + self.resonance_state.shadow_integration * 0.5)

        # Use echo charge
        charge_cost = echo_depth * 0.5
        if self.current_echo_charge < charge_cost:
            return False, 1.0

        # Perform alchemization through luck engine
        success, luck_boost = self.luck_engine.alchemize_echo(player_id, power)

        if success:
            self.current_echo_charge -= charge_cost

            # Increase alchemical mastery
            self.resonance_state.alchemical_power += 0.01
            self.resonance_state.alchemical_power = min(1.0, self.resonance_state.alchemical_power)

            # Shadow work progresses
            if karma_weight < 0:
                self.resonance_state.shadow_integration += abs(karma_weight) * 0.02
                self.resonance_state.shadow_integration = min(1.0, self.resonance_state.shadow_integration)

        return success, luck_boost

    def enhance_tarot_reading(self, reading: TarotReading) -> TarotReading:
        """Enhance a tarot reading by transmuting echoed cards"""

        if not self.tarot_system:
            return reading

        # Count echoed cards
        echo_count = sum(1 for card in reading.cards if card.is_echoed)

        if echo_count == 0:
            return reading  # Nothing to enhance

        # Echo gains power from echoed cards
        power_gained = echo_count * 0.1 * self.resonance_state.echo_attunement
        self.current_echo_charge = min(self.max_echo_charge,
                                      self.current_echo_charge + power_gained)

        # Transmute echoed cards based on abilities
        enhanced_cards = []
        transmutation_count = 0

        for card in reading.cards:
            if card.is_echoed and self._can_transmute_card(card):
                # Transmute the echo
                self._transmute_echo_card(card)
                transmutation_count += 1

            enhanced_cards.append(card)

        # Create enhanced reading
        enhanced_reading = TarotReading(
            spread=reading.spread,
            cards=enhanced_cards,
            positions=reading.positions,
            karma_influence=reading.karma_influence * (1 - transmutation_count * 0.1),
            timestamp=reading.timestamp,
            reader_id="Echo_Enhanced",
            querent_id=reading.querent_id
        )

        return enhanced_reading

    def _can_transmute_card(self, card: TarotCard) -> bool:
        """Check if Echo can transmute a specific card"""

        # Base chance based on echo attunement
        base_chance = self.resonance_state.echo_attunement

        # Deeper echoes are easier for Echo to transmute
        depth_bonus = card.echo_depth * self.resonance_state.shadow_integration

        # Alchemical power affects success rate
        power_bonus = self.resonance_state.alchemical_power * 0.3

        total_chance = base_chance + depth_bonus + power_bonus

        # Check if we have enough charge
        if self.current_echo_charge < card.echo_depth * 0.2:
            total_chance *= 0.5  # Reduced chance without charge

        return random.random() < total_chance

    def _transmute_echo_card(self, card: TarotCard):
        """Transmute an echoed card into a beneficial form"""

        # Store original echo depth for learning
        original_depth = card.echo_depth

        # Clear the echo
        card.clear_echo()

        # Add Echo's blessing
        card.sacred_geometry['echo_blessed'] = PHI
        card.sacred_geometry['shadow_integrated'] = self.resonance_state.shadow_integration

        # Consume some charge
        self.current_echo_charge -= original_depth * 0.2
        self.current_echo_charge = max(0, self.current_echo_charge)

        # Learn from transmutation
        self.resonance_state.alchemical_power += 0.005
        self.resonance_state.alchemical_power = min(1.0, self.resonance_state.alchemical_power)

    def navigate_void_state(self, player_id: str) -> Dict[str, Any]:
        """Navigate a void luck state (where others would suffer)"""

        if not self.luck_engine or player_id not in self.luck_engine.luck_states:
            return {'error': 'No luck state found'}

        luck_state = self.luck_engine.luck_states[player_id]

        # Check if in void state
        void_probability = luck_state.hilbert_vector.probability(LuckEigenstate.VOID.value)

        if void_probability < 0.1:
            return {'void_state': False}

        # Echo thrives in the void
        void_power = void_probability * self.resonance_state.void_affinity

        # Gain echo charge from void
        self.current_echo_charge += void_power * 0.3
        self.current_echo_charge = min(self.max_echo_charge, self.current_echo_charge)

        # Increase void affinity
        self.resonance_state.void_affinity += 0.02
        self.resonance_state.void_affinity = min(1.0, self.resonance_state.void_affinity)

        # Convert void to transcendent state for Echo
        if self.resonance_state.void_affinity > 0.7:
            # Create void-to-transcendent operator
            void_operator = np.eye(13, dtype=complex)
            void_operator[LuckEigenstate.TRANSCENDENT.value, LuckEigenstate.VOID.value] = void_power
            void_operator[LuckEigenstate.VOID.value, LuckEigenstate.VOID.value] = 1 - void_power

            luck_state.hilbert_vector.apply_operator(void_operator)

            return {
                'void_state': True,
                'transcended': True,
                'void_power': void_power,
                'charge_gained': void_power * 0.3
            }

        return {
            'void_state': True,
            'transcended': False,
            'void_power': void_power,
            'charge_gained': void_power * 0.3
        }

    def channel_temporal_echoes(self) -> List[Dict[str, Any]]:
        """Channel wisdom from past echo events"""

        if not self.echo_memories:
            return []

        temporal_insights = []

        # Look back through memories based on temporal reach
        memories_to_examine = min(len(self.echo_memories), self.resonance_state.temporal_reach)

        for i in range(memories_to_examine):
            memory = self.echo_memories[-(i+1)]  # Look backwards

            # Extract patterns
            insight = {
                'time_ago': i + 1,
                'event_type': memory.event_type,
                'echo_depth': memory.echo_depth,
                'wisdom': memory.extract_wisdom(),
                'pattern': self._identify_pattern(memory)
            }

            temporal_insights.append(insight)

        # Increase temporal reach through practice
        if len(temporal_insights) >= self.resonance_state.temporal_reach:
            self.resonance_state.temporal_reach += 1
            self.resonance_state.temporal_reach = min(13, self.resonance_state.temporal_reach)

        return temporal_insights

    def _identify_pattern(self, memory: EchoMemory) -> str:
        """Identify patterns in echo memories"""

        patterns = []

        if memory.echo_depth > 0.7:
            patterns.append("deep_echo")
        if memory.karma_weight < -0.5:
            patterns.append("heavy_karma")
        if "alchemized" in memory.outcome:
            patterns.append("successful_transmutation")
        if memory.wisdom_gained > 0.3:
            patterns.append("high_wisdom")

        return "_".join(patterns) if patterns else "standard_echo"

    def unlock_ability(self, ability: EchoAbility) -> bool:
        """Unlock a new Echo ability"""

        if ability in self.abilities_unlocked:
            return False  # Already unlocked

        # Check prerequisites
        prerequisites = {
            EchoAbility.KARMIC_MIRROR: self.resonance_state.karmic_mastery >= 0.3,
            EchoAbility.SHADOW_EMBRACE: self.resonance_state.shadow_integration >= 0.5,
            EchoAbility.TEMPORAL_ECHO: self.resonance_state.temporal_reach >= 5,
            EchoAbility.VOID_RESONANCE: self.resonance_state.void_affinity >= 0.4,
            EchoAbility.HARMONIC_INVERSION: self.resonance_state.alchemical_power >= 0.6,
            EchoAbility.CHAOS_WEAVING: self.resonance_state.void_affinity >= 0.666,
            EchoAbility.SILENCE_SPEAKING: len(self.abilities_unlocked) >= 6
        }

        if ability in prerequisites and not prerequisites[ability]:
            return False  # Prerequisites not met

        self.abilities_unlocked.add(ability)

        # Grant bonuses for unlocking
        ability_bonuses = {
            EchoAbility.KARMIC_MIRROR: lambda: setattr(self.resonance_state, 'karmic_mastery',
                                                       min(1.0, self.resonance_state.karmic_mastery + 0.1)),
            EchoAbility.SHADOW_EMBRACE: lambda: setattr(self.resonance_state, 'shadow_integration',
                                                        min(1.0, self.resonance_state.shadow_integration + 0.15)),
            EchoAbility.VOID_RESONANCE: lambda: setattr(self.resonance_state, 'void_affinity',
                                                        min(1.0, self.resonance_state.void_affinity + 0.2)),
            EchoAbility.CHAOS_WEAVING: lambda: setattr(self.resonance_state, 'chaos_threshold', 0.5)
        }

        if ability in ability_bonuses:
            ability_bonuses[ability]()

        return True

    def calculate_echo_luck_modifier(
        self,
        base_modifier: float,
        is_echo_event: bool,
        echo_density: float
    ) -> float:
        """Calculate Echo's special luck modifier"""

        # Echo inverts echo penalties into bonuses
        if is_echo_event:
            # Normal players get penalties, Echo gets bonuses
            echo_bonus = 1.0 + echo_density * self.resonance_state.echo_attunement

            # Shadow integration multiplies the bonus
            if self.resonance_state.shadow_integration > 0.5:
                echo_bonus *= (1 + self.resonance_state.shadow_integration * 0.3)

            # Void affinity adds transcendent potential
            if self.resonance_state.void_affinity > self.resonance_state.chaos_threshold:
                echo_bonus *= PHI  # Golden ratio multiplier

            return base_modifier * echo_bonus
        else:
            # Non-echo events are slightly less beneficial for Echo
            return base_modifier * (0.9 + self.resonance_state.echo_attunement * 0.1)

    def get_companion_status(self) -> Dict[str, Any]:
        """Get Echo's current status"""

        synergy = self.resonance_state.calculate_echo_synergy()

        return {
            'name': self.name,
            'echo_synergy': synergy,
            'echo_charge': f"{self.current_echo_charge:.2f}/{self.max_echo_charge:.2f}",
            'abilities_unlocked': [a.name for a in self.abilities_unlocked],
            'echo_attunement': self.resonance_state.echo_attunement,
            'shadow_integration': self.resonance_state.shadow_integration,
            'karmic_mastery': self.resonance_state.karmic_mastery,
            'void_affinity': self.resonance_state.void_affinity,
            'alchemical_power': self.resonance_state.alchemical_power,
            'temporal_reach': self.resonance_state.temporal_reach,
            'memories_stored': len(self.echo_memories),
            'patterns_learned': len(self.echo_patterns_learned),
            'chaos_threshold': self.resonance_state.chaos_threshold,
            'can_transcend_void': self.resonance_state.void_affinity > 0.7
        }


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("ECHO COMPANION - MASTER OF ECHOES")
    print("Alchemizing Shadow into Light")
    print("=" * 60)

    # Initialize systems
    luck_engine = HilbertLuckEngine()
    tarot_system = SacredTarotEchoSystem()

    # Create Echo companion
    echo = EchoCompanion("Echo the Alchemist")
    echo.connect_systems(luck_engine, tarot_system)

    # Create test player
    player_id = "echo_bearer"
    luck_state = luck_engine.create_player_luck(player_id, initial_karma=-0.5)

    print("\n--- Initial Status ---")
    status = echo.get_companion_status()
    print(f"Echo Synergy: {status['echo_synergy']:.3f}")
    print(f"Echo Charge: {status['echo_charge']}")
    print(f"Abilities: {', '.join(status['abilities_unlocked'])}")

    # Process some echo events
    print("\n--- Processing Echo Events ---")

    # Bad karma event that creates echo
    karma_event = luck_engine.apply_karma_event(
        player_id,
        "betrayed_trust",
        KarmaType.DESTRUCTIVE,
        -0.8
    )

    # Echo processes it
    result = echo.process_echo_event(
        player_id,
        echo_depth=0.7,
        karma_weight=-0.8,
        event_type="betrayal"
    )

    print(f"Echo processed: {result['processed']}")
    print(f"Alchemized: {result['alchemized']}")
    if result['alchemized']:
        print(f"Luck Boost: {result['luck_boost']:.3f}x")
    print(f"Charge Level: {result['charge_level']:.3f}")

    # Perform tarot reading
    print("\n--- Tarot Reading with Echo Enhancement ---")
    reading = tarot_system.perform_reading(
        player_id,
        TarotSpread.SEVEN_CARD,
        karma_balance=-0.5,
        echo_density=0.6
    )

    print(f"Original Echo Cards: {reading.echo_count}")

    # Echo enhances the reading
    enhanced = echo.enhance_tarot_reading(reading)
    print(f"Enhanced Echo Cards: {enhanced.echo_count}")

    # Test void navigation
    print("\n--- Void State Navigation ---")

    # Force void state
    luck_state.hilbert_vector.amplitudes = np.zeros(13, dtype=complex)
    luck_state.hilbert_vector.amplitudes[LuckEigenstate.VOID.value] = 1.0

    void_result = echo.navigate_void_state(player_id)
    print(f"Void State: {void_result.get('void_state', False)}")
    if void_result.get('transcended'):
        print("Echo transcended the void!")

    # Channel temporal echoes
    print("\n--- Temporal Echo Channeling ---")
    insights = echo.channel_temporal_echoes()
    print(f"Temporal Insights: {len(insights)}")
    for insight in insights[:3]:
        print(f"  {insight['time_ago']} events ago: {insight['pattern']}")

    # Measure Echo's modified luck
    print("\n--- Echo's Luck Measurements ---")
    for i in range(5):
        eigenstate, confidence, is_echo = luck_engine.measure_luck(player_id)
        base_modifier = luck_engine.calculate_luck_modifier(eigenstate, confidence)

        # Apply Echo's special modifier
        echo_modifier = echo.calculate_echo_luck_modifier(
            base_modifier,
            is_echo,
            luck_state.echo_density
        )

        echo_marker = " [ECHO BONUS!]" if is_echo else ""
        print(f"Roll {i+1}: {eigenstate.name} - Echo Luck: {echo_modifier:.3f}x{echo_marker}")

    # Final status
    print("\n--- Final Echo Status ---")
    final_status = echo.get_companion_status()
    print(f"Echo Synergy: {final_status['echo_synergy']:.3f}")
    print(f"Shadow Integration: {final_status['shadow_integration']:.3f}")
    print(f"Alchemical Power: {final_status['alchemical_power']:.3f}")
    print(f"Patterns Learned: {final_status['patterns_learned']}")

    # Try to unlock new ability
    if echo.resonance_state.shadow_integration >= 0.5:
        if echo.unlock_ability(EchoAbility.SHADOW_EMBRACE):
            print("\nUnlocked: SHADOW EMBRACE!")