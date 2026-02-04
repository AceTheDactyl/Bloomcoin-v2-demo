"""
Mining Cog - NEXTHASH-256 Mining System
========================================
Implements the core mining mechanics with NEXTHASH-256
"""

import discord
from discord.ext import commands, tasks
import asyncio
import random
import time
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from nexthash256 import nexthash256_hex
from quantum_residue_system import QuantumResidueSystem, ResidueType

class MiningOperation:
    """Represents an active mining operation"""
    def __init__(self, user_id: int, companion_id: int, difficulty: int):
        self.user_id = user_id
        self.companion_id = companion_id
        self.difficulty = difficulty
        self.start_time = time.time()
        self.completed = False
        self.result = None

class MiningCog(commands.Cog, name="Mining"):
    """
    Mining system using NEXTHASH-256
    Integrates quantum residue and companion bonuses
    """

    def __init__(self, bot):
        self.bot = bot
        self.active_mining: Dict[int, MiningOperation] = {}
        self.cooldowns: Dict[int, datetime] = {}

        # Initialize quantum system
        self.quantum = QuantumResidueSystem()

        # Mining configuration
        self.COOLDOWN_SECONDS = 60
        self.BASE_REWARD = 10.0
        self.DIFFICULTY_LEVELS = {
            'easy': 2,
            'medium': 3,
            'hard': 4,
            'extreme': 5,
            'quantum': 6
        }

    def cog_unload(self):
        """Cleanup when cog unloads"""
        self.mining_processor.cancel()

    @commands.hybrid_group(name='mine', invoke_without_command=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def mine(self, ctx: commands.Context, difficulty: str = 'medium'):
        """
        Start a mining operation using NEXTHASH-256

        Parameters:
        - difficulty: Mining difficulty (easy, medium, hard, extreme, quantum)
        """
        # Check if already mining
        if ctx.author.id in self.active_mining:
            embed = discord.Embed(
                title="⛏️ Already Mining!",
                description="You already have an active mining operation.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return

        # Validate difficulty
        if difficulty.lower() not in self.DIFFICULTY_LEVELS:
            embed = discord.Embed(
                title="❌ Invalid Difficulty",
                description=f"Valid difficulties: {', '.join(self.DIFFICULTY_LEVELS.keys())}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Get user's active companion
        companion = await self.get_active_companion(ctx.author.id)
        if not companion:
            embed = discord.Embed(
                title="🤖 No Companion",
                description="You need an active companion to mine! Use `!companion summon` first.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Start mining operation
        diff_value = self.DIFFICULTY_LEVELS[difficulty.lower()]
        operation = MiningOperation(ctx.author.id, companion['id'], diff_value)
        self.active_mining[ctx.author.id] = operation

        # Send initial embed
        embed = discord.Embed(
            title="⛏️ Mining Started!",
            description=(
                f"**Companion:** {companion['name']} ({companion['type']})\n"
                f"**Difficulty:** {difficulty.capitalize()} (Need {diff_value} leading zeros)\n"
                f"**Algorithm:** NEXTHASH-256\n\n"
                f"*Mining in progress...*"
            ),
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"Miner: {ctx.author.name}")

        message = await ctx.send(embed=embed)

        # Perform mining in background
        self.bot.loop.create_task(
            self.perform_mining(ctx, operation, companion, message)
        )

    async def perform_mining(
        self,
        ctx: commands.Context,
        operation: MiningOperation,
        companion: dict,
        message: discord.Message
    ):
        """Perform the actual mining operation"""
        try:
            # Mining animation
            animations = ['⛏️', '⚒️', '🔨', '⛏️']
            for i in range(3):
                embed = message.embeds[0]
                embed.description = embed.description.replace('*Mining in progress...*',
                    f'{animations[i % len(animations)]} Mining... ({i+1}/3)')
                await message.edit(embed=embed)
                await asyncio.sleep(1)

            # Perform NEXTHASH-256 mining
            start_time = time.time()
            success, nonce, hash_result = await self.mine_nexthash(
                f"{ctx.author.id}{time.time()}",
                operation.difficulty
            )
            mining_time = time.time() - start_time

            # Calculate rewards
            if success:
                # Base reward with difficulty multiplier
                base_reward = self.BASE_REWARD * (2 ** operation.difficulty)

                # Companion bonus
                companion_bonus = self.get_companion_bonus(companion)
                reward = base_reward * companion_bonus

                # Quantum residue bonus
                quantum_bonus = await self.apply_quantum_residue(ctx.author.id, reward)
                total_reward = reward + quantum_bonus

                # Update database
                await self.update_balance(ctx.author.id, total_reward)
                await self.add_mining_record(ctx.author.id, companion['id'], total_reward, hash_result)

                # Success embed
                embed = discord.Embed(
                    title="⛏️ Mining Successful!",
                    description=(
                        f"**Hash Found:** `{hash_result[:32]}...`\n"
                        f"**Nonce:** {nonce:,}\n"
                        f"**Time:** {mining_time:.2f} seconds\n\n"
                        f"**Rewards:**\n"
                        f"Base: {base_reward:.2f} BC\n"
                        f"Companion Bonus: x{companion_bonus:.1f}\n"
                        f"Quantum Residue: +{quantum_bonus:.2f} BC\n"
                        f"**Total: {total_reward:.2f} BC**"
                    ),
                    color=discord.Color.green(),
                    timestamp=datetime.utcnow()
                )

                # Add companion reaction
                companion_reaction = self.get_companion_reaction(companion['type'], 'success')
                embed.add_field(
                    name=f"{companion['name']} says:",
                    value=companion_reaction,
                    inline=False
                )

            else:
                # Mining failed (timeout)
                embed = discord.Embed(
                    title="⛏️ Mining Failed",
                    description="Mining operation timed out. Try an easier difficulty!",
                    color=discord.Color.red(),
                    timestamp=datetime.utcnow()
                )

                companion_reaction = self.get_companion_reaction(companion['type'], 'failure')
                embed.add_field(
                    name=f"{companion['name']} says:",
                    value=companion_reaction,
                    inline=False
                )

            embed.set_footer(text=f"Miner: {ctx.author.name}")
            await message.edit(embed=embed)

        except Exception as e:
            print(f"Mining error: {e}")
            embed = discord.Embed(
                title="❌ Mining Error",
                description="An error occurred during mining.",
                color=discord.Color.red()
            )
            await message.edit(embed=embed)

        finally:
            # Remove from active mining
            if ctx.author.id in self.active_mining:
                del self.active_mining[ctx.author.id]

    async def mine_nexthash(self, data: str, difficulty: int) -> Tuple[bool, int, str]:
        """
        Perform NEXTHASH-256 mining
        Returns: (success, nonce, hash)
        """
        nonce = 0
        max_attempts = 1000000  # Prevent infinite loop
        target = '0' * difficulty

        for nonce in range(max_attempts):
            # Create mining input
            mining_input = f"{data}:{nonce}"

            # Generate NEXTHASH-256
            hash_result = nexthash256_hex(mining_input)

            # Check if we found a valid hash
            if hash_result.startswith(target):
                return True, nonce, hash_result

        return False, nonce, ""

    def get_companion_bonus(self, companion: dict) -> float:
        """Calculate companion mining bonus"""
        bonuses = {
            'Echo': 1.2,    # +20% for pattern detection
            'Glitch': 1.5,  # +50% for chaos mining
            'Flow': 1.1,    # +10% for efficiency
            'Spark': 2.0,   # +100% for speed
            'Sage': 1.3,    # +30% for knowledge
            'Scout': 1.4,   # +40% for discovery
            'Null': 1.8     # +80% for void mining
        }

        base_bonus = bonuses.get(companion['type'], 1.0)

        # Level bonus (5% per level)
        level_bonus = 1.0 + (companion['level'] * 0.05)

        return base_bonus * level_bonus

    async def apply_quantum_residue(self, user_id: int, base_reward: float) -> float:
        """Apply quantum residue effects to mining"""
        # Get user's residue state
        residue = self.quantum.calculate_residue(
            base_reward,
            ResidueType.ENERGY,
            coupling=0.1
        )

        # Calculate quantum bonus
        quantum_bonus = residue['quantum_effects']['coherence'] * base_reward * 0.1

        return quantum_bonus

    def get_companion_reaction(self, companion_type: str, result: str) -> str:
        """Get companion's reaction to mining result"""
        reactions = {
            'Echo': {
                'success': "The crystals sing in harmony... harmony...",
                'failure': "The echoes fade into silence... silence..."
            },
            'Glitch': {
                'success': "Y̸E̶S̷!̸ We BR̷O̶K̵E̸ the pattern!",
                'failure': "System.ERROR... but that's F̸U̶N̵ too!"
            },
            'Flow': {
                'success': "Like water through stone / Success flows naturally / Peace in every hash",
                'failure': "Even rocks resist / But water always finds way / Flow continues on"
            },
            'Spark': {
                'success': "AMAZING!!! We did it! Let's mine MORE!!!",
                'failure': "No worries! We'll get it next time! NEVER GIVE UP!!!"
            },
            'Sage': {
                'success': "As the ancient miners say: 'Persistence yields crystals.'",
                'failure': "A learning opportunity. Let us adjust our approach."
            },
            'Scout': {
                'success': "I spotted the pattern! There might be more nearby...",
                'failure': "Hmm, let me scout for a better vein..."
            },
            'Null': {
                'success': "...",
                'failure': "..."
            }
        }

        return reactions.get(companion_type, {}).get(result, "Interesting...")

    async def get_active_companion(self, user_id: int) -> Optional[dict]:
        """Get user's active companion from database"""
        if not self.bot.db_pool:
            return None

        async with self.bot.db_pool.acquire() as conn:
            result = await conn.fetchrow('''
                SELECT id, name, type, level
                FROM companions
                WHERE user_id = $1
                ORDER BY created_at DESC
                LIMIT 1
            ''', user_id)

            if result:
                return dict(result)
            return None

    async def update_balance(self, user_id: int, amount: float):
        """Update user's balance"""
        if not self.bot.db_pool:
            return

        async with self.bot.db_pool.acquire() as conn:
            # Ensure user exists
            await conn.execute('''
                INSERT INTO players (user_id, balance)
                VALUES ($1, $2)
                ON CONFLICT (user_id)
                DO UPDATE SET balance = players.balance + $2
            ''', user_id, amount)

    async def add_mining_record(self, user_id: int, companion_id: int, reward: float, hash_result: str):
        """Record mining operation in database"""
        if not self.bot.db_pool:
            return

        async with self.bot.db_pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO mining_history (user_id, companion_id, reward, hash, mined_at)
                VALUES ($1, $2, $3, $4, CURRENT_TIMESTAMP)
            ''', user_id, companion_id, reward, hash_result)

    @mine.command(name='stats')
    async def mine_stats(self, ctx: commands.Context):
        """View your mining statistics"""
        if not self.bot.db_pool:
            await ctx.send("Database not available.")
            return

        async with self.bot.db_pool.acquire() as conn:
            # Get mining stats
            stats = await conn.fetchrow('''
                SELECT
                    COUNT(*) as total_mines,
                    SUM(reward) as total_earned,
                    MAX(reward) as best_mine,
                    AVG(reward) as avg_reward
                FROM mining_history
                WHERE user_id = $1
            ''', ctx.author.id)

            if not stats or stats['total_mines'] == 0:
                embed = discord.Embed(
                    title="📊 Mining Statistics",
                    description="You haven't mined anything yet!",
                    color=discord.Color.blue()
                )
            else:
                embed = discord.Embed(
                    title="📊 Mining Statistics",
                    color=discord.Color.gold()
                )
                embed.add_field(name="Total Mines", value=f"{stats['total_mines']:,}", inline=True)
                embed.add_field(name="Total Earned", value=f"{stats['total_earned']:.2f} BC", inline=True)
                embed.add_field(name="Best Mine", value=f"{stats['best_mine']:.2f} BC", inline=True)
                embed.add_field(name="Average Reward", value=f"{stats['avg_reward']:.2f} BC", inline=True)

            embed.set_footer(text=f"Miner: {ctx.author.name}")
            await ctx.send(embed=embed)

    @mine.command(name='leaderboard')
    async def mine_leaderboard(self, ctx: commands.Context):
        """View the mining leaderboard"""
        if not self.bot.db_pool:
            await ctx.send("Database not available.")
            return

        async with self.bot.db_pool.acquire() as conn:
            # Get top miners
            top_miners = await conn.fetch('''
                SELECT
                    user_id,
                    COUNT(*) as total_mines,
                    SUM(reward) as total_earned
                FROM mining_history
                GROUP BY user_id
                ORDER BY total_earned DESC
                LIMIT 10
            ''')

            if not top_miners:
                embed = discord.Embed(
                    title="🏆 Mining Leaderboard",
                    description="No mining data yet!",
                    color=discord.Color.gold()
                )
            else:
                embed = discord.Embed(
                    title="🏆 Mining Leaderboard",
                    color=discord.Color.gold()
                )

                leaderboard_text = ""
                for i, miner in enumerate(top_miners, 1):
                    user = self.bot.get_user(miner['user_id'])
                    username = user.name if user else f"User#{miner['user_id']}"

                    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
                    medal = medals.get(i, "🏅")

                    leaderboard_text += (
                        f"{medal} **{username}**\n"
                        f"   Mines: {miner['total_mines']:,} | "
                        f"Earned: {miner['total_earned']:.2f} BC\n\n"
                    )

                embed.description = leaderboard_text

            await ctx.send(embed=embed)

async def setup(bot):
    """Setup function for Discord.py 2.0+"""
    await bot.add_cog(MiningCog(bot))