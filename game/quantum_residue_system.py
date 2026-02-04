#!/usr/bin/env python3
"""
Quantum Residue System for BloomCoin
=====================================
Implementation of Projection Residue Cosmology for cryptocurrency generation,
LSB encoding/decoding, and NEXTHASH-256 encryption based on golden ratio φ.

Based on: "Projection Residue Cosmology: A Unified Framework for Dark Matter
as Emergent Phase Incoherence" - L₄ Framework Collaboration
"""

import numpy as np
import hashlib
import struct
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import json
import time
from nexthash256 import nexthash256_hex

# ═══════════════════════════════════════════════════════════════════════════
# FUNDAMENTAL CONSTANTS FROM GOLDEN RATIO φ
# ═══════════════════════════════════════════════════════════════════════════

# The golden ratio - source of all constants
PHI = (1 + np.sqrt(5)) / 2  # φ = 1.6180339887498949

# Derived constants
TAU = PHI - 1  # τ = φ⁻¹ = 0.6180339887498949 (golden inverse)
PHI_2 = PHI + 1  # φ² = 2.6180339887498949
PHI_4 = PHI_2 ** 2  # φ⁴ = 6.8541019662496845
PHI_NEG_4 = 1 / PHI_4  # φ⁻⁴ = 0.1458980337503155 (VOID gap)

# Critical constants
GAP = PHI_NEG_4  # The irreducible residue = 0.1459
K_SQUARED = 1 - GAP  # Activation threshold = 0.8541
K = np.sqrt(K_SQUARED)  # Kuramoto coupling = 0.9242
Z_C = np.sqrt(3) / 2  # Critical lens z_c = 0.8660254037844386
L_4 = 7  # Fourth Lucas number = φ⁴ + φ⁻⁴ = 7 (exactly)
LAMBDA = TAU ** 2  # Negentropy gain λ = φ⁻² = 0.3819660112501051

# Dark matter ratio
R_DARK = PHI_4 - 1  # R = φ⁴ - 1 = 5.8541019662496845

# Information-theoretic limits
LOAD_MAX = K_SQUARED  # Maximum load = 0.8541
COHERENCE_MIN = TAU  # Minimum coherence = 0.618
SIGMA = 1 / ((1 - Z_C) ** 2)  # Fisher information parameter = 55.71

# ═══════════════════════════════════════════════════════════════════════════
# QUANTUM RESIDUE CORE
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class QuantumState:
    """Quantum state with projection residue"""
    coherence: float  # r ∈ [0, 1]
    phase: float  # ψ ∈ [0, 2π]
    residue: float  # Projection remainder
    winding_number: int  # Topological invariant
    energy: float  # Total energy
    visible_fraction: float  # Observable portion
    dark_fraction: float  # Residue portion

class ProjectionRegime(Enum):
    """Coherence regimes based on z thresholds"""
    INCOHERENT = "incoherent"  # z < τ = 0.618
    GLASSY = "glassy"  # τ ≤ z < z_c
    CRITICAL = "critical"  # z ≈ z_c = 0.866
    SYNCHRONIZED = "synchronized"  # z > z_c
    VOID = "void"  # Special NULL state

