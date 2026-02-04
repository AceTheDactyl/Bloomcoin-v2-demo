#!/usr/bin/env python3
"""
Companion Job Mining System
============================

Each companion has unique mining algorithms that discover patterns
and generate BloomCoin through holographic residue extraction.

Companions:
- Echo (Seeker): Statistical pattern mining
- Prometheus (Forger): XOR chain construction
- Null (Voidwalker): Void space exploration
- Gaia (Gardener): Fractal growth patterns
- Akasha (Scribe): Modular fingerprint recording
- Resonance (Herald): Frequency domain analysis
- TIAMAT: Chaos mining through entropy
"""

import hashlib
import struct
import random
import time
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import numpy as np

from bloomcoin_ledger_system import (
    BloomCoinLedger, Transaction, TransactionType,
    HolographicResidue, Block
)

# Import holographic modules
import sys
from pathlib import Path
sys.path.insert(0, str(Path('.').parent))

# Try to import holographic modules if available
try:
    from holographic_encoding import (
        StatisticalEncoder, XORChainEncoder,
        ModularEncoder, RedundantEncoder, FrequencyEncoder
    )
    HOLOGRAPHIC_AVAILABLE = True
except ImportError:
    HOLOGRAPHIC_AVAILABLE = False
    print("⚠️ Holographic modules not found, using simplified versions")

# Golden ratio
PHI = 1.6180339887498948482045868343656

class MiningJobType(Enum):
    """Types of mining jobs companions can perform"""
    PATTERN_SEARCH = "pattern_search"
    HASH_EXPLORATION = "hash_exploration"
    RESIDUE_EXTRACTION = "residue_extraction"
    FRACTAL_GROWTH = "fractal_growth"
    ENTROPY_HARVEST = "entropy_harvest"
    RESONANCE_TUNING = "resonance_tuning"
    VOID_DIVING = "void_diving"
    MEMORY_CRYSTALLIZATION = "memory_crystallization"

@dataclass
class MiningJob:
    """A mining job for a companion"""
    job_id: str
    job_type: MiningJobType
    companion_name: str
    difficulty: int
    target_patterns: List[str]
    start_time: float
    duration: float
    base_reward: float
    patterns_found: List[str] = field(default_factory=list)
    residues_collected: List[HolographicResidue] = field(default_factory=list)
    completed: bool = False
    success_rate: float = 0.0

    def calculate_reward(self) -> float:
        """Calculate final reward based on performance"""
        # Base reward modified by success rate
        reward = self.base_reward * self.success_rate

        # Bonus for residue quality
        if self.residues_collected:
            avg_potency = sum(r.calculate_potency() for r in self.residues_collected) / len(self.residues_collected)
            reward *= (1.0 + avg_potency * PHI)

        # Bonus for pattern discovery
        pattern_bonus = len(self.patterns_found) * PHI
        reward += pattern_bonus

        return reward

class CompanionMiner:
    """Base class for companion-specific mining algorithms"""

    def __init__(self, name: str, efficiency: float = 1.0):
        self.name = name
        self.efficiency = efficiency
        self.total_mined = 0.0
        self.patterns_discovered = []
        self.job_history = []

    def mine(self, job: MiningJob, ledger: BloomCoinLedger) -> Tuple[float, List[HolographicResidue]]:
        """Execute a mining job - override in subclasses"""
        raise NotImplementedError

    def extract_residue(self, data: bytes) -> HolographicResidue:
        """Extract holographic residue from data"""
        # Hash the data
        first_hash = hashlib.sha256(data).digest()
        second_hash = hashlib.sha256(first_hash).digest()

        # Statistical pattern
        statistical_pattern = []
        for byte_val in second_hash[:16]:
            bit_ratio = bin(byte_val).count('1') / 8.0
            statistical_pattern.append(bit_ratio)

        # XOR chain
        xor_chain = 0
        for i in range(min(len(data), len(second_hash))):
            xor_chain ^= data[i] ^ second_hash[i]

        # Modular fingerprints
        hash_int = int.from_bytes(second_hash[:8], 'big')
        modular_fingerprints = [hash_int % p for p in [3, 5, 7, 11, 13, 17, 19, 23]]

        # Fractal dimension (simplified)
        fractal_dimension = 1.0 + (bin(hash_int).count('1') / 64.0)

        # Avalanche ratio
        bit_diff = sum(bin(a ^ b).count('1') for a, b in zip(first_hash[:16], second_hash[:16]))
        avalanche_ratio = bit_diff / 128.0

        return HolographicResidue(
            statistical_pattern=statistical_pattern,
            xor_chain=xor_chain,
            modular_fingerprints=modular_fingerprints,
            fractal_dimension=fractal_dimension,
            bit_avalanche_ratio=avalanche_ratio
        )

