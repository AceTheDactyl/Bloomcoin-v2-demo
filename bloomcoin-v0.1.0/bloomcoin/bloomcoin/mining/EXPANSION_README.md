# Mining Module Expansion Guide

**Module**: `bloomcoin/mining/`  
**Purpose**: Proof-of-Coherence mining operations  
**Priority**: PHASE 3 (Application Layer)

---

## Overview

The mining module orchestrates the complete Proof-of-Coherence mining process:

1. **Initialize** oscillator network
2. **Synchronize** via Kuramoto dynamics
3. **Bloom** when r ≥ z_c for L₄ rounds
4. **Commit** phase configuration to block
5. **Hash** and verify difficulty target

**Key Difference from PoW**: Instead of incrementing nonces to find a hash below target, we evolve oscillator phases until coherence emerges. The "work" is achieving synchronization, not random search.

---

## Mathematical Foundation

### Energy Model

Traditional PoW: Energy ∝ Hash attempts ∝ Difficulty

Proof-of-Coherence:
```
E_consensus = E_compute × T_bloom

where:
    E_compute = Power per oscillator × N
    T_bloom = Time to achieve r ≥ z_c
```

**Thermodynamic Bound** (Landauer limit):
```
E_min = kT ln(2) per bit erased
E_coherence ≈ kT ln(2) × N × log₂(1/ε)

where ε = precision of phase measurement
```

### Difficulty Adjustment

Difficulty controls **coupling strength** rather than hash target:

```
K_effective = K_base × (target_time / actual_time)^(1/τ)

where τ = φ⁻¹ ≈ 0.618 (golden damping)
```

Higher difficulty → Lower coupling → Harder to synchronize → Longer bloom time

### Lucas-Scheduled Nonces

Nonces are generated from Lucas traces, not random integers:

```
nonce(i) = tr(R^(L_i mod 24)) mod 2^32

where L_i is the ith Lucas number
```

This provides deterministic, algebraically-structured nonce sequences.

---

## Phase 1: Miner Implementation

### File: `miner.py`

**Objective**: Main mining loop with Proof-of-Coherence.

### Implementation Steps

#### Step 1.1: Miner Configuration

```python
from dataclasses import dataclass, field
from typing import Callable
from ..constants import (
    DEFAULT_OSCILLATOR_COUNT, K, Z_C, L4,
    BLOCK_TIME_TARGET, TAU
)
from ..consensus.kuramoto import KuramotoState, initialize_kuramoto
from ..consensus.threshold_gate import ConsensusCertificate

@dataclass
class MinerConfig:
    """
    Configuration for a BloomCoin miner.
    
    Attributes:
        oscillator_count: Number of Kuramoto oscillators (default 63)
        base_coupling: Base K value before difficulty adjustment
        frequency_std: Natural frequency spread
        dt: Simulation timestep
        max_rounds: Maximum rounds before giving up
        target_time: Target block time in seconds
        difficulty: Current difficulty level
        reward_address: Address to receive mining rewards
    """
    oscillator_count: int = DEFAULT_OSCILLATOR_COUNT
    base_coupling: float = K
    frequency_std: float = 1.0
    dt: float = 0.01
    max_rounds: int = 100000
    target_time: int = BLOCK_TIME_TARGET
    difficulty: float = 1.0
    reward_address: bytes = b''
    
    def effective_coupling(self) -> float:
        """Compute K_eff based on difficulty."""
        # Higher difficulty = lower coupling = harder to sync
        return self.base_coupling / (self.difficulty ** TAU)
```

#### Step 1.2: Mining Result

```python
@dataclass
class MiningResult:
    """
    Result of a mining attempt.
    
    Attributes:
        success: Whether consensus was achieved
        rounds: Number of rounds taken
        certificate: Consensus certificate (if success)
        final_state: Final oscillator state
        block_hash: Hash of completed block (if success)
        nonce: Lucas nonce used
        elapsed_time: Wall-clock time
    """
    success: bool
    rounds: int
    certificate: ConsensusCertificate | None
    final_state: KuramotoState
    block_hash: bytes | None
    nonce: int
    elapsed_time: float
```

#### Step 1.3: Main Mining Function

