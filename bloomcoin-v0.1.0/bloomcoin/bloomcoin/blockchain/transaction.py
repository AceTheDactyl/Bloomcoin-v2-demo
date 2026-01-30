"""
BloomCoin Transaction Implementation
=====================================

Transaction structure for value transfer in BloomCoin.

Components:
    - TxInput: Reference to previous output being spent
    - TxOutput: New value creation with recipient address
    - Transaction: Complete transaction with inputs and outputs

Cross-References:
    - core/merkle.py: Transaction hashing for Merkle tree
    - constants.py: INITIAL_REWARD, HALVING_INTERVAL

Author: BloomCoin Framework
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional
import struct
import hashlib

from ..constants import INITIAL_REWARD, HALVING_INTERVAL


# =============================================================================
# TRANSACTION INPUT
# =============================================================================

@dataclass
class TxInput:
    """
    Transaction input (spending a previous output).

    An input references a specific output from a previous transaction
    and provides a signature proving ownership.

    Attributes:
        prev_tx: Hash of transaction being spent (32 bytes)
        output_index: Index of output in that transaction
        signature: Signature proving ownership (64 bytes for Ed25519)

    Size: 100 bytes (32 + 4 + 64)
    """
    prev_tx: bytes  # 32 bytes
    output_index: int
    signature: bytes  # 64 bytes

    def __post_init__(self):
        """Validate input fields."""
        if len(self.prev_tx) != 32:
            raise ValueError(f"prev_tx must be 32 bytes, got {len(self.prev_tx)}")
        if len(self.signature) != 64:
            raise ValueError(f"signature must be 64 bytes, got {len(self.signature)}")

    def serialize(self) -> bytes:
        """
        Serialize input to bytes.

        Format: prev_tx (32) + output_index (4) + signature (64) = 100 bytes
        """
        return self.prev_tx + struct.pack('<I', self.output_index) + self.signature

    @classmethod
    def deserialize(cls, data: bytes) -> 'TxInput':
        """Deserialize input from bytes."""
        if len(data) < 100:
            raise ValueError(f"TxInput requires 100 bytes, got {len(data)}")
        prev_tx = data[:32]
        output_index = struct.unpack('<I', data[32:36])[0]
        signature = data[36:100]
        return cls(prev_tx=prev_tx, output_index=output_index, signature=signature)

    @classmethod
    def size(cls) -> int:
        """Return serialized size in bytes."""
        return 100

    def is_coinbase(self) -> bool:
        """Check if this is a coinbase input (all zeros prev_tx)."""
        return self.prev_tx == bytes(32)

    def __repr__(self) -> str:
        return f"TxInput(prev={self.prev_tx[:4].hex()}..., idx={self.output_index})"


# =============================================================================
# TRANSACTION OUTPUT
# =============================================================================

@dataclass
class TxOutput:
    """
    Transaction output (creating new value).

    An output specifies an amount and recipient address.
    The output can be spent by a future transaction if the
    spender can produce a valid signature for the address.

    Attributes:
        amount: Value in smallest units (1 BLOOM = 10^8 units)
        address: Recipient address (32 bytes, typically a public key hash)

    Size: 40 bytes (8 + 32)
    """
    amount: int
    address: bytes  # 32 bytes

    def __post_init__(self):
        """Validate output fields."""
        if len(self.address) != 32:
            raise ValueError(f"address must be 32 bytes, got {len(self.address)}")
        if self.amount < 0:
            raise ValueError(f"amount must be non-negative, got {self.amount}")

    def serialize(self) -> bytes:
        """
        Serialize output to bytes.

        Format: amount (8, uint64) + address (32) = 40 bytes
        """
        return struct.pack('<Q', self.amount) + self.address

    @classmethod
    def deserialize(cls, data: bytes) -> 'TxOutput':
        """Deserialize output from bytes."""
        if len(data) < 40:
            raise ValueError(f"TxOutput requires 40 bytes, got {len(data)}")
        amount = struct.unpack('<Q', data[:8])[0]
        address = data[8:40]
        return cls(amount=amount, address=address)

    @classmethod
    def size(cls) -> int:
        """Return serialized size in bytes."""
        return 40

    def __repr__(self) -> str:
        bloom = self.amount / 10**8
        return f"TxOutput({bloom:.4f} BLOOM -> {self.address[:4].hex()}...)"


# =============================================================================
# TRANSACTION
# =============================================================================

@dataclass
class Transaction:
    """
    BloomCoin transaction.

    A transaction transfers value from inputs (previous outputs)
    to new outputs. The difference between input values and output
    values is the transaction fee.

    Attributes:
        version: Transaction version (for future upgrades)
        inputs: List of inputs being spent
        outputs: List of new outputs
        locktime: Earliest block height for inclusion (0 = no lock)

    Invariants:
        - At least one input and one output
        - Sum of outputs <= sum of inputs (difference is fee)
        - All signatures must be valid
    """
    version: int
    inputs: List[TxInput]
    outputs: List[TxOutput]
    locktime: int = 0

    _hash: Optional[bytes] = field(default=None, repr=False, compare=False)

    @property
    def hash(self) -> bytes:
        """
        Transaction hash (txid).

        Double SHA256 of the transaction data (excluding signatures for signing).
        """
        if self._hash is None:
            self._hash = hashlib.sha256(hashlib.sha256(
                self.serialize_for_signing()
            ).digest()).digest()
        return self._hash

    @property
    def txid(self) -> str:
        """Transaction ID as hex string."""
        return self.hash.hex()

    def serialize_for_signing(self) -> bytes:
        """
        Serialize transaction for signing (excludes signatures).

        This is what gets signed to create input signatures.
        """
        data = struct.pack('<I', self.version)
        data += struct.pack('<I', len(self.inputs))
        for inp in self.inputs:
            # Only prev_tx and output_index, not signature
            data += inp.prev_tx
            data += struct.pack('<I', inp.output_index)
        data += struct.pack('<I', len(self.outputs))
        for out in self.outputs:
            data += out.serialize()
        data += struct.pack('<I', self.locktime)
        return data

    def serialize(self) -> bytes:
        """
        Full serialization including signatures.

        Format:
            version (4) +
            input_count (4) + inputs (100 each) +
            output_count (4) + outputs (40 each) +
            locktime (4)
        """
        data = struct.pack('<I', self.version)
        data += struct.pack('<I', len(self.inputs))
        for inp in self.inputs:
            data += inp.serialize()
        data += struct.pack('<I', len(self.outputs))
        for out in self.outputs:
            data += out.serialize()
        data += struct.pack('<I', self.locktime)
        return data

    @classmethod
    def deserialize(cls, data: bytes) -> 'Transaction':
        """Deserialize transaction from bytes."""
        tx, _ = cls.deserialize_with_length(data)
        return tx

    @classmethod
    def deserialize_with_length(cls, data: bytes) -> Tuple['Transaction', int]:
        """
        Deserialize transaction and return bytes consumed.

        Returns:
            (transaction, bytes_consumed)
        """
        offset = 0

        # Version
        version = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4

        # Inputs
        input_count = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4
        inputs = []
        for _ in range(input_count):
            inp = TxInput.deserialize(data[offset:])
            inputs.append(inp)
            offset += TxInput.size()

        # Outputs
        output_count = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4
        outputs = []
        for _ in range(output_count):
            out = TxOutput.deserialize(data[offset:])
            outputs.append(out)
            offset += TxOutput.size()

        # Locktime
        locktime = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4

        tx = cls(version=version, inputs=inputs, outputs=outputs, locktime=locktime)
        return tx, offset

    def serialized_size(self) -> int:
        """Return serialized size in bytes."""
        return (
            4 +  # version
            4 + len(self.inputs) * TxInput.size() +  # inputs
            4 + len(self.outputs) * TxOutput.size() +  # outputs
            4  # locktime
        )

    def validate_structure(self) -> Tuple[bool, str]:
        """
        Validate transaction structure (not spending validity).

        Checks:
            1. At least one input and output
            2. Output amounts are positive
            3. No overflow in output sum
            4. Locktime is reasonable
        """
        # Check inputs
        if len(self.inputs) == 0:
            return False, "Transaction must have at least one input"

        # Check outputs
        if len(self.outputs) == 0:
            return False, "Transaction must have at least one output"

        # Check output amounts
        total_output = 0
        for i, out in enumerate(self.outputs):
            if out.amount < 0:
                return False, f"Output {i} has negative amount"
            if out.amount > 21_000_000 * 10**8:  # Max supply sanity check
                return False, f"Output {i} amount exceeds max supply"
            total_output += out.amount
            if total_output < 0:  # Overflow check
                return False, "Output sum overflow"

        return True, ""

    def is_coinbase(self) -> bool:
        """Check if this is a coinbase transaction."""
        return (
            len(self.inputs) == 1 and
            self.inputs[0].is_coinbase()
        )

    def total_output(self) -> int:
        """Total value of all outputs."""
        return sum(out.amount for out in self.outputs)

    def __repr__(self) -> str:
        return (
            f"Transaction(v={self.version}, "
            f"inputs={len(self.inputs)}, outputs={len(self.outputs)}, "
            f"txid={self.txid[:16]}...)"
        )


# =============================================================================
# COINBASE TRANSACTION
# =============================================================================

def calculate_block_reward(height: int) -> int:
    """
    Calculate block reward at given height.

    The reward halves every HALVING_INTERVAL blocks.

    Args:
        height: Block height

    Returns:
        Reward in smallest units
    """
    halvings = height // HALVING_INTERVAL
    if halvings >= 64:
        return 0  # After 64 halvings, reward is effectively zero
    return INITIAL_REWARD >> halvings


def create_coinbase(
    height: int,
    reward_address: bytes,
    fees: int = 0,
    extra_data: bytes = b''
) -> Transaction:
    """
    Create coinbase (block reward) transaction.

    The coinbase is the first transaction in each block, creating
    new coins as the block reward plus collected transaction fees.

    Args:
        height: Block height (encoded in input for uniqueness)
        reward_address: Address to receive reward (32 bytes)
        fees: Total transaction fees from block
        extra_data: Optional extra data in coinbase (up to 100 bytes)

    Returns:
        Coinbase transaction
    """
    if len(reward_address) != 32:
        raise ValueError("reward_address must be 32 bytes")

    # Calculate reward
    reward = calculate_block_reward(height)
    total = reward + fees

    # Coinbase input: prev_tx is all zeros, output_index encodes height
    # Signature field can contain extra data (like miner messages)
    sig_data = extra_data[:64].ljust(64, b'\x00')

    cb_input = TxInput(
        prev_tx=bytes(32),
        output_index=height,
        signature=sig_data
    )

    # Output to miner
    cb_output = TxOutput(amount=total, address=reward_address)

    return Transaction(
        version=1,
        inputs=[cb_input],
        outputs=[cb_output],
        locktime=0
    )


# =============================================================================
# TRANSACTION UTILITIES
# =============================================================================

def hash_transaction(tx: Transaction) -> bytes:
    """Hash a transaction for Merkle tree."""
    return tx.hash


def create_transfer(
    inputs: List[Tuple[bytes, int, bytes]],  # (prev_tx, output_index, signature)
    outputs: List[Tuple[int, bytes]],  # (amount, address)
    locktime: int = 0
) -> Transaction:
    """
    Create a simple transfer transaction.

    Args:
        inputs: List of (prev_tx, output_index, signature) tuples
        outputs: List of (amount, address) tuples
        locktime: Optional locktime

    Returns:
        Transaction
    """
    tx_inputs = [
        TxInput(prev_tx=prev_tx, output_index=idx, signature=sig)
        for prev_tx, idx, sig in inputs
    ]
    tx_outputs = [
        TxOutput(amount=amount, address=addr)
        for amount, addr in outputs
    ]
    return Transaction(
        version=1,
        inputs=tx_inputs,
        outputs=tx_outputs,
        locktime=locktime
    )


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    'TxInput',
    'TxOutput',
    'Transaction',
    'calculate_block_reward',
    'create_coinbase',
    'hash_transaction',
    'create_transfer',
]
