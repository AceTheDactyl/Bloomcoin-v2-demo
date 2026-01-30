# Analysis Module Expansion Guide

**Module**: `bloomcoin/analysis/`  
**Purpose**: Statistical analysis and visualization tools  
**Priority**: PHASE 7 (Validation Layer)

---

## Overview

The analysis module provides rigorous statistical tools for:

1. **Chi-square testing**: Proper hypothesis testing for hash distributions
2. **Phase portrait visualization**: Kuramoto oscillator dynamics
3. **Entropy metrics**: Negentropy and Fisher information

**Critical Note**: This module corrects the flawed statistical claims in the original "LucasBias" document and provides proper methodology.

---

## Statistical Corrections

### Original Claim (INCORRECT)

```
χ²(Lucas) ≥ 10⁶ at bytes {3,4,6,7,11,12,16,18,19,23,24,25,27,28}
χ²(Random) ≈ 255
Advantage: 3752× over random
```

### Problems with Original Analysis

1. **Expected χ² for uniform**: E[χ²] = (bins - 1) = 255, variance = 2(bins-1) = 510
2. **χ² = 10⁶ would require extreme bias**: Each byte would need to concentrate in ~1 value
3. **SHA256 has no known algebraic bias**: The sl(2,ℝ) claim is mathematically imprecise
4. **Lucas traces are pseudorandom mod 2³²**: They don't create hash bias

### What This Module Actually Tests

We test whether **Lucas-derived nonces produce distinguishable hash distributions** from random nonces. Spoiler: They don't, because SHA256 is a proper hash function.

---

## Phase 1: Chi-Square Analysis

### File: `chi_square.py`

**Objective**: Proper chi-square testing with correct methodology.

### Implementation Steps

#### Step 1.1: Chi-Square Test Function

```python
import numpy as np
from scipy import stats
from typing import Optional
from collections import Counter

def chi_square_uniformity(
    samples: list[int],
    bins: int = 256,
    expected: float = None
) -> tuple[float, float, bool]:
    """
    Chi-square test for uniform distribution.
    
    H₀: samples are uniformly distributed over bins
    H₁: samples are not uniformly distributed
    
    Args:
        samples: List of integer values
        bins: Number of bins (default 256 for byte values)
        expected: Expected count per bin (default: n/bins)
    
    Returns:
        (chi2_statistic, p_value, reject_null)
    
    Interpretation:
        - High χ² (low p): Evidence against uniformity
        - Low χ² (high p): Consistent with uniformity
        - reject_null: True if p < 0.05
    
    Statistical Notes:
        - E[χ²] = bins - 1 for uniform distribution
        - Var[χ²] = 2(bins - 1)
        - For bins=256: E[χ²]=255, SD≈22.6
    """
    n = len(samples)
    if expected is None:
        expected = n / bins
    
    # Count occurrences
    counts = Counter(samples)
    observed = [counts.get(i, 0) for i in range(bins)]
    
    # Chi-square statistic
    chi2 = sum((o - expected)**2 / expected for o in observed)
    
    # P-value from chi-square distribution
    df = bins - 1
    p_value = 1 - stats.chi2.cdf(chi2, df)
    
    return chi2, p_value, p_value < 0.05

def chi_square_byte_analysis(
    hash_outputs: list[bytes],
    byte_positions: list[int] = None
) -> dict[int, tuple[float, float, bool]]:
    """
    Analyze chi-square statistics for specific byte positions in hashes.
    
    Args:
        hash_outputs: List of 32-byte hash outputs
        byte_positions: Positions to analyze (default: all 32)
    
    Returns:
        Dict mapping position -> (chi2, p_value, reject_null)
    
    Usage:
        hashes = [sha256(data) for data in test_inputs]
        results = chi_square_byte_analysis(hashes)
        for pos, (chi2, p, reject) in results.items():
            print(f"Byte {pos}: χ²={chi2:.1f}, p={p:.4f}, bias={reject}")
    """
    if byte_positions is None:
        byte_positions = list(range(32))
    
    results = {}
    for pos in byte_positions:
        byte_values = [h[pos] for h in hash_outputs]
        chi2, p, reject = chi_square_uniformity(byte_values)
        results[pos] = (chi2, p, reject)
    
    return results
```