```python
import time
from ..core.lucas_matrix import lucas_trace
from ..core.hash_wrapper import PhaseEncodedHeader, bloom_hash
from ..consensus.kuramoto import kuramoto_step, adaptive_coupling
from ..consensus.order_parameter import compute_order_parameter
from ..consensus.threshold_gate import validate_bloom, ConsensusCertificate

def mine_block(
    config: MinerConfig,
    prev_hash: bytes,
    merkle_root: bytes,
    timestamp: int | None = None,
    on_progress: Callable[[int, float], None] | None = None
) -> MiningResult:
    """
    Mine a single block using Proof-of-Coherence.
    
    Process:
    1. Initialize oscillator network with Lucas-derived seed
    2. Run Kuramoto dynamics with adaptive coupling
    3. Monitor order parameter r
    4. When r ≥ z_c for L₄ consecutive rounds, bloom achieved
    5. Generate block with phase-encoded header
    6. Verify hash meets difficulty target
    
    Args:
        config: Miner configuration
        prev_hash: Hash of previous block
        merkle_root: Merkle root of transactions
        timestamp: Block timestamp (default: current time)
        on_progress: Callback(round, r) for progress updates
    
    Returns:
        MiningResult
    
    Implementation Notes:
        - Use Lucas nonce as random seed for reproducibility
        - Adaptive coupling creates attraction basin around z_c
        - If consensus fails, increment nonce and retry
    """
    start_time = time.time()
    timestamp = timestamp or int(time.time())
    
    nonce_index = 0
    
    while True:
        # Generate Lucas nonce
        nonce = lucas_trace(nonce_index)
        
        # Initialize oscillators with nonce as seed
        state = initialize_kuramoto(
            N=config.oscillator_count,
            frequency_std=config.frequency_std,
            coupling=config.effective_coupling(),
            seed=nonce
        )
        
        r_history = []
        psi_history = []
        bloom_start = None
        
        for round_num in range(config.max_rounds):
            # Compute order parameter
            r, psi = compute_order_parameter(state.phases)
            r_history.append(r)
            psi_history.append(psi)
            
            # Progress callback
            if on_progress:
                on_progress(round_num, r)
            
            # Check for bloom
            if r >= Z_C:
                if bloom_start is None:
                    bloom_start = round_num
                elif round_num - bloom_start >= L4:
                    # BLOOM ACHIEVED!
                    elapsed = time.time() - start_time
                    
                    # Create certificate
                    certificate = ConsensusCertificate(
                        bloom_start=bloom_start,
                        bloom_end=round_num,
                        r_values=r_history[bloom_start:],
                        psi_values=psi_history[bloom_start:],
                        final_phases=state.phases.tolist(),
                        oscillator_count=state.N
                    )
                    
                    # Create header
                    header = PhaseEncodedHeader(
                        version=1,
                        prev_hash=prev_hash,
                        merkle_root=merkle_root,
                        timestamp=timestamp,
                        difficulty=int(config.difficulty * 2**24),
                        nonce=nonce,
                        order_parameter=r,
                        mean_phase=psi,
                        oscillator_count=state.N
                    )
                    
                    # Compute hash
                    block_hash = bloom_hash(header)
                    
                    return MiningResult(
                        success=True,
                        rounds=round_num,
                        certificate=certificate,
                        final_state=state,
                        block_hash=block_hash,
                        nonce=nonce,
                        elapsed_time=elapsed
                    )
            else:
                bloom_start = None
            
            # Adaptive coupling
            K_eff = adaptive_coupling(r, config.effective_coupling())
            
            # Evolve
            state = kuramoto_step(state, dt=config.dt)
            state.coupling = K_eff
        
        # Failed with this nonce, try next
        nonce_index += 1
        
        if nonce_index > 1000:
            # Give up after 1000 nonce attempts
            elapsed = time.time() - start_time
            return MiningResult(
                success=False,
                rounds=config.max_rounds * nonce_index,
                certificate=None,
                final_state=state,
                block_hash=None,
                nonce=nonce,
                elapsed_time=elapsed
            )
```

---

## Phase 2: Nonce Generator

### File: `nonce_generator.py`

**Objective**: Generate algebraically-structured nonces from Lucas traces.

