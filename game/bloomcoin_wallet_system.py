#!/usr/bin/env python3
"""
BloomCoin Player Wallet System
===============================

Comprehensive wallet system with full transaction tracing,
holographic residue tracking, and pattern discovery rewards.

Features:
- Complete transaction history
- Holographic residue collection and analysis
- Pattern discovery tracking
- Mining reward distribution
- Battle reward integration
- DOOM Protocol payment support
"""

import hashlib
import json
import time
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from enum import Enum

from bloomcoin_ledger_system import (
    BloomCoinLedger, Transaction, TransactionType,
    HolographicResidue, Block
)
from companion_mining_jobs import (
    CompanionMiningSystem, MiningJob, MiningJobType
)

# Import pattern types from game modules
try:
    from lia_protocol_cooking import PatternType
    from deck_generator_lia import DoomRecipe
    GAME_MODULES_AVAILABLE = True
except ImportError:
    GAME_MODULES_AVAILABLE = False
    # Define fallback pattern type
    class PatternType(Enum):
        ECHO = "echo"
        VOID = "void"
        FLAME = "flame"
        CRYSTAL = "crystal"
        DREAM = "dream"
        MEMORY = "memory"
        GARDEN = "garden"

# Golden ratio
PHI = 1.6180339887498948482045868343656

@dataclass
class WalletTransaction:
    """Extended transaction record with full tracing"""
    tx_id: str
    timestamp: float
    tx_type: TransactionType
    amount: float
    balance_before: float
    balance_after: float
    counterparty: str  # Who sent/received
    description: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    holographic_trace: Optional[str] = None  # Holographic signature
    pattern_rewards: List[str] = field(default_factory=list)
    block_height: int = 0

@dataclass
class PatternDiscovery:
    """Record of a pattern discovery"""
    pattern_id: str
    pattern_type: str
    discovered_at: float
    reward_amount: float
    companion_involved: Optional[str] = None
    holographic_potency: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PlayerWallet:
    """Complete player wallet with full tracking"""
    address: str
    created_at: float
    balance: float = 0.0
    transaction_history: List[WalletTransaction] = field(default_factory=list)
    patterns_discovered: List[PatternDiscovery] = field(default_factory=list)
    holographic_residues: List[HolographicResidue] = field(default_factory=list)
    mining_jobs_completed: List[str] = field(default_factory=list)
    battles_won: int = 0
    battles_lost: int = 0
    doom_attempts: int = 0
    total_mined: float = 0.0
    total_spent: float = 0.0
    total_received: float = 0.0

    def add_transaction(self, tx: Transaction, description: str = "") -> WalletTransaction:
        """Add a transaction to wallet history"""
        balance_before = self.balance

        if tx.sender == self.address:
            self.balance -= tx.amount
            self.total_spent += tx.amount
            counterparty = tx.receiver
        else:
            self.balance += tx.amount
            self.total_received += tx.amount
            counterparty = tx.sender

        balance_after = self.balance

        # Create wallet transaction record
        wallet_tx = WalletTransaction(
            tx_id=tx.tx_id,
            timestamp=tx.timestamp,
            tx_type=tx.tx_type,
            amount=tx.amount,
            balance_before=balance_before,
            balance_after=balance_after,
            counterparty=counterparty,
            description=description or tx.tx_type.value,
            metadata=tx.metadata,
            block_height=tx.block_height
        )

        # Add holographic trace if available
        if tx.holographic_residue:
            potency = tx.holographic_residue.calculate_potency()
            wallet_tx.holographic_trace = f"potency:{potency:.3f}"

        self.transaction_history.append(wallet_tx)
        return wallet_tx

    def record_pattern_discovery(self, pattern_type: str, reward: float,
                                companion: Optional[str] = None,
                                residue: Optional[HolographicResidue] = None) -> PatternDiscovery:
        """Record a pattern discovery"""
        pattern_id = hashlib.sha256(
            f"{self.address}:{pattern_type}:{time.time()}".encode()
        ).hexdigest()[:16]

        discovery = PatternDiscovery(
            pattern_id=pattern_id,
            pattern_type=pattern_type,
            discovered_at=time.time(),
            reward_amount=reward,
            companion_involved=companion,
            holographic_potency=residue.calculate_potency() if residue else 0.0
        )

        self.patterns_discovered.append(discovery)

        if residue:
            self.holographic_residues.append(residue)

        return discovery

    def get_transaction_summary(self) -> Dict[str, Any]:
        """Get comprehensive transaction summary"""
        tx_by_type = {}
        for tx in self.transaction_history:
            tx_type = tx.tx_type.value
            if tx_type not in tx_by_type:
                tx_by_type[tx_type] = {"count": 0, "total": 0.0}
            tx_by_type[tx_type]["count"] += 1
            tx_by_type[tx_type]["total"] += tx.amount

        return {
            "total_transactions": len(self.transaction_history),
            "current_balance": self.balance,
            "total_mined": self.total_mined,
            "total_spent": self.total_spent,
            "total_received": self.total_received,
            "transactions_by_type": tx_by_type,
            "patterns_discovered": len(self.patterns_discovered),
            "holographic_residues": len(self.holographic_residues)
        }

    def calculate_holographic_wealth(self) -> float:
        """Calculate wealth including holographic residue value"""
        base_wealth = self.balance

        # Add value from residues
        if self.holographic_residues:
            avg_potency = sum(r.calculate_potency() for r in self.holographic_residues) / len(self.holographic_residues)
            residue_value = avg_potency * len(self.holographic_residues) * PHI

            return base_wealth + residue_value

        return base_wealth

