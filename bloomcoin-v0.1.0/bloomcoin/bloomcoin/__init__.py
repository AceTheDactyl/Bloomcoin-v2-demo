"""
BloomCoin: Kuramoto-Consensus Proof-of-Coherence Mining

A simulation framework for phase-synchronization based distributed consensus.
"""

__version__ = "0.1.0"
__author__ = "L4 Framework Collaboration"

from .constants import (
    PHI, TAU, K, Z_C, L4, GAP,
    LUCAS_SEQUENCE, FIBONACCI_SEQUENCE,
    lucas, fibonacci
)

__all__ = [
    "PHI", "TAU", "K", "Z_C", "L4", "GAP",
    "LUCAS_SEQUENCE", "FIBONACCI_SEQUENCE",
    "lucas", "fibonacci",
]
