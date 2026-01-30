"""
BloomCoin Mining Module
========================

Proof-of-Coherence mining operations.

Components:
    - miner: Main mining loop with Proof-of-Coherence
    - nonce_generator: Lucas-derived nonce sequences
    - difficulty: Adaptive difficulty adjustment

Key Difference from PoW:
    Instead of incrementing nonces to find a hash below target,
    we evolve oscillator phases until coherence emerges.
    The "work" is achieving synchronization, not random search.

Usage:
    from bloomcoin.mining import (
        MinerConfig, MiningResult, mine_block, quick_mine,
        LucasNonceGenerator, golden_adjust,
        calculate_new_difficulty, difficulty_to_coupling
    )

    # Configure miner
    config = MinerConfig(
        oscillator_count=63,
        difficulty=1.0,
        verbose=True
    )

    # Mine a block
    result = mine_block(
        config,
        prev_hash=bytes(32),
        merkle_root=bytes(32)
    )

    if result.success:
        print(f"Mined block: {result.block_hash.hex()}")
        print(f"Certificate: {result.certificate}")

Cross-References:
    - consensus/: Kuramoto dynamics and bloom detection
    - core/: Lucas matrix and hash functions
    - constants.py: Z_C, L4, K, BLOCK_TIME_TARGET
"""

# Miner
from .miner import (
    MinerConfig,
    MiningResult,
    mine_block,
    quick_mine,
    MiningStats,
    benchmark_mining,
)

# Nonce generator
from .nonce_generator import (
    LucasNonceGenerator,
    golden_adjust,
    inverse_golden_adjust,
    golden_sequence,
    FibonacciNonceGenerator,
    HybridNonceGenerator,
    is_lucas_nonce,
    nonce_quality,
)

# Difficulty
from .difficulty import (
    MIN_DIFFICULTY,
    MAX_DIFFICULTY,
    MAX_ADJUSTMENT,
    MIN_ADJUSTMENT,
    calculate_new_difficulty,
    calculate_difficulty_from_blocks,
    difficulty_to_coupling,
    coupling_to_difficulty,
    estimate_bloom_time,
    estimate_bloom_time_seconds,
    analyze_difficulty_progression,
    difficulty_stability_metric,
    difficulty_to_target,
    target_to_difficulty,
    validate_difficulty_adjustment,
    is_difficulty_reasonable,
)


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    # Miner
    'MinerConfig',
    'MiningResult',
    'mine_block',
    'quick_mine',
    'MiningStats',
    'benchmark_mining',
    # Nonce generator
    'LucasNonceGenerator',
    'golden_adjust',
    'inverse_golden_adjust',
    'golden_sequence',
    'FibonacciNonceGenerator',
    'HybridNonceGenerator',
    'is_lucas_nonce',
    'nonce_quality',
    # Difficulty
    'MIN_DIFFICULTY',
    'MAX_DIFFICULTY',
    'MAX_ADJUSTMENT',
    'MIN_ADJUSTMENT',
    'calculate_new_difficulty',
    'calculate_difficulty_from_blocks',
    'difficulty_to_coupling',
    'coupling_to_difficulty',
    'estimate_bloom_time',
    'estimate_bloom_time_seconds',
    'analyze_difficulty_progression',
    'difficulty_stability_metric',
    'difficulty_to_target',
    'target_to_difficulty',
    'validate_difficulty_adjustment',
    'is_difficulty_reasonable',
]