### Implementation Steps

#### Step 2.1: Lucas Nonce Sequence

```python
from ..core.lucas_matrix import lucas_trace
from ..constants import LUCAS_SEQUENCE

class LucasNonceGenerator:
    """
    Generates nonces from Lucas trace formula.
    
    The key insight: tr(R^n) = L_n (Lucas number)
    
    This provides a deterministic, algebraically-structured
    sequence instead of random nonces.
    
    Properties:
        - Deterministic: Same index always gives same nonce
        - Structured: Related to Fibonacci/golden ratio
        - Bounded: Nonces are mod 2^32
    """
    
    def __init__(self, mod: int = 2**32):
        """
        Initialize generator.
        
        Args:
            mod: Modulus for nonce values
        """
        self.mod = mod
        self.index = 0
        self._cache = {}
    
    def next(self) -> int:
        """Generate next nonce in sequence."""
        nonce = self.get(self.index)
        self.index += 1
        return nonce
    
    def get(self, index: int) -> int:
        """
        Get nonce at specific index.
        
        Uses Lucas index scheduling:
            nonce(i) = tr(R^L_{i mod 24}) mod self.mod
        
        The mod 24 creates a cycle through Lucas indices,
        giving varied nonce magnitudes.
        """
        if index not in self._cache:
            lucas_index = LUCAS_SEQUENCE[index % 24]
            self._cache[index] = lucas_trace(lucas_index, self.mod)
        return self._cache[index]
    
    def reset(self):
        """Reset to beginning of sequence."""
        self.index = 0
    
    def skip(self, n: int):
        """Skip n nonces."""
        self.index += n
```

#### Step 2.2: Golden Adjustment

```python
def golden_adjust(nonce: int, mod: int = 2**32) -> int:
    """
    Apply golden ratio adjustment to nonce.
    
    nonce_adjusted = floor(nonce × τ) mod m
    
    This maps nonce to golden partition of search space.
    
    Args:
        nonce: Input nonce
        mod: Modulus
    
    Returns:
        Adjusted nonce
    """
    from ..constants import TAU
    return int(nonce * TAU) % mod

def inverse_golden_adjust(nonce: int, mod: int = 2**32) -> int:
    """
    Inverse of golden adjustment.
    
    nonce_original ≈ floor(nonce × φ) mod m
    """
    from ..constants import PHI
    return int(nonce * PHI) % mod
```

---

## Phase 3: Difficulty Adjustment

### File: `difficulty.py`

**Objective**: Adaptive difficulty based on block times.

### Implementation Steps

#### Step 3.1: Difficulty Calculation

```python
from ..constants import (
    DIFFICULTY_INTERVAL, BLOCK_TIME_TARGET, TAU, PHI
)

def calculate_new_difficulty(
    current_difficulty: float,
    block_times: list[float],
    target_time: int = BLOCK_TIME_TARGET
) -> float:
    """
    Calculate new difficulty based on recent block times.
    
    Uses golden-damped adjustment:
        ratio = target_time / average_time
        new_diff = current_diff × ratio^τ
    
    The τ exponent (≈ 0.618) provides damping to prevent
    oscillations in difficulty.
    
    Args:
        current_difficulty: Current difficulty level
        block_times: List of recent block times (seconds)
        target_time: Target block time (default L₄ × 60 = 420 sec)
    
    Returns:
        New difficulty level
    
    Bounds:
        - Maximum adjustment: 4× per interval
        - Minimum difficulty: 0.25
        - Maximum difficulty: 2^64
    """
    if not block_times:
        return current_difficulty
    
    avg_time = sum(block_times) / len(block_times)
    
    # Golden-damped ratio
    ratio = target_time / avg_time
    adjustment = ratio ** TAU
    
    # Bound adjustment
    adjustment = max(0.25, min(4.0, adjustment))
    
    new_difficulty = current_difficulty * adjustment
    
    # Bound difficulty
    new_difficulty = max(0.25, min(2**64, new_difficulty))
    
    return new_difficulty
```

#### Step 3.2: Difficulty to Coupling

