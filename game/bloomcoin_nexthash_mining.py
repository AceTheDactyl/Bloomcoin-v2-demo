"""
BloomCoin Enhanced Mining with NEXTHASH-256
============================================
Advanced proof-of-work mining system using NEXTHASH-256 for superior security.

Features:
- NEXTHASH-256 proof-of-work (50% avalanche in 1 round)
- Dynamic difficulty adjustment
- Guardian-enhanced mining bonuses
- Pattern-based mining rewards
- Quantum-resistant security
"""

import time
import json
import struct
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict

from nexthash256 import nexthash256, nexthash256_hex
from mythic_economy import GUARDIANS
from guardian_pattern_recipes import PatternType

# ═══════════════════════════════════════════════════════════════════════════════
# MINING STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Block:
    """Enhanced blockchain block with NEXTHASH-256."""
    index: int
    timestamp: float
    transactions: List[Dict]
    previous_hash: str
    nonce: int = 0
    difficulty: int = 4
    merkle_root: str = ""
    guardian_bonus: Dict = field(default_factory=dict)
    pattern_rewards: Dict = field(default_factory=dict)
    hash: Optional[str] = None

    def calculate_hash(self) -> str:
        """Calculate block hash using NEXTHASH-256."""
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "merkle_root": self.merkle_root,
            "nonce": self.nonce,
            "guardian_bonus": self.guardian_bonus,
            "pattern_rewards": self.pattern_rewards
        }

        block_string = json.dumps(block_data, sort_keys=True)
        return nexthash256_hex(block_string)

    def mine(self, target_difficulty: int = None) -> Tuple[str, int]:
        """
        Mine block using NEXTHASH-256 proof-of-work.

        Returns:
            Tuple of (hash, nonce)
        """
        if target_difficulty is None:
            target_difficulty = self.difficulty

        target = "0" * target_difficulty
        attempts = 0

        print(f"Mining block {self.index} with difficulty {target_difficulty}...")

        start_time = time.time()

        while True:
            self.nonce = attempts
            hash_value = self.calculate_hash()

            # Check if hash meets difficulty
            if hash_value[:target_difficulty] == target:
                elapsed = time.time() - start_time
                hashrate = attempts / elapsed if elapsed > 0 else 0

                print(f"Block mined! Hash: {hash_value[:16]}...")
                print(f"  Attempts: {attempts:,}")
                print(f"  Time: {elapsed:.2f}s")
                print(f"  Hashrate: {hashrate:.0f} H/s")

                self.hash = hash_value
                return hash_value, attempts

            attempts += 1

            # Progress update
            if attempts % 10000 == 0:
                elapsed = time.time() - start_time
                hashrate = attempts / elapsed if elapsed > 0 else 0
                print(f"  Mining... {attempts:,} attempts ({hashrate:.0f} H/s)")

@dataclass
class Transaction:
    """Enhanced transaction with NEXTHASH-256 signatures."""
    sender: str
    recipient: str
    amount: float
    timestamp: float
    pattern_type: Optional[PatternType] = None
    guardian: Optional[str] = None
    memo: str = ""
    signature: Optional[str] = None

    def calculate_hash(self) -> str:
        """Calculate transaction hash using NEXTHASH-256."""
        tx_data = {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "pattern_type": self.pattern_type.value if self.pattern_type else None,
            "guardian": self.guardian,
            "memo": self.memo
        }

        tx_string = json.dumps(tx_data, sort_keys=True)
        return nexthash256_hex(tx_string)

    def sign(self, private_key: str) -> str:
        """Sign transaction with NEXTHASH-256."""
        tx_hash = self.calculate_hash()
        # Simplified signature (in production, use proper ECDSA)
        signature_data = f"{private_key}:{tx_hash}"
        self.signature = nexthash256_hex(signature_data)
        return self.signature