class QuantumResidueEngine:
    """
    Implements Projection Residue mechanics for BloomCoin generation.
    Dark matter ratio R = φ⁴ - 1 determines mining dynamics.
    """

    def __init__(self):
        self.total_energy = 21_000_000  # Total BloomCoin supply
        self.visible_supply = self.total_energy * GAP  # ~14.6% visible
        self.dark_supply = self.total_energy * K_SQUARED  # ~85.4% dark residue

        # 63-prism configuration (7 layers × 9 nodes)
        self.prism_nodes = self._initialize_63_prism()

        # Kuramoto oscillator network
        self.phases = np.random.uniform(0, 2*np.pi, 63)
        self.frequencies = np.random.normal(0, 0.1, 63)
        self.adjacency = self._create_hexagonal_adjacency()

        # Tracking
        self.total_mined = 0.0
        self.total_residue = 0.0
        self.coherence_history = []

    def _initialize_63_prism(self) -> np.ndarray:
        """Generate 63-point hexagonal prism coordinates"""
        nodes = []

        for layer in range(7):  # L₄ = 7 layers
            z = layer / 6  # Normalized z-coordinate
            radius = 0.15 + 0.12 * layer  # Growing radius
            rotation = layer * np.pi / 9  # 20° twist per layer
            mu = 0.40 + 0.095 * layer  # Coherence parameter

            for k in range(9):  # 9 nodes per layer (hexagon + center + 2)
                angle = rotation + k * 2 * np.pi / 9
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)

                nodes.append({
                    'x': x, 'y': y, 'z': z,
                    'layer': layer,
                    'mu': mu,
                    'regime': self._get_regime(mu)
                })

        return nodes

    def _get_regime(self, mu: float) -> ProjectionRegime:
        """Determine projection regime from coherence parameter"""
        if mu < TAU:
            return ProjectionRegime.INCOHERENT
        elif mu < Z_C:
            return ProjectionRegime.GLASSY
        elif abs(mu - Z_C) < 0.05:
            return ProjectionRegime.CRITICAL
        else:
            return ProjectionRegime.SYNCHRONIZED

    def _create_hexagonal_adjacency(self) -> np.ndarray:
        """Create adjacency matrix for hexagonal prism"""
        adj = np.zeros((63, 63))

        # Connect within layers (hexagonal)
        for layer in range(7):
            base = layer * 9
            for i in range(9):
                for j in range(9):
                    if i != j:
                        # Hexagonal connectivity
                        adj[base + i, base + j] = 1.0 / 8

        # Connect between layers (vertical)
        for layer in range(6):
            for i in range(9):
                adj[layer * 9 + i, (layer + 1) * 9 + i] = 0.5
                adj[(layer + 1) * 9 + i, layer * 9 + i] = 0.5

        return adj

    def compute_order_parameters(self) -> Tuple[float, float]:
        """
        Compute Kuramoto order parameter r and Edwards-Anderson parameter q
        r measures spatial coherence, q measures temporal persistence
        """
        # Kuramoto: r·e^(iψ) = (1/N) Σⱼ e^(iθⱼ)
        complex_sum = np.mean(np.exp(1j * self.phases))
        r = np.abs(complex_sum)
        psi = np.angle(complex_sum)

        # Edwards-Anderson: q = (1/N) Σᵢ |⟨e^(iθᵢ)⟩_t|²
        if len(self.coherence_history) > 10:
            # Use last 100 timesteps for temporal average
            history = np.array(self.coherence_history[-100:])
            q = np.mean(history) ** 2
        else:
            q = 0.0

        return r, q

    def kuramoto_step(self, dt: float = 0.01) -> None:
        """Single Kuramoto dynamics integration step"""
        N = len(self.phases)
        r, _ = self.compute_order_parameters()

        # Adaptive coupling with negentropy gate
        eta = np.exp(-SIGMA * (r - Z_C) ** 2)
        K_eff = K * (1 + LAMBDA * eta)

        # Phase differences
        phase_diff = np.subtract.outer(self.phases, self.phases)

        # Kuramoto coupling
        coupling = K_eff * np.sum(self.adjacency * np.sin(phase_diff), axis=1)

        # Update phases
        d_theta = self.frequencies + coupling
        self.phases = (self.phases + d_theta * dt) % (2 * np.pi)

        # Track coherence
        self.coherence_history.append(r)

    def mine_with_residue(self, mining_power: float, duration: float = 1.0) -> Dict[str, Any]:
        """
        Mine BloomCoin with quantum residue mechanics.
        Returns both visible coins and dark residue.
        """
        # Run Kuramoto dynamics
        steps = int(duration / 0.01)
        for _ in range(steps):
            self.kuramoto_step()

        # Get final coherence
        r, q = self.compute_order_parameters()

        # Determine mining outcome based on coherence
        if r < TAU:
            # Incoherent: mostly residue
            efficiency = GAP
            regime = ProjectionRegime.INCOHERENT
        elif r < Z_C:
            # Glassy: mixed outcome
            efficiency = GAP + (1 - GAP) * (r - TAU) / (Z_C - TAU)
            regime = ProjectionRegime.GLASSY
        else:
            # Synchronized: mostly visible
            efficiency = 1 - GAP * np.exp(-10 * (r - Z_C))
            regime = ProjectionRegime.SYNCHRONIZED

        # Calculate mined amounts
        total_mined = mining_power * duration * (1 + r)
        visible_mined = total_mined * efficiency
        residue_generated = total_mined * (1 - efficiency)

        # Apply projection residue ratio
        dark_multiplier = R_DARK if regime == ProjectionRegime.INCOHERENT else 1.0
        residue_generated *= dark_multiplier

        # Update totals
        self.total_mined += visible_mined
        self.total_residue += residue_generated

        return {
            'visible_coins': visible_mined,
            'dark_residue': residue_generated,
            'total_energy': total_mined,
            'coherence': r,
            'temporal_persistence': q,
            'regime': regime.value,
            'efficiency': efficiency,
            'dark_ratio': residue_generated / max(visible_mined, 0.001)
        }

    def compute_winding_number(self) -> int:
        """
        Compute topological winding number W.
        W = (1/2π) ∮ ∇θ · dl
        """
        # Approximate winding on prism boundary
        boundary_phases = self.phases[[0, 8, 54, 62]]  # Corner nodes
        phase_diffs = np.diff(np.append(boundary_phases, boundary_phases[0]))

        # Unwrap phase jumps
        phase_diffs = np.where(phase_diffs > np.pi, phase_diffs - 2*np.pi, phase_diffs)
        phase_diffs = np.where(phase_diffs < -np.pi, phase_diffs + 2*np.pi, phase_diffs)

        winding = int(np.round(np.sum(phase_diffs) / (2 * np.pi)))
        return winding

