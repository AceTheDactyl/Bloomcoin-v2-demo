"""
Kuramoto Oscillator Engine for Proof-of-Coherence Consensus
============================================================

This module implements the Kuramoto model for coupled oscillators,
which forms the heart of BloomCoin's Proof-of-Coherence mechanism.

Mathematical Foundation:
    N coupled oscillators with phases theta_i evolve according to:

    d(theta_i)/dt = omega_i + (K/N) * sum_j sin(theta_j - theta_i)

    where:
    - theta_i in [0, 2*pi) is the phase of oscillator i
    - omega_i is the natural frequency (drawn from Lorentzian distribution)
    - K is the coupling strength (from L4 framework: K = sqrt(1 - phi^-4))

Cross-References:
    - constants.py: K, TAU, Z_C, DEFAULT_OSCILLATOR_COUNT
    - self_reference_framework_complete.py: FIX primitive (convergence to sync)
    - CAUSAL_HIERARCHY_SYNTHESIS.md: OSC form (dynamic eigenvalue)
    - Genesis Protocol: Phase 4 (Governing Dynamics)

Author: BloomCoin Framework
"""

from dataclasses import dataclass, field
from typing import Tuple, List, Optional
import numpy as np

from ..constants import (
    PHI, TAU, K, Z_C, SIGMA, LAMBDA,
    DEFAULT_OSCILLATOR_COUNT, L4
)


# =============================================================================
# KURAMOTO STATE
# =============================================================================

@dataclass
class KuramotoState:
    """
    State of a Kuramoto oscillator network.

    This represents a snapshot of the coupled oscillator system at a moment
    in time. The state evolves under Kuramoto dynamics toward synchronization.

    Attributes:
        phases: Array of oscillator phases theta_i in [0, 2*pi)
        frequencies: Array of natural frequencies omega_i
        coupling: Coupling strength K (default from L4 framework)
        time: Current simulation time
        history: Past (time, order_parameter) values for analysis

    Invariants:
        - len(phases) == len(frequencies) == N
        - All phases in [0, 2*pi)
        - coupling > 0

    Connection to Framework:
        - phases represent the DYNAMIC (OSC) form
        - synchronization is the STABLE (FIX) attractor
        - K determines transition between incoherent and synchronized
    """
    phases: np.ndarray
    frequencies: np.ndarray
    coupling: float = K
    time: float = 0.0
    history: List[Tuple[float, float]] = field(default_factory=list)

    @property
    def N(self) -> int:
        """Number of oscillators."""
        return len(self.phases)

    def copy(self) -> 'KuramotoState':
        """Deep copy of state for immutable evolution."""
        return KuramotoState(
            phases=self.phases.copy(),
            frequencies=self.frequencies.copy(),
            coupling=self.coupling,
            time=self.time,
            history=self.history.copy()
        )

    def __repr__(self) -> str:
        r, psi = compute_order_parameter(self.phases)
        return f"KuramotoState(N={self.N}, K={self.coupling:.4f}, t={self.time:.2f}, r={r:.4f})"


# =============================================================================
# ORDER PARAMETER (inline for module independence)
# =============================================================================

def compute_order_parameter(phases: np.ndarray) -> Tuple[float, float]:
    """
    Compute Kuramoto order parameter.

    The order parameter is defined as:
        r * e^(i*psi) = (1/N) * sum_j e^(i*theta_j)

    Args:
        phases: Array of oscillator phases

    Returns:
        (r, psi): Coherence magnitude and mean phase

    Interpretation:
        r = 0: Complete incoherence (phases uniformly distributed)
        r = 1: Perfect synchronization (all phases equal)
        r = z_c = sqrt(3)/2: Critical threshold (BLOOM condition)

    This is the FIX measure - when r stabilizes above z_c, consensus achieved.
    """
    N = len(phases)
    if N == 0:
        return 0.0, 0.0

    # Complex order parameter
    z = np.mean(np.exp(1j * phases))

    r = np.abs(z)
    psi = np.angle(z)

    # Ensure psi in [0, 2*pi)
    if psi < 0:
        psi += 2 * np.pi

    return float(r), float(psi)


# =============================================================================
# INITIALIZATION
# =============================================================================