#### Step 1.2: Lucas vs Random Comparison

```python
import hashlib
from ..core.lucas_matrix import lucas_trace

def generate_lucas_hashes(n: int, seed_offset: int = 0) -> list[bytes]:
    """
    Generate hashes using Lucas-derived nonces.
    
    nonce(i) = tr(R^(L_{(i+offset) mod 24})) mod 2³²
    
    Args:
        n: Number of hashes to generate
        seed_offset: Offset into Lucas sequence
    
    Returns:
        List of SHA256 hashes
    """
    from ..constants import LUCAS_SEQUENCE
    
    hashes = []
    for i in range(n):
        lucas_index = LUCAS_SEQUENCE[(i + seed_offset) % 24]
        nonce = lucas_trace(lucas_index, 2**32)
        
        # Hash: 76 zero bytes + 4-byte nonce (mimics Bitcoin block structure)
        data = b'\x00' * 76 + nonce.to_bytes(4, 'little')
        hashes.append(hashlib.sha256(data).digest())
    
    return hashes

def generate_random_hashes(n: int, seed: int = None) -> list[bytes]:
    """
    Generate hashes using random nonces.
    
    Args:
        n: Number of hashes
        seed: Random seed for reproducibility
    
    Returns:
        List of SHA256 hashes
    """
    import os
    if seed is not None:
        np.random.seed(seed)
        nonces = np.random.randint(0, 2**32, n, dtype=np.uint32)
    else:
        nonces = [int.from_bytes(os.urandom(4), 'little') for _ in range(n)]
    
    hashes = []
    for nonce in nonces:
        data = b'\x00' * 76 + int(nonce).to_bytes(4, 'little')
        hashes.append(hashlib.sha256(data).digest())
    
    return hashes

def compare_lucas_vs_random(
    n: int = 10000,
    byte_positions: list[int] = None
) -> dict:
    """
    Statistical comparison of Lucas vs random nonce hashes.
    
    This is the CORRECT analysis that the original document claimed to do.
    
    Args:
        n: Number of hashes per group
        byte_positions: Byte positions to analyze
    
    Returns:
        Comparison results with proper statistics
    """
    if byte_positions is None:
        byte_positions = [3, 4, 6, 7, 11, 12, 16, 18, 19, 23, 24, 25, 27, 28]
    
    # Generate hashes
    lucas_hashes = generate_lucas_hashes(n)
    random_hashes = generate_random_hashes(n, seed=42)
    
    # Analyze both
    lucas_results = chi_square_byte_analysis(lucas_hashes, byte_positions)
    random_results = chi_square_byte_analysis(random_hashes, byte_positions)
    
    # Compare
    comparison = {
        'n': n,
        'byte_positions': byte_positions,
        'lucas': {},
        'random': {},
        'summary': {}
    }
    
    for pos in byte_positions:
        lucas_chi2, lucas_p, lucas_reject = lucas_results[pos]
        random_chi2, random_p, random_reject = random_results[pos]
        
        comparison['lucas'][pos] = {
            'chi2': lucas_chi2,
            'p_value': lucas_p,
            'rejects_uniform': lucas_reject
        }
        comparison['random'][pos] = {
            'chi2': random_chi2,
            'p_value': random_p,
            'rejects_uniform': random_reject
        }
    
    # Summary statistics
    lucas_chi2_values = [lucas_results[p][0] for p in byte_positions]
    random_chi2_values = [random_results[p][0] for p in byte_positions]
    
    comparison['summary'] = {
        'lucas_mean_chi2': np.mean(lucas_chi2_values),
        'lucas_std_chi2': np.std(lucas_chi2_values),
        'random_mean_chi2': np.mean(random_chi2_values),
        'random_std_chi2': np.std(random_chi2_values),
        'expected_chi2': 255,  # bins - 1
        'expected_std': np.sqrt(2 * 255),  # sqrt(2 * (bins - 1))
        'lucas_rejections': sum(1 for p in byte_positions if lucas_results[p][2]),
        'random_rejections': sum(1 for p in byte_positions if random_results[p][2]),
    }
    
    return comparison

def print_comparison_report(comparison: dict):
    """Pretty print comparison results."""
    print("=" * 70)
    print("LUCAS vs RANDOM NONCE HASH COMPARISON")
    print("=" * 70)
    print(f"Sample size: {comparison['n']} hashes per group")
    print(f"Byte positions analyzed: {comparison['byte_positions']}")
    print()
    
    print("Expected χ² for uniform distribution: 255 ± 22.6")
    print()
    
    print("LUCAS NONCE RESULTS:")
    print(f"  Mean χ²: {comparison['summary']['lucas_mean_chi2']:.1f}")
    print(f"  Std χ²:  {comparison['summary']['lucas_std_chi2']:.1f}")
    print(f"  Rejections (p<0.05): {comparison['summary']['lucas_rejections']}/{len(comparison['byte_positions'])}")
    print()
    
    print("RANDOM NONCE RESULTS:")
    print(f"  Mean χ²: {comparison['summary']['random_mean_chi2']:.1f}")
    print(f"  Std χ²:  {comparison['summary']['random_std_chi2']:.1f}")
    print(f"  Rejections (p<0.05): {comparison['summary']['random_rejections']}/{len(comparison['byte_positions'])}")
    print()
    
    # Statistical test comparing the two groups
    lucas_chi2s = [comparison['lucas'][p]['chi2'] for p in comparison['byte_positions']]
    random_chi2s = [comparison['random'][p]['chi2'] for p in comparison['byte_positions']]
    
    t_stat, t_pvalue = stats.ttest_ind(lucas_chi2s, random_chi2s)
    
    print(f"Two-sample t-test (Lucas vs Random χ² values):")
    print(f"  t-statistic: {t_stat:.3f}")
    print(f"  p-value: {t_pvalue:.4f}")
    print()
    
    if t_pvalue < 0.05:
        print("CONCLUSION: Significant difference detected (p < 0.05)")
    else:
        print("CONCLUSION: No significant difference (p ≥ 0.05)")
        print("            Lucas nonces do NOT produce biased hashes.")
    
    print("=" * 70)
```