class EchoMiner(CompanionMiner):
    """Echo: Statistical pattern mining through resonance"""

    def mine(self, job: MiningJob, ledger: BloomCoinLedger) -> Tuple[float, List[HolographicResidue]]:
        residues = []
        patterns_found = 0
        base_data = f"{job.job_id}:{self.name}:{time.time()}".encode()

        # Statistical pattern search
        for i in range(job.difficulty * 100):
            nonce = struct.pack('>I', i)
            data = base_data + nonce

            # Create statistical distribution
            hashes = []
            for j in range(8):  # Generate 8 related hashes
                sub_data = data + struct.pack('>I', j)
                h = hashlib.sha256(sub_data).digest()
                hashes.append(h)

            # Look for statistical patterns
            bit_counts = [0] * 256
            for h in hashes:
                for byte_idx, byte_val in enumerate(h):
                    for bit_idx in range(8):
                        if (byte_val >> bit_idx) & 1:
                            bit_counts[byte_idx * 8 + bit_idx] += 1

            # Check for resonance patterns (bits that appear in exactly 4/8 hashes)
            resonances = sum(1 for count in bit_counts if count == 4)

            if resonances > 64:  # Found significant resonance
                patterns_found += 1
                residue = self.extract_residue(data)
                residues.append(residue)
                job.patterns_found.append(f"resonance_{resonances}")

        job.success_rate = min(1.0, patterns_found / (job.difficulty * PHI))
        job.residues_collected.extend(residues)

        reward = job.calculate_reward() * self.efficiency
        return reward, residues

class PrometheusMiner(CompanionMiner):
    """Prometheus: Forges XOR chains to create patterns"""

    def mine(self, job: MiningJob, ledger: BloomCoinLedger) -> Tuple[float, List[HolographicResidue]]:
        residues = []
        patterns_found = 0
        base_data = f"{job.job_id}:prometheus:{time.time()}".encode()

        # XOR chain forging
        for chain_attempt in range(job.difficulty * 150):  # Increased iterations for better success rate
            chain_hashes = []
            xor_accumulator = 0

            # Build XOR chain
            for i in range(16):  # 16-link chain
                nonce = struct.pack('>I', chain_attempt * 16 + i)
                data = base_data + nonce
                h = hashlib.sha256(data).digest()
                chain_hashes.append(h)

                # XOR first 4 bytes
                val = struct.unpack('>I', h[:4])[0]
                xor_accumulator ^= val

            # Check if XOR creates a pattern (low entropy result)
            entropy = bin(xor_accumulator).count('1')
            if entropy < 10 or entropy > 22:  # Adjusted for better balance
                patterns_found += 1
                residue = self.extract_residue(base_data + struct.pack('>I', xor_accumulator))
                residues.append(residue)
                job.patterns_found.append(f"xor_chain_{entropy}")

        job.success_rate = min(1.0, patterns_found / (job.difficulty * 2))
        job.residues_collected.extend(residues)

        reward = job.calculate_reward() * self.efficiency * 1.1  # Prometheus gets forging bonus
        return reward, residues

