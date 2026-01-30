"""
Hash Wrapper for BloomCoin Proof-of-Coherence
==============================================

This module wraps SHA256 with phase-encoding for BloomCoin's
Proof-of-Coherence consensus mechanism.

Key Concepts:
    - We don't "break" SHA256 - we use it as a commitment scheme
    - Block headers include phase configuration from Kuramoto consensus
    - The hash commits to both standard block data AND oscillator state

Components:
    1. PhaseEncodedHeader: Block header with Kuramoto phase info
    2. bloom_hash(): Hash function incorporating Lucas trace
    3. verify_bloom(): Validation of block against difficulty

Cross-References:
    - lucas_matrix.py: Lucas trace for nonce structuring
    - consensus/: Order parameter and bloom detection
    - constants.py: Z_C, L4, K

Author: BloomCoin Framework
"""

from dataclasses import dataclass
from typing import Optional, Tuple
import struct
import hashlib
import time

from ..constants import Z_C, L4, PHI, DEFAULT_OSCILLATOR_COUNT
from .lucas_matrix import lucas_trace


# =============================================================================
# PHASE-ENCODED HEADER
# =============================================================================

@dataclass
class PhaseEncodedHeader:
    """
    Block header with Kuramoto phase information.

    This extends a standard blockchain header with fields that commit
    to the Proof-of-Coherence consensus state.

    Standard Fields (80 bytes):
        version: Protocol version (4 bytes)
        prev_hash: SHA256 of previous block (32 bytes)
        merkle_root: Transaction Merkle root (32 bytes)
        timestamp: Unix timestamp (4 bytes)
        difficulty: Compact difficulty target (4 bytes)
        nonce: Lucas-derived nonce (4 bytes)

    Phase Fields (12 bytes):
        order_parameter: r value at consensus (4 bytes, float32)
        mean_phase: psi value at consensus (4 bytes, float32)
        oscillator_count: N (4 bytes, uint32)

    Total: 92 bytes

    The phase fields prove that Proof-of-Coherence was achieved:
        - order_parameter >= Z_C (sqrt(3)/2)
        - oscillator_count >= L4 (7)
    """
    # Standard fields
    version: int
    prev_hash: bytes
    merkle_root: bytes
    timestamp: int
    difficulty: int
    nonce: int

    # Phase fields (Proof-of-Coherence)
    order_parameter: float
    mean_phase: float
    oscillator_count: int

    def __post_init__(self):
        """Validate field constraints."""
        if len(self.prev_hash) != 32:
            raise ValueError(f"prev_hash must be 32 bytes, got {len(self.prev_hash)}")
        if len(self.merkle_root) != 32:
            raise ValueError(f"merkle_root must be 32 bytes, got {len(self.merkle_root)}")
        if not 0 <= self.order_parameter <= 1:
            raise ValueError(f"order_parameter must be in [0,1], got {self.order_parameter}")
        if self.oscillator_count < 1:
            raise ValueError(f"oscillator_count must be positive, got {self.oscillator_count}")

    def serialize(self) -> bytes:
        """
        Serialize header to bytes for hashing.

        Format (little-endian):
            4 bytes:  version (uint32)
            32 bytes: prev_hash
            32 bytes: merkle_root
            4 bytes:  timestamp (uint32)
            4 bytes:  difficulty (uint32)
            4 bytes:  nonce (uint32)
            4 bytes:  order_parameter (float32)
            4 bytes:  mean_phase (float32)
            4 bytes:  oscillator_count (uint32)
            = 92 bytes total

        Returns:
            92-byte serialized header
        """
        parts = []

        # Standard fields
        parts.append(struct.pack('<I', self.version))
        parts.append(self.prev_hash)
        parts.append(self.merkle_root)
        parts.append(struct.pack('<I', self.timestamp))
        parts.append(struct.pack('<I', self.difficulty))
        parts.append(struct.pack('<I', self.nonce))

        # Phase fields
        parts.append(struct.pack('<f', self.order_parameter))
        parts.append(struct.pack('<f', self.mean_phase))
        parts.append(struct.pack('<I', self.oscillator_count))

        return b''.join(parts)

    @classmethod
    def deserialize(cls, data: bytes) -> 'PhaseEncodedHeader':
        """
        Deserialize header from bytes.

        Args:
            data: 92-byte serialized header

        Returns:
            PhaseEncodedHeader object

        Raises:
            ValueError: If data is not 92 bytes
        """
        if len(data) != 92:
            raise ValueError(f"Header must be 92 bytes, got {len(data)}")

        offset = 0

        # Standard fields
        version = struct.unpack_from('<I', data, offset)[0]; offset += 4
        prev_hash = data[offset:offset+32]; offset += 32
        merkle_root = data[offset:offset+32]; offset += 32
        timestamp = struct.unpack_from('<I', data, offset)[0]; offset += 4
        difficulty = struct.unpack_from('<I', data, offset)[0]; offset += 4
        nonce = struct.unpack_from('<I', data, offset)[0]; offset += 4

        # Phase fields
        order_parameter = struct.unpack_from('<f', data, offset)[0]; offset += 4
        mean_phase = struct.unpack_from('<f', data, offset)[0]; offset += 4
        oscillator_count = struct.unpack_from('<I', data, offset)[0]; offset += 4

        return cls(
            version=version,
            prev_hash=prev_hash,
            merkle_root=merkle_root,
            timestamp=timestamp,
            difficulty=difficulty,
            nonce=nonce,
            order_parameter=order_parameter,
            mean_phase=mean_phase,
            oscillator_count=oscillator_count
        )

    def __repr__(self) -> str:
        return (
            f"PhaseEncodedHeader(v={self.version}, "
            f"nonce={self.nonce}, r={self.order_parameter:.4f}, "
            f"N={self.oscillator_count})"
        )