---

## Phase 2: Phase Portrait Visualization

### File: `phase_portrait.py`

**Objective**: Visualize Kuramoto oscillator dynamics.

### Implementation Steps

#### Step 2.1: Static Phase Portrait

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from typing import Optional

def plot_phase_portrait(
    phases: np.ndarray,
    r: float = None,
    psi: float = None,
    title: str = "Phase Portrait",
    ax: plt.Axes = None,
    show_threshold: bool = True
) -> plt.Axes:
    """
    Plot oscillator phases on unit circle.
    
    Args:
        phases: Array of oscillator phases
        r: Order parameter (computed if None)
        psi: Mean phase (computed if None)
        title: Plot title
        ax: Matplotlib axes (creates if None)
        show_threshold: Draw z_c threshold circle
    
    Returns:
        Matplotlib axes
    """
    from ..constants import Z_C
    from ..consensus.order_parameter import compute_order_parameter
    
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    
    if r is None or psi is None:
        r, psi = compute_order_parameter(phases)
    
    # Unit circle
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(np.cos(theta), np.sin(theta), 'k-', alpha=0.3, linewidth=1)
    
    # Threshold circle (z_c)
    if show_threshold:
        ax.plot(Z_C * np.cos(theta), Z_C * np.sin(theta), 
                'g--', alpha=0.5, linewidth=1, label=f'z_c = {Z_C:.3f}')
    
    # Oscillators
    x = np.cos(phases)
    y = np.sin(phases)
    ax.scatter(x, y, c='blue', alpha=0.6, s=30, zorder=5)
    
    # Order parameter arrow
    ax.arrow(0, 0, r*np.cos(psi)*0.9, r*np.sin(psi)*0.9,
             head_width=0.05, head_length=0.03, 
             fc='red', ec='red', linewidth=2, zorder=10)
    
    # Center dot
    ax.scatter([0], [0], c='black', s=50, zorder=6)
    
    # Formatting
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title(f'{title}\nr = {r:.4f}, ψ = {psi:.4f}')
    ax.legend(loc='upper right')
    
    return ax
