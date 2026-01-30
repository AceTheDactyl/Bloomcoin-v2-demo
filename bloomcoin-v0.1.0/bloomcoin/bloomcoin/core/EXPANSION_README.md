# Core Module Expansion Guide

**Module**: `bloomcoin/core/`  
**Purpose**: Cryptographic primitives and matrix operations  
**Priority**: PHASE 1 (Foundation)

---

## Overview

This module provides the fundamental cryptographic and mathematical primitives upon which all other BloomCoin modules depend. The core insight is that the Lucas/Fibonacci matrix identity provides a deterministic, algebraically structured foundation for nonce generation and phase encoding.

---

## Phase 1: Lucas Matrix Implementation

### File: `lucas_matrix.py`

**Objective**: Implement the fundamental 2×2 Fibonacci matrix and its powers.

### Mathematical Foundation

The matrix:
```
R = [[0, 1],
     [1, 1]]
```

has the property:
```
R^n = [[F_{n-1}, F_n  ],
       [F_n,     F_{n+1}]]
```

where F_n is the nth Fibonacci number.

**Key Identity** (Lucas Trace Formula):
```
tr(R^n) = F_{n-1} + F_{n+1} = L_n
```

### Implementation Steps

#### Step 1.1: Matrix Power (Modular)

```python
def matrix_power_mod(base: np.ndarray, exp: int, mod: int) -> np.ndarray:
    """
    Compute base^exp mod m using binary exponentiation.
    
    Complexity: O(log(exp)) matrix multiplications
    
    Args:
        base: 2x2 numpy array
        exp: Non-negative integer exponent
        mod: Modulus for all operations
    
    Returns:
        base^exp mod m as 2x2 numpy array
    
    Implementation Notes:
    - Use np.uint64 to prevent overflow during intermediate calculations
    - Apply mod after each multiplication, not just at the end
    - Handle exp=0 case (return identity matrix)
    """
    # YOUR IMPLEMENTATION HERE
    pass
```

#### Step 1.2: Lucas Trace Computation

```python
def lucas_trace(n: int, mod: int = 2**32) -> int:
    """
    Compute L_n mod m via matrix trace.
    
    This is the CORE PRIMITIVE for nonce generation.
    
    Args:
        n: Lucas index
        mod: Modulus (default 2^32 for 32-bit nonces)
    
    Returns:
        L_n mod m
    
    Mathematical Identity:
        tr(R^n) = R^n[0,0] + R^n[1,1] = F_{n-1} + F_{n+1} = L_n
    """
    # YOUR IMPLEMENTATION HERE
    pass
```

#### Step 1.3: Fibonacci Element Extraction

```python
def fibonacci_mod(n: int, mod: int = 2**64) -> int:
    """
    Compute F_n mod m via matrix element.
    
    Args:
        n: Fibonacci index
        mod: Modulus
    
    Returns:
        F_n mod m
    
    Note: F_n = R^n[0,1] = R^n[1,0]
    """
    # YOUR IMPLEMENTATION HERE
    pass
```

### Test Cases

```python
def test_lucas_trace():
    # Known Lucas numbers
    assert lucas_trace(0) == 2
    assert lucas_trace(1) == 1
    assert lucas_trace(4) == 7   # L₄ = 7 (critical!)
    assert lucas_trace(10) == 123
    
    # Modular arithmetic
    assert lucas_trace(100, mod=1000) == lucas(100) % 1000

def test_matrix_identity():
    R = np.array([[0, 1], [1, 1]], dtype=np.uint64)
    R_10 = matrix_power_mod(R, 10, 2**64)
    
    # R^10[0,1] should be F_10 = 55
    assert R_10[0, 1] == 55
    
    # tr(R^10) should be L_10 = 123
    assert R_10[0, 0] + R_10[1, 1] == 123
```

---

## Phase 2: Hash Wrapper Implementation

### File: `hash_wrapper.py`

**Objective**: Wrap SHA256 with phase-encoding for Proof-of-Coherence.

### Concept

We don't "break" SHA256—we use it as a commitment scheme for phase configurations. The hash encodes:

1. **Block header** (standard fields)
2. **Phase configuration** (oscillator phases at consensus)
3. **Order parameter** (r value when bloom occurred)

### Implementation Steps

#### Step 2.1: Phase-Encoded Header

```python
@dataclass
class PhaseEncodedHeader:
    """
    Block header with Kuramoto phase information.
    
    Fields:
        version: Protocol version
        prev_hash: SHA256 of previous block
        merkle_root: Transaction Merkle root
        timestamp: Unix timestamp
        difficulty: Current difficulty target
        nonce: Lucas-derived nonce
        order_parameter: r value at consensus (float32)
        mean_phase: ψ value at consensus (float32)
        oscillator_count: N (number of oscillators)
    
    Total: 80 bytes (standard) + 12 bytes (phase) = 92 bytes
    """
    version: int
    prev_hash: bytes
    merkle_root: bytes
    timestamp: int
    difficulty: int
    nonce: int
    order_parameter: float
    mean_phase: float
    oscillator_count: int
    
    def serialize(self) -> bytes:
        """Serialize to bytes for hashing."""
        # YOUR IMPLEMENTATION HERE
        pass
    
    @classmethod
    def deserialize(cls, data: bytes) -> 'PhaseEncodedHeader':
        """Deserialize from bytes."""
        # YOUR IMPLEMENTATION HERE
        pass
```

