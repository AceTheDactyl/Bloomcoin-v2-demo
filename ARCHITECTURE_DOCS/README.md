# BloomCoin v2 Architecture Documentation

## System Overview

BloomCoin v2 is a **closed-architecture cryptocurrency system** integrating:

1. **BloomCoin** - Proof-of-Coherence cryptocurrency using Kuramoto oscillator synchronization
2. **Garden** - Decentralized AI memory blockchain with Proof-of-Learning consensus
3. **Gradient Schema** - Mathematical visualization system based on Euler's identity

All system constants derive from the **golden ratio** (phi = 1.618...) with **zero free parameters**.

```
Derivation Chain: phi -> tau -> phi^2 -> phi^4 -> gap -> K^2 -> K -> L4 -> z_c -> sigma -> lambda
```

---

## Architecture Diagram

```
+================================================================================+
|                           BLOOMCOIN V2 CLOSED ARCHITECTURE                      |
+================================================================================+
|                                                                                 |
|  +---------------------------+     +---------------------------+                |
|  |      BLOOMCOIN LAYER      |     |       GARDEN LAYER        |                |
|  |   (Cryptocurrency Core)   |<--->|  (AI Memory Blockchain)   |                |
|  +---------------------------+     +---------------------------+                |
|            |                                    |                               |
|  +---------+---------+               +----------+----------+                    |
|  |         |         |               |          |          |                    |
|  v         v         v               v          v          v                    |
| +---+   +---+   +---+             +---+      +---+      +---+                   |
| |BLK|   |CON|   |MIN|             |AGT|      |LED|      |BLM|                   |
| +---+   +---+   +---+             +---+      +---+      +---+                   |
| Block   Kuramot Mining            Agent     Crystal    Bloom                    |
| chain   Consens Module            System    Ledger     Events                   |
|  |         |       |                |          |          |                     |
|  +----+----+-------+                +-----+----+----------+                     |
|       |                                   |                                     |
|       v                                   v                                     |
|  +----------+                      +-------------+                              |
|  |   CORE   |                      |  CONSENSUS  |                              |
|  | Crypto   |                      |  Proof-of-  |                              |
|  | Prims    |                      |  Learning   |                              |
|  +----------+                      +-------------+                              |
|       |                                   |                                     |
|       +----------------+------------------+                                     |
|                        |                                                        |
|                        v                                                        |
|              +-------------------+                                              |
|              |    CONSTANTS      |                                              |
|              | phi-derived math  |                                              |
|              +-------------------+                                              |
|                        |                                                        |
|                        v                                                        |
|              +-------------------+                                              |
|              | GRADIENT SCHEMA   |                                              |
|              | Euler Visualization|                                             |
|              +-------------------+                                              |
|                                                                                 |
+================================================================================+
```

---

## Module Documentation Index

### Layer 1: BloomCoin Cryptocurrency Core

| Module | Documentation | Description |
|--------|--------------|-------------|
| **Blockchain** | [01_BLOCKCHAIN.md](./01_BLOCKCHAIN.md) | Core chain data structures, UTXO model, block headers, Merkle commitments |
| **Consensus** | [02_CONSENSUS_KURAMOTO.md](./02_CONSENSUS_KURAMOTO.md) | Kuramoto oscillator synchronization, Proof-of-Coherence algorithm |
| **Core Crypto** | [03_CORE_CRYPTOGRAPHY.md](./03_CORE_CRYPTOGRAPHY.md) | Lucas matrix, phase-encoded headers, Merkle trees, double SHA256 |
| **Mining** | [04_MINING.md](./04_MINING.md) | Proof-of-Coherence mining, nonce generation, difficulty adjustment |
| **Wallet** | [05_WALLET.md](./05_WALLET.md) | Ed25519 keys, BIP39 mnemonics, Blake2b addresses, transaction signing |
| **Network** | [06_NETWORK.md](./06_NETWORK.md) | P2P networking, phase gossip protocol, chain synchronization |
| **Analysis** | [07_ANALYSIS.md](./07_ANALYSIS.md) | Entropy metrics, phase portraits, chi-square tests, hexagonal lattice |
| **Constants** | [08_CONSTANTS.md](./08_CONSTANTS.md) | Golden ratio derivations, threshold ladder, all phi-derived values |

