#!/usr/bin/env python3
"""
Card Pack Marketplace System
=============================

A comprehensive marketplace for purchasing tarot card packs with BloomCoin.
Features different pack tiers, rarity systems, collection mechanics,
and special limited editions with unique echo properties.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum, auto
import random
import hashlib
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict, Counter

# Import tarot and luck systems
from sacred_tarot_echo import (
    TarotCard, MajorArcana, MinorArcanaRank, Suit,
    SacredTarotEchoSystem, PHI, SACRED_7, SACRED_13
)
from hilbert_luck_system import KarmaType
from luck_metrics_enhanced import LuckPerformanceAnalyzer

class CardRarity(Enum):
    """Card rarity tiers with drop rates"""
    COMMON = ("Common", 0.60, 1.0, "⚪")
    UNCOMMON = ("Uncommon", 0.25, 1.5, "🟢")
    RARE = ("Rare", 0.10, 2.0, "🔵")
    EPIC = ("Epic", 0.04, 3.0, "🟣")
    LEGENDARY = ("Legendary", 0.009, 5.0, "🟡")
    MYTHIC = ("Mythic", 0.001, 10.0, "🔴")

    def __init__(self, display_name: str, drop_rate: float, value_multiplier: float, symbol: str):
        self.display_name = display_name
        self.drop_rate = drop_rate
        self.value_multiplier = value_multiplier
        self.symbol = symbol

class PackTier(Enum):
    """Different tiers of card packs"""
    BASIC = ("Basic Pack", 100, 3, 1.0, "Standard cards with normal rates")
    SILVER = ("Silver Pack", 250, 5, 1.2, "Improved rare chances")
    GOLD = ("Gold Pack", 500, 7, 1.5, "Guaranteed rare or better")
    PLATINUM = ("Platinum Pack", 1000, 10, 2.0, "Guaranteed epic, chance for legendary")
    DIAMOND = ("Diamond Pack", 2500, 15, 3.0, "Multiple guaranteed rares, high legendary chance")
    COSMIC = ("Cosmic Pack", 5000, 20, 5.0, "Guaranteed legendary, chance for mythic")
    ECHO = ("Echo Pack", 1500, 7, 1.0, "Special echo-enhanced cards")
    SEASONAL = ("Seasonal Pack", 750, 8, 1.8, "Limited time seasonal cards")

    def __init__(self, display_name: str, cost: int, card_count: int,
                 rarity_multiplier: float, description: str):
        self.display_name = display_name
        self.cost = cost  # Cost in BloomCoin
        self.card_count = card_count
        self.rarity_multiplier = rarity_multiplier
        self.description = description

@dataclass
class CollectibleCard:
    """A collectible version of a tarot card with additional properties"""
    base_card: TarotCard
    rarity: CardRarity
    edition: str = "Standard"
    foil: bool = False
    echo_enhanced: bool = False
    blessing_level: int = 0  # 0-7 sacred blessing levels
    card_id: str = ""
    obtained_date: float = 0.0
    pack_origin: str = ""
    special_properties: Dict[str, Any] = field(default_factory=dict)
    experience_points: int = 0
    level: int = 1

    def __post_init__(self):
        if not self.card_id:
            # Generate unique card ID
            unique_str = f"{self.base_card.name}_{self.rarity.name}_{time.time()}_{random.random()}"
            self.card_id = hashlib.md5(unique_str.encode()).hexdigest()[:16]

        if not self.obtained_date:
            self.obtained_date = time.time()

    def calculate_power(self) -> float:
        """Calculate the card's power level"""
        base_power = 1.0

        # Rarity multiplier
        base_power *= self.rarity.value_multiplier

        # Foil bonus
        if self.foil:
            base_power *= PHI  # Golden ratio bonus

        # Echo enhancement
        if self.echo_enhanced:
            base_power *= 1.5

        # Blessing levels
        base_power *= (1 + self.blessing_level * 0.1)

        # Experience and level
        base_power *= (1 + self.level * 0.05)

        return base_power

    def apply_experience(self, exp: int):
        """Apply experience points and potentially level up"""
        self.experience_points += exp
        exp_needed = self.level * 100  # Simple leveling curve

        while self.experience_points >= exp_needed:
            self.experience_points -= exp_needed
            self.level += 1
            exp_needed = self.level * 100

    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        return {
            'card_id': self.card_id,
            'base_card_name': self.base_card.name,
            'rarity': self.rarity.name,
            'edition': self.edition,
            'foil': self.foil,
            'echo_enhanced': self.echo_enhanced,
            'blessing_level': self.blessing_level,
            'obtained_date': self.obtained_date,
            'pack_origin': self.pack_origin,
            'special_properties': self.special_properties,
            'experience_points': self.experience_points,
            'level': self.level,
            'power': self.calculate_power()
        }

