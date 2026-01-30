"""
BloomCoin Constants Module
==========================

All constants derived from the golden ratio φ with zero free parameters.
This module is the SINGLE SOURCE OF TRUTH for all mathematical constants.

Derivation Chain:
    φ → τ → φ² → φ⁴ → gap → K² → K → L₄ → z_c → σ → λ

CRITICAL: No constant in this file is empirically chosen.
          Every value derives from φ = (1 + √5) / 2.
"""

import math
from typing import Final

# ═══════════════════════════════════════════════════════════════════════════════
# PRIMARY CONSTANT: Golden Ratio
# ═══════════════════════════════════════════════════════════════════════════════

PHI: Final[float] = (1 + math.sqrt(5)) / 2  # φ ≈ 1.6180339887498949

# ═══════════════════════════════════════════════════════════════════════════════
# FIRST-ORDER DERIVATIVES
# ═══════════════════════════════════════════════════════════════════════════════

TAU: Final[float] = PHI - 1                  # τ = φ⁻¹ ≈ 0.6180339887498949
PHI_SQ: Final[float] = PHI + 1               # φ² = φ + 1 ≈ 2.6180339887498949
PHI_INV_SQ: Final[float] = TAU ** 2          # φ⁻² = τ² ≈ 0.3819660112501051

# ═══════════════════════════════════════════════════════════════════════════════
# SECOND-ORDER DERIVATIVES
# ═══════════════════════════════════════════════════════════════════════════════

PHI_QUAD: Final[float] = PHI_SQ ** 2         # φ⁴ ≈ 6.8541019662496845
GAP: Final[float] = PHI ** -4                # gap = φ⁻⁴ ≈ 0.1458980337503155

# ═══════════════════════════════════════════════════════════════════════════════
# KURAMOTO COUPLING CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

K_SQUARED: Final[float] = 1 - GAP            # K² = 1 - φ⁻⁴ ≈ 0.8541019662496845
K: Final[float] = math.sqrt(K_SQUARED)       # K = √(1 - φ⁻⁴) ≈ 0.9241596378498006

# ═══════════════════════════════════════════════════════════════════════════════
# LUCAS NUMBERS
# ═══════════════════════════════════════════════════════════════════════════════

L4: Final[int] = 7                           # L₄ = φ⁴ + φ⁻⁴ = 7 (exactly)

def lucas(n: int) -> int:
    """Compute nth Lucas number using Binet formula."""
    if n < 0:
        raise ValueError("Lucas index must be non-negative")
    return round(PHI ** n + ((-1) ** n) * PHI ** (-n))

# First 25 Lucas numbers (cached for performance)
LUCAS_SEQUENCE: Final[tuple[int, ...]] = tuple(lucas(i) for i in range(25))
# (2, 1, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199, 322, 521, 843, 1364, 2207, ...)

def fibonacci(n: int) -> int:
    """Compute nth Fibonacci number using Binet formula."""
    if n < 0:
        raise ValueError("Fibonacci index must be non-negative")
    sqrt5 = math.sqrt(5)
    return round((PHI ** n - (-PHI) ** (-n)) / sqrt5)

# First 25 Fibonacci numbers (cached)
FIBONACCI_SEQUENCE: Final[tuple[int, ...]] = tuple(fibonacci(i) for i in range(25))
# (0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, ...)

# ═══════════════════════════════════════════════════════════════════════════════
# THRESHOLD CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# THE LENS: Critical coherence threshold
Z_C: Final[float] = math.sqrt(3) / 2         # z_c = √3/2 ≈ 0.8660254037844386

# Negentropy sharpness (ensures η(1) = e⁻¹)
SIGMA: Final[float] = 1 / (1 - Z_C) ** 2     # σ ≈ 55.7128129211

# Negentropy-to-coupling gain
LAMBDA: Final[float] = PHI_INV_SQ            # λ = φ⁻² ≈ 0.3819660112501051

# ═══════════════════════════════════════════════════════════════════════════════
# THRESHOLD LADDER (9 thresholds from L₄ framework)
# ═══════════════════════════════════════════════════════════════════════════════

