"""
BloomCoin Core Module
======================

Provides fundamental cryptographic and mathematical primitives:

Components:
    - lucas_matrix: Fibonacci/Lucas matrix operations for nonce generation
    - hash_wrapper: SHA256 with phase-encoding for Proof-of-Coherence
    - merkle: Merkle tree for transaction commitment

Dependency Order:
    constants.py -> lucas_matrix.py -> hash_wrapper.py -> merkle.py

Usage:
    from bloomcoin.core import (
        # Lucas operations
        lucas_trace, fibonacci_mod, matrix_power_mod,
        lucas_nonce, lucas_nonce_batch,
        # Hashing
        PhaseEncodedHeader, bloom_hash, verify_bloom,
        create_header, create_genesis_header,
        # Merkle
        compute_merkle_root, generate_merkle_proof, MerkleProof
    )

Cross-References:
    - SINGULARITY_ENGINE.py: R matrix is the fundamental recursion
    - resonance_formalism.md: Lucas numbers in mass formulas
    - consensus/: Uses bloom verification in mining
"""

# Lucas matrix operations
from .lucas_matrix import (
    # Constants
    R_MATRIX,
    I_MATRIX,
    # Matrix operations
    matrix_multiply_mod,
    matrix_power_mod,
    # Lucas/Fibonacci
    lucas_trace,
    fibonacci_mod,
    fibonacci_pair_mod,
    # Nonce generation
    lucas_nonce,
    lucas_nonce_batch,
    # Verification
    verify_lucas_identity,
    verify_matrix_eigenvalues,
    get_matrix_at_power,
    # Cross-reference
    lucas_mass_indices,
)

# Hash wrapper
from .hash_wrapper import (
    # Header
    PhaseEncodedHeader,
    # Hashing
    double_sha256,
    bloom_hash,
    bloom_hash_int,
    # Difficulty
    compact_to_target,
    target_to_compact,
    verify_bloom,
    compute_difficulty,
    # Creation
    create_genesis_header,
    create_header,
)

# Merkle tree
from .merkle import (
    # Hashing
    merkle_hash,
    # Root computation
    compute_merkle_root,
    compute_merkle_root_with_tree,
    # Proofs
    MerkleProof,
    generate_merkle_proof,
    verify_merkle_path,
    # Utilities
    hash_transaction,
    get_merkle_tree_height,
    get_proof_size,
    # Batch
    generate_all_proofs,
    verify_all_proofs,
)


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    # Lucas matrix
    'R_MATRIX',
    'I_MATRIX',
    'matrix_multiply_mod',
    'matrix_power_mod',
    'lucas_trace',
    'fibonacci_mod',
    'fibonacci_pair_mod',
    'lucas_nonce',
    'lucas_nonce_batch',
    'verify_lucas_identity',
    'verify_matrix_eigenvalues',
    'get_matrix_at_power',
    'lucas_mass_indices',
    # Hash wrapper
    'PhaseEncodedHeader',
    'double_sha256',
    'bloom_hash',
    'bloom_hash_int',
    'compact_to_target',
    'target_to_compact',
    'verify_bloom',
    'compute_difficulty',
    'create_genesis_header',
    'create_header',
    # Merkle
    'merkle_hash',
    'compute_merkle_root',
    'compute_merkle_root_with_tree',
    'MerkleProof',
    'generate_merkle_proof',
    'verify_merkle_path',
    'hash_transaction',
    'get_merkle_tree_height',
    'get_proof_size',
    'generate_all_proofs',
    'verify_all_proofs',
]
