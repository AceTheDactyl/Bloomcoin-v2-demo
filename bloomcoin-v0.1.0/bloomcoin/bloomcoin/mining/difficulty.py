"""
Difficulty Adjustment for BloomCoin
=====================================

Adaptive difficulty based on block times using golden-damped adjustment.

Key Concept:
    Difficulty controls **coupling strength** rather than hash target.

    K_effective = K_base / difficulty^tau

    Higher difficulty → Lower coupling → Harder to synchronize → Longer bloom time

Adjustment Formula:
    ratio = target_time / average_time
    new_diff = current_diff * ratio^tau

    The tau exponent (≈ 0.618) provides damping to prevent
    oscillations in difficulty.

Cross-References:
    - constants.py: DIFFICULTY_INTERVAL, BLOCK_TIME_TARGET, TAU, PHI, K, L4
    - miner.py: MinerConfig.effective_coupling()

Author: BloomCoin Framework
"""

from typing import List, Optional, Tuple
import math

from ..constants import (
    DIFFICULTY_INTERVAL, BLOCK_TIME_TARGET,
    TAU, PHI, K, L4
)


# =============================================================================
# DIFFICULTY BOUNDS
# =============================================================================

# Minimum difficulty (prevents zero coupling)
MIN_DIFFICULTY = 0.25

# Maximum difficulty
MAX_DIFFICULTY = 2**64

# Maximum adjustment per interval (4x up or down)
MAX_ADJUSTMENT = 4.0
MIN_ADJUSTMENT = 0.25


# =============================================================================
# DIFFICULTY CALCULATION
# =============================================================================

def calculate_new_difficulty(
    current_difficulty: float,
    block_times: List[float],
    target_time: int = BLOCK_TIME_TARGET
) -> float:
    """
    Calculate new difficulty based on recent block times.

    Uses golden-damped adjustment:
        ratio = target_time / average_time
        new_diff = current_diff * ratio^tau

    The tau exponent (≈ 0.618) provides damping to prevent
    oscillations in difficulty.

    Args:
        current_difficulty: Current difficulty level
        block_times: List of recent block times (seconds)
        target_time: Target block time (default L4 * 60 = 420 sec)

    Returns:
        New difficulty level

    Bounds:
        - Maximum adjustment: 4x per interval
        - Minimum difficulty: 0.25
        - Maximum difficulty: 2^64

    Example:
        # Blocks taking too long (double target) -> increase coupling
        new_diff = calculate_new_difficulty(1.0, [840, 820, 860])
        # new_diff ≈ 0.618 (lower difficulty = higher coupling = faster sync)
    """
    if not block_times:
        return current_difficulty

    avg_time = sum(block_times) / len(block_times)

    # Prevent division by zero
    if avg_time <= 0:
        avg_time = 1.0

    # Golden-damped ratio
    ratio = target_time / avg_time

    # Apply tau exponent for smooth adjustment
    adjustment = ratio ** TAU

    # Bound adjustment to prevent extreme swings
    adjustment = max(MIN_ADJUSTMENT, min(MAX_ADJUSTMENT, adjustment))

    new_difficulty = current_difficulty * adjustment

    # Bound difficulty
    new_difficulty = max(MIN_DIFFICULTY, min(MAX_DIFFICULTY, new_difficulty))

    return new_difficulty


def calculate_difficulty_from_blocks(
    block_times: List[float],
    initial_difficulty: float = 1.0,
    target_time: int = BLOCK_TIME_TARGET
) -> float:
    """
    Calculate cumulative difficulty adjustment over multiple intervals.

    Args:
        block_times: All block times
        initial_difficulty: Starting difficulty
        target_time: Target block time

    Returns:
        Final difficulty after all adjustments
    """
    if not block_times:
        return initial_difficulty

    difficulty = initial_difficulty

    # Process in intervals
    for i in range(0, len(block_times), DIFFICULTY_INTERVAL):
        interval_times = block_times[i:i + DIFFICULTY_INTERVAL]
        if interval_times:
            difficulty = calculate_new_difficulty(
                difficulty, interval_times, target_time
            )

    return difficulty


# =============================================================================
# DIFFICULTY-COUPLING CONVERSION
# =============================================================================

