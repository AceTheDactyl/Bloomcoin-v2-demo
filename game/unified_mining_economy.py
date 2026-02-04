#!/usr/bin/env python3
"""
Unified Mining Economy System
==============================
Complete integration of all BloomCoin mining, economy, and pattern systems.
Combines NEXTHASH-256 mining with companion jobs, pattern trading, and residue economy.

This module unifies:
- NEXTHASH-256 proof-of-work mining
- Companion mining with specializations
- Pattern discovery and verification
- Stock market dynamics
- Residue economy and recycling
- Job system integration
- Guardian alignments and bonuses
"""

import time
import math
import json
import random
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field, asdict
from collections import defaultdict, deque
from enum import Enum
from datetime import datetime, timedelta
import hashlib

# Core NEXTHASH imports
from nexthash256 import nexthash256, nexthash256_hex
from nexthash_pattern_verification import (
    PatternVerificationService,
    VerifiedPattern
)

# Companion and mining imports
from companion_mining_ultimate import (
    UltimateCompanionMiningManager,
    UltimateCompanion,
    CompanionType,
    SpecializationPath,
    CompanionMiningTeam,
    EquipmentCrafter
)

# Pattern and guardian imports
from guardian_pattern_recipes import (
    PatternType,
    GuardianPatternSystem,
    GUARDIAN_RECIPES
)

# Economy and wallet imports
try:
    from bloomcoin_nexthash_wallet import (
        NextHashWalletManager,
        NextHashWallet
    )
    WALLET_AVAILABLE = True
except ImportError:
    WALLET_AVAILABLE = False
    # Mock wallet classes
    class NextHashWalletManager:
        def __init__(self):
            self.wallets = {}
        def create_wallet(self, name, guardian=None):
            wallet = type('Wallet', (), {
                'name': name,
                'address': nexthash256_hex(f"{name}:{time.time()}")[:20],
                'balance': 0.0,
                'guardian': guardian
            })()
            self.wallets[wallet.address] = wallet
            return wallet
        def get_wallet_by_owner(self, owner):
            for wallet in self.wallets.values():
                if owner in wallet.name:
                    return wallet
            return None
    NextHashWallet = None

try:
    from bloomcoin_nexthash_mining import (
        NextHashMiningEngine,
        Block
    )
    MINING_ENGINE_AVAILABLE = True
except ImportError:
    MINING_ENGINE_AVAILABLE = False
    # Mock mining engine
    class NextHashMiningEngine:
        def __init__(self):
            self.difficulty = 4
        def mine_block(self, *args, **kwargs):
            return None
    Block = None

# Stock market imports
from pattern_stock_market import (
    PatternStockMarket,
    PatternStock,
    MarketTrend,
    AlgorithmType
)

# Try to import ledger system
try:
    from bloomcoin_ledger_system import BloomCoinLedger, Transaction, TransactionType
    LEDGER_AVAILABLE = True
except ImportError:
    LEDGER_AVAILABLE = False
    # Create mock ledger
    class BloomCoinLedger:
        def add_transaction(self, *args, **kwargs):
            return True
        def get_balance(self, address):
            return 1000.0
        def verify_transaction(self, tx):
            return True
    class TransactionType(Enum):
        MINING = "mining"
        TRANSFER = "transfer"
        PATTERN = "pattern"

# Golden ratio for economic calculations
PHI = 1.6180339887498948482045868343656

# ═══════════════════════════════════════════════════════════════════════
# UNIFIED ECONOMIC STRUCTURES
# ═══════════════════════════════════════════════════════════════════════