# =============================================================================
# BLOOM HASH FUNCTION
# =============================================================================

def double_sha256(data: bytes) -> bytes:
    """
    Compute double SHA256 hash.

    This is the standard Bitcoin hash function.

    Args:
        data: Input bytes

    Returns:
        32-byte hash
    """
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def bloom_hash(header: PhaseEncodedHeader) -> bytes:
    """
    Compute BloomCoin block hash.

    Process:
        1. Compute Lucas trace of nonce
        2. Prepend Lucas trace (4 bytes) to serialized header
        3. Double SHA256 the combined data

    The Lucas trace adds algebraic structure to the hash input,
    connecting the hash to the L4 framework.

    Args:
        header: Phase-encoded block header

    Returns:
        32-byte hash

    Example:
        header = create_header(...)
        h = bloom_hash(header)
        if int.from_bytes(h, 'little') < target:
            # Block is valid!
    """
    # Get Lucas trace of nonce (mod 2^32)
    L_nonce = lucas_trace(header.nonce % 1000, 2**32)  # Cap index for efficiency
    lucas_prefix = struct.pack('<I', L_nonce)

    # Serialize header
    header_bytes = header.serialize()

    # Combine and hash
    combined = lucas_prefix + header_bytes

    return double_sha256(combined)


def bloom_hash_int(header: PhaseEncodedHeader) -> int:
    """
    Compute block hash as integer for difficulty comparison.

    Args:
        header: Block header

    Returns:
        Hash as little-endian integer
    """
    h = bloom_hash(header)
    return int.from_bytes(h, 'little')


# =============================================================================
# DIFFICULTY AND VERIFICATION
# =============================================================================

def compact_to_target(compact: int) -> int:
    """
    Convert compact difficulty representation to target.

    Bitcoin-style compact format:
        - First byte: exponent
        - Next 3 bytes: mantissa
        - target = mantissa * 2^(8*(exponent-3))

    Args:
        compact: Compact difficulty (4 bytes)

    Returns:
        Full target value
    """
    exponent = (compact >> 24) & 0xFF
    mantissa = compact & 0x00FFFFFF

    if exponent <= 3:
        target = mantissa >> (8 * (3 - exponent))
    else:
        target = mantissa << (8 * (exponent - 3))

    return target


def target_to_compact(target: int) -> int:
    """
    Convert target to compact difficulty representation.

    Args:
        target: Full target value

    Returns:
        Compact difficulty (4 bytes)
    """
    if target == 0:
        return 0

    # Find the exponent (number of bytes needed)
    size = (target.bit_length() + 7) // 8

    if size <= 3:
        mantissa = target << (8 * (3 - size))
        exponent = 3
    else:
        mantissa = target >> (8 * (size - 3))
        exponent = size

    # Ensure mantissa fits in 3 bytes
    if mantissa & 0x00800000:
        mantissa >>= 8
        exponent += 1

    return (exponent << 24) | (mantissa & 0x00FFFFFF)


