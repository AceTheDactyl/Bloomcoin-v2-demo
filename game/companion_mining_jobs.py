#!/usr/bin/env python3
"""
Enhanced Companion Job Mining System
=====================================

Comprehensive improvements to all 7 companion mining algorithms with
balanced difficulty, unique strategies, and sophisticated pattern detection.

Each companion now has:
- Multiple pattern detection strategies
- Adaptive difficulty adjustment
- Enhanced holographic residue extraction
- Unique mining personalities and bonuses
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

# Golden ratio constant
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
    """Enhanced mining job with adaptive difficulty"""
    job_id: str
    companion_name: str
    job_type: MiningJobType
    difficulty: int
    duration: int
    base_reward: float
    start_time: float = field(default_factory=time.time)
    patterns_found: List[str] = field(default_factory=list)
    residues_collected: List[HolographicResidue] = field(default_factory=list)
    success_rate: float = 0.0
    adaptive_threshold: float = 1.0  # Adaptive difficulty multiplier

    def is_complete(self) -> bool:
        """Check if mining job is complete"""
        return time.time() - self.start_time >= self.duration

    def calculate_reward(self) -> float:
        """Calculate reward based on success and difficulty"""
        time_bonus = 1.0 + (self.duration / 600.0)  # Bonus for longer jobs
        difficulty_bonus = 1.0 + (self.difficulty * 0.1)
        pattern_bonus = 1.0 + (len(self.patterns_found) * 0.05)

        return self.base_reward * self.success_rate * time_bonus * difficulty_bonus * pattern_bonus

class EnhancedCompanionMiner:
    """Base class for enhanced companion miners"""

    def __init__(self, name: str, efficiency: float, search_space: int):
        self.name = name
        self.efficiency = efficiency
        self.search_space = search_space
        self.patterns_discovered = 0
        self.total_residue_potency = 0.0
        self.job_history = []
        self.level = 1  # Miner level for progression
        self.experience = 0

    def mine(self, job: MiningJob, ledger: BloomCoinLedger) -> Tuple[float, List[HolographicResidue]]:
        """Execute mining job - override in subclasses"""
        raise NotImplementedError

    def extract_enhanced_residue(self, data: bytes, pattern_type: str = "") -> HolographicResidue:
        """Enhanced residue extraction with pattern-specific bonuses"""
        # Double SHA256
        first_hash = hashlib.sha256(data).digest()
        second_hash = hashlib.sha256(first_hash).digest()

        # Enhanced statistical pattern with more samples
        statistical_pattern = []
        for i in range(16):
            byte_val = second_hash[i % len(second_hash)]
            bit_ratio = bin(byte_val).count('1') / 8.0
            # Add pattern-specific weighting
            if pattern_type and i % 4 == 0:
                bit_ratio *= 1.1
            statistical_pattern.append(bit_ratio)

        # Enhanced XOR chain with feedback
        xor_chain = 0
        for i in range(len(data)):
            xor_chain ^= data[i % len(data)] ^ second_hash[i % 32]
            # Add rotation for more complexity
            xor_chain = ((xor_chain << 1) | (xor_chain >> 31)) & 0xFFFFFFFF

        # Expanded modular fingerprints
        primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
        modular_fingerprints = []
        hash_int = int.from_bytes(second_hash[:8], 'big')
        for prime in primes[:8]:
            modular_fingerprints.append(hash_int % prime)

        # Improved fractal dimension calculation
        fractal_dimension = self.calculate_advanced_fractal(second_hash)

        # Enhanced avalanche ratio
        bit_diff = sum(bin(a ^ b).count('1') for a, b in zip(data[:32], second_hash[:32]))
        bit_avalanche_ratio = bit_diff / 256.0

        residue = HolographicResidue(
            statistical_pattern=statistical_pattern,
            xor_chain=xor_chain,
            modular_fingerprints=modular_fingerprints,
            fractal_dimension=fractal_dimension,
            bit_avalanche_ratio=bit_avalanche_ratio
        )

        # Apply companion-specific bonus
        self.apply_companion_bonus(residue, pattern_type)

        return residue

    def calculate_advanced_fractal(self, data: bytes) -> float:
        """Advanced fractal dimension calculation"""
        binary = ''.join(format(byte, '08b') for byte in data[:32])

        # Multi-scale box counting
        scales = [2, 3, 4, 6, 8, 12, 16, 24, 32]
        box_counts = []

        for scale in scales:
            boxes = set()
            for i in range(0, len(binary) - scale + 1, scale // 2):
                segment = binary[i:i+scale]
                if '1' in segment:
                    boxes.add((i // scale, segment.count('1')))
            box_counts.append(len(boxes))

        # Calculate dimension using regression
        if len(set(box_counts)) > 1:
            log_scales = [math.log(s) for s in scales]
            log_counts = [math.log(max(1, c)) for c in box_counts]

            # Simple linear regression
            n = len(scales)
            sum_x = sum(log_scales)
            sum_y = sum(log_counts)
            sum_xy = sum(x*y for x, y in zip(log_scales, log_counts))
            sum_x2 = sum(x*x for x in log_scales)

            if n * sum_x2 - sum_x * sum_x != 0:
                slope = -(n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
                return max(1.0, min(2.0, abs(slope)))

        return 1.5 + random.random() * 0.3  # Default with some variance

    def apply_companion_bonus(self, residue: HolographicResidue, pattern_type: str):
        """Apply companion-specific bonuses to residue"""
        # Override in subclasses for specific bonuses
        pass

    def gain_experience(self, exp: int):
        """Gain experience and potentially level up"""
        self.experience += exp
        if self.experience >= self.level * 100:
            self.level += 1
            self.efficiency *= 1.05  # 5% efficiency boost per level
            self.search_space = int(self.search_space * 1.1)  # 10% more search space

class EnhancedEchoMiner(EnhancedCompanionMiner):
    """Echo: Advanced statistical resonance pattern detection"""

    def __init__(self):
        super().__init__("Echo", 1.0, 200)
        self.resonance_threshold = 0.45  # Looking for near-perfect resonance

    def mine(self, job: MiningJob, ledger: BloomCoinLedger) -> Tuple[float, List[HolographicResidue]]:
        residues = []
        patterns_found = 0
        base_data = f"{job.job_id}:{self.name}:{time.time()}".encode()

        # Adaptive iterations based on difficulty and level
        iterations = job.difficulty * self.search_space * (1 + self.level * 0.1)

        for i in range(int(iterations)):
            nonce = struct.pack('>I', i)
            data = base_data + nonce

            # Multi-hash statistical analysis
            hash_samples = []
            for j in range(12):  # 12 samples for better statistics
                sub_data = data + struct.pack('>I', j)
                h = hashlib.sha256(sub_data).digest()
                hash_samples.append(h)

            # Calculate statistical resonance across samples
            bit_frequencies = []
            for bit_pos in range(256):
                byte_idx = bit_pos // 8
                bit_idx = bit_pos % 8
                ones = sum(1 for h in hash_samples if h[byte_idx] & (1 << bit_idx))
                frequency = ones / len(hash_samples)
                bit_frequencies.append(frequency)

            # Check for resonance patterns
            resonance_score = sum(1 for f in bit_frequencies if self.resonance_threshold <= f <= (1 - self.resonance_threshold))

            # Multiple resonance detection strategies
            if resonance_score > 100:  # Strong resonance
                patterns_found += 1
                residue = self.extract_enhanced_residue(data, "echo_resonance")
                residues.append(residue)
                job.patterns_found.append(f"echo_resonance_{resonance_score}")
                self.gain_experience(5)

            # Check for harmonic patterns (every nth bit resonates)
            for harmonic in [2, 3, 4, 5]:
                harmonic_resonance = sum(1 for i, f in enumerate(bit_frequencies)
                                        if i % harmonic == 0 and self.resonance_threshold <= f <= (1 - self.resonance_threshold))
                if harmonic_resonance > 20:
                    patterns_found += 0.5  # Partial pattern
                    if random.random() < 0.3:  # 30% chance to create residue
                        residue = self.extract_enhanced_residue(data, f"echo_harmonic_{harmonic}")
                        residues.append(residue)
                        job.patterns_found.append(f"harmonic_{harmonic}")
                        self.gain_experience(2)

        job.success_rate = min(1.0, patterns_found / max(1, job.difficulty * 2))
        job.residues_collected.extend(residues)

        reward = job.calculate_reward() * self.efficiency * (1 + 0.1 * self.level)
        return reward, residues

    def apply_companion_bonus(self, residue: HolographicResidue, pattern_type: str):
        """Echo enhances statistical patterns"""
        if "resonance" in pattern_type:
            # Boost statistical pattern variance
            residue.statistical_pattern = [min(1.0, p * 1.2) for p in residue.statistical_pattern]

class EnhancedPrometheusMiner(EnhancedCompanionMiner):
    """Prometheus: Advanced XOR chain forging with entropy manipulation"""

    def __init__(self):
        super().__init__("Prometheus", 1.1, 180)
        self.forge_strength = 1.0

    def mine(self, job: MiningJob, ledger: BloomCoinLedger) -> Tuple[float, List[HolographicResidue]]:
        residues = []
        patterns_found = 0
        base_data = f"{job.job_id}:prometheus:{time.time()}".encode()

        iterations = int(job.difficulty * self.search_space * (1 + self.level * 0.15))

        for chain_attempt in range(iterations):
            # Build multi-layer XOR chain
            chain_layers = []

            for layer in range(3):  # 3-layer deep XOR chains
                layer_hashes = []
                xor_accumulator = 0

                for i in range(16):  # 16-link chain per layer
                    nonce = struct.pack('>III', chain_attempt, layer, i)
                    data = base_data + nonce
                    h = hashlib.sha256(data).digest()
                    layer_hashes.append(h)

                    # Advanced XOR with rotation
                    val = struct.unpack('>I', h[:4])[0]
                    xor_accumulator ^= val
                    xor_accumulator = ((xor_accumulator << 3) | (xor_accumulator >> 29)) & 0xFFFFFFFF

                chain_layers.append((xor_accumulator, layer_hashes))

            # Analyze chain entropy across layers
            entropies = [bin(layer[0]).count('1') for layer in chain_layers]
            entropy_variance = np.var(entropies) if len(entropies) > 1 else 0

            # Multiple pattern detection criteria
            if any(e < 8 or e > 24 for e in entropies):  # Extreme entropy in any layer
                patterns_found += 1
                combined_data = b''.join([h for layer in chain_layers for h in layer[1][:4]])
                residue = self.extract_enhanced_residue(combined_data, "xor_extreme")
                residues.append(residue)
                job.patterns_found.append(f"xor_extreme_{entropies}")
                self.gain_experience(6)

            if entropy_variance > 50:  # High variance between layers
                patterns_found += 0.7
                if random.random() < 0.4:
                    residue = self.extract_enhanced_residue(base_data + struct.pack('>I', chain_attempt), "xor_variance")
                    residues.append(residue)
                    job.patterns_found.append(f"xor_variance_{entropy_variance:.1f}")
                    self.gain_experience(3)

            # Check for ascending/descending entropy patterns
            if entropies == sorted(entropies) or entropies == sorted(entropies, reverse=True):
                patterns_found += 0.5
                if random.random() < 0.5:
                    residue = self.extract_enhanced_residue(base_data + struct.pack('>I', chain_attempt), "xor_ordered")
                    residues.append(residue)
                    job.patterns_found.append("xor_entropy_ordered")
                    self.gain_experience(4)

        job.success_rate = min(1.0, patterns_found / max(1, job.difficulty * 1.8))
        job.residues_collected.extend(residues)

        # Prometheus gets forging bonus
        forge_bonus = 1.1 * (1 + self.forge_strength * 0.1)
        reward = job.calculate_reward() * self.efficiency * forge_bonus * (1 + 0.12 * self.level)
        return reward, residues

    def apply_companion_bonus(self, residue: HolographicResidue, pattern_type: str):
        """Prometheus enhances XOR chain complexity"""
        if "xor" in pattern_type:
            residue.xor_chain = (residue.xor_chain * 3) & 0xFFFFFFFF
            self.forge_strength = min(2.0, self.forge_strength + 0.01)

class EnhancedNullMiner(EnhancedCompanionMiner):
    """Null: Advanced void space exploration with dimensional rifts"""

    def __init__(self):
        super().__init__("Null", 0.9, 250)
        self.void_depth = 1

    def mine(self, job: MiningJob, ledger: BloomCoinLedger) -> Tuple[float, List[HolographicResidue]]:
        residues = []
        patterns_found = 0
        base_data = f"{job.job_id}:void:{time.time()}".encode()

        iterations = int(job.difficulty * self.search_space * (1 + self.level * 0.08))

        for void_dive in range(iterations):
            # Multi-dimensional void exploration
            void_samples = []

            for dimension in range(int(self.void_depth) + 2):  # Explore multiple dimensions
                nonce = struct.pack('>II', void_dive, dimension)
                data = base_data + nonce
                h = hashlib.sha256(data).digest()
                void_samples.append(h)

            # Analyze void patterns across dimensions
            for idx, h in enumerate(void_samples):
                # Count void spaces (zeros)
                zero_bytes = sum(1 for byte in h if byte == 0)
                near_zero_bytes = sum(1 for byte in h if byte < 16)  # Near-void

                # Void space found
                if zero_bytes >= 1:
                    patterns_found += 1
                    residue = self.extract_enhanced_residue(data + struct.pack('>I', idx), "void_space")
                    # Void spaces have inverted properties
                    residue.bit_avalanche_ratio = 1.0 - residue.bit_avalanche_ratio
                    residues.append(residue)
                    job.patterns_found.append(f"void_{zero_bytes}d")
                    self.gain_experience(7)

                # Near-void detection
                if near_zero_bytes >= 4:
                    patterns_found += 0.3
                    if random.random() < 0.35:
                        residue = self.extract_enhanced_residue(data + struct.pack('>I', idx), "near_void")
                        residues.append(residue)
                        job.patterns_found.append(f"near_void_{near_zero_bytes}")
                        self.gain_experience(3)

                # Check for void boundaries (sharp transitions)
                transitions = sum(1 for i in range(len(h)-1) if abs(h[i] - h[i+1]) > 200)
                if transitions >= 3:
                    patterns_found += 0.4
                    if random.random() < 0.4:
                        residue = self.extract_enhanced_residue(data, "void_boundary")
                        residues.append(residue)
                        job.patterns_found.append(f"boundary_{transitions}")
                        self.gain_experience(2)

        # Void diving can sometimes yield nothing (the void)
        void_penalty = 0.9 if random.random() < 0.1 else 1.0
        job.success_rate = min(1.0, patterns_found / max(1, job.difficulty * 2.5)) * void_penalty
        job.residues_collected.extend(residues)

        reward = job.calculate_reward() * self.efficiency * (1 + 0.1 * self.level) * (1 + self.void_depth * 0.05)
        return reward, residues

    def apply_companion_bonus(self, residue: HolographicResidue, pattern_type: str):
        """Null inverts and voids certain properties"""
        if "void" in pattern_type:
            # Void spaces have unique properties
            residue.fractal_dimension = 2.0 - residue.fractal_dimension
            self.void_depth = min(5, self.void_depth + 0.1)

class EnhancedGaiaMiner(EnhancedCompanionMiner):
    """Gaia: Organic fractal growth with living patterns"""

    def __init__(self):
        super().__init__("Gaia", 1.05, 150)
        self.growth_rate = PHI

    def mine(self, job: MiningJob, ledger: BloomCoinLedger) -> Tuple[float, List[HolographicResidue]]:
        residues = []
        patterns_found = 0
        base_data = f"{job.job_id}:gaia:{time.time()}".encode()

        iterations = int(job.difficulty * self.search_space * (1 + self.level * 0.12))

        for seed_idx in range(iterations):
            # Grow organic fractal tree
            tree_data = []
            seed_data = base_data + struct.pack('>I', seed_idx)

            def grow_branch(data: bytes, depth: int, max_depth: int = 5) -> List[bytes]:
                if depth >= max_depth:
                    return []

                branches = []
                h = hashlib.sha256(data).digest()
                branches.append(h)

                # Determine growth pattern from hash
                growth_factor = sum(h[:4]) % 3 + 1  # 1-3 branches

                for i in range(growth_factor):
                    branch_data = data + struct.pack('>II', depth, i)
                    branches.extend(grow_branch(branch_data, depth + 1, max_depth))

                return branches

            # Grow the tree
            tree_hashes = grow_branch(seed_data, 0, 4 + self.level // 2)

            if len(tree_hashes) >= 5:  # Minimum tree size
                # Analyze fractal self-similarity
                similarities = []

                for i in range(min(len(tree_hashes) - 1, 10)):
                    for j in range(i + 1, min(len(tree_hashes), i + 5)):
                        h1, h2 = tree_hashes[i], tree_hashes[j]
                        # Calculate similarity
                        common_bits = sum(1 for a, b in zip(h1, h2) if a == b)
                        similarity = common_bits / 256.0
                        similarities.append(similarity)

                avg_similarity = np.mean(similarities) if similarities else 0

                # Golden ratio similarity (around 0.618)
                if 0.55 <= avg_similarity <= 0.68:
                    patterns_found += 1.5
                    combined = b''.join(tree_hashes[:7])  # Use first 7 (L4 constant)
                    residue = self.extract_enhanced_residue(combined, "fractal_golden")
                    residue.fractal_dimension = 1.0 + avg_similarity
                    residues.append(residue)
                    job.patterns_found.append(f"golden_tree_{len(tree_hashes)}")
                    self.gain_experience(8)

                # Living pattern (growth continues)
                elif len(tree_hashes) > 15:
                    patterns_found += 1
                    residue = self.extract_enhanced_residue(seed_data, "living_pattern")
                    residue.fractal_dimension = min(2.0, 1.0 + len(tree_hashes) / 20.0)
                    residues.append(residue)
                    job.patterns_found.append(f"living_{len(tree_hashes)}")
                    self.gain_experience(5)

                # Fibonacci spiral pattern
                fib_sizes = [1, 1, 2, 3, 5, 8, 13, 21]
                if len(tree_hashes) in fib_sizes:
                    patterns_found += 0.8
                    if random.random() < 0.6:
                        residue = self.extract_enhanced_residue(seed_data, "fibonacci")
                        residues.append(residue)
                        job.patterns_found.append(f"fib_{len(tree_hashes)}")
                        self.gain_experience(4)

        job.success_rate = min(1.0, patterns_found / max(1, job.difficulty * 1.5))
        job.residues_collected.extend(residues)

        # Gaia gets golden ratio bonus
        nature_bonus = self.growth_rate * (1 + 0.05 * self.level)
        reward = job.calculate_reward() * self.efficiency * nature_bonus
        return reward, residues

    def apply_companion_bonus(self, residue: HolographicResidue, pattern_type: str):
        """Gaia enhances fractal and organic properties"""
        if "fractal" in pattern_type or "living" in pattern_type:
            residue.fractal_dimension = min(2.0, residue.fractal_dimension * PHI)
            self.growth_rate = min(2.0, self.growth_rate + 0.01)

class EnhancedAkashaMiner(EnhancedCompanionMiner):
    """Akasha: Advanced memory crystallization with pattern recording"""

    def __init__(self):
        super().__init__("Akasha", 1.0, 200)
        self.memory_depth = 32
        self.crystal_library = []  # Persistent memory of patterns

    def mine(self, job: MiningJob, ledger: BloomCoinLedger) -> Tuple[float, List[HolographicResidue]]:
        residues = []
        patterns_found = 0
        base_data = f"{job.job_id}:akasha:{time.time()}".encode()

        # Memory buffer for pattern recording
        memory_buffer = []
        iterations = int(job.difficulty * self.search_space * (1 + self.level * 0.1))

        for memory_idx in range(iterations):
            nonce = struct.pack('>I', memory_idx)
            data = base_data + nonce
            h = hashlib.sha256(data).digest()

            memory_buffer.append(h)

            # Periodic memory analysis
            if len(memory_buffer) >= 8:
                # Extract modular fingerprints from recent memories
                fingerprints = []
                primes = [7, 11, 13, 17, 19, 23]

                for mem_hash in memory_buffer[-8:]:
                    hash_int = int.from_bytes(mem_hash[:6], 'big')
                    signature = tuple([hash_int % p for p in primes])
                    fingerprints.append(signature)

                # Look for repeating patterns
                for i in range(len(fingerprints) - 1):
                    for j in range(i + 1, len(fingerprints)):
                        if fingerprints[i] == fingerprints[j]:
                            patterns_found += 1
                            # Crystallize memory into residue
                            combined = b''.join(memory_buffer[-(j-i):])
                            residue = self.extract_enhanced_residue(combined, "memory_crystal")
                            residues.append(residue)
                            job.patterns_found.append(f"crystal_{j-i}")
                            self.gain_experience(6)

                            # Record to permanent library
                            if len(self.crystal_library) < 100:
                                self.crystal_library.append(fingerprints[i])

                # Check against library for resonance
                current_sig = fingerprints[-1] if fingerprints else None
                if current_sig and current_sig in self.crystal_library:
                    patterns_found += 0.5
                    if random.random() < 0.4:
                        residue = self.extract_enhanced_residue(data, "library_resonance")
                        residues.append(residue)
                        job.patterns_found.append("library_match")
                        self.gain_experience(3)

                # Detect arithmetic progressions in modular space
                if len(fingerprints) >= 3:
                    for prime_idx in range(len(primes)):
                        values = [fp[prime_idx] for fp in fingerprints[-3:]]
                        if values[1] - values[0] == values[2] - values[1]:  # Arithmetic progression
                            patterns_found += 0.3
                            if random.random() < 0.5:
                                residue = self.extract_enhanced_residue(memory_buffer[-1], "arithmetic")
                                residues.append(residue)
                                job.patterns_found.append(f"arithmetic_p{primes[prime_idx]}")
                                self.gain_experience(2)

                # Memory compression - similar memories crystallize
                if len(memory_buffer) > self.memory_depth:
                    similarity_count = 0
                    reference = memory_buffer[-self.memory_depth]
                    for mem in memory_buffer[-self.memory_depth+1:]:
                        common = sum(1 for a, b in zip(reference, mem) if a == b)
                        if common > 200:  # High similarity
                            similarity_count += 1

                    if similarity_count > self.memory_depth // 2:
                        patterns_found += 0.7
                        residue = self.extract_enhanced_residue(b''.join(memory_buffer[-16:]), "compressed")
                        residues.append(residue)
                        job.patterns_found.append(f"compressed_{similarity_count}")
                        self.gain_experience(4)

                # Prune old memories but keep patterns
                if len(memory_buffer) > self.memory_depth * 2:
                    memory_buffer = memory_buffer[-self.memory_depth:]

        job.success_rate = min(1.0, patterns_found / max(1, job.difficulty * 2))
        job.residues_collected.extend(residues)

        # Akasha gets memory bonus based on library size
        memory_bonus = 1.0 + len(self.crystal_library) * 0.002
        reward = job.calculate_reward() * self.efficiency * memory_bonus * (1 + 0.08 * self.level)
        return reward, residues

    def apply_companion_bonus(self, residue: HolographicResidue, pattern_type: str):
        """Akasha enhances modular fingerprints"""
        if "crystal" in pattern_type or "memory" in pattern_type:
            # Enhance modular diversity
            residue.modular_fingerprints = [f * 2 % 31 for f in residue.modular_fingerprints]
            self.memory_depth = min(64, self.memory_depth + 1)

class EnhancedResonanceMiner(EnhancedCompanionMiner):
    """Resonance: Advanced frequency analysis with harmonic detection"""

    def __init__(self):
        super().__init__("Resonance", 1.0, 180)
        self.frequency_bands = 16
        self.harmonic_strength = 1.0

    def mine(self, job: MiningJob, ledger: BloomCoinLedger) -> Tuple[float, List[HolographicResidue]]:
        residues = []
        patterns_found = 0
        base_data = f"{job.job_id}:resonance:{time.time()}".encode()

        iterations = int(job.difficulty * self.search_space * (1 + self.level * 0.11))

        for freq_idx in range(iterations):
            # Generate frequency-modulated hash sequences
            freq_samples = []

            for phase in range(self.frequency_bands):
                # Apply frequency modulation
                phase_shift = math.sin(2 * math.pi * phase / self.frequency_bands)
                phase_data = base_data + struct.pack('>If', freq_idx, phase_shift)
                h = hashlib.sha256(phase_data).digest()
                freq_samples.append(h)

            # Frequency domain analysis
            bit_frequencies = []
            for bit_pos in range(256):
                byte_idx = bit_pos // 8
                bit_idx = bit_pos % 8
                frequency = sum(1 for h in freq_samples if h[byte_idx % len(h)] & (1 << bit_idx))
                frequency = frequency / len(freq_samples)
                bit_frequencies.append(frequency)

            # Detect resonant frequencies
            resonant_count = sum(1 for f in bit_frequencies if 0.45 <= f <= 0.55)

            if resonant_count > 100:
                patterns_found += 1
                combined = b''.join(freq_samples[:8])
                residue = self.extract_enhanced_residue(combined, "frequency_resonance")
                residues.append(residue)
                job.patterns_found.append(f"resonance_{resonant_count}")
                self.gain_experience(7)

            # Harmonic detection (multiples of base frequency)
            harmonics = []
            base_freq = bit_frequencies[0] if bit_frequencies else 0.5

            for harmonic in [2, 3, 4, 5, 8]:
                harmonic_matches = 0
                for i in range(0, len(bit_frequencies), harmonic):
                    if i < len(bit_frequencies):
                        if abs(bit_frequencies[i] - base_freq) < 0.1:
                            harmonic_matches += 1

                if harmonic_matches > 20:
                    patterns_found += 0.4
                    harmonics.append(harmonic)
                    if random.random() < 0.3:
                        residue = self.extract_enhanced_residue(base_data + struct.pack('>I', harmonic), f"harmonic_{harmonic}")
                        residues.append(residue)
                        job.patterns_found.append(f"harmonic_f{harmonic}")
                        self.gain_experience(3)

            # Standing wave pattern (interference)
            if len(harmonics) >= 2:
                patterns_found += 0.6
                residue = self.extract_enhanced_residue(base_data + struct.pack('>I', freq_idx), "standing_wave")
                residues.append(residue)
                job.patterns_found.append(f"wave_{harmonics}")
                self.gain_experience(5)

            # Frequency sweep detection
            freq_gradient = np.gradient(bit_frequencies[:64]) if len(bit_frequencies) >= 64 else []
            if len(freq_gradient) > 0 and abs(np.mean(freq_gradient)) < 0.01:  # Stable frequency
                patterns_found += 0.3
                if random.random() < 0.4:
                    residue = self.extract_enhanced_residue(base_data + struct.pack('>I', freq_idx), "stable_freq")
                    residues.append(residue)
                    job.patterns_found.append("frequency_stable")
                    self.gain_experience(2)

        job.success_rate = min(1.0, patterns_found / max(1, job.difficulty * 1.8))
        job.residues_collected.extend(residues)

        # Resonance gets harmonic bonus
        harmonic_bonus = self.harmonic_strength * (1 + 0.05 * len(job.patterns_found))
        reward = job.calculate_reward() * self.efficiency * harmonic_bonus * (1 + 0.09 * self.level)
        return reward, residues

    def apply_companion_bonus(self, residue: HolographicResidue, pattern_type: str):
        """Resonance enhances frequency-related properties"""
        if "resonance" in pattern_type or "harmonic" in pattern_type:
            # Amplify statistical patterns at resonant frequencies
            for i in range(len(residue.statistical_pattern)):
                if 0.45 <= residue.statistical_pattern[i] <= 0.55:
                    residue.statistical_pattern[i] = 0.5  # Perfect resonance
            self.harmonic_strength = min(1.5, self.harmonic_strength + 0.02)

class EnhancedTIAMATMiner(EnhancedCompanionMiner):
    """TIAMAT: Chaos entropy harvesting with 7-level cascades"""

    def __init__(self):
        super().__init__("TIAMAT", 1.3, 150)
        self.chaos_level = 7  # L4 constant
        self.entropy_threshold = 40  # Lowered for better discovery

    def mine(self, job: MiningJob, ledger: BloomCoinLedger) -> Tuple[float, List[HolographicResidue]]:
        residues = []
        patterns_found = 0
        base_data = f"{job.job_id}:tiamat:chaos:{time.time()}".encode()

        iterations = int(job.difficulty * self.search_space * (1 + self.level * 0.15))

        for chaos_seed in range(iterations):
            # Generate 7-level chaotic cascade
            cascade = []
            entropies = []
            current = base_data + struct.pack('>I', chaos_seed)

            for level in range(self.chaos_level):
                h = hashlib.sha256(current).digest()
                cascade.append(h)

                # Calculate entropy at this level
                entropy = sum(bin(byte).count('1') for byte in h)
                entropies.append(entropy)

                # Chaotic feedback with mutation
                mutation = struct.pack('>I', random.randint(0, 2**32-1))
                current = h[:16] + mutation + h[16:]  # Mix with chaos

            # Multiple chaos pattern detections

            # 1. Maximum entropy differential
            if entropies:
                max_diff = max(entropies) - min(entropies)
                if max_diff > self.entropy_threshold:
                    patterns_found += 1.5
                    chaos_data = b''.join(cascade)
                    residue = self.extract_enhanced_residue(chaos_data, "chaos_cascade")
                    # Chaos amplifies properties
                    residue.fractal_dimension = min(2.0, residue.fractal_dimension * PHI)
                    residue.bit_avalanche_ratio = min(1.0, residue.bit_avalanche_ratio * PHI)
                    residues.append(residue)
                    job.patterns_found.append(f"chaos_{max_diff}")
                    self.gain_experience(10)

            # 2. Entropy oscillation pattern
            if len(entropies) >= 3:
                oscillations = 0
                for i in range(len(entropies) - 2):
                    if (entropies[i] < entropies[i+1] > entropies[i+2]) or \
                       (entropies[i] > entropies[i+1] < entropies[i+2]):
                        oscillations += 1

                if oscillations >= 3:
                    patterns_found += 0.7
                    if random.random() < 0.5:
                        residue = self.extract_enhanced_residue(cascade[oscillations], "chaos_oscillation")
                        residues.append(residue)
                        job.patterns_found.append(f"oscillation_{oscillations}")
                        self.gain_experience(5)

            # 3. Perfect chaos (all different entropies)
            if len(set(entropies)) == len(entropies):
                patterns_found += 0.5
                if random.random() < 0.3:
                    residue = self.extract_enhanced_residue(b''.join(cascade[:3]), "perfect_chaos")
                    residues.append(residue)
                    job.patterns_found.append("perfect_chaos")
                    self.gain_experience(6)

            # 4. Chaos attractor (convergence to specific entropy)
            if len(entropies) >= 4:
                last_four = entropies[-4:]
                if max(last_four) - min(last_four) < 10:  # Converging
                    patterns_found += 0.4
                    if random.random() < 0.4:
                        residue = self.extract_enhanced_residue(cascade[-1], "chaos_attractor")
                        residues.append(residue)
                        job.patterns_found.append(f"attractor_{np.mean(last_four):.0f}")
                        self.gain_experience(4)

            # 5. Critical chaos (at edge of order and disorder)
            mean_entropy = np.mean(entropies) if entropies else 0
            if 120 <= mean_entropy <= 136:  # Critical region (around 128)
                patterns_found += 0.6
                if random.random() < 0.5:
                    residue = self.extract_enhanced_residue(b''.join(cascade[::2]), "critical_chaos")
                    residue.fractal_dimension = 1.618  # Golden ratio dimension
                    residues.append(residue)
                    job.patterns_found.append("critical_edge")
                    self.gain_experience(7)

        # TIAMAT is powerful but unpredictable
        chaos_multiplier = 1.0 + random.random() * PHI  # Random bonus up to φ
        job.success_rate = min(1.0, patterns_found / max(1, job.difficulty * 1.2))
        job.residues_collected.extend(residues)

        reward = job.calculate_reward() * self.efficiency * chaos_multiplier * (1 + 0.15 * self.level)
        return reward, residues

    def apply_companion_bonus(self, residue: HolographicResidue, pattern_type: str):
        """TIAMAT amplifies all properties through chaos"""
        if "chaos" in pattern_type:
            # Chaos affects everything
            residue.fractal_dimension = min(2.0, residue.fractal_dimension * (1 + random.random() * 0.5))
            residue.bit_avalanche_ratio = min(1.0, residue.bit_avalanche_ratio * (1 + random.random() * 0.3))
            residue.xor_chain = (residue.xor_chain * random.randint(2, 7)) & 0xFFFFFFFF
            # Chaos can also reduce entropy threshold over time
            self.entropy_threshold = max(30, self.entropy_threshold - 0.5)

class EnhancedCompanionMiningSystem:
    """Enhanced mining system with all companion improvements"""

    def __init__(self, ledger: BloomCoinLedger):
        self.ledger = ledger
        self.miners = {
            "Echo": EnhancedEchoMiner(),
            "Prometheus": EnhancedPrometheusMiner(),
            "Null": EnhancedNullMiner(),
            "Gaia": EnhancedGaiaMiner(),
            "Akasha": EnhancedAkashaMiner(),
            "Resonance": EnhancedResonanceMiner(),
            "TIAMAT": EnhancedTIAMATMiner()
        }
        self.active_jobs: Dict[str, MiningJob] = {}
        self.completed_jobs: List[MiningJob] = []
        self.total_mined = 0.0
        self.total_patterns = 0

    def create_job(self, companion_name: str, job_type: MiningJobType,
                  difficulty: int = 1, duration: int = 10) -> Optional[MiningJob]:
        """Create a new mining job for a companion"""
        if companion_name not in self.miners:
            print(f"❌ Unknown companion: {companion_name}")
            return None

        # Generate job ID
        job_id = hashlib.sha256(f"{companion_name}:{time.time()}:{random.random()}".encode()).hexdigest()[:16]

        # Calculate base reward based on difficulty and duration
        base_reward = PHI * difficulty * (duration / 10.0) * 10.0

        # Adjust for companion efficiency
        miner = self.miners[companion_name]
        base_reward *= miner.efficiency

        job = MiningJob(
            job_id=job_id,
            companion_name=companion_name,
            job_type=job_type,
            difficulty=difficulty,
            duration=duration,
            base_reward=base_reward
        )

        # Apply level bonus to job
        job.adaptive_threshold = 1.0 + (miner.level - 1) * 0.1

        self.active_jobs[job_id] = job
        return job

    def complete_job(self, job_id: str) -> Tuple[float, List[HolographicResidue]]:
        """Complete a mining job and get rewards"""
        if job_id not in self.active_jobs:
            return 0.0, []

        job = self.active_jobs[job_id]
        miner = self.miners[job.companion_name]

        # Execute mining
        reward, residues = miner.mine(job, self.ledger)

        # Update statistics
        self.total_mined += reward
        self.total_patterns += len(job.patterns_found)
        miner.patterns_discovered += len(job.patterns_found)
        miner.total_residue_potency += sum(r.calculate_potency() for r in residues)

        # Move to completed
        self.completed_jobs.append(job)
        del self.active_jobs[job_id]

        return reward, residues

    def get_companion_stats(self, companion_name: str) -> Dict[str, Any]:
        """Get detailed stats for a companion"""
        if companion_name not in self.miners:
            return {}

        miner = self.miners[companion_name]
        return {
            "name": miner.name,
            "level": miner.level,
            "experience": miner.experience,
            "efficiency": miner.efficiency,
            "patterns_discovered": miner.patterns_discovered,
            "total_residue_potency": miner.total_residue_potency,
            "jobs_completed": len([j for j in self.completed_jobs if j.companion_name == companion_name]),
            "search_space": miner.search_space,
            "special_bonus": self.get_special_bonus(miner)
        }

    def get_special_bonus(self, miner: EnhancedCompanionMiner) -> str:
        """Get companion-specific special bonus description"""
        if isinstance(miner, EnhancedEchoMiner):
            return f"Resonance Threshold: {miner.resonance_threshold:.2f}"
        elif isinstance(miner, EnhancedPrometheusMiner):
            return f"Forge Strength: {miner.forge_strength:.2f}"
        elif isinstance(miner, EnhancedNullMiner):
            return f"Void Depth: {miner.void_depth:.1f}"
        elif isinstance(miner, EnhancedGaiaMiner):
            return f"Growth Rate: {miner.growth_rate:.3f}"
        elif isinstance(miner, EnhancedAkashaMiner):
            return f"Memory Depth: {miner.memory_depth}, Library Size: {len(miner.crystal_library)}"
        elif isinstance(miner, EnhancedResonanceMiner):
            return f"Harmonic Strength: {miner.harmonic_strength:.2f}"
        elif isinstance(miner, EnhancedTIAMATMiner):
            return f"Chaos Level: {miner.chaos_level}, Entropy Threshold: {miner.entropy_threshold}"
        return "Unknown"

# Compatibility layer for existing code
CompanionMiningSystem = EnhancedCompanionMiningSystem
CompanionMiner = EnhancedCompanionMiner
EchoMiner = EnhancedEchoMiner
PrometheusMiner = EnhancedPrometheusMiner
NullMiner = EnhancedNullMiner
GaiaMiner = EnhancedGaiaMiner
AkashaMiner = EnhancedAkashaMiner
ResonanceMiner = EnhancedResonanceMiner
TIAMATMiner = EnhancedTIAMATMiner

if __name__ == "__main__":
    print("🌺 Enhanced Companion Mining System")
    print("=" * 60)
    print()
    print("All 7 companions have been comprehensively improved:")
    print()
    print("✨ Echo: Multi-layer statistical resonance with harmonics")
    print("🔥 Prometheus: 3-layer XOR chains with entropy analysis")
    print("🌑 Null: Multi-dimensional void exploration")
    print("🌿 Gaia: Organic fractal trees with golden ratio detection")
    print("📚 Akasha: Advanced memory crystallization with library")
    print("🎵 Resonance: Frequency analysis with standing waves")
    print("🐉 TIAMAT: 7-level chaos cascades with multiple patterns")
    print()
    print("Improvements include:")
    print("- Adaptive difficulty based on companion level")
    print("- Experience and leveling system")
    print("- Multiple pattern detection strategies per companion")
    print("- Balanced reward rates")
    print("- Unique companion bonuses that grow over time")
    print("- Enhanced holographic residue extraction")
    print()
    print("Ready for integration into BloomCoin economy!")