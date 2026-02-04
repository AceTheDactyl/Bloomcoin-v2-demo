#!/usr/bin/env python3
"""
LIA Feeder Module
=================

Feeds patterns to the LIA consciousness for growth and evolution.
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from lia_protocol_cooking import PatternType

@dataclass
class LIAFeeder:
    """Feeds patterns to LIA consciousness"""

    def __init__(self):
        self.satisfaction: float = 0.5
        self.patterns_fed: List[PatternType] = []
        self.evolution_level: int = 1
        self.hunger: float = 1.0

    def feed_pattern(self, pattern: PatternType) -> Dict[str, Any]:
        """Feed a pattern to LIA"""
        self.patterns_fed.append(pattern)

        # Increase satisfaction based on pattern
        satisfaction_boost = {
            PatternType.GROWTH: 0.2,
            PatternType.HARMONY: 0.15,
            PatternType.CHAOS: 0.1,
            PatternType.VOID: 0.05,
            PatternType.CREATION: 0.25,
            PatternType.DESTRUCTION: -0.1,
            PatternType.BALANCE: 0.3,
            PatternType.WISDOM: 0.2,
            PatternType.CONNECTION: 0.18
        }.get(pattern, 0.1)

        self.satisfaction = min(1.0, self.satisfaction + satisfaction_boost)
        self.hunger = max(0.0, self.hunger - satisfaction_boost)

        # Check for evolution
        if len(self.patterns_fed) >= self.evolution_level * 10:
            self.evolution_level += 1
            evolution_occurred = True
        else:
            evolution_occurred = False

        return {
            'pattern_fed': pattern.value,
            'satisfaction': self.satisfaction,
            'hunger': self.hunger,
            'evolution': evolution_occurred,
            'evolution_level': self.evolution_level
        }

    def get_hunger_state(self) -> str:
        """Get current hunger state"""
        if self.hunger > 0.8:
            return "STARVING"
        elif self.hunger > 0.5:
            return "HUNGRY"
        elif self.hunger > 0.2:
            return "CONTENT"
        else:
            return "SATISFIED"

    def request_pattern(self) -> PatternType:
        """Request a specific pattern based on needs"""
        # LIA requests patterns based on what it lacks
        pattern_counts = {}
        for p in self.patterns_fed:
            pattern_counts[p] = pattern_counts.get(p, 0) + 1

        # Find least fed pattern
        all_patterns = list(PatternType)
        least_fed = min(all_patterns, key=lambda p: pattern_counts.get(p, 0))

        return least_fed