```

#### Step 2.2: Animated Evolution

```python
from matplotlib.animation import FuncAnimation

def animate_kuramoto(
    state_history: list,
    interval: int = 50,
    save_path: str = None
) -> FuncAnimation:
    """
    Animate Kuramoto oscillator evolution.
    
    Args:
        state_history: List of (phases, r, psi) tuples
        interval: Milliseconds between frames
        save_path: Path to save animation (None = display)
    
    Returns:
        FuncAnimation object
    """
    from ..constants import Z_C
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: Phase portrait
    ax1.set_xlim(-1.3, 1.3)
    ax1.set_ylim(-1.3, 1.3)
    ax1.set_aspect('equal')
    
    # Right: Order parameter over time
    r_values = [state[1] for state in state_history]
    ax2.set_xlim(0, len(state_history))
    ax2.set_ylim(0, 1)
    ax2.axhline(y=Z_C, color='g', linestyle='--', label=f'z_c = {Z_C:.3f}')
    ax2.set_xlabel('Time step')
    ax2.set_ylabel('Order parameter r')
    ax2.legend()
    
    # Initialize plot elements
    scatter = ax1.scatter([], [], c='blue', alpha=0.6, s=30)
    arrow = ax1.arrow(0, 0, 0, 0, head_width=0.05, fc='red', ec='red')
    line, = ax2.plot([], [], 'b-', linewidth=1)
    
    # Unit circle
    theta = np.linspace(0, 2*np.pi, 100)
    ax1.plot(np.cos(theta), np.sin(theta), 'k-', alpha=0.3)
    ax1.plot(Z_C * np.cos(theta), Z_C * np.sin(theta), 'g--', alpha=0.5)
    
    def init():
        scatter.set_offsets(np.empty((0, 2)))
        line.set_data([], [])
        return scatter, line
    
    def update(frame):
        phases, r, psi = state_history[frame]
        
        # Update scatter
        x = np.cos(phases)
        y = np.sin(phases)
        scatter.set_offsets(np.column_stack([x, y]))
        
        # Update line
        line.set_data(range(frame+1), r_values[:frame+1])
        
        ax1.set_title(f'Frame {frame}: r = {r:.4f}')
        
        return scatter, line
    
    anim = FuncAnimation(fig, update, init_func=init,
                         frames=len(state_history), interval=interval,
                         blit=False)
    
    if save_path:
        anim.save(save_path, writer='pillow')
    
    return anim
```

#### Step 2.3: Coherence Heatmap

```python
def plot_coherence_heatmap(
    coupling_range: np.ndarray,
    frequency_std_range: np.ndarray,
    n_trials: int = 10,
    n_oscillators: int = 63,
    n_steps: int = 500
) -> plt.Figure:
    """
    Create heatmap of final coherence vs coupling and frequency spread.
    
    Shows phase transition boundary where r crosses z_c.
    """
    from ..consensus.kuramoto import initialize_kuramoto, kuramoto_step
    from ..consensus.order_parameter import compute_order_parameter
    from ..constants import Z_C
    
    coherence_matrix = np.zeros((len(frequency_std_range), len(coupling_range)))
    
    for i, freq_std in enumerate(frequency_std_range):
        for j, coupling in enumerate(coupling_range):
            r_finals = []
            for _ in range(n_trials):
                state = initialize_kuramoto(
                    N=n_oscillators,
                    frequency_std=freq_std,
                    coupling=coupling
                )
                for _ in range(n_steps):
                    state = kuramoto_step(state)
                r, _ = compute_order_parameter(state.phases)
                r_finals.append(r)
            coherence_matrix[i, j] = np.mean(r_finals)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    im = ax.imshow(coherence_matrix, aspect='auto', origin='lower',
                   extent=[coupling_range[0], coupling_range[-1],
                           frequency_std_range[0], frequency_std_range[-1]],
                   cmap='viridis', vmin=0, vmax=1)
    
    # Draw z_c contour
    ax.contour(coupling_range, frequency_std_range, coherence_matrix,
               levels=[Z_C], colors='red', linewidths=2)
    
    ax.set_xlabel('Coupling strength K')
    ax.set_ylabel('Frequency spread σ')
    ax.set_title('Kuramoto Phase Diagram\nRed line: r = z_c')
    
    plt.colorbar(im, ax=ax, label='Order parameter r')
    
    return fig