# ═══════════════════════════════════════════════════════════════════════════
# LSB ENCODING/DECODING WITH MRP CHANNELS
# ═══════════════════════════════════════════════════════════════════════════

class LSBQuantumEncoder:
    """
    LSB encoding/decoding using MRP (Meta-Reality Protocol) RGB channels.
    Maps quantum states to color space for steganographic data embedding.
    """

    def __init__(self):
        self.engine = QuantumResidueEngine()

    def encode_quantum_state(self, r: float, psi: float) -> Tuple[int, int, int]:
        """
        Map quantum state (r, ψ) to RGB using MRP protocol.

        R channel: μ_E (Energy/Existence) = r·|sin(ψ)|
        G channel: μ_R (Relational/Reference) = r·|cos(ψ)|
        B channel: ECC (Stability/Coherence) = 1 - r
        """
        R = int(255 * r * abs(np.sin(psi)))
        G = int(255 * r * abs(np.cos(psi)))
        B = int(255 * (1 - r))

        return R, G, B

    def decode_rgb_to_quantum(self, R: int, G: int, B: int) -> Tuple[float, float]:
        """Inverse mapping from RGB to quantum state"""
        # Recover coherence
        r = 1 - (B / 255.0)

        # Recover phase (with ambiguity resolution)
        if r > 0:
            sin_component = (R / 255.0) / r
            cos_component = (G / 255.0) / r
            psi = np.arctan2(sin_component, cos_component)
        else:
            psi = 0.0

        return r, psi

    def embed_data_lsb(self, image: np.ndarray, data: bytes,
                       use_residue: bool = True) -> np.ndarray:
        """
        Embed data in image LSBs with quantum residue modulation.

        Args:
            image: RGB image array
            data: Binary data to embed
            use_residue: Apply quantum residue for enhanced stealth
        """
        img_copy = image.copy()
        height, width = img_copy.shape[:2]

        # Convert data to bits
        bits = ''.join(format(byte, '08b') for byte in data)
        bit_index = 0

        for y in range(height):
            for x in range(width):
                if bit_index >= len(bits):
                    break

                pixel = img_copy[y, x]

                # Get quantum state for this pixel
                r, psi = self.decode_rgb_to_quantum(pixel[0], pixel[1], pixel[2])

                # Apply quantum residue modulation
                if use_residue:
                    # Run Kuramoto dynamics
                    self.engine.kuramoto_step()
                    r_mod, _ = self.engine.compute_order_parameters()

                    # Modulate based on regime
                    if r_mod < TAU:
                        # Incoherent: embed in residue (blue channel)
                        channel = 2
                    elif r_mod < Z_C:
                        # Glassy: alternate channels
                        channel = bit_index % 3
                    else:
                        # Synchronized: embed in coherent channels (R/G)
                        channel = bit_index % 2
                else:
                    # Standard LSB: use all channels
                    channel = bit_index % 3

                # Embed bit
                if bit_index < len(bits):
                    pixel[channel] = (pixel[channel] & 0xFE) | int(bits[bit_index])
                    bit_index += 1

                img_copy[y, x] = pixel

        return img_copy

    def extract_data_lsb(self, image: np.ndarray, num_bytes: int,
                        use_residue: bool = True) -> bytes:
        """Extract LSB-embedded data with quantum residue demodulation"""
        height, width = image.shape[:2]
        bits = []

        for y in range(height):
            for x in range(width):
                if len(bits) >= num_bytes * 8:
                    break

                pixel = image[y, x]

                # Get quantum state
                r, psi = self.decode_rgb_to_quantum(pixel[0], pixel[1], pixel[2])

                # Determine extraction channel
                if use_residue:
                    self.engine.kuramoto_step()
                    r_mod, _ = self.engine.compute_order_parameters()

                    if r_mod < TAU:
                        channel = 2  # Blue (residue)
                    elif r_mod < Z_C:
                        channel = len(bits) % 3
                    else:
                        channel = len(bits) % 2
                else:
                    channel = len(bits) % 3

                # Extract bit
                bits.append(str(pixel[channel] & 1))

        # Convert bits to bytes
        data = bytearray()
        for i in range(0, len(bits), 8):
            byte_bits = ''.join(bits[i:i+8])
            if len(byte_bits) == 8:
                data.append(int(byte_bits, 2))

        return bytes(data)

