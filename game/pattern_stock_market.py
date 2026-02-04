"""
Pattern Stock Market System
===========================
Advanced farming system with stock market simulation and algorithmic solving
Patterns are traded as stocks with fluctuating values and algorithmic bonuses
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Callable
from enum import Enum
import random
import math
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict, deque
import hashlib

from guardian_pattern_recipes import PatternType

# ═══════════════════════════════════════════════════════════════════════
#   MARKET STRUCTURES
# ═══════════════════════════════════════════════════════════════════════

class MarketTrend(Enum):
    """Market trend states"""
    BULL_RUN = ("Bull Run", 1.5, "Prices surge upward")
    BULL = ("Bullish", 1.2, "Steady growth")
    NEUTRAL = ("Neutral", 1.0, "Sideways movement")
    BEAR = ("Bearish", 0.8, "Declining prices")
    CRASH = ("Market Crash", 0.5, "Severe downturn")
    BUBBLE = ("Bubble", 2.0, "Unsustainable growth")

class AlgorithmType(Enum):
    """Types of algorithms to solve for bonuses"""
    FIBONACCI = "Generate next Fibonacci sequence"
    PRIME_FACTORIZATION = "Find prime factors"
    HASH_COLLISION = "Find hash collision"
    PATTERN_MATCHING = "Match complex pattern"
    OPTIMIZATION = "Optimize portfolio allocation"
    PREDICTION = "Predict next market move"
    ARBITRAGE = "Find arbitrage opportunity"
    QUANTUM_STATE = "Calculate quantum state"
    FRACTAL_GENERATION = "Generate fractal pattern"
    CIPHER_BREAKING = "Break encryption cipher"

class InvestmentStrategy(Enum):
    """Investment strategies for pattern stocks"""
    HODL = "Hold long term"
    DAY_TRADING = "Buy and sell within cycles"
    SWING_TRADING = "Ride market swings"
    ARBITRAGE = "Exploit price differences"
    OPTIONS = "Trade pattern options"
    FUTURES = "Trade pattern futures"
    MARGIN = "Leveraged trading"
    SHORT_SELLING = "Bet against patterns"
    ALGO_TRADING = "Algorithmic trading"
    INDEX_FUND = "Diversified portfolio"

@dataclass
class PatternStock:
    """A pattern treated as a tradeable stock"""
    symbol: str  # e.g., "ECHO", "QNTM", "VOID"
    pattern_type: PatternType
    current_price: float
    opening_price: float
    high_24h: float
    low_24h: float
    volume_24h: int
    market_cap: float
    volatility: float  # 0.0 to 1.0
    trend: MarketTrend
    price_history: deque = field(default_factory=lambda: deque(maxlen=100))

    # Technical indicators
    moving_average_7: float = 0.0
    moving_average_30: float = 0.0
    rsi: float = 50.0  # Relative Strength Index
    bollinger_upper: float = 0.0
    bollinger_lower: float = 0.0

    # Algorithmic modifiers
    algorithm_bonus: float = 1.0
    solved_algorithms: List[AlgorithmType] = field(default_factory=list)

    def update_price(self, new_price: float):
        """Update stock price and technical indicators"""
        self.price_history.append(self.current_price)
        self.current_price = new_price

        # Update 24h high/low
        if new_price > self.high_24h:
            self.high_24h = new_price
        if new_price < self.low_24h:
            self.low_24h = new_price

        # Update moving averages
        if len(self.price_history) >= 7:
            self.moving_average_7 = np.mean(list(self.price_history)[-7:])
        if len(self.price_history) >= 30:
            self.moving_average_30 = np.mean(list(self.price_history)[-30:])

        # Update RSI
        self._update_rsi()

        # Update Bollinger Bands
        self._update_bollinger_bands()

    def _update_rsi(self):
        """Calculate Relative Strength Index"""
        if len(self.price_history) < 14:
            return

        gains = []
        losses = []
        for i in range(1, min(14, len(self.price_history))):
            change = self.price_history[i] - self.price_history[i-1]
            if change > 0:
                gains.append(change)
            else:
                losses.append(abs(change))

        if gains and losses:
            avg_gain = np.mean(gains) if gains else 0
            avg_loss = np.mean(losses) if losses else 0

            if avg_loss > 0:
                rs = avg_gain / avg_loss
                self.rsi = 100 - (100 / (1 + rs))
            else:
                self.rsi = 100 if avg_gain > 0 else 50

    def _update_bollinger_bands(self):
        """Calculate Bollinger Bands"""
        if len(self.price_history) >= 20:
            prices = list(self.price_history)[-20:]
            ma20 = np.mean(prices)
            std20 = np.std(prices)

            self.bollinger_upper = ma20 + (std20 * 2)
            self.bollinger_lower = ma20 - (std20 * 2)

    def calculate_rsi(self) -> float:
        """Get current RSI value"""
        return self.rsi

    def calculate_bollinger_bands(self) -> dict:
        """Get current Bollinger Bands"""
        if len(self.price_history) >= 20:
            prices = list(self.price_history)[-20:]
            middle = np.mean(prices)
        else:
            middle = self.current_price

        return {
            "upper": self.bollinger_upper if self.bollinger_upper > 0 else middle * 1.02,
            "middle": middle,
            "lower": self.bollinger_lower if self.bollinger_lower > 0 else middle * 0.98
        }

    def calculate_moving_averages(self) -> dict:
        """Get moving averages"""
        return {
            "MA7": self.moving_average_7 if self.moving_average_7 > 0 else self.current_price,
            "MA30": self.moving_average_30 if self.moving_average_30 > 0 else self.current_price
        }

@dataclass
class MarketOrder:
    """An order in the pattern stock market"""
    order_id: str
    player_id: str
    stock_symbol: str
    order_type: str  # "buy", "sell", "short", "cover"
    quantity: int
    price: float
    timestamp: datetime
    strategy: InvestmentStrategy
    leverage: float = 1.0  # For margin trading
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None

@dataclass
class Portfolio:
    """Player's investment portfolio"""
    player_id: str
    cash_balance: float
    holdings: Dict[str, int] = field(default_factory=dict)  # symbol -> quantity
    short_positions: Dict[str, int] = field(default_factory=dict)
    orders: List[MarketOrder] = field(default_factory=list)
    realized_gains: float = 0.0
    unrealized_gains: float = 0.0
    total_invested: float = 0.0
    algorithm_solutions: Dict[AlgorithmType, int] = field(default_factory=dict)
    strategy_performance: Dict[InvestmentStrategy, float] = field(default_factory=dict)