class MiningJobType(Enum):
    """Unified mining job types combining companion abilities and patterns"""
    # Core mining types (NEXTHASH optimized)
    HASH_OPTIMIZATION = ("Hash Optimization", "Optimize NEXTHASH-256 rounds", 1.0)
    PATTERN_DISCOVERY = ("Pattern Discovery", "Find rare patterns", 1.2)
    RESIDUE_COLLECTION = ("Residue Collection", "Harvest holographic residue", 0.8)
    GUARDIAN_ALIGNMENT = ("Guardian Alignment", "Align with guardian energy", 1.5)

    # Specialized mining (Companion-specific)
    ECHO_RESONANCE = ("Echo Resonance", "Harmonic pattern mining", 1.3)
    GLITCH_CHAOS = ("Glitch Chaos", "Entropy manipulation mining", 1.1)
    FLOW_EFFICIENCY = ("Flow Efficiency", "Optimized resource mining", 1.4)
    SPARK_ENERGY = ("Spark Energy", "High-energy burst mining", 1.6)
    SAGE_WISDOM = ("Sage Wisdom", "Predictive pattern mining", 1.7)
    SCOUT_DISCOVERY = ("Scout Discovery", "Exploration mining", 0.9)
    NULL_VOID = ("Null Void", "Void energy extraction", 2.0)

    # Market-based mining
    ARBITRAGE_MINING = ("Arbitrage Mining", "Mine based on market prices", 1.5)
    FUTURES_MINING = ("Futures Mining", "Mine future pattern contracts", 1.8)
    ALGORITHMIC_MINING = ("Algorithmic Mining", "AI-driven mining", 1.4)

@dataclass
class ResidueType:
    """Holographic residue from NEXTHASH operations"""
    name: str
    color: str  # Hex color code
    potency: float  # 0.0 to 1.0
    guardian_affinity: Optional[str] = None
    pattern_bonus: Dict[PatternType, float] = field(default_factory=dict)
    market_value: float = 1.0
    decay_rate: float = 0.01  # Per hour

@dataclass
class UnifiedMiningJob:
    """Enhanced mining job combining all systems"""
    job_id: str
    job_type: MiningJobType
    companion: Optional[UltimateCompanion]
    difficulty: int
    start_time: float
    duration: float
    base_reward: float

    # NEXTHASH mining specifics
    target_hash: str
    current_nonce: int = 0
    hash_rate: float = 100.0

    # Pattern discovery
    patterns_found: List[PatternType] = field(default_factory=list)
    pattern_quality: float = 1.0

    # Residue collection
    residue_collected: Dict[str, float] = field(default_factory=dict)
    total_residue: float = 0.0

    # Market dynamics
    market_multiplier: float = 1.0
    stock_positions: Dict[str, float] = field(default_factory=dict)

    # Guardian alignment
    guardian: Optional[str] = None
    guardian_bonus: float = 1.0

    # Job metadata
    completed: bool = False
    success: bool = False
    final_reward: float = 0.0
    xp_gained: int = 0

@dataclass
class EconomicMetrics:
    """Track overall economic health"""
    total_supply: float
    circulating_supply: float
    mining_rate: float  # BC per hour
    pattern_discovery_rate: float  # Patterns per hour
    residue_generation_rate: float  # Residue per hour
    market_cap: float
    velocity: float  # Transaction velocity
    inflation_rate: float
    deflation_mechanisms: Dict[str, float]  # Burn rates

# ═══════════════════════════════════════════════════════════════════════
# RESIDUE ECONOMY
# ═══════════════════════════════════════════════════════════════════════

