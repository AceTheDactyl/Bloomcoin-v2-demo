"""
Lucas Nonce Generator for BloomCoin
=====================================

Generates algebraically-structured nonces from Lucas traces.

Key Insight:
    tr(R^n) = L_n (Lucas number)

Instead of random nonces, we use deterministic sequences based on
Lucas numbers, providing algebraic structure to the mining process.

Properties:
    - Deterministic: Same index always gives same nonce
    - Structured: Related to Fibonacci/golden ratio
    - Bounded: Nonces are mod 2^32

Cross-References:
    - core/lucas_matrix.py: lucas_trace, lucas_nonce
    - constants.py: LUCAS_SEQUENCE, PHI, TAU

Author: BloomCoin Framework
"""

from typing import List, Iterator, Optional
import numpy as np

from ..core.lucas_matrix import lucas_trace, lucas_nonce_batch
from ..constants import LUCAS_SEQUENCE, PHI, TAU


# =============================================================================
# LUCAS NONCE GENERATOR
# =============================================================================

class LucasNonceGenerator:
    """
    Generates nonces from Lucas trace formula.

    The key insight: tr(R^n) = L_n (Lucas number)

    This provides a deterministic, algebraically-structured
    sequence instead of random nonces.

    Properties:
        - Deterministic: Same index always gives same nonce
        - Structured: Related to Fibonacci/golden ratio
        - Bounded: Nonces are mod 2^32

    Example:
        gen = LucasNonceGenerator()
        nonce = gen.next()  # First Lucas-derived nonce
        nonce = gen.get(42)  # Specific index

    The generator uses Lucas index scheduling:
        nonce(i) = tr(R^L_{i mod 24}) mod self.mod

    The mod 24 creates a cycle through the first 24 Lucas indices,
    giving varied nonce magnitudes.
    """

    def __init__(self, mod: int = 2**32, use_scheduling: bool = True):
        """
        Initialize generator.

        Args:
            mod: Modulus for nonce values (default 2^32 for 32-bit nonces)
            use_scheduling: If True, use Lucas index scheduling (L_i mod 24)
                           If False, use direct index
        """
        self.mod = mod
        self.use_scheduling = use_scheduling
        self.index = 0
        self._cache: dict = {}

    def next(self) -> int:
        """
        Generate next nonce in sequence.

        Returns:
            Next nonce value
        """
        nonce = self.get(self.index)
        self.index += 1
        return nonce

    def get(self, index: int) -> int:
        """
        Get nonce at specific index.

        Uses Lucas index scheduling (if enabled):
            nonce(i) = tr(R^L_{i mod 24}) mod self.mod

        The mod 24 creates a cycle through Lucas indices,
        giving varied nonce magnitudes.

        Args:
            index: Sequence index

        Returns:
            Nonce value at index
        """
        if index not in self._cache:
            if self.use_scheduling and index < len(LUCAS_SEQUENCE) * 100:
                # Use Lucas index scheduling
                lucas_index = LUCAS_SEQUENCE[index % len(LUCAS_SEQUENCE)]
                self._cache[index] = lucas_trace(lucas_index, self.mod)
            else:
                # Direct computation for high indices
                self._cache[index] = lucas_trace(index, self.mod)
        return self._cache[index]

    def get_batch(self, start: int, count: int) -> List[int]:
        """
        Get a batch of consecutive nonces efficiently.

        Args:
            start: Starting index
            count: Number of nonces

        Returns:
            List of nonce values
        """
        if self.use_scheduling:
            # For scheduled nonces, compute individually (different Lucas indices)
            return [self.get(start + i) for i in range(count)]
        else:
            # For direct indices, use recurrence-based batch generation
            return lucas_nonce_batch(0, start, count, self.mod).tolist()

    def reset(self):
        """Reset to beginning of sequence."""
        self.index = 0

    def skip(self, n: int):
        """
        Skip n nonces in sequence.

        Args:
            n: Number of nonces to skip
        """
        self.index += n

    def seek(self, index: int):
        """
        Set sequence to specific index.

        Args:
            index: New sequence index
        """
        self.index = index

    def peek(self) -> int:
        """
        Peek at next nonce without advancing.

        Returns:
            Next nonce value
        """
        return self.get(self.index)

    def __iter__(self) -> Iterator[int]:
        """Make generator iterable."""
        return self

    def __next__(self) -> int:
        """Python iterator protocol."""
        return self.next()

    def clear_cache(self):
        """Clear nonce cache to free memory."""
        self._cache.clear()

    @property
    def cache_size(self) -> int:
        """Number of cached nonces."""
        return len(self._cache)


# =============================================================================
# GOLDEN ADJUSTMENT
# =============================================================================

