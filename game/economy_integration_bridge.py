#!/usr/bin/env python3
"""
Economy Integration Bridge
===========================
Bridges and adapters to connect all existing BloomCoin systems with the
unified mining economy. Provides backwards compatibility and migration paths.

This module connects:
- Old companion_mining_jobs.py → unified_mining_economy.py
- bloomcoin_economy_complete.py → unified system
- pattern_stock_market.py → integrated market
- Various pattern systems → unified pattern economy
"""

import time
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict

# Import unified system
from unified_mining_economy import (
    UnifiedMiningEconomy,
    UnifiedMiningJob,
    MiningJobType,
    ResidueType,
    format_bloomcoin
)

# Import legacy systems for compatibility
try:
    from companion_mining_jobs import (
        CompanionMiningSystem as LegacyMiningSystem,
        MiningJob as LegacyMiningJob,
        MiningJobType as LegacyJobType
    )
    LEGACY_MINING_AVAILABLE = True
except ImportError:
    LEGACY_MINING_AVAILABLE = False

try:
    from bloomcoin_economy_complete import BloomCoinEconomy as LegacyEconomy
    LEGACY_ECONOMY_AVAILABLE = True
except ImportError:
    LEGACY_ECONOMY_AVAILABLE = False

# ═══════════════════════════════════════════════════════════════════════
# MIGRATION MAPPINGS
# ═══════════════════════════════════════════════════════════════════════

class JobTypeMigration:
    """Maps legacy job types to unified system"""

    LEGACY_TO_UNIFIED = {
        # From companion_mining_jobs.py
        "RESONANCE_TUNING": MiningJobType.ECHO_RESONANCE,
        "PATTERN_SEARCH": MiningJobType.PATTERN_DISCOVERY,
        "VOID_DIVING": MiningJobType.NULL_VOID,
        "HASH_EXPLORATION": MiningJobType.HASH_OPTIMIZATION,
        "ENTROPY_HARVEST": MiningJobType.GLITCH_CHAOS,
        "MEMORY_CRYSTALLIZATION": MiningJobType.SAGE_WISDOM,
        "FRACTAL_GROWTH": MiningJobType.FLOW_EFFICIENCY,

        # From advanced_mining_jobs.py (unused but mapped for completeness)
        "HASH_ENGINEER": MiningJobType.HASH_OPTIMIZATION,
        "CRYPTO_GEOLOGIST": MiningJobType.PATTERN_DISCOVERY,
        "QUANTUM_MINER": MiningJobType.GUARDIAN_ALIGNMENT,
        "PATTERN_WEAVER": MiningJobType.PATTERN_DISCOVERY,
        "EFFICIENCY_EXPERT": MiningJobType.FLOW_EFFICIENCY,
        "LUCK_MANIPULATOR": MiningJobType.GLITCH_CHAOS,
        "TIME_BENDER": MiningJobType.SPARK_ENERGY,
        "NEXTHASH_SPECIALIST": MiningJobType.HASH_OPTIMIZATION,
        "VOID_WALKER": MiningJobType.NULL_VOID,
        "ECHO_HARMONIZER": MiningJobType.ECHO_RESONANCE,
        "CRYSTAL_SHAPER": MiningJobType.GUARDIAN_ALIGNMENT,
        "CHAOS_CONTROLLER": MiningJobType.GLITCH_CHAOS
    }

    @classmethod
    def migrate(cls, legacy_type: Union[str, Any]) -> MiningJobType:
        """Convert legacy job type to unified type"""
        if isinstance(legacy_type, str):
            type_str = legacy_type
        elif hasattr(legacy_type, 'name'):
            type_str = legacy_type.name
        elif hasattr(legacy_type, 'value'):
            type_str = legacy_type.value
        else:
            type_str = str(legacy_type)

        return cls.LEGACY_TO_UNIFIED.get(
            type_str,
            MiningJobType.PATTERN_DISCOVERY  # Default
        )

# ═══════════════════════════════════════════════════════════════════════
# COMPATIBILITY ADAPTERS
# ═══════════════════════════════════════════════════════════════════════