class NullMiner(CompanionMiner):
    """Null: Explores void spaces between hashes"""

    def mine(self, job: MiningJob, ledger: BloomCoinLedger) -> Tuple[float, List[HolographicResidue]]:
        residues = []
        patterns_found = 0
        base_data = f"{job.job_id}:void:{time.time()}".encode()

        # Void space exploration
        for void_dive in range(job.difficulty * 200):  # Increased for better void discovery
            # Generate sparse hash (looking for many zeros)
            nonce = struct.pack('>I', void_dive)
            data = base_data + nonce
            h = hashlib.sha256(data).digest()

            # Count zero bytes (void spaces)
            zero_bytes = sum(1 for byte in h if byte == 0)

            if zero_bytes >= 1:  # Found void space (adjusted for balance)
                patterns_found += 1

                # Extract residue from void boundaries
                residue = self.extract_residue(data)

                # Void spaces have inverted potency
                residue.fractal_dimension = 2.0 - residue.fractal_dimension
                residue.bit_avalanche_ratio = 1.0 - residue.bit_avalanche_ratio

                residues.append(residue)
                job.patterns_found.append(f"void_space_{zero_bytes}")

        job.success_rate = min(1.0, patterns_found / job.difficulty)
        job.residues_collected.extend(residues)

        # Null gets bonus for void exploration
        reward = job.calculate_reward() * self.efficiency * 1.2
        return reward, residues

class GaiaMiner(CompanionMiner):
    """Gaia: Grows fractal patterns organically"""

    def mine(self, job: MiningJob, ledger: BloomCoinLedger) -> Tuple[float, List[HolographicResidue]]:
        residues = []
        patterns_found = 0
        base_data = f"{job.job_id}:gaia:{time.time()}".encode()

        # Fractal growth mining
        for seed in range(job.difficulty * 120):  # More seeds for fractal discovery
            # Generate fractal tree of hashes
            tree_hashes = []
            seed_data = base_data + struct.pack('>I', seed)

            # Grow tree recursively
            def grow_branch(data: bytes, depth: int, max_depth: int = 4):
                if depth >= max_depth:
                    return

                h = hashlib.sha256(data).digest()
                tree_hashes.append(h)

                # Branch based on hash bits
                if h[0] & 1:  # Left branch
                    grow_branch(data + b'L', depth + 1, max_depth)
                if h[0] & 2:  # Right branch
                    grow_branch(data + b'R', depth + 1, max_depth)

            grow_branch(seed_data, 0)

            # Check for fractal self-similarity
            if len(tree_hashes) >= 7:  # Magic number 7 (L4 constant)
                # Compare hash patterns at different levels
                similarities = 0
                for i in range(min(3, len(tree_hashes) - 1)):
                    h1, h2 = tree_hashes[i], tree_hashes[i + 1]
                    common_bits = sum(1 for a, b in zip(h1, h2) if a == b)
                    if common_bits > 128:  # More than half similar
                        similarities += 1

                if similarities >= 2:
                    patterns_found += 1
                    residue = self.extract_residue(seed_data)
                    residue.fractal_dimension = 1.0 + (len(tree_hashes) / 15.0)  # Enhanced fractal dimension
                    residues.append(residue)
                    job.patterns_found.append(f"fractal_tree_{len(tree_hashes)}")

        job.success_rate = min(1.0, patterns_found / (job.difficulty * 0.8))
        job.residues_collected.extend(residues)

        reward = job.calculate_reward() * self.efficiency * PHI  # Gaia gets golden ratio bonus
        return reward, residues