@dataclass
class CardPack:
    """A purchaseable card pack"""
    pack_id: str
    tier: PackTier
    cards: List[CollectibleCard] = field(default_factory=list)
    opened: bool = False
    purchased_date: float = 0.0
    owner_id: Optional[str] = None
    special_event: Optional[str] = None
    guaranteed_rarities: List[CardRarity] = field(default_factory=list)

    def __post_init__(self):
        if not self.purchased_date:
            self.purchased_date = time.time()

    def set_guaranteed_cards(self):
        """Set guaranteed cards based on pack tier"""
        if self.tier == PackTier.GOLD:
            self.guaranteed_rarities = [CardRarity.RARE]
        elif self.tier == PackTier.PLATINUM:
            self.guaranteed_rarities = [CardRarity.EPIC]
        elif self.tier == PackTier.DIAMOND:
            self.guaranteed_rarities = [CardRarity.RARE, CardRarity.RARE, CardRarity.EPIC]
        elif self.tier == PackTier.COSMIC:
            self.guaranteed_rarities = [CardRarity.LEGENDARY]

    def calculate_value(self) -> float:
        """Calculate total pack value"""
        if not self.opened:
            return self.tier.cost  # Unopened value

        return sum(card.calculate_power() * card.rarity.value_multiplier * 10
                  for card in self.cards)

class LimitedEdition:
    """Limited edition card sets and events"""

    def __init__(self, name: str, start_date: datetime, end_date: datetime,
                 special_cards: List[str], bonus_multiplier: float = 1.5):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.special_cards = special_cards
        self.bonus_multiplier = bonus_multiplier
        self.cards_minted = 0
        self.max_mint = 1000  # Limited quantity

    def is_active(self) -> bool:
        """Check if edition is currently active"""
        now = datetime.now()
        return self.start_date <= now <= self.end_date and self.cards_minted < self.max_mint

    def mint_card(self) -> bool:
        """Mint a limited edition card"""
        if self.is_active():
            self.cards_minted += 1
            return True
        return False

