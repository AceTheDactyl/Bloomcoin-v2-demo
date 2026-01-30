# Consensus Module Expansion Guide

**Module**: `bloomcoin/consensus/`  
**Purpose**: Kuramoto-based Proof-of-Coherence consensus mechanism  
**Priority**: PHASE 2 (Core Algorithm)

---

## Overview

The consensus module implements the heart of BloomCoin: **Proof-of-Coherence (PoC)**. Instead of Proof-of-Work's energy expenditure or Proof-of-Stake's capital lockup, PoC requires miners to achieve phase synchronization among a network of coupled oscillators.

**Key Insight**: Consensus is a phase transition. When the Kuramoto order parameter r crosses the critical threshold z_c = √3/2, the network "blooms" into agreement.

---

## Mathematical Foundation

### The Kuramoto Model

N coupled oscillators with phases θᵢ evolve according to:

```
dθᵢ/dt = ωᵢ + (K/N) Σⱼ sin(θⱼ - θᵢ)
```

where:
- θᵢ ∈ [0, 2π) is the phase of oscillator i
- ωᵢ is the natural frequency (drawn from distribution g(ω))
- K is the coupling strength
- The sum is over all oscillators j

### Order Parameter

The collective synchronization is measured by:

```
r · e^(iψ) = (1/N) Σⱼ e^(iθⱼ)
```

where:
- r ∈ [0, 1] is the **coherence magnitude**
- ψ is the **mean phase**

### Critical Transition

For a Lorentzian frequency distribution with width Γ:

```
K_c = 2Γ (critical coupling)

r = 0           if K < K_c (incoherent)
r = √(1 - K_c/K) if K > K_c (synchronized)
```

### BloomCoin Threshold

We use the L₄ framework threshold:

```
z_c = √3/2 ≈ 0.8660254037844386
```

**Consensus achieved when r ≥ z_c for L₄ = 7 consecutive rounds.**

---

## Phase 1: Kuramoto Engine

### File: `kuramoto.py`

**Objective**: Implement the Kuramoto oscillator dynamics.

### Implementation Steps

#### Step 1.1: Oscillator State

```python
from dataclasses import dataclass, field
import numpy as np
from ..constants import PHI, TAU, K, Z_C, L4, DEFAULT_OSCILLATOR_COUNT

@dataclass
class KuramotoState:
    """
    State of a Kuramoto oscillator network.
    
    Attributes:
        phases: Array of oscillator phases θᵢ ∈ [0, 2π)
        frequencies: Array of natural frequencies ωᵢ
        coupling: Coupling strength K
        time: Current simulation time
        history: Past order parameter values
    
    Invariants:
        - len(phases) == len(frequencies) == N
        - All phases in [0, 2π)
        - coupling > 0
    """
    phases: np.ndarray
    frequencies: np.ndarray
    coupling: float = K
    time: float = 0.0
    history: list[tuple[float, float]] = field(default_factory=list)
    
    @property
    def N(self) -> int:
        return len(self.phases)
    
    def copy(self) -> 'KuramotoState':
        """Deep copy of state."""
        return KuramotoState(
            phases=self.phases.copy(),
            frequencies=self.frequencies.copy(),
            coupling=self.coupling,
            time=self.time,
            history=self.history.copy()
        )
```

#### Step 1.2: Initialization

```python
def initialize_kuramoto(
    N: int = DEFAULT_OSCILLATOR_COUNT,
    frequency_std: float = 1.0,
    coupling: float = K,
    seed: int | None = None
) -> KuramotoState:
    """
    Initialize a Kuramoto network.
    
    Args:
        N: Number of oscillators (default 63 = 7 × 9)
        frequency_std: Standard deviation of natural frequencies
        coupling: Coupling strength K
        seed: Random seed for reproducibility
    
    Returns:
        Initialized KuramotoState
    
    Frequency Distribution:
        We use Lorentzian (Cauchy) distribution centered at 0
        with scale parameter Γ = frequency_std * τ
        
        This gives critical coupling K_c = 2Γ = 2 * frequency_std * τ
    
    Phase Initialization:
        Uniform random in [0, 2π) — the "scattered" state
    """
    # YOUR IMPLEMENTATION HERE
    pass
```

#### Step 1.3: Dynamics Step

