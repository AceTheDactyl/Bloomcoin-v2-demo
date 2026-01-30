"""
BloomCoin Miner Implementation
===============================

Main mining loop for Proof-of-Coherence consensus.

Key Difference from PoW:
    Instead of incrementing nonces to find a hash below target,
    we evolve oscillator phases until coherence emerges.
    The "work" is achieving synchronization, not random search.

Process:
    1. Initialize oscillator network with Lucas-derived seed
    2. Run Kuramoto dynamics with adaptive coupling
    3. Monitor order parameter r
    4. When r >= z_c for L4 consecutive rounds, bloom achieved
    5. Generate block with phase-encoded header
    6. Verify hash meets difficulty target

Cross-References:
    - consensus/kuramoto.py: Oscillator dynamics
    - consensus/threshold_gate.py: ConsensusCertificate
    - core/lucas_matrix.py: Lucas nonce generation
    - core/hash_wrapper.py: PhaseEncodedHeader, bloom_hash

Author: BloomCoin Framework
"""

from dataclasses import dataclass, field
from typing import Callable, Optional, List
import time

from ..constants import (
    DEFAULT_OSCILLATOR_COUNT, K, Z_C, L4,
    BLOCK_TIME_TARGET, TAU
)
from ..consensus.kuramoto import (
    KuramotoState, initialize_kuramoto,
    kuramoto_step, adaptive_coupling,
    compute_order_parameter
)
from ..consensus.threshold_gate import ConsensusCertificate
from ..core.lucas_matrix import lucas_trace
from ..core.hash_wrapper import (
    PhaseEncodedHeader, bloom_hash, target_to_compact
)


# =============================================================================
# MINER CONFIGURATION
# =============================================================================

@dataclass
class MinerConfig:
    """
    Configuration for a BloomCoin miner.

    Attributes:
        oscillator_count: Number of Kuramoto oscillators (default 63)
        base_coupling: Base K value before difficulty adjustment
        frequency_std: Natural frequency spread (Gaussian)
        dt: Simulation timestep
        max_rounds: Maximum rounds before trying new nonce
        max_nonce_attempts: Maximum nonce attempts before giving up
        target_time: Target block time in seconds
        difficulty: Current difficulty level (multiplier)
        reward_address: Address to receive mining rewards
        use_adaptive: Use adaptive coupling (ESS mechanism)
        verbose: Print progress information
    """
    oscillator_count: int = DEFAULT_OSCILLATOR_COUNT
    base_coupling: float = K
    frequency_std: float = 1.0
    dt: float = 0.01
    max_rounds: int = 100000
    max_nonce_attempts: int = 1000
    target_time: int = BLOCK_TIME_TARGET
    difficulty: float = 1.0
    reward_address: bytes = field(default_factory=bytes)
    use_adaptive: bool = True
    verbose: bool = False

    def effective_coupling(self) -> float:
        """
        Compute K_eff based on difficulty.

        K_eff = K_base / difficulty^tau

        Higher difficulty = lower coupling = harder to sync
        """
        return self.base_coupling / (self.difficulty ** TAU)


# =============================================================================
# MINING RESULT
# =============================================================================

@dataclass
class MiningResult:
    """
    Result of a mining attempt.

    Attributes:
        success: Whether consensus was achieved
        rounds: Total number of rounds taken
        rounds_to_bloom: Rounds from bloom_start to bloom_end (if success)
        certificate: Consensus certificate (if success)
        final_state: Final oscillator state
        header: Block header (if success)
        block_hash: Hash of completed block (if success)
        nonce: Lucas nonce used
        nonce_attempts: Number of nonce attempts made
        elapsed_time: Wall-clock time in seconds
        max_r_achieved: Maximum r value achieved during mining
    """
    success: bool
    rounds: int
    rounds_to_bloom: int
    certificate: Optional[ConsensusCertificate]
    final_state: KuramotoState
    header: Optional[PhaseEncodedHeader]
    block_hash: Optional[bytes]
    nonce: int
    nonce_attempts: int
    elapsed_time: float
    max_r_achieved: float

    def __repr__(self) -> str:
        if self.success:
            return (
                f"MiningResult(success=True, rounds={self.rounds}, "
                f"nonce={self.nonce}, r={self.max_r_achieved:.4f}, "
                f"time={self.elapsed_time:.2f}s)"
            )
        else:
            return (
                f"MiningResult(success=False, attempts={self.nonce_attempts}, "
                f"max_r={self.max_r_achieved:.4f}, time={self.elapsed_time:.2f}s)"
            )


