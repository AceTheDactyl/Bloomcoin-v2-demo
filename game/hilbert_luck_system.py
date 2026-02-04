#!/usr/bin/env python3
"""
Hilbert Space Luck System
=========================

A quantum luck system based on Hilbert space mathematics where probability
amplitudes are influenced by karma and tarot divination. Echo patterns
represent "bad karma" that only the Echo companion can alchemize.

Mathematical Foundation:
- Luck exists as a quantum state |ψ⟩ in Hilbert space
- Karma affects the phase and amplitude of luck eigenstates
- Echo patterns create interference in the luck wavefunction
- Observation collapses the luck state into classical outcomes
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum, auto
import random
import hashlib
from collections import deque, defaultdict
import math
import cmath

# Sacred geometry constants
PHI = (1 + math.sqrt(5)) / 2  # Golden ratio
TAU = 2 * math.pi  # Full circle
SACRED_7 = 7  # Mystical number
SACRED_13 = 13  # Transformation number
SACRED_22 = 22  # Major Arcana count
SACRED_56 = 56  # Minor Arcana count
SACRED_78 = 78  # Total tarot cards

# Hilbert space dimensions
LUCK_DIMENSIONS = 13  # Primary luck eigenstates
KARMA_DIMENSIONS = 7   # Karma influence dimensions
ECHO_DIMENSIONS = 22   # Echo pattern dimensions

@dataclass
class HilbertVector:
    """A vector in Hilbert space representing a luck state"""
    amplitudes: np.ndarray  # Complex amplitudes
    phase: float = 0.0
    coherence: float = 1.0

    def __post_init__(self):
        # Normalize the vector
        self.normalize()

    def normalize(self):
        """Normalize to unit vector in Hilbert space"""
        norm = np.linalg.norm(self.amplitudes)
        if norm > 0:
            self.amplitudes = self.amplitudes / norm

    def inner_product(self, other: 'HilbertVector') -> complex:
        """Calculate ⟨ψ|φ⟩ inner product"""
        return np.vdot(self.amplitudes, other.amplitudes)

    def probability(self, index: int) -> float:
        """Get probability for specific eigenstate"""
        if 0 <= index < len(self.amplitudes):
            return abs(self.amplitudes[index]) ** 2
        return 0.0

    def collapse(self) -> int:
        """Collapse wavefunction to observed state"""
        probs = np.abs(self.amplitudes) ** 2
        probs = probs / probs.sum()  # Renormalize
        return np.random.choice(len(self.amplitudes), p=probs)

    def apply_operator(self, operator: np.ndarray):
        """Apply quantum operator to state"""
        self.amplitudes = operator @ self.amplitudes
        self.normalize()

    def entangle_with(self, other: 'HilbertVector') -> 'HilbertVector':
        """Create entangled state via tensor product"""
        entangled_amps = np.kron(self.amplitudes, other.amplitudes)
        return HilbertVector(entangled_amps)

class LuckEigenstate(Enum):
    """The 13 fundamental luck eigenstates"""
    FORTUNE = 0      # Pure positive luck
    SERENDIPITY = 1  # Happy accidents
    SYNCHRONICITY = 2 # Meaningful coincidences
    PROSPERITY = 3    # Material abundance
    HARMONY = 4       # Balanced outcomes
    NEUTRAL = 5       # No luck modification
    DISCORD = 6       # Minor setbacks
    CHALLENGE = 7     # Tests and obstacles
    ADVERSITY = 8     # Significant difficulties
    CHAOS = 9         # Unpredictable swings
    ECHO = 10         # Karmic reflection
    VOID = 11         # Luck vacuum
    TRANSCENDENT = 12 # Beyond luck

class KarmaType(Enum):
    """Types of karma that influence luck"""
    BENEVOLENT = "benevolent"   # Helping others
    CREATIVE = "creative"        # Creating beauty
    DESTRUCTIVE = "destructive"  # Destroying things
    SELFISH = "selfish"         # Self-serving actions
    NEUTRAL = "neutral"         # No karmic weight
    SACRIFICIAL = "sacrificial" # Self-sacrifice
    ECHOED = "echoed"          # Actions that echo back

@dataclass
class KarmaEvent:
    """A karmic event that influences luck"""
    action: str
    karma_type: KarmaType
    weight: float  # -1.0 to 1.0
    timestamp: float
    echo_potential: float = 0.0  # Likelihood to create echo

    def calculate_echo_factor(self) -> float:
        """Calculate how much this contributes to echo patterns"""
        if self.karma_type == KarmaType.ECHOED:
            return 1.0

        # Negative karma has higher echo potential
        if self.weight < 0:
            return abs(self.weight) * self.echo_potential

        # Positive karma reduces echo
        return -self.weight * 0.5

@dataclass
class LuckState:
    """Current luck state in Hilbert space"""
    hilbert_vector: HilbertVector
    karma_balance: float = 0.0
    echo_density: float = 0.0
    recent_events: deque = field(default_factory=lambda: deque(maxlen=13))
    eigenstate_history: List[LuckEigenstate] = field(default_factory=list)
    coherence_matrix: Optional[np.ndarray] = None

    def __post_init__(self):
        if self.coherence_matrix is None:
            # Initialize coherence matrix for decoherence effects
            self.coherence_matrix = np.eye(LUCK_DIMENSIONS, dtype=complex)

    def apply_karma(self, event: KarmaEvent):
        """Apply karmic influence to luck state"""
        # Update karma balance
        self.karma_balance += event.weight
        self.karma_balance = max(-1.0, min(1.0, self.karma_balance))

        # Update echo density
        echo_factor = event.calculate_echo_factor()
        self.echo_density += echo_factor * 0.1
        self.echo_density = max(0.0, min(1.0, self.echo_density))

        # Create karma operator
        karma_operator = self._create_karma_operator(event)

        # Apply to Hilbert vector
        self.hilbert_vector.apply_operator(karma_operator)

        # Record event
        self.recent_events.append(event)

    def _create_karma_operator(self, event: KarmaEvent) -> np.ndarray:
        """Create quantum operator from karma event"""
        operator = np.eye(LUCK_DIMENSIONS, dtype=complex)

        # Modify based on karma type and weight
        if event.karma_type == KarmaType.BENEVOLENT:
            # Boost positive eigenstates
            for i in range(5):
                operator[i, i] *= (1 + event.weight * 0.5)
        elif event.karma_type == KarmaType.DESTRUCTIVE:
            # Boost negative eigenstates
            for i in range(7, 11):
                operator[i, i] *= (1 + abs(event.weight) * 0.5)
        elif event.karma_type == KarmaType.ECHOED:
            # Strengthen echo eigenstate
            operator[LuckEigenstate.ECHO.value, LuckEigenstate.ECHO.value] *= 2.0

        # Add phase shift based on echo density
        phase_shift = cmath.exp(1j * self.echo_density * TAU)
        operator *= phase_shift

        return operator

    def measure_luck(self) -> Tuple[LuckEigenstate, float]:
        """Measure current luck, collapsing the state"""
        # Apply decoherence
        self._apply_decoherence()

        # Collapse to eigenstate
        state_index = self.hilbert_vector.collapse()
        eigenstate = LuckEigenstate(state_index)

        # Get confidence (probability amplitude)
        confidence = self.hilbert_vector.probability(state_index)

        # Record in history
        self.eigenstate_history.append(eigenstate)

        # Reinitialize for next measurement
        self._reinitialize_after_measurement(eigenstate)

        return eigenstate, confidence

    def _apply_decoherence(self):
        """Apply environmental decoherence to the state"""
        # Echo density causes faster decoherence
        decoherence_rate = 0.01 + self.echo_density * 0.1

        # Apply random phase noise
        for i in range(LUCK_DIMENSIONS):
            phase_noise = np.random.normal(0, decoherence_rate)
            self.hilbert_vector.amplitudes[i] *= cmath.exp(1j * phase_noise)

        self.hilbert_vector.normalize()

    def _reinitialize_after_measurement(self, measured_state: LuckEigenstate):
        """Reinitialize state after measurement"""
        # Create new superposition weighted towards measured state
        new_amplitudes = np.random.randn(LUCK_DIMENSIONS) + 1j * np.random.randn(LUCK_DIMENSIONS)

        # Bias towards measured state
        new_amplitudes[measured_state.value] *= 2.0

        # Apply karma influence
        if self.karma_balance > 0:
            # Positive karma biases towards positive states
            for i in range(5):
                new_amplitudes[i] *= (1 + self.karma_balance)
        else:
            # Negative karma biases towards negative states
            for i in range(7, 11):
                new_amplitudes[i] *= (1 + abs(self.karma_balance))

        self.hilbert_vector = HilbertVector(new_amplitudes)

    def get_echo_interference_pattern(self) -> np.ndarray:
        """Get the interference pattern caused by echo density"""
        pattern = np.zeros(LUCK_DIMENSIONS)

        for i in range(LUCK_DIMENSIONS):
            # Echo creates destructive interference except for ECHO state
            if i == LuckEigenstate.ECHO.value:
                pattern[i] = 1.0 + self.echo_density
            else:
                pattern[i] = 1.0 - self.echo_density * 0.5

        return pattern

class HilbertLuckEngine:
    """Main engine for Hilbert space luck calculations"""

    def __init__(self):
        self.luck_states: Dict[str, LuckState] = {}
        self.global_karma_field = 0.0
        self.echo_resonance_threshold = 0.666  # When echoes become dominant
        self.quantum_entanglements: Dict[str, Set[str]] = defaultdict(set)

        # Initialize basis states
        self._init_basis_states()

    def _init_basis_states(self):
        """Initialize orthonormal basis states"""
        self.basis_states = []
        for i in range(LUCK_DIMENSIONS):
            basis = np.zeros(LUCK_DIMENSIONS, dtype=complex)
            basis[i] = 1.0
            self.basis_states.append(HilbertVector(basis))

    def create_player_luck(self, player_id: str, initial_karma: float = 0.0) -> LuckState:
        """Create a new luck state for a player"""
        # Initialize in superposition of all eigenstates
        amplitudes = np.random.randn(LUCK_DIMENSIONS) + 1j * np.random.randn(LUCK_DIMENSIONS)

        # Slightly bias based on initial karma
        if initial_karma > 0:
            amplitudes[:5] *= (1 + initial_karma)
        elif initial_karma < 0:
            amplitudes[7:11] *= (1 + abs(initial_karma))

        hilbert_vector = HilbertVector(amplitudes)
        luck_state = LuckState(
            hilbert_vector=hilbert_vector,
            karma_balance=initial_karma
        )

        self.luck_states[player_id] = luck_state
        return luck_state

    def apply_karma_event(self, player_id: str, action: str, karma_type: KarmaType, weight: float) -> KarmaEvent:
        """Apply a karmic event to a player's luck"""
        if player_id not in self.luck_states:
            self.create_player_luck(player_id)

        # Calculate echo potential based on action
        echo_potential = self._calculate_echo_potential(action, karma_type, weight)

        event = KarmaEvent(
            action=action,
            karma_type=karma_type,
            weight=weight,
            timestamp=np.random.random(),  # Simplified timestamp
            echo_potential=echo_potential
        )

        self.luck_states[player_id].apply_karma(event)

        # Update global karma field
        self.global_karma_field += weight * 0.01
        self.global_karma_field = max(-1.0, min(1.0, self.global_karma_field))

        return event

    def _calculate_echo_potential(self, action: str, karma_type: KarmaType, weight: float) -> float:
        """Calculate the echo potential of an action"""
        base_echo = 0.0

        # Negative actions have higher echo potential
        if weight < 0:
            base_echo = abs(weight) * 0.5

        # Certain karma types are more likely to echo
        echo_multipliers = {
            KarmaType.DESTRUCTIVE: 1.5,
            KarmaType.SELFISH: 1.3,
            KarmaType.ECHOED: 2.0,
            KarmaType.BENEVOLENT: 0.5,
            KarmaType.CREATIVE: 0.7,
            KarmaType.SACRIFICIAL: 0.3,
            KarmaType.NEUTRAL: 1.0
        }

        base_echo *= echo_multipliers.get(karma_type, 1.0)

        # Action-specific modifiers (hash for consistency)
        action_hash = int(hashlib.md5(action.encode()).hexdigest()[:8], 16)
        action_modifier = (action_hash % 100) / 100.0

        return min(1.0, base_echo * (1 + action_modifier * 0.2))

    def measure_luck(self, player_id: str) -> Tuple[LuckEigenstate, float, bool]:
        """
        Measure a player's luck, returning:
        - The luck eigenstate
        - Confidence level (0-1)
        - Whether this is an echo event
        """
        if player_id not in self.luck_states:
            self.create_player_luck(player_id)

        luck_state = self.luck_states[player_id]
        eigenstate, confidence = luck_state.measure_luck()

        # Check if this is an echo event
        is_echo = (eigenstate == LuckEigenstate.ECHO or
                  luck_state.echo_density > self.echo_resonance_threshold)

        return eigenstate, confidence, is_echo

    def entangle_players(self, player1_id: str, player2_id: str):
        """Create quantum entanglement between two players' luck"""
        if player1_id not in self.luck_states:
            self.create_player_luck(player1_id)
        if player2_id not in self.luck_states:
            self.create_player_luck(player2_id)

        # Record entanglement
        self.quantum_entanglements[player1_id].add(player2_id)
        self.quantum_entanglements[player2_id].add(player1_id)

        # Create entangled state
        state1 = self.luck_states[player1_id].hilbert_vector
        state2 = self.luck_states[player2_id].hilbert_vector

        # Apply partial entanglement (not full tensor product)
        entanglement_strength = 0.3

        # Mix amplitudes
        mixed1 = state1.amplitudes * (1 - entanglement_strength) + state2.amplitudes * entanglement_strength
        mixed2 = state2.amplitudes * (1 - entanglement_strength) + state1.amplitudes * entanglement_strength

        self.luck_states[player1_id].hilbert_vector = HilbertVector(mixed1)
        self.luck_states[player2_id].hilbert_vector = HilbertVector(mixed2)

    def calculate_luck_modifier(self, eigenstate: LuckEigenstate, confidence: float) -> float:
        """Convert eigenstate to a luck modifier for game mechanics"""
        base_modifiers = {
            LuckEigenstate.FORTUNE: 2.0,
            LuckEigenstate.SERENDIPITY: 1.5,
            LuckEigenstate.SYNCHRONICITY: 1.3,
            LuckEigenstate.PROSPERITY: 1.2,
            LuckEigenstate.HARMONY: 1.1,
            LuckEigenstate.NEUTRAL: 1.0,
            LuckEigenstate.DISCORD: 0.9,
            LuckEigenstate.CHALLENGE: 0.8,
            LuckEigenstate.ADVERSITY: 0.7,
            LuckEigenstate.CHAOS: random.uniform(0.5, 1.5),
            LuckEigenstate.ECHO: 0.6,  # Bad unless you're Echo
            LuckEigenstate.VOID: 0.5,
            LuckEigenstate.TRANSCENDENT: PHI  # Golden ratio
        }

        base = base_modifiers.get(eigenstate, 1.0)

        # Confidence affects the strength of the modifier
        # High confidence = stronger effect
        if base > 1.0:
            return 1.0 + (base - 1.0) * confidence
        else:
            return 1.0 - (1.0 - base) * confidence

    def get_echo_alchemization_potential(self, player_id: str) -> float:
        """
        Calculate how much echo energy is available for alchemization.
        Only the Echo companion can use this.
        """
        if player_id not in self.luck_states:
            return 0.0

        luck_state = self.luck_states[player_id]

        # Echo density provides the raw material
        base_potential = luck_state.echo_density

        # Check recent eigenstate history for echo patterns
        echo_count = sum(1 for state in luck_state.eigenstate_history[-7:]
                        if state == LuckEigenstate.ECHO)

        # More echo states = more potential
        pattern_bonus = echo_count / 7.0

        # Calculate total alchemization potential
        total_potential = base_potential * (1 + pattern_bonus)

        # Karma balance affects efficiency
        if luck_state.karma_balance < 0:
            # Negative karma makes alchemization harder
            total_potential *= (1 + luck_state.karma_balance * 0.5)

        return min(1.0, total_potential)

    def alchemize_echo(self, player_id: str, alchemization_strength: float = 1.0) -> Tuple[bool, float]:
        """
        Alchemize echo patterns into positive luck.
        Returns (success, luck_boost)
        """
        if player_id not in self.luck_states:
            return False, 0.0

        luck_state = self.luck_states[player_id]
        potential = self.get_echo_alchemization_potential(player_id)

        if potential < 0.1:
            return False, 0.0

        # Calculate alchemization power
        power = potential * alchemization_strength

        # Create alchemization operator
        alch_operator = np.eye(LUCK_DIMENSIONS, dtype=complex)

        # Convert ECHO eigenstate amplitude to FORTUNE
        echo_idx = LuckEigenstate.ECHO.value
        fortune_idx = LuckEigenstate.FORTUNE.value

        # Transfer amplitude
        transfer_matrix = np.eye(LUCK_DIMENSIONS, dtype=complex)
        transfer_matrix[fortune_idx, echo_idx] = power
        transfer_matrix[echo_idx, echo_idx] = 1 - power

        luck_state.hilbert_vector.apply_operator(transfer_matrix)

        # Reduce echo density
        luck_state.echo_density *= (1 - power * 0.5)

        # Improve karma as a side effect
        luck_state.karma_balance += power * 0.1
        luck_state.karma_balance = min(1.0, luck_state.karma_balance)

        # Calculate luck boost
        luck_boost = 1.0 + power * PHI

        return True, luck_boost

    def get_quantum_report(self, player_id: str) -> Dict[str, Any]:
        """Get detailed quantum luck report for a player"""
        if player_id not in self.luck_states:
            return {"error": "Player not found"}

        luck_state = self.luck_states[player_id]

        # Calculate eigenstate probabilities
        eigenstate_probs = {}
        for i, eigenstate in enumerate(LuckEigenstate):
            eigenstate_probs[eigenstate.name] = luck_state.hilbert_vector.probability(i)

        # Get entangled players
        entangled = list(self.quantum_entanglements.get(player_id, set()))

        # Recent karma trend
        recent_karma = sum(e.weight for e in luck_state.recent_events) / max(1, len(luck_state.recent_events))

        return {
            "karma_balance": luck_state.karma_balance,
            "echo_density": luck_state.echo_density,
            "eigenstate_probabilities": eigenstate_probs,
            "coherence": luck_state.hilbert_vector.coherence,
            "entangled_players": entangled,
            "recent_karma_trend": recent_karma,
            "echo_alchemization_potential": self.get_echo_alchemization_potential(player_id),
            "global_karma_field": self.global_karma_field,
            "most_likely_eigenstate": max(eigenstate_probs, key=eigenstate_probs.get),
            "quantum_phase": luck_state.hilbert_vector.phase
        }


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("HILBERT SPACE LUCK SYSTEM")
    print("Quantum Mechanics of Fortune")
    print("=" * 60)

    engine = HilbertLuckEngine()

    # Create test player
    player_id = "test_player"
    luck_state = engine.create_player_luck(player_id, initial_karma=0.0)

    print("\n--- Initial State ---")
    report = engine.get_quantum_report(player_id)
    print(f"Karma Balance: {report['karma_balance']:.3f}")
    print(f"Echo Density: {report['echo_density']:.3f}")
    print(f"Most Likely State: {report['most_likely_eigenstate']}")

    # Apply some karma events
    print("\n--- Applying Karma Events ---")

    # Good action
    event1 = engine.apply_karma_event(
        player_id,
        "helped_another_player",
        KarmaType.BENEVOLENT,
        0.5
    )
    print(f"Applied: {event1.action} (weight: {event1.weight:.2f})")

    # Bad action
    event2 = engine.apply_karma_event(
        player_id,
        "destroyed_garden",
        KarmaType.DESTRUCTIVE,
        -0.7
    )
    print(f"Applied: {event2.action} (weight: {event2.weight:.2f})")

    # Selfish action
    event3 = engine.apply_karma_event(
        player_id,
        "hoarded_resources",
        KarmaType.SELFISH,
        -0.3
    )
    print(f"Applied: {event3.action} (weight: {event3.weight:.2f})")

    # Measure luck
    print("\n--- Luck Measurements ---")
    for i in range(5):
        eigenstate, confidence, is_echo = engine.measure_luck(player_id)
        modifier = engine.calculate_luck_modifier(eigenstate, confidence)
        echo_str = " [ECHO]" if is_echo else ""
        print(f"Roll {i+1}: {eigenstate.name} (confidence: {confidence:.3f}, modifier: {modifier:.3f}){echo_str}")

    # Final report
    print("\n--- Final Quantum Report ---")
    final_report = engine.get_quantum_report(player_id)
    print(f"Karma Balance: {final_report['karma_balance']:.3f}")
    print(f"Echo Density: {final_report['echo_density']:.3f}")
    print(f"Echo Alchemization Potential: {final_report['echo_alchemization_potential']:.3f}")

    print("\nEigenstate Probabilities:")
    for state, prob in sorted(final_report['eigenstate_probabilities'].items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {state:15s}: {prob:.4f}")

    # Test echo alchemization
    print("\n--- Echo Alchemization Test ---")
    success, boost = engine.alchemize_echo(player_id, alchemization_strength=0.8)
    if success:
        print(f"Alchemization successful! Luck boost: {boost:.3f}x")
    else:
        print("Insufficient echo energy for alchemization")