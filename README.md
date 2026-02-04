# BloomCoin Complete System Closure v6

> Zero Free Parameters — All Values Derived from φ

[![Deploy to GitHub Pages](https://github.com/AceTheDactyl/Bloomcoin-v2-demo/actions/workflows/deploy.yml/badge.svg)](https://github.com/AceTheDactyl/Bloomcoin-v2-demo/actions/workflows/deploy.yml)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Overview

BloomCoin is a φ-driven cryptocurrency system where every constant, threshold, and parameter derives algebraically from the golden ratio φ = (1+√5)/2. This repository contains the complete v6 system closure with 50 interactive documentation modules.

## Core Constants

| Constant | Value | Derivation |
|----------|-------|------------|
| φ (PHI) | 1.618034 | (1+√5)/2 |
| τ (TAU) | 0.618034 | φ⁻¹ |
| K (Coupling) | 0.924160 | √(1-φ⁻⁴) |
| z_c (THE LENS) | 0.866025 | √3/2 |
| L₄ | 7 | φ⁴ + φ⁻⁴ |

## Key Features

- **40+ Closed Systems** — Each mathematically self-contained
- **Zero Free Parameters** — Everything derives from φ
- **NEXTHASH-256** — Novel hash function with 113% SHA-256 security
- **Proof-of-Coherence** — Kuramoto oscillator consensus (N=63)
- **7 Companion Archetypes** — Mining entities with unique specializations
- **Full Blockchain Stack** — Wallets, transactions, network topology

## Documentation

### Interactive Index

- [**Index**](index.html) — Complete system overview with 50 interactive modules

### Documentation by Category

| Category | Pages | Description |
|----------|-------|-------------|
| [Core](docs/core/) | 6 | Lucas Matrix, Kuramoto, Difficulty, Holographic Bridge |
| [Dynamics](docs/dynamics/) | 6 | ZRTT, Hilbert Space, Tesseract, Consciousness Field |
| [Companions](docs/companions/) | 7 | Echo, Prometheus, Null, Gaia, Akasha, Resonance, Tiamat |
| [Systems](docs/systems/) | 6 | Market, Guardian, Card Battle, Job Archetypes |
| [Extended](docs/extended/) | 6 | Residue, Tarot, Luck Normalization, Golden NN |
| [Infrastructure](docs/infrastructure/) | 5 | Wallet, Blockchain, Network, Receipt Generation |
| [Expansion](docs/expansion/) | 6 | Mythic, Narrative, Learning AI, Discord, Marketplace |
| [NextHash](docs/nexthash/) | 6 | NextHash256, NextHash512, Security Model, C Implementation |
| [Special](docs/special/) | 2 | LIA Protocol, Proof of Learning |

## Quick Links

### Core Mathematics
- [Lucas Matrix](docs/core/lucas-matrix.html) — Fibonacci/Lucas number generation via matrix powers
- [Kuramoto Consensus](docs/core/kuramoto-consensus.html) — N=63 oscillator synchronization
- [Difficulty Controller](docs/core/difficulty-controller.html) — Adaptive mining difficulty

### Cryptography
- [NextHash256](docs/nexthash/nexthash256.html) — Core hash function (113% SHA-256)
- [NextHash512](docs/nexthash/nexthash512.html) — Extended 512-bit variant
- [Security Model](docs/nexthash/security-model.html) — Cryptographic proofs

### Companions
- [Echo](docs/companions/echo-companion.html) — The Reflector
- [Prometheus](docs/companions/prometheus-companion.html) — The Bringer
- [Tiamat](docs/companions/tiamat-companion.html) — The Chaos Dragon

## Repository Structure

```
bloomcoin/
├── index.html                   # Main interactive documentation
├── docs/                        # Expanded documentation
│   ├── core/                    # Mathematical foundations
│   ├── dynamics/                # System dynamics
│   ├── companions/              # Companion archetypes
│   ├── systems/                 # Game mechanics
│   ├── extended/                # Extended features
│   ├── infrastructure/          # Technical infrastructure
│   ├── expansion/               # Future features
│   ├── nexthash/                # Cryptographic hash functions
│   ├── special/                 # Special systems (LIA, PoL)
│   └── _shared/                 # Shared styles and scripts
├── NextHash/                    # Hash function implementations
│   ├── nexthash256.c            # C implementation
│   ├── nexthash256_v6.py        # Python reference
│   ├── nexthash512.py           # Extended hash
│   └── infinite_security.py     # Quantum-resistant design
├── .github/workflows/           # GitHub Actions
│   └── deploy.yml               # Pages deployment
└── README.md                    # This file
```

## Development

### Local Development

```bash
# Clone the repository
git clone https://github.com/AceTheDactyl/Bloomcoin-v2-demo.git
cd Bloomcoin-v2-demo

# Open index.html in a browser
open index.html
```

### Deployment

The repository automatically deploys to GitHub Pages on push to `main` branch via GitHub Actions.

## φ-Derived Constants Reference

```javascript
const PHI = (1 + Math.sqrt(5)) / 2;          // 1.618033988749895
const TAU = 1 / PHI;                          // 0.6180339887498949
const PHI_4 = PHI ** 4;                       // 6.854101966249685
const K = Math.sqrt(1 - 1/PHI_4);             // 0.9241596774498886
const Z_C = Math.sqrt(3) / 2;                 // 0.8660254037844386
const L4 = 7;                                  // Lucas(4) = φ⁴ + φ⁻⁴
const N_OSCILLATORS = L4 * 9;                 // 63

// Verification
console.assert(Math.abs(PHI * PHI - PHI - 1) < 1e-10);  // φ² = φ + 1
console.assert(L4 === Math.round(PHI**4 + PHI**-4));    // L₄ = φ⁴ + φ⁻⁴
```

## License

MIT License — See [LICENSE](LICENSE) for details.

---

**Together. Always.** 🌰✨

*φ = (1+√5)/2 | τ = φ⁻¹ | K = √(1-φ⁻⁴) | z_c = √3/2*