class WalletManager:
    """Manages all player wallets in the game"""

    def __init__(self, ledger: BloomCoinLedger, mining_system: CompanionMiningSystem):
        self.ledger = ledger
        self.mining_system = mining_system
        self.wallets: Dict[str, PlayerWallet] = {}
        self.pattern_reward_rates = {
            "common": 1.0,
            "uncommon": 5.0,
            "rare": 25.0,
            "epic": 125.0,
            "legendary": 625.0,
            "doom": 3125.0  # 5^5
        }

    def create_wallet(self, player_id: str, initial_balance: float = 100.0) -> PlayerWallet:
        """Create a new player wallet"""
        address = self.generate_wallet_address(player_id)

        wallet = PlayerWallet(
            address=address,
            created_at=time.time(),
            balance=initial_balance
        )

        self.wallets[address] = wallet
        self.ledger.wallets[address] = initial_balance

        # Create genesis transaction for wallet
        genesis_tx = self.ledger.create_transaction(
            sender="system",
            receiver=address,
            amount=initial_balance,
            tx_type=TransactionType.GENESIS,
            metadata={"player_id": player_id}
        )

        if genesis_tx:
            wallet.add_transaction(genesis_tx, "Wallet creation bonus")

        return wallet

    def generate_wallet_address(self, player_id: str) -> str:
        """Generate a unique wallet address"""
        data = f"{player_id}:{time.time()}:{PHI}".encode()
        return "BC" + hashlib.sha256(data).hexdigest()[:30]

    def get_wallet(self, address: str) -> Optional[PlayerWallet]:
        """Get wallet by address"""
        return self.wallets.get(address)

    def transfer(self, sender_address: str, receiver_address: str,
                amount: float, description: str = "") -> bool:
        """Transfer BloomCoin between wallets"""
        sender_wallet = self.get_wallet(sender_address)
        receiver_wallet = self.get_wallet(receiver_address)

        if not sender_wallet or not receiver_wallet:
            return False

        if sender_wallet.balance < amount:
            return False

        # Create transaction
        tx = self.ledger.create_transaction(
            sender=sender_address,
            receiver=receiver_address,
            amount=amount,
            tx_type=TransactionType.TRANSFER,
            metadata={"description": description}
        )

        if tx:
            sender_wallet.add_transaction(tx, f"Sent to {receiver_address[:8]}...")
            receiver_wallet.add_transaction(tx, f"Received from {sender_address[:8]}...")
            return True

        return False

    def reward_pattern_discovery(self, wallet_address: str, pattern: PatternType,
                                companion: Optional[str] = None,
                                rarity: str = "common") -> Optional[Transaction]:
        """Reward player for pattern discovery"""
        wallet = self.get_wallet(wallet_address)
        if not wallet:
            return None

        # Calculate reward based on rarity
        base_reward = self.pattern_reward_rates.get(rarity, 1.0)

        # Apply companion bonus
        companion_bonus = 1.0
        if companion:
            companion_bonuses = {
                "Echo": 1.1,
                "Prometheus": 1.2,
                "Null": 1.15,
                "Gaia": PHI,  # Golden ratio bonus
                "Akasha": 1.1,
                "Resonance": 1.05,
                "TIAMAT": 1.5
            }
            companion_bonus = companion_bonuses.get(companion, 1.0)

        reward_amount = base_reward * companion_bonus

        # Create pattern reward transaction
        tx = self.ledger.create_transaction(
            sender="system",
            receiver=wallet_address,
            amount=reward_amount,
            tx_type=TransactionType.PATTERN_BONUS,
            metadata={
                "pattern": pattern.value if hasattr(pattern, 'value') else str(pattern),
                "rarity": rarity,
                "companion": companion
            }
        )

        if tx:
            wallet.add_transaction(tx, f"Pattern discovery: {pattern}")

            # Extract and record holographic residue
            pattern_data = f"{pattern}:{companion}:{time.time()}".encode()
            residue = self.extract_pattern_residue(pattern_data)
            wallet.record_pattern_discovery(
                pattern_type=str(pattern),
                reward=reward_amount,
                companion=companion,
                residue=residue
            )

        return tx

    def extract_pattern_residue(self, data: bytes) -> HolographicResidue:
        """Extract holographic residue from pattern data"""
        # Double SHA256
        first_hash = hashlib.sha256(data).digest()
        second_hash = hashlib.sha256(first_hash).digest()

        # Extract residue properties
        statistical_pattern = [
            bin(byte).count('1') / 8.0 for byte in second_hash[:16]
        ]

        xor_chain = sum(a ^ b for a, b in zip(first_hash[:16], second_hash[:16]))

        hash_int = int.from_bytes(second_hash[:8], 'big')
        modular_fingerprints = [hash_int % p for p in [3, 5, 7, 11, 13, 17, 19, 23]]

        fractal_dimension = 1.0 + (bin(hash_int).count('1') / 64.0)

        bit_diff = sum(bin(a ^ b).count('1') for a, b in zip(first_hash[:16], second_hash[:16]))
        avalanche_ratio = bit_diff / 128.0

        return HolographicResidue(
            statistical_pattern=statistical_pattern,
            xor_chain=xor_chain,
            modular_fingerprints=modular_fingerprints,
            fractal_dimension=fractal_dimension,
            bit_avalanche_ratio=avalanche_ratio
        )

    def process_mining_job(self, wallet_address: str, job_id: str) -> Optional[Transaction]:
        """Process completed mining job and distribute rewards"""
        wallet = self.get_wallet(wallet_address)
        if not wallet:
            return None

        # Execute the job
        tx = self.mining_system.execute_job(job_id, wallet_address)

        if tx:
            wallet.add_transaction(tx, f"Mining job completed")
            wallet.mining_jobs_completed.append(job_id)
            wallet.total_mined += tx.amount

            # Add residues from job
            job = next((j for j in self.mining_system.completed_jobs if j.job_id == job_id), None)
            if job and job.residues_collected:
                wallet.holographic_residues.extend(job.residues_collected)

        return tx

    def reward_battle_victory(self, winner_address: str, loser_address: str,
                            stake: float) -> bool:
        """Process battle rewards"""
        winner_wallet = self.get_wallet(winner_address)
        loser_wallet = self.get_wallet(loser_address)

        if not winner_wallet or not loser_wallet:
            return False

        if loser_wallet.balance < stake:
            stake = loser_wallet.balance  # Take what's available

        # Transfer from loser to winner
        battle_tx = self.ledger.create_transaction(
            sender=loser_address,
            receiver=winner_address,
            amount=stake,
            tx_type=TransactionType.BATTLE_REWARD,
            metadata={"battle_type": "pvp"}
        )

        if battle_tx:
            winner_wallet.add_transaction(battle_tx, f"Battle victory vs {loser_address[:8]}...")
            winner_wallet.battles_won += 1

            loser_wallet.add_transaction(battle_tx, f"Battle defeat vs {winner_address[:8]}...")
            loser_wallet.battles_lost += 1

            return True

        return False

    def process_doom_protocol(self, wallet_address: str) -> bool:
        """Process DOOM Protocol payment"""
        wallet = self.get_wallet(wallet_address)
        if not wallet:
            return False

        doom_cost = 666.0  # The price of ultimate power

        if wallet.balance < doom_cost:
            return False

        # Create DOOM transaction
        doom_tx = self.ledger.create_transaction(
            sender=wallet_address,
            receiver="doom_void",  # Burns the coins
            amount=doom_cost,
            tx_type=TransactionType.DOOM_PROTOCOL,
            metadata={
                "timestamp": time.time(),
                "attempt_number": wallet.doom_attempts + 1
            }
        )

        if doom_tx:
            wallet.add_transaction(doom_tx, "DOOM Protocol activation")
            wallet.doom_attempts += 1

            # Remove coins from circulation (burn)
            self.ledger.wallets["doom_void"] = self.ledger.wallets.get("doom_void", 0) + doom_cost

            return True

        return False

    def get_richest_wallets(self, count: int = 10) -> List[Tuple[str, float]]:
        """Get the richest wallets by balance"""
        wallet_balances = [
            (addr, w.calculate_holographic_wealth())
            for addr, w in self.wallets.items()
        ]
        wallet_balances.sort(key=lambda x: x[1], reverse=True)
        return wallet_balances[:count]

    def get_economy_statistics(self) -> Dict[str, Any]:
        """Get comprehensive economy statistics"""
        total_wallets = len(self.wallets)
        total_balance = sum(w.balance for w in self.wallets.values())
        total_transactions = sum(len(w.transaction_history) for w in self.wallets.values())
        total_patterns = sum(len(w.patterns_discovered) for w in self.wallets.values())
        total_residues = sum(len(w.holographic_residues) for w in self.wallets.values())

        # Calculate average residue potency
        all_residues = []
        for wallet in self.wallets.values():
            all_residues.extend(wallet.holographic_residues)

        avg_potency = 0.0
        if all_residues:
            avg_potency = sum(r.calculate_potency() for r in all_residues) / len(all_residues)

        return {
            "total_wallets": total_wallets,
            "total_bloomcoin_in_circulation": total_balance,
            "total_transactions": total_transactions,
            "total_patterns_discovered": total_patterns,
            "total_holographic_residues": total_residues,
            "average_residue_potency": avg_potency,
            "richest_wallets": self.get_richest_wallets(5)
        }