```python
def kuramoto_step(
    state: KuramotoState,
    dt: float = 0.01,
    noise_intensity: float = 0.0
) -> KuramotoState:
    """
    Advance Kuramoto dynamics by one timestep.
    
    Uses Euler-Maruyama integration:
        θᵢ(t+dt) = θᵢ(t) + dθᵢ/dt · dt + √(2D·dt) · ξᵢ
    
    where:
        dθᵢ/dt = ωᵢ + (K/N) Σⱼ sin(θⱼ - θᵢ)
        ξᵢ ~ N(0, 1) is white noise
        D = noise_intensity
    
    Args:
        state: Current state
        dt: Timestep
        noise_intensity: Noise strength D (0 = deterministic)
    
    Returns:
        New state (does not modify input)
    
    Implementation Notes:
        - Use vectorized numpy operations
        - Compute all phase differences as outer product
        - Apply mod 2π after update
        - Record order parameter in history
    """
    # YOUR IMPLEMENTATION HERE
    pass
```

#### Step 1.4: Adaptive Coupling (ESS)

```python
def negentropy_gate(r: float, z_c: float = Z_C) -> float:
    """
    Compute negentropy gate function η(r).
    
    η(r) = exp(-σ(r - z_c)²)
    
    where σ = 1/(1-z_c)² ≈ 55.71
    
    Properties:
        - Maximum (η = 1) at r = z_c
        - η(0) ≈ 0 (far below threshold)
        - η(1) = e⁻¹ ≈ 0.368 (at unity)
    """
    from ..constants import SIGMA
    return np.exp(-SIGMA * (r - z_c) ** 2)

def adaptive_coupling(
    r: float,
    K_base: float = K,
    lambda_gain: float = None
) -> float:
    """
    Compute adaptive coupling K_eff(r).
    
    K_eff(r) = K₀ · [1 + λ · η(r)]
    
    This creates a "stabilization trap" around z_c:
        - Below z_c: standard coupling
        - Near z_c: enhanced coupling (locks in)
        - Above z_c: coupling drops (allows relaxation)
    
    Args:
        r: Current order parameter
        K_base: Base coupling strength
        lambda_gain: Negentropy gain (default φ⁻²)
    
    Returns:
        Effective coupling K_eff
    """
    from ..constants import LAMBDA
    if lambda_gain is None:
        lambda_gain = LAMBDA
    
    eta = negentropy_gate(r)
    return K_base * (1 + lambda_gain * eta)
```

### Test Cases

```python
def test_initialization():
    state = initialize_kuramoto(N=63, seed=42)
    assert state.N == 63
    assert len(state.phases) == 63
    assert all(0 <= p < 2*np.pi for p in state.phases)

def test_deterministic_evolution():
    state1 = initialize_kuramoto(N=10, seed=42)
    state2 = initialize_kuramoto(N=10, seed=42)
    
    for _ in range(100):
        state1 = kuramoto_step(state1, noise_intensity=0)
        state2 = kuramoto_step(state2, noise_intensity=0)
    
    np.testing.assert_array_almost_equal(state1.phases, state2.phases)

def test_synchronization():
    # High coupling should synchronize
    state = initialize_kuramoto(N=63, coupling=2.0, seed=42)
    
    for _ in range(1000):
        state = kuramoto_step(state)
    
    r, _ = compute_order_parameter(state.phases)
    assert r > 0.9  # Should be highly synchronized
```

---

## Phase 2: Order Parameter Computation

### File: `order_parameter.py`

**Objective**: Compute r, ψ, and related quantities.

### Implementation Steps

#### Step 2.1: Basic Order Parameter

```python
def compute_order_parameter(phases: np.ndarray) -> tuple[float, float]:
    """
    Compute Kuramoto order parameter.
    
    r · e^(iψ) = (1/N) Σⱼ e^(iθⱼ)
    
    Args:
        phases: Array of oscillator phases
    
    Returns:
        (r, psi): Coherence magnitude and mean phase
    
    Interpretation:
        r = 0: Complete incoherence (phases uniformly distributed)
        r = 1: Perfect synchronization (all phases equal)
    """
    # YOUR IMPLEMENTATION HERE
    pass
```

#### Step 2.2: Edwards-Anderson Parameter

