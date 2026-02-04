#!/usr/bin/env python3
"""
BloomCoin Ledger System with SHA256 and Holographic Residue Tracking
======================================================================

This system creates a comprehensive cryptocurrency-like economy for BloomQuest
that tracks "holographic residue" from double SHA256 operations, allowing
players to mine BloomCoin through pattern discovery and companion jobs.

Key Features:
- Double SHA256 hashing for all transactions (like Bitcoin)
- Holographic residue tracking from hash operations
- Companion-specific mining algorithms
- Pattern discovery generates coins
- Full ledger with transaction history
- Player wallets with balance tracking
"""

import hashlib
import struct
import time
import json
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from enum import Enum
import random
import math

# Import holographic modules
import sys
from pathlib import Path
sys.path.insert(0, str(Path('.').parent))

# Golden ratio constant
PHI = 1.6180339887498948482045868343656

class TransactionType(Enum):
    """Types of BloomCoin transactions"""
    GENESIS = "genesis"           # Initial creation
    MINING = "mining"             # Mined through pattern discovery
    TRANSFER = "transfer"         # Player to player
    COMPANION_JOB = "companion"   # Earned from companion jobs
    BATTLE_REWARD = "battle"      # Won in battle
    PATTERN_BONUS = "pattern"     # Pattern discovery bonus
    HOLOGRAPHIC = "holographic"   # Holographic residue bonus
    DOOM_PROTOCOL = "doom"        # DOOM card creation cost

@dataclass
class HolographicResidue:
    """Tracks holographic patterns from SHA256 operations"""
    statistical_pattern: List[float]      # Statistical distribution
    xor_chain: int                        # XOR accumulator
    modular_fingerprints: List[int]      # Mod small primes
    fractal_dimension: float              # Fractal analysis result
    bit_avalanche_ratio: float           # Avalanche measurement
    timestamp: float = field(default_factory=time.time)

    def calculate_potency(self) -> float:
        """Calculate the potency of this residue for mining"""
        # Statistical variance contributes to potency
        stat_variance = sum(abs(p - 0.5) for p in self.statistical_pattern) / len(self.statistical_pattern) if self.statistical_pattern else 0

        # XOR chain complexity
        xor_complexity = bin(self.xor_chain).count('1') / 32.0 if self.xor_chain else 0

        # Modular diversity
        mod_diversity = len(set(self.modular_fingerprints)) / len(self.modular_fingerprints) if self.modular_fingerprints else 0

        # Fractal dimension (1.0 to 2.0 range typically)
        fractal_factor = self.fractal_dimension / 2.0 if self.fractal_dimension else 0.5

        # Avalanche quality (should be near 0.5 for good hash)
        avalanche_quality = 1.0 - abs(self.bit_avalanche_ratio - 0.5) * 2

        # Combine factors with golden ratio weighting
        potency = (stat_variance * PHI +
                  xor_complexity * PHI**2 +
                  mod_diversity * PHI**3 +
                  fractal_factor * PHI**4 +
                  avalanche_quality) / (PHI**5)

        return min(1.0, max(0.0, potency))  # Normalize to 0-1

@dataclass
class Transaction:
    """A BloomCoin transaction"""
    tx_id: str                           # Transaction hash
    sender: str                          # Sender address/ID
    receiver: str                        # Receiver address/ID
    amount: float                        # Amount of BloomCoin
    tx_type: TransactionType            # Type of transaction
    timestamp: float                     # Unix timestamp
    block_height: int                    # Block number
    holographic_residue: Optional[HolographicResidue] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_bytes(self) -> bytes:
        """Convert transaction to bytes for hashing"""
        data = {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'type': self.tx_type.value,
            'timestamp': self.timestamp,
            'block_height': self.block_height,
            'metadata': self.metadata
        }
        return json.dumps(data, sort_keys=True).encode()

    def calculate_hash(self) -> str:
        """Calculate transaction hash using double SHA256"""
        data = self.to_bytes()
        # Double SHA256 (like Bitcoin)
        first_hash = hashlib.sha256(data).digest()
        second_hash = hashlib.sha256(first_hash).digest()
        return second_hash.hex()