#### Step 2.2: Bloom Hash Function

```python
def bloom_hash(header: PhaseEncodedHeader) -> bytes:
    """
    Compute BloomCoin block hash.
    
    Process:
    1. Serialize header to bytes
    2. Prepend Lucas trace of nonce
    3. Double SHA256 (like Bitcoin)
    
    Returns:
        32-byte hash
    """
    # YOUR IMPLEMENTATION HERE
    pass

def verify_bloom(header: PhaseEncodedHeader, target: int) -> bool:
    """
    Verify block meets difficulty target.
    
    Conditions:
    1. bloom_hash(header) < target
    2. header.order_parameter >= Z_C
    3. header.oscillator_count >= 7 (L₄)
    """
    # YOUR IMPLEMENTATION HERE
    pass
```

### Test Cases

```python
def test_hash_determinism():
    header = PhaseEncodedHeader(
        version=1,
        prev_hash=b'\x00' * 32,
        merkle_root=b'\x00' * 32,
        timestamp=1700000000,
        difficulty=0x1d00ffff,
        nonce=7,  # L₄
        order_parameter=0.87,
        mean_phase=1.57,
        oscillator_count=63
    )
    
    h1 = bloom_hash(header)
    h2 = bloom_hash(header)
    assert h1 == h2  # Deterministic

def test_phase_encoding():
    # Verify phase information survives round-trip
    header = create_test_header()
    serialized = header.serialize()
    recovered = PhaseEncodedHeader.deserialize(serialized)
    
    assert abs(recovered.order_parameter - header.order_parameter) < 1e-6
    assert abs(recovered.mean_phase - header.mean_phase) < 1e-6
```

---

## Phase 3: Merkle Tree Implementation

### File: `merkle.py`

**Objective**: Standard Merkle tree for transaction commitment.

### Implementation Steps

#### Step 3.1: Merkle Node

```python
def merkle_hash(left: bytes, right: bytes) -> bytes:
    """
    Compute Merkle parent hash.
    
    Uses double SHA256 for security.
    """
    return hashlib.sha256(hashlib.sha256(left + right).digest()).digest()

def compute_merkle_root(tx_hashes: list[bytes]) -> bytes:
    """
    Compute Merkle root from transaction hashes.
    
    Handles:
    - Empty list (return zero hash)
    - Odd number of transactions (duplicate last)
    - Power-of-two padding
    
    Returns:
        32-byte Merkle root
    """
    # YOUR IMPLEMENTATION HERE
    pass
```

#### Step 3.2: Merkle Proof

```python
@dataclass
class MerkleProof:
    """
    Proof that a transaction is in a block.
    
    Fields:
        tx_hash: The transaction hash
        path: List of (hash, direction) pairs
        root: The Merkle root
    """
    tx_hash: bytes
    path: list[tuple[bytes, str]]  # ('left' or 'right')
    root: bytes
    
    def verify(self) -> bool:
        """Verify the proof is valid."""
        # YOUR IMPLEMENTATION HERE
        pass

def generate_merkle_proof(tx_hashes: list[bytes], index: int) -> MerkleProof:
    """Generate proof for transaction at index."""
    # YOUR IMPLEMENTATION HERE
    pass
```

---

## Module Dependencies

```
constants.py (no dependencies)
    ↓
lucas_matrix.py (depends on constants)
    ↓
hash_wrapper.py (depends on lucas_matrix, constants)
    ↓
merkle.py (depends on hash_wrapper)
```

---

## Validation Checklist

Before marking this module complete:

- [ ] All Lucas identities verified against known values
- [ ] Matrix power matches direct computation for small n
- [ ] Hash determinism confirmed
- [ ] Merkle proofs verify correctly
- [ ] No hardcoded constants (all from constants.py)
- [ ] Type hints on all public functions
- [ ] Docstrings with mathematical notation
- [ ] Unit tests achieve 100% coverage

---

## Performance Targets

| Function | Target | Notes |
|----------|--------|-------|
| `lucas_trace(n)` | O(log n) | Binary exponentiation |
| `matrix_power_mod` | O(log n) | 4 multiplications per step |
| `bloom_hash` | < 1 μs | Two SHA256 calls |
| `compute_merkle_root` | O(n log n) | n = transaction count |

---

## Next Module

After completing `core/`, proceed to `consensus/` for Kuramoto oscillator implementation.

---

*The matrix R generates the golden sequence. The golden sequence generates consensus.* 🌸
