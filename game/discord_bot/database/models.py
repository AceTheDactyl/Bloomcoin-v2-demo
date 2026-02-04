"""
Database Models - SQLAlchemy ORM Models
========================================
Database schema for BloomQuest Discord Bot
"""

from sqlalchemy import (
    Column, Integer, BigInteger, String, Float, Boolean,
    DateTime, ForeignKey, Index, JSON, Enum, Text, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()

# Enumerations
class CompanionType(enum.Enum):
    ECHO = "Echo"
    GLITCH = "Glitch"
    FLOW = "Flow"
    SPARK = "Spark"
    SAGE = "Sage"
    SCOUT = "Scout"
    NULL = "Null"

class PatternType(enum.Enum):
    SIGNAL = "Signal Fragment"
    VOID = "Void Echo"
    MEMORY = "Memory Crystal"
    CHAOS = "Chaos Shard"
    HARMONY = "Harmony Stone"
    QUANTUM = "Quantum Dust"
    TEMPORAL = "Temporal Flux"
    NEURAL = "Neural Link"

class SpecializationPath(enum.Enum):
    RESONANCE_MASTER = "Resonance Master"
    CHAOS_ENGINE = "Chaos Engine"
    HARMONY_KEEPER = "Harmony Keeper"
    VOID_WALKER = "Void Walker"

class CardRarity(enum.Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"
    MYTHIC = "Mythic"

# Database Models

class Player(Base):
    """Main player/user model"""
    __tablename__ = 'players'

    # Primary key
    user_id = Column(BigInteger, primary_key=True)  # Discord user ID

    # Basic info
    username = Column(String(255), nullable=False)
    discriminator = Column(String(10))
    avatar_url = Column(String(500))

    # Game stats
    balance = Column(Float, default=100.0)  # BloomCoin balance
    level = Column(Integer, default=1)
    experience = Column(BigInteger, default=0)
    prestige = Column(Integer, default=0)

    # Quantum stats
    quantum_residue = Column(Float, default=0.0)
    quantum_coherence = Column(Float, default=0.0)
    quantum_entangled_with = Column(BigInteger, nullable=True)  # Another user_id

    # Activity tracking
    total_mines = Column(Integer, default=0)
    total_battles = Column(Integer, default=0)
    total_patterns_discovered = Column(Integer, default=0)
    total_cards_collected = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    last_active = Column(DateTime, default=func.now(), onupdate=func.now())
    last_daily = Column(DateTime, nullable=True)

    # Settings
    active_companion_id = Column(Integer, ForeignKey('companions.id'), nullable=True)
    preferred_difficulty = Column(String(50), default='medium')
    notifications_enabled = Column(Boolean, default=True)

    # Relationships
    companions = relationship("Companion", back_populates="owner", cascade="all, delete-orphan")
    patterns = relationship("PatternInventory", back_populates="owner", cascade="all, delete-orphan")
    cards = relationship("CardCollection", back_populates="owner", cascade="all, delete-orphan")
    garden_plots = relationship("GardenPlot", back_populates="owner", cascade="all, delete-orphan")
    mining_history = relationship("MiningRecord", back_populates="player", cascade="all, delete-orphan")
    battle_history = relationship("BattleRecord", back_populates="player", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="player", cascade="all, delete-orphan")

    # Indexes for performance
    __table_args__ = (
        Index('idx_player_level', 'level'),
        Index('idx_player_balance', 'balance'),
        Index('idx_player_last_active', 'last_active'),
    )

class Companion(Base):
    """AI Companion model"""
    __tablename__ = 'companions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('players.user_id'), nullable=False)

    # Basic info
    name = Column(String(100), nullable=False)
    type = Column(Enum(CompanionType), nullable=False)
    guardian = Column(String(50))  # ECHO, PHOENIX, OAK, CRYSTAL

    # Stats
    level = Column(Integer, default=1)
    experience = Column(BigInteger, default=0)
    relationship = Column(Integer, default=10)  # 0-100
    mood = Column(String(50), default='neutral')

    # Mining stats
    hash_rate = Column(Float, default=100.0)
    efficiency = Column(Float, default=1.0)
    luck = Column(Float, default=1.0)

    # Specialization
    specialization = Column(Enum(SpecializationPath), nullable=True)
    skill_points = Column(Integer, default=0)
    learned_skills = Column(JSON, default=dict)  # Skill ID -> Level

    # Equipment slots
    equipment = Column(JSON, default=dict)  # Slot -> Equipment ID

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    last_interaction = Column(DateTime, default=func.now())

    # Relationships
    owner = relationship("Player", back_populates="companions")

    # Unique constraint
    __table_args__ = (
        UniqueConstraint('user_id', 'type', name='unique_user_companion_type'),
        Index('idx_companion_user', 'user_id'),
        Index('idx_companion_type', 'type'),
    )

class PatternInventory(Base):
    """Player's pattern inventory"""
    __tablename__ = 'pattern_inventory'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('players.user_id'), nullable=False)

    pattern_type = Column(Enum(PatternType), nullable=False)
    quantity = Column(Integer, default=0)
    total_discovered = Column(Integer, default=0)

    # Market data
    last_traded_price = Column(Float, nullable=True)
    total_traded = Column(Integer, default=0)

    # Timestamps
    first_discovered = Column(DateTime, default=func.now())
    last_discovered = Column(DateTime, default=func.now())

    # Relationships
    owner = relationship("Player", back_populates="patterns")

    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'pattern_type', name='unique_user_pattern'),
        Index('idx_pattern_user', 'user_id'),
        Index('idx_pattern_type', 'pattern_type'),
    )