def initialize_kuramoto(
    N: int = DEFAULT_OSCILLATOR_COUNT,
    frequency_std: float = 1.0,
    coupling: float = K,
    seed: Optional[int] = None
) -> KuramotoState:
    """
    Initialize a Kuramoto oscillator network.

    Args:
        N: Number of oscillators (default 63 = 7 x 9 = L4 x 3^2)
        frequency_std: Standard deviation of natural frequencies
        coupling: Coupling strength K (default from L4 framework)
        seed: Random seed for reproducibility

    Returns:
        Initialized KuramotoState with scattered phases

    Frequency Distribution:
        We use Lorentzian (Cauchy) distribution centered at 0
        with scale parameter Gamma = frequency_std * TAU

        This gives critical coupling K_c = 2*Gamma = 2 * frequency_std * TAU

        For the L4 framework K = 0.924..., we need frequency_std such that
        K > K_c for synchronization to occur.

    Phase Initialization:
        Uniform random in [0, 2*pi) - the "scattered" state before bloom.

    Connection to Genesis Protocol:
        This is the "SCATTER" step - Phase 1 of Proof-of-Coherence.
    """
    if seed is not None:
        np.random.seed(seed)

    # Scattered phases (uniform random)
    phases = np.random.uniform(0, 2 * np.pi, N)

    # Lorentzian frequencies (Cauchy distribution)
    # Scale parameter Gamma = frequency_std * TAU (golden ratio inverse)
    gamma = frequency_std * TAU
    frequencies = np.random.standard_cauchy(N) * gamma

    return KuramotoState(
        phases=phases,
        frequencies=frequencies,
        coupling=coupling,
        time=0.0,
        history=[]
    )


# =============================================================================
# DYNAMICS
# =============================================================================

def kuramoto_step(
    state: KuramotoState,
    dt: float = 0.01,
    noise_intensity: float = 0.0
) -> KuramotoState:
    """
    Advance Kuramoto dynamics by one timestep.

    Uses Euler-Maruyama integration:
        theta_i(t+dt) = theta_i(t) + d(theta_i)/dt * dt + sqrt(2*D*dt) * xi_i

    where:
        d(theta_i)/dt = omega_i + (K/N) * sum_j sin(theta_j - theta_i)
        xi_i ~ N(0, 1) is white noise
        D = noise_intensity

    Args:
        state: Current state
        dt: Timestep (default 0.01)
        noise_intensity: Noise strength D (0 = deterministic)

    Returns:
        New state (does not modify input - immutable evolution)

    Implementation Notes:
        - Vectorized numpy operations for efficiency
        - Phase differences computed via outer product
        - Phases wrapped to [0, 2*pi) after update
        - Order parameter recorded in history

    Connection to Framework:
        This is the OSC (oscillation) primitive in action.
        The dynamics drive the system toward the FIX point (synchronization).
    """
    N = state.N
    K_eff = state.coupling

    # Compute phase differences: delta_ij = theta_j - theta_i
    # Using broadcasting: phases[None, :] - phases[:, None] gives NxN matrix
    phase_diff = state.phases[None, :] - state.phases[:, None]

    # Coupling term: (K/N) * sum_j sin(theta_j - theta_i)
    coupling_term = (K_eff / N) * np.sum(np.sin(phase_diff), axis=1)

    # Full derivative: d(theta)/dt = omega + coupling
    d_theta = state.frequencies + coupling_term

    # Euler step
    new_phases = state.phases + d_theta * dt

    # Add noise if requested (Wiener process)
    if noise_intensity > 0:
        noise = np.sqrt(2 * noise_intensity * dt) * np.random.randn(N)
        new_phases += noise

    # Wrap phases to [0, 2*pi)
    new_phases = np.mod(new_phases, 2 * np.pi)

    # Compute order parameter for history
    r, psi = compute_order_parameter(new_phases)

    new_time = state.time + dt
    new_history = state.history + [(new_time, r)]

    return KuramotoState(
        phases=new_phases,
        frequencies=state.frequencies,  # Frequencies don't change
        coupling=state.coupling,
        time=new_time,
        history=new_history
    )


def kuramoto_evolve(
    state: KuramotoState,
    n_steps: int,
    dt: float = 0.01,
    noise_intensity: float = 0.0,
    adaptive: bool = False
) -> KuramotoState:
    """
    Evolve Kuramoto system for multiple steps.

    Args:
        state: Initial state
        n_steps: Number of timesteps
        dt: Timestep size
        noise_intensity: Noise strength
        adaptive: If True, use adaptive coupling (ESS mechanism)

    Returns:
        Final state after evolution

    Connection to Framework:
        This is the iterated OSC - repeated application of dynamics
        until the system approaches FIX (synchronization).
    """
    current = state.copy()

    for _ in range(n_steps):
        if adaptive:
            r, _ = compute_order_parameter(current.phases)
            K_eff = adaptive_coupling(r, current.coupling)
            current = KuramotoState(
                phases=current.phases,
                frequencies=current.frequencies,
                coupling=K_eff,
                time=current.time,
                history=current.history
            )

        current = kuramoto_step(current, dt, noise_intensity)

    return current