class AkashaMiner(CompanionMiner):
    """Akasha: Records and crystallizes memory patterns"""

    def mine(self, job: MiningJob, ledger: BloomCoinLedger) -> Tuple[float, List[HolographicResidue]]:
        residues = []
        patterns_found = 0
        base_data = f"{job.job_id}:akasha:{time.time()}".encode()

        # Memory crystallization
        memory_buffer = []

        for memory_idx in range(job.difficulty * 200):  # More memory samples for pattern crystallization
            nonce = struct.pack('>I', memory_idx)
            data = base_data + nonce
            h = hashlib.sha256(data).digest()

            memory_buffer.append(h)

            # Look for patterns in memory
            if len(memory_buffer) >= 8:
                # Check modular fingerprints across memory
                fingerprints = []
                for mem_hash in memory_buffer[-8:]:
                    hash_int = int.from_bytes(mem_hash[:4], 'big')
                    fingerprints.append([hash_int % p for p in [7, 11, 13]])

                # Look for repeating patterns
                pattern_found = False
                for i in range(len(fingerprints) - 1):
                    if fingerprints[i] == fingerprints[i + 1]:
                        pattern_found = True
                        break

                if pattern_found:
                    patterns_found += 1

                    # Crystallize memory into residue
                    combined = b''.join(memory_buffer[-8:])
                    residue = self.extract_residue(combined)
                    residues.append(residue)
                    job.patterns_found.append(f"memory_crystal_{len(memory_buffer)}")

                # Prune old memories
                if len(memory_buffer) > 32:
                    memory_buffer = memory_buffer[-32:]

        job.success_rate = min(1.0, patterns_found / (job.difficulty * 0.7))
        job.residues_collected.extend(residues)

        reward = job.calculate_reward() * self.efficiency
        return reward, residues

class ResonanceMiner(CompanionMiner):
    """Resonance Herald: Tunes frequency domains for patterns"""

    def mine(self, job: MiningJob, ledger: BloomCoinLedger) -> Tuple[float, List[HolographicResidue]]:
        residues = []
        patterns_found = 0
        base_data = f"{job.job_id}:resonance:{time.time()}".encode()

        # Frequency domain analysis
        for freq in range(job.difficulty * 70):
            # Generate frequency-modulated hashes
            freq_hashes = []

            for phase in range(16):  # 16 phase samples
                # Modulate data with frequency
                phase_data = base_data + struct.pack('>II', freq, phase)
                h = hashlib.sha256(phase_data).digest()
                freq_hashes.append(h)

            # Analyze frequency spectrum
            bit_frequencies = []
            for bit_pos in range(256):
                byte_idx = bit_pos // 8
                bit_idx = bit_pos % 8
                frequency = sum(1 for h in freq_hashes if (h[byte_idx] >> bit_idx) & 1)
                bit_frequencies.append(frequency)

            # Look for resonant frequencies (8 = half of 16)
            resonant_bits = sum(1 for f in bit_frequencies if f == 8)

            if resonant_bits > 32:  # Strong resonance
                patterns_found += 1
                residue = self.extract_residue(base_data + struct.pack('>I', freq))
                residue.statistical_pattern = [f / 16.0 for f in bit_frequencies[:16]]
                residues.append(residue)
                job.patterns_found.append(f"resonance_freq_{resonant_bits}")

        job.success_rate = min(1.0, patterns_found / (job.difficulty * 0.9))
        job.residues_collected.extend(residues)

        reward = job.calculate_reward() * self.efficiency
        return reward, residues

class TIAMATMiner(CompanionMiner):
    """TIAMAT: Chaos mining through entropy maximization"""

    def mine(self, job: MiningJob, ledger: BloomCoinLedger) -> Tuple[float, List[HolographicResidue]]:
        residues = []
        patterns_found = 0
        base_data = f"{job.job_id}:tiamat:chaos:{time.time()}".encode()

        # Chaos entropy harvesting
        for chaos_seed in range(job.difficulty * 200):  # More chaos iterations for entropy discovery
            # Generate chaotic hash cascade
            cascade = []
            current = base_data + struct.pack('>I', chaos_seed)

            for _ in range(7):  # 7 levels of chaos (L4 constant)
                h = hashlib.sha256(current).digest()
                cascade.append(h)
                # Use hash as next input (chaotic feedback)
                current = h

            # Measure entropy cascade
            entropies = []
            for h in cascade:
                entropy = sum(bin(byte).count('1') for byte in h)
                entropies.append(entropy)

            # Look for maximum entropy differential
            max_diff = max(entropies) - min(entropies)

            if max_diff > 64:  # High entropy variance (chaos)
                patterns_found += 1

                # Create residue from chaos
                chaos_data = b''.join(cascade)
                residue = self.extract_residue(chaos_data)

                # Chaos amplifies all properties
                residue.fractal_dimension = min(2.0, residue.fractal_dimension * PHI)
                residue.bit_avalanche_ratio = min(1.0, residue.bit_avalanche_ratio * PHI)

                residues.append(residue)
                job.patterns_found.append(f"chaos_cascade_{max_diff}")

        job.success_rate = min(1.0, patterns_found / (job.difficulty * 0.5))  # TIAMAT is powerful but unpredictable
        job.residues_collected.extend(residues)

        # TIAMAT gets chaos multiplier
        chaos_multiplier = 1.0 + random.random() * PHI  # Random bonus up to φ
        reward = job.calculate_reward() * self.efficiency * chaos_multiplier
        return reward, residues