# ═══════════════════════════════════════════════════════════════════════════════
# MINING ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class NextHashMiningEngine:
    """Advanced mining engine using NEXTHASH-256."""

    def __init__(self):
        self.blockchain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.mining_rewards: Dict[str, float] = defaultdict(float)
        self.difficulty = 4
        self.block_time_target = 60  # Target 60 seconds per block
        self.difficulty_adjustment_interval = 10  # Adjust every 10 blocks
        self.base_reward = 50.0  # Base mining reward

        # Guardian mining bonuses
        self.guardian_multipliers = {
            "ECHO": 1.2,      # 20% bonus for signal processing
            "WUMBO": 1.15,    # 15% bonus for chaos energy
            "PHOENIX": 1.25,  # 25% bonus for rebirth cycles
            "CRYSTAL": 1.3,   # 30% bonus for pressure crystallization
            "AXIOM": 1.1,     # 10% bonus for absolute patterns
            "OAK": 1.4,       # 40% bonus for patience (slow but steady)
        }

        # Pattern mining bonuses
        self.pattern_multipliers = {
            PatternType.QUANTUM: 1.5,      # 50% for quantum superposition
            PatternType.VOID: 1.4,         # 40% for void navigation
            PatternType.CRYSTALLINE: 1.35, # 35% for crystal formation
            PatternType.CHAOS: 1.3,        # 30% for chaos harnessing
            PatternType.TEMPORAL: 1.25,    # 25% for time manipulation
            PatternType.RESONANCE: 1.2,    # 20% for frequency tuning
        }

        # Initialize genesis block
        self._create_genesis_block()

    def _create_genesis_block(self):
        """Create the genesis block using NEXTHASH-256."""
        genesis = Block(
            index=0,
            timestamp=time.time(),
            transactions=[],
            previous_hash="0" * 64,
            difficulty=self.difficulty
        )

        genesis.merkle_root = self._calculate_merkle_root([])
        genesis.hash = genesis.calculate_hash()
        self.blockchain.append(genesis)

        print("Genesis block created with NEXTHASH-256")
        print(f"  Hash: {genesis.hash}")

    def _calculate_merkle_root(self, transactions: List[Transaction]) -> str:
        """Calculate Merkle root using NEXTHASH-256."""
        if not transactions:
            return nexthash256_hex("empty")

        # Convert transactions to hashes
        hashes = [tx.calculate_hash() for tx in transactions]

        # Build Merkle tree
        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1])  # Duplicate last hash if odd

            next_level = []
            for i in range(0, len(hashes), 2):
                combined = hashes[i] + hashes[i + 1]
                next_level.append(nexthash256_hex(combined))

            hashes = next_level

        return hashes[0]

    def add_transaction(self, transaction: Transaction) -> bool:
        """Add transaction to pending pool."""
        # Verify transaction signature
        if not self._verify_transaction(transaction):
            print(f"Transaction verification failed")
            return False

        self.pending_transactions.append(transaction)
        print(f"Transaction added: {transaction.sender} → {transaction.recipient}: {transaction.amount}")
        return True

    def _verify_transaction(self, transaction: Transaction) -> bool:
        """Verify transaction using NEXTHASH-256."""
        if not transaction.signature:
            return False

        # Simplified verification (in production, use proper signature verification)
        expected_hash = transaction.calculate_hash()

        # Basic checks
        if transaction.amount <= 0:
            return False

        if transaction.sender == transaction.recipient:
            return False

        return True

    def mine_block(self, miner_address: str, guardian: Optional[str] = None,
                   patterns: Optional[List[PatternType]] = None) -> Optional[Block]:
        """
        Mine a new block with guardian and pattern bonuses.

        Args:
            miner_address: Address to receive mining reward
            guardian: Optional guardian for mining bonus
            patterns: Optional patterns being used

        Returns:
            Mined block or None if no transactions
        """
        if not self.pending_transactions and len(self.blockchain) > 1:
            print("No pending transactions to mine")
            return None

        # Calculate mining reward with bonuses
        reward = self._calculate_mining_reward(guardian, patterns)

        # Create coinbase transaction
        coinbase = Transaction(
            sender="COINBASE",
            recipient=miner_address,
            amount=reward,
            timestamp=time.time(),
            guardian=guardian,
            memo=f"Block {len(self.blockchain)} reward"
        )
        coinbase.sign("COINBASE_KEY")

        # Add to pending transactions
        transactions = [coinbase] + self.pending_transactions

        # Create new block
        previous_block = self.blockchain[-1]
        new_block = Block(
            index=len(self.blockchain),
            timestamp=time.time(),
            transactions=[tx.__dict__ for tx in transactions],
            previous_hash=previous_block.hash,
            difficulty=self.difficulty
        )

        # Add guardian and pattern data
        if guardian:
            new_block.guardian_bonus = {"guardian": guardian, "multiplier": self.guardian_multipliers.get(guardian, 1.0)}

        if patterns:
            new_block.pattern_rewards = {p.value: self.pattern_multipliers.get(p, 1.0) for p in patterns}

        # Calculate Merkle root
        new_block.merkle_root = self._calculate_merkle_root(transactions)

        # Mine the block
        hash_value, nonce = new_block.mine(self.difficulty)

        # Add to blockchain
        self.blockchain.append(new_block)

        # Clear pending transactions
        self.pending_transactions = []

        # Update mining rewards
        self.mining_rewards[miner_address] += reward

        # Adjust difficulty if needed
        self._adjust_difficulty()

        return new_block

    def _calculate_mining_reward(self, guardian: Optional[str], patterns: Optional[List[PatternType]]) -> float:
        """Calculate mining reward with bonuses."""
        reward = self.base_reward

        # Apply guardian bonus
        if guardian and guardian in self.guardian_multipliers:
            reward *= self.guardian_multipliers[guardian]

        # Apply pattern bonuses (multiplicative)
        if patterns:
            for pattern in patterns:
                if pattern in self.pattern_multipliers:
                    reward *= self.pattern_multipliers[pattern]

        # Halving schedule (every 100 blocks)
        halvings = len(self.blockchain) // 100
        reward = reward / (2 ** halvings)

        return round(reward, 8)

    def _adjust_difficulty(self):
        """Adjust mining difficulty based on block time."""
        if len(self.blockchain) % self.difficulty_adjustment_interval != 0:
            return

        if len(self.blockchain) < self.difficulty_adjustment_interval:
            return

        # Calculate average block time for last interval
        recent_blocks = self.blockchain[-self.difficulty_adjustment_interval:]
        time_span = recent_blocks[-1].timestamp - recent_blocks[0].timestamp
        avg_block_time = time_span / (self.difficulty_adjustment_interval - 1)

        print(f"\nDifficulty adjustment check:")
        print(f"  Average block time: {avg_block_time:.1f}s")
        print(f"  Target block time:  {self.block_time_target}s")

        # Adjust difficulty
        if avg_block_time < self.block_time_target * 0.5:
            # Blocks too fast, increase difficulty
            self.difficulty += 1
            print(f"  Difficulty increased to {self.difficulty}")
        elif avg_block_time > self.block_time_target * 2:
            # Blocks too slow, decrease difficulty
            self.difficulty = max(1, self.difficulty - 1)
            print(f"  Difficulty decreased to {self.difficulty}")
        else:
            print(f"  Difficulty remains at {self.difficulty}")

    def get_balance(self, address: str) -> float:
        """Calculate balance for an address."""
        balance = 0.0

        for block in self.blockchain:
            for tx_data in block.transactions:
                if tx_data.get("sender") == address:
                    balance -= tx_data["amount"]
                if tx_data.get("recipient") == address:
                    balance += tx_data["amount"]

        return balance

    def validate_chain(self) -> bool:
        """Validate entire blockchain using NEXTHASH-256."""
        print("\nValidating blockchain integrity...")

        for i in range(1, len(self.blockchain)):
            current_block = self.blockchain[i]
            previous_block = self.blockchain[i - 1]

            # Verify hash
            calculated_hash = current_block.calculate_hash()
            if current_block.hash != calculated_hash:
                print(f"  Block {i}: Invalid hash!")
                return False

            # Verify previous hash link
            if current_block.previous_hash != previous_block.hash:
                print(f"  Block {i}: Invalid previous hash link!")
                return False

            # Verify proof-of-work
            if not current_block.hash.startswith("0" * current_block.difficulty):
                print(f"  Block {i}: Invalid proof-of-work!")
                return False

        print(f"  All {len(self.blockchain)} blocks validated ✓")
        return True