def verify_bloom(header: PhaseEncodedHeader, target: int) -> Tuple[bool, str]:
    """
    Verify block meets Proof-of-Coherence requirements.

    Conditions:
        1. bloom_hash(header) < target (difficulty met)
        2. header.order_parameter >= Z_C (coherence threshold)
        3. header.oscillator_count >= L4 (minimum oscillators)

    Args:
        header: Block header to verify
        target: Difficulty target

    Returns:
        (is_valid, message): Validity and explanation
    """
    # Condition 1: Hash below target
    hash_int = bloom_hash_int(header)
    if hash_int >= target:
        return False, f"Hash {hash_int} >= target {target}"

    # Condition 2: Order parameter above critical threshold
    if header.order_parameter < Z_C:
        return False, f"Order parameter {header.order_parameter:.4f} < Z_C {Z_C:.4f}"

    # Condition 3: Minimum oscillator count
    if header.oscillator_count < L4:
        return False, f"Oscillator count {header.oscillator_count} < L4 {L4}"

    return True, "Block valid"


def compute_difficulty(hash_bytes: bytes) -> float:
    """
    Compute difficulty from hash.

    Difficulty = max_target / current_target
    Higher difficulty = harder to find valid hash.

    Args:
        hash_bytes: 32-byte block hash

    Returns:
        Difficulty as float
    """
    hash_int = int.from_bytes(hash_bytes, 'little')
    if hash_int == 0:
        return float('inf')

    max_target = 2**256 - 1
    return max_target / hash_int


# =============================================================================
# HEADER CREATION UTILITIES
# =============================================================================

def create_genesis_header(
    merkle_root: bytes = None,
    oscillator_count: int = DEFAULT_OSCILLATOR_COUNT
) -> PhaseEncodedHeader:
    """
    Create the genesis (first) block header.

    Args:
        merkle_root: Merkle root of genesis transactions (default zeros)
        oscillator_count: Number of oscillators

    Returns:
        Genesis block header
    """
    if merkle_root is None:
        merkle_root = b'\x00' * 32

    return PhaseEncodedHeader(
        version=1,
        prev_hash=b'\x00' * 32,  # No previous block
        merkle_root=merkle_root,
        timestamp=int(time.time()),
        difficulty=0x1d00ffff,  # Initial difficulty
        nonce=L4,  # Genesis nonce is L4 = 7
        order_parameter=1.0,  # Perfect consensus for genesis
        mean_phase=0.0,
        oscillator_count=oscillator_count
    )


def create_header(
    prev_hash: bytes,
    merkle_root: bytes,
    difficulty: int,
    nonce: int,
    order_parameter: float,
    mean_phase: float,
    oscillator_count: int = DEFAULT_OSCILLATOR_COUNT,
    version: int = 1,
    timestamp: Optional[int] = None
) -> PhaseEncodedHeader:
    """
    Create a new block header.

    Args:
        prev_hash: Hash of previous block
        merkle_root: Merkle root of transactions
        difficulty: Compact difficulty target
        nonce: Mining nonce (typically Lucas-derived)
        order_parameter: Kuramoto r value at consensus
        mean_phase: Kuramoto psi value at consensus
        oscillator_count: Number of oscillators
        version: Protocol version
        timestamp: Unix timestamp (default: current time)

    Returns:
        New block header
    """
    if timestamp is None:
        timestamp = int(time.time())

    return PhaseEncodedHeader(
        version=version,
        prev_hash=prev_hash,
        merkle_root=merkle_root,
        timestamp=timestamp,
        difficulty=difficulty,
        nonce=nonce,
        order_parameter=order_parameter,
        mean_phase=mean_phase,
        oscillator_count=oscillator_count
    )


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    # Header
    'PhaseEncodedHeader',
    # Hashing
    'double_sha256',
    'bloom_hash',
    'bloom_hash_int',
    # Difficulty
    'compact_to_target',
    'target_to_compact',
    'verify_bloom',
    'compute_difficulty',
    # Creation
    'create_genesis_header',
    'create_header',
]