class LegacyMiningAdapter:
    """Adapter for old companion_mining_jobs system"""

    def __init__(self, unified_economy: UnifiedMiningEconomy):
        self.unified = unified_economy
        self.job_mapping: Dict[str, str] = {}  # Legacy ID -> Unified ID

    def create_job(self, companion_name: str, job_type: Any,
                  difficulty: int) -> Optional[LegacyMiningJob]:
        """Create job using legacy interface"""

        # Map to unified system
        unified_job_type = JobTypeMigration.migrate(job_type)

        # Find or create companion in unified system
        companion_id = f"{companion_name.lower()}_legacy"

        if companion_id not in self.unified.companion_manager.companions:
            # Create companion based on name
            from companion_mining_ultimate import CompanionType

            companion_type_map = {
                "Echo": CompanionType.ECHO,
                "Glitch": CompanionType.GLITCH,
                "Flow": CompanionType.FLOW,
                "Spark": CompanionType.SPARK,
                "Sage": CompanionType.SAGE,
                "Scout": CompanionType.SCOUT,
                "Null": CompanionType.NULL
            }

            comp_type = companion_type_map.get(companion_name, CompanionType.ECHO)
            companion = self.unified.companion_manager.create_companion(
                companion_name, comp_type
            )
            self.unified.companion_manager.companions[companion_id] = companion

        # Create unified job
        unified_job = self.unified.create_mining_job(
            player_id="legacy_player",
            companion_id=companion_id,
            job_type=unified_job_type,
            difficulty=difficulty
        )

        if not unified_job:
            return None

        # Create legacy-compatible job object
        if LEGACY_MINING_AVAILABLE:
            legacy_job = LegacyMiningJob(
                job_id=unified_job.job_id,
                companion_name=companion_name,
                job_type=job_type,
                difficulty=difficulty,
                start_time=unified_job.start_time,
                duration=unified_job.duration,
                base_reward=unified_job.base_reward,
                completed=False
            )

            # Track mapping
            self.job_mapping[legacy_job.job_id] = unified_job.job_id

            return legacy_job
        else:
            # Return a mock object
            return type('LegacyMiningJob', (), {
                'job_id': unified_job.job_id,
                'companion_name': companion_name,
                'job_type': job_type,
                'difficulty': difficulty,
                'duration': unified_job.duration,
                'base_reward': unified_job.base_reward,
                'completed': False
            })()

    def complete_job(self, job_id: str) -> bool:
        """Complete job using legacy interface"""

        # Map to unified ID if needed
        unified_id = self.job_mapping.get(job_id, job_id)

        # Process in unified system
        return self.unified.process_mining(unified_id)

class LegacyEconomyBridge:
    """Bridge for old bloomcoin_economy_complete.py"""

    def __init__(self, unified_economy: UnifiedMiningEconomy):
        self.unified = unified_economy

    def create_player_account(self, player_id: str,
                             initial_balance: float = 100.0) -> Any:
        """Create account using legacy interface"""

        wallet = self.unified.wallet_manager.create_wallet(
            f"Player_{player_id}",
            guardian=None
        )

        # Add initial balance (would need transaction in real system)
        wallet.balance = initial_balance

        return wallet

    def start_companion_mining(self, wallet_address: str,
                              companion_name: str,
                              job_type: Any = None,
                              difficulty: int = None) -> Optional[Any]:
        """Start mining using legacy interface"""

        # Extract player ID from wallet
        wallet = self.unified.wallet_manager.wallets.get(wallet_address)
        if not wallet:
            return None

        player_id = wallet.name.replace("Player_", "")

        # Use adapter for job creation
        adapter = LegacyMiningAdapter(self.unified)
        return adapter.create_job(companion_name, job_type, difficulty)

# ═══════════════════════════════════════════════════════════════════════
# PATTERN SYSTEM INTEGRATION
# ═══════════════════════════════════════════════════════════════════════