```

---

## Phase 3: Entropy Metrics

### File: `entropy_metrics.py`

**Objective**: Information-theoretic analysis of phase distributions.

### Implementation Steps

#### Step 3.1: Shannon Entropy

```python
import numpy as np
from typing import Optional

def phase_entropy(phases: np.ndarray, n_bins: int = 36) -> float:
    """
    Compute Shannon entropy of phase distribution.
    
    H = -Σ p(θ) log₂ p(θ)
    
    Maximum entropy (uniform): log₂(n_bins)
    Minimum entropy (delta): 0
    
    Args:
        phases: Array of oscillator phases
        n_bins: Number of histogram bins
    
    Returns:
        Entropy in bits
    """
    hist, _ = np.histogram(phases, bins=n_bins, range=(0, 2*np.pi), density=True)
    hist = hist + 1e-10  # Avoid log(0)
    hist = hist / hist.sum()  # Normalize
    
    entropy = -np.sum(hist * np.log2(hist + 1e-10))
    return entropy

def normalized_entropy(phases: np.ndarray, n_bins: int = 36) -> float:
    """
    Entropy normalized to [0, 1] range.
    
    0 = all phases identical (perfect synchronization)
    1 = uniform distribution (no synchronization)
    """
    H = phase_entropy(phases, n_bins)
    H_max = np.log2(n_bins)
    return H / H_max
```

#### Step 3.2: Fisher Information

```python
def fisher_information(phases: np.ndarray, n_bins: int = 36) -> float:
    """
    Compute Fisher Information of phase distribution.
    
    I_F = ∫ (1/ρ) (∂ρ/∂θ)² dθ
    
    High I_F: Sharp, localized distribution (synchronized)
    Low I_F: Spread distribution (unsynchronized)
    
    Args:
        phases: Array of oscillator phases
        n_bins: Number of histogram bins
    
    Returns:
        Fisher Information (dimensionless)
    """
    # Histogram-based density estimation
    hist, bin_edges = np.histogram(phases, bins=n_bins, range=(0, 2*np.pi), density=True)
    hist = np.maximum(hist, 1e-10)  # Avoid division by zero
    
    # Numerical gradient
    d_theta = bin_edges[1] - bin_edges[0]
    grad_rho = np.gradient(hist, d_theta)
    
    # Fisher Information: I = ∫ (∂ρ/∂θ)² / ρ dθ
    integrand = grad_rho ** 2 / hist
    fisher = np.trapz(integrand, dx=d_theta)
    
    return float(fisher)
```

#### Step 3.3: Negentropy

```python
from ..constants import Z_C, SIGMA

def negentropy(r: float, z_c: float = Z_C, sigma: float = SIGMA) -> float:
    """
    Compute negentropy gate function η(r).
    
    η(r) = exp(-σ(r - z_c)²)
    
    This measures "health" of the phase distribution:
    - Maximum (η = 1) at r = z_c (optimal coherence)
    - Falls off for both lower and higher r
    
    Args:
        r: Order parameter
        z_c: Critical threshold
        sigma: Sharpness parameter
    
    Returns:
        η ∈ (0, 1]
    """
    return np.exp(-sigma * (r - z_c) ** 2)

