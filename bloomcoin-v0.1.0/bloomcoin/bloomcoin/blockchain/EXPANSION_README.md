# Blockchain Module Expansion Guide

**Module**: `bloomcoin/blockchain/`  
**Purpose**: Chain data structures and validation  
**Priority**: PHASE 4 (Data Layer)

---

## Overview

The blockchain module implements the core data structures:

- **Block**: Container for transactions + consensus certificate
- **Chain**: Ordered sequence of blocks with validation
- **Transaction**: Value transfers between addresses

**Key Difference from Bitcoin**: Blocks contain a **ConsensusCertificate** proving Proof-of-Coherence was achieved, not just a nonce that produces a low hash.

---

## Block Structure

### Standard Fields (80 bytes)

| Field | Size | Description |
|-------|------|-------------|
| version | 4 | Protocol version |
| prev_hash | 32 | SHA256 of previous block |
| merkle_root | 32 | Transaction Merkle root |
| timestamp | 4 | Unix timestamp |
| difficulty | 4 | Encoded difficulty target |
| nonce | 4 | Lucas nonce |

### Phase Extension (12 bytes)

| Field | Size | Description |
|-------|------|-------------|
| order_parameter | 4 | Final r value (float32) |
| mean_phase | 4 | Final ψ value (float32) |
| oscillator_count | 4 | N used in consensus |

### Certificate (Variable)

| Field | Size | Description |
|-------|------|-------------|
| bloom_start | 4 | Round bloom began |
| bloom_end | 4 | Round bloom ended |
| r_values | 4 × len | r values during bloom |
| psi_values | 4 × len | ψ values during bloom |
| final_phases | 4 × N | Oscillator phases at seal |

---

## Phase 1: Block Implementation

### File: `block.py`

**Objective**: Block data structure with serialization.

### Implementation Steps

#### Step 1.1: Block Header

```python
from dataclasses import dataclass
import struct
import hashlib
from typing import Optional
from ..core.hash_wrapper import bloom_hash
from ..consensus.threshold_gate import ConsensusCertificate

@dataclass
class BlockHeader:
    """
    BloomCoin block header.
    
    Total: 92 bytes (80 standard + 12 phase extension)
    """
    version: int
    prev_hash: bytes  # 32 bytes
    merkle_root: bytes  # 32 bytes
    timestamp: int
    difficulty: int
    nonce: int
    order_parameter: float
    mean_phase: float
    oscillator_count: int
    
    def serialize(self) -> bytes:
        """
        Serialize header to bytes.
        
        Format:
            version (4) + prev_hash (32) + merkle_root (32) +
            timestamp (4) + difficulty (4) + nonce (4) +
            order_parameter (4) + mean_phase (4) + oscillator_count (4)
        """
        return struct.pack(
            '<I 32s 32s I I I f f I',
            self.version,
            self.prev_hash,
            self.merkle_root,
            self.timestamp,
            self.difficulty,
            self.nonce,
            self.order_parameter,
            self.mean_phase,
            self.oscillator_count
        )
    
    @classmethod
    def deserialize(cls, data: bytes) -> 'BlockHeader':
        """Deserialize from 92 bytes."""
        fields = struct.unpack('<I 32s 32s I I I f f I', data[:92])
        return cls(
            version=fields[0],
            prev_hash=fields[1],
            merkle_root=fields[2],
            timestamp=fields[3],
            difficulty=fields[4],
            nonce=fields[5],
            order_parameter=fields[6],
            mean_phase=fields[7],
            oscillator_count=fields[8]
        )
    
    def hash(self) -> bytes:
        """Compute block hash."""
        return bloom_hash(self)
```

#### Step 1.2: Full Block