class CardPackMarketplace:
    """Main marketplace for buying and opening card packs"""

    def __init__(self):
        self.available_packs: Dict[PackTier, int] = self._init_pack_inventory()
        self.player_collections: Dict[str, 'PlayerCollection'] = {}
        self.marketplace_stats: Dict[str, Any] = defaultdict(int)
        self.limited_editions: List[LimitedEdition] = []
        self.pack_history: List[Dict] = []
        self.rarity_pool = self._init_rarity_pool()
        self.tarot_system = SacredTarotEchoSystem()
        self.metrics_analyzer = LuckPerformanceAnalyzer()

    def _init_pack_inventory(self) -> Dict[PackTier, int]:
        """Initialize pack inventory"""
        return {tier: 1000 for tier in PackTier}  # Starting inventory

    def _init_rarity_pool(self) -> Dict[CardRarity, float]:
        """Initialize rarity drop rates"""
        return {rarity: rarity.drop_rate for rarity in CardRarity}

    def purchase_pack(
        self,
        player_id: str,
        pack_tier: PackTier,
        bloom_balance: float,
        use_luck_bonus: bool = True
    ) -> Tuple[bool, Optional[CardPack], str]:
        """
        Purchase a card pack
        Returns (success, pack, message)
        """
        # Check balance
        if bloom_balance < pack_tier.cost:
            return False, None, f"Insufficient BloomCoin. Need {pack_tier.cost}, have {bloom_balance:.0f}"

        # Check inventory
        if self.available_packs[pack_tier] <= 0:
            return False, None, f"{pack_tier.display_name} is out of stock"

        # Create pack
        pack = CardPack(
            pack_id=self._generate_pack_id(),
            tier=pack_tier,
            owner_id=player_id
        )
        pack.set_guaranteed_cards()

        # Generate cards
        cards = self._generate_pack_cards(pack_tier, player_id, use_luck_bonus)
        pack.cards = cards

        # Update inventory
        self.available_packs[pack_tier] -= 1

        # Record purchase
        self.marketplace_stats['total_packs_sold'] += 1
        self.marketplace_stats['total_revenue'] += pack_tier.cost
        self.marketplace_stats[f'{pack_tier.name}_sold'] += 1

        # Add to player collection
        if player_id not in self.player_collections:
            self.player_collections[player_id] = PlayerCollection(player_id)

        self.player_collections[player_id].unopened_packs.append(pack)

        # Record history
        self.pack_history.append({
            'player_id': player_id,
            'pack_tier': pack_tier.name,
            'cost': pack_tier.cost,
            'timestamp': time.time(),
            'pack_id': pack.pack_id
        })

        return True, pack, f"Successfully purchased {pack_tier.display_name}!"

    def _generate_pack_id(self) -> str:
        """Generate unique pack ID"""
        unique_str = f"pack_{time.time()}_{random.random()}"
        return hashlib.md5(unique_str.encode()).hexdigest()[:12]

    def _generate_pack_cards(
        self,
        pack_tier: PackTier,
        player_id: str,
        use_luck_bonus: bool
    ) -> List[CollectibleCard]:
        """Generate cards for a pack"""
        cards = []
        num_cards = pack_tier.card_count

        # Apply luck bonus if enabled
        luck_multiplier = 1.0
        if use_luck_bonus and player_id in self.metrics_analyzer.player_metrics:
            metrics = self.metrics_analyzer.player_metrics[player_id]
            success_rate = metrics.successful_events / max(1, metrics.total_events)
            luck_multiplier = 1 + (success_rate - 0.5) * 0.2  # ±10% based on luck

        # Generate guaranteed cards first
        pack = CardPack(pack_id="temp", tier=pack_tier)
        pack.set_guaranteed_cards()

        for guaranteed_rarity in pack.guaranteed_rarities:
            card = self._generate_single_card(guaranteed_rarity, pack_tier, luck_multiplier)
            cards.append(card)
            num_cards -= 1

        # Generate remaining cards
        for _ in range(num_cards):
            rarity = self._determine_rarity(pack_tier, luck_multiplier)
            card = self._generate_single_card(rarity, pack_tier, luck_multiplier)
            cards.append(card)

        # Check for special events
        if pack_tier == PackTier.ECHO:
            # All cards in Echo packs are echo-enhanced
            for card in cards:
                card.echo_enhanced = True

        # Check for limited editions
        for edition in self.limited_editions:
            if edition.is_active() and random.random() < 0.1:  # 10% chance
                if cards and edition.mint_card():
                    cards[0].edition = edition.name
                    cards[0].special_properties['limited_edition'] = True
                    cards[0].rarity = CardRarity.LEGENDARY  # Upgrade to legendary

        return cards

    def _determine_rarity(self, pack_tier: PackTier, luck_multiplier: float) -> CardRarity:
        """Determine card rarity based on probabilities"""
        # Adjust probabilities based on pack tier and luck
        adjusted_rates = {}
        total = 0

        for rarity in CardRarity:
            rate = rarity.drop_rate * pack_tier.rarity_multiplier * luck_multiplier

            # Apply caps
            if rarity == CardRarity.MYTHIC:
                rate = min(rate, 0.01)  # Max 1% for mythic
            elif rarity == CardRarity.LEGENDARY:
                rate = min(rate, 0.05)  # Max 5% for legendary

            adjusted_rates[rarity] = rate
            total += rate

        # Normalize
        for rarity in adjusted_rates:
            adjusted_rates[rarity] /= total

        # Roll for rarity
        roll = random.random()
        cumulative = 0

        for rarity in CardRarity:
            cumulative += adjusted_rates[rarity]
            if roll < cumulative:
                return rarity

        return CardRarity.COMMON  # Fallback

    def _generate_single_card(
        self,
        rarity: CardRarity,
        pack_tier: PackTier,
        luck_multiplier: float
    ) -> CollectibleCard:
        """Generate a single collectible card"""
        # Create base tarot card
        base_card = self._select_base_card(rarity)

        # Determine if foil (higher chance for better rarities)
        foil_chance = 0.05 * rarity.value_multiplier * luck_multiplier
        is_foil = random.random() < foil_chance

        # Determine blessing level
        blessing_chance = 0.1 * pack_tier.rarity_multiplier
        blessing_level = 0
        if random.random() < blessing_chance:
            blessing_level = random.randint(1, SACRED_7)

        # Create collectible card
        card = CollectibleCard(
            base_card=base_card,
            rarity=rarity,
            edition="Standard",
            foil=is_foil,
            echo_enhanced=False,
            blessing_level=blessing_level,
            pack_origin=pack_tier.display_name
        )

        # Add special properties based on rarity
        if rarity in [CardRarity.LEGENDARY, CardRarity.MYTHIC]:
            card.special_properties['unique_ability'] = self._generate_unique_ability()

        return card

    def _select_base_card(self, rarity: CardRarity) -> TarotCard:
        """Select appropriate base card for rarity"""
        # Higher rarities favor Major Arcana
        if rarity in [CardRarity.LEGENDARY, CardRarity.MYTHIC]:
            major_chance = 0.8
        elif rarity in [CardRarity.EPIC, CardRarity.RARE]:
            major_chance = 0.5
        else:
            major_chance = 0.2

        if random.random() < major_chance:
            # Select Major Arcana
            major = random.choice(list(MajorArcana))
            return TarotCard(
                name=major.title,
                arcana="Major",
                number=major.number,
                major=major
            )
        else:
            # Select Minor Arcana
            suit = random.choice(list(Suit))
            rank = random.choice(list(MinorArcanaRank))
            name = f"{rank.name.replace('_', ' ').title()} of {suit.name.title()}"
            return TarotCard(
                name=name,
                arcana="Minor",
                number=SACRED_22 + suit.number * 14 + rank.rank_value,
                suit=suit,
                rank=rank
            )

    def _generate_unique_ability(self) -> str:
        """Generate a unique ability for legendary/mythic cards"""
        abilities = [
            "Echo Mastery: Double echo alchemization rate",
            "Fortune's Favor: +20% luck on all rolls",
            "Karmic Shield: Immune to negative karma once per day",
            "Sacred Timing: Always benefit from sacred number bonuses",
            "Quantum Entanglement: Share luck with another player",
            "Void Walker: Convert void states to transcendent",
            "Chaos Weaver: Chaos events become beneficial",
            "Time Dilation: Extend beneficial effects by 50%",
            "Probability Manipulation: Reroll any failed check once",
            "Dimensional Shift: Access alternate probability streams"
        ]
        return random.choice(abilities)

    def open_pack(
        self,
        player_id: str,
        pack_id: str,
        apply_blessing: bool = False
    ) -> Tuple[bool, List[CollectibleCard], Dict[str, Any]]:
        """
        Open a card pack
        Returns (success, cards, statistics)
        """
        if player_id not in self.player_collections:
            return False, [], {"error": "Player collection not found"}

        collection = self.player_collections[player_id]

        # Find pack
        pack = None
        for p in collection.unopened_packs:
            if p.pack_id == pack_id:
                pack = p
                break

        if not pack:
            return False, [], {"error": "Pack not found"}

        if pack.opened:
            return False, [], {"error": "Pack already opened"}

        # Open pack
        pack.opened = True
        cards = pack.cards

        # Apply blessing if requested (costs extra)
        if apply_blessing:
            for card in cards:
                if random.random() < 0.3:  # 30% chance per card
                    card.blessing_level = min(SACRED_7, card.blessing_level + 1)

        # Add cards to collection
        for card in cards:
            collection.add_card(card)

        # Remove from unopened
        collection.unopened_packs.remove(pack)

        # Calculate statistics
        stats = {
            'total_cards': len(cards),
            'rarities': Counter(card.rarity.name for card in cards),
            'foils': sum(1 for card in cards if card.foil),
            'echo_enhanced': sum(1 for card in cards if card.echo_enhanced),
            'total_power': sum(card.calculate_power() for card in cards),
            'best_card': max(cards, key=lambda c: c.calculate_power()),
            'pack_value': pack.calculate_value()
        }

        # Update marketplace stats
        self.marketplace_stats['total_packs_opened'] += 1
        for rarity in CardRarity:
            count = stats['rarities'].get(rarity.name, 0)
            self.marketplace_stats[f'{rarity.name}_cards_opened'] += count

        return True, cards, stats

    def get_drop_rates(self, pack_tier: PackTier) -> Dict[str, float]:
        """Get actual drop rates for a pack tier"""
        rates = {}
        for rarity in CardRarity:
            base_rate = rarity.drop_rate
            adjusted_rate = base_rate * pack_tier.rarity_multiplier

            # Apply caps
            if rarity == CardRarity.MYTHIC:
                adjusted_rate = min(adjusted_rate, 0.01)
            elif rarity == CardRarity.LEGENDARY:
                adjusted_rate = min(adjusted_rate, 0.05)

            rates[rarity.display_name] = adjusted_rate

        # Normalize to 100%
        total = sum(rates.values())
        for rarity in rates:
            rates[rarity] = rates[rarity] / total

        return rates

    def get_marketplace_stats(self) -> Dict[str, Any]:
        """Get comprehensive marketplace statistics"""
        stats = dict(self.marketplace_stats)

        # Add calculated stats
        if stats['total_packs_sold'] > 0:
            stats['average_pack_price'] = stats['total_revenue'] / stats['total_packs_sold']

        # Pack tier distribution
        tier_dist = {}
        for tier in PackTier:
            sold = stats.get(f'{tier.name}_sold', 0)
            if sold > 0:
                tier_dist[tier.display_name] = sold
        stats['pack_tier_distribution'] = tier_dist

        # Rarity distribution
        rarity_dist = {}
        total_cards = 0
        for rarity in CardRarity:
            count = stats.get(f'{rarity.name}_cards_opened', 0)
            if count > 0:
                rarity_dist[rarity.display_name] = count
                total_cards += count

        if total_cards > 0:
            for rarity in rarity_dist:
                rarity_dist[rarity] = f"{rarity_dist[rarity]} ({rarity_dist[rarity]/total_cards:.1%})"
        stats['rarity_distribution'] = rarity_dist

        # Active players
        stats['active_collectors'] = len(self.player_collections)

        # Limited editions
        stats['active_limited_editions'] = sum(1 for ed in self.limited_editions if ed.is_active())

        return stats