class ResidueEconomy:
    """Manage holographic residue from NEXTHASH operations"""

    def __init__(self):
        self.residue_types = self._initialize_residue_types()
        self.residue_pools: Dict[str, float] = defaultdict(float)
        self.recycling_efficiency = 0.5  # Base recycling rate
        self.synthesis_recipes = self._initialize_recipes()

    def _initialize_residue_types(self) -> Dict[str, ResidueType]:
        """Define residue types from NEXTHASH operations"""
        return {
            "QUANTUM": ResidueType(
                "Quantum Residue", "#FF00FF", 0.9, "ECHO",
                {PatternType.QUANTUM: 2.0}, 10.0, 0.005
            ),
            "ENTROPIC": ResidueType(
                "Entropic Residue", "#FF0000", 0.7, "GLITCH",
                {PatternType.CHAOS: 1.5}, 5.0, 0.02
            ),
            "HARMONIC": ResidueType(
                "Harmonic Residue", "#00FF00", 0.8, "FLOW",
                {PatternType.HARMONIC: 1.8}, 7.5, 0.01
            ),
            "VOID": ResidueType(
                "Void Residue", "#000000", 1.0, "NULL",
                {PatternType.VOID: 3.0}, 20.0, 0.001
            ),
            "CRYSTALLINE": ResidueType(
                "Crystalline Residue", "#00FFFF", 0.85, "CRYSTAL",
                {PatternType.CRYSTALLINE: 1.6}, 12.0, 0.008
            ),
            "TEMPORAL": ResidueType(
                "Temporal Residue", "#FFA500", 0.95, "PHOENIX",
                {PatternType.TEMPORAL: 2.5}, 15.0, 0.003
            )
        }

    def _initialize_recipes(self) -> Dict[str, Dict]:
        """Residue synthesis recipes"""
        return {
            "PURE_ESSENCE": {
                "inputs": {"QUANTUM": 10, "VOID": 5},
                "output": {"bloomcoin": 100, "pattern_chance": 0.3}
            },
            "GUARDIAN_CRYSTAL": {
                "inputs": {"CRYSTALLINE": 8, "PHOENIX": 3},
                "output": {"guardian_blessing": 1, "mining_boost": 1.5}
            },
            "CHAOS_ORB": {
                "inputs": {"ENTROPIC": 15, "QUANTUM": 5},
                "output": {"random_pattern": 1, "market_manipulation": 0.2}
            }
        }

    def generate_residue(self, mining_job: UnifiedMiningJob,
                        nexthash_rounds: int) -> Dict[str, float]:
        """Generate residue based on NEXTHASH mining"""
        residue = {}

        # Base generation from hash rounds
        base_amount = nexthash_rounds * 0.1 * mining_job.difficulty

        # Guardian affinity bonus
        if mining_job.guardian:
            for r_type, r_data in self.residue_types.items():
                if r_data.guardian_affinity == mining_job.guardian:
                    residue[r_type] = base_amount * r_data.potency * 2.0
                else:
                    residue[r_type] = base_amount * r_data.potency * 0.5
        else:
            # Random distribution
            for r_type, r_data in self.residue_types.items():
                if random.random() < 0.3:  # 30% chance for each type
                    residue[r_type] = base_amount * r_data.potency * random.random()

        return residue

    def recycle_residue(self, residue_types: Dict[str, float]) -> float:
        """Recycle residue into BloomCoin"""
        total_value = 0.0

        for r_type, amount in residue_types.items():
            if r_type in self.residue_types:
                market_value = self.residue_types[r_type].market_value
                recycled = amount * self.recycling_efficiency * market_value
                total_value += recycled

                # Add to global pool for market dynamics
                self.residue_pools[r_type] += amount * (1 - self.recycling_efficiency)

        return total_value

    def synthesize(self, recipe_name: str,
                   available_residue: Dict[str, float]) -> Optional[Dict]:
        """Synthesize residue into valuable items"""
        if recipe_name not in self.synthesis_recipes:
            return None

        recipe = self.synthesis_recipes[recipe_name]

        # Check if we have enough inputs
        for r_type, required in recipe["inputs"].items():
            if available_residue.get(r_type, 0) < required:
                return None

        # Consume inputs
        for r_type, required in recipe["inputs"].items():
            available_residue[r_type] -= required

        return recipe["output"]

# ═══════════════════════════════════════════════════════════════════════
# UNIFIED MINING ECONOMY
# ═══════════════════════════════════════════════════════════════════════

