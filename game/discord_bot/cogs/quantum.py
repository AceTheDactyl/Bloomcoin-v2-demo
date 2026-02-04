"""
Quantum Cog - Quantum Residue System
=====================================
Implements quantum residue mechanics based on golden ratio physics
"""

import discord
from discord.ext import commands
import numpy as np
import asyncio
import random
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from quantum_residue_system import QuantumResidueSystem, ResidueType
from nexthash256 import nexthash256_hex

class QuantumCog(commands.Cog, name="Quantum"):
    """
    Quantum residue system based on Projection Residue Cosmology
    Golden ratio physics: R = φ⁴ - 1 = 5.854
    """

    def __init__(self, bot):
        self.bot = bot
        self.quantum = QuantumResidueSystem()
        self.active_fields: Dict[int, dict] = {}  # User ID -> Quantum Field

        # Golden ratio constants
        self.PHI = (1 + np.sqrt(5)) / 2  # φ = 1.618...
        self.R_DARK = self.PHI**4 - 1  # R = 5.854 (dark matter ratio)
        self.TAU = 2 * np.pi * self.PHI  # Harmonic constant

    @commands.hybrid_group(name='quantum', invoke_without_command=True)
    async def quantum(self, ctx: commands.Context):
        """View your quantum field status"""
        field = await self.get_quantum_field(ctx.author.id)

        embed = discord.Embed(
            title="⚛️ Quantum Field Status",
            description="Your quantum residue field based on golden ratio physics",
            color=discord.Color.purple()
        )

        # Calculate current coherence
        coherence = self.calculate_coherence(field)
        residue = field.get('accumulated_residue', 0)

        # Field metrics
        embed.add_field(
            name="📊 Field Metrics",
            value=(
                f"**Coherence:** {coherence:.3f} / {self.TAU:.3f}\n"
                f"**Residue:** {residue:.2f} units\n"
                f"**Dark Ratio:** {self.R_DARK:.3f} (φ⁴ - 1)"
            ),
            inline=True
        )

        # Energy distribution
        energy_dist = field.get('energy_distribution', {})
        embed.add_field(
            name="⚡ Energy Distribution",
            value=(
                f"**Kinetic:** {energy_dist.get('kinetic', 0):.1f}%\n"
                f"**Potential:** {energy_dist.get('potential', 0):.1f}%\n"
                f"**Residual:** {energy_dist.get('residual', 0):.1f}%"
            ),
            inline=True
        )

        # Quantum state
        state = self.determine_quantum_state(coherence)
        embed.add_field(
            name="🌀 Quantum State",
            value=f"**{state}**",
            inline=True
        )

        # Visualization of coherence
        coherence_bar = self.create_coherence_bar(coherence)
        embed.add_field(
            name="Coherence Level",
            value=coherence_bar,
            inline=False
        )

        # Golden ratio information
        embed.add_field(
            name="🌟 Golden Ratio Physics",
            value=(
                f"Based on Projection Residue Cosmology:\n"
                f"• φ = {self.PHI:.6f} (golden ratio)\n"
                f"• R = φ⁴ - 1 = {self.R_DARK:.6f} (dark/visible matter ratio)\n"
                f"• τ = 2πφ = {self.TAU:.6f} (harmonic constant)"
            ),
            inline=False
        )

        embed.set_footer(text=f"Quantum Observer: {ctx.author.name}")
        await ctx.send(embed=embed)

    @quantum.command(name='collapse')
    @commands.cooldown(1, 300, commands.BucketType.user)  # 5 minute cooldown
    async def collapse_field(self, ctx: commands.Context):
        """
        Collapse your quantum field to extract BloomCoin from residue
        Uses Kuramoto synchronization dynamics
        """
        field = await self.get_quantum_field(ctx.author.id)
        residue = field.get('accumulated_residue', 0)

        if residue < 10:
            embed = discord.Embed(
                title="⚛️ Insufficient Residue",
                description=f"You need at least 10 residue units to collapse. (Current: {residue:.2f})",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Animation embed
        embed = discord.Embed(
            title="⚛️ Collapsing Quantum Field...",
            description="Synchronizing quantum oscillators...",
            color=discord.Color.purple()
        )
        message = await ctx.send(embed=embed)

        # Collapse animation
        animations = [
            "🌀 Measuring quantum state...",
            "⚡ Synchronizing oscillators (Kuramoto model)...",
            "✨ Approaching critical coupling K = 2...",
            "🔮 Wave function collapsing..."
        ]

        for step in animations:
            embed.description = step
            await message.edit(embed=embed)
            await asyncio.sleep(1)

        # Calculate collapse results
        coherence = self.calculate_coherence(field)
        sync_parameter = self.kuramoto_order_parameter(residue, coherence)

        # Base conversion using golden ratio
        base_conversion = residue / self.R_DARK  # Convert using dark matter ratio
        efficiency = sync_parameter  # 0 to 1 based on synchronization

        bloomcoin_extracted = base_conversion * efficiency

        # Quantum bonus for perfect coherence
        if coherence >= self.TAU * 0.9:
            quantum_bonus = bloomcoin_extracted * 0.5
            bloomcoin_extracted += quantum_bonus
            bonus_text = f"\n🌟 **Perfect Coherence Bonus:** +{quantum_bonus:.2f} BC"
        else:
            bonus_text = ""

        # Update field
        await self.reset_quantum_field(ctx.author.id)
        await self.update_balance(ctx.author.id, bloomcoin_extracted)

        # Success embed
        embed = discord.Embed(
            title="⚛️ Quantum Collapse Complete!",
            description="Wave function successfully collapsed",
            color=discord.Color.green()
        )

        embed.add_field(
            name="📊 Collapse Results",
            value=(
                f"**Residue Consumed:** {residue:.2f} units\n"
                f"**Synchronization:** {sync_parameter:.1%}\n"
                f"**Efficiency:** {efficiency:.1%}\n"
                f"**BloomCoin Extracted:** {bloomcoin_extracted:.2f} BC"
                f"{bonus_text}"
            ),
            inline=False
        )

        # Add physics explanation
        embed.add_field(
            name="🔬 Quantum Physics",
            value=(
                f"Conversion rate: 1 residue = {1/self.R_DARK:.4f} BC (at 100% sync)\n"
                f"Your sync parameter: r = {sync_parameter:.3f}\n"
                f"Based on Kuramoto model with N oscillators"
            ),
            inline=False
        )

        embed.set_footer(text=f"Collapsed by {ctx.author.name}")
        await message.edit(embed=embed)

    @quantum.command(name='entangle')
    async def entangle(self, ctx: commands.Context, target: discord.Member):
        """
        Create quantum entanglement with another player
        Shares residue generation between entangled players
        """
        if target.id == ctx.author.id:
            await ctx.send("You cannot entangle with yourself!")
            return

        if target.bot:
            await ctx.send("You cannot entangle with bots!")
            return

        # Check if already entangled
        entanglement = await self.get_entanglement(ctx.author.id)
        if entanglement:
            embed = discord.Embed(
                title="⚛️ Already Entangled",
                description=f"You are already entangled with <@{entanglement}>",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return

        # Create entanglement request
        embed = discord.Embed(
            title="⚛️ Quantum Entanglement Request",
            description=(
                f"{ctx.author.mention} wants to create quantum entanglement with {target.mention}!\n\n"
                f"**Benefits:**\n"
                f"• Shared residue generation\n"
                f"• Synchronized quantum fields\n"
                f"• Bonus coherence buildup\n\n"
                f"React with ✅ to accept or ❌ to decline (30 seconds)"
            ),
            color=discord.Color.purple()
        )
        message = await ctx.send(target.mention, embed=embed)

        # Add reactions
        await message.add_reaction('✅')
        await message.add_reaction('❌')

        # Wait for response
        def check(reaction, user):
            return (
                user == target and
                str(reaction.emoji) in ['✅', '❌'] and
                reaction.message.id == message.id
            )

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)

            if str(reaction.emoji) == '✅':
                # Create entanglement
                await self.create_entanglement(ctx.author.id, target.id)

                success_embed = discord.Embed(
                    title="⚛️ Quantum Entanglement Established!",
                    description=(
                        f"{ctx.author.mention} and {target.mention} are now quantum entangled!\n\n"
                        f"Your quantum fields are now synchronized."
                    ),
                    color=discord.Color.green()
                )
                await ctx.send(embed=success_embed)
            else:
                decline_embed = discord.Embed(
                    title="❌ Entanglement Declined",
                    description=f"{target.mention} declined the entanglement request.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=decline_embed)

        except asyncio.TimeoutError:
            timeout_embed = discord.Embed(
                title="⏰ Request Timeout",
                description="Entanglement request timed out.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=timeout_embed)

    @quantum.command(name='residue')
    async def check_residue(self, ctx: commands.Context):
        """Check your accumulated quantum residue"""
        field = await self.get_quantum_field(ctx.author.id)
        residue = field.get('accumulated_residue', 0)

        # Calculate residue components
        result = self.quantum.calculate_residue(
            residue,
            ResidueType.ENERGY,
            coupling=0.1
        )

        embed = discord.Embed(
            title="🌌 Quantum Residue Analysis",
            description=f"Total Accumulated: **{residue:.2f} units**",
            color=discord.Color.dark_purple()
        )

        # Residue breakdown
        embed.add_field(
            name="📊 Residue Components",
            value=(
                f"**Visible:** {result['visible_component']:.3f}\n"
                f"**Dark:** {result['dark_component']:.3f}\n"
                f"**Ratio:** 1 : {self.R_DARK:.3f}"
            ),
            inline=True
        )

        # Quantum effects
        effects = result['quantum_effects']
        embed.add_field(
            name="✨ Quantum Effects",
            value=(
                f"**Coherence:** {effects['coherence']:.3f}\n"
                f"**Entanglement:** {effects['entanglement']:.3f}\n"
                f"**Superposition:** {effects['superposition']:.3f}"
            ),
            inline=True
        )

        # Potential BloomCoin
        potential_bc = residue / self.R_DARK
        embed.add_field(
            name="💰 Potential BloomCoin",
            value=f"**{potential_bc:.2f} BC** (at 100% efficiency)",
            inline=True
        )

        # Add visualization
        residue_visual = self.create_residue_visualization(residue)
        embed.add_field(
            name="Residue Accumulation",
            value=residue_visual,
            inline=False
        )

        embed.set_footer(text=f"Observer: {ctx.author.name}")
        await ctx.send(embed=embed)

    @quantum.command(name='encrypt')
    async def quantum_encrypt(self, ctx: commands.Context, *, message: str):
        """
        Encrypt a message using quantum residue and NEXTHASH-256
        Uses LSB encoding with MRP channels
        """
        if len(message) > 100:
            await ctx.send("Message too long! Maximum 100 characters.")
            return

        # Get user's quantum field
        field = await self.get_quantum_field(ctx.author.id)
        residue = field.get('accumulated_residue', 0)

        if residue < 1:
            await ctx.send("You need at least 1 residue unit to encrypt messages!")
            return

        # Perform encryption
        # Generate quantum key from residue
        quantum_key = nexthash256_hex(f"{ctx.author.id}:{residue}:{message}")[:16]

        # XOR encryption with quantum key
        encrypted = ""
        for i, char in enumerate(message):
            key_char = quantum_key[i % len(quantum_key)]
            encrypted += chr(ord(char) ^ ord(key_char))

        # Convert to hex for display
        encrypted_hex = encrypted.encode('utf-8', errors='ignore').hex()

        # Consume residue
        await self.consume_residue(ctx.author.id, 1.0)

        embed = discord.Embed(
            title="🔐 Quantum Encrypted Message",
            description="Message encrypted using quantum residue",
            color=discord.Color.dark_blue()
        )

        embed.add_field(
            name="Original Length",
            value=f"{len(message)} characters",
            inline=True
        )

        embed.add_field(
            name="Encryption Method",
            value="NEXTHASH-256 + Quantum XOR",
            inline=True
        )

        embed.add_field(
            name="Residue Cost",
            value="1.0 unit",
            inline=True
        )

        embed.add_field(
            name="Encrypted Data",
            value=f"```{encrypted_hex[:100]}...```" if len(encrypted_hex) > 100 else f"```{encrypted_hex}```",
            inline=False
        )

        embed.add_field(
            name="Quantum Key (first 8 bytes)",
            value=f"`{quantum_key[:8]}********`",
            inline=False
        )

        embed.set_footer(text="Only you can decrypt this with your quantum signature")
        await ctx.send(embed=embed)

    @quantum.command(name='simulate')
    async def quantum_simulate(self, ctx: commands.Context, iterations: int = 100):
        """
        Run a quantum field simulation
        Demonstrates Kuramoto synchronization dynamics
        """
        if iterations < 10 or iterations > 1000:
            await ctx.send("Iterations must be between 10 and 1000")
            return

        embed = discord.Embed(
            title="🔬 Quantum Field Simulation",
            description=f"Running {iterations} iterations of Kuramoto dynamics...",
            color=discord.Color.blue()
        )
        message = await ctx.send(embed=embed)

        # Run simulation
        results = []
        for i in range(0, iterations, max(1, iterations // 10)):
            # Simulate Kuramoto order parameter evolution
            t = i / iterations * self.TAU
            r = (1 - np.exp(-t / 2)) * np.sin(t) ** 2
            results.append(r)

            # Update progress
            if i % (iterations // 10) == 0:
                progress = i / iterations
                embed.description = f"Simulating... {progress:.0%} complete"
                await message.edit(embed=embed)

        # Calculate statistics
        max_coherence = max(results)
        avg_coherence = sum(results) / len(results)
        final_coherence = results[-1]

        # Create result embed
        embed = discord.Embed(
            title="🔬 Simulation Complete",
            description=f"Simulated {iterations} iterations of quantum dynamics",
            color=discord.Color.green()
        )

        embed.add_field(
            name="📊 Results",
            value=(
                f"**Max Coherence:** {max_coherence:.3f}\n"
                f"**Average:** {avg_coherence:.3f}\n"
                f"**Final State:** {final_coherence:.3f}"
            ),
            inline=True
        )

        embed.add_field(
            name="🌀 Quantum Behavior",
            value=(
                f"**Oscillation Period:** {self.TAU:.3f}\n"
                f"**Damping Factor:** 0.5\n"
                f"**Coupling Strength:** K = 2"
            ),
            inline=True
        )

        # Visualize coherence evolution (simplified)
        graph = self.create_simple_graph(results)
        embed.add_field(
            name="📈 Coherence Evolution",
            value=graph,
            inline=False
        )

        embed.set_footer(text=f"Simulated by {ctx.author.name}")
        await message.edit(embed=embed)

    def calculate_coherence(self, field: dict) -> float:
        """Calculate quantum field coherence"""
        residue = field.get('accumulated_residue', 0)
        time_factor = field.get('last_interaction', 0)

        # Kuramoto-inspired coherence calculation
        base_coherence = np.tanh(residue / 10) * self.TAU
        time_decay = np.exp(-time_factor / 3600)  # Decay over 1 hour

        return base_coherence * time_decay

    def kuramoto_order_parameter(self, residue: float, coherence: float) -> float:
        """
        Calculate Kuramoto order parameter for synchronization
        r ∈ [0, 1] where 1 is perfect synchronization
        """
        K = 2.0  # Coupling strength (critical value)
        N = residue  # Number of oscillators proportional to residue

        # Order parameter calculation
        if N <= 0:
            return 0

        # Simplified Kuramoto dynamics
        r = np.tanh(K * coherence / self.TAU) * min(1, np.sqrt(N / 100))

        return min(1, max(0, r))

    def determine_quantum_state(self, coherence: float) -> str:
        """Determine current quantum state based on coherence"""
        ratio = coherence / self.TAU

        if ratio >= 0.9:
            return "⚡ Supercoherent"
        elif ratio >= 0.7:
            return "🌟 Highly Coherent"
        elif ratio >= 0.5:
            return "✨ Coherent"
        elif ratio >= 0.3:
            return "🌀 Partially Coherent"
        elif ratio >= 0.1:
            return "💫 Decoherent"
        else:
            return "⚫ Quantum Vacuum"

    def create_coherence_bar(self, coherence: float) -> str:
        """Create visual coherence bar"""
        max_coherence = self.TAU
        ratio = coherence / max_coherence
        filled = int(ratio * 10)
        empty = 10 - filled

        bar = "🟦" * filled + "⬜" * empty
        percentage = ratio * 100

        return f"{bar} {percentage:.1f}%"

    def create_residue_visualization(self, residue: float) -> str:
        """Create visual representation of residue accumulation"""
        levels = [
            (1000, "🌟"),
            (500, "💎"),
            (100, "💠"),
            (50, "🔷"),
            (10, "🔹"),
            (1, "▪️")
        ]

        visual = ""
        remaining = residue

        for threshold, symbol in levels:
            count = int(remaining // threshold)
            if count > 0:
                visual += symbol * min(count, 10)
                if count > 10:
                    visual += f" x{count}"
                visual += " "
                remaining %= threshold

        return visual if visual else "◾ (< 1 unit)"

    def create_simple_graph(self, data: list) -> str:
        """Create a simple ASCII graph"""
        if not data:
            return "No data"

        # Normalize data to 0-5 range
        max_val = max(data) if max(data) > 0 else 1
        normalized = [int(d / max_val * 5) for d in data]

        # Create graph lines
        lines = []
        for i in range(5, -1, -1):
            line = ""
            for val in normalized[:20]:  # Show first 20 points
                if val >= i:
                    line += "█"
                else:
                    line += "░"
            lines.append(line)

        return "```\n" + "\n".join(lines) + "\n```"

    async def get_quantum_field(self, user_id: int) -> dict:
        """Get or create user's quantum field"""
        # This would normally fetch from database
        # For now, return a mock field
        return {
            'accumulated_residue': random.uniform(0, 100),
            'energy_distribution': {
                'kinetic': random.uniform(20, 40),
                'potential': random.uniform(20, 40),
                'residual': random.uniform(20, 40)
            },
            'last_interaction': 0
        }

    async def reset_quantum_field(self, user_id: int):
        """Reset user's quantum field after collapse"""
        # Would update database
        pass

    async def consume_residue(self, user_id: int, amount: float):
        """Consume residue for quantum operations"""
        # Would update database
        pass

    async def update_balance(self, user_id: int, amount: float):
        """Update user's BloomCoin balance"""
        if not self.bot.db_pool:
            return

        async with self.bot.db_pool.acquire() as conn:
            await conn.execute('''
                UPDATE players
                SET balance = balance + $2
                WHERE user_id = $1
            ''', user_id, amount)

    async def get_entanglement(self, user_id: int) -> Optional[int]:
        """Get user's entanglement partner"""
        # Would fetch from database
        return None

    async def create_entanglement(self, user1_id: int, user2_id: int):
        """Create quantum entanglement between two users"""
        # Would update database
        pass

async def setup(bot):
    """Setup function for Discord.py 2.0+"""
    await bot.add_cog(QuantumCog(bot))