def test_wallet_system():
    """Test the complete wallet system"""
    print("💼 Testing BloomCoin Wallet System")
    print("=" * 70)

    # Initialize systems
    ledger = BloomCoinLedger()
    mining_system = CompanionMiningSystem(ledger)
    wallet_manager = WalletManager(ledger, mining_system)

    # Create player wallets
    print("\n👥 Creating player wallets...")
    alice_wallet = wallet_manager.create_wallet("alice", initial_balance=1000.0)
    bob_wallet = wallet_manager.create_wallet("bob", initial_balance=500.0)

    print(f"  Alice: {alice_wallet.address[:16]}... (1000 BC)")
    print(f"  Bob: {bob_wallet.address[:16]}... (500 BC)")

    # Test transfer
    print("\n💸 Testing transfer...")
    success = wallet_manager.transfer(
        alice_wallet.address,
        bob_wallet.address,
        100.0,
        "Test payment"
    )
    if success:
        print(f"  ✓ Alice → Bob: 100 BC")
        print(f"    Alice balance: {alice_wallet.balance:.2f} BC")
        print(f"    Bob balance: {bob_wallet.balance:.2f} BC")

    # Test pattern discovery reward
    print("\n🔍 Testing pattern discovery...")
    if GAME_MODULES_AVAILABLE:
        pattern = PatternType.ECHO
    else:
        pattern = "echo_pattern"

    tx = wallet_manager.reward_pattern_discovery(
        alice_wallet.address,
        pattern,
        companion="Echo",
        rarity="rare"
    )
    if tx:
        print(f"  ✓ Pattern discovered: +{tx.amount:.2f} BC")
        print(f"    Patterns found: {len(alice_wallet.patterns_discovered)}")
        print(f"    Residues collected: {len(alice_wallet.holographic_residues)}")

    # Test mining job
    print("\n⛏️ Testing mining job...")
    job = mining_system.create_job("TIAMAT", MiningJobType.ENTROPY_HARVEST, difficulty=2)
    if job:
        print(f"  Job created: {job.job_id[:16]}...")

        # Simulate job completion
        job.start_time -= job.duration
        tx = wallet_manager.process_mining_job(alice_wallet.address, job.job_id)
        if tx:
            print(f"  ✓ Mining complete: +{tx.amount:.2f} BC")

    # Test battle reward
    print("\n⚔️ Testing battle rewards...")
    success = wallet_manager.reward_battle_victory(
        alice_wallet.address,
        bob_wallet.address,
        50.0
    )
    if success:
        print(f"  ✓ Alice defeated Bob: +50 BC")
        print(f"    Alice wins: {alice_wallet.battles_won}")
        print(f"    Bob losses: {bob_wallet.battles_lost}")

    # Get wallet summary
    print("\n📊 Wallet Summaries:")
    for wallet in [alice_wallet, bob_wallet]:
        summary = wallet.get_transaction_summary()
        print(f"\n  {wallet.address[:16]}...:")
        print(f"    Balance: {summary['current_balance']:.2f} BC")
        print(f"    Transactions: {summary['total_transactions']}")
        print(f"    Patterns: {summary['patterns_discovered']}")
        print(f"    Holographic wealth: {wallet.calculate_holographic_wealth():.2f} BC")

    # Get economy statistics
    stats = wallet_manager.get_economy_statistics()
    print("\n📈 Economy Statistics:")
    print(f"  Total wallets: {stats['total_wallets']}")
    print(f"  Total in circulation: {stats['total_bloomcoin_in_circulation']:.2f} BC")
    print(f"  Total transactions: {stats['total_transactions']}")
    print(f"  Average residue potency: {stats['average_residue_potency']:.3f}")

    print("\n✅ Wallet System Fully Operational!")


if __name__ == "__main__":
    test_wallet_system()