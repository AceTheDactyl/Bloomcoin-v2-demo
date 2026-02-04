#!/usr/bin/env python3
"""
Modular Garden System Demonstration
====================================

Comprehensive demo showing user gardens, pattern creation,
profession specialization, and companion affinities.
"""

import random
from modular_garden_system import (
    ModularGardenManager, UserGarden, PatternTemplate,
    GardenBiome, GardenProfession
)
from quantum_farm_module import CropType, QuantumState
from bloomcoin_ledger_system import BloomCoinLedger
from companion_mining_jobs import CompanionMiningSystem

def print_separator():
    print("=" * 70)

def demonstrate_modular_gardens():
    """Demonstrate all features of the modular garden system"""
    print("🌱 MODULAR GARDEN SYSTEM DEMONSTRATION")
    print_separator()
    print()

    # Initialize systems
    print("📦 Initializing core systems...")
    ledger = BloomCoinLedger()
    mining_system = CompanionMiningSystem(ledger)
    garden_manager = ModularGardenManager(ledger, mining_system)
    print("✅ Systems initialized")
    print()

    # ============ PHASE 1: User Garden Creation ============
    print("👤 PHASE 1: USER GARDEN CREATION")
    print_separator()

    # Create multiple users with different professions
    users = [
        ("alice_farmer", "Alice's Quantum Farm", GardenProfession.QUANTUM_BOTANIST, GardenBiome.QUANTUM_MEADOW),
        ("bob_void", "Bob's Void Garden", GardenProfession.VOID_CULTIVATOR, GardenBiome.VOID_SANCTUARY),
        ("carol_pattern", "Carol's Pattern Paradise", GardenProfession.PATTERN_WEAVER, GardenBiome.FRACTAL_GROVE),
        ("dave_chaos", "Dave's Chaos Field", GardenProfession.CHAOS_GARDENER, GardenBiome.CHAOS_WASTES),
        ("eve_golden", "Eve's Golden Sanctuary", GardenProfession.GOLDEN_ARCHITECT, GardenBiome.GOLDEN_SPIRAL)
    ]

    created_gardens = []
    for user_id, garden_name, profession, biome in users[:3]:  # Create first 3 for demo
        garden = garden_manager.create_user_garden(
            user_id, garden_name, biome, profession, grid_size=(4, 4)
        )
        created_gardens.append(garden)

        print(f"🌿 Created: {garden_name}")
        print(f"   Owner: {user_id}")
        print(f"   Profession: {profession.value}")
        print(f"   Biome: {biome.value}")
        print(f"   Starting skills: {garden.profession.skills_unlocked}")
        print(f"   Pattern slots: {garden.profession.pattern_slots}")
        print(f"   Unlocked biomes: {len(garden.unlocked_biomes)}")
        print()

    print_separator()

    # ============ PHASE 2: Pattern Creation ============
    print("\n🎨 PHASE 2: PATTERN CREATION")
    print_separator()

    alice_garden = created_gardens[0]

    # Alice creates an efficient pattern
    pattern1_positions = {
        (0, 0): CropType.QUANTUM_WHEAT,
        (1, 1): CropType.QUANTUM_WHEAT,
        (2, 0): CropType.ETHEREAL_CORN,
        (0, 2): CropType.ETHEREAL_CORN,
        (1, 2): CropType.FRACTAL_HERBS,
        (2, 1): CropType.FRACTAL_HERBS
    }

    pattern1_companions = {
        "Gaia": [(0, 0), (1, 1)],
        "Echo": [(2, 0), (0, 2)],
        "Akasha": [(1, 2), (2, 1)]
    }

    pattern1 = garden_manager.create_pattern(
        "alice_farmer",
        "Checkerboard Harmony",
        pattern1_positions,
        pattern1_companions,
        "An efficient checkerboard pattern for balanced growth",
        ["efficient", "balanced", "beginner-friendly"]
    )

    if pattern1:
        print(f"✅ Pattern created: {pattern1.name}")
        print(f"   ID: {pattern1.pattern_id}")
        print(f"   Efficiency: {pattern1.efficiency_rating:.2%}")
        print(f"   Crops: {len(pattern1.crop_positions)}")
        print(f"   Companions: {len(pattern1.companion_assignments)}")
        print(f"   Tags: {', '.join(pattern1.tags)}")

    # Carol (pattern specialist) creates a complex pattern
    carol_garden = created_gardens[2] if len(created_gardens) > 2 else None

    if carol_garden:
        # Fibonacci spiral pattern
        pattern2_positions = {
            (1, 1): CropType.GOLDEN_ACORNS,  # Center
            (1, 0): CropType.PHI_SPIRALS,
            (2, 1): CropType.PHI_SPIRALS,
            (1, 2): CropType.BLOOM_LOTUS,
            (0, 1): CropType.BLOOM_LOTUS,
            (2, 0): CropType.FRACTAL_HERBS,
            (2, 2): CropType.FRACTAL_HERBS,
            (0, 0): CropType.CRYSTAL_FLOWERS,
            (0, 2): CropType.CRYSTAL_FLOWERS
        }

        pattern2_companions = {
            "Gaia": [(1, 1)],  # Center focus
            "Resonance": [(1, 0), (2, 1), (1, 2), (0, 1)],  # Cardinal points
            "Echo": [(0, 0), (2, 0), (0, 2), (2, 2)]  # Corners
        }

        pattern2 = garden_manager.create_pattern(
            "carol_pattern",
            "Golden Spiral",
            pattern2_positions,
            pattern2_companions,
            "A golden ratio spiral pattern for maximum harmony",
            ["advanced", "golden-ratio", "high-yield", "artistic"]
        )

        if pattern2:
            print(f"\n✅ Advanced pattern created: {pattern2.name}")
            print(f"   Efficiency: {pattern2.efficiency_rating:.2%}")
            print(f"   Required profession: {pattern2.required_profession.value}")
            print(f"   Required level: {pattern2.required_level}")

    # Register pattern in global registry
    if pattern1:
        garden_manager.pattern_registry.register_pattern(pattern1)
        print(f"\n📚 Pattern registered globally")

    print_separator()

    # ============ PHASE 3: Companion Affinities ============
    print("\n👥 PHASE 3: COMPANION AFFINITIES")
    print_separator()

    for garden in created_gardens[:2]:
        print(f"\n🌿 {garden.garden_name} - Companion Affinities:")

        # Show top 3 companions for this biome
        affinities = []
        for comp_name, affinity in garden.companion_affinities.items():
            biome_bonus = affinity.biome_affinities.get(garden.biome, 1.0)
            affinities.append((comp_name, biome_bonus))

        affinities.sort(key=lambda x: x[1], reverse=True)

        for comp_name, bonus in affinities[:3]:
            mood_icon = "😊" if bonus > 1.2 else "😐" if bonus > 0.8 else "😔"
            print(f"   {mood_icon} {comp_name}: {bonus:.1f}x affinity")

            # Show crop preferences
            comp_affinity = garden.companion_affinities[comp_name]
            if comp_affinity.crop_affinities:
                preferred = list(comp_affinity.crop_affinities.keys())[:2]
                print(f"      Prefers: {', '.join(c.value for c in preferred)}")

    print_separator()

    # ============ PHASE 4: Applying Patterns ============
    print("\n🔧 PHASE 4: APPLYING PATTERNS")
    print_separator()

    if pattern1 and alice_garden:
        success = garden_manager.apply_pattern("alice_farmer", pattern1.pattern_id)
        if success:
            print(f"✅ Applied pattern '{pattern1.name}' to Alice's garden")

            # Show what was planted
            planted_count = sum(1 for plot in alice_garden.quantum_farm.plots.values() if plot.crop)
            print(f"   Crops planted: {planted_count}")
            print(f"   Active pattern: {alice_garden.active_pattern[:8]}...")

            # Update companion moods based on assignment
            for comp_name in pattern1.companion_assignments.keys():
                garden_manager.update_companion_mood("alice_farmer", comp_name, 0.2)
                print(f"   {comp_name} mood improved!")

    print_separator()

    # ============ PHASE 5: Profession Progression ============
    print("\n📈 PHASE 5: PROFESSION PROGRESSION")
    print_separator()

    # Simulate some harvests to gain experience
    print("Simulating harvests and experience gain...")

    for _ in range(5):
        # Alice harvests some crops
        positions = [(0, 0), (1, 1), (2, 0)]
        for pos in positions:
            # Plant and instantly grow for demo
            alice_garden.quantum_farm.plant_crop(pos, CropType.QUANTUM_WHEAT)
            if pos in alice_garden.quantum_farm.plots:
                plot = alice_garden.quantum_farm.plots[pos]
                if plot.crop:
                    plot.crop.growth_progress = 1.0
                    plot.crop.state = QuantumState.COLLAPSED

            # Harvest with profession bonuses
            result = garden_manager.process_harvest_with_profession("alice_farmer", pos)
            if result:
                alice_garden.profession.gain_experience(50)

    print(f"\n👤 Alice's Profession Progress:")
    print(f"   Profession: {alice_garden.profession.profession.value}")
    print(f"   Level: {alice_garden.profession.level}")
    print(f"   Experience: {alice_garden.profession.experience}")
    print(f"   Pattern slots: {alice_garden.profession.pattern_slots}")
    print(f"   Efficiency bonus: {alice_garden.profession.efficiency_bonus:.1%}")
    print(f"   Skills unlocked: {', '.join(alice_garden.profession.skills_unlocked)}")

    print_separator()

    # ============ PHASE 6: Biome Unlocking ============
    print("\n🌍 PHASE 6: BIOME UNLOCKING")
    print_separator()

    # Check what biomes Alice can unlock
    print("Checking biome unlock requirements for Alice...")

    potential_biomes = [
        GardenBiome.FRACTAL_GROVE,
        GardenBiome.ETHEREAL_HIGHLANDS,
        GardenBiome.CRYSTAL_TERRACES
    ]

    for biome in potential_biomes:
        can_unlock = garden_manager.unlock_biome("alice_farmer", biome)
        status = "✅ Unlocked!" if can_unlock else "❌ Requirements not met"
        print(f"   {biome.value}: {status}")

    print(f"\n📍 Total unlocked biomes: {len(alice_garden.unlocked_biomes)}")
    for biome in alice_garden.unlocked_biomes:
        print(f"   • {biome.value}")

    print_separator()

    # ============ PHASE 7: Pattern Search & Community ============
    print("\n🔍 PHASE 7: PATTERN SEARCH & COMMUNITY")
    print_separator()

    # Search for patterns
    print("Searching pattern registry...")

    # Search for efficient patterns
    efficient_patterns = garden_manager.pattern_registry.search_patterns(
        tags=["efficient"],
        min_efficiency=0.5
    )

    print(f"Found {len(efficient_patterns)} efficient patterns:")
    for pattern in efficient_patterns:
        print(f"   📋 {pattern.name}")
        print(f"      Creator: {pattern.creator}")
        print(f"      Efficiency: {pattern.efficiency_rating:.2%}")
        print(f"      Times used: {pattern.times_used}")

    # Rate a pattern
    if pattern1:
        for _ in range(5):  # Simulate 5 ratings
            rating = random.uniform(4.0, 5.0)
            garden_manager.pattern_registry.rate_pattern(pattern1.pattern_id, rating)

        print(f"\n⭐ Community rated '{pattern1.name}':")
        print(f"   Rating: {pattern1.community_rating:.2f}/5.0")
        print(f"   Times used: {pattern1.times_used}")

    print_separator()

    # ============ PHASE 8: Garden Statistics ============
    print("\n📊 PHASE 8: GARDEN STATISTICS")
    print_separator()

    for garden in created_gardens:
        print(f"\n🌿 {garden.garden_name}:")
        print(f"   Total harvests: {garden.total_harvests}")
        print(f"   Total earnings: {garden.total_earnings:.2f} BC")
        print(f"   Patterns created: {garden.patterns_created}")
        print(f"   Perfect harvests: {garden.perfect_harvests}")
        print(f"   Biome bonuses: {garden.biome_bonuses_earned:.2f} BC")
        print(f"   Achievements: {len(garden.achievements)}")

        if garden.achievements:
            print(f"   🏆 {', '.join(list(garden.achievements)[:3])}")

    print_separator()

    # ============ PHASE 9: Save & Load Test ============
    print("\n💾 PHASE 9: SAVE & LOAD TEST")
    print_separator()

    # Save Alice's garden
    print("Saving Alice's garden...")
    garden_manager.save_garden("alice_farmer")
    print("✅ Garden saved successfully")

    # Simulate clearing memory
    del garden_manager.user_gardens["alice_farmer"]
    print("🗑️ Garden removed from memory")

    # Load it back
    print("Loading Alice's garden...")
    loaded_garden = garden_manager.load_garden("alice_farmer")

    if loaded_garden:
        print("✅ Garden loaded successfully!")
        print(f"   Name: {loaded_garden.garden_name}")
        print(f"   Level: {loaded_garden.profession.level}")
        print(f"   Total earnings: {loaded_garden.total_earnings:.2f} BC")
        print(f"   Patterns saved: {len(loaded_garden.saved_patterns)}")
        print(f"   Last save: {loaded_garden.last_save}")

    print_separator()

    # ============ PHASE 10: Leaderboards ============
    print("\n🏆 PHASE 10: LEADERBOARDS")
    print_separator()

    categories = ["earnings", "level", "patterns", "harvests"]

    for category in categories:
        leaderboard = garden_manager.get_leaderboard(category)
        if leaderboard:
            print(f"\n📊 Top {category.capitalize()}:")
            for i, (user_id, value) in enumerate(leaderboard[:3], 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
                garden = garden_manager.user_gardens.get(user_id)
                name = garden.garden_name if garden else user_id
                print(f"   {medal} {name}: {value:.0f}")

    print_separator()

    # ============ FINAL SUMMARY ============
    print("\n✨ MODULAR GARDEN SYSTEM FEATURES DEMONSTRATED:")
    print("  ✅ User-specific gardens with different professions")
    print("  ✅ Pattern creation and efficiency calculation")
    print("  ✅ Global pattern registry and sharing")
    print("  ✅ Companion-biome affinity system")
    print("  ✅ Profession progression and skill unlocks")
    print("  ✅ Biome unlocking and requirements")
    print("  ✅ Pattern search and community rating")
    print("  ✅ Comprehensive statistics tracking")
    print("  ✅ Save/load system for persistence")
    print("  ✅ Leaderboards and achievements")

    print("\n🌱 Modular Garden System demonstration complete!")

if __name__ == "__main__":
    demonstrate_modular_gardens()