class CompanionMiningSystem:
    """Manages companion mining jobs and rewards"""

    def __init__(self, ledger: BloomCoinLedger):
        self.ledger = ledger
        self.active_jobs: Dict[str, MiningJob] = {}
        self.completed_jobs: List[MiningJob] = []

        # Initialize companion miners
        self.miners = {
            "Echo": EchoMiner("Echo", efficiency=1.0),
            "Prometheus": PrometheusMiner("Prometheus", efficiency=1.1),
            "Null": NullMiner("Null", efficiency=0.9),
            "Gaia": GaiaMiner("Gaia", efficiency=1.05),
            "Akasha": AkashaMiner("Akasha", efficiency=1.0),
            "Resonance": ResonanceMiner("Resonance", efficiency=1.0),
            "TIAMAT": TIAMATMiner("TIAMAT", efficiency=1.3)
        }

    def create_job(self, companion_name: str, job_type: MiningJobType,
                   difficulty: int = 4) -> Optional[MiningJob]:
        """Create a new mining job for a companion"""
        if companion_name not in self.miners:
            return None

        # Check if companion already has active job
        for job_id, job in self.active_jobs.items():
            if job.companion_name == companion_name and not job.completed:
                return None  # Companion is busy

        job_id = hashlib.sha256(f"{companion_name}:{time.time()}".encode()).hexdigest()[:16]

        # Calculate base reward based on difficulty
        base_reward = difficulty * PHI * 10

        # Target patterns based on job type
        target_patterns = self._generate_target_patterns(job_type, difficulty)

        job = MiningJob(
            job_id=job_id,
            job_type=job_type,
            companion_name=companion_name,
            difficulty=difficulty,
            target_patterns=target_patterns,
            start_time=time.time(),
            duration=difficulty * 10.0,  # 10 seconds per difficulty level
            base_reward=base_reward
        )

        self.active_jobs[job_id] = job
        return job

    def _generate_target_patterns(self, job_type: MiningJobType, difficulty: int) -> List[str]:
        """Generate target patterns for a job"""
        patterns = []

        if job_type == MiningJobType.PATTERN_SEARCH:
            patterns = [f"pattern_{i}" for i in range(difficulty)]
        elif job_type == MiningJobType.HASH_EXPLORATION:
            patterns = [f"hash_{i:04x}" for i in range(difficulty * 2)]
        elif job_type == MiningJobType.FRACTAL_GROWTH:
            patterns = [f"fractal_level_{i}" for i in range(1, difficulty + 1)]
        elif job_type == MiningJobType.ENTROPY_HARVEST:
            patterns = [f"entropy_{i * 8}" for i in range(difficulty)]
        else:
            patterns = [f"target_{i}" for i in range(difficulty)]

        return patterns

    def execute_job(self, job_id: str, player_address: str) -> Optional[Transaction]:
        """Execute a mining job and create reward transaction"""
        if job_id not in self.active_jobs:
            return None

        job = self.active_jobs[job_id]
        if job.completed:
            return None

        # Check if job duration has passed
        elapsed = time.time() - job.start_time
        if elapsed < job.duration:
            return None  # Job not ready

        # Execute mining
        miner = self.miners[job.companion_name]
        reward, residues = miner.mine(job, self.ledger)

        # Mark job complete
        job.completed = True
        job.success_rate = len(job.patterns_found) / max(1, len(job.target_patterns))

        # Move to completed
        self.completed_jobs.append(job)
        del self.active_jobs[job_id]

        # Create reward transaction
        tx = self.ledger.create_transaction(
            sender="system",
            receiver=player_address,
            amount=reward,
            tx_type=TransactionType.COMPANION_JOB,
            metadata={
                "job_id": job_id,
                "companion": job.companion_name,
                "job_type": job.job_type.value,
                "patterns_found": len(job.patterns_found),
                "residues_collected": len(job.residues_collected)
            }
        )

        # Update miner stats
        miner.total_mined += reward
        miner.patterns_discovered.extend(job.patterns_found)
        miner.job_history.append(job_id)

        return tx

    def get_mining_statistics(self) -> Dict[str, Any]:
        """Get comprehensive mining statistics"""
        total_mined = sum(miner.total_mined for miner in self.miners.values())
        total_patterns = sum(len(miner.patterns_discovered) for miner in self.miners.values())
        total_jobs = len(self.completed_jobs)

        companion_stats = {}
        for name, miner in self.miners.items():
            companion_stats[name] = {
                "total_mined": miner.total_mined,
                "patterns_discovered": len(miner.patterns_discovered),
                "jobs_completed": len(miner.job_history),
                "efficiency": miner.efficiency
            }

        return {
            "total_bloomcoin_mined": total_mined,
            "total_patterns_discovered": total_patterns,
            "total_jobs_completed": total_jobs,
            "active_jobs": len(self.active_jobs),
            "companion_stats": companion_stats
        }