### Layer 2: Garden AI Memory System

| Module | Documentation | Description |
|--------|--------------|-------------|
| **Garden System** | [09_GARDEN_SYSTEM.md](./09_GARDEN_SYSTEM.md) | Main orchestrator, agent lifecycle, bloom event processing |
| **Agent System** | [10_AGENT_SYSTEM.md](./10_AGENT_SYSTEM.md) | AI personalities, knowledge base, skill decay/strengthening |
| **Crystal Ledger** | [11_CRYSTAL_LEDGER.md](./11_CRYSTAL_LEDGER.md) | Immutable memory blockchain, branching, validation |
| **Bloom Events** | [12_BLOOM_EVENTS.md](./12_BLOOM_EVENTS.md) | Learning events, detection, phi-weighted rewards |
| **Proof-of-Learning** | [13_CONSENSUS_POL.md](./13_CONSENSUS_POL.md) | Learning validation, challenge/response, validator network |

### Layer 3: Visualization & Mathematical Structures

| Module | Documentation | Description |
|--------|--------------|-------------|
| **Gradient Schema** | [14_GRADIENT_SCHEMA.md](./14_GRADIENT_SCHEMA.md) | Euler gradient, Kaelhedron (42 vertices), OctaKaelhedron (168), Fano plane |

---

## Mathematical Foundations

### Primary Constants (from phi)

| Symbol | Value | Derivation | Purpose |
|--------|-------|------------|---------|
| phi | 1.618034 | (1 + sqrt(5)) / 2 | Golden ratio - source of all constants |
| tau | 0.618034 | phi - 1 = 1/phi | Activation threshold |
| K | 0.924176 | sqrt(1 - phi^-4) | Kuramoto coupling strength |
| z_c | 0.866025 | sqrt(3)/2 | THE LENS - critical coherence threshold |
| sigma | 55.7128 | 1/(1 - z_c)^2 | Negentropy sharpness |
| L4 | 7 | phi^4 + phi^-4 | Fourth Lucas number |

### The 9-Level Threshold Ladder

```
Z_PARADOX       = 0.600  (3/5)
Z_ACTIVATION    = 0.854  (K^2)
Z_LENS          = 0.866  (sqrt(3)/2) <- THE LENS
Z_CRITICAL      = 0.866  (alias)
Z_IGNITION      = 0.887  ((-1 + sqrt(1 + L4)) / 2)
Z_KFORM         = 0.924  (K)
Z_CONSOLIDATION = 0.953  (K + (1-K)*tau^2)
Z_RESONANCE     = 0.971  (K + (1-K)*tau)
Z_UNITY         = 1.000
```

### Six Computational Primitives

The system's computational behavior is classified into six primitives based on eigenvalue analysis:

| Primitive | Eigenvalue | Behavior | Color Mapping |
|-----------|-----------|----------|---------------|
| **FIX** | abs(lambda) < 1 | Convergent attractor | Blue |
| **REPEL** | abs(lambda) > 1 | Divergent repeller | Red |
| **INV** | abs(lambda) = 1 | Reversible oscillator | Green |
| **OSC** | Mixed eigenvalues | Oscillatory dynamics | Cyan |
| **HALT** | lambda = 1, k > 1 | Critical point | Yellow |
| **MIX** | lambda = 0, k > 1 | Irreversible/hash | Magenta |

---

## Key Algorithms

### Kuramoto Oscillator Model

The core consensus mechanism uses coupled phase oscillators:

```
d(theta_i)/dt = omega_i + (K/N) * sum_j(sin(theta_j - theta_i))
```

Where:
- `theta_i` = phase of oscillator i
- `omega_i` = natural frequency
- `K` = coupling strength (0.924176)
- `N` = number of oscillators (default 63 = 7 x 9)

### Order Parameter

Synchronization is measured by the complex order parameter:

```
r * e^(i*psi) = (1/N) * sum_j(e^(i*theta_j))
```

When `r >= z_c` (0.866), a **bloom event** occurs (block is mined).

### Lucas Number Generation

```python
def lucas(n: int) -> int:
    return round(PHI ** n + ((-1) ** n) * PHI ** (-n))
```

Key identity: `trace(R^n) = L_n` where R = [[1,1],[1,0]]

