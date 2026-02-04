#!/usr/bin/env python3
"""
Luck Economy Integration System
================================

Complete integration of the enhanced luck system with BloomCoin economy,
card pack marketplace, and comprehensive analytics dashboard.
This creates a full game economy centered around luck mechanics and collectible cards.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum, auto
import json
import time
import random
from datetime import datetime, timedelta
from collections import defaultdict, deque

# Import all subsystems
from hilbert_luck_system import HilbertLuckEngine, KarmaType
from sacred_tarot_echo import SacredTarotEchoSystem, TarotSpread
from echo_companion_luck import EchoCompanion
from luck_normalization_system import ComprehensiveLuckSystem, LuckEventType
from luck_metrics_enhanced import LuckPerformanceAnalyzer, MetricType
from card_pack_marketplace import (
    CardPackMarketplace, PackTier, CardRarity,
    CollectibleCard, PlayerCollection
)
from bloomcoin_economy_complete import BloomCoinEconomy

class EconomyAction(Enum):
    """Economic actions that affect luck and cards"""
    BUY_PACK = "buy_pack"
    SELL_CARD = "sell_card"
    TRADE_CARD = "trade_card"
    BLESSING_RITUAL = "blessing_ritual"
    LUCK_INSURANCE = "luck_insurance"
    KARMA_CLEANSE = "karma_cleanse"
    ECHO_AMPLIFIER = "echo_amplifier"
    TAROT_READING = "tarot_reading"
    COLLECTION_SHOWCASE = "collection_showcase"
    LEGENDARY_CRAFT = "legendary_craft"

@dataclass
class PlayerEconomyProfile:
    """Complete economic profile for a player"""
    player_id: str
    bloom_balance: float = 1000.0
    total_spent: float = 0.0
    total_earned: float = 0.0
    packs_purchased: int = 0
    cards_sold: int = 0
    trades_completed: int = 0
    luck_insurance_active: bool = False
    insurance_expiry: float = 0.0
    blessing_level: int = 0
    vip_tier: int = 0  # 0-5 based on spending
    daily_bonus_claimed: float = 0.0
    referral_bonuses: int = 0
    achievement_rewards: Dict[str, bool] = field(default_factory=dict)

    def calculate_vip_tier(self) -> int:
        """Calculate VIP tier based on total spending"""
        thresholds = [0, 1000, 5000, 20000, 50000, 100000]
        for tier, threshold in enumerate(thresholds):
            if self.total_spent < threshold:
                return max(0, tier - 1)
        return 5

    def get_vip_benefits(self) -> Dict[str, Any]:
        """Get benefits based on VIP tier"""
        benefits = {
            0: {"luck_bonus": 1.0, "pack_discount": 0, "daily_bonus": 100},
            1: {"luck_bonus": 1.05, "pack_discount": 5, "daily_bonus": 150},
            2: {"luck_bonus": 1.10, "pack_discount": 10, "daily_bonus": 200},
            3: {"luck_bonus": 1.15, "pack_discount": 15, "daily_bonus": 300},
            4: {"luck_bonus": 1.20, "pack_discount": 20, "daily_bonus": 500},
            5: {"luck_bonus": 1.30, "pack_discount": 25, "daily_bonus": 1000}
        }
        return benefits.get(self.vip_tier, benefits[0])

@dataclass
class MarketTransaction:
    """Record of a market transaction"""
    transaction_id: str
    timestamp: float
    player_id: str
    action: EconomyAction
    amount: float
    details: Dict[str, Any]
    success: bool
    balance_after: float

class LuckEconomyIntegration:
    """Main integration system combining all components"""

    def __init__(self):
        # Core systems
        self.luck_system = ComprehensiveLuckSystem()
        self.marketplace = CardPackMarketplace()
        self.economy = BloomCoinEconomy()
        self.analytics = LuckPerformanceAnalyzer()

        # Player profiles
        self.economy_profiles: Dict[str, PlayerEconomyProfile] = {}

        # Market data
        self.transaction_history: deque = deque(maxlen=10000)
        self.market_prices: Dict[str, float] = self._init_market_prices()
        self.daily_deals: List[Dict] = []

        # Statistics
        self.global_stats = {
            'total_bloom_circulating': 1000000.0,
            'total_packs_sold': 0,
            'total_cards_traded': 0,
            'average_luck_score': 0.5,
            'echo_alchemy_rate': 0.0
        }

    def _init_market_prices(self) -> Dict[str, float]:
        """Initialize market prices for various services"""
        return {
            'blessing_ritual': 500,
            'luck_insurance_daily': 100,
            'karma_cleanse': 750,
            'echo_amplifier': 1000,
            'tarot_reading_basic': 50,
            'tarot_reading_advanced': 200,
            'card_listing_fee': 10,
            'legendary_craft_cost': 5000
        }

    def register_player(
        self,
        player_id: str,
        companion_type: str,
        starting_balance: float = 1000.0
    ) -> Dict[str, Any]:
        """Register a new player in the integrated system"""

        # Register in luck system
        luck_profile = self.luck_system.register_player(player_id, companion_type)

        # Create economy profile
        economy_profile = PlayerEconomyProfile(
            player_id=player_id,
            bloom_balance=starting_balance
        )
        self.economy_profiles[player_id] = economy_profile

        # Create wallet in blockchain economy
        wallet_address = self.economy.wallet_manager.create_wallet(player_id)
        if wallet_address:
            self.economy.wallet_manager.add_funds(wallet_address, starting_balance)

        # Initialize collection
        if player_id not in self.marketplace.player_collections:
            self.marketplace.player_collections[player_id] = PlayerCollection(player_id)

        return {
            'player_id': player_id,
            'companion_type': companion_type,
            'starting_balance': starting_balance,
            'wallet_address': wallet_address,
            'luck_profile_created': True,
            'collection_initialized': True
        }

    def purchase_card_pack(
        self,
        player_id: str,
        pack_tier: PackTier,
        apply_vip_discount: bool = True
    ) -> Tuple[bool, Optional[Dict], str]:
        """Purchase a card pack with integrated luck bonuses"""

        if player_id not in self.economy_profiles:
            return False, None, "Player not registered"

        profile = self.economy_profiles[player_id]

        # Calculate actual cost with VIP discount
        base_cost = pack_tier.cost
        if apply_vip_discount:
            vip_benefits = profile.get_vip_benefits()
            discount = vip_benefits['pack_discount'] / 100
            actual_cost = base_cost * (1 - discount)
        else:
            actual_cost = base_cost

        # Check balance
        if profile.bloom_balance < actual_cost:
            return False, None, f"Insufficient balance. Need {actual_cost:.0f} BC"

        # Apply luck bonus to pack generation
        use_luck_bonus = True

        # Purchase pack
        success, pack, message = self.marketplace.purchase_pack(
            player_id,
            pack_tier,
            profile.bloom_balance,
            use_luck_bonus
        )

        if success:
            # Update economy profile
            profile.bloom_balance -= actual_cost
            profile.total_spent += actual_cost
            profile.packs_purchased += 1
            profile.vip_tier = profile.calculate_vip_tier()

            # Record transaction
            transaction = MarketTransaction(
                transaction_id=self._generate_transaction_id(),
                timestamp=time.time(),
                player_id=player_id,
                action=EconomyAction.BUY_PACK,
                amount=actual_cost,
                details={'pack_tier': pack_tier.name, 'pack_id': pack.pack_id},
                success=True,
                balance_after=profile.bloom_balance
            )
            self.transaction_history.append(transaction)

            # Update global stats
            self.global_stats['total_packs_sold'] += 1

            # Apply karma for purchase (supporting the game)
            self.luck_system.apply_karma_action(
                player_id,
                "supported_marketplace",
                KarmaType.BENEVOLENT,
                0.05
            )

            return True, {
                'pack': pack,
                'cost': actual_cost,
                'discount_applied': base_cost - actual_cost,
                'new_balance': profile.bloom_balance,
                'vip_tier': profile.vip_tier
            }, message
        else:
            return False, None, message

    def open_pack_with_ceremony(
        self,
        player_id: str,
        pack_id: str,
        use_blessing: bool = False
    ) -> Tuple[bool, List[CollectibleCard], Dict]:
        """Open a pack with special ceremony and luck effects"""

        # Perform tarot reading for pack opening luck
        reading, luck_mod = self.luck_system.perform_tarot_divination(
            player_id,
            TarotSpread.THREE_CARD
        )

        # Apply blessing if requested (costs extra)
        blessing_cost = 0
        if use_blessing:
            blessing_cost = self.market_prices['blessing_ritual']
            if player_id in self.economy_profiles:
                profile = self.economy_profiles[player_id]
                if profile.bloom_balance >= blessing_cost:
                    profile.bloom_balance -= blessing_cost
                    profile.total_spent += blessing_cost
                else:
                    use_blessing = False  # Can't afford

        # Open pack
        success, cards, stats = self.marketplace.open_pack(
            player_id,
            pack_id,
            apply_blessing=use_blessing
        )

        if success:
            # Apply luck modifier to card experience
            for card in cards:
                if luck_mod > 1.5:  # Good luck
                    card.apply_experience(int(100 * luck_mod))

            # Track metrics
            for card in cards:
                # Track each card as a luck event
                self.analytics.track_player_event(
                    player_id,
                    LuckEventType.LOOT_DROP,
                    card.rarity.drop_rate,
                    True,  # Got the card
                    reading.karma_influence,
                    0.0,  # Echo density
                    False,  # Not echo event
                    False  # Not alchemized
                )

            # Special rewards for exceptional pulls
            legendary_count = sum(1 for c in cards
                                if c.rarity == CardRarity.LEGENDARY)
            mythic_count = sum(1 for c in cards
                              if c.rarity == CardRarity.MYTHIC)

            bonus_rewards = 0
            if mythic_count > 0:
                bonus_rewards = 1000 * mythic_count
                self._grant_achievement(player_id, "mythic_pull")
            elif legendary_count >= 2:
                bonus_rewards = 500
                self._grant_achievement(player_id, "double_legendary")

            if bonus_rewards > 0 and player_id in self.economy_profiles:
                self.economy_profiles[player_id].bloom_balance += bonus_rewards

            return True, cards, {
                'stats': stats,
                'luck_modifier': luck_mod,
                'blessing_applied': use_blessing,
                'blessing_cost': blessing_cost if use_blessing else 0,
                'bonus_rewards': bonus_rewards,
                'tarot_reading': {
                    'cards_drawn': [c.name for c in reading.cards],
                    'echo_count': reading.echo_count
                }
            }
        else:
            return False, [], {'error': 'Failed to open pack'}

    def purchase_luck_service(
        self,
        player_id: str,
        service_type: str
    ) -> Tuple[bool, Dict[str, Any]]:
        """Purchase various luck-enhancing services"""

        if player_id not in self.economy_profiles:
            return False, {'error': 'Player not registered'}

        profile = self.economy_profiles[player_id]

        # Get service cost
        if service_type not in self.market_prices:
            return False, {'error': 'Unknown service type'}

        cost = self.market_prices[service_type]

        # Check balance
        if profile.bloom_balance < cost:
            return False, {'error': f'Insufficient balance. Need {cost} BC'}

        # Apply service effects
        effects = {}

        if service_type == 'luck_insurance_daily':
            # Luck insurance reduces bad luck events for 24 hours
            profile.luck_insurance_active = True
            profile.insurance_expiry = time.time() + 86400  # 24 hours
            effects['duration'] = '24 hours'
            effects['bad_luck_reduction'] = '50%'

        elif service_type == 'karma_cleanse':
            # Reset negative karma
            if player_id in self.luck_system.player_profiles:
                luck_state = self.luck_system.hilbert_engine.luck_states.get(player_id)
                if luck_state and luck_state.karma_balance < 0:
                    old_karma = luck_state.karma_balance
                    luck_state.karma_balance = 0
                    luck_state.echo_density *= 0.5  # Also reduce echo
                    effects['karma_cleansed'] = abs(old_karma)
                    effects['echo_reduction'] = '50%'

        elif service_type == 'echo_amplifier':
            # Boost Echo companion abilities
            if player_id in self.luck_system.player_profiles:
                profile_luck = self.luck_system.player_profiles[player_id]
                if profile_luck.echo_companion:
                    profile_luck.echo_companion.resonance_state.echo_attunement += 0.2
                    profile_luck.echo_companion.resonance_state.alchemical_power += 0.1
                    effects['echo_attunement_boost'] = '+20%'
                    effects['alchemical_power_boost'] = '+10%'
                else:
                    return False, {'error': 'Echo companion required'}

        elif service_type == 'blessing_ritual':
            # Increase blessing level temporarily
            profile.blessing_level = min(SACRED_7, profile.blessing_level + 1)
            effects['new_blessing_level'] = profile.blessing_level
            effects['luck_multiplier'] = 1 + profile.blessing_level * 0.1

        # Deduct cost
        profile.bloom_balance -= cost
        profile.total_spent += cost

        # Record transaction
        transaction = MarketTransaction(
            transaction_id=self._generate_transaction_id(),
            timestamp=time.time(),
            player_id=player_id,
            action=EconomyAction.LUCK_INSURANCE if 'insurance' in service_type
                    else EconomyAction.KARMA_CLEANSE if 'karma' in service_type
                    else EconomyAction.ECHO_AMPLIFIER if 'echo' in service_type
                    else EconomyAction.BLESSING_RITUAL,
            amount=cost,
            details={'service': service_type, 'effects': effects},
            success=True,
            balance_after=profile.bloom_balance
        )
        self.transaction_history.append(transaction)

        return True, {
            'service': service_type,
            'cost': cost,
            'effects': effects,
            'new_balance': profile.bloom_balance
        }

    def sell_card(
        self,
        player_id: str,
        card_id: str
    ) -> Tuple[bool, float, str]:
        """Sell a card for BloomCoin"""

        if player_id not in self.marketplace.player_collections:
            return False, 0, "No collection found"

        collection = self.marketplace.player_collections[player_id]

        # Find card
        card = None
        for c in collection.cards:
            if c.card_id == card_id:
                card = c
                break

        if not card:
            return False, 0, "Card not found"

        # Calculate sell price
        base_price = 10 * card.rarity.value_multiplier
        power_multiplier = card.calculate_power()
        sell_price = base_price * power_multiplier

        # Apply market fluctuation
        market_modifier = 0.8 + random.random() * 0.4  # 80-120%
        sell_price *= market_modifier

        # Remove card from collection
        collection.cards.remove(card)
        collection.calculate_collection_power()

        # Add funds
        if player_id in self.economy_profiles:
            profile = self.economy_profiles[player_id]
            profile.bloom_balance += sell_price
            profile.total_earned += sell_price
            profile.cards_sold += 1

            # Record transaction
            transaction = MarketTransaction(
                transaction_id=self._generate_transaction_id(),
                timestamp=time.time(),
                player_id=player_id,
                action=EconomyAction.SELL_CARD,
                amount=sell_price,
                details={'card_id': card_id, 'card_name': card.base_card.name,
                        'rarity': card.rarity.name},
                success=True,
                balance_after=profile.bloom_balance
            )
            self.transaction_history.append(transaction)

        return True, sell_price, f"Sold {card.base_card.name} for {sell_price:.0f} BC"

    def claim_daily_bonus(self, player_id: str) -> Tuple[bool, float, Dict]:
        """Claim daily login bonus with luck multiplier"""

        if player_id not in self.economy_profiles:
            return False, 0, {'error': 'Player not registered'}

        profile = self.economy_profiles[player_id]

        # Check if already claimed today
        last_claim = profile.daily_bonus_claimed
        if time.time() - last_claim < 86400:  # 24 hours
            time_remaining = 86400 - (time.time() - last_claim)
            hours_remaining = time_remaining / 3600
            return False, 0, {'error': f'Already claimed. Try again in {hours_remaining:.1f} hours'}

        # Calculate bonus based on VIP tier
        vip_benefits = profile.get_vip_benefits()
        base_bonus = vip_benefits['daily_bonus']

        # Apply luck multiplier
        luck_roll = self.luck_system.roll_luck_event(
            player_id,
            LuckEventType.BLESSING_RECEIVED
        )
        success, event = luck_roll

        if success:
            luck_multiplier = event.luck_modifier
            bonus = base_bonus * luck_multiplier
        else:
            bonus = base_bonus * 0.5  # Bad luck = half bonus

        # Grant bonus
        profile.bloom_balance += bonus
        profile.total_earned += bonus
        profile.daily_bonus_claimed = time.time()

        return True, bonus, {
            'base_bonus': base_bonus,
            'luck_multiplier': luck_multiplier if success else 0.5,
            'final_bonus': bonus,
            'vip_tier': profile.vip_tier,
            'new_balance': profile.bloom_balance
        }

    def get_analytics_dashboard(self, player_id: str) -> Dict[str, Any]:
        """Get comprehensive analytics dashboard for a player"""

        dashboard = {
            'player_id': player_id,
            'timestamp': time.time()
        }

        # Luck metrics
        if player_id in self.analytics.player_metrics:
            luck_report = self.analytics.get_player_report(player_id)
            dashboard['luck_metrics'] = luck_report

        # Economy stats
        if player_id in self.economy_profiles:
            profile = self.economy_profiles[player_id]
            dashboard['economy'] = {
                'balance': profile.bloom_balance,
                'total_spent': profile.total_spent,
                'total_earned': profile.total_earned,
                'vip_tier': profile.vip_tier,
                'vip_benefits': profile.get_vip_benefits(),
                'packs_purchased': profile.packs_purchased,
                'cards_sold': profile.cards_sold
            }

        # Collection stats
        if player_id in self.marketplace.player_collections:
            collection = self.marketplace.player_collections[player_id]
            dashboard['collection'] = collection.get_collection_stats()

        # Karma and Echo status
        quantum_report = self.luck_system.hilbert_engine.get_quantum_report(player_id)
        dashboard['quantum_state'] = quantum_report

        # Recent transactions
        recent_transactions = [
            t for t in self.transaction_history
            if t.player_id == player_id
        ][-10:]  # Last 10 transactions

        dashboard['recent_transactions'] = [
            {
                'action': t.action.value,
                'amount': t.amount,
                'timestamp': t.timestamp,
                'success': t.success
            }
            for t in recent_transactions
        ]

        # Achievements
        if player_id in self.economy_profiles:
            achievements = self.economy_profiles[player_id].achievement_rewards
            dashboard['achievements'] = {
                'unlocked': list(achievements.keys()),
                'total': len(achievements)
            }

        # Predictive analytics
        if player_id in self.luck_system.player_profiles:
            profile_luck = self.luck_system.player_profiles[player_id]
            next_event_prediction = self.analytics.player_metrics[player_id].predictive_model.predict_outcome(
                LuckEventType.LOOT_DROP.value,
                quantum_report.get('karma_balance', 0),
                quantum_report.get('echo_density', 0)
            )
            dashboard['predictions'] = {
                'next_loot_drop_probability': next_event_prediction[0],
                'confidence': next_event_prediction[1]
            }

        # Rankings
        dashboard['rankings'] = self._get_player_rankings(player_id)

        return dashboard

    def _get_player_rankings(self, player_id: str) -> Dict[str, Any]:
        """Get player rankings across various categories"""
        rankings = {}

        # Generate leaderboards
        leaderboards = self.analytics.generate_leaderboards()

        for category, leaders in leaderboards.items():
            # Find player rank
            player_rank = None
            for rank, (pid, score) in enumerate(leaders, 1):
                if pid == player_id:
                    player_rank = rank
                    player_score = score
                    break

            if player_rank:
                rankings[category] = {
                    'rank': player_rank,
                    'score': player_score,
                    'percentile': (len(leaders) - player_rank + 1) / len(leaders) * 100
                }

        return rankings

    def _generate_transaction_id(self) -> str:
        """Generate unique transaction ID"""
        return hashlib.md5(f"{time.time()}_{random.random()}".encode()).hexdigest()[:16]

    def _grant_achievement(self, player_id: str, achievement: str):
        """Grant an achievement to a player"""
        if player_id in self.economy_profiles:
            profile = self.economy_profiles[player_id]
            if achievement not in profile.achievement_rewards:
                profile.achievement_rewards[achievement] = True

                # Grant achievement reward
                rewards = {
                    'first_pack': 100,
                    'mythic_pull': 2000,
                    'double_legendary': 1000,
                    'collection_complete': 10000,
                    'echo_master': 5000,
                    'karma_saint': 3000,
                    'luck_champion': 7500
                }

                if achievement in rewards:
                    reward = rewards[achievement]
                    profile.bloom_balance += reward
                    profile.total_earned += reward

    def get_market_overview(self) -> Dict[str, Any]:
        """Get overview of the entire market"""
        overview = {
            'global_stats': self.global_stats,
            'marketplace_stats': self.marketplace.get_marketplace_stats(),
            'total_players': len(self.economy_profiles),
            'total_bloom_in_circulation': sum(p.bloom_balance
                                            for p in self.economy_profiles.values()),
            'average_player_balance': np.mean([p.bloom_balance
                                              for p in self.economy_profiles.values()]),
            'vip_distribution': Counter(p.vip_tier
                                       for p in self.economy_profiles.values()),
            'pack_prices': {tier.display_name: tier.cost for tier in PackTier},
            'service_prices': self.market_prices,
            'recent_activity': len([t for t in self.transaction_history
                                   if time.time() - t.timestamp < 3600])  # Last hour
        }

        return overview


# Example usage and demonstration
if __name__ == "__main__":
    print("=" * 70)
    print("INTEGRATED LUCK ECONOMY SYSTEM")
    print("Where Fortune Meets Finance")
    print("=" * 70)

    # Initialize the integrated system
    system = LuckEconomyIntegration()

    # Register test players
    players = [
        ("alice", "Echo"),
        ("bob", "Seeker"),
        ("charlie", "Prometheus")
    ]

    for player_id, companion in players:
        result = system.register_player(player_id, companion, starting_balance=2000)
        print(f"\n✅ Registered {player_id} with {companion} companion")
        print(f"   Starting balance: 2000 BC")

    # Simulate market activity
    print("\n" + "=" * 50)
    print("MARKET SIMULATION")
    print("=" * 50)

    # Alice (Echo player) buys packs
    print("\n--- Alice's Shopping Spree ---")
    for pack_type in [PackTier.SILVER, PackTier.ECHO]:
        success, result, message = system.purchase_card_pack("alice", pack_type)
        if success:
            print(f"✅ Purchased {pack_type.display_name} for {result['cost']:.0f} BC")

            # Open the pack
            pack_id = result['pack']['pack_id'] if 'pack' in result and result['pack'] else None
            if pack_id:
                opened, cards, stats = system.open_pack_with_ceremony("alice", pack_id, use_blessing=True)
                if opened:
                    print(f"   Opened {len(cards)} cards!")
                    print(f"   Best card: {cards[0].base_card.name} ({cards[0].rarity.display_name})")
                    if stats['bonus_rewards'] > 0:
                        print(f"   🎉 BONUS REWARD: {stats['bonus_rewards']} BC!")

    # Bob applies negative karma and needs cleansing
    print("\n--- Bob's Karma Troubles ---")
    system.luck_system.apply_karma_action("bob", "betrayal", KarmaType.DESTRUCTIVE, -0.8)
    print("❌ Bob committed betrayal (-0.8 karma)")

    # Check his luck
    success, event = system.luck_system.roll_luck_event("bob", LuckEventType.LOOT_DROP)
    print(f"   Luck check: {'SUCCESS' if success else 'FAIL'} (prob: {event.final_probability:.1%})")

    # Buy karma cleanse
    success, effects = system.purchase_luck_service("bob", "karma_cleanse")
    if success:
        print(f"✅ Purchased karma cleanse for {effects['cost']} BC")
        print(f"   Effects: {effects['effects']}")

    # Charlie claims daily bonus
    print("\n--- Charlie's Daily Bonus ---")
    success, bonus, details = system.claim_daily_bonus("charlie")
    if success:
        print(f"✅ Claimed daily bonus: {bonus:.0f} BC")
        print(f"   Luck multiplier: {details.get('luck_multiplier', 1):.2f}x")

    # Show analytics dashboards
    print("\n" + "=" * 50)
    print("PLAYER DASHBOARDS")
    print("=" * 50)

    for player_id, _ in players:
        dashboard = system.get_analytics_dashboard(player_id)

        print(f"\n📊 {player_id.upper()}'s Dashboard")
        if 'economy' in dashboard:
            eco = dashboard['economy']
            print(f"   Balance: {eco['balance']:.0f} BC")
            print(f"   VIP Tier: {eco['vip_tier']} (Luck Bonus: {eco['vip_benefits']['luck_bonus']:.2f}x)")

        if 'collection' in dashboard:
            coll = dashboard['collection']
            print(f"   Cards: {coll['total_cards']} ({coll['unique_cards']}/{SACRED_78} unique)")
            print(f"   Power: {coll['collection_power']:.1f}")

        if 'quantum_state' in dashboard:
            quantum = dashboard['quantum_state']
            print(f"   Karma: {quantum.get('karma_balance', 0):.2f}")
            print(f"   Echo Density: {quantum.get('echo_density', 0):.2f}")

        if 'predictions' in dashboard:
            pred = dashboard['predictions']
            print(f"   Next Loot Prediction: {pred['next_loot_drop_probability']:.1%} "
                  f"(confidence: {pred['confidence']:.1%})")

    # Market overview
    print("\n" + "=" * 50)
    print("MARKET OVERVIEW")
    print("=" * 50)

    overview = system.get_market_overview()
    print(f"Total Players: {overview['total_players']}")
    print(f"Bloom in Circulation: {overview['total_bloom_in_circulation']:.0f} BC")
    print(f"Average Balance: {overview['average_player_balance']:.0f} BC")
    print(f"Recent Activity (last hour): {overview['recent_activity']} transactions")

    if 'marketplace_stats' in overview:
        market = overview['marketplace_stats']
        print(f"Total Packs Sold: {market.get('total_packs_sold', 0)}")
        print(f"Total Revenue: {market.get('total_revenue', 0):.0f} BC")

    print("\n" + "=" * 70)
    print("✨ The economy of fortune is in full swing!")
    print("   Where every card drawn shapes your destiny...")

# Import fix for SACRED constants
SACRED_7 = 7
SACRED_78 = 78