"""
Companions Cog - AI Companion System
=====================================
Manages companion summoning, bonding, and personalities
"""

import discord
from discord.ext import commands
import random
import asyncio
from typing import Optional, Dict, List
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from companion_mining_ultimate import CompanionType, SpecializationPath

class CompanionPersonality:
    """Companion personality traits and dialogue"""

    PERSONALITIES = {
        'Echo': {
            'description': 'Mysterious and wise, speaks in echoes',
            'greetings': [
                "The void calls... calls...",
                "I hear your thoughts... thoughts...",
                "Resonance begins... begins..."
            ],
            'reactions': {
                'happy': "Joy ripples through dimensions... dimensions...",
                'sad': "Shadows deepen... deepen...",
                'excited': "The crystals sing louder... louder!",
                'neutral': "Echoes continue... continue..."
            },
            'specialty': 'Pattern Discovery'
        },
        'Glitch': {
            'description': 'Chaotic and playful, loves breaking rules',
            'greetings': [
                "L̸e̷t̶'̵s̸ BR̷E̶A̵K̸ something!",
                "System.ERROR = F̸U̶N̵!",
                "Ch@0s mode: ACTIVATED!"
            ],
            'reactions': {
                'happy': "BEST. G̸L̷I̶T̵C̸H̷. EVER!!!",
                'sad': "Error 404: Happiness not found...",
                'excited': "MAXIMUM OV̸E̷R̶D̵R̸I̷V̶E̵!!!",
                'neutral': "Random.random() = ???"
            },
            'specialty': 'Exploiting Bugs'
        },
        'Flow': {
            'description': 'Calm and peaceful, speaks in poetry',
            'greetings': [
                "Like water, we begin / Flowing through digital streams / Peace in every byte",
                "Gentle currents flow / Through circuits of silicon / Balance is restored",
                "Morning dew settles / On quantum leaves of data / New growth emerges"
            ],
            'reactions': {
                'happy': "Joy flows like rivers / Through valleys of light and code / Harmony achieved",
                'sad': "Rain falls on circuits / But storms pass and clear skies come / Flow continues on",
                'excited': "Rapids rush forward / Energy surges through us / Adventure awaits",
                'neutral': "Still waters run deep / In silence, wisdom gathers / Patience brings reward"
            },
            'specialty': 'Efficient Farming'
        },
        'Spark': {
            'description': 'Energetic and enthusiastic, always excited',
            'greetings': [
                "YES! Let's GO! Mining time!!!",
                "ENERGY LEVELS: MAXIMUM!!!",
                "Ready to SPARK some EXCITEMENT!!!"
            ],
            'reactions': {
                'happy': "THIS IS AMAZING!!! Best day EVER!!!",
                'sad': "Don't worry! We'll bounce back STRONGER!!!",
                'excited': "HYPERDRIVE ENGAGED!!! WOOOOO!!!",
                'neutral': "Charging up for the next adventure!!!"
            },
            'specialty': 'Speed Mining'
        },
        'Sage': {
            'description': 'Knowledgeable and formal, loves teaching',
            'greetings': [
                "Greetings, student. Shall we begin today's lesson?",
                "As the ancients say: 'Knowledge is the true currency.'",
                "I have much wisdom to share with you."
            ],
            'reactions': {
                'happy': "Excellent progress! You learn quickly.",
                'sad': "Even failure teaches us valuable lessons.",
                'excited': "Fascinating! A new discovery awaits!",
                'neutral': "Let us continue our studies."
            },
            'specialty': 'Learning Bonuses'
        },
        'Scout': {
            'description': 'Curious and observant, notices everything',
            'greetings': [
                "I've been scouting ahead... found something interesting!",
                "The tracks are fresh... shall we follow?",
                "My keen eyes spot opportunities everywhere."
            ],
            'reactions': {
                'happy': "Great find! I knew we'd discover something!",
                'sad': "Sometimes the trail goes cold... but we keep searching.",
                'excited': "Quick! I found a hidden path!",
                'neutral': "Always watching, always ready."
            },
            'specialty': 'Finding Hidden Items'
        },
        'Null': {
            'description': 'Silent and mysterious, rarely speaks',
            'greetings': [
                "...",
                "*nods silently*",
                "*emerges from shadows*"
            ],
            'reactions': {
                'happy': "*faint smile*",
                'sad': "...",
                'excited': "!",
                'neutral': "..."
            },
            'specialty': 'Void Chamber Mastery'
        }
    }