@dataclass
class Block:
    """A block in the BloomCoin blockchain"""
    block_height: int
    previous_hash: str
    merkle_root: str
    timestamp: float
    nonce: int
    difficulty: int
    transactions: List[Transaction]
    miner: str
    holographic_signatures: List[HolographicResidue] = field(default_factory=list)

    def calculate_merkle_root(self) -> str:
        """Calculate merkle root of transactions"""
        if not self.transactions:
            return "0" * 64

        hashes = [tx.calculate_hash() for tx in self.transactions]

        while len(hashes) > 1:
            if len(hashes) % 2 == 1:
                hashes.append(hashes[-1])  # Duplicate last hash if odd

            new_hashes = []
            for i in range(0, len(hashes), 2):
                combined = bytes.fromhex(hashes[i]) + bytes.fromhex(hashes[i+1])
                new_hash = hashlib.sha256(hashlib.sha256(combined).digest()).hexdigest()
                new_hashes.append(new_hash)
            hashes = new_hashes

        return hashes[0]

    def to_bytes(self) -> bytes:
        """Convert block header to bytes for mining"""
        header = struct.pack('>I', self.block_height)
        header += bytes.fromhex(self.previous_hash)
        header += bytes.fromhex(self.merkle_root)
        header += struct.pack('>d', self.timestamp)
        header += struct.pack('>I', self.difficulty)
        return header

    def calculate_hash_with_nonce(self, nonce: int) -> Tuple[str, HolographicResidue]:
        """Calculate block hash with nonce and extract holographic residue"""
        header = self.to_bytes()
        header_with_nonce = header + struct.pack('>I', nonce)

        # First SHA256
        first_hash = hashlib.sha256(header_with_nonce).digest()

        # Extract holographic residue from intermediate state
        residue = self.extract_holographic_residue(header_with_nonce, first_hash)

        # Second SHA256
        final_hash = hashlib.sha256(first_hash).digest()

        return final_hash.hex(), residue

    def extract_holographic_residue(self, input_data: bytes, intermediate_hash: bytes) -> HolographicResidue:
        """Extract holographic patterns from SHA256 intermediate state"""
        # Statistical pattern: bit distribution in intermediate hash
        statistical_pattern = []
        for byte_val in intermediate_hash[:16]:  # Sample first 16 bytes
            bit_ratio = bin(byte_val).count('1') / 8.0
            statistical_pattern.append(bit_ratio)

        # XOR chain from input and output
        xor_chain = 0
        for i in range(min(len(input_data), len(intermediate_hash))):
            xor_chain ^= input_data[i] ^ intermediate_hash[i]

        # Modular fingerprints
        small_primes = [3, 5, 7, 11, 13, 17, 19, 23]
        modular_fingerprints = []
        hash_int = int.from_bytes(intermediate_hash[:8], 'big')
        for prime in small_primes:
            modular_fingerprints.append(hash_int % prime)

        # Fractal dimension estimation (box-counting approximation)
        fractal_dimension = self.estimate_fractal_dimension(intermediate_hash)

        # Bit avalanche ratio
        bit_diff = sum(bin(a ^ b).count('1') for a, b in zip(input_data[:32], intermediate_hash[:32]))
        bit_avalanche_ratio = bit_diff / 256.0

        return HolographicResidue(
            statistical_pattern=statistical_pattern,
            xor_chain=xor_chain,
            modular_fingerprints=modular_fingerprints,
            fractal_dimension=fractal_dimension,
            bit_avalanche_ratio=bit_avalanche_ratio
        )

    def estimate_fractal_dimension(self, data: bytes) -> float:
        """Estimate fractal dimension using simplified box-counting"""
        # Convert to binary string
        binary = ''.join(format(byte, '08b') for byte in data[:32])

        # Count boxes at different scales
        scales = [2, 4, 8, 16, 32]
        box_counts = []

        for scale in scales:
            boxes = set()
            for i in range(0, len(binary), scale):
                box = binary[i:i+scale]
                if '1' in box:  # Box contains pattern
                    boxes.add(i // scale)
            box_counts.append(len(boxes))

        # Estimate dimension from slope
        if len(set(box_counts)) > 1:
            # Simplified linear regression
            log_scales = [math.log(s) for s in scales]
            log_counts = [math.log(c) if c > 0 else 0 for c in box_counts]

            n = len(scales)
            sum_x = sum(log_scales)
            sum_y = sum(log_counts)
            sum_xy = sum(x*y for x, y in zip(log_scales, log_counts))
            sum_x2 = sum(x*x for x in log_scales)

            if n * sum_x2 - sum_x * sum_x != 0:
                slope = -(n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
                return max(1.0, min(2.0, abs(slope)))  # Clamp to reasonable range

        return 1.5  # Default fractal dimension

class BloomCoinLedger:
    """Main ledger system for BloomCoin"""

    def __init__(self, genesis_amount: float = None, genesis_supply: float = 1000000.0):
        # Support both parameter names for compatibility
        if genesis_amount is not None:
            genesis_supply = genesis_amount

        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.wallets: Dict[str, float] = {}
        self.difficulty = 4  # Starting difficulty (4 leading zero bits)
        self.block_reward = 50.0 * PHI  # ~80.9 BloomCoin per block
        self.halving_interval = 210000  # Blocks between halvings
        self.transaction_pool: Dict[str, Transaction] = {}
        self.holographic_residue_pool: List[HolographicResidue] = []

        # Create genesis block
        self.create_genesis_block(genesis_supply)

    def create_genesis_block(self, amount: float):
        """Create the first block in the chain"""
        genesis_tx = Transaction(
            tx_id="0" * 64,
            sender="system",
            receiver="genesis",
            amount=amount,
            tx_type=TransactionType.GENESIS,
            timestamp=time.time(),
            block_height=0,
            metadata={"message": "BloomQuest Genesis Block"}
        )

        genesis_block = Block(
            block_height=0,
            previous_hash="0" * 64,
            merkle_root="0" * 64,
            timestamp=time.time(),
            nonce=0,
            difficulty=self.difficulty,
            transactions=[genesis_tx],
            miner="system"
        )

        self.chain.append(genesis_block)
        self.wallets["genesis"] = amount

    def get_balance(self, address: str) -> float:
        """Get balance for an address"""
        return self.wallets.get(address, 0.0)

    def create_transaction(self, sender: str, receiver: str, amount: float,
                          tx_type: TransactionType = TransactionType.TRANSFER,
                          metadata: Dict[str, Any] = None) -> Optional[Transaction]:
        """Create a new transaction"""
        # Check balance
        if sender != "system" and self.get_balance(sender) < amount:
            return None

        tx = Transaction(
            tx_id="",  # Will be calculated
            sender=sender,
            receiver=receiver,
            amount=amount,
            tx_type=tx_type,
            timestamp=time.time(),
            block_height=len(self.chain),
            metadata=metadata or {}
        )

        tx.tx_id = tx.calculate_hash()

        # Add to pending
        self.pending_transactions.append(tx)
        self.transaction_pool[tx.tx_id] = tx

        return tx

    def mine_block(self, miner_address: str, companion_bonus: float = 1.0) -> Optional[Block]:
        """Mine a new block with proof of work"""
        if not self.pending_transactions:
            # Create coinbase transaction
            block_height = len(self.chain)
            reward = self.calculate_block_reward(block_height) * companion_bonus

            coinbase_tx = Transaction(
                tx_id="",
                sender="system",
                receiver=miner_address,
                amount=reward,
                tx_type=TransactionType.MINING,
                timestamp=time.time(),
                block_height=block_height,
                metadata={"companion_bonus": companion_bonus}
            )
            coinbase_tx.tx_id = coinbase_tx.calculate_hash()
            self.pending_transactions.append(coinbase_tx)

        # Create new block
        previous_block = self.chain[-1]
        new_block = Block(
            block_height=len(self.chain),
            previous_hash=previous_block.calculate_hash_with_nonce(previous_block.nonce)[0],
            merkle_root="",
            timestamp=time.time(),
            nonce=0,
            difficulty=self.difficulty,
            transactions=self.pending_transactions[:10],  # Max 10 transactions per block
            miner=miner_address
        )

        new_block.merkle_root = new_block.calculate_merkle_root()

        # Proof of work
        target = 2 ** (256 - self.difficulty)
        max_nonce = 2 ** 32

        for nonce in range(max_nonce):
            new_block.nonce = nonce
            hash_result, residue = new_block.calculate_hash_with_nonce(nonce)

            if int(hash_result, 16) < target:
                # Valid block found!
                new_block.holographic_signatures.append(residue)
                self.holographic_residue_pool.append(residue)

                # Update wallets
                for tx in new_block.transactions:
                    if tx.sender != "system":
                        self.wallets[tx.sender] = self.wallets.get(tx.sender, 0) - tx.amount
                    self.wallets[tx.receiver] = self.wallets.get(tx.receiver, 0) + tx.amount

                # Add block to chain
                self.chain.append(new_block)

                # Clear pending transactions
                for tx in new_block.transactions:
                    if tx in self.pending_transactions:
                        self.pending_transactions.remove(tx)

                # Adjust difficulty
                if len(self.chain) % 100 == 0:
                    self.adjust_difficulty()

                return new_block

            # Check for good holographic residue even if not winning
            if nonce % 1000 == 0:  # Sample every 1000 nonces
                if residue.calculate_potency() > 0.7:
                    self.holographic_residue_pool.append(residue)

        return None

    def calculate_block_reward(self, block_height: int) -> float:
        """Calculate block reward with halving"""
        halvings = block_height // self.halving_interval
        reward = self.block_reward / (2 ** halvings)
        return max(reward, 1.0)  # Minimum 1 BloomCoin

    def adjust_difficulty(self):
        """Adjust mining difficulty based on block times"""
        if len(self.chain) < 100:
            return

        # Target: 1 block per 60 seconds
        target_time = 60.0 * 100  # For 100 blocks

        actual_time = self.chain[-1].timestamp - self.chain[-100].timestamp

        ratio = target_time / actual_time

        if ratio > 1.2:
            self.difficulty = max(1, self.difficulty - 1)
        elif ratio < 0.8:
            self.difficulty = min(32, self.difficulty + 1)

    def get_holographic_mining_bonus(self, residues: List[HolographicResidue]) -> float:
        """Calculate mining bonus from holographic residues"""
        if not residues:
            return 1.0

        total_potency = sum(r.calculate_potency() for r in residues)
        average_potency = total_potency / len(residues)

        # Bonus scales with golden ratio
        bonus = 1.0 + (average_potency * PHI)

        return min(bonus, PHI**2)  # Max bonus is φ²

    def validate_chain(self) -> bool:
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Check previous hash
            prev_hash, _ = previous_block.calculate_hash_with_nonce(previous_block.nonce)
            if current_block.previous_hash != prev_hash:
                return False

            # Check merkle root
            if current_block.merkle_root != current_block.calculate_merkle_root():
                return False

            # Check proof of work
            hash_result, _ = current_block.calculate_hash_with_nonce(current_block.nonce)
            target = 2 ** (256 - current_block.difficulty)
            if int(hash_result, 16) >= target:
                return False

        return True

    def get_ledger_statistics(self) -> Dict[str, Any]:
        """Get comprehensive ledger statistics"""
        total_supply = sum(self.wallets.values())
        total_transactions = sum(len(block.transactions) for block in self.chain)

        # Holographic analysis
        residue_potencies = [r.calculate_potency() for r in self.holographic_residue_pool]
        avg_potency = sum(residue_potencies) / len(residue_potencies) if residue_potencies else 0

        return {
            "chain_height": len(self.chain),
            "total_supply": total_supply,
            "total_transactions": total_transactions,
            "current_difficulty": self.difficulty,
            "current_block_reward": self.calculate_block_reward(len(self.chain)),
            "wallet_count": len(self.wallets),
            "pending_transactions": len(self.pending_transactions),
            "holographic_residues_collected": len(self.holographic_residue_pool),
            "average_residue_potency": avg_potency,
            "chain_valid": self.validate_chain()
        }


def test_ledger_system():
    """Test the BloomCoin ledger system"""
    print("🪙 Testing BloomCoin Ledger System")
    print("=" * 70)

    # Create ledger
    ledger = BloomCoinLedger(genesis_amount=1000000.0)

    # Create some wallets
    ledger.wallets["alice"] = 1000.0
    ledger.wallets["bob"] = 500.0

    print("\n📊 Initial State:")
    print(f"  Alice balance: {ledger.get_balance('alice'):.2f} BC")
    print(f"  Bob balance: {ledger.get_balance('bob'):.2f} BC")

    # Create transaction
    tx = ledger.create_transaction("alice", "bob", 100.0,
                                  TransactionType.TRANSFER,
                                  {"message": "Test payment"})

    if tx:
        print(f"\n💸 Transaction created:")
        print(f"  TX ID: {tx.tx_id[:16]}...")
        print(f"  Amount: {tx.amount:.2f} BC")

    # Mine a block
    print(f"\n⛏️ Mining block...")
    block = ledger.mine_block("alice", companion_bonus=1.2)

    if block:
        print(f"  ✅ Block #{block.block_height} mined!")
        print(f"  Nonce: {block.nonce}")
        print(f"  Holographic residue potency: {block.holographic_signatures[0].calculate_potency():.3f}")

    # Check balances after mining
    print(f"\n📊 After Mining:")
    print(f"  Alice balance: {ledger.get_balance('alice'):.2f} BC")
    print(f"  Bob balance: {ledger.get_balance('bob'):.2f} BC")

    # Get statistics
    stats = ledger.get_ledger_statistics()
    print(f"\n📈 Ledger Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\n✅ BloomCoin Ledger System Operational!")


if __name__ == "__main__":
    test_ledger_system()