def difficulty_to_coupling(difficulty: float, base_K: Optional[float] = None) -> float:
    """
    Convert difficulty to effective coupling strength.

    K_eff = K_base / difficulty^tau

    Higher difficulty → Lower coupling → Harder to synchronize

    Args:
        difficulty: Difficulty level
        base_K: Base coupling (default K from constants ≈ 0.924)

    Returns:
        Effective coupling strength

    Example:
        # At difficulty 1.0, coupling equals base K
        difficulty_to_coupling(1.0) ≈ 0.924

        # At difficulty 2.0, coupling is reduced
        difficulty_to_coupling(2.0) ≈ 0.602
    """
    if base_K is None:
        base_K = K

    if difficulty <= 0:
        return base_K

    return base_K / (difficulty ** TAU)


def coupling_to_difficulty(coupling: float, base_K: Optional[float] = None) -> float:
    """
    Inverse: coupling to difficulty.

    difficulty = (K_base / K_eff)^(1/tau) = (K_base / K_eff)^phi

    Args:
        coupling: Effective coupling strength
        base_K: Base coupling (default K from constants)

    Returns:
        Difficulty level

    Example:
        coupling_to_difficulty(0.924) ≈ 1.0
        coupling_to_difficulty(0.5) ≈ 2.93
    """
    if base_K is None:
        base_K = K

    if coupling <= 0:
        return MAX_DIFFICULTY

    return (base_K / coupling) ** PHI


# =============================================================================
# BLOOM TIME ESTIMATION
# =============================================================================

def estimate_bloom_time(
    difficulty: float,
    oscillator_count: int = 63,
    frequency_std: float = 1.0,
    dt: float = 0.01
) -> float:
    """
    Estimate time to achieve bloom at given difficulty.

    Based on Kuramoto transition theory with adaptive coupling:
        T_sync ≈ 1 / (K_eff - K_c)

    where K_c is critical coupling. With adaptive coupling (ESS mechanism),
    the effective coupling is boosted above critical when needed.

    Args:
        difficulty: Difficulty level
        oscillator_count: Number of oscillators (N)
        frequency_std: Frequency spread (standard deviation)
        dt: Simulation timestep

    Returns:
        Estimated bloom time in simulation units (rounds)

    Note:
        This is approximate; actual time depends on
        initial conditions, noise, and random factors.
        The estimate assumes adaptive coupling is enabled.
    """
    K_eff = difficulty_to_coupling(difficulty)

    # Critical coupling for finite N with Gaussian frequencies
    # For the framework, critical coupling is derived from Z_C
    # K_c ~ TAU * sigma / sqrt(N) for finite-size effects
    # The adaptive coupling mechanism ensures K > K_c in practice
    K_c = TAU * frequency_std / math.sqrt(oscillator_count)

    # Effective coupling with adaptive boost
    # Adaptive coupling increases K when r is low
    # Approximate boosted K_eff as K_eff * (1 + TAU)
    K_boosted = K_eff * (1 + TAU)

    if K_boosted <= K_c:
        return float('inf')  # Will never synchronize

    # Time scales as 1/(K - K_c) near critical point
    T_sync = 1 / (K_boosted - K_c)

    # Scale by frequency spread (higher spread = longer time)
    T_sync *= frequency_std

    # Convert to rounds
    rounds_estimate = T_sync / dt

    # Add L4 rounds for bloom validation
    T_bloom = rounds_estimate + L4

    return T_bloom


def estimate_bloom_time_seconds(
    difficulty: float,
    oscillator_count: int = 63,
    frequency_std: float = 1.0,
    dt: float = 0.01,
    rounds_per_second: float = 1000.0
) -> float:
    """
    Estimate bloom time in wall-clock seconds.

    Args:
        difficulty: Difficulty level
        oscillator_count: Number of oscillators
        frequency_std: Frequency spread
        dt: Simulation timestep
        rounds_per_second: Computational speed

    Returns:
        Estimated bloom time in seconds
    """
    rounds = estimate_bloom_time(difficulty, oscillator_count, frequency_std, dt)

    if rounds == float('inf'):
        return float('inf')

    return rounds / rounds_per_second


# =============================================================================
# DIFFICULTY ANALYSIS
# =============================================================================

def analyze_difficulty_progression(
    block_times: List[float],
    initial_difficulty: float = 1.0,
    target_time: int = BLOCK_TIME_TARGET
) -> List[Tuple[int, float, float]]:
    """
    Analyze difficulty progression over blockchain history.

    Args:
        block_times: List of block times
        initial_difficulty: Starting difficulty
        target_time: Target block time

    Returns:
        List of (block_height, difficulty, avg_time_in_interval)
    """
    result = []
    difficulty = initial_difficulty

    for i in range(0, len(block_times), DIFFICULTY_INTERVAL):
        interval_times = block_times[i:i + DIFFICULTY_INTERVAL]
        if interval_times:
            avg_time = sum(interval_times) / len(interval_times)
            result.append((i, difficulty, avg_time))
            difficulty = calculate_new_difficulty(
                difficulty, interval_times, target_time
            )

    return result