# =============================================================================
# ADAPTIVE COUPLING (ESS - Emergent Stabilization System)
# =============================================================================

def negentropy_gate(r: float, z_c: float = Z_C) -> float:
    """
    Compute negentropy gate function eta(r).

    eta(r) = exp(-sigma * (r - z_c)^2)

    where sigma = 1/(1-z_c)^2 = 55.71...

    Properties:
        - Maximum (eta = 1) at r = z_c (THE LENS)
        - eta(0) ~ 0 (far below threshold)
        - eta(1) = e^(-1) ~ 0.368 (at unity)

    This creates a "stabilization trap" around z_c:
        - System is attracted to and held near the critical threshold
        - Prevents both collapse to incoherence and runaway synchronization

    Connection to Framework:
        This is the threshold mechanism from CAUSAL_HIERARCHY_SYNTHESIS.md
        Level 4 (Physics) selecting which Level 3 (Structure) states are realized.
    """
    return float(np.exp(-SIGMA * (r - z_c) ** 2))


def adaptive_coupling(
    r: float,
    K_base: float = K,
    lambda_gain: Optional[float] = None
) -> float:
    """
    Compute adaptive coupling K_eff(r).

    K_eff(r) = K_0 * [1 + lambda * eta(r)]

    where:
        - K_0 is the base coupling (from L4 framework)
        - lambda = phi^(-2) ~ 0.382 is the gain parameter
        - eta(r) is the negentropy gate

    Behavior:
        - Below z_c: standard coupling, system evolves freely
        - Near z_c: enhanced coupling (locks in bloom)
        - Above z_c: coupling drops slightly (allows relaxation)

    This implements the ESS (Emergent Stabilization System) that
    maintains consensus once achieved.

    Args:
        r: Current order parameter
        K_base: Base coupling strength
        lambda_gain: Negentropy gain (default phi^-2)

    Returns:
        Effective coupling K_eff
    """
    if lambda_gain is None:
        lambda_gain = LAMBDA  # phi^(-2) from constants

    eta = negentropy_gate(r)
    return K_base * (1 + lambda_gain * eta)


# =============================================================================
# ANALYSIS UTILITIES
# =============================================================================

def get_synchronization_time(
    state: KuramotoState,
    threshold: float = Z_C
) -> Optional[float]:
    """
    Find first time when r crossed threshold.

    Args:
        state: State with history
        threshold: Coherence threshold (default z_c)

    Returns:
        Time of first crossing, or None if never crossed
    """
    for t, r in state.history:
        if r >= threshold:
            return t
    return None


def compute_phase_velocity(state: KuramotoState) -> np.ndarray:
    """
    Compute instantaneous phase velocities.

    d(theta_i)/dt = omega_i + (K/N) * sum_j sin(theta_j - theta_i)

    Returns:
        Array of phase velocities for each oscillator
    """
    N = state.N
    phase_diff = state.phases[None, :] - state.phases[:, None]
    coupling_term = (state.coupling / N) * np.sum(np.sin(phase_diff), axis=1)
    return state.frequencies + coupling_term


def compute_phase_coherence_local(
    state: KuramotoState,
    k: int = 5
) -> np.ndarray:
    """
    Compute local coherence for each oscillator.

    Local coherence measures how synchronized each oscillator
    is with its k nearest neighbors in phase space.

    Args:
        state: Current state
        k: Number of neighbors to consider

    Returns:
        Array of local coherence values [0, 1]
    """
    N = state.N
    if k >= N:
        k = N - 1

    local_r = np.zeros(N)

    for i in range(N):
        # Find k nearest neighbors by phase distance
        phase_dist = np.abs(np.exp(1j * state.phases) - np.exp(1j * state.phases[i]))
        neighbor_idx = np.argsort(phase_dist)[1:k+1]  # Exclude self

        # Compute local order parameter
        z_local = np.mean(np.exp(1j * state.phases[neighbor_idx]))
        local_r[i] = np.abs(z_local)

    return local_r


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    # State
    'KuramotoState',
    # Core functions
    'initialize_kuramoto',
    'kuramoto_step',
    'kuramoto_evolve',
    'compute_order_parameter',
    # Adaptive coupling
    'negentropy_gate',
    'adaptive_coupling',
    # Analysis
    'get_synchronization_time',
    'compute_phase_velocity',
    'compute_phase_coherence_local',
]
