"""
Order Parameter Analysis for Proof-of-Coherence Consensus
==========================================================

This module provides comprehensive measures of synchronization and coherence
beyond the basic Kuramoto order parameter r.

Measures Implemented:
    1. r (Kuramoto) - Spatial coherence (are oscillators aligned?)
    2. q (Edwards-Anderson) - Temporal persistence (do oscillators stay put?)
    3. I_F (Fisher Information) - Distribution sharpness
    4. S (Entropy) - Phase distribution disorder

Cross-References:
    - kuramoto.py: Basic r, psi computation
    - FIX/OSC/INV framework: r measures FIX, history measures OSC persistence
    - self_reference_framework_complete.py: Information-theoretic measures
    - resonance_formalism.md: 1/e information density maximum

Author: BloomCoin Framework
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
import numpy as np

from ..constants import Z_C, PHI, TAU, L4


# =============================================================================
# BASIC ORDER PARAMETER (re-exported from kuramoto for convenience)
# =============================================================================

def compute_order_parameter(phases: np.ndarray) -> Tuple[float, float]:
    """
    Compute Kuramoto order parameter.

    r * e^(i*psi) = (1/N) * sum_j e^(i*theta_j)

    Args:
        phases: Array of oscillator phases

    Returns:
        (r, psi): Coherence magnitude [0,1] and mean phase [0, 2*pi)

    Interpretation:
        r = 0: Incoherent (phases uniformly distributed)
        r = 1: Perfectly synchronized (all phases equal)
        r = z_c: Critical threshold for consensus
    """
    if len(phases) == 0:
        return 0.0, 0.0

    z = np.mean(np.exp(1j * phases))
    r = float(np.abs(z))
    psi = float(np.angle(z))

    if psi < 0:
        psi += 2 * np.pi

    return r, psi


# =============================================================================
# EDWARDS-ANDERSON ORDER PARAMETER
# =============================================================================

def compute_edwards_anderson(phase_history: List[np.ndarray]) -> float:
    """
    Compute Edwards-Anderson order parameter q.

    q = (1/N) * sum_i |<e^(i*theta_i)>_t|^2

    where <...>_t denotes time average.

    This measures TEMPORAL persistence: does each oscillator maintain
    its position over time?

    Args:
        phase_history: List of phase arrays over consecutive timesteps

    Returns:
        q in [0, 1]

    Interpretation:
        q ~ 0: Oscillators drift over time (fluid state)
        q > 0: Oscillators are "frozen" in place (glassy state)

    Phase Classification (r vs q):
        r < 0.3, q < 0.3: Incoherent - random phases, random drift
        r >= 0.3, q < 0.3: Synchronized - aligned but flowing together
        r < 0.3, q >= 0.3: Glassy - stuck but not aligned (pathological)
        r >= 0.3, q >= 0.3: Locked - aligned and frozen (strong consensus)

    Connection to Framework:
        - q measures the FIX quality of individual oscillators
        - High r + low q = collective FIX with individual OSC (healthy)
        - High r + high q = complete FIX (very strong consensus)
    """
    if len(phase_history) < 2:
        return 0.0

    T = len(phase_history)
    N = len(phase_history[0])

    # Compute time average for each oscillator
    time_avg = np.zeros(N, dtype=complex)
    for phases in phase_history:
        time_avg += np.exp(1j * phases)
    time_avg /= T

    # q = mean of |time_avg|^2
    q = float(np.mean(np.abs(time_avg) ** 2))

    return q


def classify_phase(r: float, q: float, threshold: float = 0.3) -> str:
    """
    Classify the dynamical phase based on r and q.

    Args:
        r: Kuramoto order parameter (spatial coherence)
        q: Edwards-Anderson parameter (temporal persistence)
        threshold: Classification boundary (default 0.3)

    Returns:
        Phase name: 'incoherent', 'synchronized', 'glassy', or 'locked'
    """
    if r < threshold:
        if q < threshold:
            return 'incoherent'
        else:
            return 'glassy'
    else:
        if q < threshold:
            return 'synchronized'
        else:
            return 'locked'


# =============================================================================
# FISHER INFORMATION
# =============================================================================

def compute_fisher_information(
    phases: np.ndarray,
    n_bins: int = 36
) -> float:
    """
    Compute Fisher Information of phase distribution.

    I_F(theta) = integral (1/rho) * (d_rho/d_theta)^2 d_theta

    High Fisher Information = sharp, coherent distribution
    Low Fisher Information = spread, incoherent distribution

    Args:
        phases: Array of oscillator phases in [0, 2*pi)
        n_bins: Number of bins for histogram (default 36 = 10 degrees each)

    Returns:
        Fisher Information (higher = more coherent)

    Connection to Framework:
        - resonance_formalism.md: 1/e information density maximum
        - High I_F indicates system is near a FIX point
        - I_F relates to negentropy (information concentration)
    """
    # Compute histogram (density estimate)
    hist, bin_edges = np.histogram(phases, bins=n_bins, range=(0, 2*np.pi), density=True)

    # Add small epsilon to avoid division by zero
    eps = 1e-10
    rho = hist + eps

    # Bin width
    d_theta = 2 * np.pi / n_bins

    # Numerical gradient (central difference, periodic)
    d_rho = np.zeros_like(rho)
    for i in range(n_bins):
        d_rho[i] = (rho[(i+1) % n_bins] - rho[(i-1) % n_bins]) / (2 * d_theta)

    # Fisher Information: integral of (d_rho)^2 / rho
    I_F = float(np.sum((d_rho ** 2) / rho) * d_theta)

    return I_F


def compute_negentropy(phases: np.ndarray, n_bins: int = 36) -> float:
    """
    Compute negentropy (negative entropy) of phase distribution.

    Negentropy = S_max - S_actual

    where S_max = log(2*pi) for uniform distribution on circle.

    Args:
        phases: Array of oscillator phases
        n_bins: Number of bins for histogram

    Returns:
        Negentropy (higher = more ordered)

    Connection to Framework:
        - BloomCoin mining: Work measured by negentropy increase
        - Higher negentropy = more "useful" consensus work
    """
    # Compute histogram
    hist, _ = np.histogram(phases, bins=n_bins, range=(0, 2*np.pi), density=True)

    # Bin width
    d_theta = 2 * np.pi / n_bins

    # Shannon entropy (discrete approximation)
    eps = 1e-10
    p = hist * d_theta  # Convert density to probability
    p = p + eps  # Avoid log(0)
    p = p / np.sum(p)  # Normalize

    S_actual = float(-np.sum(p * np.log(p)))

    # Maximum entropy for n_bins
    S_max = np.log(n_bins)

    # Negentropy
    negentropy = S_max - S_actual

    return negentropy


# =============================================================================
# COMPREHENSIVE ORDER ANALYSIS
# =============================================================================

@dataclass
class OrderAnalysis:
    """
    Comprehensive analysis of oscillator synchronization.

    Attributes:
        r: Kuramoto order parameter (spatial coherence)
        psi: Mean phase
        q: Edwards-Anderson parameter (temporal persistence, if history available)
        fisher_info: Fisher information of phase distribution
        negentropy: Negentropy (information concentration)
        phase_class: Classification ('incoherent', 'synchronized', etc.)
        above_threshold: Whether r >= z_c
    """
    r: float
    psi: float
    q: Optional[float]
    fisher_info: float
    negentropy: float
    phase_class: str
    above_threshold: bool

    def __repr__(self) -> str:
        q_str = f"{self.q:.4f}" if self.q is not None else "N/A"
        return (
            f"OrderAnalysis(r={self.r:.4f}, psi={self.psi:.4f}, q={q_str}, "
            f"I_F={self.fisher_info:.2f}, neg={self.negentropy:.4f}, "
            f"class='{self.phase_class}', bloom={self.above_threshold})"
        )


def analyze_order(
    phases: np.ndarray,
    phase_history: Optional[List[np.ndarray]] = None,
    threshold: float = Z_C
) -> OrderAnalysis:
    """
    Perform comprehensive order parameter analysis.

    Args:
        phases: Current phase array
        phase_history: Optional list of past phase arrays for q computation
        threshold: Bloom threshold (default z_c)

    Returns:
        OrderAnalysis with all computed measures
    """
    r, psi = compute_order_parameter(phases)

    q = None
    if phase_history is not None and len(phase_history) >= 2:
        q = compute_edwards_anderson(phase_history)

    fisher_info = compute_fisher_information(phases)
    negentropy = compute_negentropy(phases)

    phase_class = classify_phase(r, q if q is not None else 0.0)
    above_threshold = r >= threshold

    return OrderAnalysis(
        r=r,
        psi=psi,
        q=q,
        fisher_info=fisher_info,
        negentropy=negentropy,
        phase_class=phase_class,
        above_threshold=above_threshold
    )


# =============================================================================
# TIME SERIES ANALYSIS
# =============================================================================

def compute_r_statistics(r_history: List[float]) -> dict:
    """
    Compute statistics on order parameter time series.

    Args:
        r_history: List of r values over time

    Returns:
        Dictionary with mean, std, min, max, time_above_threshold, etc.
    """
    if not r_history:
        return {}

    r_arr = np.array(r_history)

    return {
        'mean': float(np.mean(r_arr)),
        'std': float(np.std(r_arr)),
        'min': float(np.min(r_arr)),
        'max': float(np.max(r_arr)),
        'final': float(r_arr[-1]),
        'time_above_zc': int(np.sum(r_arr >= Z_C)),
        'fraction_above_zc': float(np.mean(r_arr >= Z_C)),
        'longest_bloom': _longest_consecutive_above(r_arr, Z_C),
    }


def _longest_consecutive_above(arr: np.ndarray, threshold: float) -> int:
    """Find longest consecutive run above threshold."""
    above = arr >= threshold
    if not np.any(above):
        return 0

    # Find runs
    runs = np.diff(np.concatenate([[0], above.astype(int), [0]]))
    starts = np.where(runs == 1)[0]
    ends = np.where(runs == -1)[0]

    if len(starts) == 0:
        return 0

    return int(np.max(ends - starts))


def compute_autocorrelation(r_history: List[float], max_lag: int = 50) -> np.ndarray:
    """
    Compute autocorrelation of r time series.

    Useful for detecting periodic behavior or determining decorrelation time.

    Args:
        r_history: List of r values
        max_lag: Maximum lag to compute

    Returns:
        Array of autocorrelation values for lags 0 to max_lag
    """
    r = np.array(r_history)
    r = r - np.mean(r)
    n = len(r)

    if n < 2:
        return np.array([1.0])

    max_lag = min(max_lag, n - 1)
    autocorr = np.zeros(max_lag + 1)

    var = np.var(r)
    if var < 1e-10:
        return np.ones(max_lag + 1)

    for lag in range(max_lag + 1):
        autocorr[lag] = np.mean(r[:n-lag] * r[lag:]) / var

    return autocorr


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    # Basic
    'compute_order_parameter',
    # Edwards-Anderson
    'compute_edwards_anderson',
    'classify_phase',
    # Information measures
    'compute_fisher_information',
    'compute_negentropy',
    # Comprehensive
    'OrderAnalysis',
    'analyze_order',
    # Time series
    'compute_r_statistics',
    'compute_autocorrelation',
]