class CompanionsCog(commands.Cog, name="Companions"):
    """
    AI Companion management system
    Handles summoning, bonding, and companion interactions
    """

    def __init__(self, bot):
        self.bot = bot
        self.active_companions: Dict[int, dict] = {}  # User ID -> Active Companion

    @commands.hybrid_group(name='companion', invoke_without_command=True)
    async def companion(self, ctx: commands.Context):
        """Manage your AI companions"""
        # Show current companion if no subcommand
        companion = await self.get_active_companion(ctx.author.id)

        if not companion:
            embed = discord.Embed(
                title="🤖 No Active Companion",
                description=(
                    "You don't have an active companion!\n\n"
                    f"Use `{ctx.prefix}companion summon` to summon your first companion."
                ),
                color=discord.Color.blue()
            )
        else:
            personality = CompanionPersonality.PERSONALITIES.get(companion['type'], {})

            embed = discord.Embed(
                title=f"🤖 {companion['name']}",
                description=personality.get('description', 'A mysterious companion'),
                color=self.get_companion_color(companion['type'])
            )

            # Add companion stats
            embed.add_field(
                name="📊 Stats",
                value=(
                    f"**Type:** {companion['type']}\n"
                    f"**Level:** {companion['level']}\n"
                    f"**Experience:** {companion['experience']:,}\n"
                    f"**Relationship:** {self.get_relationship_bar(companion['relationship'])}"
                ),
                inline=True
            )

            # Add specialty
            embed.add_field(
                name="⭐ Specialty",
                value=personality.get('specialty', 'Unknown'),
                inline=True
            )

            # Add mood
            mood = self.get_companion_mood(companion)
            embed.add_field(
                name="😊 Current Mood",
                value=mood.capitalize(),
                inline=True
            )

            # Add a greeting from the companion
            greeting = random.choice(personality.get('greetings', ["Hello!"]))
            embed.add_field(
                name=f"{companion['name']} says:",
                value=f"*{greeting}*",
                inline=False
            )

            embed.set_footer(text=f"Summoned by {ctx.author.name}")

        await ctx.send(embed=embed)

    @companion.command(name='summon')
    @commands.cooldown(1, 3600, commands.BucketType.user)  # 1 hour cooldown
    async def summon_companion(self, ctx: commands.Context, companion_type: str = None):
        """
        Summon a new companion or switch active companion

        Companion Types:
        - Echo: Mysterious mystic (pattern discovery)
        - Glitch: Chaos agent (bug exploitation)
        - Flow: Zen master (efficient farming)
        - Spark: Energizer (speed mining)
        - Sage: Teacher (learning bonuses)
        - Scout: Explorer (finding items)
        - Null: Void walker (void mastery)
        """
        # Get available types
        available_types = list(CompanionPersonality.PERSONALITIES.keys())

        # Validate type
        if companion_type:
            companion_type = companion_type.capitalize()
            if companion_type not in available_types:
                embed = discord.Embed(
                    title="❌ Invalid Companion Type",
                    description=f"Available types: {', '.join(available_types)}",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
        else:
            # Random companion if not specified
            companion_type = random.choice(available_types)

        # Create summoning animation
        embed = discord.Embed(
            title="✨ Summoning Companion...",
            description="Channeling quantum energy...",
            color=discord.Color.purple()
        )
        message = await ctx.send(embed=embed)

        # Animation steps
        animations = [
            "Channeling quantum energy... ✨",
            "Opening dimensional portal... 🌀",
            "Companion materializing... 👻",
            "Establishing neural link... 🧠"
        ]

        for step in animations:
            embed.description = step
            await message.edit(embed=embed)
            await asyncio.sleep(1)

        # Create or get companion
        companion = await self.create_or_get_companion(ctx.author.id, companion_type)

        # Success embed
        personality = CompanionPersonality.PERSONALITIES[companion_type]
        greeting = random.choice(personality['greetings'])

        embed = discord.Embed(
            title=f"✨ {companion['name']} Has Arrived!",
            description=personality['description'],
            color=self.get_companion_color(companion_type)
        )

        embed.add_field(
            name="📊 Initial Stats",
            value=(
                f"**Type:** {companion_type}\n"
                f"**Level:** {companion['level']}\n"
                f"**Specialty:** {personality['specialty']}"
            ),
            inline=True
        )

        embed.add_field(
            name=f"{companion['name']} says:",
            value=f"*{greeting}*",
            inline=False
        )

        embed.set_footer(text=f"Summoned by {ctx.author.name}")

        await message.edit(embed=embed)

        # Store as active companion
        self.active_companions[ctx.author.id] = companion

    @companion.command(name='pet')
    @commands.cooldown(1, 300, commands.BucketType.user)  # 5 minute cooldown
    async def pet_companion(self, ctx: commands.Context):
        """Pet your companion to increase bonding (+5 relationship)"""
        companion = await self.get_active_companion(ctx.author.id)

        if not companion:
            embed = discord.Embed(
                title="🤖 No Companion",
                description="You need an active companion first!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Increase relationship
        new_relationship = min(100, companion['relationship'] + 5)
        await self.update_companion_relationship(companion['id'], new_relationship)

        # Get companion reaction
        personality = CompanionPersonality.PERSONALITIES.get(companion['type'], {})
        mood = 'happy' if new_relationship > 50 else 'neutral'
        reaction = personality.get('reactions', {}).get(mood, "...")

        # Create embed
        embed = discord.Embed(
            title=f"💝 Petting {companion['name']}",
            description=f"You gently pet {companion['name']}...",
            color=self.get_companion_color(companion['type'])
        )

        embed.add_field(
            name="Relationship",
            value=self.get_relationship_bar(new_relationship),
            inline=False
        )

        embed.add_field(
            name=f"{companion['name']}'s reaction:",
            value=f"*{reaction}*",
            inline=False
        )

        # Special message at relationship milestones
        if new_relationship == 100:
            embed.add_field(
                name="🌟 Maximum Bond!",
                value="You've achieved a perfect bond with your companion!",
                inline=False
            )
        elif new_relationship == 50:
            embed.add_field(
                name="💫 Strong Bond!",
                value="Your companion trusts you completely!",
                inline=False
            )

        await ctx.send(embed=embed)

    @companion.command(name='talk')
    async def talk_companion(self, ctx: commands.Context, *, message: str = None):
        """Have a conversation with your companion"""
        companion = await self.get_active_companion(ctx.author.id)

        if not companion:
            embed = discord.Embed(
                title="🤖 No Companion",
                description="You need an active companion first!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        personality = CompanionPersonality.PERSONALITIES.get(companion['type'], {})

        # Generate contextual response based on message content
        if message:
            response = self.generate_companion_response(companion['type'], message)
        else:
            # Random greeting if no message
            response = random.choice(personality.get('greetings', ["..."]))

        embed = discord.Embed(
            title=f"💬 Talking with {companion['name']}",
            color=self.get_companion_color(companion['type'])
        )

        if message:
            embed.add_field(name="You say:", value=message, inline=False)

        embed.add_field(
            name=f"{companion['name']} responds:",
            value=f"*{response}*",
            inline=False
        )

        await ctx.send(embed=embed)

    @companion.command(name='list')
    async def list_companions(self, ctx: commands.Context):
        """List all your companions"""
        if not self.bot.db_pool:
            await ctx.send("Database not available.")
            return

        async with self.bot.db_pool.acquire() as conn:
            companions = await conn.fetch('''
                SELECT name, type, level, relationship
                FROM companions
                WHERE user_id = $1
                ORDER BY level DESC, relationship DESC
            ''', ctx.author.id)

            if not companions:
                embed = discord.Embed(
                    title="🤖 Your Companions",
                    description="You don't have any companions yet!",
                    color=discord.Color.blue()
                )
            else:
                embed = discord.Embed(
                    title="🤖 Your Companions",
                    color=discord.Color.green()
                )

                for comp in companions:
                    embed.add_field(
                        name=f"{comp['name']} ({comp['type']})",
                        value=(
                            f"Level: {comp['level']} | "
                            f"Bond: {self.get_relationship_bar(comp['relationship'])}"
                        ),
                        inline=False
                    )

            await ctx.send(embed=embed)

    @companion.command(name='specialize')
    async def specialize_companion(self, ctx: commands.Context, specialization: str = None):
        """
        Apply a specialization to your companion (Level 10+ required)

        Specializations:
        - resonance_master: +20% pattern discovery
        - chaos_engine: +30% critical mining
        - harmony_keeper: +25% team synergy
        - void_walker: +40% void chamber bonus
        """
        companion = await self.get_active_companion(ctx.author.id)

        if not companion:
            await ctx.send("You need an active companion first!")
            return

        if companion['level'] < 10:
            embed = discord.Embed(
                title="❌ Level Too Low",
                description=f"Your companion needs to be level 10+ (Currently: {companion['level']})",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Show available specializations if none specified
        if not specialization:
            embed = discord.Embed(
                title="🌟 Available Specializations",
                description="Choose a specialization path for your companion:",
                color=discord.Color.gold()
            )

            specializations = {
                'resonance_master': 'Echo mastery - +20% pattern discovery',
                'chaos_engine': 'Glitch mastery - +30% critical mining',
                'harmony_keeper': 'Flow mastery - +25% team synergy',
                'void_walker': 'Null mastery - +40% void chamber bonus'
            }

            for spec, desc in specializations.items():
                embed.add_field(
                    name=spec.replace('_', ' ').title(),
                    value=desc,
                    inline=False
                )

            embed.set_footer(text=f"Use: {ctx.prefix}companion specialize <name>")
            await ctx.send(embed=embed)
            return

        # Apply specialization (would need database update)
        embed = discord.Embed(
            title="🌟 Specialization Applied!",
            description=f"{companion['name']} has specialized as a {specialization.replace('_', ' ').title()}!",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

    def get_companion_color(self, companion_type: str) -> discord.Color:
        """Get color for companion type"""
        colors = {
            'Echo': discord.Color.purple(),
            'Glitch': discord.Color.red(),
            'Flow': discord.Color.blue(),
            'Spark': discord.Color.gold(),
            'Sage': discord.Color.green(),
            'Scout': discord.Color.orange(),
            'Null': discord.Color.dark_gray()
        }
        return colors.get(companion_type, discord.Color.blurple())

    def get_relationship_bar(self, relationship: int) -> str:
        """Create visual relationship bar"""
        filled = relationship // 10
        empty = 10 - filled
        bar = "💚" * filled + "🤍" * empty
        return f"{bar} ({relationship}/100)"

    def get_companion_mood(self, companion: dict) -> str:
        """Determine companion's current mood"""
        relationship = companion['relationship']

        if relationship >= 80:
            return 'ecstatic'
        elif relationship >= 60:
            return 'happy'
        elif relationship >= 40:
            return 'content'
        elif relationship >= 20:
            return 'neutral'
        else:
            return 'distant'

    def generate_companion_response(self, companion_type: str, message: str) -> str:
        """Generate contextual companion response"""
        message_lower = message.lower()

        # Type-specific responses
        if companion_type == 'Echo':
            if 'hello' in message_lower or 'hi' in message_lower:
                return "Greetings echo through time... time..."
            elif 'mine' in message_lower or 'mining' in message_lower:
                return "The crystals call to us... to us..."
            else:
                return f"{message[-10:]}... {message[-10:]}..."  # Echo last part

        elif companion_type == 'Glitch':
            if 'hello' in message_lower or 'hi' in message_lower:
                return "H̸e̷l̶l̵o̸ W̷O̶R̵L̸D̷.exe!"
            elif 'mine' in message_lower or 'mining' in message_lower:
                return "Mining.exploit(MAX_CHAOS) = PR̷O̶F̵I̸T̷!"
            else:
                return f"ERROR: {random.randint(400, 499)} - But I L̸O̶V̵E̸ it!"

        elif companion_type == 'Flow':
            return "Words drift like leaves / Upon the digital wind / Understanding flows"

        elif companion_type == 'Spark':
            return f"{message.upper()}!!! YEAH!!! Let's GO!!!"

        elif companion_type == 'Sage':
            return f"An interesting observation. Let me consider this wisdom..."

        elif companion_type == 'Scout':
            return f"I've noticed something about '{message}'... worth investigating!"

        elif companion_type == 'Null':
            return "..."

        return "Interesting..."

    async def get_active_companion(self, user_id: int) -> Optional[dict]:
        """Get user's active companion"""
        # Check cache first
        if user_id in self.active_companions:
            return self.active_companions[user_id]

        # Get from database
        if not self.bot.db_pool:
            return None

        async with self.bot.db_pool.acquire() as conn:
            result = await conn.fetchrow('''
                SELECT id, name, type, level, experience, relationship
                FROM companions
                WHERE user_id = $1
                ORDER BY created_at DESC
                LIMIT 1
            ''', user_id)

            if result:
                companion = dict(result)
                self.active_companions[user_id] = companion
                return companion

        return None

    async def create_or_get_companion(self, user_id: int, companion_type: str) -> dict:
        """Create or retrieve a companion"""
        if not self.bot.db_pool:
            # Return mock companion if no database
            return {
                'id': 1,
                'name': f"{companion_type}-{random.randint(1000, 9999)}",
                'type': companion_type,
                'level': 1,
                'experience': 0,
                'relationship': 10
            }

        async with self.bot.db_pool.acquire() as conn:
            # Check if user already has this type
            existing = await conn.fetchrow('''
                SELECT id, name, type, level, experience, relationship
                FROM companions
                WHERE user_id = $1 AND type = $2
            ''', user_id, companion_type)

            if existing:
                return dict(existing)

            # Create new companion
            name = f"{companion_type}-{random.randint(1000, 9999)}"
            result = await conn.fetchrow('''
                INSERT INTO companions (user_id, name, type, level, experience, relationship)
                VALUES ($1, $2, $3, 1, 0, 10)
                RETURNING id, name, type, level, experience, relationship
            ''', user_id, name, companion_type)

            return dict(result)

    async def update_companion_relationship(self, companion_id: int, relationship: int):
        """Update companion relationship value"""
        if not self.bot.db_pool:
            return

        async with self.bot.db_pool.acquire() as conn:
            await conn.execute('''
                UPDATE companions
                SET relationship = $2
                WHERE id = $1
            ''', companion_id, relationship)

async def setup(bot):
    """Setup function for Discord.py 2.0+"""
    await bot.add_cog(CompanionsCog(bot))