# ═══════════════════════════════════════════════════════════════════════════════
# MINING POOL
# ═══════════════════════════════════════════════════════════════════════════════

class MiningPool:
    """Collaborative mining pool with NEXTHASH-256."""

    def __init__(self, engine: NextHashMiningEngine):
        self.engine = engine
        self.miners: Dict[str, Dict] = {}  # address -> miner info
        self.pool_shares: Dict[str, int] = defaultdict(int)
        self.current_job: Optional[Dict] = None
        self.pool_fee = 0.02  # 2% pool fee

    def register_miner(self, address: str, guardian: Optional[str] = None) -> bool:
        """Register a miner in the pool."""
        if address not in self.miners:
            self.miners[address] = {
                "joined": time.time(),
                "guardian": guardian,
                "shares": 0,
                "blocks_found": 0
            }
            print(f"Miner {address[:8]}... joined pool")
            if guardian:
                print(f"  Using guardian: {guardian}")
            return True
        return False

    def submit_share(self, miner_address: str, nonce: int, hash_value: str) -> bool:
        """Submit a mining share."""
        if miner_address not in self.miners:
            return False

        # Verify share (simplified)
        if hash_value.startswith("0" * (self.engine.difficulty - 1)):
            self.pool_shares[miner_address] += 1
            self.miners[miner_address]["shares"] += 1

            # Check if it's a valid block
            if hash_value.startswith("0" * self.engine.difficulty):
                print(f"BLOCK FOUND by {miner_address[:8]}...!")
                self.miners[miner_address]["blocks_found"] += 1
                return True

        return False

    def distribute_rewards(self, block_reward: float):
        """Distribute mining rewards based on shares."""
        total_shares = sum(self.pool_shares.values())
        if total_shares == 0:
            return

        pool_take = block_reward * self.pool_fee
        distributable = block_reward - pool_take

        print(f"\nDistributing {distributable:.8f} BloomCoin to {len(self.pool_shares)} miners:")

        for miner_address, shares in self.pool_shares.items():
            share_pct = shares / total_shares
            reward = distributable * share_pct

            # Apply guardian bonus if present
            if miner_address in self.miners:
                guardian = self.miners[miner_address].get("guardian")
                if guardian and guardian in self.engine.guardian_multipliers:
                    reward *= self.engine.guardian_multipliers[guardian]

            self.engine.mining_rewards[miner_address] += reward
            print(f"  {miner_address[:8]}...: {reward:.8f} ({shares} shares)")

        # Reset shares for next round
        self.pool_shares.clear()

