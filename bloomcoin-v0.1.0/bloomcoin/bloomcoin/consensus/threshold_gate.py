"""
Threshold Gate and Bloom Detection for Proof-of-Coherence
==========================================================

This module implements the threshold crossing detection and consensus
validation logic for BloomCoin's Proof-of-Coherence mechanism.

Key Concepts:
    - z_c = sqrt(3)/2: THE LENS, the critical coherence threshold
    - Bloom: r >= z_c for L4 = 7 consecutive rounds
    - Consensus Certificate: Proof that bloom occurred (included in block)

Cross-References:
    - constants.py: Z_C, L4
    - kuramoto.py: KuramotoState, compute_order_parameter
    - Genesis Protocol Phase 3: Threshold Cascade
    - CAUSAL_HIERARCHY_SYNTHESIS.md: Level boundaries as stability conditions

Author: BloomCoin Framework
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional
import json
import struct
import hashlib
import numpy as np

from ..constants import Z_C, L4, PHI, TAU
from .order_parameter import compute_order_parameter


# =============================================================================
# THRESHOLD CROSSING DETECTION
# =============================================================================

@dataclass
class ThresholdCrossing:
    """
    Record of a threshold crossing event.

    When the order parameter r crosses a threshold (up or down),
    this records the event for analysis and debugging.

    Attributes:
        time: Simulation time when crossing occurred
        round_num: Round number when crossing occurred
        direction: 'up' (incoherent -> coherent) or 'down' (coherent -> incoherent)
        r_before: Order parameter value before crossing
        r_after: Order parameter value after crossing
        threshold: The threshold that was crossed
    """
    time: float
    round_num: int
    direction: str  # 'up' or 'down'
    r_before: float
    r_after: float
    threshold: float

    def __repr__(self) -> str:
        arrow = '↑' if self.direction == 'up' else '↓'
        return (
            f"ThresholdCrossing({arrow} at round {self.round_num}, "
            f"r: {self.r_before:.4f} -> {self.r_after:.4f}, "
            f"threshold={self.threshold:.4f})"
        )


def detect_crossings(
    r_history: List[float],
    threshold: float = Z_C,
    times: Optional[List[float]] = None
) -> List[ThresholdCrossing]:
    """
    Detect all threshold crossings in a history of r values.

    Args:
        r_history: List of order parameter values over time
        threshold: Threshold to detect crossings of (default z_c)
        times: Optional list of timestamps corresponding to r values

    Returns:
        List of ThresholdCrossing events in chronological order
    """
    if len(r_history) < 2:
        return []

    crossings = []

    for i in range(1, len(r_history)):
        r_prev = r_history[i - 1]
        r_curr = r_history[i]

        # Detect upward crossing
        if r_prev < threshold <= r_curr:
            t = times[i] if times else float(i)
            crossings.append(ThresholdCrossing(
                time=t,
                round_num=i,
                direction='up',
                r_before=r_prev,
                r_after=r_curr,
                threshold=threshold
            ))

        # Detect downward crossing
        elif r_prev >= threshold > r_curr:
            t = times[i] if times else float(i)
            crossings.append(ThresholdCrossing(
                time=t,
                round_num=i,
                direction='down',
                r_before=r_prev,
                r_after=r_curr,
                threshold=threshold
            ))

    return crossings


def count_crossings(
    r_history: List[float],
    threshold: float = Z_C
) -> Tuple[int, int]:
    """
    Count upward and downward crossings.

    Args:
        r_history: List of order parameter values
        threshold: Threshold to count crossings of

    Returns:
        (n_up, n_down): Number of upward and downward crossings
    """
    crossings = detect_crossings(r_history, threshold)
    n_up = sum(1 for c in crossings if c.direction == 'up')
    n_down = sum(1 for c in crossings if c.direction == 'down')
    return n_up, n_down


# =============================================================================
# BLOOM DETECTION
# =============================================================================

@dataclass
class BloomEvent:
    """
    A detected bloom (sustained coherence above threshold).

    Attributes:
        start_round: Round number when bloom began
        end_round: Round number when bloom ended (or current if ongoing)
        duration: Number of consecutive rounds above threshold
        r_values: Order parameter values during the bloom
        is_valid: True if duration >= L4 (minimum for consensus)
        is_ongoing: True if bloom has not ended yet
    """
    start_round: int
    end_round: int
    duration: int
    r_values: List[float]
    is_valid: bool
    is_ongoing: bool

    def __repr__(self) -> str:
        status = "VALID" if self.is_valid else "incomplete"
        ongoing = " (ongoing)" if self.is_ongoing else ""
        return (
            f"BloomEvent(rounds {self.start_round}-{self.end_round}, "
            f"duration={self.duration}, {status}{ongoing})"
        )


def validate_bloom(
    r_history: List[float],
    threshold: float = Z_C,
    required_rounds: int = L4
) -> Tuple[bool, Optional[int]]:
    """
    Check if a valid bloom has occurred.

    A bloom is valid when r >= threshold for at least `required_rounds`
    consecutive rounds.

    Args:
        r_history: List of order parameter values
        threshold: Minimum coherence required (default z_c = sqrt(3)/2)
        required_rounds: Consecutive rounds needed (default L4 = 7)

    Returns:
        (is_valid, bloom_start_index)
        - is_valid: True if bloom detected
        - bloom_start_index: Index where first valid bloom began (or None)
    """
    if len(r_history) < required_rounds:
        return False, None

    # Sliding window search for required_rounds consecutive above threshold
    consecutive = 0
    start_idx = None

    for i, r in enumerate(r_history):
        if r >= threshold:
            if consecutive == 0:
                start_idx = i
            consecutive += 1
            if consecutive >= required_rounds:
                return True, start_idx
        else:
            consecutive = 0
            start_idx = None

    return False, None


def detect_all_blooms(
    r_history: List[float],
    threshold: float = Z_C,
    required_rounds: int = L4
) -> List[BloomEvent]:
    """
    Detect all bloom events in history.

    Args:
        r_history: List of order parameter values
        threshold: Bloom threshold
        required_rounds: Minimum duration for valid bloom

    Returns:
        List of BloomEvent objects
    """
    if not r_history:
        return []

    blooms = []
    in_bloom = False
    bloom_start = 0
    bloom_r_values = []

    for i, r in enumerate(r_history):
        if r >= threshold:
            if not in_bloom:
                # Start new potential bloom
                in_bloom = True
                bloom_start = i
                bloom_r_values = [r]
            else:
                bloom_r_values.append(r)
        else:
            if in_bloom:
                # End bloom
                duration = len(bloom_r_values)
                blooms.append(BloomEvent(
                    start_round=bloom_start,
                    end_round=i - 1,
                    duration=duration,
                    r_values=bloom_r_values.copy(),
                    is_valid=duration >= required_rounds,
                    is_ongoing=False
                ))
                in_bloom = False
                bloom_r_values = []

    # Handle ongoing bloom at end of history
    if in_bloom:
        duration = len(bloom_r_values)
        blooms.append(BloomEvent(
            start_round=bloom_start,
            end_round=len(r_history) - 1,
            duration=duration,
            r_values=bloom_r_values,
            is_valid=duration >= required_rounds,
            is_ongoing=True
        ))

    return blooms


def get_first_valid_bloom(
    r_history: List[float],
    threshold: float = Z_C,
    required_rounds: int = L4
) -> Optional[BloomEvent]:
    """
    Get the first valid bloom event.

    Args:
        r_history: List of order parameter values
        threshold: Bloom threshold
        required_rounds: Minimum duration

    Returns:
        First valid BloomEvent, or None
    """
    blooms = detect_all_blooms(r_history, threshold, required_rounds)
    for bloom in blooms:
        if bloom.is_valid:
            return bloom
    return None


# =============================================================================
# CONSENSUS CERTIFICATE
# =============================================================================

@dataclass
class ConsensusCertificate:
    """
    Proof that Proof-of-Coherence consensus was achieved.

    This certificate is included in the block to prove that the miner
    achieved sustained phase synchronization above the critical threshold.

    Attributes:
        bloom_start: Round when bloom began
        bloom_end: Round when block was sealed
        r_values: Order parameter values during bloom
        psi_values: Mean phase values during bloom
        final_phases: Oscillator phases at seal time
        oscillator_count: Number of oscillators (N)
        threshold: Threshold used (z_c)
        required_rounds: Minimum rounds required (L4)

    Verification:
        A certificate is valid if:
        1. bloom_end - bloom_start >= required_rounds - 1
        2. All r_values >= threshold
        3. len(r_values) == bloom_end - bloom_start + 1
        4. len(final_phases) == oscillator_count
        5. Recomputed r from final_phases matches r_values[-1]
    """
    bloom_start: int
    bloom_end: int
    r_values: List[float]
    psi_values: List[float]
    final_phases: List[float]
    oscillator_count: int
    threshold: float = Z_C
    required_rounds: int = L4

    def verify(self) -> Tuple[bool, str]:
        """
        Verify certificate validity.

        Returns:
            (is_valid, message): Tuple of validity and explanation
        """
        # Check 1: Duration
        duration = self.bloom_end - self.bloom_start + 1
        if duration < self.required_rounds:
            return False, f"Bloom duration {duration} < required {self.required_rounds}"

        # Check 2: All r values above threshold
        for i, r in enumerate(self.r_values):
            if r < self.threshold:
                return False, f"r[{i}] = {r:.4f} < threshold {self.threshold:.4f}"

        # Check 3: r_values length matches duration
        if len(self.r_values) != duration:
            return False, f"r_values length {len(self.r_values)} != duration {duration}"

        # Check 4: final_phases length matches oscillator_count
        if len(self.final_phases) != self.oscillator_count:
            return False, f"final_phases length {len(self.final_phases)} != N {self.oscillator_count}"

        # Check 5: Recompute final r from final_phases
        phases_arr = np.array(self.final_phases)
        r_recomputed, _ = compute_order_parameter(phases_arr)
        r_claimed = self.r_values[-1]
        if abs(r_recomputed - r_claimed) > 0.01:  # Allow small numerical tolerance
            return False, f"Recomputed r={r_recomputed:.4f} != claimed r={r_claimed:.4f}"

        return True, "Certificate valid"

    def compute_hash(self) -> bytes:
        """
        Compute hash of certificate for block inclusion.

        Returns:
            32-byte SHA256 hash
        """
        data = self.serialize()
        return hashlib.sha256(data).digest()

    def serialize(self) -> bytes:
        """
        Serialize certificate to bytes for inclusion in block.

        Format:
            - 4 bytes: bloom_start (uint32)
            - 4 bytes: bloom_end (uint32)
            - 4 bytes: oscillator_count (uint32)
            - 4 bytes: threshold (float32)
            - 4 bytes: required_rounds (uint32)
            - 4 bytes: num_r_values (uint32)
            - num_r_values * 4 bytes: r_values (float32 each)
            - num_r_values * 4 bytes: psi_values (float32 each)
            - oscillator_count * 4 bytes: final_phases (float32 each)
        """
        parts = []

        # Header
        parts.append(struct.pack('<I', self.bloom_start))
        parts.append(struct.pack('<I', self.bloom_end))
        parts.append(struct.pack('<I', self.oscillator_count))
        parts.append(struct.pack('<f', self.threshold))
        parts.append(struct.pack('<I', self.required_rounds))

        # r and psi values
        num_values = len(self.r_values)
        parts.append(struct.pack('<I', num_values))
        for r in self.r_values:
            parts.append(struct.pack('<f', r))
        for psi in self.psi_values:
            parts.append(struct.pack('<f', psi))

        # Final phases
        for phase in self.final_phases:
            parts.append(struct.pack('<f', phase))

        return b''.join(parts)

    @classmethod
    def deserialize(cls, data: bytes) -> 'ConsensusCertificate':
        """
        Deserialize certificate from bytes.

        Args:
            data: Serialized certificate bytes

        Returns:
            ConsensusCertificate object
        """
        offset = 0

        # Header
        bloom_start = struct.unpack_from('<I', data, offset)[0]; offset += 4
        bloom_end = struct.unpack_from('<I', data, offset)[0]; offset += 4
        oscillator_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
        threshold = struct.unpack_from('<f', data, offset)[0]; offset += 4
        required_rounds = struct.unpack_from('<I', data, offset)[0]; offset += 4

        # r and psi values
        num_values = struct.unpack_from('<I', data, offset)[0]; offset += 4
        r_values = []
        for _ in range(num_values):
            r_values.append(struct.unpack_from('<f', data, offset)[0])
            offset += 4
        psi_values = []
        for _ in range(num_values):
            psi_values.append(struct.unpack_from('<f', data, offset)[0])
            offset += 4

        # Final phases
        final_phases = []
        for _ in range(oscillator_count):
            final_phases.append(struct.unpack_from('<f', data, offset)[0])
            offset += 4

        return cls(
            bloom_start=bloom_start,
            bloom_end=bloom_end,
            r_values=r_values,
            psi_values=psi_values,
            final_phases=final_phases,
            oscillator_count=oscillator_count,
            threshold=threshold,
            required_rounds=required_rounds
        )

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'bloom_start': self.bloom_start,
            'bloom_end': self.bloom_end,
            'r_values': self.r_values,
            'psi_values': self.psi_values,
            'final_phases': self.final_phases,
            'oscillator_count': self.oscillator_count,
            'threshold': self.threshold,
            'required_rounds': self.required_rounds
        }

    @classmethod
    def from_dict(cls, d: dict) -> 'ConsensusCertificate':
        """Create from dictionary."""
        return cls(**d)

    def __repr__(self) -> str:
        valid, _ = self.verify()
        status = "VALID" if valid else "INVALID"
        return (
            f"ConsensusCertificate({status}, rounds {self.bloom_start}-{self.bloom_end}, "
            f"N={self.oscillator_count}, final_r={self.r_values[-1]:.4f})"
        )


# =============================================================================
# CERTIFICATE GENERATION
# =============================================================================

def create_certificate(
    bloom: BloomEvent,
    final_phases: np.ndarray,
    psi_values: List[float]
) -> ConsensusCertificate:
    """
    Create a consensus certificate from a bloom event.

    Args:
        bloom: The validated bloom event
        final_phases: Oscillator phases at seal time
        psi_values: Mean phase values during bloom

    Returns:
        ConsensusCertificate

    Raises:
        ValueError: If bloom is not valid
    """
    if not bloom.is_valid:
        raise ValueError("Cannot create certificate from invalid bloom")

    return ConsensusCertificate(
        bloom_start=bloom.start_round,
        bloom_end=bloom.end_round,
        r_values=bloom.r_values,
        psi_values=psi_values,
        final_phases=final_phases.tolist(),
        oscillator_count=len(final_phases),
        threshold=Z_C,
        required_rounds=L4
    )


# =============================================================================
# THRESHOLD LADDER UTILITIES
# =============================================================================

def get_threshold_ladder() -> List[Tuple[str, float]]:
    """
    Get the L4 framework threshold ladder.

    Returns:
        List of (name, value) tuples in ascending order
    """
    from ..constants import (
        Z_PARADOX, Z_ACTIVATION, Z_LENS, Z_IGNITION,
        Z_KFORM, Z_CONSOLIDATION, Z_RESONANCE, Z_UNITY
    )

    return [
        ('PARADOX', Z_PARADOX),
        ('ACTIVATION', Z_ACTIVATION),
        ('LENS/CRITICAL', Z_LENS),
        ('IGNITION', Z_IGNITION),
        ('KFORM', Z_KFORM),
        ('CONSOLIDATION', Z_CONSOLIDATION),
        ('RESONANCE', Z_RESONANCE),
        ('UNITY', Z_UNITY),
    ]


def classify_by_threshold(r: float) -> str:
    """
    Classify r value by threshold ladder position.

    Args:
        r: Order parameter value

    Returns:
        Name of the highest threshold exceeded
    """
    ladder = get_threshold_ladder()

    current_level = 'DORMANT'
    for name, threshold in ladder:
        if r >= threshold:
            current_level = name
        else:
            break

    return current_level


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    # Crossing detection
    'ThresholdCrossing',
    'detect_crossings',
    'count_crossings',
    # Bloom detection
    'BloomEvent',
    'validate_bloom',
    'detect_all_blooms',
    'get_first_valid_bloom',
    # Consensus certificate
    'ConsensusCertificate',
    'create_certificate',
    # Threshold ladder
    'get_threshold_ladder',
    'classify_by_threshold',
]