```python
def compute_edwards_anderson(phase_history: list[np.ndarray]) -> float:
    """
    Compute Edwards-Anderson order parameter q.
    
    q = (1/N) Σᵢ |⟨e^(iθᵢ)⟩_t|²
    
    This measures TEMPORAL persistence (does each oscillator stay put?)
    vs r which measures SPATIAL coherence (are oscillators aligned?)
    
    Args:
        phase_history: List of phase arrays over time
    
    Returns:
        q ∈ [0, 1]
    
    Interpretation:
        q ≈ 0: Oscillators drift over time
        q > 0: Oscillators are "frozen" (glassy state)
    
    Phase Classification:
        r < 0.3, q < 0.3: Incoherent
        r ≥ 0.3, q < 0.3: Synchronized (healthy consensus)
        r < 0.3, q ≥ 0.3: Glassy (stuck, bad)
        r ≥ 0.3, q ≥ 0.3: Mixed
    """
    # YOUR IMPLEMENTATION HERE
    pass
```

#### Step 2.3: Fisher Information

```python
def compute_fisher_information(phases: np.ndarray, n_bins: int = 36) -> float:
    """
    Compute Fisher Information of phase distribution.
    
    I_F(θ) = ∫ (1/ρ) (∂ρ/∂θ)² dθ
    
    High Fisher Information = sharp, coherent distribution
    Low Fisher Information = spread, incoherent distribution
    
    Args:
        phases: Array of oscillator phases
        n_bins: Number of bins for histogram
    
    Returns:
        Fisher Information (higher = more coherent)
    
    Implementation:
        1. Compute histogram ρ(θ) using n_bins
        2. Compute numerical gradient ∂ρ/∂θ
        3. Integrate (∂ρ/∂θ)² / ρ
    """
    # YOUR IMPLEMENTATION HERE
    pass
```

---

## Phase 3: Threshold Gate

### File: `threshold_gate.py`

**Objective**: Detect when r crosses z_c and validate consensus.

### Implementation Steps

#### Step 3.1: Crossing Detection

```python
@dataclass
class ThresholdCrossing:
    """
    Record of a threshold crossing event.
    
    Attributes:
        time: When the crossing occurred
        direction: 'up' or 'down'
        r_before: Order parameter before crossing
        r_after: Order parameter after crossing
        threshold: The threshold crossed
    """
    time: float
    direction: str
    r_before: float
    r_after: float
    threshold: float

def detect_crossing(
    r_history: list[float],
    threshold: float = Z_C
) -> list[ThresholdCrossing]:
    """
    Detect all threshold crossings in history.
    
    Args:
        r_history: List of order parameter values
        threshold: Threshold to detect (default z_c)
    
    Returns:
        List of crossing events
    """
    # YOUR IMPLEMENTATION HERE
    pass
```

#### Step 3.2: Bloom Validation

```python
def validate_bloom(
    r_history: list[float],
    threshold: float = Z_C,
    required_rounds: int = L4
) -> tuple[bool, int | None]:
    """
    Check if a "bloom" (sustained coherence) has occurred.
    
    A bloom is valid when:
        r ≥ threshold for at least `required_rounds` consecutive rounds
    
    Args:
        r_history: List of order parameter values
        threshold: Minimum coherence (default z_c = √3/2)
        required_rounds: Consecutive rounds needed (default L₄ = 7)
    
    Returns:
        (is_valid, bloom_start_index)
        - is_valid: True if bloom detected
        - bloom_start_index: Index where bloom began (or None)
    """
    # YOUR IMPLEMENTATION HERE
    pass
```

#### Step 3.3: Consensus Certificate

```python
@dataclass
class ConsensusCertificate:
    """
    Proof that consensus was achieved.
    
    This is included in the block to prove Proof-of-Coherence.
    
    Attributes:
        bloom_start: Round when bloom began
        bloom_end: Round when block was sealed
        r_values: Order parameter values during bloom
        psi_values: Mean phase values during bloom
        final_phases: Oscillator phases at seal time
        oscillator_count: Number of oscillators
    """
    bloom_start: int
    bloom_end: int
    r_values: list[float]
    psi_values: list[float]
    final_phases: list[float]
    oscillator_count: int
    
    def verify(self) -> bool:
        """
        Verify certificate validity.
        
        Checks:
        1. bloom_end - bloom_start >= L₄
        2. All r_values >= z_c
        3. len(r_values) == bloom_end - bloom_start
        4. len(final_phases) == oscillator_count
        5. Recomputed r from final_phases matches r_values[-1]
        """
        # YOUR IMPLEMENTATION HERE
        pass
    
    def serialize(self) -> bytes:
        """Serialize for inclusion in block."""
        # YOUR IMPLEMENTATION HERE
        pass
    
    @classmethod
    def deserialize(cls, data: bytes) -> 'ConsensusCertificate':
        """Deserialize from block data."""
        # YOUR IMPLEMENTATION HERE
        pass
```