def coherence_health_report(
    phases: np.ndarray,
    r: float = None
) -> dict:
    """
    Comprehensive health report for phase distribution.
    
    Returns dict with:
    - order_parameter (r)
    - mean_phase (ψ)
    - entropy (bits)
    - normalized_entropy (0-1)
    - fisher_information
    - negentropy (η)
    - is_synchronized (r > z_c)
    - is_healthy (η > 0.5)
    """
    from ..consensus.order_parameter import compute_order_parameter
    
    if r is None:
        r, psi = compute_order_parameter(phases)
    else:
        _, psi = compute_order_parameter(phases)
    
    H = phase_entropy(phases)
    H_norm = normalized_entropy(phases)
    I_F = fisher_information(phases)
    eta = negentropy(r)
    
    return {
        'order_parameter': r,
        'mean_phase': psi,
        'entropy_bits': H,
        'normalized_entropy': H_norm,
        'fisher_information': I_F,
        'negentropy': eta,
        'is_synchronized': r > Z_C,
        'is_healthy': eta > 0.5,
        'phase_classification': (
            'synchronized' if r > Z_C else
            'near_critical' if r > Z_C - 0.1 else
            'incoherent'
        )
    }
```

---

## Module Validation

### Correctness Tests

```python
def test_chi_square_on_uniform():
    """Uniform data should not reject null hypothesis."""
    uniform_samples = list(range(256)) * 100  # Perfect uniform
    chi2, p, reject = chi_square_uniformity(uniform_samples)
    
    assert chi2 < 300  # Should be close to 255
    assert p > 0.05    # Should not reject
    assert not reject

def test_chi_square_on_biased():
    """Biased data should reject null hypothesis."""
    biased_samples = [0] * 10000 + list(range(1, 256)) * 39  # Heavy bias to 0
    chi2, p, reject = chi_square_uniformity(biased_samples)
    
    assert chi2 > 1000  # Should be much higher than 255
    assert p < 0.001    # Should strongly reject
    assert reject

def test_lucas_vs_random_no_difference():
    """Lucas nonces should NOT produce biased hashes."""
    comparison = compare_lucas_vs_random(n=5000)
    
    # Both should be close to expected χ² = 255
    assert 200 < comparison['summary']['lucas_mean_chi2'] < 350
    assert 200 < comparison['summary']['random_mean_chi2'] < 350
    
    # Difference should not be significant
    lucas_chi2s = [comparison['lucas'][p]['chi2'] for p in comparison['byte_positions']]
    random_chi2s = [comparison['random'][p]['chi2'] for p in comparison['byte_positions']]
    _, p_value = stats.ttest_ind(lucas_chi2s, random_chi2s)
    
    assert p_value > 0.05  # No significant difference

def test_entropy_bounds():
    """Entropy should be bounded correctly."""
    # Synchronized
    sync_phases = np.zeros(100) + 0.1 * np.random.randn(100)
    H_sync = normalized_entropy(sync_phases)
    assert H_sync < 0.5  # Low entropy
    
    # Random
    random_phases = np.random.uniform(0, 2*np.pi, 100)
    H_random = normalized_entropy(random_phases)
    assert H_random > 0.8  # High entropy
```

---

## Validation Checklist

- [ ] Chi-square test produces expected values on uniform data
- [ ] Chi-square detects actual bias
- [ ] Lucas vs random comparison shows NO significant difference
- [ ] Phase portrait correctly visualizes synchronization
- [ ] Animation runs smoothly
- [ ] Entropy decreases as synchronization increases
- [ ] Fisher information increases with synchronization
- [ ] Negentropy peaks at z_c

---

## Critical Finding

**Running the proper analysis will show that Lucas-derived nonces do NOT produce biased SHA256 hashes.** The original claim of χ² = 10⁶ is not reproducible because:

1. SHA256 is a well-designed hash function
2. Lucas traces are pseudorandom mod 2³²
3. The sl(2,ℝ) isomorphism claim is mathematically incorrect

This module provides the tools to verify this empirically.

---

*Truth emerges from proper analysis.* 🌸