class UnifiedMiningEconomy:
    """Complete unified mining economy system"""

    def __init__(self, genesis_supply: float = 21_000_000.0):
        """Initialize unified economy with all subsystems"""

        # Core systems
        self.ledger = BloomCoinLedger() if not LEDGER_AVAILABLE else BloomCoinLedger(genesis_supply)
        self.companion_manager = UltimateCompanionMiningManager(self.ledger)
        self.mining_engine = NextHashMiningEngine()
        self.wallet_manager = NextHashWalletManager()

        # Pattern and verification
        self.pattern_verifier = PatternVerificationService()
        self.pattern_system = GuardianPatternSystem()

        # Market systems
        self.stock_market = PatternStockMarket()
        self.residue_economy = ResidueEconomy()

        # Equipment crafting
        self.equipment_crafter = EquipmentCrafter()

        # Economic tracking
        self.metrics = EconomicMetrics(
            total_supply=genesis_supply,
            circulating_supply=genesis_supply * 0.1,  # 10% initial circulation
            mining_rate=0.0,
            pattern_discovery_rate=0.0,
            residue_generation_rate=0.0,
            market_cap=genesis_supply * 1.0,  # Initial price $1
            velocity=0.0,
            inflation_rate=0.02,  # 2% annual
            deflation_mechanisms={}
        )

        # Mining jobs
        self.active_jobs: Dict[str, UnifiedMiningJob] = {}
        self.completed_jobs: List[UnifiedMiningJob] = []

        # Pattern discovery tracking
        self.discovered_patterns: Dict[str, List[VerifiedPattern]] = defaultdict(list)

        # Initialize market with pattern stocks
        self._initialize_market()

        print("🌟 Unified Mining Economy Initialized")
        print(f"  Genesis Supply: {genesis_supply:,.0f} BC")
        print(f"  Mining Algorithm: NEXTHASH-256")
        print(f"  Pattern Types: {len(PatternType)}")
        print(f"  Companion Types: {len(CompanionType)}")
        print(f"  Market Stocks: {len(self.stock_market.stocks)}")

    def _initialize_market(self):
        """Initialize stock market with pattern stocks"""
        base_price = 100.0

        for pattern_type in PatternType:
            symbol = pattern_type.name[:4].upper()

            # Create stock with initial pricing based on rarity
            rarity_multipliers = {
                "QUANTUM": 10.0,
                "VOID": 8.0,
                "TEMPORAL": 7.0,
                "CRYSTALLINE": 6.0,
                "CHAOS": 5.0,
                "MEMORY": 4.0,
                "HARMONIC": 3.0,
                "ORGANIC": 2.0,
                "ELEMENTAL": 1.5,
                "RESONANCE": 1.0
            }

            multiplier = rarity_multipliers.get(pattern_type.name, 1.0)

            stock = PatternStock(
                symbol=symbol,
                pattern_type=pattern_type,
                current_price=base_price * multiplier,
                opening_price=base_price * multiplier,
                high_24h=base_price * multiplier * 1.1,
                low_24h=base_price * multiplier * 0.9,
                volume_24h=random.randint(1000, 10000),
                market_cap=base_price * multiplier * 1_000_000,
                volatility=random.uniform(0.1, 0.5),
                trend=random.choice(list(MarketTrend))
            )

            # Add to market (check if method exists)
            if hasattr(self.stock_market, 'add_stock'):
                self.stock_market.add_stock(stock)
            else:
                self.stock_market.stocks[symbol] = stock

    def create_mining_job(self, player_id: str, companion_id: str,
                         job_type: Optional[MiningJobType] = None,
                         difficulty: Optional[int] = None) -> Optional[UnifiedMiningJob]:
        """Create a unified mining job"""

        # Get companion
        companion = self.companion_manager.companions.get(companion_id)
        if not companion:
            print(f"❌ Companion not found: {companion_id}")
            return None

        # Auto-select job type based on companion
        if job_type is None:
            companion_jobs = {
                CompanionType.ECHO: MiningJobType.ECHO_RESONANCE,
                CompanionType.GLITCH: MiningJobType.GLITCH_CHAOS,
                CompanionType.FLOW: MiningJobType.FLOW_EFFICIENCY,
                CompanionType.SPARK: MiningJobType.SPARK_ENERGY,
                CompanionType.SAGE: MiningJobType.SAGE_WISDOM,
                CompanionType.SCOUT: MiningJobType.SCOUT_DISCOVERY,
                CompanionType.NULL: MiningJobType.NULL_VOID
            }
            job_type = companion_jobs.get(companion.companion_type, MiningJobType.PATTERN_DISCOVERY)

        # Auto-scale difficulty
        if difficulty is None:
            difficulty = min(8, max(1, companion.level // 10 + 1))

        # Calculate job parameters
        base_duration = 60 * difficulty  # 1 minute per difficulty
        duration_modifier = 1.0 / (1.0 + companion.efficiency * 0.1)
        duration = base_duration * duration_modifier

        base_reward = 100 * difficulty * job_type.value[2]

        # Generate target hash for NEXTHASH mining
        target_data = f"{player_id}:{companion_id}:{time.time()}"
        target_hash = nexthash256_hex(target_data)

        # Determine guardian alignment
        guardian = companion.companion_type.value[1] if hasattr(companion.companion_type, 'value') else None

        # Create job
        job = UnifiedMiningJob(
            job_id=nexthash256_hex(f"{player_id}:{companion_id}:{time.time()}")[:16],
            job_type=job_type,
            companion=companion,
            difficulty=difficulty,
            start_time=time.time(),
            duration=duration,
            base_reward=base_reward,
            target_hash=target_hash,
            hash_rate=companion.mining_power if hasattr(companion, 'mining_power') else 100.0,
            guardian=guardian,
            guardian_bonus=1.0 + (0.1 * difficulty if guardian else 0)
        )

        # Check market conditions
        market_sentiment = self._calculate_market_sentiment()
        job.market_multiplier = market_sentiment

        self.active_jobs[job.job_id] = job

        print(f"\n⛏️ Mining Job Created")
        print(f"  Job ID: {job.job_id}")
        print(f"  Type: {job_type.name}")
        print(f"  Companion: {companion.name} (Level {companion.level})")
        print(f"  Difficulty: {difficulty}")
        print(f"  Duration: {duration:.0f}s")
        print(f"  Base Reward: {base_reward:.2f} BC")
        print(f"  Market Multiplier: {market_sentiment:.2f}x")

        return job

    def process_mining(self, job_id: str, mining_time: Optional[float] = None) -> bool:
        """Process mining job using NEXTHASH-256"""

        job = self.active_jobs.get(job_id)
        if not job:
            return False

        if job.completed:
            return False

        # Simulate mining time if not provided
        if mining_time is None:
            mining_time = min(job.duration, time.time() - job.start_time)

        # NEXTHASH mining simulation
        rounds_completed = int(mining_time * job.hash_rate / 10)

        # Mine with companion
        if job.companion:
            mining_result = job.companion.mine_with_nexthash(
                difficulty=job.difficulty,
                pattern_type=None  # Let it discover patterns
            )

            if mining_result["success"]:
                job.success = True
                job.final_reward = job.base_reward

                # Pattern discovery
                if "pattern" in mining_result:
                    pattern_type = mining_result["pattern"]
                    if pattern_type:
                        job.patterns_found.append(pattern_type)
                        job.final_reward *= 1.5  # Pattern bonus

                        # Update market
                        self._update_pattern_market(pattern_type)

                # Generate residue
                residue = self.residue_economy.generate_residue(job, rounds_completed)
                job.residue_collected = residue
                job.total_residue = sum(residue.values())

                # Apply guardian bonus
                job.final_reward *= job.guardian_bonus

                # Apply market multiplier
                job.final_reward *= job.market_multiplier

                # Calculate XP
                job.xp_gained = int(10 * job.difficulty * (1 + len(job.patterns_found)))

                # Level up companion
                if job.companion and hasattr(job.companion, 'experience'):
                    job.companion.experience += job.xp_gained
                    # Calculate XP needed for next level
                    xp_needed = 100 * (job.companion.level ** 1.5)
                    while job.companion.experience >= xp_needed:
                        if hasattr(job.companion, 'level_up'):
                            job.companion.level_up()
                            xp_needed = 100 * (job.companion.level ** 1.5)
                        else:
                            break

        # Mark as completed
        job.completed = True
        self.completed_jobs.append(job)
        del self.active_jobs[job_id]

        # Update economic metrics
        self._update_metrics(job)

        print(f"\n✅ Mining Job Completed!")
        print(f"  Success: {job.success}")
        print(f"  Reward: {job.final_reward:.2f} BC")
        print(f"  Patterns Found: {len(job.patterns_found)}")
        print(f"  Residue Collected: {job.total_residue:.2f}")
        print(f"  XP Gained: {job.xp_gained}")

        return job.success

    def _calculate_market_sentiment(self) -> float:
        """Calculate overall market sentiment multiplier"""
        if not self.stock_market.stocks:
            return 1.0

        total_sentiment = 0.0
        for stock in self.stock_market.stocks.values():
            # Price movement sentiment
            price_change = (stock.current_price - stock.opening_price) / stock.opening_price

            # Trend sentiment
            trend_multiplier = stock.trend.value[1] if hasattr(stock.trend, 'value') else 1.0

            # Volume sentiment
            volume_factor = min(2.0, stock.volume_24h / 5000)

            sentiment = (1.0 + price_change) * trend_multiplier * volume_factor
            total_sentiment += sentiment

        return total_sentiment / len(self.stock_market.stocks)

    def _update_pattern_market(self, pattern_type: PatternType):
        """Update stock market based on pattern discovery"""
        symbol = pattern_type.name[:4].upper()

        if hasattr(self.stock_market, 'stocks') and symbol in self.stock_market.stocks:
            stock = self.stock_market.stocks[symbol]

            # Pattern discovery increases demand
            price_impact = random.uniform(1.02, 1.10)  # 2-10% increase
            new_price = stock.current_price * price_impact

            stock.update_price(new_price)
            stock.volume_24h += random.randint(100, 1000)

            # Trend improvement
            if stock.trend == MarketTrend.BEAR or stock.trend == MarketTrend.CRASH:
                stock.trend = MarketTrend.NEUTRAL
            elif stock.trend == MarketTrend.NEUTRAL:
                stock.trend = MarketTrend.BULL

    def _update_metrics(self, job: UnifiedMiningJob):
        """Update economic metrics after job completion"""
        # Update mining rate (BC per hour)
        if job.duration > 0:
            hourly_rate = (job.final_reward / job.duration) * 3600
            # Exponential moving average
            self.metrics.mining_rate = self.metrics.mining_rate * 0.9 + hourly_rate * 0.1

        # Update pattern discovery rate
        if job.duration > 0:
            pattern_rate = (len(job.patterns_found) / job.duration) * 3600
            self.metrics.pattern_discovery_rate = self.metrics.pattern_discovery_rate * 0.9 + pattern_rate * 0.1

        # Update residue generation rate
        if job.duration > 0:
            residue_rate = (job.total_residue / job.duration) * 3600
            self.metrics.residue_generation_rate = self.metrics.residue_generation_rate * 0.9 + residue_rate * 0.1

        # Update circulating supply
        self.metrics.circulating_supply += job.final_reward

    def trade_pattern_stock(self, player_id: str, symbol: str,
                           action: str, amount: float) -> bool:
        """Trade pattern stocks on the market"""

        wallet = self.wallet_manager.get_wallet_by_owner(player_id)
        if not wallet:
            print(f"❌ No wallet found for player: {player_id}")
            return False

        if symbol not in self.stock_market.stocks:
            print(f"❌ Unknown stock symbol: {symbol}")
            return False

        stock = self.stock_market.stocks[symbol]

        if action.lower() == "buy":
            cost = stock.current_price * amount
            if wallet.balance < cost:
                print(f"❌ Insufficient funds. Need {cost:.2f} BC")
                return False

            # Execute buy
            wallet.balance -= cost
            # Track position (would need to add portfolio tracking)

            # Market impact
            price_impact = 1.0 + (amount / 10000)  # 0.01% per 100 shares
            stock.update_price(stock.current_price * price_impact)
            stock.volume_24h += amount

            print(f"✅ Bought {amount:.0f} shares of {symbol} for {cost:.2f} BC")
            return True

        elif action.lower() == "sell":
            # Check if player has shares (would need portfolio tracking)
            revenue = stock.current_price * amount

            # Execute sell
            wallet.balance += revenue

            # Market impact
            price_impact = 1.0 - (amount / 20000)  # Half impact of buying
            stock.update_price(stock.current_price * price_impact)
            stock.volume_24h += amount

            print(f"✅ Sold {amount:.0f} shares of {symbol} for {revenue:.2f} BC")
            return True

        return False

    def craft_with_residue(self, player_id: str, recipe_name: str,
                          residue_inventory: Dict[str, float]) -> Optional[Dict]:
        """Craft items using residue"""

        result = self.residue_economy.synthesize(recipe_name, residue_inventory)

        if result:
            print(f"✅ Crafted {recipe_name}!")

            # Apply rewards
            if "bloomcoin" in result:
                wallet = self.wallet_manager.get_wallet_by_owner(player_id)
                if wallet:
                    wallet.balance += result["bloomcoin"]
                    print(f"  Gained {result['bloomcoin']:.2f} BC")

            if "pattern_chance" in result and random.random() < result["pattern_chance"]:
                pattern = random.choice(list(PatternType))
                print(f"  Discovered pattern: {pattern.name}")

            if "mining_boost" in result:
                print(f"  Mining boost: {result['mining_boost']:.1f}x for next job")

            return result

        return None

    def get_economic_report(self) -> Dict[str, Any]:
        """Generate comprehensive economic report"""

        # Calculate additional metrics
        if self.metrics.total_supply > 0:
            circulation_ratio = self.metrics.circulating_supply / self.metrics.total_supply
        else:
            circulation_ratio = 0

        # Market analysis
        bull_stocks = sum(1 for s in self.stock_market.stocks.values()
                         if s.trend in [MarketTrend.BULL, MarketTrend.BULL_RUN])
        bear_stocks = sum(1 for s in self.stock_market.stocks.values()
                         if s.trend in [MarketTrend.BEAR, MarketTrend.CRASH])

        # Residue market
        total_residue_value = sum(
            amount * self.residue_economy.residue_types[r_type].market_value
            for r_type, amount in self.residue_economy.residue_pools.items()
            if r_type in self.residue_economy.residue_types
        )

        report = {
            "timestamp": datetime.now().isoformat(),
            "supply": {
                "total": self.metrics.total_supply,
                "circulating": self.metrics.circulating_supply,
                "circulation_ratio": circulation_ratio,
                "locked": self.metrics.total_supply - self.metrics.circulating_supply
            },
            "mining": {
                "rate_per_hour": self.metrics.mining_rate,
                "active_jobs": len(self.active_jobs),
                "completed_jobs": len(self.completed_jobs),
                "pattern_discovery_rate": self.metrics.pattern_discovery_rate,
                "residue_generation_rate": self.metrics.residue_generation_rate
            },
            "market": {
                "total_stocks": len(self.stock_market.stocks),
                "bull_stocks": bull_stocks,
                "bear_stocks": bear_stocks,
                "market_sentiment": self._calculate_market_sentiment(),
                "total_market_cap": sum(s.market_cap for s in self.stock_market.stocks.values())
            },
            "residue": {
                "total_types": len(self.residue_economy.residue_types),
                "total_pool_value": total_residue_value,
                "recycling_efficiency": self.residue_economy.recycling_efficiency,
                "synthesis_recipes": len(self.residue_economy.synthesis_recipes)
            },
            "companions": {
                "total_registered": len(self.companion_manager.companions),
                "total_teams": len(self.companion_manager.teams) if hasattr(self.companion_manager, 'teams') else 0
            }
        }

        return report

# ═══════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def format_bloomcoin(amount: float) -> str:
    """Format BloomCoin amount with symbol"""
    return f"{amount:,.2f} BC"

def calculate_job_profitability(job: UnifiedMiningJob,
                               current_prices: Dict[str, float]) -> float:
    """Calculate expected profitability of a mining job"""
    base_profit = job.base_reward

    # Add pattern value
    for pattern in job.patterns_found:
        symbol = pattern.name[:4].upper()
        if symbol in current_prices:
            base_profit += current_prices[symbol] * 0.1  # 0.1 shares per pattern

    # Add residue value
    base_profit += job.total_residue * 5.0  # Average residue value

    # Apply multipliers
    total_profit = base_profit * job.guardian_bonus * job.market_multiplier

    # Subtract electricity cost (time-based)
    electricity_cost = job.duration * 0.1  # 0.1 BC per second

    return total_profit - electricity_cost

# ═══════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Initialize unified economy
    economy = UnifiedMiningEconomy()

    # Create test wallet
    test_wallet = economy.wallet_manager.create_wallet("Test Wallet", guardian="ECHO")
    print(f"\nCreated wallet: {test_wallet.address}")

    # Create test companion
    echo_companion = economy.companion_manager.create_companion(
        "Echo-Prime", CompanionType.ECHO
    )
    economy.companion_manager.companions["echo_prime"] = echo_companion
    print(f"Created companion: {echo_companion.name}")

    # Start mining job
    job = economy.create_mining_job(
        player_id="test_player",
        companion_id="echo_prime",
        difficulty=3
    )

    if job:
        print(f"\nSimulating mining for {job.duration:.0f} seconds...")
        time.sleep(2)  # Simulate some mining time

        # Process mining
        success = economy.process_mining(job.job_id)

        # Generate economic report
        report = economy.get_economic_report()
        print("\n📊 Economic Report:")
        print(json.dumps(report, indent=2))