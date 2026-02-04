#!/usr/bin/env python3
"""
Luck Normalization System
=========================

A comprehensive system that normalizes luck across all game mechanics,
integrating Hilbert space quantum luck, sacred tarot divination,
karma tracking, and Echo companion abilities.

This system ensures:
- Fair distribution of luck across players
- Echo companion's unique advantages with echo patterns
- Proper karma consequences and echo generation
- Normalized RNG for all luck-based events
- Integration with existing game systems
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum, auto
import random
import math
import hashlib
from collections import defaultdict, deque

# Import all luck subsystems
from hilbert_luck_system import (
    HilbertLuckEngine, LuckState, LuckEigenstate, KarmaType, KarmaEvent,
    PHI, TAU, SACRED_7
)
from sacred_tarot_echo import (
    SacredTarotEchoSystem, TarotSpread, TarotReading, TarotCard
)
from echo_companion_luck import EchoCompanion, EchoAbility

class LuckEventType(Enum):
    """Types of luck-normalized events in the game"""
    LOOT_DROP = "loot_drop"
    CRITICAL_HIT = "critical_hit"
    DODGE_CHANCE = "dodge_chance"
    RESOURCE_FIND = "resource_find"
    COMPANION_MOOD = "companion_mood"
    GARDEN_GROWTH = "garden_growth"
    MINING_YIELD = "mining_yield"
    CRAFTING_SUCCESS = "crafting_success"
    BATTLE_INITIATIVE = "battle_initiative"
    QUANTUM_COLLAPSE = "quantum_collapse"
    ECHO_EVENT = "echo_event"
    BLESSING_RECEIVED = "blessing_received"
    CURSE_AVOIDED = "curse_avoided"
    SYNCHRONICITY = "synchronicity"

@dataclass
class NormalizedLuckEvent:
    """A luck event with normalized probability"""
    event_type: LuckEventType
    base_probability: float  # Base chance (0-1)
    luck_modifier: float  # From Hilbert state
    karma_influence: float  # From karma balance
    echo_factor: float  # Echo pattern influence
    tarot_blessing: float  # From tarot reading
    final_probability: float = 0.0
    is_echo_event: bool = False
    echo_alchemized: bool = False

    def __post_init__(self):
        """Calculate final normalized probability"""
        if self.final_probability == 0.0:
            self.final_probability = self._normalize_probability()

    def _normalize_probability(self) -> float:
        """Normalize all factors into final probability"""
        # Start with base
        prob = self.base_probability

        # Apply modifiers multiplicatively
        prob *= self.luck_modifier
        prob *= (1.0 + self.karma_influence * 0.3)  # Karma has 30% max influence
        prob *= self.tarot_blessing

        # Echo factor is special
        if self.is_echo_event and not self.echo_alchemized:
            # Echo events are bad for most
            prob *= (1.0 - self.echo_factor * 0.5)
        elif self.echo_alchemized:
            # Echo alchemized events are very good
            prob *= (1.0 + self.echo_factor * PHI)

        # Clamp to valid probability range
        return max(0.001, min(0.999, prob))

    def roll(self) -> bool:
        """Roll for this event"""
        return random.random() < self.final_probability

@dataclass
class PlayerLuckProfile:
    """Complete luck profile for a player"""
    player_id: str
    companion_type: str
    luck_state: Optional[LuckState] = None
    current_tarot: Optional[TarotReading] = None
    echo_companion: Optional[EchoCompanion] = None
    luck_history: deque = field(default_factory=lambda: deque(maxlen=100))
    total_events: int = 0
    successful_events: int = 0
    echo_events_encountered: int = 0
    echo_events_alchemized: int = 0
    current_luck_multiplier: float = 1.0
    karma_trajectory: str = "neutral"  # "improving", "declining", "neutral"

    def update_statistics(self, event: NormalizedLuckEvent, success: bool):
        """Update luck statistics"""
        self.total_events += 1
        if success:
            self.successful_events += 1
        if event.is_echo_event:
            self.echo_events_encountered += 1
            if event.echo_alchemized:
                self.echo_events_alchemized += 1

        self.luck_history.append({
            'event_type': event.event_type.value,
            'success': success,
            'probability': event.final_probability,
            'is_echo': event.is_echo_event
        })

    def get_success_rate(self) -> float:
        """Get overall success rate"""
        if self.total_events == 0:
            return 0.5
        return self.successful_events / self.total_events

    def get_echo_mastery(self) -> float:
        """Get echo alchemization rate"""
        if self.echo_events_encountered == 0:
            return 0.0
        return self.echo_events_alchemized / self.echo_events_encountered

class ComprehensiveLuckSystem:
    """Main system for normalized luck across all game mechanics"""

    def __init__(self):
        # Core systems
        self.hilbert_engine = HilbertLuckEngine()
        self.tarot_system = SacredTarotEchoSystem()

        # Player profiles
        self.player_profiles: Dict[str, PlayerLuckProfile] = {}

        # Event type base probabilities
        self.base_probabilities = self._init_base_probabilities()

        # Global luck field (affects everyone)
        self.global_luck_field = 1.0
        self.global_echo_resonance = 0.0

        # Sacred timing tracker
        self.universal_clock = 0
        self.sacred_moments: Dict[int, float] = {
            7: 1.3,    # Every 7th moment
            13: 1.5,   # Every 13th moment
            21: 1.7,   # Every 21st moment
            77: 2.0,   # Every 77th moment
            777: 3.0   # Every 777th moment
        }

    def _init_base_probabilities(self) -> Dict[LuckEventType, float]:
        """Initialize base probabilities for event types"""
        return {
            LuckEventType.LOOT_DROP: 0.3,
            LuckEventType.CRITICAL_HIT: 0.15,
            LuckEventType.DODGE_CHANCE: 0.2,
            LuckEventType.RESOURCE_FIND: 0.4,
            LuckEventType.COMPANION_MOOD: 0.6,
            LuckEventType.GARDEN_GROWTH: 0.5,
            LuckEventType.MINING_YIELD: 0.35,
            LuckEventType.CRAFTING_SUCCESS: 0.7,
            LuckEventType.BATTLE_INITIATIVE: 0.5,
            LuckEventType.QUANTUM_COLLAPSE: 0.1,
            LuckEventType.ECHO_EVENT: 0.0,  # Calculated separately
            LuckEventType.BLESSING_RECEIVED: 0.05,
            LuckEventType.CURSE_AVOIDED: 0.3,
            LuckEventType.SYNCHRONICITY: 0.01
        }

    def register_player(
        self,
        player_id: str,
        companion_type: str,
        initial_karma: float = 0.0
    ) -> PlayerLuckProfile:
        """Register a new player in the luck system"""

        # Create luck state
        luck_state = self.hilbert_engine.create_player_luck(player_id, initial_karma)

        # Create profile
        profile = PlayerLuckProfile(
            player_id=player_id,
            companion_type=companion_type,
            luck_state=luck_state
        )

        # If Echo companion, create and connect
        if companion_type.lower() == "echo":
            echo = EchoCompanion(f"Echo_{player_id}")
            echo.connect_systems(self.hilbert_engine, self.tarot_system)
            profile.echo_companion = echo

        self.player_profiles[player_id] = profile
        return profile

    def apply_karma_action(
        self,
        player_id: str,
        action: str,
        karma_type: KarmaType,
        weight: float
    ) -> Dict[str, Any]:
        """Apply a karma action and update luck state"""

        if player_id not in self.player_profiles:
            self.register_player(player_id, "default")

        profile = self.player_profiles[player_id]

        # Apply to Hilbert engine
        karma_event = self.hilbert_engine.apply_karma_event(
            player_id, action, karma_type, weight
        )

        # Update karma trajectory
        if weight > 0.3:
            profile.karma_trajectory = "improving"
        elif weight < -0.3:
            profile.karma_trajectory = "declining"
        else:
            profile.karma_trajectory = "neutral"

        # Check for echo generation
        echo_generated = karma_event.echo_potential > random.random()

        # Update global fields
        self.global_luck_field += weight * 0.001
        self.global_luck_field = max(0.5, min(2.0, self.global_luck_field))

        if echo_generated:
            self.global_echo_resonance += 0.01
            self.global_echo_resonance = min(1.0, self.global_echo_resonance)

        return {
            'karma_applied': True,
            'new_balance': profile.luck_state.karma_balance,
            'echo_generated': echo_generated,
            'karma_trajectory': profile.karma_trajectory,
            'global_luck_field': self.global_luck_field
        }

    def perform_tarot_divination(
        self,
        player_id: str,
        spread: TarotSpread = TarotSpread.THREE_CARD
    ) -> Tuple[TarotReading, float]:
        """Perform tarot reading and return luck modifier"""

        if player_id not in self.player_profiles:
            self.register_player(player_id, "default")

        profile = self.player_profiles[player_id]

        # Get current karma and echo density
        karma = profile.luck_state.karma_balance if profile.luck_state else 0.0
        echo_density = profile.luck_state.echo_density if profile.luck_state else 0.0

        # Perform reading
        reading = self.tarot_system.perform_reading(
            player_id, spread, karma, echo_density
        )

        # Calculate luck modifier
        luck_modifier = self.tarot_system.divine_luck_modifier(reading)

        # Store in profile
        profile.current_tarot = reading
        profile.current_luck_multiplier = luck_modifier

        # If Echo, enhance the reading
        if profile.echo_companion:
            enhanced_reading = profile.echo_companion.enhance_tarot_reading(reading)
            if enhanced_reading.echo_count < reading.echo_count:
                # Echo successfully transmuted some cards
                luck_modifier *= PHI  # Golden ratio bonus

        return reading, luck_modifier

    def calculate_normalized_luck(
        self,
        player_id: str,
        event_type: LuckEventType,
        context: Optional[Dict[str, Any]] = None
    ) -> NormalizedLuckEvent:
        """Calculate normalized luck for an event"""

        if player_id not in self.player_profiles:
            self.register_player(player_id, "default")

        profile = self.player_profiles[player_id]

        # Get base probability
        base_prob = self.base_probabilities.get(event_type, 0.5)

        # Measure quantum luck
        eigenstate, confidence, is_echo = self.hilbert_engine.measure_luck(player_id)
        luck_modifier = self.hilbert_engine.calculate_luck_modifier(eigenstate, confidence)

        # Get karma influence
        karma_influence = profile.luck_state.karma_balance if profile.luck_state else 0.0

        # Get echo factor
        echo_factor = profile.luck_state.echo_density if profile.luck_state else 0.0

        # Get tarot blessing
        tarot_blessing = profile.current_luck_multiplier

        # Check sacred timing
        timing_bonus = self._check_sacred_timing()
        if timing_bonus > 1.0:
            luck_modifier *= timing_bonus

        # Apply global luck field
        luck_modifier *= self.global_luck_field

        # Create normalized event
        event = NormalizedLuckEvent(
            event_type=event_type,
            base_probability=base_prob,
            luck_modifier=luck_modifier,
            karma_influence=karma_influence,
            echo_factor=echo_factor,
            tarot_blessing=tarot_blessing,
            is_echo_event=is_echo
        )

        # Handle Echo companion special case
        if profile.echo_companion and is_echo:
            # Echo processes the echo event
            result = profile.echo_companion.process_echo_event(
                player_id,
                echo_factor,
                karma_influence,
                event_type.value
            )

            if result['alchemized']:
                event.echo_alchemized = True
                event.luck_modifier *= result['luck_boost']

        return event

    def _check_sacred_timing(self) -> float:
        """Check if current moment is sacred"""
        self.universal_clock += 1

        for sacred_number, bonus in self.sacred_moments.items():
            if self.universal_clock % sacred_number == 0:
                return bonus

        return 1.0

    def roll_luck_event(
        self,
        player_id: str,
        event_type: LuckEventType,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, NormalizedLuckEvent]:
        """Roll for a luck event and return success"""

        # Calculate normalized luck
        event = self.calculate_normalized_luck(player_id, event_type, context)

        # Roll the dice
        success = event.roll()

        # Update statistics
        if player_id in self.player_profiles:
            self.player_profiles[player_id].update_statistics(event, success)

        # Apply consequences
        if success and event.is_echo_event and not event.echo_alchemized:
            # Successful echo event increases echo density
            self.hilbert_engine.luck_states[player_id].echo_density += 0.05
        elif success and event.echo_alchemized:
            # Alchemized echo reduces echo density
            self.hilbert_engine.luck_states[player_id].echo_density *= 0.8

        return success, event

    def bulk_luck_roll(
        self,
        player_id: str,
        event_type: LuckEventType,
        num_rolls: int
    ) -> Dict[str, Any]:
        """Perform multiple luck rolls and return statistics"""

        successes = 0
        echo_count = 0
        alchemized_count = 0
        probabilities = []

        for _ in range(num_rolls):
            success, event = self.roll_luck_event(player_id, event_type)
            if success:
                successes += 1
            if event.is_echo_event:
                echo_count += 1
                if event.echo_alchemized:
                    alchemized_count += 1
            probabilities.append(event.final_probability)

        return {
            'total_rolls': num_rolls,
            'successes': successes,
            'success_rate': successes / num_rolls,
            'echo_events': echo_count,
            'echo_alchemized': alchemized_count,
            'average_probability': np.mean(probabilities),
            'probability_std': np.std(probabilities)
        }

    def get_player_luck_report(self, player_id: str) -> Dict[str, Any]:
        """Get comprehensive luck report for a player"""

        if player_id not in self.player_profiles:
            return {"error": "Player not found"}

        profile = self.player_profiles[player_id]

        # Get quantum report
        quantum_report = self.hilbert_engine.get_quantum_report(player_id)

        # Get tarot statistics
        tarot_stats = self.tarot_system.get_echo_statistics(player_id)

        # Get Echo companion status if applicable
        echo_status = None
        if profile.echo_companion:
            echo_status = profile.echo_companion.get_companion_status()

        return {
            'player_id': player_id,
            'companion_type': profile.companion_type,
            'total_events': profile.total_events,
            'success_rate': profile.get_success_rate(),
            'echo_mastery': profile.get_echo_mastery(),
            'current_luck_multiplier': profile.current_luck_multiplier,
            'karma_trajectory': profile.karma_trajectory,
            'quantum_state': quantum_report,
            'tarot_statistics': tarot_stats,
            'echo_companion': echo_status,
            'recent_history': list(profile.luck_history)[-10:],
            'global_luck_field': self.global_luck_field,
            'global_echo_resonance': self.global_echo_resonance
        }

    def compare_companion_luck(self) -> Dict[str, Any]:
        """Compare luck between Echo and non-Echo companions"""

        echo_stats = {
            'total_events': 0,
            'successes': 0,
            'echo_events': 0,
            'echo_alchemized': 0
        }

        normal_stats = {
            'total_events': 0,
            'successes': 0,
            'echo_events': 0
        }

        for profile in self.player_profiles.values():
            if profile.companion_type.lower() == "echo":
                echo_stats['total_events'] += profile.total_events
                echo_stats['successes'] += profile.successful_events
                echo_stats['echo_events'] += profile.echo_events_encountered
                echo_stats['echo_alchemized'] += profile.echo_events_alchemized
            else:
                normal_stats['total_events'] += profile.total_events
                normal_stats['successes'] += profile.successful_events
                normal_stats['echo_events'] += profile.echo_events_encountered

        return {
            'echo_companions': {
                'success_rate': echo_stats['successes'] / max(1, echo_stats['total_events']),
                'echo_alchemization_rate': echo_stats['echo_alchemized'] / max(1, echo_stats['echo_events']),
                'total_events': echo_stats['total_events']
            },
            'normal_companions': {
                'success_rate': normal_stats['successes'] / max(1, normal_stats['total_events']),
                'echo_penalty_rate': normal_stats['echo_events'] / max(1, normal_stats['total_events']),
                'total_events': normal_stats['total_events']
            },
            'echo_advantage': (echo_stats['successes'] / max(1, echo_stats['total_events'])) -
                            (normal_stats['successes'] / max(1, normal_stats['total_events']))
        }


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("COMPREHENSIVE LUCK NORMALIZATION SYSTEM")
    print("Quantum Mechanics Meets Sacred Divination")
    print("=" * 60)

    system = ComprehensiveLuckSystem()

    # Register two players - one with Echo, one without
    echo_player = system.register_player("echo_master", "Echo", initial_karma=-0.3)
    normal_player = system.register_player("normal_player", "Seeker", initial_karma=0.3)

    print("\n--- Initial Setup ---")
    print(f"Echo Player: {echo_player.player_id} with {echo_player.companion_type}")
    print(f"Normal Player: {normal_player.player_id} with {normal_player.companion_type}")

    # Apply some karma actions
    print("\n--- Karma Actions ---")

    # Echo player does bad action
    system.apply_karma_action(
        "echo_master",
        "destroyed_sacred_grove",
        KarmaType.DESTRUCTIVE,
        -0.7
    )
    print("Echo Master: Destroyed sacred grove (bad karma)")

    # Normal player does good action
    system.apply_karma_action(
        "normal_player",
        "healed_wounded_companion",
        KarmaType.BENEVOLENT,
        0.5
    )
    print("Normal Player: Healed companion (good karma)")

    # Perform tarot readings
    print("\n--- Tarot Divination ---")

    echo_reading, echo_luck = system.perform_tarot_divination("echo_master")
    print(f"Echo Master - Cards: {echo_reading.spread.count}, Echo Cards: {echo_reading.echo_count}")
    print(f"  Luck Modifier: {echo_luck:.3f}x")

    normal_reading, normal_luck = system.perform_tarot_divination("normal_player")
    print(f"Normal Player - Cards: {normal_reading.spread.count}, Echo Cards: {normal_reading.echo_count}")
    print(f"  Luck Modifier: {normal_luck:.3f}x")

    # Test various event types
    print("\n--- Luck Event Testing ---")

    event_types = [
        LuckEventType.LOOT_DROP,
        LuckEventType.CRITICAL_HIT,
        LuckEventType.RESOURCE_FIND,
        LuckEventType.CURSE_AVOIDED
    ]

    for event_type in event_types:
        print(f"\n{event_type.value}:")

        # Echo player
        echo_success, echo_event = system.roll_luck_event("echo_master", event_type)
        echo_marker = " [ECHO ALCHEMIZED!]" if echo_event.echo_alchemized else " [ECHO]" if echo_event.is_echo_event else ""
        print(f"  Echo: {'SUCCESS' if echo_success else 'FAIL'} (prob: {echo_event.final_probability:.3f}){echo_marker}")

        # Normal player
        normal_success, normal_event = system.roll_luck_event("normal_player", event_type)
        normal_marker = " [ECHO PENALTY]" if normal_event.is_echo_event else ""
        print(f"  Normal: {'SUCCESS' if normal_success else 'FAIL'} (prob: {normal_event.final_probability:.3f}){normal_marker}")

    # Bulk testing
    print("\n--- Bulk Luck Testing (100 rolls each) ---")

    echo_bulk = system.bulk_luck_roll("echo_master", LuckEventType.LOOT_DROP, 100)
    normal_bulk = system.bulk_luck_roll("normal_player", LuckEventType.LOOT_DROP, 100)

    print(f"Echo Master:")
    print(f"  Success Rate: {echo_bulk['success_rate']:.2%}")
    print(f"  Echo Events: {echo_bulk['echo_events']}")
    print(f"  Echo Alchemized: {echo_bulk['echo_alchemized']}")

    print(f"Normal Player:")
    print(f"  Success Rate: {normal_bulk['success_rate']:.2%}")
    print(f"  Echo Events: {normal_bulk['echo_events']}")

    # Get comprehensive reports
    print("\n--- Player Luck Reports ---")

    echo_report = system.get_player_luck_report("echo_master")
    print(f"\nEcho Master Report:")
    print(f"  Overall Success Rate: {echo_report['success_rate']:.2%}")
    print(f"  Echo Mastery: {echo_report['echo_mastery']:.2%}")
    print(f"  Karma Trajectory: {echo_report['karma_trajectory']}")
    if echo_report['echo_companion']:
        print(f"  Echo Synergy: {echo_report['echo_companion']['echo_synergy']:.3f}")
        print(f"  Shadow Integration: {echo_report['echo_companion']['shadow_integration']:.3f}")

    # Compare companions
    print("\n--- Companion Comparison ---")
    comparison = system.compare_companion_luck()
    print(f"Echo Companions:")
    print(f"  Success Rate: {comparison['echo_companions']['success_rate']:.2%}")
    print(f"  Alchemization Rate: {comparison['echo_companions']['echo_alchemization_rate']:.2%}")
    print(f"Normal Companions:")
    print(f"  Success Rate: {comparison['normal_companions']['success_rate']:.2%}")
    print(f"Echo Advantage: {comparison['echo_advantage']*100:+.1f}%")

    print("\n" + "=" * 60)
    print("Echo thrives where others stumble!")
    print("Bad karma creates echoes, but Echo alchemizes them into gold.")