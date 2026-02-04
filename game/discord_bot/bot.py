"""
BloomQuest Discord Bot - Main Entry Point
=========================================
A unified Discord bot for the BloomCoin ecosystem
"""

import os
import asyncio
import logging
from typing import Optional
from datetime import datetime
import discord
from discord.ext import commands
import aioredis
import asyncpg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('BloomQuest')

# Bot configuration
class BotConfig:
    """Bot configuration settings"""
    TOKEN = os.getenv('DISCORD_TOKEN')
    PREFIX = os.getenv('BOT_PREFIX', '!')
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/bloomquest')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost')

    # Feature flags
    ENABLE_WEB_DASHBOARD = os.getenv('ENABLE_WEB_DASHBOARD', 'false').lower() == 'true'
    ENABLE_VOICE_FEATURES = os.getenv('ENABLE_VOICE_FEATURES', 'false').lower() == 'true'

    # Game settings
    STARTING_BALANCE = float(os.getenv('STARTING_BALANCE', '100.0'))
    MINING_COOLDOWN = int(os.getenv('MINING_COOLDOWN', '60'))
    MAX_COMPANIONS = int(os.getenv('MAX_COMPANIONS', '7'))

class BloomQuestBot(commands.Bot):
    """
    Main bot class for BloomQuest Discord Bot
    Integrates all game systems into a unified Discord experience
    """

    def __init__(self):
        # Initialize intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True

        # Initialize bot
        super().__init__(
            command_prefix=self.get_prefix,
            intents=intents,
            description='BloomQuest - A quantum cryptocurrency adventure',
            help_command=None  # We'll create a custom help command
        )

        # Initialize connections
        self.db_pool: Optional[asyncpg.Pool] = None
        self.redis: Optional[aioredis.Redis] = None
        self.config = BotConfig()

        # Game state managers
        self.active_sessions = {}  # User ID -> Game Session
        self.mining_operations = {}  # User ID -> Mining Operation
        self.battles = {}  # Channel ID -> Battle Instance

        # Performance metrics
        self.start_time = datetime.utcnow()
        self.commands_processed = 0

    async def get_prefix(self, message: discord.Message):
        """Dynamic prefix support"""
        # Support mentions as prefix
        base_prefixes = [f'<@!{self.user.id}> ', f'<@{self.user.id}> ']

        # Get custom prefix from database if in guild
        if message.guild:
            custom_prefix = await self.get_guild_prefix(message.guild.id)
            if custom_prefix:
                base_prefixes.append(custom_prefix)

        # Add default prefix
        base_prefixes.append(self.config.PREFIX)

        return base_prefixes

    async def get_guild_prefix(self, guild_id: int) -> Optional[str]:
        """Get custom prefix for a guild from database"""
        if not self.db_pool:
            return None

        try:
            async with self.db_pool.acquire() as conn:
                result = await conn.fetchval(
                    "SELECT prefix FROM guild_settings WHERE guild_id = $1",
                    guild_id
                )
                return result
        except Exception as e:
            logger.error(f"Error fetching guild prefix: {e}")
            return None

    async def setup_hook(self):
        """Initialize bot systems before starting"""
        logger.info("Initializing BloomQuest systems...")

        # Setup database connection
        await self.setup_database()

        # Setup Redis cache
        await self.setup_redis()

        # Load all cogs
        await self.load_extensions()

        # Sync slash commands (if using hybrid commands)
        if self.config.PREFIX == '/':
            logger.info("Syncing slash commands...")
            await self.tree.sync()

        logger.info("BloomQuest initialization complete!")

    async def setup_database(self):
        """Setup PostgreSQL connection pool"""
        try:
            self.db_pool = await asyncpg.create_pool(
                self.config.DATABASE_URL,
                min_size=10,
                max_size=20,
                command_timeout=60
            )

            # Run migrations
            await self.run_migrations()

            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            logger.warning("Bot will run with limited functionality")

    async def setup_redis(self):
        """Setup Redis connection for caching"""
        try:
            self.redis = await aioredis.create_redis_pool(
                self.config.REDIS_URL,
                encoding='utf-8'
            )
            logger.info("Redis cache connection established")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            logger.warning("Running without cache (performance may be impacted)")

    async def run_migrations(self):
        """Run database migrations"""
        if not self.db_pool:
            return

        async with self.db_pool.acquire() as conn:
            # Create tables if they don't exist
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    user_id BIGINT PRIMARY KEY,
                    username VARCHAR(255),
                    balance DECIMAL(20, 8) DEFAULT 100.0,
                    level INTEGER DEFAULT 1,
                    experience BIGINT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            await conn.execute('''
                CREATE TABLE IF NOT EXISTS companions (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT REFERENCES players(user_id),
                    name VARCHAR(100),
                    type VARCHAR(50),
                    level INTEGER DEFAULT 1,
                    experience BIGINT DEFAULT 0,
                    relationship INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            await conn.execute('''
                CREATE TABLE IF NOT EXISTS patterns (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT REFERENCES players(user_id),
                    pattern_type VARCHAR(100),
                    quantity INTEGER DEFAULT 0,
                    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            await conn.execute('''
                CREATE TABLE IF NOT EXISTS guild_settings (
                    guild_id BIGINT PRIMARY KEY,
                    prefix VARCHAR(10) DEFAULT '!',
                    welcome_channel BIGINT,
                    log_channel BIGINT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            logger.info("Database migrations completed")

    async def load_extensions(self):
        """Load all cog extensions"""
        cogs = [
            'cogs.mining',
            'cogs.companions',
            'cogs.garden',
            'cogs.patterns',
            'cogs.battle',
            'cogs.economy',
            'cogs.quantum',
            'cogs.admin',
            'cogs.help',
            'cogs.events'
        ]

        for cog in cogs:
            try:
                await self.load_extension(cog)
                logger.info(f"Loaded cog: {cog}")
            except Exception as e:
                logger.error(f"Failed to load cog {cog}: {e}")

    async def on_ready(self):
        """Bot is ready and connected to Discord"""
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logger.info(f'Connected to {len(self.guilds)} guilds')

        # Set presence
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name=f"BloomQuest | {self.config.PREFIX}help")
        )

        # Start background tasks
        self.loop.create_task(self.status_updater())
        self.loop.create_task(self.cache_cleanup())

    async def on_guild_join(self, guild: discord.Guild):
        """Handle bot joining a new guild"""
        logger.info(f"Joined new guild: {guild.name} (ID: {guild.id})")

        # Create guild settings
        if self.db_pool:
            async with self.db_pool.acquire() as conn:
                await conn.execute('''
                    INSERT INTO guild_settings (guild_id)
                    VALUES ($1)
                    ON CONFLICT DO NOTHING
                ''', guild.id)

        # Send welcome message
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                embed = discord.Embed(
                    title="🌸 BloomQuest Has Arrived!",
                    description=(
                        f"Thank you for inviting BloomQuest to {guild.name}!\n\n"
                        f"**Getting Started:**\n"
                        f"• Use `{self.config.PREFIX}start` to begin your adventure\n"
                        f"• Use `{self.config.PREFIX}help` to see all commands\n"
                        f"• Use `{self.config.PREFIX}guide` for gameplay tips\n\n"
                        f"**Features:**\n"
                        f"• ⛏️ NEXTHASH-256 Mining\n"
                        f"• 🤖 AI Companions\n"
                        f"• 🌱 Quantum Gardens\n"
                        f"• 🃏 Card Battles\n"
                        f"• 📊 Pattern Trading\n"
                        f"• ✨ Quantum Residue System\n\n"
                        f"*Let the adventure begin!*"
                    ),
                    color=discord.Color.green()
                )
                await channel.send(embed=embed)
                break

    async def on_message(self, message: discord.Message):
        """Process messages"""
        # Ignore bot messages
        if message.author.bot:
            return

        # Process commands
        await self.process_commands(message)

        # Update user activity
        if self.db_pool and not message.author.bot:
            async with self.db_pool.acquire() as conn:
                await conn.execute('''
                    UPDATE players
                    SET last_active = CURRENT_TIMESTAMP
                    WHERE user_id = $1
                ''', message.author.id)

    async def on_command_completion(self, ctx: commands.Context):
        """Track command usage"""
        self.commands_processed += 1

        # Log command usage
        logger.info(
            f"Command '{ctx.command}' used by {ctx.author} "
            f"in {ctx.guild.name if ctx.guild else 'DM'}"
        )

    async def on_command_error(self, ctx: commands.Context, error: Exception):
        """Handle command errors"""
        # Ignore certain errors
        if isinstance(error, commands.CommandNotFound):
            return

        # Handle specific error types
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="⏰ Cooldown Active",
                description=f"Please wait {error.retry_after:.1f} seconds before using this command again.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed, delete_after=10)

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="❌ Missing Argument",
                description=f"Missing required argument: `{error.param.name}`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                title="🚫 Permission Denied",
                description="You don't have permission to use this command.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed, delete_after=10)

        else:
            # Log unexpected errors
            logger.error(f"Unhandled error in command {ctx.command}: {error}", exc_info=error)

            embed = discord.Embed(
                title="❌ An Error Occurred",
                description="An unexpected error occurred. The developers have been notified.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    async def status_updater(self):
        """Update bot status periodically"""
        await self.wait_until_ready()

        statuses = [
            f"{self.config.PREFIX}help | Mining BloomCoin",
            f"{len(self.guilds)} servers | {self.config.PREFIX}start",
            f"NEXTHASH-256 Mining",
            f"Quantum Residue: {5.854:.3f}",
            f"{self.commands_processed} commands processed"
        ]

        current = 0
        while not self.is_closed():
            await self.change_presence(
                activity=discord.Game(name=statuses[current])
            )
            current = (current + 1) % len(statuses)
            await asyncio.sleep(300)  # Update every 5 minutes

    async def cache_cleanup(self):
        """Clean up Redis cache periodically"""
        await self.wait_until_ready()

        while not self.is_closed():
            if self.redis:
                try:
                    # Clean up expired keys
                    expired = await self.redis.execute('DBSIZE')
                    logger.info(f"Cache cleanup: {expired} keys in cache")
                except Exception as e:
                    logger.error(f"Cache cleanup error: {e}")

            await asyncio.sleep(3600)  # Run every hour

    async def close(self):
        """Cleanup on bot shutdown"""
        logger.info("Shutting down BloomQuest bot...")

        # Close database connection
        if self.db_pool:
            await self.db_pool.close()

        # Close Redis connection
        if self.redis:
            self.redis.close()
            await self.redis.wait_closed()

        await super().close()

def main():
    """Main entry point"""
    # Check for token
    if not BotConfig.TOKEN:
        logger.error("No Discord token found! Set DISCORD_TOKEN in .env file")
        return

    # Create and run bot
    bot = BloomQuestBot()

    try:
        bot.run(BotConfig.TOKEN)
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)

if __name__ == "__main__":
    main()