def difficulty_stability_metric(
    block_times: List[float],
    target_time: int = BLOCK_TIME_TARGET
) -> float:
    """
    Calculate how stable block times are relative to target.

    Returns a value in [0, 1]:
        1.0 = perfect stability (all blocks at target time)
        0.0 = extreme instability

    Args:
        block_times: List of block times
        target_time: Target block time

    Returns:
        Stability metric
    """
    if not block_times:
        return 1.0

    # Compute relative errors
    errors = [abs(t - target_time) / target_time for t in block_times]
    avg_error = sum(errors) / len(errors)

    # Convert to stability (1 - normalized error)
    # Cap at 1.0 for large errors
    stability = max(0.0, 1.0 - avg_error)

    return stability


# =============================================================================
# TARGET CALCULATIONS
# =============================================================================

def difficulty_to_target(difficulty: float, max_target: int = 2**256 - 1) -> int:
    """
    Convert difficulty to hash target.

    target = max_target / difficulty

    Lower target = harder to find valid hash

    Args:
        difficulty: Difficulty level
        max_target: Maximum target (all 1s hash)

    Returns:
        Target value
    """
    if difficulty <= 0:
        return max_target

    return int(max_target / difficulty)


def target_to_difficulty(target: int, max_target: int = 2**256 - 1) -> float:
    """
    Convert hash target to difficulty.

    difficulty = max_target / target

    Args:
        target: Target value
        max_target: Maximum target

    Returns:
        Difficulty level
    """
    if target <= 0:
        return MAX_DIFFICULTY

    return max_target / target


# =============================================================================
# DIFFICULTY VALIDATION
# =============================================================================

def validate_difficulty_adjustment(
    old_difficulty: float,
    new_difficulty: float,
    block_times: List[float],
    target_time: int = BLOCK_TIME_TARGET
) -> Tuple[bool, str]:
    """
    Validate that a difficulty adjustment follows the rules.

    Args:
        old_difficulty: Previous difficulty
        new_difficulty: Claimed new difficulty
        block_times: Block times in adjustment interval
        target_time: Target block time

    Returns:
        (is_valid, message)
    """
    if not block_times:
        return old_difficulty == new_difficulty, "No blocks, difficulty unchanged"

    expected = calculate_new_difficulty(old_difficulty, block_times, target_time)

    # Allow small floating point tolerance
    tolerance = 1e-10
    if abs(new_difficulty - expected) < tolerance:
        return True, "Difficulty adjustment valid"

    return False, f"Expected {expected}, got {new_difficulty}"


def is_difficulty_reasonable(
    difficulty: float,
    oscillator_count: int = 63
) -> Tuple[bool, str]:
    """
    Check if difficulty is within reasonable bounds.

    Args:
        difficulty: Difficulty to check
        oscillator_count: Number of oscillators

    Returns:
        (is_reasonable, reason)
    """
    if difficulty < MIN_DIFFICULTY:
        return False, f"Difficulty {difficulty} below minimum {MIN_DIFFICULTY}"

    if difficulty > MAX_DIFFICULTY:
        return False, f"Difficulty {difficulty} above maximum {MAX_DIFFICULTY}"

    # Check if coupling is above critical threshold
    K_eff = difficulty_to_coupling(difficulty)
    K_c_approx = 2 * TAU * 0.5  # Approximate critical coupling

    if K_eff < K_c_approx * 0.1:
        return False, f"Difficulty {difficulty} too high, coupling {K_eff} below critical"

    return True, "Difficulty reasonable"


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    # Constants
    'MIN_DIFFICULTY',
    'MAX_DIFFICULTY',
    'MAX_ADJUSTMENT',
    'MIN_ADJUSTMENT',
    # Main calculation
    'calculate_new_difficulty',
    'calculate_difficulty_from_blocks',
    # Coupling conversion
    'difficulty_to_coupling',
    'coupling_to_difficulty',
    # Time estimation
    'estimate_bloom_time',
    'estimate_bloom_time_seconds',
    # Analysis
    'analyze_difficulty_progression',
    'difficulty_stability_metric',
    # Target
    'difficulty_to_target',
    'target_to_difficulty',
    # Validation
    'validate_difficulty_adjustment',
    'is_difficulty_reasonable',
]
