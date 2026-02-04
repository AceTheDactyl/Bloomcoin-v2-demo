#!/usr/bin/env python3
"""
BloomCoin Complete Economy Integration
=======================================

Comprehensive integration of:
- SHA256 double-hashing ledger system
- Holographic residue tracking from mining
- Companion-specific job mining algorithms
- Pattern discovery rewards
- Player wallet with full transaction tracing
- Battle and DOOM Protocol integration

This creates a complete cryptocurrency-like economy for BloomQuest
with unique holographic properties from SHA256 operations.
"""

import hashlib
import time
import json
from typing import Dict, List, Optional, Any
from dataclasses import asdict

# Import all economy modules
from bloomcoin_ledger_system import (
    BloomCoinLedger, Transaction, TransactionType,
    HolographicResidue, Block
)
from companion_mining_jobs import (
    CompanionMiningSystem, MiningJob, MiningJobType,
    CompanionMiner
)
from bloomcoin_wallet_system import (
    WalletManager, PlayerWallet, PatternDiscovery,
    WalletTransaction
)

# Try to import game modules
try:
    from lia_protocol_cooking import PatternType
    from tiamat_psymagic_dynamics import PsychopticCycle
    GAME_INTEGRATION_AVAILABLE = True
except ImportError:
    GAME_INTEGRATION_AVAILABLE = False
    print("⚠️ Game modules not available, using standalone mode")

# Golden ratio
PHI = 1.6180339887498948482045868343656