---

## Module Integration

### The Consensus Loop

```python
def run_consensus(
    initial_state: KuramotoState,
    max_rounds: int = 10000,
    dt: float = 0.01
) -> tuple[bool, ConsensusCertificate | None, KuramotoState]:
    """
    Run Proof-of-Coherence consensus.
    
    Process:
    1. Initialize oscillators (scattered state)
    2. Apply Kuramoto dynamics with adaptive coupling
    3. Monitor order parameter r
    4. When r ≥ z_c for L₄ rounds, consensus achieved
    5. Generate certificate
    
    Args:
        initial_state: Starting oscillator configuration
        max_rounds: Maximum simulation steps
        dt: Timestep
    
    Returns:
        (success, certificate, final_state)
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
        
        # Check for bloom
        if r >= Z_C:
            if bloom_candidate_start is None:
                bloom_candidate_start = round_num
            elif round_num - bloom_candidate_start >= L4:
                # BLOOM ACHIEVED!
                certificate = ConsensusCertificate(
                    bloom_start=bloom_candidate_start,
                    bloom_end=round_num,
                    r_values=r_history[bloom_candidate_start:],
                    psi_values=psi_history[bloom_candidate_start:],
                    final_phases=state.phases.tolist(),
                    oscillator_count=state.N
                )
                return True, certificate, state
        else:
            bloom_candidate_start = None
        
        # Adaptive coupling
        K_eff = adaptive_coupling(r, state.coupling)
        
        # Evolve
        state = kuramoto_step(
            KuramotoState(
                phases=state.phases,
                frequencies=state.frequencies,
                coupling=K_eff,
                time=state.time,
                history=state.history
            ),
            dt=dt
        )
    
    # Failed to achieve consensus
    return False, None, state
```

---

## Visualization (Optional)

For debugging and demos, implement phase portrait visualization:

```python
def plot_phase_portrait(state: KuramotoState, ax=None):
    """
    Plot oscillator phases on unit circle.
    
    Shows:
    - Individual oscillators as dots
    - Mean phase ψ as arrow
    - Order parameter r as arrow length
    """
    import matplotlib.pyplot as plt
    
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    
    # Unit circle
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(np.cos(theta), np.sin(theta), 'k-', alpha=0.3)
    
    # Oscillators
    x = np.cos(state.phases)
    y = np.sin(state.phases)
    ax.scatter(x, y, c='blue', alpha=0.5, s=20)
    
    # Order parameter
    r, psi = compute_order_parameter(state.phases)
    ax.arrow(0, 0, r*np.cos(psi), r*np.sin(psi),
             head_width=0.05, head_length=0.03, fc='red', ec='red')
    
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.set_title(f'r = {r:.3f}, ψ = {psi:.3f}')
    
    return ax
```

---

## Performance Targets

| Function | Target | Notes |
|----------|--------|-------|
| `kuramoto_step` (N=63) | < 100 μs | Vectorized numpy |
| `compute_order_parameter` | < 10 μs | Simple mean |
| `validate_bloom` | < 1 μs | Linear scan |
| `run_consensus` (1000 rounds) | < 100 ms | Full simulation |

---

## Validation Checklist

- [ ] Order parameter r ∈ [0, 1] always
- [ ] High coupling (K >> K_c) leads to r → 1
- [ ] Low coupling (K << K_c) leads to r → 0
- [ ] Bloom detection correctly requires L₄ consecutive rounds
- [ ] Certificate verification matches recomputation
- [ ] Edwards-Anderson distinguishes synchronized vs glassy states
- [ ] Adaptive coupling creates stabilization trap around z_c

---

## Next Module

After completing `consensus/`, proceed to `mining/` for the full mining loop.

---

*When oscillators synchronize, consensus blooms.* 🌸