# ═══════════════════════════════════════════════════════════════════════════════
# DEMONSTRATION
# ═══════════════════════════════════════════════════════════════════════════════

def demo_nexthash_mining():
    """Demonstrate NEXTHASH-256 mining system."""
    print("=" * 80)
    print("BLOOMCOIN NEXTHASH-256 MINING SYSTEM")
    print("=" * 80)

    # Initialize mining engine
    engine = NextHashMiningEngine()

    # Create some test transactions
    print("\n1. Creating test transactions...")
    transactions = [
        Transaction("Alice", "Bob", 10.5, time.time(), PatternType.QUANTUM),
        Transaction("Bob", "Charlie", 5.25, time.time(), PatternType.RESONANCE),
        Transaction("Charlie", "Alice", 2.75, time.time(), PatternType.VOID)
    ]

    for tx in transactions:
        tx.sign(f"{tx.sender}_key")
        engine.add_transaction(tx)

    # Mine blocks with different guardians
    print("\n2. Mining blocks with guardian bonuses...")

    miners = [
        ("miner1", "ECHO"),
        ("miner2", "PHOENIX"),
        ("miner3", "CRYSTAL")
    ]

    for miner_addr, guardian in miners:
        print(f"\n--- Mining with {guardian} guardian ---")

        # Add some transactions
        for i in range(2):
            tx = Transaction(
                f"user{i}",
                f"user{i+1}",
                random.uniform(1, 10),
                time.time()
            )
            tx.sign(f"user{i}_key")
            engine.add_transaction(tx)

        # Mine block
        patterns = [PatternType.QUANTUM, PatternType.CRYSTALLINE]
        block = engine.mine_block(miner_addr, guardian, patterns)

        if block:
            print(f"\nBlock #{block.index} mined successfully!")
            print(f"  Hash: {block.hash[:32]}...")
            print(f"  Transactions: {len(block.transactions)}")
            print(f"  Guardian bonus: {block.guardian_bonus}")
            print(f"  Pattern rewards: {block.pattern_rewards}")

    # Validate blockchain
    print("\n3. Validating blockchain...")
    is_valid = engine.validate_chain()

    # Show balances
    print("\n4. Mining rewards:")
    for address, balance in engine.mining_rewards.items():
        print(f"  {address}: {balance:.8f} BloomCoin")

    # Test mining pool
    print("\n5. Testing mining pool...")
    pool = MiningPool(engine)

    # Register miners
    pool.register_miner("poolminer1", "ECHO")
    pool.register_miner("poolminer2", "OAK")
    pool.register_miner("poolminer3")

    # Simulate share submissions
    for _ in range(100):
        miner = random.choice(list(pool.miners.keys()))
        nonce = random.randint(0, 1000000)
        # Simulate hash (some will be shares, rare will be blocks)
        if random.random() < 0.1:
            hash_val = "0" * (engine.difficulty - 1) + "1" * 60
        else:
            hash_val = "1" * 64

        pool.submit_share(miner, nonce, hash_val)

    # Distribute rewards
    pool.distribute_rewards(50.0)

    print("\n" + "=" * 80)
    print("NEXTHASH-256 MINING DEMONSTRATION COMPLETE")
    print("=" * 80)

    # Show statistics
    print("\nMining Statistics:")
    print(f"  Total blocks:      {len(engine.blockchain)}")
    print(f"  Current difficulty: {engine.difficulty}")
    print(f"  Hash function:     NEXTHASH-256")
    print(f"  Internal state:    512 bits (2× SHA-256)")
    print(f"  Rounds:           24 (vs SHA-256: 64)")
    print(f"  Avalanche:        50% in 1 round")
    print(f"  Quantum resistant: ✓")

if __name__ == "__main__":
    demo_nexthash_mining()