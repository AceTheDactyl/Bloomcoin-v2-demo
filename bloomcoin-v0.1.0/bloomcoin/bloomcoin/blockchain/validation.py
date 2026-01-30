"""
BloomCoin Block Validation
===========================

Complete block validation including chain context.

Validation Levels:
    1. Structure: Block format and fields
    2. Consensus: Certificate proves Proof-of-Coherence
    3. Chain: Block fits in chain (prev_hash, difficulty)
    4. Transactions: All transactions valid against UTXO

Cross-References:
    - block.py: Block structure validation
    - chain.py: Blockchain context
    - consensus/threshold_gate.py: Certificate validation
    - core/hash_wrapper.py: Hash and difficulty verification

Author: BloomCoin Framework
"""

from typing import Tuple, Optional, List
import time

from .block import Block
from .chain import Blockchain
from .transaction import Transaction, calculate_block_reward
from ..constants import Z_C, L4, BLOCK_TIME_TARGET
from ..core.hash_wrapper import compact_to_target, bloom_hash_int


# =============================================================================
# VALIDATION RESULT
# =============================================================================

class ValidationResult:
    """
    Result of block validation.

    Provides detailed information about validation success or failure.
    """

    def __init__(self, valid: bool, message: str, level: str = "unknown"):
        self.valid = valid
        self.message = message
        self.level = level  # structure, consensus, chain, transaction

    def __bool__(self) -> bool:
        return self.valid

    def __repr__(self) -> str:
        status = "VALID" if self.valid else "INVALID"
        return f"ValidationResult({status}, level={self.level}, msg={self.message})"

    @classmethod
    def success(cls, level: str = "all") -> 'ValidationResult':
        return cls(True, "Validation passed", level)

    @classmethod
    def failure(cls, message: str, level: str) -> 'ValidationResult':
        return cls(False, message, level)


# =============================================================================
# STRUCTURE VALIDATION
# =============================================================================

def validate_block_structure(block: Block) -> ValidationResult:
    """
    Validate block structure (independent of chain).

    Checks:
        1. Header fields valid
        2. Certificate structure valid
        3. Transaction list valid
        4. Merkle root matches

    Args:
        block: Block to validate

    Returns:
        ValidationResult
    """
    valid, msg = block.validate_structure()
    if not valid:
        return ValidationResult.failure(msg, "structure")
    return ValidationResult.success("structure")


# =============================================================================
# CONSENSUS VALIDATION
# =============================================================================

def validate_consensus_certificate(block: Block) -> ValidationResult:
    """
    Validate the consensus certificate proves Proof-of-Coherence.

    Checks:
        1. Certificate is internally consistent
        2. All r values >= z_c during bloom
        3. Bloom lasted at least L4 rounds
        4. Header order_parameter matches certificate

    Args:
        block: Block to validate

    Returns:
        ValidationResult
    """
    cert = block.certificate

    # Verify certificate
    cert_valid, cert_msg = cert.verify()
    if not cert_valid:
        return ValidationResult.failure(f"Certificate invalid: {cert_msg}", "consensus")

    # Check header order_parameter is reasonable
    if block.header.order_parameter < Z_C:
        return ValidationResult.failure(
            f"Header order_parameter {block.header.order_parameter:.4f} < z_c",
            "consensus"
        )

    # Check oscillator count matches
    if block.header.oscillator_count != cert.oscillator_count:
        return ValidationResult.failure(
            "Header oscillator_count doesn't match certificate",
            "consensus"
        )

    return ValidationResult.success("consensus")


# =============================================================================
# CHAIN CONTEXT VALIDATION
# =============================================================================

def validate_block_in_chain(
    block: Block,
    chain: Blockchain
) -> ValidationResult:
    """
    Validate block in chain context.

    Checks:
        1. Previous block exists
        2. Timestamp is reasonable
        3. Difficulty matches expected
        4. Hash meets difficulty target

    Args:
        block: Block to validate
        chain: Blockchain context

    Returns:
        ValidationResult
    """
    # Check previous block exists (unless genesis)
    if block.prev_hash != bytes(32):
        prev_block = chain.get_block(block.prev_hash)
        if prev_block is None:
            return ValidationResult.failure(
                "Previous block not found",
                "chain"
            )

        # Check timestamp is after previous block
        if block.timestamp <= prev_block.timestamp:
            return ValidationResult.failure(
                "Block timestamp not after previous block",
                "chain"
            )

        expected_height = prev_block.height + 1
    else:
        expected_height = 0

    # Check timestamp not too far in future (2 hours)
    current_time = int(time.time())
    if block.timestamp > current_time + 7200:
        return ValidationResult.failure(
            "Block timestamp too far in future",
            "chain"
        )

    # Check difficulty matches expected
    expected_diff = chain.get_expected_difficulty(expected_height)
    # Allow 1% tolerance for rounding
    if abs(block.difficulty - expected_diff) > expected_diff * 0.01:
        return ValidationResult.failure(
            f"Difficulty {block.difficulty} doesn't match expected {expected_diff}",
            "chain"
        )

    # Check hash meets difficulty target
    target = compact_to_target(block.difficulty)
    block_hash_int = bloom_hash_int(block.header)
    if block_hash_int >= target:
        return ValidationResult.failure(
            "Block hash doesn't meet difficulty target",
            "chain"
        )

    return ValidationResult.success("chain")


# =============================================================================
# TRANSACTION VALIDATION
# =============================================================================