class PatternSystemIntegration:
    """Integrates all pattern systems with unified economy"""

    def __init__(self, unified_economy: UnifiedMiningEconomy):
        self.unified = unified_economy

    def register_pattern_discovery(self, player_id: str,
                                   pattern_type: Any,
                                   source: str = "unknown") -> bool:
        """Register pattern discovery from any system"""

        # Create verified pattern
        from guardian_pattern_recipes import PatternType

        # Convert pattern type if needed
        if isinstance(pattern_type, str):
            try:
                pattern = PatternType[pattern_type.upper()]
            except KeyError:
                pattern = PatternType.SEED  # Default
        else:
            pattern = pattern_type

        # Create verification
        verified = self.unified.pattern_verifier.create_verified_pattern(
            pattern_type=pattern,
            creator=player_id,
            data={"source": source, "timestamp": time.time()},
            guardian=None
        )

        if verified:
            self.unified.discovered_patterns[player_id].append(verified)

            # Update market
            self.unified._update_pattern_market(pattern)

            # Reward discovery
            wallet = self.unified.wallet_manager.get_wallet_by_owner(player_id)
            if wallet:
                reward = 10.0 * (1 + len(self.unified.discovered_patterns[player_id]) * 0.1)
                wallet.balance += reward
                print(f"✅ Pattern {pattern.name} discovered! Reward: {reward:.2f} BC")

            return True

        return False

    def get_pattern_portfolio(self, player_id: str) -> Dict[str, Any]:
        """Get player's pattern portfolio value"""

        patterns = self.unified.discovered_patterns.get(player_id, [])

        portfolio = {
            "total_patterns": len(patterns),
            "unique_types": len(set(p.pattern_type for p in patterns)),
            "total_value": 0.0,
            "patterns_by_type": {},
            "market_values": {}
        }

        for pattern in patterns:
            p_type = pattern.pattern_type.name

            # Count patterns
            if p_type not in portfolio["patterns_by_type"]:
                portfolio["patterns_by_type"][p_type] = 0
            portfolio["patterns_by_type"][p_type] += 1

            # Calculate value
            symbol = p_type[:4].upper()
            if symbol in self.unified.stock_market.stocks:
                stock = self.unified.stock_market.stocks[symbol]
                value = stock.current_price
                portfolio["total_value"] += value
                portfolio["market_values"][p_type] = stock.current_price

        return portfolio

# ═══════════════════════════════════════════════════════════════════════
# RESIDUE RECYCLING INTERFACE
# ═══════════════════════════════════════════════════════════════════════

class ResidueRecyclingInterface:
    """User-friendly interface for residue economy"""

    def __init__(self, unified_economy: UnifiedMiningEconomy):
        self.unified = unified_economy

    def show_available_recipes(self) -> List[Dict[str, Any]]:
        """Show all available synthesis recipes"""
        recipes = []

        for name, recipe in self.unified.residue_economy.synthesis_recipes.items():
            recipes.append({
                "name": name,
                "inputs": recipe["inputs"],
                "outputs": recipe["output"],
                "description": self._describe_recipe(name)
            })

        return recipes

    def _describe_recipe(self, recipe_name: str) -> str:
        """Generate human-readable recipe description"""
        descriptions = {
            "PURE_ESSENCE": "Distill quantum and void residue into pure BloomCoin",
            "GUARDIAN_CRYSTAL": "Forge a crystal that enhances guardian alignment",
            "CHAOS_ORB": "Create an orb of pure chaos for market manipulation"
        }
        return descriptions.get(recipe_name, "Unknown recipe")

    def recycle_all_residue(self, player_id: str,
                           residue_inventory: Dict[str, float]) -> float:
        """Recycle all residue to BloomCoin"""

        total_bc = self.unified.residue_economy.recycle_residue(residue_inventory)

        # Add to wallet
        wallet = self.unified.wallet_manager.get_wallet_by_owner(player_id)
        if wallet:
            wallet.balance += total_bc

        print(f"♻️ Recycled residue into {total_bc:.2f} BC")
        return total_bc

    def auto_synthesize(self, player_id: str,
                       residue_inventory: Dict[str, float]) -> List[Dict]:
        """Automatically synthesize best recipes"""

        results = []

        # Try each recipe in order of value
        priority_recipes = ["GUARDIAN_CRYSTAL", "PURE_ESSENCE", "CHAOS_ORB"]

        for recipe_name in priority_recipes:
            result = self.unified.craft_with_residue(
                player_id, recipe_name, residue_inventory
            )
            if result:
                results.append({
                    "recipe": recipe_name,
                    "result": result
                })

        return results