def golden_adjust(nonce: int, mod: int = 2**32) -> int:
    """
    Apply golden ratio adjustment to nonce.

    nonce_adjusted = floor(nonce * tau) mod m

    This maps nonce to golden partition of search space.
    The golden ratio partitioning ensures optimal coverage
    without clustering.

    Args:
        nonce: Input nonce
        mod: Modulus

    Returns:
        Adjusted nonce

    Mathematical Note:
        tau = 1/phi = phi - 1 = 0.618...
        This is the "most irrational" number in terms of
        continued fraction representation, providing
        optimal spacing in number sequences.
    """
    return int(nonce * TAU) % mod


def inverse_golden_adjust(nonce: int, mod: int = 2**32) -> int:
    """
    Inverse of golden adjustment.

    nonce_original = floor(nonce * phi) mod m

    This recovers approximately the original nonce.

    Args:
        nonce: Adjusted nonce
        mod: Modulus

    Returns:
        Approximately original nonce

    Note:
        Due to floor operations, this is not exactly invertible
        for all inputs.
    """
    return int(nonce * PHI) % mod


def golden_sequence(start: int, count: int, mod: int = 2**32) -> List[int]:
    """
    Generate a golden ratio spaced sequence.

    Each value is spaced by tau * mod from the previous,
    creating a low-discrepancy sequence.

    Args:
        start: Starting value
        count: Number of values to generate
        mod: Modulus

    Returns:
        List of golden-spaced values

    This is related to the Fibonacci hashing technique
    and provides excellent coverage of the nonce space.
    """
    result = []
    current = start
    increment = int(TAU * mod)

    for _ in range(count):
        result.append(current % mod)
        current = (current + increment) % mod

    return result


# =============================================================================
# SPECIALIZED NONCE GENERATORS
# =============================================================================

class FibonacciNonceGenerator:
    """
    Generate nonces from Fibonacci sequence.

    Uses F_n mod m instead of L_n (Lucas).
    Provides alternative algebraic structure.
    """

    def __init__(self, mod: int = 2**32):
        self.mod = mod
        self.index = 0
        # Start with F_1 = 1, F_2 = 1
        self.prev = 0
        self.curr = 1

    def next(self) -> int:
        """Generate next Fibonacci nonce."""
        result = self.curr
        self.prev, self.curr = self.curr, (self.prev + self.curr) % self.mod
        self.index += 1
        return result

    def reset(self):
        """Reset to beginning of sequence."""
        self.index = 0
        self.prev = 0
        self.curr = 1


class HybridNonceGenerator:
    """
    Combine Lucas and Fibonacci nonces with golden mixing.

    nonce(i) = (L_i + golden_adjust(F_i)) mod m

    This creates a more complex sequence with both
    Lucas and Fibonacci algebraic structure.
    """

    def __init__(self, mod: int = 2**32):
        self.mod = mod
        self.lucas = LucasNonceGenerator(mod, use_scheduling=False)
        self.fib = FibonacciNonceGenerator(mod)

    def next(self) -> int:
        """Generate next hybrid nonce."""
        L = self.lucas.next()
        F = self.fib.next()
        return (L + golden_adjust(F, self.mod)) % self.mod

    def reset(self):
        """Reset both generators."""
        self.lucas.reset()
        self.fib.reset()


# =============================================================================
# NONCE VALIDATION
# =============================================================================

def is_lucas_nonce(nonce: int, max_index: int = 10000, mod: int = 2**32) -> Optional[int]:
    """
    Check if a nonce is a Lucas trace value.

    Args:
        nonce: Nonce to check
        max_index: Maximum Lucas index to check
        mod: Modulus

    Returns:
        Lucas index if nonce is L_n mod m, else None

    Note:
        This is a brute-force check, O(max_index).
        Not efficient for cryptographic validation.
    """
    for i in range(max_index):
        if lucas_trace(i, mod) == nonce:
            return i
    return None


def nonce_quality(nonce: int, mod: int = 2**32) -> float:
    """
    Compute quality metric for a nonce.

    Quality is based on how close the nonce is to golden
    partitioning of the space.

    Args:
        nonce: Nonce value
        mod: Modulus

    Returns:
        Quality score in [0, 1], higher is better

    A "high quality" nonce is one that divides the search
    space according to golden ratio principles.
    """
    # Distance from nearest golden partition point
    normalized = nonce / mod
    # Golden spacing: distances should be near tau or 1-tau
    fractional = (normalized * PHI) % 1
    # Best if fractional is near tau
    quality = 1.0 - abs(fractional - TAU) / 0.5
    return max(0.0, min(1.0, quality))


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    # Main generator
    'LucasNonceGenerator',
    # Golden adjustment
    'golden_adjust',
    'inverse_golden_adjust',
    'golden_sequence',
    # Alternative generators
    'FibonacciNonceGenerator',
    'HybridNonceGenerator',
    # Validation
    'is_lucas_nonce',
    'nonce_quality',
]