```python
@dataclass
class Block:
    """
    Complete BloomCoin block.
    
    Contains:
        - Header (92 bytes)
        - Consensus certificate (variable)
        - Transactions (variable)
    """
    header: BlockHeader
    certificate: ConsensusCertificate
    transactions: list  # List[Transaction]
    
    _hash: bytes = None  # Cached hash
    
    @property
    def hash(self) -> bytes:
        """Block hash (cached)."""
        if self._hash is None:
            self._hash = self.header.hash()
        return self._hash
    
    @property
    def height(self) -> int:
        """Block height (must be set externally)."""
        return getattr(self, '_height', -1)
    
    @height.setter
    def height(self, value: int):
        self._height = value
    
    def serialize(self) -> bytes:
        """
        Serialize complete block.
        
        Format:
            header (92) + cert_len (4) + certificate + tx_count (4) + transactions
        """
        cert_bytes = self.certificate.serialize()
        tx_bytes = b''.join(tx.serialize() for tx in self.transactions)
        
        return (
            self.header.serialize() +
            struct.pack('<I', len(cert_bytes)) +
            cert_bytes +
            struct.pack('<I', len(self.transactions)) +
            tx_bytes
        )
    
    @classmethod
    def deserialize(cls, data: bytes) -> 'Block':
        """Deserialize from bytes."""
        # Parse header
        header = BlockHeader.deserialize(data[:92])
        offset = 92
        
        # Parse certificate
        cert_len = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4
        certificate = ConsensusCertificate.deserialize(data[offset:offset+cert_len])
        offset += cert_len
        
        # Parse transactions
        tx_count = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4
        transactions = []
        for _ in range(tx_count):
            tx, tx_len = Transaction.deserialize_with_length(data[offset:])
            transactions.append(tx)
            offset += tx_len
        
        return cls(header=header, certificate=certificate, transactions=transactions)
    
    def validate(self) -> tuple[bool, str]:
        """
        Validate block.
        
        Checks:
        1. Header hash meets difficulty
        2. Certificate proves r ≥ z_c for L₄ rounds
        3. Merkle root matches transactions
        4. All transactions are valid
        
        Returns:
            (is_valid, error_message)
        """
        from ..constants import Z_C, L4
        from ..core.merkle import compute_merkle_root
        
        # Check certificate
        if not self.certificate.verify():
            return False, "Invalid consensus certificate"
        
        # Check r threshold
        if self.header.order_parameter < Z_C:
            return False, f"Order parameter {self.header.order_parameter} < z_c"
        
        # Check bloom duration
        bloom_duration = self.certificate.bloom_end - self.certificate.bloom_start
        if bloom_duration < L4:
            return False, f"Bloom duration {bloom_duration} < L₄"
        
        # Check Merkle root
        tx_hashes = [tx.hash for tx in self.transactions]
        computed_root = compute_merkle_root(tx_hashes)
        if computed_root != self.header.merkle_root:
            return False, "Merkle root mismatch"
        
        # Validate transactions
        for tx in self.transactions:
            valid, msg = tx.validate()
            if not valid:
                return False, f"Invalid transaction: {msg}"
        
        return True, ""
```

#### Step 1.3: Genesis Block

```python
def create_genesis_block() -> Block:
    """
    Create the genesis (first) block.
    
    Genesis block has:
        - prev_hash = all zeros
        - No transactions (or just coinbase)
        - Predefined certificate (simulated consensus)
        - Timestamp = project start time
    """
    from ..constants import L4, Z_C, DEFAULT_OSCILLATOR_COUNT
    import numpy as np
    
    # Simulated consensus for genesis
    genesis_phases = np.linspace(0, 0.1, DEFAULT_OSCILLATOR_COUNT).tolist()
    genesis_r = 0.95  # High coherence
    genesis_psi = 0.05
    
    certificate = ConsensusCertificate(
        bloom_start=0,
        bloom_end=L4,
        r_values=[genesis_r] * L4,
        psi_values=[genesis_psi] * L4,
        final_phases=genesis_phases,
        oscillator_count=DEFAULT_OSCILLATOR_COUNT
    )
    
    header = BlockHeader(
        version=1,
        prev_hash=b'\x00' * 32,
        merkle_root=b'\x00' * 32,
        timestamp=1700000000,  # Fixed genesis time
        difficulty=1,
        nonce=7,  # L₄
        order_parameter=genesis_r,
        mean_phase=genesis_psi,
        oscillator_count=DEFAULT_OSCILLATOR_COUNT
    )
    
    return Block(header=header, certificate=certificate, transactions=[])
```

---

## Phase 2: Chain Implementation

### File: `chain.py`

**Objective**: Blockchain with validation and storage.

### Implementation Steps

#### Step 2.1: Chain State

```python
from dataclasses import dataclass, field
from typing import Optional, Iterator
import threading

@dataclass
class ChainState:
    """
    Current state of the blockchain.
    
    Attributes:
        height: Current chain height
        tip_hash: Hash of the tip block
        total_work: Cumulative difficulty
        utxo_set: Unspent transaction outputs
    """
    height: int = 0
    tip_hash: bytes = b'\x00' * 32
    total_work: float = 0.0
    utxo_set: dict = field(default_factory=dict)
```

#### Step 2.2: Blockchain Class

