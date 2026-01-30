"""
BloomCoin Blockchain Module
============================

Chain data structures and validation for BloomCoin.

Components:
    - transaction: TxInput, TxOutput, Transaction
    - block: Block, BlockHeader, create_genesis_block
    - chain: Blockchain, UTXOSet, ChainState
    - validation: Full block validation

Key Difference from Bitcoin:
    Blocks contain a ConsensusCertificate proving Proof-of-Coherence
    was achieved, not just a nonce that produces a low hash.

Usage:
    from bloomcoin.blockchain import (
        # Transactions
        Transaction, TxInput, TxOutput, create_coinbase,
        # Blocks
        Block, BlockHeader, create_genesis_block, create_block,
        # Chain
        Blockchain, UTXOSet, UTXO,
        # Validation
        validate_block_full, ValidationResult
    )

    # Create and use blockchain
    chain = Blockchain()
    print(f"Genesis: {chain.tip.hash.hex()}")

    # Add a mined block
    success, msg = chain.add_block(new_block)

Cross-References:
    - consensus/: Proof-of-Coherence and certificates
    - core/: Hashing and Merkle trees
    - mining/: Block mining
"""

# Transaction
from .transaction import (
    TxInput,
    TxOutput,
    Transaction,
    calculate_block_reward,
    create_coinbase,
    hash_transaction,
    create_transfer,
)

# Block
from .block import (
    BlockHeader,
    Block,
    create_genesis_block,
    create_block,
)

# Chain
from .chain import (
    UTXO,
    ChainState,
    UTXOSet,
    Blockchain,
)

# Validation
from .validation import (
    ValidationResult,
    validate_block_structure,
    validate_consensus_certificate,
    validate_block_in_chain,
    validate_block_transactions,
    validate_transaction,
    calculate_block_fees,
    validate_block_full,
    validate_block_quick,
    validate_blocks_batch,
)


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    # Transaction
    'TxInput',
    'TxOutput',
    'Transaction',
    'calculate_block_reward',
    'create_coinbase',
    'hash_transaction',
    'create_transfer',
    # Block
    'BlockHeader',
    'Block',
    'create_genesis_block',
    'create_block',
    # Chain
    'UTXO',
    'ChainState',
    'UTXOSet',
    'Blockchain',
    # Validation
    'ValidationResult',
    'validate_block_structure',
    'validate_consensus_certificate',
    'validate_block_in_chain',
    'validate_block_transactions',
    'validate_transaction',
    'calculate_block_fees',
    'validate_block_full',
    'validate_block_quick',
    'validate_blocks_batch',
]