class CardCollection(Base):
    """Player's card collection"""
    __tablename__ = 'card_collection'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('players.user_id'), nullable=False)

    card_id = Column(String(100), nullable=False)  # Unique card identifier
    card_name = Column(String(200), nullable=False)
    card_type = Column(String(50))  # Attack, Defense, Support, etc.
    guardian_type = Column(String(50))  # ECHO, PHOENIX, OAK, CRYSTAL

    # Card stats
    rarity = Column(Enum(CardRarity), nullable=False)
    power = Column(Integer, default=0)
    defense = Column(Integer, default=0)
    cost = Column(Integer, default=0)

    # Collection stats
    quantity = Column(Integer, default=1)
    level = Column(Integer, default=1)
    in_deck = Column(Boolean, default=False)

    # Timestamps
    obtained_at = Column(DateTime, default=func.now())

    # Relationships
    owner = relationship("Player", back_populates="cards")

    # Indexes
    __table_args__ = (
        Index('idx_card_user', 'user_id'),
        Index('idx_card_rarity', 'rarity'),
        Index('idx_card_in_deck', 'user_id', 'in_deck'),
    )

class GardenPlot(Base):
    """Quantum garden plots"""
    __tablename__ = 'garden_plots'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('players.user_id'), nullable=False)

    plot_number = Column(Integer, nullable=False)  # 1-9
    crop_type = Column(String(100), nullable=True)
    planted_at = Column(DateTime, nullable=True)
    growth_stage = Column(Integer, default=0)  # 0-100

    # Quantum properties
    quantum_enhanced = Column(Boolean, default=False)
    coherence_level = Column(Float, default=0.0)
    expected_yield = Column(Float, default=1.0)

    # Harvest data
    last_harvested = Column(DateTime, nullable=True)
    total_harvests = Column(Integer, default=0)
    total_yield = Column(Float, default=0.0)

    # Relationships
    owner = relationship("Player", back_populates="garden_plots")

    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'plot_number', name='unique_user_plot'),
        Index('idx_garden_user', 'user_id'),
    )

class MiningRecord(Base):
    """Mining history records"""
    __tablename__ = 'mining_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('players.user_id'), nullable=False)
    companion_id = Column(Integer, ForeignKey('companions.id'), nullable=True)

    # Mining data
    difficulty = Column(Integer, nullable=False)
    hash = Column(String(256), nullable=False)
    nonce = Column(BigInteger, nullable=False)
    reward = Column(Float, nullable=False)

    # Pattern discovery
    pattern_found = Column(Enum(PatternType), nullable=True)
    pattern_quantity = Column(Integer, default=0)

    # Quantum data
    quantum_bonus = Column(Float, default=0.0)
    residue_generated = Column(Float, default=0.0)

    # Timestamps
    mined_at = Column(DateTime, default=func.now())
    mining_time = Column(Float)  # Seconds

    # Relationships
    player = relationship("Player", back_populates="mining_history")

    # Indexes
    __table_args__ = (
        Index('idx_mining_user', 'user_id'),
        Index('idx_mining_time', 'mined_at'),
        Index('idx_mining_reward', 'reward'),
    )

