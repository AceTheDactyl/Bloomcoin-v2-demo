#!/usr/bin/env python3
"""
Blockchain Integration Module for BloomQuest
============================================
Integrates the game with the BloomCoin blockchain for:
- Persistent game state storage
- Secure transactions
- Achievement verification
- Multiplayer coordination
- Anti-cheat mechanisms
"""

import hashlib
import json
import time
import pickle
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
import numpy as np

# Import bloomcoin blockchain components
import sys
sys.path.append(str(Path(__file__).parent.parent / "bloomcoin-v0.1.0" / "bloomcoin"))

from bloomcoin.blockchain import Blockchain, Block
from bloomcoin.transaction import Transaction
from bloomcoin.wallet.wallet import Wallet
from bloomcoin.constants import PHI, Z_C
from bloomcoin.consensus import ProofOfCoherence
from garden.crystal_ledger.ledger import CrystalLedger
from garden.crystal_ledger.block import MemoryBlock
from garden.bloom_events.bloom_event import BloomEvent, BloomEventType

@dataclass
class GameTransaction:
    """Represents a game-specific transaction on the blockchain"""
    transaction_id: str
    player_id: str
    transaction_type: str  # "trade", "reward", "purchase", "achievement"
    amount: float
    item_data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    coherence_score: float = 0.5
    verified: bool = False

    def to_blockchain_transaction(self, wallet: Wallet) -> Transaction:
        """Convert to blockchain transaction format"""
        # Include game data in transaction metadata
        tx_data = {
            "type": self.transaction_type,
            "player": self.player_id,
            "items": self.item_data,
            "coherence": self.coherence_score,
            "game_metadata": self.metadata
        }

        # Create transaction
        transaction = Transaction(
            sender=wallet.address,
            receiver=self.metadata.get("receiver", "game_treasury"),
            amount=self.amount,
            data=json.dumps(tx_data)
        )

        # Sign transaction
        transaction.sign(wallet.private_key)

        return transaction

@dataclass
class GameState:
    """Complete game state for a player"""
    player_id: str
    character_data: Dict[str, Any]
    inventory: Dict[str, int]
    achievements: List[str]
    quest_progress: Dict[str, float]
    location: str
    coherence: float
    play_time: float
    last_save: float = field(default_factory=time.time)
    version: str = "1.0.0"

    def calculate_hash(self) -> str:
        """Calculate hash of game state for verification"""
        state_str = json.dumps(asdict(self), sort_keys=True)
        return hashlib.sha256(state_str.encode()).hexdigest()

@dataclass
class Achievement:
    """Blockchain-verified achievement"""
    achievement_id: str
    name: str
    description: str
    criteria: Dict[str, Any]
    reward_amount: float
    reward_items: Dict[str, int]
    rarity: str  # "common", "rare", "epic", "legendary"
    blockchain_verified: bool = False
    verification_hash: Optional[str] = None