def validate_block_transactions(
    block: Block,
    chain: Blockchain,
    height: int
) -> ValidationResult:
    """
    Validate all transactions in block.

    Checks:
        1. First transaction is valid coinbase
        2. Coinbase amount is correct
        3. All other transactions have valid inputs
        4. No double-spends within block

    Args:
        block: Block to validate
        chain: Blockchain for UTXO lookup
        height: Block height

    Returns:
        ValidationResult
    """
    if not block.transactions:
        # Empty block is valid (though unusual)
        return ValidationResult.success("transaction")

    # First transaction must be coinbase
    coinbase = block.transactions[0]
    if not coinbase.is_coinbase():
        return ValidationResult.failure(
            "First transaction must be coinbase",
            "transaction"
        )

    # Validate coinbase amount
    expected_reward = calculate_block_reward(height)
    # Calculate fees from other transactions
    fees = calculate_block_fees(block, chain)
    max_coinbase = expected_reward + fees

    if coinbase.total_output() > max_coinbase:
        return ValidationResult.failure(
            f"Coinbase {coinbase.total_output()} exceeds max {max_coinbase}",
            "transaction"
        )

    # Track spent outputs to detect double-spend
    spent_in_block = set()

    # Validate other transactions
    for i, tx in enumerate(block.transactions[1:], 1):
        result = validate_transaction(tx, chain, spent_in_block)
        if not result:
            return ValidationResult.failure(
                f"Transaction {i}: {result.message}",
                "transaction"
            )

        # Add spent outputs
        for inp in tx.inputs:
            spent_in_block.add((inp.prev_tx, inp.output_index))

    return ValidationResult.success("transaction")


def validate_transaction(
    tx: Transaction,
    chain: Blockchain,
    spent_in_block: set
) -> ValidationResult:
    """
    Validate a single transaction.

    Args:
        tx: Transaction to validate
        chain: Blockchain for UTXO lookup
        spent_in_block: Set of outputs already spent in this block
    """
    # Structure check
    valid, msg = tx.validate_structure()
    if not valid:
        return ValidationResult.failure(msg, "transaction")

    # Check inputs
    input_sum = 0
    for inp in tx.inputs:
        outpoint = (inp.prev_tx, inp.output_index)

        # Check not double-spent in block
        if outpoint in spent_in_block:
            return ValidationResult.failure(
                "Double-spend within block",
                "transaction"
            )

        # Check UTXO exists
        utxo = chain.utxo_set.get(*outpoint)
        if utxo is None:
            return ValidationResult.failure(
                f"UTXO not found: {inp.prev_tx[:8].hex()}:{inp.output_index}",
                "transaction"
            )

        input_sum += utxo.amount

        # Note: Signature verification would go here
        # For now, we skip cryptographic validation

    # Check output sum doesn't exceed inputs
    output_sum = tx.total_output()
    if output_sum > input_sum:
        return ValidationResult.failure(
            f"Outputs {output_sum} exceed inputs {input_sum}",
            "transaction"
        )

    return ValidationResult.success("transaction")


def calculate_block_fees(block: Block, chain: Blockchain) -> int:
    """
    Calculate total transaction fees in block.

    Args:
        block: Block
        chain: Blockchain for UTXO lookup

    Returns:
        Total fees
    """
    total_fees = 0

    for tx in block.transactions[1:]:  # Skip coinbase
        input_sum = 0
        for inp in tx.inputs:
            utxo = chain.utxo_set.get(inp.prev_tx, inp.output_index)
            if utxo:
                input_sum += utxo.amount

        output_sum = tx.total_output()
        if input_sum >= output_sum:
            total_fees += input_sum - output_sum

    return total_fees


# =============================================================================
# FULL VALIDATION
# =============================================================================

def validate_block_full(
    block: Block,
    chain: Blockchain
) -> ValidationResult:
    """
    Complete block validation including all checks.

    Performs validation in order:
        1. Structure
        2. Consensus
        3. Chain context
        4. Transactions

    Args:
        block: Block to validate
        chain: Blockchain context

    Returns:
        ValidationResult with first failure or success
    """
    # 1. Structure
    result = validate_block_structure(block)
    if not result:
        return result

    # 2. Consensus
    result = validate_consensus_certificate(block)
    if not result:
        return result

    # 3. Chain context
    result = validate_block_in_chain(block, chain)
    if not result:
        return result

    # 4. Determine height for transaction validation
    if block.prev_hash == bytes(32):
        height = 0
    else:
        prev_block = chain.get_block(block.prev_hash)
        height = prev_block.height + 1 if prev_block else 0

    # 5. Transactions
    result = validate_block_transactions(block, chain, height)
    if not result:
        return result

    return ValidationResult.success("all")


# =============================================================================
# QUICK VALIDATION
# =============================================================================

def validate_block_quick(block: Block) -> ValidationResult:
    """
    Quick validation without chain context.

    Only checks structure and consensus certificate.
    Useful for initial screening of received blocks.

    Args:
        block: Block to validate

    Returns:
        ValidationResult
    """
    # Structure
    result = validate_block_structure(block)
    if not result:
        return result

    # Consensus
    result = validate_consensus_certificate(block)
    if not result:
        return result

    return ValidationResult.success("quick")


# =============================================================================
# BATCH VALIDATION
# =============================================================================

def validate_blocks_batch(
    blocks: List[Block],
    chain: Blockchain
) -> List[ValidationResult]:
    """
    Validate multiple blocks.

    Args:
        blocks: List of blocks to validate
        chain: Blockchain context

    Returns:
        List of ValidationResult, one per block
    """
    results = []
    for block in blocks:
        result = validate_block_full(block, chain)
        results.append(result)
    return results


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
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