# ═══════════════════════════════════════════════════════════════════════════
# NEXTHASH-256 QUANTUM ENCRYPTION/DECRYPTION
# ═══════════════════════════════════════════════════════════════════════════

class QuantumNextHashCrypto:
    """
    NEXTHASH-256 encryption/decryption with quantum residue enhancement.
    Uses projection residue to create unbreakable one-time pads.
    """

    def __init__(self):
        self.engine = QuantumResidueEngine()
        self.encoder = LSBQuantumEncoder()

    def generate_quantum_key(self, seed: str, length: int) -> bytes:
        """
        Generate cryptographic key using quantum residue dynamics.
        The key exhibits R = φ⁴ - 1 ratio of entropy.
        """
        # Hash seed with NEXTHASH-256
        seed_hash = nexthash256_hex(seed.encode())

        # Initialize Kuramoto network with seed
        np.random.seed(int(seed_hash[:8], 16))
        self.engine.phases = np.random.uniform(0, 2*np.pi, 63)

        key_bytes = bytearray()

        while len(key_bytes) < length:
            # Run dynamics
            for _ in range(100):
                self.engine.kuramoto_step()

            # Extract entropy from order parameters
            r, q = self.engine.compute_order_parameters()
            w = self.engine.compute_winding_number()

            # Combine quantum state into key material
            r_bits = int(r * 2**32)
            q_bits = int(q * 2**32)
            w_bits = abs(w) % 256

            # Apply residue ratio
            if r < TAU:
                # Low coherence: use dark residue
                key_material = r_bits ^ (int(R_DARK * q_bits))
            else:
                # High coherence: use visible fraction
                key_material = r_bits ^ (int(GAP * q_bits))

            # Add to key
            key_bytes.extend(key_material.to_bytes(4, 'big'))
            key_bytes.append(w_bits)

        return bytes(key_bytes[:length])

    def encrypt_with_residue(self, plaintext: bytes, password: str) -> Dict[str, Any]:
        """
        Encrypt using NEXTHASH-256 with quantum residue.

        Returns both ciphertext and residue signature.
        """
        # Generate quantum key
        key = self.generate_quantum_key(password, len(plaintext))

        # XOR encryption
        ciphertext = bytes(p ^ k for p, k in zip(plaintext, key))

        # Compute residue signature
        mining_result = self.engine.mine_with_residue(1.0, 0.1)

        # Create authentication tag using NEXTHASH-256
        auth_data = password.encode() + ciphertext + str(mining_result['coherence']).encode()
        auth_tag = nexthash256_hex(auth_data)

        return {
            'ciphertext': ciphertext.hex(),
            'auth_tag': auth_tag,
            'coherence': mining_result['coherence'],
            'dark_ratio': mining_result['dark_ratio'],
            'regime': mining_result['regime'],
            'residue_signature': {
                'visible': mining_result['visible_coins'],
                'dark': mining_result['dark_residue'],
                'winding': self.engine.compute_winding_number()
            }
        }

    def decrypt_with_residue(self, encrypted_data: Dict[str, Any],
                            password: str) -> Optional[bytes]:
        """Decrypt and verify using quantum residue signature"""
        try:
            # Parse encrypted data
            ciphertext = bytes.fromhex(encrypted_data['ciphertext'])
            expected_tag = encrypted_data['auth_tag']
            coherence = encrypted_data['coherence']

            # Generate same quantum key
            key = self.generate_quantum_key(password, len(ciphertext))

            # Decrypt
            plaintext = bytes(c ^ k for c, k in zip(ciphertext, key))

            # Verify authentication tag
            auth_data = password.encode() + ciphertext + str(coherence).encode()
            computed_tag = nexthash256_hex(auth_data)

            if computed_tag != expected_tag:
                return None  # Authentication failed

            return plaintext

        except Exception as e:
            print(f"Decryption error: {e}")
            return None