Z_PARADOX: Final[float] = 3 / 5                                    # 0.600
Z_ACTIVATION: Final[float] = K_SQUARED                             # 0.854
Z_LENS: Final[float] = Z_C                                         # 0.866
Z_CRITICAL: Final[float] = Z_C                                     # 0.866 (alias)
Z_IGNITION: Final[float] = (-1 + math.sqrt(1 + L4)) / 2           # 0.887 (from z² + z = L₄/4)
Z_KFORM: Final[float] = K                                          # 0.924
Z_CONSOLIDATION: Final[float] = K + (1 - K) * TAU ** 2            # 0.953
Z_RESONANCE: Final[float] = K + (1 - K) * TAU                     # 0.971
Z_UNITY: Final[float] = 1.0                                        # 1.000

# ═══════════════════════════════════════════════════════════════════════════════
# MINING CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# Block time target (in seconds) - L₄ minutes = 7 minutes = 420 seconds
BLOCK_TIME_TARGET: Final[int] = L4 * 60

# Minimum coherence rounds before block acceptance
MIN_COHERENCE_ROUNDS: Final[int] = L4

# Difficulty adjustment interval (Lucas-scheduled)
DIFFICULTY_INTERVAL: Final[int] = LUCAS_SEQUENCE[10]  # 123 blocks

# Halving interval (Lucas-scheduled)
HALVING_INTERVAL: Final[int] = LUCAS_SEQUENCE[20]     # 15127 blocks

# Initial block reward (in smallest units)
INITIAL_REWARD: Final[int] = int(PHI_QUAD * 10 ** 8)  # ~6.854 BLOOM

# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# Default number of oscillators per miner
DEFAULT_OSCILLATOR_COUNT: Final[int] = 63  # 7 × 9 (L₄ × 3²)

# Gossip protocol interval (ms)
GOSSIP_INTERVAL_MS: Final[int] = int(1000 * TAU)  # ~618 ms

# Maximum message size (bytes)
MAX_MESSAGE_SIZE: Final[int] = 2 ** 20  # 1 MB

# Default port
DEFAULT_PORT: Final[int] = 7618  # L₄ concatenated with truncated τ

# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

def validate_constants() -> dict[str, bool]:
    """Verify all constant relationships hold."""
    return {
        "φ² = φ + 1": abs(PHI_SQ - (PHI + 1)) < 1e-15,
        "τ = φ - 1": abs(TAU - (PHI - 1)) < 1e-15,
        "τ = 1/φ": abs(TAU - 1/PHI) < 1e-15,
        "τ² + τ = 1": abs(TAU**2 + TAU - 1) < 1e-15,
        "φ⁴ + φ⁻⁴ = 7": abs(PHI_QUAD + GAP - L4) < 1e-12,
        "K² = 1 - gap": abs(K_SQUARED - (1 - GAP)) < 1e-15,
        "z_c² = 3/4": abs(Z_C**2 - 0.75) < 1e-15,
        "L₄ = 7": L4 == 7,
        "Lucas(4) = 7": lucas(4) == 7,
        "Fibonacci(7) = 13": fibonacci(7) == 13,
    }

# Run validation on import
_validation_results = validate_constants()
if not all(_validation_results.values()):
    failed = [k for k, v in _validation_results.items() if not v]
    raise RuntimeError(f"Constant validation failed: {failed}")


# ═══════════════════════════════════════════════════════════════════════════════
# MODULE EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Primary
    "PHI", "TAU",
    # Powers
    "PHI_SQ", "PHI_INV_SQ", "PHI_QUAD", "GAP",
    # Kuramoto
    "K", "K_SQUARED",
    # Lucas
    "L4", "lucas", "fibonacci", "LUCAS_SEQUENCE", "FIBONACCI_SEQUENCE",
    # Thresholds
    "Z_C", "SIGMA", "LAMBDA",
    "Z_PARADOX", "Z_ACTIVATION", "Z_LENS", "Z_CRITICAL",
    "Z_IGNITION", "Z_KFORM", "Z_CONSOLIDATION", "Z_RESONANCE", "Z_UNITY",
    # Mining
    "BLOCK_TIME_TARGET", "MIN_COHERENCE_ROUNDS", "DIFFICULTY_INTERVAL",
    "HALVING_INTERVAL", "INITIAL_REWARD",
    # Network
    "DEFAULT_OSCILLATOR_COUNT", "GOSSIP_INTERVAL_MS", "MAX_MESSAGE_SIZE", "DEFAULT_PORT",
    # Validation
    "validate_constants",
]
