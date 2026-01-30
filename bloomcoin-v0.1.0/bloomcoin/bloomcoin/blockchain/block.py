"""
BloomCoin Block Implementation
===============================

Block data structure for the BloomCoin blockchain.

Key Difference from Bitcoin:
    Blocks contain a ConsensusCertificate proving Proof-of-Coherence
    was achieved, not just a nonce that produces a low hash.

Block Structure:
    - Header (92 bytes): Standard fields + phase extension
    - Certificate (variable): Proof of oscillator synchronization
    - Transactions (variable): Value transfers

Cross-References:
    - core/hash_wrapper.py: PhaseEncodedHeader, bloom_hash
    - consensus/threshold_gate.py: ConsensusCertificate
    - transaction.py: Transaction, create_coinbase

Author: BloomCoin Framework
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import struct
import time
import numpy as np

from ..core.hash_wrapper import (
    PhaseEncodedHeader, bloom_hash, create_genesis_header
)
from ..core.merkle import compute_merkle_root
from ..consensus.threshold_gate import ConsensusCertificate
from ..constants import Z_C, L4, DEFAULT_OSCILLATOR_COUNT
from .transaction import Transaction, create_coinbase


# =============================================================================
# BLOCK HEADER ALIAS
# =============================================================================

# Use PhaseEncodedHeader as BlockHeader
# This maintains consistency with the core module
BlockHeader = PhaseEncodedHeader


# =============================================================================
# BLOCK
# =============================================================================

@dataclass
class Block:
    """
    Complete BloomCoin block.

    A block contains:
        - Header (92 bytes): Metadata and phase information
        - Certificate (variable): Proof of Kuramoto synchronization
        - Transactions (variable): List of value transfers

    The header commits to both standard block data (prev_hash, merkle_root)
    AND the oscillator state at consensus (order_parameter, mean_phase).

    Attributes:
        header: Block header with phase extension
        certificate: Consensus certificate proving bloom
        transactions: List of transactions (first is coinbase)
    """
    header: BlockHeader
    certificate: ConsensusCertificate
    transactions: List[Transaction]

    _hash: Optional[bytes] = field(default=None, repr=False, compare=False)
    _height: int = field(default=-1, repr=False, compare=False)

    @property
    def hash(self) -> bytes:
        """Block hash (cached)."""
        if self._hash is None:
            self._hash = bloom_hash(self.header)
        return self._hash

    @property
    def hash_hex(self) -> str:
        """Block hash as hex string."""
        return self.hash.hex()

    @property
    def height(self) -> int:
        """Block height (must be set externally)."""
        return self._height

    @height.setter
    def height(self, value: int):
        self._height = value

    @property
    def prev_hash(self) -> bytes:
        """Previous block hash."""
        return self.header.prev_hash

    @property
    def merkle_root(self) -> bytes:
        """Transaction Merkle root."""
        return self.header.merkle_root

    @property
    def timestamp(self) -> int:
        """Block timestamp."""
        return self.header.timestamp

    @property
    def difficulty(self) -> int:
        """Block difficulty (compact representation)."""
        return self.header.difficulty

    @property
    def nonce(self) -> int:
        """Block nonce (Lucas-derived)."""
        return self.header.nonce

    @property
    def order_parameter(self) -> float:
        """Final order parameter r at consensus."""
        return self.header.order_parameter

    @property
    def oscillator_count(self) -> int:
        """Number of oscillators used in consensus."""
        return self.header.oscillator_count

    def serialize(self) -> bytes:
        """
        Serialize complete block to bytes.

        Format:
            header (92) +
            cert_len (4) + certificate (variable) +
            tx_count (4) + transactions (variable)
        """
        parts = []

        # Header
        parts.append(self.header.serialize())

        # Certificate
        cert_bytes = self.certificate.serialize()
        parts.append(struct.pack('<I', len(cert_bytes)))
        parts.append(cert_bytes)

        # Transactions
        parts.append(struct.pack('<I', len(self.transactions)))
        for tx in self.transactions:
            tx_bytes = tx.serialize()
            parts.append(struct.pack('<I', len(tx_bytes)))
            parts.append(tx_bytes)

        return b''.join(parts)

    @classmethod
    def deserialize(cls, data: bytes) -> 'Block':
        """Deserialize block from bytes."""
        offset = 0

        # Header (92 bytes)
        header = BlockHeader.deserialize(data[offset:offset+92])
        offset += 92

        # Certificate
        cert_len = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4
        certificate = ConsensusCertificate.deserialize(data[offset:offset+cert_len])
        offset += cert_len

        # Transactions
        tx_count = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4
        transactions = []
        for _ in range(tx_count):
            tx_len = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4
            tx = Transaction.deserialize(data[offset:offset+tx_len])
            transactions.append(tx)
            offset += tx_len

        return cls(header=header, certificate=certificate, transactions=transactions)

    def serialized_size(self) -> int:
        """Return serialized size in bytes."""
        size = 92  # Header
        size += 4 + len(self.certificate.serialize())  # Certificate
        size += 4  # tx_count
        for tx in self.transactions:
            size += 4 + tx.serialized_size()
        return size

    def validate_structure(self) -> Tuple[bool, str]:
        """
        Validate block structure (not chain context).

        Checks:
            1. Certificate proves r >= z_c for L4 rounds
            2. Order parameter in header matches certificate
            3. Merkle root matches transactions
            4. All transactions have valid structure
        """
        # Check certificate validity
        cert_valid, cert_msg = self.certificate.verify()
        if not cert_valid:
            return False, f"Invalid certificate: {cert_msg}"

        # Check r threshold
        if self.header.order_parameter < Z_C:
            return False, f"Order parameter {self.header.order_parameter:.4f} < z_c ({Z_C:.4f})"

        # Check bloom duration
        bloom_duration = self.certificate.bloom_end - self.certificate.bloom_start + 1
        if bloom_duration < L4:
            return False, f"Bloom duration {bloom_duration} < L4 ({L4})"

        # Check oscillator count
        if self.header.oscillator_count < L4:
            return False, f"Oscillator count {self.header.oscillator_count} < L4"

        # Check Merkle root
        if self.transactions:
            tx_hashes = [tx.hash for tx in self.transactions]
            computed_root = compute_merkle_root(tx_hashes)
            if computed_root != self.header.merkle_root:
                return False, "Merkle root mismatch"

        # Validate each transaction structure
        for i, tx in enumerate(self.transactions):
            valid, msg = tx.validate_structure()
            if not valid:
                return False, f"Transaction {i} invalid: {msg}"

        # First transaction should be coinbase (if any transactions)
        if self.transactions and not self.transactions[0].is_coinbase():
            return False, "First transaction must be coinbase"

        return True, "Block structure valid"

    def get_coinbase(self) -> Optional[Transaction]:
        """Get the coinbase transaction if present."""
        if self.transactions and self.transactions[0].is_coinbase():
            return self.transactions[0]
        return None

    def total_fees(self, input_values: Optional[dict] = None) -> int:
        """
        Calculate total fees (requires input values lookup).

        Args:
            input_values: Dict mapping (prev_tx, output_index) -> amount

        Returns:
            Total fees if input_values provided, else 0
        """
        if input_values is None:
            return 0

        total_fees = 0
        for tx in self.transactions[1:]:  # Skip coinbase
            input_sum = 0
            for inp in tx.inputs:
                key = (inp.prev_tx, inp.output_index)
                if key in input_values:
                    input_sum += input_values[key]
            output_sum = tx.total_output()
            if input_sum >= output_sum:
                total_fees += input_sum - output_sum

        return total_fees

    def __repr__(self) -> str:
        return (
            f"Block(height={self._height}, "
            f"hash={self.hash[:4].hex()}..., "
            f"txs={len(self.transactions)}, "
            f"r={self.order_parameter:.4f})"
        )


# =============================================================================
# GENESIS BLOCK
# =============================================================================

def create_genesis_block(
    reward_address: Optional[bytes] = None,
    timestamp: Optional[int] = None,
    oscillator_count: int = DEFAULT_OSCILLATOR_COUNT
) -> Block:
    """
    Create the genesis (first) block.

    The genesis block is special:
        - prev_hash is all zeros (no previous block)
        - Contains only a coinbase transaction (or none)
        - Has a predefined consensus certificate
        - Uses a fixed timestamp for reproducibility

    Args:
        reward_address: Address for genesis reward (None = no coinbase)
        timestamp: Block timestamp (default: fixed value for reproducibility)
        oscillator_count: Number of oscillators

    Returns:
        Genesis block
    """
    # Fixed genesis timestamp for reproducibility
    if timestamp is None:
        timestamp = 1700000000  # November 14, 2023

    # Import compute_order_parameter to ensure r matches phases
    from ..consensus.kuramoto import compute_order_parameter

    # Simulated final phases (nearly synchronized, tight cluster)
    genesis_phases = np.linspace(0, 0.1, oscillator_count).tolist()

    # Compute actual r and psi from these phases
    # This ensures the certificate will verify correctly
    phases_arr = np.array(genesis_phases)
    genesis_r, genesis_psi = compute_order_parameter(phases_arr)

    # Create certificate
    certificate = ConsensusCertificate(
        bloom_start=0,
        bloom_end=L4 - 1,
        r_values=[genesis_r] * L4,
        psi_values=[genesis_psi] * L4,
        final_phases=genesis_phases,
        oscillator_count=oscillator_count,
        threshold=Z_C,
        required_rounds=L4
    )

    # Create transactions (optional coinbase)
    transactions = []
    merkle_root = bytes(32)  # All zeros if no transactions

    if reward_address is not None:
        if len(reward_address) != 32:
            raise ValueError("reward_address must be 32 bytes")
        coinbase = create_coinbase(height=0, reward_address=reward_address)
        transactions.append(coinbase)
        merkle_root = coinbase.hash

    # Create header
    header = BlockHeader(
        version=1,
        prev_hash=bytes(32),  # No previous block
        merkle_root=merkle_root,
        timestamp=timestamp,
        difficulty=0x1d00ffff,  # Initial difficulty
        nonce=L4,  # Genesis nonce is L4 = 7
        order_parameter=genesis_r,
        mean_phase=genesis_psi,
        oscillator_count=oscillator_count
    )

    block = Block(
        header=header,
        certificate=certificate,
        transactions=transactions
    )
    block.height = 0

    return block


# =============================================================================
# BLOCK CREATION UTILITIES
# =============================================================================

def create_block(
    prev_block: Block,
    transactions: List[Transaction],
    certificate: ConsensusCertificate,
    nonce: int,
    difficulty: int,
    miner_address: bytes,
    timestamp: Optional[int] = None
) -> Block:
    """
    Create a new block extending the chain.

    Args:
        prev_block: Previous block in chain
        transactions: Transactions to include (without coinbase)
        certificate: Proof of consensus
        nonce: Mining nonce
        difficulty: Difficulty target (compact)
        miner_address: Address for block reward
        timestamp: Block timestamp (default: current time)

    Returns:
        New block
    """
    if timestamp is None:
        timestamp = int(time.time())

    new_height = prev_block.height + 1

    # Create coinbase as first transaction
    fees = 0  # Would need UTXO lookup to calculate actual fees
    coinbase = create_coinbase(new_height, miner_address, fees)
    all_transactions = [coinbase] + transactions

    # Compute Merkle root
    tx_hashes = [tx.hash for tx in all_transactions]
    merkle_root = compute_merkle_root(tx_hashes)

    # Get final r and psi from certificate
    final_r = certificate.r_values[-1] if certificate.r_values else 0.0
    final_psi = certificate.psi_values[-1] if certificate.psi_values else 0.0

    # Create header
    header = BlockHeader(
        version=1,
        prev_hash=prev_block.hash,
        merkle_root=merkle_root,
        timestamp=timestamp,
        difficulty=difficulty,
        nonce=nonce,
        order_parameter=final_r,
        mean_phase=final_psi,
        oscillator_count=certificate.oscillator_count
    )

    block = Block(
        header=header,
        certificate=certificate,
        transactions=all_transactions
    )
    block.height = new_height

    return block


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    'BlockHeader',
    'Block',
    'create_genesis_block',
    'create_block',
]