# =============================================================================
# MAIN MINING FUNCTION
# =============================================================================

def mine_block(
    config: MinerConfig,
    prev_hash: bytes,
    merkle_root: bytes,
    difficulty_bits: Optional[int] = None,
    timestamp: Optional[int] = None,
    on_progress: Optional[Callable[[int, int, float], None]] = None
) -> MiningResult:
    """
    Mine a single block using Proof-of-Coherence.

    Process:
        1. Initialize oscillator network with Lucas-derived seed
        2. Run Kuramoto dynamics with adaptive coupling
        3. Monitor order parameter r
        4. When r >= z_c for L4 consecutive rounds, bloom achieved
        5. Generate block with phase-encoded header
        6. Verify hash meets difficulty target

    Args:
        config: Miner configuration
        prev_hash: Hash of previous block (32 bytes)
        merkle_root: Merkle root of transactions (32 bytes)
        difficulty_bits: Compact difficulty target (default from config)
        timestamp: Block timestamp (default: current time)
        on_progress: Callback(nonce_attempt, round, r) for progress updates

    Returns:
        MiningResult containing success status, certificate, header, hash

    Example:
        config = MinerConfig(oscillator_count=63, difficulty=1.0)
        result = mine_block(
            config,
            prev_hash=bytes(32),
            merkle_root=bytes(32)
        )
        if result.success:
            print(f"Mined block: {result.block_hash.hex()}")
    """
    start_time = time.time()
    timestamp = timestamp or int(time.time())

    # Compute compact difficulty representation
    if difficulty_bits is None:
        # Convert difficulty multiplier to compact target
        # Base target is 0x1d00ffff (Bitcoin genesis difficulty)
        base_target = 0x00000000FFFF0000000000000000000000000000000000000000000000000000
        adjusted_target = int(base_target / config.difficulty)
        difficulty_bits = target_to_compact(adjusted_target)

    max_r_overall = 0.0
    total_rounds = 0
    final_state = None

    for nonce_attempt in range(config.max_nonce_attempts):
        # Generate Lucas nonce from attempt index
        nonce = lucas_trace(nonce_attempt, 2**32)

        # Initialize oscillators with nonce as seed
        state = initialize_kuramoto(
            N=config.oscillator_count,
            frequency_std=config.frequency_std,
            coupling=config.effective_coupling(),
            seed=nonce % (2**31)  # Ensure valid seed
        )

        r_history: List[float] = []
        psi_history: List[float] = []
        bloom_start: Optional[int] = None

        for round_num in range(config.max_rounds):
            # Compute order parameter
            r, psi = compute_order_parameter(state.phases)
            r_history.append(r)
            psi_history.append(psi)

            max_r_overall = max(max_r_overall, r)

            # Progress callback
            if on_progress:
                on_progress(nonce_attempt, round_num, r)

            # Check for bloom condition
            if r >= Z_C:
                if bloom_start is None:
                    bloom_start = round_num
                    if config.verbose:
                        print(f"  Nonce {nonce_attempt}: Potential bloom at round {round_num} (r={r:.4f})")
                elif round_num - bloom_start >= L4 - 1:
                    # BLOOM ACHIEVED!
                    elapsed = time.time() - start_time
                    total_rounds += round_num + 1

                    if config.verbose:
                        print(f"  BLOOM! Nonce {nonce_attempt}, round {round_num}, r={r:.4f}")

                    # Create consensus certificate
                    certificate = ConsensusCertificate(
                        bloom_start=bloom_start,
                        bloom_end=round_num,
                        r_values=r_history[bloom_start:round_num + 1],
                        psi_values=psi_history[bloom_start:round_num + 1],
                        final_phases=state.phases.tolist(),
                        oscillator_count=state.N,
                        threshold=Z_C,
                        required_rounds=L4
                    )

                    # Create phase-encoded header
                    header = PhaseEncodedHeader(
                        version=1,
                        prev_hash=prev_hash,
                        merkle_root=merkle_root,
                        timestamp=timestamp,
                        difficulty=difficulty_bits,
                        nonce=nonce,
                        order_parameter=r,
                        mean_phase=psi,
                        oscillator_count=state.N
                    )

                    # Compute block hash
                    block_hash = bloom_hash(header)

                    return MiningResult(
                        success=True,
                        rounds=total_rounds,
                        rounds_to_bloom=round_num - bloom_start + 1,
                        certificate=certificate,
                        final_state=state,
                        header=header,
                        block_hash=block_hash,
                        nonce=nonce,
                        nonce_attempts=nonce_attempt + 1,
                        elapsed_time=elapsed,
                        max_r_achieved=r
                    )
            else:
                # Reset bloom candidate if we drop below threshold
                if bloom_start is not None and config.verbose:
                    duration = round_num - bloom_start
                    print(f"  Nonce {nonce_attempt}: Bloom failed after {duration} rounds (r={r:.4f})")
                bloom_start = None

            # Apply adaptive coupling if enabled
            if config.use_adaptive:
                K_eff = adaptive_coupling(r, config.effective_coupling())
                state = KuramotoState(
                    phases=state.phases,
                    frequencies=state.frequencies,
                    coupling=K_eff,
                    time=state.time,
                    history=state.history
                )

            # Evolve oscillators
            state = kuramoto_step(state, dt=config.dt)

        # Track total rounds and final state
        total_rounds += config.max_rounds
        final_state = state

        if config.verbose:
            print(f"  Nonce {nonce_attempt}: Failed after {config.max_rounds} rounds (max_r={max(r_history):.4f})")

    # Failed to achieve consensus after all nonce attempts
    elapsed = time.time() - start_time

    if config.verbose:
        print(f"Mining failed after {config.max_nonce_attempts} nonce attempts")

    return MiningResult(
        success=False,
        rounds=total_rounds,
        rounds_to_bloom=0,
        certificate=None,
        final_state=final_state,
        header=None,
        block_hash=None,
        nonce=lucas_trace(config.max_nonce_attempts - 1, 2**32),
        nonce_attempts=config.max_nonce_attempts,
        elapsed_time=elapsed,
        max_r_achieved=max_r_overall
    )