# ═══════════════════════════════════════════════════════════════════════
# MARKET TRADING INTERFACE
# ═══════════════════════════════════════════════════════════════════════

class MarketTradingInterface:
    """Simplified interface for pattern stock trading"""

    def __init__(self, unified_economy: UnifiedMiningEconomy):
        self.unified = unified_economy

    def get_market_overview(self) -> Dict[str, Any]:
        """Get simplified market overview"""

        if not self.unified.stock_market.stocks:
            return {"error": "Market not initialized"}

        top_gainers = []
        top_losers = []

        for symbol, stock in self.unified.stock_market.stocks.items():
            change = ((stock.current_price - stock.opening_price) /
                     stock.opening_price * 100)

            stock_info = {
                "symbol": symbol,
                "price": stock.current_price,
                "change": change,
                "volume": stock.volume_24h,
                "trend": stock.trend.name if hasattr(stock.trend, 'name') else "UNKNOWN"
            }

            if change > 0:
                top_gainers.append(stock_info)
            else:
                top_losers.append(stock_info)

        # Sort by change
        top_gainers.sort(key=lambda x: x["change"], reverse=True)
        top_losers.sort(key=lambda x: x["change"])

        return {
            "total_stocks": len(self.unified.stock_market.stocks),
            "market_sentiment": self.unified._calculate_market_sentiment(),
            "top_gainers": top_gainers[:5],
            "top_losers": top_losers[:5]
        }

    def execute_market_order(self, player_id: str, symbol: str,
                            order_type: str, amount: float) -> bool:
        """Execute a simple market order"""

        return self.unified.trade_pattern_stock(
            player_id, symbol, order_type, amount
        )

    def get_recommended_trades(self, player_id: str) -> List[Dict]:
        """Get AI-recommended trades based on patterns owned"""

        recommendations = []
        patterns = self.unified.discovered_patterns.get(player_id, [])

        if not patterns:
            return recommendations

        # Analyze owned patterns
        owned_types = set(p.pattern_type.name for p in patterns)

        for symbol, stock in self.unified.stock_market.stocks.items():
            pattern_name = stock.pattern_type.name if hasattr(stock, 'pattern_type') else symbol

            # Recommend buying undervalued patterns we own
            if pattern_name in owned_types:
                if stock.current_price < stock.moving_average_30 * 0.95:
                    recommendations.append({
                        "action": "BUY",
                        "symbol": symbol,
                        "reason": "Undervalued pattern you already own",
                        "confidence": 0.8
                    })

            # Recommend selling overvalued patterns
            if stock.current_price > stock.moving_average_7 * 1.2:
                recommendations.append({
                    "action": "SELL",
                    "symbol": symbol,
                    "reason": "Overvalued, take profits",
                    "confidence": 0.7
                })

        return recommendations[:5]  # Top 5 recommendations

# ═══════════════════════════════════════════════════════════════════════
# UNIFIED GAME INTERFACE
# ═══════════════════════════════════════════════════════════════════════