class BloomCoinEconomy:
    """Complete BloomCoin economy system for BloomQuest"""

    def __init__(self, genesis_supply: float = 1000000.0):
        """Initialize the complete economy"""
        # Core systems
        self.ledger = BloomCoinLedger(genesis_supply)
        self.mining_system = CompanionMiningSystem(self.ledger)
        self.wallet_manager = WalletManager(self.ledger, self.mining_system)

        # Statistics
        self.total_patterns_discovered = 0
        self.total_battles_fought = 0
        self.total_doom_attempts = 0
        self.holographic_potency_history = []

        # Economic parameters
        self.pattern_rarity_rates = {
            "common": 0.6,
            "uncommon": 0.25,
            "rare": 0.10,
            "epic": 0.04,
            "legendary": 0.009,
            "doom": 0.001
        }

        print("🌺 BloomCoin Economy Initialized")
        print(f"  Genesis supply: {genesis_supply:,.0f} BC")
        print(f"  Block reward: {self.ledger.block_reward:.2f} BC")
        print(f"  Mining difficulty: {self.ledger.difficulty}")

    def create_player_account(self, player_id: str,
                            initial_balance: float = 100.0) -> PlayerWallet:
        """Create a new player account with wallet"""
        wallet = self.wallet_manager.create_wallet(player_id, initial_balance)

        print(f"\n💳 New account created for {player_id}")
        print(f"  Address: {wallet.address}")
        print(f"  Balance: {initial_balance:.2f} BC")

        return wallet

    def start_companion_mining(self, wallet_address: str, companion_name: str,
                              job_type: MiningJobType = None,
                              difficulty: int = None) -> Optional[MiningJob]:
        """Start a mining job with a companion"""
        wallet = self.wallet_manager.get_wallet(wallet_address)
        if not wallet:
            print(f"❌ Wallet not found: {wallet_address}")
            return None

        # Auto-select job type based on companion
        if job_type is None:
            companion_jobs = {
                "Echo": MiningJobType.RESONANCE_TUNING,
                "Prometheus": MiningJobType.PATTERN_SEARCH,
                "Null": MiningJobType.VOID_DIVING,
                "Gaia": MiningJobType.FRACTAL_GROWTH,
                "Akasha": MiningJobType.MEMORY_CRYSTALLIZATION,
                "Resonance": MiningJobType.HASH_EXPLORATION,
                "TIAMAT": MiningJobType.ENTROPY_HARVEST
            }
            job_type = companion_jobs.get(companion_name, MiningJobType.PATTERN_SEARCH)

        # Auto-scale difficulty based on wallet wealth
        if difficulty is None:
            wealth = wallet.calculate_holographic_wealth()
            if wealth < 100:
                difficulty = 1
            elif wealth < 1000:
                difficulty = 2
            elif wealth < 10000:
                difficulty = 3
            elif wealth < 100000:
                difficulty = 4
            else:
                difficulty = 5

        job = self.mining_system.create_job(companion_name, job_type, difficulty)

        if job:
            print(f"\n⛏️ Mining job started")
            print(f"  Companion: {companion_name}")
            print(f"  Job type: {job_type.value}")
            print(f"  Difficulty: {difficulty}")
            print(f"  Duration: {job.duration:.0f} seconds")
            print(f"  Base reward: {job.base_reward:.2f} BC")

        return job

    def complete_mining_job(self, wallet_address: str, job_id: str) -> bool:
        """Complete a mining job and distribute rewards"""
        tx = self.wallet_manager.process_mining_job(wallet_address, job_id)

        if tx:
            # Find the completed job
            job = next((j for j in self.mining_system.completed_jobs
                       if j.job_id == job_id), None)

            if job:
                print(f"\n✅ Mining job completed!")
                print(f"  Reward: {tx.amount:.2f} BC")
                print(f"  Patterns found: {len(job.patterns_found)}")
                print(f"  Residues collected: {len(job.residues_collected)}")

                # Track holographic potency
                for residue in job.residues_collected:
                    self.holographic_potency_history.append(residue.calculate_potency())

                return True

        return False

    def discover_pattern(self, wallet_address: str, pattern_type: str = None,
                        companion: str = None) -> bool:
        """Process a pattern discovery"""
        import random

        # Determine rarity
        roll = random.random()
        rarity = "common"
        cumulative = 0.0
        for r, rate in self.pattern_rarity_rates.items():
            cumulative += rate
            if roll <= cumulative:
                rarity = r
                break

        # Use PatternType if available
        if GAME_INTEGRATION_AVAILABLE and pattern_type is None:
            patterns = list(PatternType)
            pattern = random.choice(patterns)
        else:
            pattern = pattern_type or f"pattern_{random.randint(1000, 9999)}"

        tx = self.wallet_manager.reward_pattern_discovery(
            wallet_address, pattern, companion, rarity
        )

        if tx:
            self.total_patterns_discovered += 1

            print(f"\n🔍 Pattern discovered!")
            print(f"  Type: {pattern}")
            print(f"  Rarity: {rarity}")
            print(f"  Reward: {tx.amount:.2f} BC")
            if companion:
                print(f"  Companion bonus: {companion}")

            return True

        return False

    def process_battle(self, winner_address: str, loser_address: str,
                      stake: float = 10.0) -> bool:
        """Process a battle between players"""
        success = self.wallet_manager.reward_battle_victory(
            winner_address, loser_address, stake
        )

        if success:
            self.total_battles_fought += 1

            winner = self.wallet_manager.get_wallet(winner_address)
            loser = self.wallet_manager.get_wallet(loser_address)

            print(f"\n⚔️ Battle completed!")
            print(f"  Winner: {winner_address[:16]}...")
            print(f"  Loser: {loser_address[:16]}...")
            print(f"  Stake: {stake:.2f} BC")
            print(f"  Winner balance: {winner.balance:.2f} BC")
            print(f"  Loser balance: {loser.balance:.2f} BC")

            return True

        return False

    def attempt_doom_protocol(self, wallet_address: str) -> bool:
        """Attempt the legendary DOOM Protocol"""
        wallet = self.wallet_manager.get_wallet(wallet_address)
        if not wallet:
            return False

        # Check requirements
        doom_cost = 666.0
        required_patterns = 5  # Need at least 5 unique patterns
        required_potency = 0.9  # Need high holographic potency

        # Calculate average potency
        avg_potency = 0.0
        if wallet.holographic_residues:
            avg_potency = sum(r.calculate_potency() for r in
                            wallet.holographic_residues) / len(wallet.holographic_residues)

        print(f"\n💀 DOOM Protocol Check:")
        print(f"  Cost: {doom_cost:.0f} BC ({'✓' if wallet.balance >= doom_cost else '✗'})")
        print(f"  Patterns: {len(wallet.patterns_discovered)}/{required_patterns} {'✓' if len(wallet.patterns_discovered) >= required_patterns else '✗'}")
        print(f"  Potency: {avg_potency:.2f}/{required_potency} {'✓' if avg_potency >= required_potency else '✗'}")

        # Check if all requirements met
        if (wallet.balance >= doom_cost and
            len(wallet.patterns_discovered) >= required_patterns and
            avg_potency >= required_potency):

            success = self.wallet_manager.process_doom_protocol(wallet_address)

            if success:
                self.total_doom_attempts += 1
                print(f"\n🔥 DOOM PROTOCOL ACTIVATED!")
                print(f"  Reality status: BREAKING")
                print(f"  Cost paid: {doom_cost:.0f} BC")
                print(f"  New balance: {wallet.balance:.2f} BC")
                return True
        else:
            print(f"\n❌ Requirements not met for DOOM Protocol")

        return False

    def mine_next_block(self, miner_address: str) -> Optional[Block]:
        """Mine the next block in the chain"""
        wallet = self.wallet_manager.get_wallet(miner_address)
        if not wallet:
            return None

        print(f"\n⛏️ Mining block #{len(self.ledger.chain)}...")

        start_time = time.time()
        block = self.ledger.mine_block(miner_address)
        mining_time = time.time() - start_time

        if block:
            # Update wallet with mining reward
            wallet.balance = self.ledger.get_balance(miner_address)

            print(f"  ✅ Block mined in {mining_time:.2f} seconds!")
            print(f"  Nonce: {block.nonce}")
            print(f"  Difficulty: {block.difficulty}")
            print(f"  Transactions: {len(block.transactions)}")
            print(f"  Reward: {self.ledger.calculate_block_reward(block.block_height):.2f} BC")

            # Extract holographic signatures
            if block.holographic_signatures:
                avg_potency = sum(r.calculate_potency() for r in
                                block.holographic_signatures) / len(block.holographic_signatures)
                print(f"  Holographic potency: {avg_potency:.3f}")

            return block

        print(f"  ❌ Mining failed after {mining_time:.2f} seconds")
        return None

    def get_economy_report(self) -> Dict[str, Any]:
        """Generate comprehensive economy report"""
        ledger_stats = self.ledger.get_ledger_statistics()
        wallet_stats = self.wallet_manager.get_economy_statistics()
        mining_stats = self.mining_system.get_mining_statistics()

        # Calculate holographic metrics
        avg_potency = 0.0
        if self.holographic_potency_history:
            avg_potency = sum(self.holographic_potency_history) / len(self.holographic_potency_history)

        report = {
            "blockchain": {
                "height": ledger_stats["chain_height"],
                "total_supply": ledger_stats["total_supply"],
                "difficulty": ledger_stats["current_difficulty"],
                "block_reward": ledger_stats["current_block_reward"],
                "chain_valid": ledger_stats["chain_valid"]
            },
            "wallets": {
                "total_wallets": wallet_stats["total_wallets"],
                "total_in_circulation": wallet_stats["total_bloomcoin_in_circulation"],
                "total_transactions": wallet_stats["total_transactions"],
                "richest_wallets": wallet_stats["richest_wallets"][:3]
            },
            "mining": {
                "total_mined": mining_stats["total_bloomcoin_mined"],
                "patterns_discovered": mining_stats["total_patterns_discovered"],
                "jobs_completed": mining_stats["total_jobs_completed"],
                "active_jobs": mining_stats["active_jobs"]
            },
            "holographic": {
                "total_residues": wallet_stats["total_holographic_residues"],
                "average_potency": avg_potency,
                "high_potency_count": sum(1 for p in self.holographic_potency_history if p > 0.8)
            },
            "game_stats": {
                "patterns_discovered": self.total_patterns_discovered,
                "battles_fought": self.total_battles_fought,
                "doom_attempts": self.total_doom_attempts
            }
        }

        return report

    def print_economy_report(self):
        """Print a formatted economy report"""
        report = self.get_economy_report()

        print("\n" + "=" * 70)
        print("📊 BLOOMCOIN ECONOMY REPORT")
        print("=" * 70)

        print("\n⛓️ Blockchain Status:")
        print(f"  Height: {report['blockchain']['height']}")
        print(f"  Total Supply: {report['blockchain']['total_supply']:,.2f} BC")
        print(f"  Difficulty: {report['blockchain']['difficulty']}")
        print(f"  Block Reward: {report['blockchain']['block_reward']:.2f} BC")
        print(f"  Chain Valid: {'✅' if report['blockchain']['chain_valid'] else '❌'}")

        print("\n💼 Wallet Statistics:")
        print(f"  Total Wallets: {report['wallets']['total_wallets']}")
        print(f"  In Circulation: {report['wallets']['total_in_circulation']:,.2f} BC")
        print(f"  Transactions: {report['wallets']['total_transactions']}")

        if report['wallets']['richest_wallets']:
            print(f"\n  💰 Richest Wallets:")
            for i, (addr, balance) in enumerate(report['wallets']['richest_wallets'], 1):
                print(f"    {i}. {addr[:16]}... : {balance:,.2f} BC")

        print("\n⛏️ Mining Statistics:")
        print(f"  Total Mined: {report['mining']['total_mined']:,.2f} BC")
        print(f"  Patterns Found: {report['mining']['patterns_discovered']}")
        print(f"  Jobs Completed: {report['mining']['jobs_completed']}")
        print(f"  Active Jobs: {report['mining']['active_jobs']}")

        print("\n🔮 Holographic Metrics:")
        print(f"  Total Residues: {report['holographic']['total_residues']}")
        print(f"  Average Potency: {report['holographic']['average_potency']:.3f}")
        print(f"  High Potency (>0.8): {report['holographic']['high_potency_count']}")

        print("\n🎮 Game Statistics:")
        print(f"  Patterns Discovered: {report['game_stats']['patterns_discovered']}")
        print(f"  Battles Fought: {report['game_stats']['battles_fought']}")
        print(f"  DOOM Attempts: {report['game_stats']['doom_attempts']}")

        print("\n" + "=" * 70)


