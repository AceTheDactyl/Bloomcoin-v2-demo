"""
Merkle Tree Implementation for BloomCoin
=========================================

This module implements a standard Merkle tree for transaction commitment
in BloomCoin blocks.

Merkle trees provide:
    1. Efficient transaction inclusion proofs (O(log n))
    2. Tamper-evident data structure
    3. Compact commitment to arbitrary transaction sets

Cross-References:
    - hash_wrapper.py: double_sha256 for node hashing
    - blockchain/block.py: Uses merkle_root in block header
    - Bitcoin: Compatible Merkle tree structure

Author: BloomCoin Framework
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
import hashlib


# =============================================================================
# MERKLE HASHING
# =============================================================================

def double_sha256(data: bytes) -> bytes:
    """
    Compute double SHA256 hash.

    Args:
        data: Input bytes

    Returns:
        32-byte hash
    """
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def merkle_hash(left: bytes, right: bytes) -> bytes:
    """
    Compute Merkle parent hash from two children.

    Uses double SHA256 for security (same as Bitcoin).

    Args:
        left: Left child hash (32 bytes)
        right: Right child hash (32 bytes)

    Returns:
        Parent hash (32 bytes)
    """
    return double_sha256(left + right)


# =============================================================================
# MERKLE ROOT COMPUTATION
# =============================================================================

def compute_merkle_root(tx_hashes: List[bytes]) -> bytes:
    """
    Compute Merkle root from a list of transaction hashes.

    Handles:
        - Empty list: returns 32 zero bytes
        - Single transaction: returns its hash
        - Odd number: duplicates the last element
        - Builds tree bottom-up

    Args:
        tx_hashes: List of 32-byte transaction hashes

    Returns:
        32-byte Merkle root

    Example:
        hashes = [hash_tx(tx) for tx in transactions]
        root = compute_merkle_root(hashes)
    """
    # Empty case
    if not tx_hashes:
        return b'\x00' * 32

    # Single transaction
    if len(tx_hashes) == 1:
        return tx_hashes[0]

    # Make a copy to avoid modifying input
    current_level = list(tx_hashes)

    # Build tree bottom-up
    while len(current_level) > 1:
        next_level = []

        # If odd number, duplicate last element
        if len(current_level) % 2 == 1:
            current_level.append(current_level[-1])

        # Pair up and hash
        for i in range(0, len(current_level), 2):
            parent = merkle_hash(current_level[i], current_level[i + 1])
            next_level.append(parent)

        current_level = next_level

    return current_level[0]


def compute_merkle_root_with_tree(
    tx_hashes: List[bytes]
) -> Tuple[bytes, List[List[bytes]]]:
    """
    Compute Merkle root and return the full tree.

    Args:
        tx_hashes: List of transaction hashes

    Returns:
        (root, tree) where tree[0] is leaves, tree[-1] is [root]
    """
    if not tx_hashes:
        return b'\x00' * 32, [[b'\x00' * 32]]

    if len(tx_hashes) == 1:
        return tx_hashes[0], [tx_hashes]

    tree = [list(tx_hashes)]
    current_level = list(tx_hashes)

    while len(current_level) > 1:
        next_level = []

        if len(current_level) % 2 == 1:
            current_level.append(current_level[-1])

        for i in range(0, len(current_level), 2):
            parent = merkle_hash(current_level[i], current_level[i + 1])
            next_level.append(parent)

        tree.append(next_level)
        current_level = next_level

    return current_level[0], tree


# =============================================================================
# MERKLE PROOF
# =============================================================================

@dataclass
class MerkleProof:
    """
    Proof that a transaction is included in a Merkle tree.

    A Merkle proof consists of the transaction hash plus the
    sibling hashes needed to reconstruct the path to the root.

    Attributes:
        tx_hash: The transaction hash being proved
        path: List of (sibling_hash, direction) pairs
              direction is 'left' if sibling is on left, 'right' if on right
        root: The Merkle root

    Verification:
        Start with tx_hash, combine with each sibling according to direction,
        result should equal root.
    """
    tx_hash: bytes
    path: List[Tuple[bytes, str]]
    root: bytes

    def verify(self) -> bool:
        """
        Verify the Merkle proof.

        Returns:
            True if proof is valid (reconstructed root matches claimed root)
        """
        current = self.tx_hash

        for sibling, direction in self.path:
            if direction == 'left':
                current = merkle_hash(sibling, current)
            else:  # direction == 'right'
                current = merkle_hash(current, sibling)

        return current == self.root

    def serialize(self) -> bytes:
        """
        Serialize proof to bytes.

        Format:
            32 bytes: tx_hash
            32 bytes: root
            4 bytes: path_length (uint32)
            For each path element:
                32 bytes: sibling_hash
                1 byte: direction (0=left, 1=right)
        """
        import struct

        parts = []
        parts.append(self.tx_hash)
        parts.append(self.root)
        parts.append(struct.pack('<I', len(self.path)))

        for sibling, direction in self.path:
            parts.append(sibling)
            parts.append(b'\x00' if direction == 'left' else b'\x01')

        return b''.join(parts)

    @classmethod
    def deserialize(cls, data: bytes) -> 'MerkleProof':
        """
        Deserialize proof from bytes.
        """
        import struct

        offset = 0
        tx_hash = data[offset:offset+32]; offset += 32
        root = data[offset:offset+32]; offset += 32
        path_length = struct.unpack_from('<I', data, offset)[0]; offset += 4

        path = []
        for _ in range(path_length):
            sibling = data[offset:offset+32]; offset += 32
            direction = 'left' if data[offset] == 0 else 'right'; offset += 1
            path.append((sibling, direction))

        return cls(tx_hash=tx_hash, path=path, root=root)

    def __repr__(self) -> str:
        return (
            f"MerkleProof(tx={self.tx_hash[:4].hex()}..., "
            f"path_len={len(self.path)}, "
            f"valid={self.verify()})"
        )


def generate_merkle_proof(tx_hashes: List[bytes], index: int) -> MerkleProof:
    """
    Generate a Merkle proof for the transaction at given index.

    Args:
        tx_hashes: List of all transaction hashes
        index: Index of transaction to prove

    Returns:
        MerkleProof for the transaction

    Raises:
        IndexError: If index is out of range
    """
    if not tx_hashes:
        raise ValueError("Cannot generate proof for empty tree")

    if index < 0 or index >= len(tx_hashes):
        raise IndexError(f"Index {index} out of range [0, {len(tx_hashes)})")

    # Get the full tree
    root, tree = compute_merkle_root_with_tree(tx_hashes)

    # Build the path from leaf to root
    path = []
    current_index = index

    for level in range(len(tree) - 1):  # Don't include root level
        level_hashes = tree[level]

        # Handle odd-sized levels (last element duplicated)
        if len(level_hashes) % 2 == 1 and current_index == len(level_hashes) - 1:
            # This element was duplicated
            sibling_index = current_index
        elif current_index % 2 == 0:
            # Current is left child, sibling is on right
            sibling_index = current_index + 1
            if sibling_index >= len(level_hashes):
                sibling_index = current_index  # Duplicate case
        else:
            # Current is right child, sibling is on left
            sibling_index = current_index - 1

        sibling_hash = level_hashes[sibling_index] if sibling_index < len(level_hashes) else level_hashes[-1]

        # Direction indicates where the sibling is
        if current_index % 2 == 0:
            direction = 'right'  # Sibling is on right
        else:
            direction = 'left'   # Sibling is on left

        path.append((sibling_hash, direction))

        # Move to parent level
        current_index = current_index // 2

    return MerkleProof(
        tx_hash=tx_hashes[index],
        path=path,
        root=root
    )


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def hash_transaction(tx_data: bytes) -> bytes:
    """
    Hash transaction data for Merkle tree inclusion.

    Args:
        tx_data: Serialized transaction bytes

    Returns:
        32-byte transaction hash
    """
    return double_sha256(tx_data)


def verify_merkle_path(
    tx_hash: bytes,
    path: List[Tuple[bytes, str]],
    root: bytes
) -> bool:
    """
    Verify a Merkle path without creating a MerkleProof object.

    Args:
        tx_hash: Transaction hash
        path: List of (sibling, direction) pairs
        root: Expected Merkle root

    Returns:
        True if path is valid
    """
    current = tx_hash

    for sibling, direction in path:
        if direction == 'left':
            current = merkle_hash(sibling, current)
        else:
            current = merkle_hash(current, sibling)

    return current == root


def get_merkle_tree_height(n_transactions: int) -> int:
    """
    Get the height of a Merkle tree with n transactions.

    Args:
        n_transactions: Number of leaf nodes

    Returns:
        Tree height (number of levels including leaves)
    """
    if n_transactions <= 0:
        return 0
    if n_transactions == 1:
        return 1

    import math
    return math.ceil(math.log2(n_transactions)) + 1


def get_proof_size(n_transactions: int) -> int:
    """
    Get the size of a Merkle proof in bytes.

    Args:
        n_transactions: Number of transactions in tree

    Returns:
        Proof size in bytes
    """
    if n_transactions <= 1:
        return 64 + 4  # tx_hash + root + path_length (empty path)

    import math
    path_length = math.ceil(math.log2(n_transactions))

    # tx_hash(32) + root(32) + path_length(4) + path_elements(33 each)
    return 32 + 32 + 4 + path_length * 33


# =============================================================================
# BATCH OPERATIONS
# =============================================================================

def generate_all_proofs(tx_hashes: List[bytes]) -> List[MerkleProof]:
    """
    Generate proofs for all transactions efficiently.

    More efficient than calling generate_merkle_proof for each
    because the tree is only computed once.

    Args:
        tx_hashes: List of transaction hashes

    Returns:
        List of MerkleProof objects, one per transaction
    """
    if not tx_hashes:
        return []

    root, tree = compute_merkle_root_with_tree(tx_hashes)
    proofs = []

    for index in range(len(tx_hashes)):
        path = []
        current_index = index

        for level in range(len(tree) - 1):
            level_hashes = tree[level]

            # Handle odd-sized levels
            actual_size = len(level_hashes)
            if actual_size % 2 == 1:
                level_hashes = level_hashes + [level_hashes[-1]]

            if current_index % 2 == 0:
                sibling_index = current_index + 1
                direction = 'right'
            else:
                sibling_index = current_index - 1
                direction = 'left'

            sibling_hash = level_hashes[sibling_index]
            path.append((sibling_hash, direction))

            current_index = current_index // 2

        proofs.append(MerkleProof(
            tx_hash=tx_hashes[index],
            path=path,
            root=root
        ))

    return proofs


def verify_all_proofs(proofs: List[MerkleProof]) -> bool:
    """
    Verify all proofs in a batch.

    All proofs must have the same root and all must be valid.

    Args:
        proofs: List of MerkleProof objects

    Returns:
        True if all proofs are valid and consistent
    """
    if not proofs:
        return True

    expected_root = proofs[0].root

    for proof in proofs:
        if proof.root != expected_root:
            return False
        if not proof.verify():
            return False

    return True


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    # Hashing
    'double_sha256',
    'merkle_hash',
    # Root computation
    'compute_merkle_root',
    'compute_merkle_root_with_tree',
    # Proofs
    'MerkleProof',
    'generate_merkle_proof',
    'verify_merkle_path',
    # Utilities
    'hash_transaction',
    'get_merkle_tree_height',
    'get_proof_size',
    # Batch
    'generate_all_proofs',
    'verify_all_proofs',
]