```python
class Blockchain:
    """
    BloomCoin blockchain.
    
    Stores blocks and maintains chain state.
    Thread-safe for concurrent access.
    """
    
    def __init__(self, storage_path: str = None):
        """
        Initialize blockchain.
        
        Args:
            storage_path: Path for persistent storage (None = memory only)
        """
        self._blocks: dict[bytes, Block] = {}  # hash -> block
        self._height_index: dict[int, bytes] = {}  # height -> hash
        self._state = ChainState()
        self._lock = threading.RLock()
        self._storage_path = storage_path
        
        # Initialize with genesis
        genesis = create_genesis_block()
        self._add_block_internal(genesis, height=0)
    
    @property
    def height(self) -> int:
        return self._state.height
    
    @property
    def tip(self) -> Block:
        return self._blocks[self._state.tip_hash]
    
    def get_block(self, block_hash: bytes) -> Optional[Block]:
        """Get block by hash."""
        return self._blocks.get(block_hash)
    
    def get_block_at_height(self, height: int) -> Optional[Block]:
        """Get block at specific height."""
        block_hash = self._height_index.get(height)
        if block_hash:
            return self._blocks.get(block_hash)
        return None
    
    def add_block(self, block: Block) -> tuple[bool, str]:
        """
        Add a new block to the chain.
        
        Validates block and updates chain state.
        
        Returns:
            (success, error_message)
        """
        with self._lock:
            # Validate block
            valid, msg = block.validate()
            if not valid:
                return False, msg
            
            # Check prev_hash points to current tip
            if block.header.prev_hash != self._state.tip_hash:
                # Could be fork - handle separately
                return self._handle_fork(block)
            
            # Validate transactions against UTXO set
            valid, msg = self._validate_transactions(block)
            if not valid:
                return False, msg
            
            # Add block
            new_height = self._state.height + 1
            self._add_block_internal(block, new_height)
            
            # Update UTXO set
            self._update_utxo(block)
            
            return True, ""
    
    def _add_block_internal(self, block: Block, height: int):
        """Internal block addition (no validation)."""
        block.height = height
        self._blocks[block.hash] = block
        self._height_index[height] = block.hash
        self._state.height = height
        self._state.tip_hash = block.hash
        self._state.total_work += block.header.difficulty
    
    def _handle_fork(self, block: Block) -> tuple[bool, str]:
        """
        Handle potential chain fork.
        
        If new chain has more work, reorganize.
        """
        # Find common ancestor
        # Compare total work
        # Reorganize if necessary
        # YOUR IMPLEMENTATION HERE
        pass
    
    def _validate_transactions(self, block: Block) -> tuple[bool, str]:
        """Validate all transactions against current UTXO set."""
        # YOUR IMPLEMENTATION HERE
        pass
    
    def _update_utxo(self, block: Block):
        """Update UTXO set with block transactions."""
        # YOUR IMPLEMENTATION HERE
        pass
    
    def get_recent_block_times(self, count: int) -> list[float]:
        """Get timestamps of recent blocks for difficulty adjustment."""
        times = []
        current = self.tip
        
        for _ in range(count):
            if current.height == 0:
                break
            prev = self.get_block(current.header.prev_hash)
            if prev:
                times.append(current.header.timestamp - prev.header.timestamp)
                current = prev
            else:
                break
        
        return times
    
    def iterate_blocks(self, start: int = 0) -> Iterator[Block]:
        """Iterate over blocks from start height."""
        for height in range(start, self._state.height + 1):
            block = self.get_block_at_height(height)
            if block:
                yield block
```

---

## Phase 3: Transaction Implementation

### File: `transaction.py`

**Objective**: Transaction structure with signing and validation.

### Implementation Steps

#### Step 3.1: Transaction Input/Output

```python
@dataclass
class TxInput:
    """
    Transaction input (spending a previous output).
    
    Attributes:
        prev_tx: Hash of transaction being spent
        output_index: Index of output in that transaction
        signature: Signature proving ownership
    """
    prev_tx: bytes  # 32 bytes
    output_index: int
    signature: bytes  # 64 bytes (Ed25519)
    
    def serialize(self) -> bytes:
        return struct.pack('<32s I 64s', self.prev_tx, self.output_index, self.signature)
    
    @classmethod
    def deserialize(cls, data: bytes) -> 'TxInput':
        fields = struct.unpack('<32s I 64s', data[:100])
        return cls(prev_tx=fields[0], output_index=fields[1], signature=fields[2])

@dataclass
class TxOutput:
    """
    Transaction output (creating new value).
    
    Attributes:
        amount: Value in smallest units (1 BLOOM = 10^8 units)
        address: Recipient address (32 bytes)
    """
    amount: int
    address: bytes  # 32 bytes
    
    def serialize(self) -> bytes:
        return struct.pack('<Q 32s', self.amount, self.address)
    
    @classmethod
    def deserialize(cls, data: bytes) -> 'TxOutput':
        fields = struct.unpack('<Q 32s', data[:40])
        return cls(amount=fields[0], address=fields[1])
```

#### Step 3.2: Transaction

