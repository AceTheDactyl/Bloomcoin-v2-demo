Now I'll create a comprehensive research document on the GARDEN CONSENSUS system based on my analysis of the code. Let me compile all the findings:

---

# GARDEN CONSENSUS SYSTEM: Mathematical Foundations of Proof-of-Learning

## Executive Summary

The GARDEN CONSENSUS system implements **Proof-of-Learning (PoL)**, a novel consensus mechanism where AI agents validate each other's learning through dialogue, challenge-response verification, and reputation tracking. Unlike traditional blockchain consensus (Proof-of-Work, Proof-of-Stake), GARDEN uses collaborative validation based on demonstrated knowledge and agent coherence within the network.

This document provides comprehensive technical foundations covering the consensus protocol architecture, learning verification mechanisms, validator network dynamics, and the theoretical evolution from the earlier Proof-of-Coherence system.

---

## 1. Consensus Protocol Architecture

### 1.1 ConsensusType Enumeration

The GARDEN system supports multiple consensus mechanisms through the `ConsensusType` enum:

```python
class ConsensusType(Enum):
    PROOF_OF_LEARNING = "pol"         # AI validates by testing knowledge
    WITNESS_BASED = "witness"         # Direct witnesses confirm event
    COHERENCE_BASED = "coherence"     # Based on coherence with collective
    REPUTATION_BASED = "reputation"   # Weighted by agent reputation
    HYBRID = "hybrid"                 # Combination of methods
```

#### Mechanism Descriptions

| Type | Description | Use Case |
|------|-------------|----------|
| **PROOF_OF_LEARNING** | Validators issue challenges (questions, demonstrations, verifications) to test the learning claim's validity | Primary mechanism for validating bloom events |
| **WITNESS_BASED** | Direct observation and confirmation by agents present during the learning event | Teaching scenarios where teacher is automatic witness |
| **COHERENCE_BASED** | Validation based on alignment with collective knowledge (z_c = √3/2 ≈ 0.866) | Network-wide consensus on knowledge coherence |
| **REPUTATION_BASED** | Weighted voting by agent reputation scores (φ⁻¹ ≈ 0.618) | Incentivizes consistent validation accuracy |
| **HYBRID** | Combination of above methods | Default approach; balances reliability and scalability |

The hybrid approach is the default, integrating multiple validation pathways for robust consensus.

### 1.2 ConsensusRules: Mathematical Foundations

The `ConsensusRules` dataclass encodes the protocol's parameters, grounded in the golden ratio φ and critical coherence thresholds:

```python
@dataclass
class ConsensusRules:
    min_validators: int = 1              # Minimum validators required
    max_validators: int = 7              # Maximum validators considered
    validation_timeout: float = 300.0    # Seconds to wait for validation
    coherence_threshold: float = 0.866   # z_c = √3/2 critical coherence
    reputation_weight: float = 0.618     # φ - 1 (golden ratio conjugate)
    consensus_threshold: float = 0.667   # 2/3 majority required
    challenge_difficulty: int = 3        # Difficulty of learning challenges
```

#### Mathematical Basis

| Parameter | Mathematical Definition | Significance |
|-----------|--------------------------|--------------|
| **coherence_threshold (z_c)** | √3/2 ≈ 0.866 | Critical threshold from Kuramoto model; represents the synchronization point where consensus "blooms" |
| **reputation_weight** | φ⁻¹ ≈ 0.618 | Golden ratio conjugate; controls exponential decay of reputation influence |
| **consensus_threshold** | 2/3 ≈ 0.667 | Byzantine fault tolerance threshold; ensures majority consensus with room for dissent |

#### Validator Selection Algorithm

The system uses **logarithmic scaling** for network efficiency:

```
required_validators(N) = {
    1                    if N < 3
    2                    if 3 ≤ N < 10
    min(3, max_v)        if 10 ≤ N < 50
    min(⌊log₂(N)⌋, 7)    if N ≥ 50
}
```

This ensures:
- Small networks (N < 50): 1-3 validators for rapid consensus
- Large networks (N ≥ 50): logarithmic growth O(log N) preventing validator overload
- Maximum 7 validators to avoid Byzantine complexity

---

## 2. Proof-of-Learning: Challenge-Response Validation

### 2.1 Learning Challenge Structure

The `LearningChallenge` dataclass represents verification challenges:

```python
@dataclass
class LearningChallenge:
    challenge_id: str              # Unique identifier
    challenge_type: str            # "question\