class GameBlockchain:
    """Main blockchain interface for the game"""

    def __init__(self, node_url: Optional[str] = None):
        self.blockchain = Blockchain()
        self.crystal_ledger = CrystalLedger()
        self.consensus = ProofOfCoherence()
        self.node_url = node_url

        # Game-specific storage
        self.game_states: Dict[str, GameState] = {}
        self.pending_transactions: List[GameTransaction] = []
        self.achievement_registry: Dict[str, Achievement] = {}
        self.player_wallets: Dict[str, Wallet] = {}

        # Initialize achievement registry
        self._initialize_achievements()

    def _initialize_achievements(self):
        """Initialize the achievement system"""
        achievements = [
            Achievement(
                "first_coherence",
                "First Coherence",
                "Achieve coherence above 0.618 for the first time",
                {"coherence_min": 1/PHI},
                PHI * 10,
                {"coherence_shard": 1},
                "common"
            ),
            Achievement(
                "perfect_coherence",
                "Perfect Coherence",
                "Achieve perfect coherence (1.0)",
                {"coherence_min": 1.0},
                PHI * 100,
                {"void_anchor": 1, "coherence_shard": 3},
                "legendary"
            ),
            Achievement(
                "void_conqueror",
                "Void Conqueror",
                "Defeat the void guardian",
                {"boss_defeated": "void_guardian"},
                PHI * 50,
                {"void_fragment": 5},
                "epic"
            ),
            Achievement(
                "merchant_prince",
                "Merchant Prince",
                "Accumulate 1000 BloomCoins",
                {"coins_min": 1000},
                PHI * 25,
                {"golden_ledger": 1},
                "rare"
            ),
            Achievement(
                "oscillator_master",
                "Oscillator Master",
                "Complete 10 oscillator challenges perfectly",
                {"oscillator_perfects": 10},
                PHI * 30,
                {"resonance_tuner": 2},
                "rare"
            )
        ]

        for achievement in achievements:
            self.achievement_registry[achievement.achievement_id] = achievement

    def create_player_wallet(self, player_id: str) -> Wallet:
        """Create or retrieve a player's blockchain wallet"""
        if player_id not in self.player_wallets:
            wallet = Wallet()
            wallet.generate_keys()
            self.player_wallets[player_id] = wallet

            # Give initial coins
            initial_coins = PHI * 10
            self._mint_coins(wallet.address, initial_coins)

        return self.player_wallets[player_id]

    def _mint_coins(self, address: str, amount: float):
        """Mint new coins (for game rewards)"""
        # Create a coinbase transaction
        mint_tx = Transaction(
            sender="COINBASE",
            receiver=address,
            amount=amount,
            data=json.dumps({"type": "mint", "reason": "game_reward"})
        )

        # Add to blockchain
        self.blockchain.add_transaction(mint_tx)

    def save_game_state(self, player_id: str, state: GameState) -> str:
        """Save game state to blockchain"""
        # Calculate state hash
        state_hash = state.calculate_hash()

        # Create memory block for Crystal Ledger
        memory_data = {
            "player_id": player_id,
            "state_hash": state_hash,
            "save_time": time.time(),
            "coherence": state.coherence,
            "location": state.location
        }

        memory_block = MemoryBlock(
            memory_type="game_save",
            content=json.dumps(asdict(state)),
            metadata=memory_data,
            significance=state.coherence  # Use coherence as significance
        )

        # Add to Crystal Ledger
        self.crystal_ledger.add_memory(memory_block)

        # Store locally
        self.game_states[player_id] = state

        # Create blockchain transaction for save event
        save_tx = GameTransaction(
            transaction_id=state_hash[:16],
            player_id=player_id,
            transaction_type="save_game",
            amount=0,  # No coin transfer for saves
            metadata={
                "state_hash": state_hash,
                "coherence": state.coherence,
                "play_time": state.play_time
            },
            coherence_score=state.coherence
        )

        self._process_transaction(save_tx)

        return state_hash

    def load_game_state(self, player_id: str) -> Optional[GameState]:
        """Load game state from blockchain"""
        # First check local cache
        if player_id in self.game_states:
            return self.game_states[player_id]

        # Search Crystal Ledger for latest save
        saves = []
        for block in self.crystal_ledger.chain:
            if block.memory_type == "game_save":
                memory_data = json.loads(block.content)
                if memory_data.get("player_id") == player_id:
                    saves.append((block.timestamp, memory_data))

        if not saves:
            return None

        # Get most recent save
        saves.sort(key=lambda x: x[0], reverse=True)
        latest_save = saves[0][1]

        # Reconstruct GameState
        state = GameState(**latest_save)

        # Verify integrity
        if state.calculate_hash() != block.metadata.get("state_hash"):
            print("Warning: Save state integrity check failed!")
            return None

        self.game_states[player_id] = state
        return state

    def process_game_transaction(self, transaction: GameTransaction) -> bool:
        """Process a game transaction through the blockchain"""
        # Verify transaction coherence
        if not self._verify_coherence(transaction):
            return False

        # Add to pending
        self.pending_transactions.append(transaction)

        # Process if enough pending
        if len(self.pending_transactions) >= 5:
            self._batch_process_transactions()

        return True

    def _verify_coherence(self, transaction: GameTransaction) -> bool:
        """Verify transaction coherence using Kuramoto oscillators"""
        # Check if coherence score meets threshold
        if transaction.coherence_score < Z_C * 0.5:
            return False

        # Additional verification based on transaction type
        if transaction.transaction_type == "trade":
            # Verify both parties have sufficient items/coins
            return self._verify_trade(transaction)
        elif transaction.transaction_type == "achievement":
            # Verify achievement criteria met
            return self._verify_achievement(transaction)

        return True

    def _verify_trade(self, transaction: GameTransaction) -> bool:
        """Verify a trade transaction"""
        player_id = transaction.player_id
        receiver_id = transaction.metadata.get("receiver_id")

        if not receiver_id:
            return False

        # Check both players exist
        if player_id not in self.game_states or receiver_id not in self.game_states:
            return False

        player_state = self.game_states[player_id]
        receiver_state = self.game_states[receiver_id]

        # Verify sender has items/coins
        if transaction.amount > 0:
            wallet = self.player_wallets.get(player_id)
            if not wallet or wallet.balance < transaction.amount:
                return False

        # Verify items
        for item, count in transaction.item_data.items():
            if player_state.inventory.get(item, 0) < count:
                return False

        return True

    def _verify_achievement(self, transaction: GameTransaction) -> bool:
        """Verify an achievement transaction"""
        achievement_id = transaction.metadata.get("achievement_id")
        if achievement_id not in self.achievement_registry:
            return False

        achievement = self.achievement_registry[achievement_id]
        player_state = self.game_states.get(transaction.player_id)

        if not player_state:
            return False

        # Check if already earned
        if achievement_id in player_state.achievements:
            return False

        # Verify criteria
        for criterion, value in achievement.criteria.items():
            if criterion == "coherence_min":
                if player_state.coherence < value:
                    return False
            elif criterion == "coins_min":
                wallet = self.player_wallets.get(transaction.player_id)
                if not wallet or wallet.balance < value:
                    return False
            # Add more criteria checks as needed

        return True

    def _batch_process_transactions(self):
        """Process pending transactions as a batch"""
        if not self.pending_transactions:
            return

        # Convert to blockchain transactions
        blockchain_txs = []
        for game_tx in self.pending_transactions:
            player_wallet = self.player_wallets.get(game_tx.player_id)
            if player_wallet:
                blockchain_tx = game_tx.to_blockchain_transaction(player_wallet)
                blockchain_txs.append(blockchain_tx)

        # Mine new block
        if blockchain_txs:
            new_block = self.blockchain.mine_block(blockchain_txs)

            # Clear pending
            self.pending_transactions.clear()

            # Trigger events
            self._on_block_mined(new_block)

    def _on_block_mined(self, block: Block):
        """Handle newly mined block"""
        # Create bloom event
        event = BloomEvent(
            type=BloomEventType.CONSENSUS,
            description=f"Block {block.index} mined",
            participants=list(self.player_wallets.keys()),
            significance=PHI
        )

        # Distribute mining rewards
        self._distribute_mining_rewards(block)

    def _distribute_mining_rewards(self, block: Block):
        """Distribute mining rewards to participants"""
        # Reward based on coherence participation
        total_coherence = sum(tx.coherence_score
                            for tx in self.pending_transactions
                            if hasattr(tx, 'coherence_score'))

        if total_coherence > 0:
            for tx in self.pending_transactions:
                if hasattr(tx, 'coherence_score') and tx.coherence_score > 0:
                    # Reward proportional to coherence contribution
                    reward = (tx.coherence_score / total_coherence) * PHI * 5
                    player_wallet = self.player_wallets.get(tx.player_id)
                    if player_wallet:
                        self._mint_coins(player_wallet.address, reward)

    def award_achievement(self, player_id: str, achievement_id: str) -> bool:
        """Award an achievement to a player"""
        if achievement_id not in self.achievement_registry:
            return False

        achievement = self.achievement_registry[achievement_id]
        player_state = self.game_states.get(player_id)

        if not player_state:
            return False

        # Check if already has achievement
        if achievement_id in player_state.achievements:
            return False

        # Verify criteria met
        if not self._verify_achievement_criteria(player_state, achievement):
            return False

        # Add achievement
        player_state.achievements.append(achievement_id)

        # Create achievement transaction
        achievement_tx = GameTransaction(
            transaction_id=hashlib.md5(
                f"{player_id}_{achievement_id}_{time.time()}".encode()
            ).hexdigest()[:16],
            player_id=player_id,
            transaction_type="achievement",
            amount=achievement.reward_amount,
            item_data=achievement.reward_items,
            metadata={
                "achievement_id": achievement_id,
                "achievement_name": achievement.name,
                "rarity": achievement.rarity
            },
            coherence_score=player_state.coherence
        )

        # Process transaction
        self.process_game_transaction(achievement_tx)

        # Award coins
        player_wallet = self.player_wallets.get(player_id)
        if player_wallet:
            self._mint_coins(player_wallet.address, achievement.reward_amount)

        # Award items
        for item, count in achievement.reward_items.items():
            player_state.inventory[item] = player_state.inventory.get(item, 0) + count

        # Mark as blockchain verified
        achievement.blockchain_verified = True
        achievement.verification_hash = achievement_tx.transaction_id

        return True

    def _verify_achievement_criteria(self, player_state: GameState,
                                    achievement: Achievement) -> bool:
        """Verify if player meets achievement criteria"""
        for criterion, value in achievement.criteria.items():
            if criterion == "coherence_min":
                if player_state.coherence < value:
                    return False
            elif criterion == "coins_min":
                wallet = self.player_wallets.get(player_state.player_id)
                if not wallet or wallet.balance < value:
                    return False
            elif criterion == "boss_defeated":
                if value not in player_state.achievements:
                    return False
            # Add more criteria as needed

        return True

    def execute_trade(self, sender_id: str, receiver_id: str,
                     coins: float, items: Dict[str, int]) -> bool:
        """Execute a trade between two players"""
        # Get states
        sender_state = self.game_states.get(sender_id)
        receiver_state = self.game_states.get(receiver_id)

        if not sender_state or not receiver_state:
            return False

        # Create trade transaction
        trade_tx = GameTransaction(
            transaction_id=hashlib.md5(
                f"{sender_id}_{receiver_id}_{time.time()}".encode()
            ).hexdigest()[:16],
            player_id=sender_id,
            transaction_type="trade",
            amount=coins,
            item_data=items,
            metadata={
                "receiver_id": receiver_id,
                "trade_time": time.time()
            },
            coherence_score=(sender_state.coherence + receiver_state.coherence) / 2
        )

        # Verify and process
        if not self._verify_trade(trade_tx):
            return False

        # Execute trade
        # Transfer coins
        if coins > 0:
            sender_wallet = self.player_wallets.get(sender_id)
            receiver_wallet = self.player_wallets.get(receiver_id)

            if sender_wallet and receiver_wallet:
                if sender_wallet.balance >= coins:
                    sender_wallet.balance -= coins
                    receiver_wallet.balance += coins
                else:
                    return False

        # Transfer items
        for item, count in items.items():
            if sender_state.inventory.get(item, 0) >= count:
                sender_state.inventory[item] -= count
                receiver_state.inventory[item] = receiver_state.inventory.get(item, 0) + count
            else:
                return False

        # Process transaction
        return self.process_game_transaction(trade_tx)

    def get_leaderboard(self, metric: str = "coherence") -> List[Dict]:
        """Get game leaderboard from blockchain"""
        leaderboard = []

        for player_id, state in self.game_states.items():
            wallet = self.player_wallets.get(player_id)
            entry = {
                "player_id": player_id,
                "coherence": state.coherence,
                "achievements": len(state.achievements),
                "play_time": state.play_time,
                "coins": wallet.balance if wallet else 0
            }
            leaderboard.append(entry)

        # Sort by metric
        leaderboard.sort(key=lambda x: x.get(metric, 0), reverse=True)

        return leaderboard[:10]  # Top 10

    def verify_game_integrity(self) -> bool:
        """Verify the integrity of all game data on blockchain"""
        # Verify blockchain integrity
        if not self.blockchain.is_chain_valid():
            print("Blockchain integrity check failed!")
            return False

        # Verify Crystal Ledger
        if not self.crystal_ledger.validate_chain():
            print("Crystal Ledger integrity check failed!")
            return False

        # Verify game states
        for player_id, state in self.game_states.items():
            calculated_hash = state.calculate_hash()
            # Find corresponding blockchain entry
            found = False
            for block in self.blockchain.chain:
                for tx in block.transactions:
                    if isinstance(tx, dict):
                        tx_data = json.loads(tx.get("data", "{}"))
                        if (tx_data.get("player") == player_id and
                            tx_data.get("game_metadata", {}).get("state_hash") == calculated_hash):
                            found = True
                            break

            if not found:
                print(f"State verification failed for player {player_id}")
                return False

        return True

    def _process_transaction(self, transaction: GameTransaction):
        """Internal method to process a single transaction"""
        # Verify transaction
        if not self._verify_coherence(transaction):
            return

        # Create blockchain transaction
        player_wallet = self.player_wallets.get(transaction.player_id)
        if not player_wallet:
            player_wallet = self.create_player_wallet(transaction.player_id)

        blockchain_tx = transaction.to_blockchain_transaction(player_wallet)

        # Add to blockchain
        self.blockchain.add_transaction(blockchain_tx)

        # Mark as verified
        transaction.verified = True