# ═══════════════════════════════════════════════════════════════════════
#   ALGORITHMIC CHALLENGES
# ═══════════════════════════════════════════════════════════════════════

class AlgorithmicChallenge:
    """Algorithmic puzzles that provide market bonuses"""

    @staticmethod
    def generate_challenge(algo_type: AlgorithmType, difficulty: int = 1) -> Dict[str, Any]:
        """Generate an algorithmic challenge"""
        generators = {
            AlgorithmType.FIBONACCI: AlgorithmicChallenge._fibonacci_challenge,
            AlgorithmType.PRIME_FACTORIZATION: AlgorithmicChallenge._prime_factor_challenge,
            AlgorithmType.HASH_COLLISION: AlgorithmicChallenge._hash_collision_challenge,
            AlgorithmType.PATTERN_MATCHING: AlgorithmicChallenge._pattern_match_challenge,
            AlgorithmType.OPTIMIZATION: AlgorithmicChallenge._optimization_challenge,
            AlgorithmType.PREDICTION: AlgorithmicChallenge._prediction_challenge,
            AlgorithmType.ARBITRAGE: AlgorithmicChallenge._arbitrage_challenge,
            AlgorithmType.QUANTUM_STATE: AlgorithmicChallenge._quantum_state_challenge,
            AlgorithmType.FRACTAL_GENERATION: AlgorithmicChallenge._fractal_challenge,
            AlgorithmType.CIPHER_BREAKING: AlgorithmicChallenge._cipher_challenge
        }

        generator = generators.get(algo_type, AlgorithmicChallenge._default_challenge)
        return generator(difficulty)

    @staticmethod
    def _fibonacci_challenge(difficulty: int) -> Dict[str, Any]:
        """Generate Fibonacci sequence challenge"""
        start = random.randint(1, 10 * difficulty)
        length = 5 + difficulty * 2

        # Generate the sequence
        sequence = [start, start]
        for i in range(2, length):
            sequence.append(sequence[i-1] + sequence[i-2])

        # Hide some numbers
        hidden_indices = random.sample(range(2, length), min(difficulty + 1, length - 2))
        challenge_sequence = sequence.copy()
        for idx in hidden_indices:
            challenge_sequence[idx] = None

        return {
            "type": AlgorithmType.FIBONACCI,
            "description": f"Complete the Fibonacci sequence: {challenge_sequence}",
            "challenge_data": challenge_sequence,
            "solution": sequence,
            "reward_multiplier": 1.0 + (0.1 * difficulty),
            "time_limit": 60 - (difficulty * 5)
        }

    @staticmethod
    def _prime_factor_challenge(difficulty: int) -> Dict[str, Any]:
        """Generate prime factorization challenge"""
        # Generate a composite number based on difficulty
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        num_factors = min(2 + difficulty, 5)
        factors = random.sample(primes[:5 + difficulty], num_factors)

        number = 1
        for factor in factors:
            number *= factor ** random.randint(1, min(2, difficulty))

        return {
            "type": AlgorithmType.PRIME_FACTORIZATION,
            "description": f"Find all prime factors of {number}",
            "challenge_data": number,
            "solution": sorted(factors),
            "reward_multiplier": 1.0 + (0.15 * difficulty),
            "time_limit": 90 - (difficulty * 10)
        }

    @staticmethod
    def _hash_collision_challenge(difficulty: int) -> Dict[str, Any]:
        """Generate hash collision challenge"""
        target_hash = hashlib.md5(str(random.randint(0, 1000)).encode()).hexdigest()[:4 + difficulty]

        return {
            "type": AlgorithmType.HASH_COLLISION,
            "description": f"Find a string that produces hash starting with: {target_hash}",
            "challenge_data": target_hash,
            "solution": None,  # Multiple valid solutions
            "reward_multiplier": 1.0 + (0.2 * difficulty),
            "time_limit": 120
        }

    @staticmethod
    def _pattern_match_challenge(difficulty: int) -> Dict[str, Any]:
        """Generate pattern matching challenge"""
        patterns = {
            1: ["ABAB", "1221", "XYYX"],
            2: ["ABCABC", "123321", "XYZXYZ"],
            3: ["ABCDABCD", "12344321", "XYZWXYZW"]
        }

        pattern_set = patterns.get(min(difficulty, 3), patterns[1])
        pattern = random.choice(pattern_set)

        # Create partial pattern
        mask_count = min(len(pattern) // 3, difficulty + 1)
        masked = list(pattern)
        for _ in range(mask_count):
            idx = random.randint(0, len(pattern) - 1)
            masked[idx] = '?'

        return {
            "type": AlgorithmType.PATTERN_MATCHING,
            "description": f"Complete the pattern: {''.join(masked)}",
            "challenge_data": ''.join(masked),
            "solution": pattern,
            "reward_multiplier": 1.0 + (0.12 * difficulty),
            "time_limit": 45
        }

    @staticmethod
    def _optimization_challenge(difficulty: int) -> Dict[str, Any]:
        """Generate portfolio optimization challenge"""
        num_stocks = 3 + difficulty
        stocks = []

        for i in range(num_stocks):
            stocks.append({
                "symbol": f"STK{i}",
                "expected_return": random.uniform(0.05, 0.25),
                "risk": random.uniform(0.1, 0.4),
                "price": random.uniform(10, 100)
            })

        budget = 1000 * difficulty
        target_return = random.uniform(0.1, 0.2)

        return {
            "type": AlgorithmType.OPTIMIZATION,
            "description": f"Optimize portfolio with budget {budget} for {target_return:.1%} return",
            "challenge_data": {
                "stocks": stocks,
                "budget": budget,
                "target_return": target_return
            },
            "solution": None,  # Multiple valid solutions
            "reward_multiplier": 1.0 + (0.18 * difficulty),
            "time_limit": 90
        }

    @staticmethod
    def _prediction_challenge(difficulty: int) -> Dict[str, Any]:
        """Generate market prediction challenge"""
        # Generate price history
        history = [100.0]
        trend = random.choice([0.01, -0.01, 0.02, -0.02])

        for _ in range(20 + difficulty * 5):
            noise = random.uniform(-2, 2)
            next_price = history[-1] * (1 + trend) + noise
            history.append(max(50, min(150, next_price)))

        # Predict next 3 prices
        return {
            "type": AlgorithmType.PREDICTION,
            "description": f"Predict next 3 prices based on history",
            "challenge_data": history[:-3],
            "solution": history[-3:],  # Approximate solution
            "reward_multiplier": 1.0 + (0.15 * difficulty),
            "time_limit": 60,
            "tolerance": 5.0  # Price tolerance for correctness
        }

    @staticmethod
    def _arbitrage_challenge(difficulty: int) -> Dict[str, Any]:
        """Generate arbitrage opportunity challenge"""
        exchanges = ["Exchange A", "Exchange B", "Exchange C"]

        # Create price discrepancies
        prices = {}
        for exchange in exchanges[:2 + difficulty]:
            prices[exchange] = {}
            for symbol in ["ECHO", "QNTM", "VOID"]:
                base_price = random.uniform(50, 150)
                prices[exchange][symbol] = base_price * random.uniform(0.95, 1.05)

        return {
            "type": AlgorithmType.ARBITRAGE,
            "description": "Find and exploit arbitrage opportunity",
            "challenge_data": prices,
            "solution": None,  # Calculate best arbitrage path
            "reward_multiplier": 1.0 + (0.25 * difficulty),
            "time_limit": 30
        }

    @staticmethod
    def _quantum_state_challenge(difficulty: int) -> Dict[str, Any]:
        """Generate quantum state calculation challenge"""
        # Simplified quantum state problem
        qubits = 2 + difficulty
        initial_state = [complex(random.random(), random.random()) for _ in range(2**qubits)]

        # Normalize
        norm = sum(abs(x)**2 for x in initial_state) ** 0.5
        initial_state = [x/norm for x in initial_state]

        return {
            "type": AlgorithmType.QUANTUM_STATE,
            "description": f"Calculate probability of measuring |0⟩ in {qubits}-qubit system",
            "challenge_data": {
                "qubits": qubits,
                "state": [str(x) for x in initial_state]
            },
            "solution": abs(initial_state[0])**2,
            "reward_multiplier": 1.0 + (0.3 * difficulty),
            "time_limit": 120,
            "tolerance": 0.01
        }

    @staticmethod
    def _fractal_challenge(difficulty: int) -> Dict[str, Any]:
        """Generate fractal pattern challenge"""
        iterations = 3 + difficulty

        # Simplified fractal generation
        fractal_rules = {
            "A": "AB",
            "B": "A"
        }

        start = "A"
        for _ in range(iterations - 1):
            next_iter = ""
            for char in start:
                next_iter += fractal_rules.get(char, char)
            start = next_iter

        # Hide parts
        masked = list(start)
        for _ in range(difficulty + 1):
            if len(start) > 0:
                idx = random.randint(0, len(start) - 1)
                masked[idx] = '?'

        return {
            "type": AlgorithmType.FRACTAL_GENERATION,
            "description": f"Complete the L-system fractal: {''.join(masked)}",
            "challenge_data": ''.join(masked),
            "solution": start,
            "reward_multiplier": 1.0 + (0.2 * difficulty),
            "time_limit": 60
        }

    @staticmethod
    def _cipher_challenge(difficulty: int) -> Dict[str, Any]:
        """Generate cipher breaking challenge"""
        # Caesar cipher with shift
        shift = random.randint(1, 25)
        messages = [
            "PATTERN MARKET BULL",
            "VOID STOCKS RISING",
            "QUANTUM YIELDS HIGH",
            "ECHO DIVIDENDS PAID"
        ]

        message = random.choice(messages)

        # Encrypt
        encrypted = ""
        for char in message:
            if char.isalpha():
                shifted = ord(char) - ord('A')
                shifted = (shifted + shift) % 26
                encrypted += chr(shifted + ord('A'))
            else:
                encrypted += char

        return {
            "type": AlgorithmType.CIPHER_BREAKING,
            "description": f"Decrypt the message: {encrypted}",
            "challenge_data": encrypted,
            "solution": message,
            "reward_multiplier": 1.0 + (0.15 * difficulty),
            "time_limit": 90
        }

    @staticmethod
    def _default_challenge(difficulty: int) -> Dict[str, Any]:
        """Default challenge if type not found"""
        return {
            "type": None,
            "description": "Solve the puzzle",
            "challenge_data": None,
            "solution": None,
            "reward_multiplier": 1.0,
            "time_limit": 60
        }

# ═══════════════════════════════════════════════════════════════════════
#   PATTERN STOCK MARKET ENGINE
# ═══════════════════════════════════════════════════════════════════════

class PatternStockMarket:
    """Main stock market simulation for pattern farming"""

    def __init__(self):
        self.stocks: Dict[str, PatternStock] = self._initialize_stocks()
        self.portfolios: Dict[str, Portfolio] = {}
        self.order_book: List[MarketOrder] = []
        self.market_trend = MarketTrend.NEUTRAL
        self.market_events: deque = deque(maxlen=50)
        self.global_multiplier = 1.0
        self.tick = 0

        # Market metrics
        self.total_volume = 0
        self.total_market_cap = 0
        self.market_index = 1000.0  # Pattern Market Index (PMI)
        self.volatility_index = 50.0  # Pattern Volatility Index (PVI)

    def _initialize_stocks(self) -> Dict[str, PatternStock]:
        """Initialize pattern stocks"""
        stocks = {}

        pattern_configs = [
            ("ECHO", PatternType.RESONANCE, 100.0, 0.3),
            ("QNTM", PatternType.QUANTUM, 150.0, 0.5),
            ("VOID", PatternType.VOID, 120.0, 0.4),
            ("CHAO", PatternType.CHAOS, 80.0, 0.7),
            ("ORGN", PatternType.ORGANIC, 90.0, 0.2),
            ("CRYS", PatternType.CRYSTALLINE, 110.0, 0.25),
            ("TEMP", PatternType.TEMPORAL, 130.0, 0.35),
            ("ELEM", PatternType.ELEMENTAL, 95.0, 0.3),
            ("HARM", PatternType.HARMONIC, 105.0, 0.28),
            ("MEMR", PatternType.MEMORY, 115.0, 0.32)
        ]

        for symbol, pattern_type, base_price, volatility in pattern_configs:
            stock = PatternStock(
                symbol=symbol,
                pattern_type=pattern_type,
                current_price=base_price,
                opening_price=base_price,
                high_24h=base_price,
                low_24h=base_price,
                volume_24h=0,
                market_cap=base_price * 1000000,
                volatility=volatility,
                trend=MarketTrend.NEUTRAL
            )
            stocks[symbol] = stock

        return stocks

    def create_portfolio(self, player_id: str, initial_balance: float) -> Portfolio:
        """Create a new portfolio for a player"""
        portfolio = Portfolio(
            player_id=player_id,
            cash_balance=initial_balance,
            total_invested=initial_balance
        )
        self.portfolios[player_id] = portfolio
        return portfolio

    def tick_market(self) -> Dict[str, Any]:
        """Process one market tick"""
        self.tick += 1

        # Update market trend
        if self.tick % 10 == 0:
            self._update_market_trend()

        # Process each stock
        for symbol, stock in self.stocks.items():
            self._update_stock_price(stock)

        # Process orders
        self._process_orders()

        # Update portfolios
        self._update_portfolios()

        # Generate market events
        if random.random() < 0.1:
            event = self._generate_market_event()
            self.market_events.append(event)

        # Update market indices
        self._update_market_indices()

        return {
            "tick": self.tick,
            "market_trend": self.market_trend.value[0],
            "market_index": self.market_index,
            "volatility_index": self.volatility_index,
            "events": list(self.market_events)[-5:]
        }

    def _update_stock_price(self, stock: PatternStock):
        """Update individual stock price"""
        # Base price movement
        trend_multiplier = self.market_trend.value[1]
        volatility_factor = random.gauss(0, stock.volatility)

        # Technical analysis influence
        ma_influence = 0
        if stock.moving_average_7 > 0:
            if stock.current_price > stock.moving_average_7:
                ma_influence = 0.01  # Upward pressure
            else:
                ma_influence = -0.01  # Downward pressure

        # RSI influence
        rsi_influence = 0
        if stock.rsi > 70:
            rsi_influence = -0.02  # Overbought, likely to fall
        elif stock.rsi < 30:
            rsi_influence = 0.02  # Oversold, likely to rise

        # Bollinger band influence
        bb_influence = 0
        if stock.bollinger_upper > 0 and stock.current_price > stock.bollinger_upper:
            bb_influence = -0.03  # Likely to revert
        elif stock.bollinger_lower > 0 and stock.current_price < stock.bollinger_lower:
            bb_influence = 0.03  # Likely to bounce

        # Algorithm bonus influence
        algo_influence = (stock.algorithm_bonus - 1.0) * 0.1

        # Calculate price change
        price_change = (
            volatility_factor * 0.02 +
            ma_influence +
            rsi_influence +
            bb_influence +
            algo_influence
        ) * trend_multiplier * self.global_multiplier

        # Apply price change
        new_price = stock.current_price * (1 + price_change)
        new_price = max(1.0, new_price)  # Minimum price floor

        # Random events
        if random.random() < 0.01:  # 1% chance of major event
            if random.random() < 0.5:
                new_price *= random.uniform(1.1, 1.3)  # Pump
                self.market_events.append(f"{stock.symbol} surges {((new_price/stock.current_price)-1)*100:.1f}%!")
            else:
                new_price *= random.uniform(0.7, 0.9)  # Dump
                self.market_events.append(f"{stock.symbol} crashes {(1-(new_price/stock.current_price))*100:.1f}%!")

        stock.update_price(new_price)

    def _update_market_trend(self):
        """Update overall market trend"""
        # Calculate market momentum
        total_rsi = sum(stock.rsi for stock in self.stocks.values())
        avg_rsi = total_rsi / len(self.stocks) if self.stocks else 50

        # Determine new trend based on momentum
        if avg_rsi > 70:
            if self.market_trend == MarketTrend.BULL:
                self.market_trend = MarketTrend.BUBBLE
            else:
                self.market_trend = MarketTrend.BULL
        elif avg_rsi > 55:
            self.market_trend = MarketTrend.BULL
        elif avg_rsi > 45:
            self.market_trend = MarketTrend.NEUTRAL
        elif avg_rsi > 30:
            self.market_trend = MarketTrend.BEAR
        else:
            if self.market_trend == MarketTrend.BEAR:
                self.market_trend = MarketTrend.CRASH
            else:
                self.market_trend = MarketTrend.BEAR

        # Random major events
        if random.random() < 0.05:
            events = [
                (MarketTrend.BULL_RUN, "📈 Bull run begins! Pattern yields soar!"),
                (MarketTrend.CRASH, "📉 Market crash! Panic selling ensues!"),
                (MarketTrend.BUBBLE, "🫧 Bubble warning! Unsustainable growth detected!")
            ]
            event = random.choice(events)
            self.market_trend = event[0]
            self.market_events.append(event[1])

    def _process_orders(self):
        """Process pending orders"""
        for order in self.order_book[:]:  # Copy to avoid modification during iteration
            stock = self.stocks.get(order.stock_symbol)
            if not stock:
                continue

            portfolio = self.portfolios.get(order.player_id)
            if not portfolio:
                continue

            # Check stop loss
            if order.stop_loss and stock.current_price <= order.stop_loss:
                self._execute_order(order, portfolio, stock, "stop_loss")
                self.order_book.remove(order)

            # Check take profit
            elif order.take_profit and stock.current_price >= order.take_profit:
                self._execute_order(order, portfolio, stock, "take_profit")
                self.order_book.remove(order)

            # Market order execution
            elif abs(stock.current_price - order.price) < stock.current_price * 0.01:
                self._execute_order(order, portfolio, stock, "market")
                self.order_book.remove(order)

    def _execute_order(self, order: MarketOrder, portfolio: Portfolio,
                      stock: PatternStock, execution_type: str):
        """Execute a market order"""
        total_cost = order.quantity * stock.current_price * order.leverage

        if order.order_type == "buy":
            if portfolio.cash_balance >= total_cost:
                portfolio.cash_balance -= total_cost
                portfolio.holdings[order.stock_symbol] = portfolio.holdings.get(order.stock_symbol, 0) + order.quantity
                stock.volume_24h += order.quantity

        elif order.order_type == "sell":
            if portfolio.holdings.get(order.stock_symbol, 0) >= order.quantity:
                portfolio.cash_balance += total_cost
                portfolio.holdings[order.stock_symbol] -= order.quantity
                stock.volume_24h += order.quantity

                # Calculate realized gains
                cost_basis = order.price * order.quantity
                sale_value = stock.current_price * order.quantity
                portfolio.realized_gains += (sale_value - cost_basis)

        elif order.order_type == "short":
            # Short selling
            portfolio.short_positions[order.stock_symbol] = portfolio.short_positions.get(order.stock_symbol, 0) + order.quantity
            portfolio.cash_balance += total_cost

        elif order.order_type == "cover":
            # Covering short position
            if portfolio.short_positions.get(order.stock_symbol, 0) >= order.quantity:
                portfolio.short_positions[order.stock_symbol] -= order.quantity
                portfolio.cash_balance -= total_cost

    def _update_portfolios(self):
        """Update portfolio values"""
        for portfolio in self.portfolios.values():
            # Calculate unrealized gains
            unrealized = 0
            for symbol, quantity in portfolio.holdings.items():
                if symbol in self.stocks:
                    current_value = self.stocks[symbol].current_price * quantity
                    # Assuming average cost basis for simplicity
                    cost_basis = 100 * quantity  # Would track actual in production
                    unrealized += (current_value - cost_basis)

            portfolio.unrealized_gains = unrealized

    def _generate_market_event(self) -> str:
        """Generate random market events"""
        events = [
            "🔮 Quantum patterns show unusual activity",
            "🌊 Echo resonance detected in market",
            "🕳️ Void patterns absorbing excess liquidity",
            "🔥 Chaos indicators spike unexpectedly",
            "💎 Crystal patterns forming support level",
            "🌱 Organic growth detected in farming yields",
            "⏰ Temporal anomaly affects trading algorithms",
            "🎵 Harmonic convergence in price action",
            "💾 Memory patterns suggest historical repeat",
            "⚡ Elemental volatility surge incoming"
        ]

        return random.choice(events)

    def _update_market_indices(self):
        """Update market-wide indices"""
        # Calculate Pattern Market Index (PMI)
        total_cap = sum(stock.current_price * 1000000 for stock in self.stocks.values())
        base_cap = len(self.stocks) * 100 * 1000000  # Base market cap
        self.market_index = 1000 * (total_cap / base_cap)

        # Calculate Pattern Volatility Index (PVI)
        avg_volatility = sum(stock.volatility for stock in self.stocks.values()) / len(self.stocks)
        self.volatility_index = avg_volatility * 100

        self.total_market_cap = total_cap
        self.total_volume = sum(stock.volume_24h for stock in self.stocks.values())

    def place_order(self, player_id: str, order: MarketOrder) -> Dict[str, Any]:
        """Place a market order"""
        portfolio = self.portfolios.get(player_id)
        if not portfolio:
            return {"success": False, "error": "Portfolio not found"}

        stock = self.stocks.get(order.stock_symbol)
        if not stock:
            return {"success": False, "error": "Stock not found"}

        # Validate order
        if order.order_type == "buy":
            required_balance = order.quantity * order.price * order.leverage
            if portfolio.cash_balance < required_balance:
                return {"success": False, "error": "Insufficient funds"}

        elif order.order_type == "sell":
            if portfolio.holdings.get(order.stock_symbol, 0) < order.quantity:
                return {"success": False, "error": "Insufficient holdings"}

        # Add to order book
        self.order_book.append(order)
        portfolio.orders.append(order)

        return {
            "success": True,
            "order_id": order.order_id,
            "message": f"Order placed: {order.order_type} {order.quantity} {order.stock_symbol} @ {order.price}"
        }

    def solve_algorithm(self, player_id: str, algo_type: AlgorithmType,
                       solution: Any) -> Dict[str, Any]:
        """Solve an algorithmic challenge for bonuses"""
        portfolio = self.portfolios.get(player_id)
        if not portfolio:
            return {"success": False, "error": "Portfolio not found"}

        # Generate challenge
        difficulty = portfolio.algorithm_solutions.get(algo_type, 0) + 1
        challenge = AlgorithmicChallenge.generate_challenge(algo_type, difficulty)

        # Check solution
        correct = False
        if challenge["solution"] is not None:
            if "tolerance" in challenge:
                # Numerical solution with tolerance
                correct = abs(solution - challenge["solution"]) <= challenge["tolerance"]
            else:
                # Exact match
                correct = solution == challenge["solution"]
        else:
            # Open-ended challenge - validate format/feasibility
            correct = self._validate_open_solution(algo_type, solution, challenge["challenge_data"])

        if correct:
            # Apply bonus
            portfolio.algorithm_solutions[algo_type] = difficulty
            reward_mult = challenge["reward_multiplier"]

            # Apply bonus to relevant stocks
            bonus_applied = []
            for symbol, stock in self.stocks.items():
                if self._algorithm_affects_stock(algo_type, stock.pattern_type):
                    stock.algorithm_bonus = min(3.0, stock.algorithm_bonus * reward_mult)
                    stock.solved_algorithms.append(algo_type)
                    bonus_applied.append(symbol)

            return {
                "success": True,
                "algorithm": algo_type.value,
                "difficulty": difficulty,
                "reward_multiplier": reward_mult,
                "stocks_affected": bonus_applied,
                "message": f"Algorithm solved! {reward_mult:.1%} bonus applied"
            }
        else:
            return {
                "success": False,
                "error": "Incorrect solution",
                "hint": challenge.get("hint", "Try again")
            }

    def _validate_open_solution(self, algo_type: AlgorithmType, solution: Any,
                               challenge_data: Any) -> bool:
        """Validate open-ended algorithmic solutions"""
        if algo_type == AlgorithmType.OPTIMIZATION:
            # Check if portfolio allocation is valid
            if isinstance(solution, dict):
                total_spent = sum(solution.values())
                budget = challenge_data.get("budget", 0)
                return total_spent <= budget

        elif algo_type == AlgorithmType.ARBITRAGE:
            # Check if arbitrage path exists
            if isinstance(solution, list) and len(solution) >= 2:
                return True  # Simplified validation

        elif algo_type == AlgorithmType.HASH_COLLISION:
            # Check if hash matches
            if isinstance(solution, str):
                hash_result = hashlib.md5(solution.encode()).hexdigest()
                return hash_result.startswith(challenge_data)

        return False

    def _algorithm_affects_stock(self, algo_type: AlgorithmType, pattern_type: PatternType) -> bool:
        """Determine if algorithm type affects specific pattern stock"""
        relationships = {
            AlgorithmType.FIBONACCI: [PatternType.ORGANIC, PatternType.HARMONIC],
            AlgorithmType.PRIME_FACTORIZATION: [PatternType.CRYSTALLINE],
            AlgorithmType.HASH_COLLISION: [PatternType.MEMORY],
            AlgorithmType.PATTERN_MATCHING: [PatternType.RESONANCE],
            AlgorithmType.OPTIMIZATION: [PatternType.ELEMENTAL],
            AlgorithmType.PREDICTION: [PatternType.TEMPORAL],
            AlgorithmType.ARBITRAGE: [PatternType.CHAOS],
            AlgorithmType.QUANTUM_STATE: [PatternType.QUANTUM],
            AlgorithmType.FRACTAL_GENERATION: [PatternType.ORGANIC],
            AlgorithmType.CIPHER_BREAKING: [PatternType.VOID]
        }

        affected_types = relationships.get(algo_type, [])
        return pattern_type in affected_types

# ═══════════════════════════════════════════════════════════════════════
#   FARMING INTEGRATION
# ═══════════════════════════════════════════════════════════════════════

class StockMarketFarming:
    """Integration between stock market and farming system"""

    def __init__(self, market: PatternStockMarket):
        self.market = market
        self.farm_investments: Dict[str, Dict[str, float]] = defaultdict(dict)

    def invest_in_farm(self, player_id: str, pattern_type: PatternType, amount: float) -> Dict[str, Any]:
        """Invest in pattern farming with stock market mechanics"""
        portfolio = self.market.portfolios.get(player_id)
        if not portfolio:
            return {"success": False, "error": "No portfolio found"}

        if portfolio.cash_balance < amount:
            return {"success": False, "error": "Insufficient funds"}

        # Find corresponding stock
        stock_symbol = self._pattern_to_stock(pattern_type)
        stock = self.market.stocks.get(stock_symbol)

        if not stock:
            return {"success": False, "error": "Stock not found for pattern type"}

        # Calculate shares based on current price
        shares = amount / stock.current_price

        # Deduct from portfolio
        portfolio.cash_balance -= amount

        # Add to farm investment
        farm_key = f"{player_id}:{pattern_type.value}"
        self.farm_investments[farm_key] = {
            "invested_amount": amount,
            "shares": shares,
            "entry_price": stock.current_price,
            "timestamp": datetime.now()
        }

        return {
            "success": True,
            "pattern_type": pattern_type.value,
            "amount_invested": amount,
            "shares_acquired": shares,
            "current_price": stock.current_price,
            "message": f"Invested {amount} in {pattern_type.value} farming"
        }

    def calculate_farming_yield(self, player_id: str, pattern_type: PatternType) -> Dict[str, Any]:
        """Calculate farming yield based on stock performance"""
        farm_key = f"{player_id}:{pattern_type.value}"
        investment = self.farm_investments.get(farm_key)

        if not investment:
            return {"success": False, "error": "No investment found"}

        stock_symbol = self._pattern_to_stock(pattern_type)
        stock = self.market.stocks.get(stock_symbol)

        if not stock:
            return {"success": False, "error": "Stock not found"}

        # Calculate returns
        current_value = investment["shares"] * stock.current_price
        invested_amount = investment["invested_amount"]
        profit = current_value - invested_amount
        roi = (profit / invested_amount) * 100 if invested_amount > 0 else 0

        # Apply algorithm bonuses
        algorithm_bonus = stock.algorithm_bonus

        # Calculate pattern yield
        base_yield = int(investment["shares"] * 10)  # Base patterns per share
        market_multiplier = self.market.market_trend.value[1]
        final_yield = int(base_yield * market_multiplier * algorithm_bonus)

        # Special bonuses for strategies
        portfolio = self.market.portfolios.get(player_id)
        if portfolio:
            if InvestmentStrategy.HODL in portfolio.strategy_performance:
                if (datetime.now() - investment["timestamp"]).days > 7:
                    final_yield = int(final_yield * 1.5)  # Long-term holding bonus

        return {
            "success": True,
            "pattern_type": pattern_type.value,
            "invested_amount": invested_amount,
            "current_value": current_value,
            "profit": profit,
            "roi_percent": roi,
            "pattern_yield": final_yield,
            "market_trend": self.market.market_trend.value[0],
            "algorithm_bonus": algorithm_bonus,
            "stock_price": stock.current_price
        }

    def _pattern_to_stock(self, pattern_type: PatternType) -> str:
        """Map pattern type to stock symbol"""
        mapping = {
            PatternType.RESONANCE: "ECHO",
            PatternType.QUANTUM: "QNTM",
            PatternType.VOID: "VOID",
            PatternType.CHAOS: "CHAO",
            PatternType.ORGANIC: "ORGN",
            PatternType.CRYSTALLINE: "CRYS",
            PatternType.TEMPORAL: "TEMP",
            PatternType.ELEMENTAL: "ELEM",
            PatternType.HARMONIC: "HARM",
            PatternType.MEMORY: "MEMR"
        }
        return mapping.get(pattern_type, "ECHO")

if __name__ == "__main__":
    # Demo the system
    market = PatternStockMarket()
    farming = StockMarketFarming(market)

    # Create player portfolio
    player_id = "test_player"
    portfolio = market.create_portfolio(player_id, 10000)

    print("=" * 60)
    print("PATTERN STOCK MARKET DEMONSTRATION")
    print("=" * 60)

    # Show initial stocks
    print("\nInitial Stock Prices:")
    for symbol, stock in market.stocks.items():
        print(f"  {symbol}: ${stock.current_price:.2f} ({stock.pattern_type.value})")

    # Simulate market ticks
    print("\nSimulating market...")
    for i in range(5):
        result = market.tick_market()
        print(f"\nTick {result['tick']}: {result['market_trend']} | PMI: {result['market_index']:.1f}")
        if result['events']:
            print(f"  Events: {result['events'][-1]}")

    # Solve an algorithm
    print("\nSolving Fibonacci Algorithm...")
    algo_result = market.solve_algorithm(player_id, AlgorithmType.FIBONACCI, [1, 1, 2, 3, 5, 8, 13, 21])
    print(f"  Result: {algo_result['message'] if algo_result['success'] else algo_result['error']}")

    # Invest in farming
    print("\nInvesting in Pattern Farming...")
    farm_result = farming.invest_in_farm(player_id, PatternType.QUANTUM, 1000)
    print(f"  {farm_result['message'] if farm_result['success'] else farm_result['error']}")

    # Calculate yield
    yield_result = farming.calculate_farming_yield(player_id, PatternType.QUANTUM)
    if yield_result['success']:
        print(f"  Pattern Yield: {yield_result['pattern_yield']} patterns")
        print(f"  ROI: {yield_result['roi_percent']:.1f}%")

    print("\n" + "=" * 60)