class BattleRecord(Base):
    """Battle history records"""
    __tablename__ = 'battle_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('players.user_id'), nullable=False)
    opponent_id = Column(BigInteger, nullable=True)  # NULL for NPC battles

    # Battle data
    battle_type = Column(String(50))  # PvP, PvE, Tournament
    winner_id = Column(BigInteger, nullable=False)
    rounds = Column(Integer, default=0)

    # Deck data
    player_deck = Column(JSON)  # Card IDs used
    opponent_deck = Column(JSON)

    # Rewards
    winner_reward = Column(Float, default=0.0)
    loser_reward = Column(Float, default=0.0)
    experience_gained = Column(Integer, default=0)

    # Timestamps
    battle_start = Column(DateTime, default=func.now())
    battle_end = Column(DateTime)
    duration = Column(Integer)  # Seconds

    # Relationships
    player = relationship("Player", back_populates="battle_history")

    # Indexes
    __table_args__ = (
        Index('idx_battle_user', 'user_id'),
        Index('idx_battle_time', 'battle_start'),
    )

class Transaction(Base):
    """Transaction/trade history"""
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('players.user_id'), nullable=False)

    # Transaction info
    type = Column(String(50), nullable=False)  # mining, battle, trade, purchase, etc.
    amount = Column(Float, nullable=False)  # Can be negative for expenses
    balance_after = Column(Float, nullable=False)

    # Additional data
    description = Column(Text)
    metadata = Column(JSON)  # Store any additional transaction data

    # Timestamps
    created_at = Column(DateTime, default=func.now())

    # Relationships
    player = relationship("Player", back_populates="transactions")

    # Indexes
    __table_args__ = (
        Index('idx_transaction_user', 'user_id'),
        Index('idx_transaction_time', 'created_at'),
        Index('idx_transaction_type', 'type'),
    )

class GuildSettings(Base):
    """Discord guild/server settings"""
    __tablename__ = 'guild_settings'

    guild_id = Column(BigInteger, primary_key=True)  # Discord guild ID
    guild_name = Column(String(255))

    # Bot settings
    prefix = Column(String(10), default='!')
    language = Column(String(10), default='en')

    # Channel settings
    welcome_channel = Column(BigInteger, nullable=True)
    log_channel = Column(BigInteger, nullable=True)
    battle_channel = Column(BigInteger, nullable=True)
    market_channel = Column(BigInteger, nullable=True)

    # Feature toggles
    mining_enabled = Column(Boolean, default=True)
    battles_enabled = Column(Boolean, default=True)
    trading_enabled = Column(Boolean, default=True)
    gardens_enabled = Column(Boolean, default=True)

    # Economy settings
    mining_multiplier = Column(Float, default=1.0)
    battle_rewards_multiplier = Column(Float, default=1.0)

    # Moderation
    banned_users = Column(JSON, default=list)  # List of banned user IDs
    moderator_roles = Column(JSON, default=list)  # List of moderator role IDs

    # Timestamps
    joined_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Indexes
    __table_args__ = (
        Index('idx_guild_name', 'guild_name'),
    )

class MarketListing(Base):
    """Pattern/Card marketplace listings"""
    __tablename__ = 'market_listings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    seller_id = Column(BigInteger, ForeignKey('players.user_id'), nullable=False)

    # Item info
    item_type = Column(String(50), nullable=False)  # pattern, card, equipment
    item_id = Column(String(100), nullable=False)
    quantity = Column(Integer, default=1)

    # Pricing
    price_per_unit = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)

    # Status
    active = Column(Boolean, default=True)
    sold_quantity = Column(Integer, default=0)

    # Timestamps
    listed_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, nullable=True)
    last_updated = Column(DateTime, default=func.now())

    # Indexes
    __table_args__ = (
        Index('idx_market_seller', 'seller_id'),
        Index('idx_market_active', 'active'),
        Index('idx_market_item', 'item_type', 'item_id'),
        Index('idx_market_price', 'price_per_unit'),
    )

class LearningProgress(Base):
    """Track learning module progress"""
    __tablename__ = 'learning_progress'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('players.user_id'), nullable=False)

    module_id = Column(String(100), nullable=False)
    module_name = Column(String(200))
    category = Column(String(100))  # mining, quantum, economics, etc.

    # Progress tracking
    completed = Column(Boolean, default=False)
    score = Column(Integer, default=0)
    attempts = Column(Integer, default=0)
    best_score = Column(Integer, default=0)

    # Rewards earned
    experience_earned = Column(Integer, default=0)
    bloomcoin_earned = Column(Float, default=0.0)
    patterns_earned = Column(JSON, default=dict)

    # Timestamps
    started_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime, nullable=True)
    last_attempt = Column(DateTime, default=func.now())

    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'module_id', name='unique_user_module'),
        Index('idx_learning_user', 'user_id'),
        Index('idx_learning_module', 'module_id'),
    )

# Database initialization function
def init_db(engine):
    """Initialize database with all tables"""
    Base.metadata.create_all(bind=engine)