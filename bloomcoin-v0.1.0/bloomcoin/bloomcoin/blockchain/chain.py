"""
BloomCoin Blockchain Implementation
=====================================

Blockchain data structure with validation and state management.

Components:
    - ChainState: Current state (height, tip, UTXO set)
    - Blockchain: Block storage and chain operations
    - UTXO management

Cross-References:
    - block.py: Block, create_genesis_block
    - transaction.py: Transaction, TxOutput
    - validation.py: Full block validation

Author: BloomCoin Framework
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, Iterator, List, Tuple, Set
import threading
import time

from .block import Block, create_genesis_block
from .transaction import Transaction, TxOutput, calculate_block_reward
from ..constants import (
    DIFFICULTY_INTERVAL, BLOCK_TIME_TARGET,
    DEFAULT_OSCILLATOR_COUNT
)
from ..mining.difficulty import calculate_new_difficulty


# =============================================================================
# UTXO (Unspent Transaction Output)
# =============================================================================

@dataclass
class UTXO:
    """
    Unspent Transaction Output.

    Represents an output that has not yet been spent.

    Attributes:
        tx_hash: Transaction hash containing this output
        output_index: Index of output in transaction
        output: The actual TxOutput
        block_height: Height of block containing transaction
        is_coinbase: Whether this is from a coinbase transaction
    """
    tx_hash: bytes
    output_index: int
    output: TxOutput
    block_height: int
    is_coinbase: bool = False

    @property
    def amount(self) -> int:
        return self.output.amount

    @property
    def address(self) -> bytes:
        return self.output.address

    def outpoint(self) -> Tuple[bytes, int]:
        """Return (tx_hash, output_index) tuple for UTXO lookup."""
        return (self.tx_hash, self.output_index)

    def __repr__(self) -> str:
        bloom = self.amount / 10**8
        return f"UTXO({bloom:.4f} BLOOM, height={self.block_height})"


# =============================================================================
# CHAIN STATE
# =============================================================================

@dataclass
class ChainState:
    """
    Current state of the blockchain.

    Tracks the chain tip and cumulative statistics.

    Attributes:
        height: Current chain height (genesis = 0)
        tip_hash: Hash of the tip (latest) block
        total_work: Cumulative difficulty
        total_transactions: Total transactions processed
        total_coins: Total coins in circulation
    """
    height: int = 0
    tip_hash: bytes = field(default_factory=lambda: bytes(32))
    total_work: float = 0.0
    total_transactions: int = 0
    total_coins: int = 0


# =============================================================================
# UTXO SET
# =============================================================================

class UTXOSet:
    """
    Set of unspent transaction outputs.

    Provides efficient lookup and update of UTXOs.
    """

    def __init__(self):
        # Main storage: (tx_hash, output_index) -> UTXO
        self._utxos: Dict[Tuple[bytes, int], UTXO] = {}
        # Index by address for balance queries
        self._by_address: Dict[bytes, Set[Tuple[bytes, int]]] = {}

    def add(self, utxo: UTXO):
        """Add a UTXO to the set."""
        key = utxo.outpoint()
        self._utxos[key] = utxo

        # Update address index
        addr = utxo.address
        if addr not in self._by_address:
            self._by_address[addr] = set()
        self._by_address[addr].add(key)

    def remove(self, tx_hash: bytes, output_index: int) -> Optional[UTXO]:
        """Remove and return a UTXO from the set."""
        key = (tx_hash, output_index)
        utxo = self._utxos.pop(key, None)

        if utxo:
            # Update address index
            addr = utxo.address
            if addr in self._by_address:
                self._by_address[addr].discard(key)
                if not self._by_address[addr]:
                    del self._by_address[addr]

        return utxo

    def get(self, tx_hash: bytes, output_index: int) -> Optional[UTXO]:
        """Get a UTXO without removing it."""
        return self._utxos.get((tx_hash, output_index))

    def contains(self, tx_hash: bytes, output_index: int) -> bool:
        """Check if UTXO exists."""
        return (tx_hash, output_index) in self._utxos

    def get_by_address(self, address: bytes) -> List[UTXO]:
        """Get all UTXOs for an address."""
        keys = self._by_address.get(address, set())
        return [self._utxos[k] for k in keys if k in self._utxos]

    def get_balance(self, address: bytes) -> int:
        """Get total balance for an address."""
        return sum(u.amount for u in self.get_by_address(address))

    def __len__(self) -> int:
        return len(self._utxos)

    def total_value(self) -> int:
        """Total value of all UTXOs."""
        return sum(u.amount for u in self._utxos.values())


# =============================================================================
# BLOCKCHAIN
# =============================================================================

class Blockchain:
    """
    BloomCoin blockchain.

    Stores blocks and maintains chain state.
    Thread-safe for concurrent access.

    Features:
        - In-memory block storage
        - UTXO set for transaction validation
        - Difficulty adjustment
        - Fork handling (longest chain rule)
    """

    def __init__(
        self,
        genesis_reward_address: Optional[bytes] = None,
        auto_create_genesis: bool = True
    ):
        """
        Initialize blockchain.

        Args:
            genesis_reward_address: Address for genesis block reward
            auto_create_genesis: If True, create genesis block on init
        """
        # Block storage
        self._blocks: Dict[bytes, Block] = {}
        self._height_index: Dict[int, bytes] = {}

        # Chain state
        self._state = ChainState()

        # UTXO set
        self._utxo_set = UTXOSet()

        # Thread safety
        self._lock = threading.RLock()

        # Initialize with genesis block
        if auto_create_genesis:
            genesis = create_genesis_block(
                reward_address=genesis_reward_address,
                oscillator_count=DEFAULT_OSCILLATOR_COUNT
            )
            self._add_block_internal(genesis, height=0)
            # Apply genesis transactions to UTXO set
            self._apply_block_to_utxo(genesis, height=0)

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def height(self) -> int:
        """Current chain height."""
        return self._state.height

    @property
    def tip(self) -> Block:
        """Tip (latest) block."""
        return self._blocks[self._state.tip_hash]

    @property
    def tip_hash(self) -> bytes:
        """Hash of tip block."""
        return self._state.tip_hash

    @property
    def total_work(self) -> float:
        """Cumulative difficulty."""
        return self._state.total_work

    @property
    def utxo_set(self) -> UTXOSet:
        """UTXO set."""
        return self._utxo_set

    # -------------------------------------------------------------------------
    # Block Access
    # -------------------------------------------------------------------------

    def get_block(self, block_hash: bytes) -> Optional[Block]:
        """Get block by hash."""
        return self._blocks.get(block_hash)

    def get_block_at_height(self, height: int) -> Optional[Block]:
        """Get block at specific height on main chain."""
        block_hash = self._height_index.get(height)
        if block_hash:
            return self._blocks.get(block_hash)
        return None

    def has_block(self, block_hash: bytes) -> bool:
        """Check if block exists."""
        return block_hash in self._blocks

    def get_blocks_range(self, start: int, end: int) -> List[Block]:
        """Get blocks in height range [start, end)."""
        blocks = []
        for h in range(start, end):
            block = self.get_block_at_height(h)
            if block:
                blocks.append(block)
        return blocks

    # -------------------------------------------------------------------------
    # Block Addition
    # -------------------------------------------------------------------------

    def add_block(self, block: Block) -> Tuple[bool, str]:
        """
        Add a new block to the chain.

        Validates block and updates chain state.

        Args:
            block: Block to add

        Returns:
            (success, error_message)
        """
        with self._lock:
            # Validate block structure
            valid, msg = block.validate_structure()
            if not valid:
                return False, f"Invalid structure: {msg}"

            # Check previous block exists
            if block.prev_hash != bytes(32):  # Not genesis
                prev_block = self.get_block(block.prev_hash)
                if prev_block is None:
                    return False, "Previous block not found"

                expected_height = prev_block.height + 1
            else:
                expected_height = 0

            # Check if this extends the main chain
            if block.prev_hash == self._state.tip_hash:
                # Simple case: extends tip
                return self._extend_chain(block, expected_height)
            else:
                # Could be a fork
                return self._handle_potential_fork(block, expected_height)

    def _extend_chain(self, block: Block, height: int) -> Tuple[bool, str]:
        """Extend the main chain with a new block."""
        # Validate transactions against UTXO set
        valid, msg = self._validate_block_transactions(block, height)
        if not valid:
            return False, msg

        # Add block
        self._add_block_internal(block, height)

        # Update UTXO set
        self._apply_block_to_utxo(block, height)

        return True, ""

    def _add_block_internal(self, block: Block, height: int):
        """Internal block addition (no validation)."""
        block.height = height
        self._blocks[block.hash] = block
        self._height_index[height] = block.hash
        self._state.height = height
        self._state.tip_hash = block.hash
        self._state.total_work += block.difficulty
        self._state.total_transactions += len(block.transactions)

    def _handle_potential_fork(
        self,
        block: Block,
        height: int
    ) -> Tuple[bool, str]:
        """
        Handle a block that doesn't extend the main chain.

        Uses longest chain rule (most cumulative work).
        """
        # Find the block this extends
        prev_block = self.get_block(block.prev_hash)
        if prev_block is None:
            return False, "Previous block not found for fork"

        # Calculate work of the potential new chain
        fork_work = prev_block.difficulty + block.difficulty

        # Compare with current chain work from same height
        # For simplicity, we only accept if it would create a longer chain
        if height > self._state.height:
            # This fork is longer, reorganize
            # Note: Full reorg implementation would be more complex
            return self._extend_chain(block, height)
        else:
            # Store the block but don't switch chains
            block.height = height
            self._blocks[block.hash] = block
            return True, "Block stored (fork, not main chain)"

    # -------------------------------------------------------------------------
    # Transaction Validation
    # -------------------------------------------------------------------------

    def _validate_block_transactions(
        self,
        block: Block,
        height: int
    ) -> Tuple[bool, str]:
        """Validate all transactions in a block against UTXO set."""
        if not block.transactions:
            return True, ""

        # First transaction must be coinbase
        coinbase = block.transactions[0]
        if not coinbase.is_coinbase():
            return False, "First transaction must be coinbase"

        # Validate coinbase amount
        expected_reward = calculate_block_reward(height)
        # Note: Would also add fees here
        coinbase_output = coinbase.total_output()
        if coinbase_output > expected_reward:
            return False, f"Coinbase reward {coinbase_output} exceeds allowed {expected_reward}"

        # Validate other transactions
        spent_in_block: Set[Tuple[bytes, int]] = set()

        for i, tx in enumerate(block.transactions[1:], 1):
            # Check each input
            for inp in tx.inputs:
                outpoint = (inp.prev_tx, inp.output_index)

                # Check not double-spent within block
                if outpoint in spent_in_block:
                    return False, f"Double spend in block (tx {i})"
                spent_in_block.add(outpoint)

                # Check UTXO exists
                if not self._utxo_set.contains(*outpoint):
                    return False, f"UTXO not found for tx {i} input"

        return True, ""

    def _apply_block_to_utxo(self, block: Block, height: int):
        """Update UTXO set with block transactions."""
        for tx in block.transactions:
            # Remove spent outputs
            if not tx.is_coinbase():
                for inp in tx.inputs:
                    self._utxo_set.remove(inp.prev_tx, inp.output_index)

            # Add new outputs
            for idx, output in enumerate(tx.outputs):
                utxo = UTXO(
                    tx_hash=tx.hash,
                    output_index=idx,
                    output=output,
                    block_height=height,
                    is_coinbase=tx.is_coinbase()
                )
                self._utxo_set.add(utxo)

    # -------------------------------------------------------------------------
    # Difficulty
    # -------------------------------------------------------------------------

    def get_expected_difficulty(self, height: int) -> int:
        """
        Get expected difficulty for block at given height.

        Difficulty adjusts every DIFFICULTY_INTERVAL blocks.
        """
        if height == 0:
            return 0x1d00ffff  # Genesis difficulty

        # Only adjust at interval boundaries
        if height % DIFFICULTY_INTERVAL != 0:
            return self.tip.difficulty

        # Get block times for adjustment
        block_times = self.get_recent_block_times(DIFFICULTY_INTERVAL)

        if not block_times:
            return self.tip.difficulty

        # Calculate new difficulty
        current_diff = float(self.tip.difficulty)
        new_diff = calculate_new_difficulty(
            current_diff, block_times, BLOCK_TIME_TARGET
        )

        return int(new_diff)

    def get_recent_block_times(self, count: int) -> List[float]:
        """Get timestamps differences for recent blocks."""
        times = []
        current = self.tip

        for _ in range(min(count, self._state.height)):
            if current.height <= 0:
                break
            prev = self.get_block(current.prev_hash)
            if prev:
                time_diff = current.timestamp - prev.timestamp
                times.append(float(time_diff))
                current = prev
            else:
                break

        return times

    # -------------------------------------------------------------------------
    # Iteration
    # -------------------------------------------------------------------------

    def iterate_blocks(
        self,
        start: int = 0,
        end: Optional[int] = None
    ) -> Iterator[Block]:
        """
        Iterate over blocks in height order.

        Args:
            start: Starting height (inclusive)
            end: Ending height (exclusive, None = to tip)
        """
        if end is None:
            end = self._state.height + 1

        for height in range(start, end):
            block = self.get_block_at_height(height)
            if block:
                yield block

    def __iter__(self) -> Iterator[Block]:
        """Iterate over all blocks."""
        return self.iterate_blocks()

    def __len__(self) -> int:
        """Number of blocks in chain."""
        return self._state.height + 1

    # -------------------------------------------------------------------------
    # Chain Info
    # -------------------------------------------------------------------------

    def get_chain_info(self) -> dict:
        """Get summary information about the chain."""
        return {
            'height': self._state.height,
            'tip_hash': self._state.tip_hash.hex(),
            'total_work': self._state.total_work,
            'total_transactions': self._state.total_transactions,
            'utxo_count': len(self._utxo_set),
            'total_value': self._utxo_set.total_value(),
        }

    def __repr__(self) -> str:
        return (
            f"Blockchain(height={self._state.height}, "
            f"tip={self._state.tip_hash[:4].hex()}..., "
            f"utxos={len(self._utxo_set)})"
        )


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    'UTXO',
    'ChainState',
    'UTXOSet',
    'Blockchain',
]