```python
@dataclass
class Transaction:
    """
    BloomCoin transaction.
    
    Attributes:
        version: Transaction version
        inputs: List of inputs being spent
        outputs: List of new outputs
        locktime: Earliest block height for inclusion
    """
    version: int
    inputs: list[TxInput]
    outputs: list[TxOutput]
    locktime: int = 0
    
    _hash: bytes = None
    
    @property
    def hash(self) -> bytes:
        """Transaction hash (txid)."""
        if self._hash is None:
            self._hash = hashlib.sha256(hashlib.sha256(
                self.serialize_for_signing()
            ).digest()).digest()
        return self._hash
    
    def serialize_for_signing(self) -> bytes:
        """Serialize transaction for signing (excludes signatures)."""
        data = struct.pack('<I', self.version)
        data += struct.pack('<I', len(self.inputs))
        for inp in self.inputs:
            data += struct.pack('<32s I', inp.prev_tx, inp.output_index)
        data += struct.pack('<I', len(self.outputs))
        for out in self.outputs:
            data += out.serialize()
        data += struct.pack('<I', self.locktime)
        return data
    
    def serialize(self) -> bytes:
        """Full serialization including signatures."""
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
    def deserialize_with_length(cls, data: bytes) -> tuple['Transaction', int]:
        """Deserialize and return bytes consumed."""
        # YOUR IMPLEMENTATION HERE
        pass
    
    def validate(self) -> tuple[bool, str]:
        """
        Validate transaction.
        
        Checks:
        1. At least one input and output
        2. Output amounts are positive
        3. Sum of outputs <= sum of inputs (difference is fee)
        4. All signatures are valid
        """
        # YOUR IMPLEMENTATION HERE
        pass
    
    @property
    def fee(self) -> int:
        """Transaction fee (inputs - outputs)."""
        # Requires UTXO lookup to determine input values
        # YOUR IMPLEMENTATION HERE
        pass
```

#### Step 3.3: Coinbase Transaction

```python
def create_coinbase(
    height: int,
    reward_address: bytes,
    fees: int = 0
) -> Transaction:
    """
    Create coinbase (block reward) transaction.
    
    Args:
        height: Block height (encoded in input)
        reward_address: Address to receive reward
        fees: Total transaction fees from block
    
    Returns:
        Coinbase transaction
    """
    from ..constants import INITIAL_REWARD, HALVING_INTERVAL
    
    # Calculate reward with halving
    halvings = height // HALVING_INTERVAL
    reward = INITIAL_REWARD >> halvings  # Divide by 2^halvings
    
    total = reward + fees
    
    # Coinbase input (no prev_tx)
    cb_input = TxInput(
        prev_tx=b'\x00' * 32,
        output_index=height,  # Encode height
        signature=b'\x00' * 64
    )
    
    # Output to miner
    cb_output = TxOutput(amount=total, address=reward_address)
    
    return Transaction(
        version=1,
        inputs=[cb_input],
        outputs=[cb_output],
        locktime=0
    )
```

---

## Module Integration

### Full Block Validation

```python
def validate_block_full(block: Block, chain: Blockchain) -> tuple[bool, str]:
    """
    Complete block validation including chain context.
    
    Checks:
    1. Block structure valid
    2. Consensus certificate valid
    3. Previous block exists
    4. Timestamp reasonable
    5. Difficulty matches expected
    6. All transactions valid
    7. Coinbase amount correct
    """
    # Structural validation
    valid, msg = block.validate()
    if not valid:
        return False, msg
    
    # Check previous block
    prev = chain.get_block(block.header.prev_hash)
    if prev is None:
        return False, "Previous block not found"
    
    # Check timestamp (not too far in future)
    import time
    if block.header.timestamp > time.time() + 7200:  # 2 hours
        return False, "Block timestamp too far in future"
    
    # Check difficulty
    expected_diff = chain.get_expected_difficulty(prev.height + 1)
    if abs(block.header.difficulty - expected_diff) > expected_diff * 0.01:
        return False, "Difficulty mismatch"
    
    # Check coinbase
    if block.transactions:
        coinbase = block.transactions[0]
        expected_reward = calculate_reward(prev.height + 1)
        fees = sum(tx.fee for tx in block.transactions[1:])
        if coinbase.outputs[0].amount > expected_reward + fees:
            return False, "Coinbase reward too high"
    
    return True, ""
```

---

## Validation Checklist

- [ ] Genesis block has correct structure
- [ ] Block serialization round-trips correctly
- [ ] Block hash is deterministic
- [ ] Chain tip updates correctly on new blocks
- [ ] Fork handling selects higher-work chain
- [ ] Transaction signatures verify
- [ ] UTXO set updates correctly
- [ ] Coinbase reward calculates with halving
- [ ] Merkle root validates transactions

---

## Next Module

After completing `blockchain/`, proceed to `network/` for P2P communication.

---

*Blocks are containers for coherence.* 🌸