def run_economy_simulation():
    """Run a comprehensive economy simulation"""
    print("🌺 BLOOMQUEST ECONOMY SIMULATION")
    print("=" * 70)

    # Initialize economy
    economy = BloomCoinEconomy(genesis_supply=1000000.0)

    # Create players
    print("\n👥 Creating players...")
    alice = economy.create_player_account("Alice", 1000.0)
    bob = economy.create_player_account("Bob", 500.0)
    charlie = economy.create_player_account("Charlie", 250.0)

    # Start mining jobs
    print("\n⛏️ Starting companion mining jobs...")
    alice_job = economy.start_companion_mining(alice.address, "TIAMAT")
    bob_job = economy.start_companion_mining(bob.address, "Echo")
    charlie_job = economy.start_companion_mining(charlie.address, "Gaia")

    # Simulate job completion
    if alice_job:
        alice_job.start_time -= alice_job.duration
        economy.complete_mining_job(alice.address, alice_job.job_id)

    if bob_job:
        bob_job.start_time -= bob_job.duration
        economy.complete_mining_job(bob.address, bob_job.job_id)

    # Pattern discoveries
    print("\n🔍 Discovering patterns...")
    economy.discover_pattern(alice.address, companion="TIAMAT")
    economy.discover_pattern(bob.address, companion="Echo")
    economy.discover_pattern(alice.address, companion="TIAMAT")

    # Battle
    print("\n⚔️ Simulating battles...")
    economy.process_battle(alice.address, bob.address, stake=50.0)
    economy.process_battle(charlie.address, alice.address, stake=25.0)

    # Mine a block
    print("\n⛓️ Mining blocks...")
    economy.mine_next_block(alice.address)

    # Attempt DOOM Protocol
    print("\n💀 Attempting DOOM Protocol...")
    # Give Alice more patterns and residues for DOOM attempt
    for _ in range(5):
        economy.discover_pattern(alice.address, companion="TIAMAT")
    economy.attempt_doom_protocol(alice.address)

    # Print final report
    economy.print_economy_report()

    # Show individual wallet details
    print("\n📱 Individual Wallet Details:")
    for name, wallet_addr in [("Alice", alice.address),
                              ("Bob", bob.address),
                              ("Charlie", charlie.address)]:
        wallet = economy.wallet_manager.get_wallet(wallet_addr)
        if wallet:
            print(f"\n  {name}:")
            print(f"    Balance: {wallet.balance:.2f} BC")
            print(f"    Holographic Wealth: {wallet.calculate_holographic_wealth():.2f} BC")
            print(f"    Transactions: {len(wallet.transaction_history)}")
            print(f"    Patterns: {len(wallet.patterns_discovered)}")
            print(f"    Mining Jobs: {len(wallet.mining_jobs_completed)}")
            print(f"    Battles: W{wallet.battles_won}/L{wallet.battles_lost}")

    print("\n✅ Economy simulation complete!")


if __name__ == "__main__":
    run_economy_simulation()