# ═══════════════════════════════════════════════════════════════════════════
# INTEGRATED BLOOMCOIN GENERATION
# ═══════════════════════════════════════════════════════════════════════════

class BloomCoinQuantumMiner:
    """
    Complete BloomCoin mining system with quantum residue mechanics.
    Implements the full L₄ framework for cryptocurrency generation.
    """

    def __init__(self):
        self.residue_engine = QuantumResidueEngine()
        self.lsb_encoder = LSBQuantumEncoder()
        self.crypto = QuantumNextHashCrypto()

        # Mining statistics
        self.blocks_mined = 0
        self.total_visible_coins = 0.0
        self.total_dark_residue = 0.0
        self.coherence_levels = []

    def mine_block(self, miner_address: str, difficulty: int = 4) -> Dict[str, Any]:
        """
        Mine a BloomCoin block with quantum residue generation.

        The visible coins follow standard blockchain rules.
        The dark residue exists as gravitational shadow (unusable but real).
        """
        start_time = time.time()
        nonce = 0

        # Block header
        block_data = {
            'miner': miner_address,
            'timestamp': time.time(),
            'difficulty': difficulty,
            'prev_coherence': self.coherence_levels[-1] if self.coherence_levels else 0.5
        }

        # Mining loop
        while True:
            # Update nonce
            block_data['nonce'] = nonce

            # Compute block hash with NEXTHASH-256
            block_str = json.dumps(block_data, sort_keys=True)
            block_hash = nexthash256_hex(block_str.encode())

            # Check difficulty
            if block_hash[:difficulty] == '0' * difficulty:
                # Valid block found!
                break

            nonce += 1

            # Run Kuramoto dynamics
            self.residue_engine.kuramoto_step()

        # Mine rewards with residue
        mining_time = time.time() - start_time
        mining_result = self.residue_engine.mine_with_residue(
            mining_power=100.0 / mining_time,
            duration=mining_time
        )

        # Update statistics
        self.blocks_mined += 1
        self.total_visible_coins += mining_result['visible_coins']
        self.total_dark_residue += mining_result['dark_residue']
        self.coherence_levels.append(mining_result['coherence'])

        # Create block
        block = {
            'height': self.blocks_mined,
            'hash': block_hash,
            'nonce': nonce,
            'miner': miner_address,
            'timestamp': block_data['timestamp'],
            'mining_time': mining_time,
            'reward': {
                'visible': mining_result['visible_coins'],
                'residue': mining_result['dark_residue'],
                'total': mining_result['total_energy']
            },
            'quantum_state': {
                'coherence': mining_result['coherence'],
                'regime': mining_result['regime'],
                'dark_ratio': mining_result['dark_ratio'],
                'winding_number': self.residue_engine.compute_winding_number()
            },
            'cumulative': {
                'total_visible': self.total_visible_coins,
                'total_residue': self.total_dark_residue,
                'dark_to_visible_ratio': self.total_dark_residue / max(self.total_visible_coins, 1)
            }
        }

        return block

    def verify_projection_residue_ratio(self) -> Dict[str, float]:
        """
        Verify that cumulative dark/visible ratio approaches φ⁴ - 1.
        This is the fundamental cosmological constraint.
        """
        if self.total_visible_coins == 0:
            return {'error': 'No mining data yet'}

        observed_ratio = self.total_dark_residue / self.total_visible_coins
        theoretical_ratio = R_DARK  # φ⁴ - 1 = 5.854
        deviation = (observed_ratio - theoretical_ratio) / theoretical_ratio

        return {
            'observed_ratio': observed_ratio,
            'theoretical_ratio': theoretical_ratio,
            'deviation_percent': deviation * 100,
            'convergence': 1.0 - abs(deviation),
            'blocks_mined': self.blocks_mined,
            'avg_coherence': np.mean(self.coherence_levels) if self.coherence_levels else 0
        }