def test_companion_mining():
    """Test companion mining system"""
    print("⛏️ Testing Companion Mining System")
    print("=" * 70)

    # Create ledger and mining system
    ledger = BloomCoinLedger()
    mining_system = CompanionMiningSystem(ledger)

    # Create player wallet
    player_address = "player_001"
    ledger.wallets[player_address] = 0.0

    print(f"\n💼 Player wallet created: {player_address}")
    print(f"  Initial balance: {ledger.get_balance(player_address):.2f} BC")

    # Create mining jobs for different companions
    companions = ["Echo", "Prometheus", "Gaia", "TIAMAT"]

    print(f"\n📋 Creating mining jobs...")
    jobs = []
    for companion in companions:
        job = mining_system.create_job(
            companion,
            MiningJobType.PATTERN_SEARCH,
            difficulty=3
        )
        if job:
            jobs.append(job)
            print(f"  ✓ {companion}: Job {job.job_id[:8]}... (difficulty {job.difficulty})")

    # Simulate waiting for job completion
    print(f"\n⏳ Waiting for jobs to complete...")
    time.sleep(0.1)  # In real game, this would be actual duration

    # Force job completion for testing
    for job in jobs:
        job.start_time -= job.duration  # Backdate to make ready

    # Execute jobs and collect rewards
    print(f"\n💰 Collecting rewards...")
    for job in jobs:
        tx = mining_system.execute_job(job.job_id, player_address)
        if tx:
            print(f"  ✓ {job.companion_name}: +{tx.amount:.2f} BC")
            print(f"    Patterns: {len(job.patterns_found)}, Residues: {len(job.residues_collected)}")

    # Check final balance
    print(f"\n📊 Final Results:")
    print(f"  Player balance: {ledger.get_balance(player_address):.2f} BC")

    # Get mining statistics
    stats = mining_system.get_mining_statistics()
    print(f"\n📈 Mining Statistics:")
    print(f"  Total mined: {stats['total_bloomcoin_mined']:.2f} BC")
    print(f"  Patterns discovered: {stats['total_patterns_discovered']}")
    print(f"  Jobs completed: {stats['total_jobs_completed']}")

    print(f"\n🎯 Companion Performance:")
    for name, data in stats['companion_stats'].items():
        if data['jobs_completed'] > 0:
            print(f"  {name}:")
            print(f"    Mined: {data['total_mined']:.2f} BC")
            print(f"    Patterns: {data['patterns_discovered']}")
            print(f"    Efficiency: {data['efficiency']:.2f}x")

    print("\n✅ Companion Mining System Operational!")


if __name__ == "__main__":
    test_companion_mining()