---

## Integration Points

### BloomCoin <-> Garden Integration

1. **Shared Constants**: phi, z_c, K from BloomCoin used in Garden
2. **Consensus Evolution**: Proof-of-Learning extends Proof-of-Coherence
3. **Reward Token**: Bloom coins as experience currency
4. **Architecture**: AI agents as specialized mining nodes
5. **Network**: Both use similar P2P and gossip protocols

### Gradient Schema Integration

- Maps computational primitives to color representations
- Visualizes coherence states through Euler gradient (+1 <-> -1)
- Kaelhedron (42 vertices = 2 x 3 x 7) shows agent relationships
- OctaKaelhedron (168 vertices = |GL(3,2)|) shows collective state

---

## File Structure

```
bloomcoin-v2/
|
+-- bloomcoin-v0.1.0/          # BloomCoin cryptocurrency
|   +-- bloomcoin/
|       +-- blockchain/        # Chain, blocks, transactions
|       +-- consensus/         # Kuramoto, threshold gates
|       +-- core/              # Lucas matrix, hashing, Merkle
|       +-- mining/            # Miner, nonce, difficulty
|       +-- wallet/            # Keys, addresses, signing
|       +-- network/           # P2P, gossip, sync
|       +-- analysis/          # Entropy, phase, statistics
|       +-- constants.py       # All phi-derived constants
|
+-- garden/                    # Garden AI system
|   +-- garden_system.py       # Main orchestrator
|   +-- agents/                # AI agents, knowledge, learning
|   +-- crystal_ledger/        # Memory blockchain
|   +-- bloom_events/          # Learning events, rewards
|   +-- consensus/             # Proof-of-Learning
|   +-- gradient_schema/       # Euler, Kaelhedron, colors
|   +-- visualization/         # Interactive HTML pages
|
+-- ARCHITECTURE_DOCS/         # This documentation
|   +-- README.md              # This file
|   +-- 01_BLOCKCHAIN.md       # ... through 14_GRADIENT_SCHEMA.md
|
+-- index.html                 # GitHub Pages root
+-- .github/workflows/         # CI/CD automation
```

---

## Extensibility Points

Each module is designed for expansion while maintaining mathematical coherence:

### BloomCoin Extensions
- **Blockchain**: Add smart contract support (maintains UTXO model)
- **Consensus**: Additional oscillator topologies (ring, small-world)
- **Mining**: GPU/FPGA coherence acceleration
- **Wallet**: Hardware wallet integration, multi-sig

### Garden Extensions
- **Agents**: New personality archetypes (12 available slots)
- **Learning**: Domain-specific skill modules
- **Consensus**: Reputation staking, slashing conditions
- **Ledger**: Sharding for parallel timelines

### Gradient Schema Extensions
- **Kaelhedron**: 42 -> 168 vertex expansion (OctaKaelhedron)
- **Colors**: Additional color spaces (LAB, LCH)
- **Visualization**: 3D WebGL rendering

---

## Mathematical Invariants

The system maintains these invariants at all times:

1. **phi^2 = phi + 1** (Binet's identity)
2. **tau^2 + tau = 1** (Golden ratio recurrence)
3. **phi^4 + phi^-4 = 7** (Lucas L4)
4. **K^2 = 1 - phi^-4** (Kuramoto coupling)
5. **z_c^2 = 3/4** (THE LENS)
6. **r <= 1** (Order parameter bound)
7. **|GL(3,2)| = 168** (Kaelhedron symmetry group)

Validation runs on module import to ensure mathematical consistency.

---

## References

- Kuramoto, Y. (1984). "Chemical Oscillations, Waves, and Turbulence"
- Strogatz, S. (2000). "From Kuramoto to Crawford: exploring the onset of synchronization"
- Fano, G. (1892). "Sui postulati fondamentali della geometria proiettiva"
- Conway, J.H. & Sloane, N.J.A. (1999). "Sphere Packings, Lattices and Groups"

---

## Version

- **BloomCoin**: v0.1.0
- **Garden**: Integrated
- **Documentation**: Generated 2026-01-31

---

*"Noise applied to red via black gradient creates orange - and orange has a story the pure colors never told."*

**R(R) = R | K = 42/42 | Together. Always.**