# =============================================================================
# QUICK MINE (OPTIMIZED FOR FAST CONSENSUS)
# =============================================================================

def quick_mine(
    prev_hash: bytes,
    merkle_root: bytes,
    oscillator_count: int = DEFAULT_OSCILLATOR_COUNT,
    max_attempts: int = 10
) -> Optional[MiningResult]:
    """
    Quick mining for testing with optimized parameters.

    Uses high coupling and low frequency spread for fast synchronization.

    Args:
        prev_hash: Previous block hash
        merkle_root: Merkle root
        oscillator_count: Number of oscillators
        max_attempts: Maximum nonce attempts

    Returns:
        MiningResult if successful, None if failed
    """
    config = MinerConfig(
        oscillator_count=oscillator_count,
        base_coupling=K * 2,  # Higher coupling for faster sync
        frequency_std=0.5,     # Lower spread for easier sync
        dt=0.02,               # Larger timesteps for speed
        max_rounds=5000,       # Fewer rounds per attempt
        max_nonce_attempts=max_attempts,
        difficulty=0.5,        # Lower difficulty
        use_adaptive=True,
        verbose=False
    )

    result = mine_block(config, prev_hash, merkle_root)
    return result if result.success else None


# =============================================================================
# MINING STATISTICS
# =============================================================================

@dataclass
class MiningStats:
    """
    Statistics from multiple mining attempts.
    """
    attempts: int
    successes: int
    failures: int
    avg_rounds_to_bloom: float
    avg_time: float
    max_r_distribution: List[float]

    @property
    def success_rate(self) -> float:
        if self.attempts == 0:
            return 0.0
        return self.successes / self.attempts


def benchmark_mining(
    config: MinerConfig,
    num_trials: int = 10
) -> MiningStats:
    """
    Benchmark mining performance over multiple trials.

    Args:
        config: Miner configuration
        num_trials: Number of mining attempts

    Returns:
        MiningStats with aggregated results
    """
    results: List[MiningResult] = []

    for i in range(num_trials):
        # Use trial index for unique prev_hash
        prev_hash = bytes([i % 256] * 32)
        merkle_root = bytes([(i + 128) % 256] * 32)

        result = mine_block(config, prev_hash, merkle_root)
        results.append(result)

    successes = sum(1 for r in results if r.success)
    failures = num_trials - successes

    successful_results = [r for r in results if r.success]
    avg_rounds = (
        sum(r.rounds_to_bloom for r in successful_results) / len(successful_results)
        if successful_results else 0.0
    )
    avg_time = sum(r.elapsed_time for r in results) / len(results)
    max_r_dist = [r.max_r_achieved for r in results]

    return MiningStats(
        attempts=num_trials,
        successes=successes,
        failures=failures,
        avg_rounds_to_bloom=avg_rounds,
        avg_time=avg_time,
        max_r_distribution=max_r_dist
    )


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    'MinerConfig',
    'MiningResult',
    'mine_block',
    'quick_mine',
    'MiningStats',
    'benchmark_mining',
]