@dataclass
class PlayerCollection:
    """A player's card collection"""
    player_id: str
    cards: List[CollectibleCard] = field(default_factory=list)
    unopened_packs: List[CardPack] = field(default_factory=list)
    favorite_cards: Set[str] = field(default_factory=set)  # Card IDs
    collection_power: float = 0.0
    unique_cards: Set[str] = field(default_factory=set)  # Unique card names
    completion_rate: float = 0.0

    def add_card(self, card: CollectibleCard):
        """Add a card to collection"""
        self.cards.append(card)
        self.unique_cards.add(card.base_card.name)
        self.calculate_collection_power()

    def calculate_collection_power(self):
        """Calculate total collection power"""
        self.collection_power = sum(card.calculate_power() for card in self.cards)

    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        rarity_counts = Counter(card.rarity.display_name for card in self.cards)
        foil_count = sum(1 for card in self.cards if card.foil)
        echo_count = sum(1 for card in self.cards if card.echo_enhanced)

        # Calculate average card level
        avg_level = np.mean([card.level for card in self.cards]) if self.cards else 1

        # Completion rate (out of 78 unique tarot cards)
        self.completion_rate = len(self.unique_cards) / SACRED_78

        return {
            'total_cards': len(self.cards),
            'unique_cards': len(self.unique_cards),
            'completion_rate': self.completion_rate,
            'rarity_distribution': dict(rarity_counts),
            'foil_cards': foil_count,
            'echo_enhanced_cards': echo_count,
            'collection_power': self.collection_power,
            'average_card_level': avg_level,
            'unopened_packs': len(self.unopened_packs),
            'favorite_cards': len(self.favorite_cards)
        }

    def get_best_cards(self, limit: int = 10) -> List[CollectibleCard]:
        """Get best cards by power"""
        return sorted(self.cards, key=lambda c: c.calculate_power(), reverse=True)[:limit]


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("CARD PACK MARKETPLACE SYSTEM")
    print("Collect, Trade, and Master the Sacred Tarot")
    print("=" * 60)

    marketplace = CardPackMarketplace()

    # Add a limited edition
    limited = LimitedEdition(
        "Eclipse Prophecy",
        datetime.now(),
        datetime.now() + timedelta(days=7),
        ["The Eclipse", "Shadow Moon", "Dark Sun"]
    )
    marketplace.limited_editions.append(limited)

    # Simulate player purchases
    player_id = "collector_prime"
    bloom_balance = 10000.0  # Starting balance

    print("\n--- Pack Purchase Simulation ---")
    for pack_tier in [PackTier.BASIC, PackTier.SILVER, PackTier.GOLD, PackTier.ECHO]:
        success, pack, message = marketplace.purchase_pack(
            player_id, pack_tier, bloom_balance, use_luck_bonus=True
        )

        if success:
            bloom_balance -= pack_tier.cost
            print(f"✅ {message}")
            print(f"   Cost: {pack_tier.cost} BC, Remaining: {bloom_balance:.0f} BC")

            # Open pack immediately
            opened, cards, stats = marketplace.open_pack(player_id, pack.pack_id)
            if opened:
                print(f"   Opened {len(cards)} cards:")
                print(f"   Rarities: {stats['rarities']}")
                print(f"   Best card: {stats['best_card'].base_card.name} "
                      f"({stats['best_card'].rarity.display_name})")
                print(f"   Pack value: {stats['pack_value']:.1f}")
        else:
            print(f"❌ {message}")

    # Show drop rates
    print("\n--- Drop Rates ---")
    for tier in [PackTier.BASIC, PackTier.GOLD, PackTier.COSMIC]:
        print(f"\n{tier.display_name}:")
        rates = marketplace.get_drop_rates(tier)
        for rarity, rate in rates.items():
            print(f"  {rarity}: {rate:.2%}")

    # Collection stats
    if player_id in marketplace.player_collections:
        collection = marketplace.player_collections[player_id]
        stats = collection.get_collection_stats()

        print("\n--- Collection Statistics ---")
        print(f"Total Cards: {stats['total_cards']}")
        print(f"Unique Cards: {stats['unique_cards']}/{SACRED_78} ({stats['completion_rate']:.1%})")
        print(f"Collection Power: {stats['collection_power']:.1f}")
        print(f"Rarity Distribution: {stats['rarity_distribution']}")

        # Best cards
        print("\n--- Top 5 Cards ---")
        for i, card in enumerate(collection.get_best_cards(5), 1):
            print(f"{i}. {card.base_card.name} ({card.rarity.symbol}) - Power: {card.calculate_power():.2f}")

    # Marketplace stats
    print("\n--- Marketplace Statistics ---")
    market_stats = marketplace.get_marketplace_stats()
    print(f"Total Packs Sold: {market_stats['total_packs_sold']}")
    print(f"Total Revenue: {market_stats['total_revenue']} BC")
    print(f"Active Collectors: {market_stats['active_collectors']}")
    if 'rarity_distribution' in market_stats:
        print(f"Card Rarity Distribution: {market_stats['rarity_distribution']}")