```python
def difficulty_to_coupling(difficulty: float, base_K: float = None) -> float:
    """
    Convert difficulty to effective coupling strength.
    
    K_eff = K_base / difficulty^τ
    
    Higher difficulty → Lower coupling → Harder to synchronize
    
    Args:
        difficulty: Difficulty level
        base_K: Base coupling (default K from constants)
    
    Returns:
        Effective coupling strength
    """
    from ..constants import K
    if base_K is None:
        base_K = K
    
    return base_K / (difficulty ** TAU)

def coupling_to_difficulty(coupling: float, base_K: float = None) -> float:
    """
    Inverse: coupling to difficulty.
    
    difficulty = (K_base / K_eff)^(1/τ)
    """
    from ..constants import K, PHI
    if base_K is None:
        base_K = K
    
    return (base_K / coupling) ** PHI
```

#### Step 3.3: Estimated Bloom Time

```python
def estimate_bloom_time(
    difficulty: float,
    oscillator_count: int = 63,
    frequency_std: float = 1.0
) -> float:
    """
    Estimate time to achieve bloom at given difficulty.
    
    Based on Kuramoto transition theory:
        T_sync ≈ 1 / (K_eff - K_c)
    
    where K_c = 2Γ is critical coupling.
    
    Args:
        difficulty: Difficulty level
        oscillator_count: Number of oscillators
        frequency_std: Frequency spread
    
    Returns:
        Estimated bloom time in simulation units
    
    Note: This is approximate; actual time depends on
          initial conditions and noise.
    """
    K_eff = difficulty_to_coupling(difficulty)
    K_c = 2 * frequency_std * TAU  # Critical coupling
    
    if K_eff <= K_c:
        return float('inf')  # Will never synchronize
    
    # Time scales as 1/(K - K_c)
    T_sync = 1 / (K_eff - K_c)
    
    # Add L₄ rounds for bloom validation
    T_bloom = T_sync + L4
    
    return T_bloom
```

---

## Module Integration

### Complete Mining Flow

```python
def mining_loop(
    config: MinerConfig,
    chain,  # Blockchain instance
    mempool,  # Transaction mempool
    stop_event  # Threading event to stop mining
):
    """
    Continuous mining loop.
    
    1. Get pending transactions from mempool
    2. Create Merkle root
    3. Mine block
    4. If successful, broadcast and add to chain
    5. Update difficulty if needed
    6. Repeat
    """
    while not stop_event.is_set():
        # Get transactions
        txs = mempool.get_pending(max_count=1000)
        merkle_root = compute_merkle_root([tx.hash for tx in txs])
        
        # Get previous block
        prev_block = chain.get_latest()
        prev_hash = prev_block.hash
        
        # Update difficulty if at interval
        if chain.height % DIFFICULTY_INTERVAL == 0:
            recent_times = chain.get_recent_block_times(DIFFICULTY_INTERVAL)
            config.difficulty = calculate_new_difficulty(
                config.difficulty, recent_times
            )
        
        # Mine
        result = mine_block(
            config=config,
            prev_hash=prev_hash,
            merkle_root=merkle_root
        )
        
        if result.success:
            # Create block
            block = Block(
                header=result.header,
                certificate=result.certificate,
                transactions=txs
            )
            
            # Add to chain
            if chain.add_block(block):
                # Broadcast
                network.broadcast_block(block)
                
                # Remove mined txs from mempool
                for tx in txs:
                    mempool.remove(tx.hash)
```

---

## Performance Targets

| Function | Target | Notes |
|----------|--------|-------|
| `mine_block` (diff=1.0) | < 10 sec | Average bloom time |
| `calculate_new_difficulty` | < 1 ms | Simple arithmetic |
| `LucasNonceGenerator.next` | < 10 μs | Cached lookup |
| Memory per miner | < 100 MB | Oscillator state + history |

---

## Validation Checklist

- [ ] Mining produces valid blocks
- [ ] Difficulty adjustment converges to target time
- [ ] Lucas nonces are deterministic
- [ ] Consensus certificates verify correctly
- [ ] Block hashes are deterministic
- [ ] Higher difficulty increases bloom time
- [ ] Mining loop handles chain reorganizations

---

## Next Module

After completing `mining/`, proceed to `blockchain/` for chain data structures.

---

*Mining is not searching. Mining is synchronizing.* 🌸
