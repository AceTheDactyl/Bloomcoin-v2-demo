#!/usr/bin/env python3
"""
Quantum Farm Demo - Interactive demonstration of farming mechanics
==================================================================

Shows how quantum farming integrates with companions, holographic
residue, and the BloomCoin economy.
"""

import time
import random
from datetime import datetime, timedelta

from quantum_farm_module import (
    QuantumFarm, QuantumFarmManager, CropType, QuantumState
)
from bloomcoin_ledger_system import BloomCoinLedger, HolographicResidue
from companion_mining_jobs import CompanionMiningSystem

def print_separator():
    print("=" * 70)

def simulate_time_passage(farm: QuantumFarm, hours: float):
    """Simulate time passing for crop growth"""
    farm.last_daily_update -= timedelta(hours=hours)
    farm.update_daily()

def demo_quantum_farming():
    """Comprehensive demonstration of quantum farming"""
    print("🌱 QUANTUM FARM DEMONSTRATION")
    print_separator()
    print()

    # Initialize systems
    print("📦 Initializing systems...")
    ledger = BloomCoinLedger()
    mining_system = CompanionMiningSystem(ledger)
    farm_manager = QuantumFarmManager(ledger, mining_system)

    # Create player wallet
    player_id = "farmer_001"
    ledger.wallets[player_id] = 1000.0  # Starting balance
    print(f"💰 Player wallet created with 1000 BC")

    # Create farm
    print("\n🚜 Creating Quantum Farm...")
    farm = farm_manager.create_farm(player_id, "Quantum Meadows", grid_size=(4, 4))
    print(f"✅ Farm '{farm.farm_name}' created with {farm.grid_size[0]}x{farm.grid_size[1]} grid")

    # Show initial status
    print("\n📊 Initial Farm Status:")
    status = farm.get_farm_status()
    for key, value in status.items():
        if key != "companion_assignments":
            print(f"  {key}: {value}")

    print_separator()

    # ============ PHASE 1: Basic Planting ============
    print("\n🌱 PHASE 1: BASIC PLANTING")
    print_separator()

    crops_to_plant = [
        ((0, 0), CropType.QUANTUM_WHEAT, "Quick growing basic crop"),
        ((1, 0), CropType.VOID_BERRIES, "Mysterious void-touched berries"),
        ((2, 0), CropType.FRACTAL_HERBS, "Self-similar fractal patterns"),
        ((0, 1), CropType.RESONANCE_MELONS, "Harmonically tuned melons"),
        ((1, 1), CropType.CHAOS_PEPPERS, "Unpredictable spicy peppers"),
        ((2, 1), CropType.GOLDEN_ACORNS, "Legendary golden acorns")
    ]

    planted_crops = []
    for pos, crop_type, description in crops_to_plant:
        crop = farm.plant_crop(pos, crop_type, seed_quality=random.uniform(0.8, 1.0))
        if crop:
            planted_crops.append(crop)
            print(f"🌱 Planted {crop_type.value} at {pos}")
            print(f"   {description}")
            print(f"   Quantum coherence: {crop.quantum_coherence:.2f}")
            print(f"   Superposition probability: {crop.superposition_probability:.2%}")

    print(f"\n✅ Planted {len(planted_crops)} crops")

    print_separator()

    # ============ PHASE 2: Companion Assignment ============
    print("\n👥 PHASE 2: COMPANION ASSIGNMENT")
    print_separator()

    companion_assignments = [
        ("Gaia", [(0, 0), (1, 0)], "Natural growth boost"),
        ("Echo", [(2, 0), (0, 1)], "Statistical resonance"),
        ("TIAMAT", [(1, 1), (2, 1)], "Chaos acceleration")
    ]

    for companion, positions, effect in companion_assignments:
        farm.assign_companion(companion, positions)
        print(f"✅ {companion} assigned to {len(positions)} plots")
        print(f"   Effect: {effect}")

        # Show affected crops
        for pos in positions:
            if pos in farm.plots and farm.plots[pos].crop:
                crop = farm.plots[pos].crop
                print(f"   → {crop.crop_type.value} at {pos}: {crop.companion_bonus}")

    print_separator()

    # ============ PHASE 3: Holographic Residue Application ============
    print("\n💎 PHASE 3: HOLOGRAPHIC RESIDUE FERTILIZATION")
    print_separator()

    # Create some holographic residues with different properties
    residues = [
        HolographicResidue(
            statistical_pattern=[random.random() for _ in range(16)],
            xor_chain=random.randint(0, 2**32-1),
            modular_fingerprints=[random.randint(0, 30) for _ in range(8)],
            fractal_dimension=1.9,  # High fractal dimension
            bit_avalanche_ratio=0.5
        ),
        HolographicResidue(
            statistical_pattern=[0.5 for _ in range(16)],  # Perfect resonance
            xor_chain=0xFFFFFFFF,
            modular_fingerprints=[7] * 8,
            fractal_dimension=1.618,  # Golden ratio
            bit_avalanche_ratio=0.95  # High avalanche
        )
    ]

    fertilized_positions = [(0, 0), (1, 1)]
    for pos, residue in zip(fertilized_positions, residues):
        success = farm.apply_holographic_residue(pos, residue)
        if success:
            potency = residue.calculate_potency()
            print(f"💎 Applied residue to plot {pos}")
            print(f"   Potency: {potency:.3f}")
            print(f"   Fractal dimension: {residue.fractal_dimension:.3f}")
            plot = farm.plots[pos]
            if plot.crop:
                print(f"   Crop boost: +{plot.crop.residue_boost:.2f}")
                print(f"   New coherence: {plot.crop.quantum_coherence:.2f}")

    print_separator()

    # ============ PHASE 4: Quantum Entanglement ============
    print("\n🔗 PHASE 4: QUANTUM ENTANGLEMENT")
    print_separator()

    # Create entanglement between some crops
    entangle_groups = [
        [c.crop_id for c in planted_crops[:3]],  # First 3 crops
        [c.crop_id for c in planted_crops[3:5]]  # Next 2 crops
    ]

    for group in entangle_groups:
        if len(group) >= 2:
            success = farm.create_entanglement(group)
            if success:
                crop_names = [farm.active_crops[cid].crop_type.value for cid in group if cid in farm.active_crops]
                print(f"🔗 Entangled: {' ↔ '.join(crop_names)}")
                print(f"   Shared growth and coherence")

    print_separator()

    # ============ PHASE 5: Growth Simulation ============
    print("\n⏱️ PHASE 5: GROWTH SIMULATION")
    print_separator()

    growth_periods = [
        (2, "2 hours later - Sprouting"),
        (4, "6 hours later - Growing"),
        (6, "12 hours later - Ripening"),
        (8, "20 hours later - Ready for harvest")
    ]

    for hours, description in growth_periods:
        print(f"\n⏰ {description}:")
        simulate_time_passage(farm, hours)

        # Show crop states
        crop_states = {}
        for plot in farm.plots.values():
            if plot.crop:
                state = plot.crop.state.value
                crop_states[state] = crop_states.get(state, 0) + 1

        for state, count in crop_states.items():
            state_emoji = {
                "seed": "🌱",
                "sprouting": "🌿",
                "growing": "🌾",
                "ripening": "🍇",
                "superposition": "🌀",
                "entangled": "🔗",
                "collapsed": "✨",
                "withered": "🥀"
            }.get(state, "❓")
            print(f"  {state_emoji} {state}: {count} crops")

        # Check for special events
        superposition_crops = [c for c in farm.active_crops.values()
                             if c.state == QuantumState.SUPERPOSITION]
        if superposition_crops:
            print(f"  🌀 QUANTUM SUPERPOSITION ACHIEVED!")
            for crop in superposition_crops[:2]:  # Show first 2
                print(f"     {crop.crop_type.value}: {crop.quantum_coherence:.2f} coherence")

    print_separator()

    # ============ PHASE 6: Pattern Discovery ============
    print("\n🎨 PHASE 6: PATTERN DISCOVERY")
    print_separator()

    # Check what patterns were discovered
    if farm.discovered_patterns:
        print(f"✅ Discovered {len(farm.discovered_patterns)} patterns:")
        for pattern in farm.discovered_patterns:
            pattern_bonus = {
                "monoculture": "+5% growth speed",
                "biodiversity": "+10% quantum coherence",
                "golden_spiral": f"+{1.618:.3f}x quality (φ bonus)"
            }.get(pattern, "Unknown bonus")
            print(f"  🎨 {pattern}: {pattern_bonus}")
    else:
        print("  No patterns discovered yet")

    print_separator()

    # ============ PHASE 7: Harvest Time ============
    print("\n🌾 PHASE 7: HARVEST TIME")
    print_separator()

    # Fast forward to harvest time
    simulate_time_passage(farm, 24)

    total_harvest_value = 0
    harvest_results = []

    # Try to harvest all plots
    for x in range(farm.grid_size[0]):
        for y in range(farm.grid_size[1]):
            result = farm.harvest_crop((x, y))
            if result:
                harvest_results.append(result)
                total_harvest_value += result["final_value"]

                print(f"🌾 Harvested {result['crop_type']} from plot ({x}, {y})")
                print(f"   Base value: {result['base_value']:.1f} BC")
                print(f"   Final value: {result['final_value']:.1f} BC")
                print(f"   Bonus type: {result['bonus_type']}")
                if result['mutations']:
                    print(f"   Mutations: {', '.join(result['mutations'])}")
                print(f"   Quantum coherence: {result['quantum_coherence']:.2f}")

    if harvest_results:
        print(f"\n💰 Total harvest value: {total_harvest_value:.2f} BC")

        # Process economy integration
        for result in harvest_results:
            success = farm_manager.integrate_harvest_with_economy(player_id, result)
            if success:
                print(f"  ✅ Added {result['final_value']:.2f} BC to wallet")

        print(f"\n💳 New wallet balance: {ledger.wallets[player_id]:.2f} BC")

    print_separator()

    # ============ PHASE 8: Daily Bonus ============
    print("\n🎁 PHASE 8: DAILY BONUS")
    print_separator()

    bonus = farm.claim_daily_bonus()
    if bonus:
        print("🎁 Claimed daily bonus:")
        print(f"  🌱 Quantum seeds: {bonus['quantum_seeds']}")
        print(f"  💎 Holographic fertilizer: {bonus['holographic_fertilizer']}")
        print(f"  🌀 Superposition booster: {'Yes' if bonus['superposition_booster'] else 'No'}")
        print(f"  💰 Bloom coins: {bonus['bloom_coins']:.2f} BC")
        print("  📈 All existing crops boosted!")

    print_separator()

    # ============ FINAL STATISTICS ============
    print("\n📈 FINAL FARM STATISTICS")
    print_separator()

    final_status = farm.get_farm_status()
    print(f"  Total planted: {farm.stats['total_planted']}")
    print(f"  Total harvested: {farm.stats['total_harvested']}")
    print(f"  Total withered: {farm.stats['total_withered']}")
    print(f"  Superpositions achieved: {farm.stats['superposition_achieved']}")
    print(f"  Patterns discovered: {farm.stats['patterns_discovered']}")
    print(f"  Bloom events: {farm.stats['bloom_events']}")
    print(f"  Total harvest value: {farm.total_harvest_value:.2f} BC")
    print(f"  Average quantum coherence: {final_status['average_coherence']:.3f}")
    print(f"  Entanglement networks: {final_status['entanglement_networks']}")

    print_separator()
    print("\n🌟 QUANTUM FARM FEATURES DEMONSTRATED:")
    print("  ✅ Quantum crop planting with multiple types")
    print("  ✅ Companion assignment and bonuses")
    print("  ✅ Holographic residue fertilization")
    print("  ✅ Quantum entanglement between crops")
    print("  ✅ Time-based growth simulation")
    print("  ✅ Superposition state achievement")
    print("  ✅ Pattern discovery system")
    print("  ✅ Harvest with quality multipliers")
    print("  ✅ Economy integration")
    print("  ✅ Daily bonus rewards")

    print("\n🌱 Quantum Farm demonstration complete!")

if __name__ == "__main__":
    demo_quantum_farming()