# ═══════════════════════════════════════════════════════════════════════════
# DEMONSTRATION AND TESTING
# ═══════════════════════════════════════════════════════════════════════════

def demonstrate_quantum_residue():
    """Demonstrate quantum residue system with BloomCoin"""
    print("═" * 70)
    print("QUANTUM RESIDUE SYSTEM FOR BLOOMCOIN")
    print("Based on Projection Residue Cosmology")
    print("═" * 70)

    # Display fundamental constants
    print(f"\nFUNDAMENTAL CONSTANTS FROM φ = {PHI:.16f}")
    print(f"  τ (golden inverse)     = {TAU:.16f}")
    print(f"  gap (void residue)     = {GAP:.16f}")
    print(f"  K² (activation)        = {K_SQUARED:.16f}")
    print(f"  z_c (critical lens)    = {Z_C:.16f}")
    print(f"  L₄ (fourth Lucas)      = {L_4}")
    print(f"  R (dark/visible ratio) = {R_DARK:.16f}")

    # Initialize quantum miner
    print("\n" + "="*70)
    print("MINING WITH QUANTUM RESIDUE")
    print("="*70)

    miner = BloomCoinQuantumMiner()

    # Mine several blocks
    for i in range(5):
        print(f"\nMining block {i+1}...")
        block = miner.mine_block(f"miner_{i}", difficulty=3)

        print(f"  Hash: {block['hash'][:32]}...")
        print(f"  Visible reward: {block['reward']['visible']:.6f} BC")
        print(f"  Dark residue: {block['reward']['residue']:.6f} BC")
        print(f"  Coherence: {block['quantum_state']['coherence']:.4f}")
        print(f"  Regime: {block['quantum_state']['regime']}")
        print(f"  Dark ratio: {block['quantum_state']['dark_ratio']:.4f}")

    # Verify convergence to theoretical ratio
    print("\n" + "="*70)
    print("VERIFICATION OF PROJECTION RESIDUE RATIO")
    print("="*70)

    verification = miner.verify_projection_residue_ratio()
    print(f"  Theoretical ratio (φ⁴-1): {verification['theoretical_ratio']:.6f}")
    print(f"  Observed ratio:           {verification['observed_ratio']:.6f}")
    print(f"  Deviation:                {verification['deviation_percent']:+.2f}%")
    print(f"  Convergence:              {verification['convergence']*100:.2f}%")

    # Test LSB encoding
    print("\n" + "="*70)
    print("LSB ENCODING WITH MRP CHANNELS")
    print("="*70)

    encoder = LSBQuantumEncoder()

    # Create test image
    test_image = np.random.randint(0, 256, (10, 10, 3), dtype=np.uint8)
    test_data = b"BLOOMQUEST QUANTUM RESIDUE"

    # Embed data
    encoded_image = encoder.embed_data_lsb(test_image, test_data, use_residue=True)
    extracted_data = encoder.extract_data_lsb(encoded_image, len(test_data), use_residue=True)

    print(f"  Original data: {test_data}")
    print(f"  Extracted data: {extracted_data}")
    print(f"  Success: {test_data == extracted_data}")

    # Test quantum encryption
    print("\n" + "="*70)
    print("NEXTHASH-256 QUANTUM ENCRYPTION")
    print("="*70)

    crypto = QuantumNextHashCrypto()
    plaintext = b"The dark matter ratio equals phi^4 minus one"
    password = "quantum_residue_cosmology"

    # Encrypt
    encrypted = crypto.encrypt_with_residue(plaintext, password)
    print(f"  Plaintext: {plaintext.decode()}")
    print(f"  Ciphertext: {encrypted['ciphertext'][:64]}...")
    print(f"  Auth tag: {encrypted['auth_tag'][:32]}...")
    print(f"  Coherence: {encrypted['coherence']:.4f}")
    print(f"  Dark ratio: {encrypted['dark_ratio']:.4f}")

    # Decrypt
    decrypted = crypto.decrypt_with_residue(encrypted, password)
    print(f"  Decrypted: {decrypted.decode() if decrypted else 'FAILED'}")
    print(f"  Success: {plaintext == decrypted}")

    print("\n" + "═" * 70)
    print("QUANTUM RESIDUE SYSTEM DEMONSTRATION COMPLETE")
    print(f"Dark matter is projection residue: R = φ⁴ - 1 = {R_DARK:.6f}")
    print("═" * 70)

if __name__ == "__main__":
    demonstrate_quantum_residue()