class MultiplayerCoordinator:
    """Coordinates multiplayer interactions through blockchain"""

    def __init__(self, game_blockchain: GameBlockchain):
        self.blockchain = game_blockchain
        self.active_sessions: Dict[str, Dict] = {}
        self.pvp_matches: Dict[str, Dict] = {}
        self.coop_quests: Dict[str, Dict] = {}

    def create_pvp_match(self, player1_id: str, player2_id: str,
                        stakes: float = 0) -> str:
        """Create a PvP match with optional stakes"""
        match_id = hashlib.md5(
            f"{player1_id}_{player2_id}_{time.time()}".encode()
        ).hexdigest()[:16]

        # Create match record
        self.pvp_matches[match_id] = {
            "player1": player1_id,
            "player2": player2_id,
            "stakes": stakes,
            "started": time.time(),
            "status": "active",
            "winner": None,
            "coherence_scores": {player1_id: 0, player2_id: 0}
        }

        # Create blockchain record
        match_tx = GameTransaction(
            transaction_id=match_id,
            player_id=player1_id,
            transaction_type="pvp_start",
            amount=stakes,
            metadata={
                "opponent": player2_id,
                "match_id": match_id
            }
        )

        self.blockchain.process_game_transaction(match_tx)

        return match_id

    def resolve_pvp_match(self, match_id: str, winner_id: str) -> bool:
        """Resolve a PvP match and distribute rewards"""
        if match_id not in self.pvp_matches:
            return False

        match = self.pvp_matches[match_id]
        if match["status"] != "active":
            return False

        # Update match
        match["winner"] = winner_id
        match["status"] = "completed"
        match["ended"] = time.time()

        # Calculate rewards
        loser_id = match["player2"] if winner_id == match["player1"] else match["player1"]
        stakes = match["stakes"]

        if stakes > 0:
            # Transfer stakes
            self.blockchain.execute_trade(
                loser_id, winner_id,
                stakes, {}
            )

        # Award achievement if applicable
        winner_state = self.blockchain.game_states.get(winner_id)
        if winner_state and winner_state.coherence > Z_C:
            self.blockchain.award_achievement(winner_id, "pvp_victor")

        # Create completion transaction
        completion_tx = GameTransaction(
            transaction_id=f"{match_id}_complete",
            player_id=winner_id,
            transaction_type="pvp_complete",
            amount=stakes * 2 if stakes > 0 else PHI * 10,
            metadata={
                "match_id": match_id,
                "duration": match["ended"] - match["started"],
                "loser": loser_id
            }
        )

        self.blockchain.process_game_transaction(completion_tx)

        return True

    def create_coop_quest(self, initiator_id: str, quest_data: Dict) -> str:
        """Create a cooperative quest"""
        quest_id = hashlib.md5(
            f"{initiator_id}_{quest_data.get('name')}_{time.time()}".encode()
        ).hexdigest()[:16]

        self.coop_quests[quest_id] = {
            "quest_id": quest_id,
            "initiator": initiator_id,
            "participants": [initiator_id],
            "quest_data": quest_data,
            "status": "gathering",
            "started": None,
            "progress": 0.0,
            "rewards": quest_data.get("rewards", {})
        }

        # Broadcast quest availability
        quest_tx = GameTransaction(
            transaction_id=quest_id,
            player_id=initiator_id,
            transaction_type="coop_quest_create",
            amount=0,
            metadata=quest_data
        )

        self.blockchain.process_game_transaction(quest_tx)

        return quest_id

    def join_coop_quest(self, quest_id: str, player_id: str) -> bool:
        """Join a cooperative quest"""
        if quest_id not in self.coop_quests:
            return False

        quest = self.coop_quests[quest_id]
        if quest["status"] != "gathering":
            return False

        # Check max participants
        max_participants = quest["quest_data"].get("max_participants", 4)
        if len(quest["participants"]) >= max_participants:
            return False

        # Add participant
        quest["participants"].append(player_id)

        # Start if ready
        min_participants = quest["quest_data"].get("min_participants", 2)
        if len(quest["participants"]) >= min_participants:
            quest["status"] = "active"
            quest["started"] = time.time()

        return True

    def update_coop_progress(self, quest_id: str, progress_delta: float) -> bool:
        """Update cooperative quest progress"""
        if quest_id not in self.coop_quests:
            return False

        quest = self.coop_quests[quest_id]
        if quest["status"] != "active":
            return False

        # Update progress
        quest["progress"] = min(1.0, quest["progress"] + progress_delta)

        # Check completion
        if quest["progress"] >= 1.0:
            self._complete_coop_quest(quest_id)

        return True

    def _complete_coop_quest(self, quest_id: str):
        """Complete a cooperative quest and distribute rewards"""
        quest = self.coop_quests[quest_id]
        quest["status"] = "completed"
        quest["completed"] = time.time()

        # Calculate coherence bonus
        total_coherence = 0
        for participant in quest["participants"]:
            state = self.blockchain.game_states.get(participant)
            if state:
                total_coherence += state.coherence

        avg_coherence = total_coherence / len(quest["participants"])
        coherence_multiplier = 1 + (avg_coherence - 0.5) * PHI

        # Distribute rewards
        base_reward = quest["rewards"].get("coins", PHI * 20)
        items = quest["rewards"].get("items", {})

        for participant in quest["participants"]:
            # Coins reward
            coin_reward = base_reward * coherence_multiplier / len(quest["participants"])
            wallet = self.blockchain.player_wallets.get(participant)
            if wallet:
                self.blockchain._mint_coins(wallet.address, coin_reward)

            # Items reward
            state = self.blockchain.game_states.get(participant)
            if state:
                for item, count in items.items():
                    state.inventory[item] = state.inventory.get(item, 0) + count

            # Create reward transaction
            reward_tx = GameTransaction(
                transaction_id=f"{quest_id}_{participant}_reward",
                player_id=participant,
                transaction_type="coop_reward",
                amount=coin_reward,
                item_data=items,
                metadata={
                    "quest_id": quest_id,
                    "quest_name": quest["quest_data"].get("name"),
                    "duration": quest["completed"] - quest["started"]
                }
            )

            self.blockchain.process_game_transaction(reward_tx)

# Export main components
__all__ = [
    'GameBlockchain',
    'GameTransaction',
    'GameState',
    'Achievement',
    'MultiplayerCoordinator'
]