class UnifiedGameInterface:
    """Single interface for all game systems to interact with economy"""

    def __init__(self):
        # Initialize unified economy
        self.economy = UnifiedMiningEconomy()

        # Initialize bridges and interfaces
        self.legacy_mining = LegacyMiningAdapter(self.economy)
        self.legacy_economy = LegacyEconomyBridge(self.economy)
        self.patterns = PatternSystemIntegration(self.economy)
        self.residue = ResidueRecyclingInterface(self.economy)
        self.market = MarketTradingInterface(self.economy)

        print("🌟 Unified Game Interface Ready")
        print("  All systems integrated and operational")

    def create_player(self, player_id: str, initial_balance: float = 100.0):
        """Create new player with all systems initialized"""

        # Create wallet
        wallet = self.economy.wallet_manager.create_wallet(
            f"Player_{player_id}",
            guardian="ECHO"  # Default guardian
        )
        wallet.balance = initial_balance

        # Create initial companion
        from companion_mining_ultimate import CompanionType

        companion = self.economy.companion_manager.create_companion(
            f"{player_id}_starter",
            CompanionType.ECHO
        )
        self.economy.companion_manager.companions[f"{player_id}_starter"] = companion

        print(f"✅ Player {player_id} created")
        print(f"  Wallet: {wallet.address}")
        print(f"  Balance: {initial_balance:.2f} BC")
        print(f"  Companion: {companion.name}")

        return {
            "player_id": player_id,
            "wallet": wallet,
            "companion": companion
        }

    def start_mining(self, player_id: str, companion_id: Optional[str] = None,
                    job_type: Optional[str] = None) -> Optional[UnifiedMiningJob]:
        """Simple mining start interface"""

        if companion_id is None:
            companion_id = f"{player_id}_starter"

        if job_type:
            # Convert string to enum
            try:
                job_enum = MiningJobType[job_type.upper()]
            except KeyError:
                job_enum = None
        else:
            job_enum = None

        return self.economy.create_mining_job(
            player_id=player_id,
            companion_id=companion_id,
            job_type=job_enum
        )

    def check_mining(self, job_id: str) -> Dict[str, Any]:
        """Check mining job status"""

        if job_id in self.economy.active_jobs:
            job = self.economy.active_jobs[job_id]
            elapsed = time.time() - job.start_time
            progress = min(1.0, elapsed / job.duration)

            return {
                "status": "active",
                "progress": progress,
                "elapsed": elapsed,
                "duration": job.duration,
                "estimated_reward": job.base_reward * job.market_multiplier
            }

        # Check completed
        for job in self.economy.completed_jobs:
            if job.job_id == job_id:
                return {
                    "status": "completed",
                    "success": job.success,
                    "reward": job.final_reward,
                    "patterns": [p.name for p in job.patterns_found],
                    "residue": job.total_residue,
                    "xp": job.xp_gained
                }

        return {"status": "not_found"}

    def get_player_stats(self, player_id: str) -> Dict[str, Any]:
        """Get comprehensive player statistics"""

        wallet = self.economy.wallet_manager.get_wallet_by_owner(player_id)
        patterns = self.patterns.get_pattern_portfolio(player_id)
        market_overview = self.market.get_market_overview()

        # Count companions
        companion_count = sum(
            1 for cid in self.economy.companion_manager.companions
            if player_id in cid
        )

        return {
            "wallet": {
                "balance": wallet.balance if wallet else 0,
                "address": wallet.address if wallet else None
            },
            "patterns": patterns,
            "companions": companion_count,
            "market_sentiment": market_overview["market_sentiment"],
            "economy": self.economy.get_economic_report()
        }

# ═══════════════════════════════════════════════════════════════════════
# MAIN DEMONSTRATION
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 80)
    print("ECONOMY INTEGRATION BRIDGE DEMONSTRATION")
    print("=" * 80)

    # Initialize unified interface
    game = UnifiedGameInterface()

    # Create test player
    player_data = game.create_player("test_player", 1000.0)

    # Start mining
    print("\n⛏️ Starting mining job...")
    job = game.start_mining("test_player", job_type="ECHO_RESONANCE")

    if job:
        print(f"Job started: {job.job_id}")

        # Simulate waiting
        print("Simulating mining (2 seconds)...")
        time.sleep(2)

        # Check status
        status = game.check_mining(job.job_id)
        print(f"Status: {status}")

        # Process mining
        game.economy.process_mining(job.job_id)

        # Check final status
        final_status = game.check_mining(job.job_id)
        print(f"\nFinal status: {final_status}")

    # Show player stats
    stats = game.get_player_stats("test_player")
    print("\n📊 Player Statistics:")
    print(f"Balance: {stats['wallet']['balance']:.2f} BC")
    print(f"Patterns: {stats['patterns']['total_patterns']}")
    print(f"Market Sentiment: {stats['market_sentiment']:.2f}x")

    # Show market overview
    market = game.market.get_market_overview()
    print("\n📈 Market Overview:")
    print(f"Total Stocks: {market['total_stocks']}")
    if market.get("top_gainers"):
        print(f"Top Gainer: {market['top_gainers'][0]['symbol']} "
              f"+{market['top_gainers'][0]['change']:.1f}%")

    print("\n✅ All systems integrated and operational!")