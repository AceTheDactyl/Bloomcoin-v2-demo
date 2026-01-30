"""
BloomCoin Consensus Module
===========================

Implements Proof-of-Coherence consensus via Kuramoto oscillator synchronization.

Components:
    - kuramoto: Oscillator dynamics and evolution
    - order_parameter: Synchronization measures (r, q, Fisher info)
    - threshold_gate: Bloom detection and consensus certificates

Usage:
    from bloomcoin.consensus import (
        initialize_kuramoto, kuramoto_step, kuramoto_evolve,
        compute_order_parameter, analyze_order,
        validate_bloom, ConsensusCertificate,
        run_consensus
    )

    # Initialize oscillator network
    state = initialize_kuramoto(N=63, seed=42)

    # Run consensus
    success, certificate, final_state = run_consensus(state)

    if success:
        print(f"Consensus achieved! Certificate: {certificate}")
"""

# Kuramoto dynamics
from .kuramoto import (
    KuramotoState,
    initialize_kuramoto,
    kuramoto_step,
    kuramoto_evolve,
    compute_order_parameter,
    negentropy_gate,
    adaptive_coupling,
    get_synchronization_time,
    compute_phase_velocity,
    compute_phase_coherence_local,
)

# Order parameter analysis
from .order_parameter import (
    compute_edwards_anderson,
    classify_phase,
    compute_fisher_information,
    compute_negentropy,
    OrderAnalysis,
    analyze_order,
    compute_r_statistics,
    compute_autocorrelation,
)

# Threshold and bloom detection
from .threshold_gate import (
    ThresholdCrossing,
    detect_crossings,
    count_crossings,
    BloomEvent,
    validate_bloom,
    detect_all_blooms,
    get_first_valid_bloom,
    ConsensusCertificate,
    create_certificate,
    get_threshold_ladder,
    classify_by_threshold,
)

# Import constants for convenience
from ..constants import Z_C, L4, K


# =============================================================================
# INTEGRATED CONSENSUS LOOP
# =============================================================================

def run_consensus(
    initial_state: KuramotoState,
    max_rounds: int = 10000,
    dt: float = 0.01,
    use_adaptive: bool = True,
    verbose: bool = False
) -> tuple:
    """
    Run Proof-of-Coherence consensus algorithm.

    This is the main entry point for mining. It evolves a Kuramoto oscillator
    network until consensus is achieved (bloom detected) or max_rounds reached.

    Process:
        1. Initialize oscillators (scattered state)
        2. Apply Kuramoto dynamics with optional adaptive coupling
        3. Monitor order parameter r
        4. When r >= z_c for L4 rounds, consensus achieved
        5. Generate consensus certificate

    Args:
        initial_state: Starting oscillator configuration
        max_rounds: Maximum simulation steps before giving up
        dt: Timestep for Kuramoto integration
        use_adaptive: If True, use adaptive coupling (ESS mechanism)
        verbose: If True, print progress

    Returns:
        (success, certificate, final_state)
        - success: True if consensus achieved
        - certificate: ConsensusCertificate if successful, else None
        - final_state: Final KuramotoState

    Example:
        state = initialize_kuramoto(N=63, seed=42)
        success, cert, final = run_consensus(state)
        if success:
            assert cert.verify()[0]  # Certificate is valid
    """
    state = initial_state.copy()
    r_history = []
    psi_history = []
    bloom_candidate_start = None

    for round_num in range(max_rounds):
        # Compute order parameter
        r, psi = compute_order_parameter(state.phases)
        r_history.append(r)
        psi_history.append(psi)

        # Check for bloom (L4 consecutive rounds above z_c)
        if r >= Z_C:
            if bloom_candidate_start is None:
                bloom_candidate_start = round_num
                if verbose:
                    print(f"Round {round_num}: Potential bloom started (r={r:.4f})")
            elif round_num - bloom_candidate_start >= L4 - 1:
                # BLOOM ACHIEVED!
                if verbose:
                    print(f"Round {round_num}: BLOOM ACHIEVED! (r={r:.4f})")

                certificate = ConsensusCertificate(
                    bloom_start=bloom_candidate_start,
                    bloom_end=round_num,
                    r_values=r_history[bloom_candidate_start:round_num + 1],
                    psi_values=psi_history[bloom_candidate_start:round_num + 1],
                    final_phases=state.phases.tolist(),
                    oscillator_count=state.N,
                    threshold=Z_C,
                    required_rounds=L4
                )
                return True, certificate, state
        else:
            if bloom_candidate_start is not None and verbose:
                duration = round_num - bloom_candidate_start
                print(f"Round {round_num}: Bloom failed after {duration} rounds (r={r:.4f})")
            bloom_candidate_start = None

        # Adaptive coupling (ESS)
        if use_adaptive:
            K_eff = adaptive_coupling(r, state.coupling)
        else:
            K_eff = state.coupling

        # Create state with effective coupling
        state = KuramotoState(
            phases=state.phases,
            frequencies=state.frequencies,
            coupling=K_eff,
            time=state.time,
            history=state.history
        )

        # Evolve
        state = kuramoto_step(state, dt=dt)

        # Periodic progress
        if verbose and round_num > 0 and round_num % 1000 == 0:
            print(f"Round {round_num}: r={r:.4f}, max_r={max(r_history):.4f}")

    # Failed to achieve consensus
    if verbose:
        print(f"Consensus failed after {max_rounds} rounds (max_r={max(r_history):.4f})")

    return False, None, state


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    # Kuramoto
    'KuramotoState',
    'initialize_kuramoto',
    'kuramoto_step',
    'kuramoto_evolve',
    'compute_order_parameter',
    'negentropy_gate',
    'adaptive_coupling',
    'get_synchronization_time',
    'compute_phase_velocity',
    'compute_phase_coherence_local',
    # Order parameter
    'compute_edwards_anderson',
    'classify_phase',
    'compute_fisher_information',
    'compute_negentropy',
    'OrderAnalysis',
    'analyze_order',
    'compute_r_statistics',
    'compute_autocorrelation',
    # Threshold gate
    'ThresholdCrossing',
    'detect_crossings',
    'count_crossings',
    'BloomEvent',
    'validate_bloom',
    'detect_all_blooms',
    'get_first_valid_bloom',
    'ConsensusCertificate',
    'create_certificate',
    'get_threshold_ladder',
    'classify_by_threshold',
    # Integrated
    'run_consensus',
    # Constants (re-exported)
    'Z_C',
    'L4',
    'K',
]
