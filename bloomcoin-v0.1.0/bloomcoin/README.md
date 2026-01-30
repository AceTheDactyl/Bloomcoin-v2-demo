# BloomCoin: Kuramoto-Consensus Proof-of-Coherence Mining

**A Simulation Framework for Phase-Synchronization Based Distributed Consensus**

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BLOOMCOIN v0.1.0                                 ║
║         Symmetry Breaking Through Oppositional Equivalence Resolution         ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  Core Principle: Mining as Phase Synchronization                              ║
║  Consensus: Kuramoto Order Parameter r > z_c = √3/2                          ║
║  Energy Model: Negentropy-Bounded Proof-of-Coherence                         ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## ⚠️ Important Disclaimer

**This is an educational simulation framework.** The original "LucasBias" document contains mathematical claims that require significant correction:

1. **SHA256 is NOT broken** — The claim of sl(2,ℝ)⊕sl(2,ℝ) isomorphism is mathematically imprecise
2. **The χ² statistics cited are not reproducible** — Proper statistical analysis is provided in this framework
3. **This is a research simulation**, not a production cryptocurrency

---

## Mathematical Foundation (Corrected)

### The Lucas-Fibonacci Matrix Identity (Valid)

The matrix:
```
R = [[0, 1],
     [1, 1]]
```

satisfies:
```
R^n = [[F_{n-1}, F_n  ],
       [F_n,     F_{n+1}]]

tr(R^n) = F_{n-1} + F_{n+1} = L_n (Lucas number)
```

This identity **is correct** and forms our mathematical foundation.

### What BloomCoin Actually Does

Instead of "breaking SHA256," we implement **Proof-of-Coherence**:

1. **Kuramoto Oscillators**: Miners are phase oscillators seeking synchronization
2. **Symmetry Breaking**: Consensus emerges when r crosses z_c threshold
3. **Lucas Scheduling**: Block times follow Lucas-number intervals
4. **Negentropy Mining**: Work is measured by Fisher information increase

### Core Constants (L₄ Framework)

```python
φ = (1 + √5) / 2           # 1.6180339887498949
τ = φ⁻¹ = φ - 1            # 0.6180339887498949
gap = φ⁻⁴                  # 0.1458980337503155
K = √(1 - gap)             # 0.9241596378498006  (Kuramoto coupling)
z_c = √3 / 2               # 0.8660254037844386  (Critical threshold)
L₄ = 7                     # Fourth Lucas number
σ = 1 / (1 - z_c)²         # 55.7128... (Negentropy sharpness)
```

### The Proof-of-Coherence Algorithm

```
1. SCATTER: Initialize N oscillators with random phases θᵢ ∈ [0, 2π)
2. COUPLE:  Apply Kuramoto dynamics: dθᵢ/dt = ωᵢ + (K/N) Σⱼ sin(θⱼ - θᵢ)
3. MEASURE: Compute order parameter r = |Σⱼ e^(iθⱼ)| / N
4. BLOOM:   If r > z_c for L₄ consecutive rounds, block is valid
5. HASH:    Commit phase configuration to blockchain via SHA256
6. REWARD:  Distribute based on negentropy contribution η(r)
```

---

## Repository Structure

```
bloomcoin/
├── README.md                          # This file
├── pyproject.toml                     # Package configuration
├── LICENSE                            # MIT License
│
├── bloomcoin/
│   ├── __init__.py
│   ├── constants.py                   # L₄ framework constants
│   │
│   ├── core/                          # Core cryptographic primitives
│   │   ├── __init__.py
│   │   ├── EXPANSION_README.md        # LLM implementation guide
│   │   ├── lucas_matrix.py            # Fibonacci/Lucas matrix operations
│   │   ├── hash_wrapper.py            # SHA256 with phase encoding
│   │   └── merkle.py                  # Merkle tree for transactions
│   │
│   ├── consensus/                     # Proof-of-Coherence consensus
│   │   ├── __init__.py
│   │   ├── EXPANSION_README.md        # LLM implementation guide
│   │   ├── kuramoto.py                # Kuramoto oscillator engine
│   │   ├── order_parameter.py         # r, q, Fisher information
│   │   └── threshold_gate.py          # z_c crossing detection
│   │
│   ├── mining/                        # Mining operations
│   │   ├── __init__.py
│   │   ├── EXPANSION_README.md        # LLM implementation guide
│   │   ├── miner.py                   # Main mining loop
│   │   ├── nonce_generator.py         # Lucas-scheduled nonce generation
│   │   └── difficulty.py              # Adaptive difficulty via negentropy
│   │
│   ├── blockchain/                    # Chain data structures
│   │   ├── __init__.py
│   │   ├── EXPANSION_README.md        # LLM implementation guide
│   │   ├── block.py                   # Block structure
│   │   ├── chain.py                   # Blockchain operations
│   │   └── transaction.py             # Transaction structure
│   │
│   ├── network/                       # P2P networking
│   │   ├── __init__.py
│   │   ├── EXPANSION_README.md        # LLM implementation guide
│   │   ├── node.py                    # Network node
│   │   ├── gossip.py                  # Phase gossip protocol
│   │   └── sync.py                    # Chain synchronization
│   │
│   ├── wallet/                        # Wallet operations
│   │   ├── __init__.py
│   │   ├── EXPANSION_README.md        # LLM implementation guide
│   │   ├── keypair.py                 # Ed25519 key generation
│   │   ├── address.py                 # Address derivation
│   │   └── signer.py                  # Transaction signing
│   │
│   └── analysis/                      # Statistical analysis tools
│       ├── __init__.py
│       ├── EXPANSION_README.md        # LLM implementation guide
│       ├── chi_square.py              # Proper χ² analysis
│       ├── phase_portrait.py          # Kuramoto visualization
│       └── entropy_metrics.py         # Negentropy measurement
│
├── tests/
│   ├── test_constants.py
│   ├── test_lucas_matrix.py
│   ├── test_kuramoto.py
│   ├── test_mining.py
│   └── test_blockchain.py
│
├── examples/
│   ├── mine_single_block.py
│   ├── simulate_network.py
│   └── visualize_consensus.py
│
└── docs/
    ├── MATHEMATICAL_FOUNDATION.md
    ├── CONSENSUS_PROTOCOL.md
    └── SECURITY_ANALYSIS.md
```

---

## Quick Start

```bash
# Clone and install
git clone https://github.com/bloomcoin/bloomcoin.git
cd bloomcoin
pip install -e .

# Run single block mining simulation
python examples/mine_single_block.py

# Visualize Kuramoto consensus
python examples/visualize_consensus.py
```

---

## The Bloom: Why "BloomCoin"?

The name comes from the mathematical phenomenon of **coherence blooming**:

```
                    r = 0.4 (Incoherent)
                         ○ ○
                       ○     ○
                      ○   ·   ○
                       ○     ○
                         ○ ○
                           
                    ↓ Coupling increases ↓
                    
                    r = 0.87 (Blooming)
                         ●●
                       ●    ●
                      ●  ★  ●
                       ●    ●
                         ●●
                           
    When r > z_c = √3/2, the bloom crystallizes into consensus.
```

---

## License

MIT License — See LICENSE file.

---

## Citation

```bibtex
@software{bloomcoin2025,
  title={BloomCoin: Kuramoto-Consensus Proof-of-Coherence Mining},
  author={L₄ Framework Collaboration},
  year={2025},
  url={https://github.com/bloomcoin/bloomcoin}
}
```

---

*Together. Always.* 🌸✨
