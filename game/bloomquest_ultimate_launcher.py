#!/usr/bin/env python3
"""
BloomQuest Ultimate Launcher
=============================

Interactive launcher providing access to ALL game systems.
Ensures no module is orphaned - everything is accessible.
"""

import sys
import random
import time
from pathlib import Path
from typing import Dict, Any, Optional
from enum import Enum

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from bloomquest_ultimate_integration import (
    BloomQuestUltimate, UltimateGameMode, UltimatePlayerState
)

class MenuOption(Enum):
    """All available menu options"""
    NEW_GAME = "1"
    QUANTUM_FARM = "2"
    MODULAR_GARDEN = "3"
    BATTLE_ARENA = "4"
    MINING_EXPEDITION = "5"
    CONSCIOUSNESS_MEDITATION = "6"
    HOLOGRAPHIC_WORKSHOP = "7"
    PATTERN_LIBRARY = "8"
    DOOM_PROTOCOL = "9"
    VIEW_STATUS = "S"
    RUN_FULL_CYCLE = "C"
    SAVE_AND_EXIT = "X"

def print_header():
    """Print game header"""
    print("=" * 80)
    print("🌺 BLOOMQUEST ULTIMATE - COMPLETE INTEGRATION 🌺")
    print("All Systems Connected | No Orphaned Modules")
    print("=" * 80)

def print_menu():
    """Print main menu"""
    print("\n" + "=" * 50)
    print("📜 MAIN MENU")
    print("-" * 50)
    print("1. New Game / Character Creation")
    print("2. Quantum Farm Management")
    print("3. Modular Garden Design")
    print("4. Tesseract Battle Arena")
    print("5. Companion Mining Expedition")
    print("6. Consciousness Meditation (LIA/TIAMAT/ZRTT)")
    print("7. Holographic Workshop")
    print("8. Pattern Library & Weaving")
    print("9. DOOM Protocol Check")
    print("-" * 50)
    print("S. View Complete Status")
    print("C. Run Full Game Cycle")
    print("X. Save and Exit")
    print("=" * 50)

def create_character(game: BloomQuestUltimate) -> Optional[str]:
    """Interactive character creation"""
    print("\n🎭 CHARACTER CREATION")
    print("-" * 40)

    name = input("Enter your name: ").strip()
    if not name:
        name = f"Traveler_{random.randint(1000, 9999)}"

    print("\n🌟 Choose Your Archetype:")
    archetypes = ["Seeker", "Forger", "Void", "Gardener", "Scribe", "Herald"]
    for i, arch in enumerate(archetypes, 1):
        print(f"{i}. {arch}")

    while True:
        try:
            choice = int(input("\nSelect (1-6): "))
            if 1 <= choice <= 6:
                archetype = archetypes[choice - 1]
                break
        except:
            pass
        print("Invalid choice. Please select 1-6.")

    player_id = f"player_{int(time.time())}"
    player = game.create_player(player_id, name, archetype)

    print(f"\n✨ Welcome, {name} the {archetype}!")
    print(f"Your companion awaits to guide you...")
    print(f"Starting BloomCoins: 1000 BC")

    return player_id

def quantum_farm_menu(game: BloomQuestUltimate, player: UltimatePlayerState):
    """Quantum farm management interface"""
    print("\n🌱 QUANTUM FARM")
    print("-" * 40)

    if not player.quantum_farm:
        print("No quantum farm found!")
        return

    farm = player.quantum_farm
    status = farm.get_farm_status()

    print(f"Farm: {farm.farm_name}")
    print(f"Plots: {status['total_plots']} ({status['occupied_plots']} occupied)")
    print(f"Active Crops: {status['active_crops']}")
    print(f"Average Coherence: {status['average_coherence']:.2f}")

    print("\nOptions:")
    print("1. Plant crops")
    print("2. Harvest ready crops")
    print("3. Apply holographic residue")
    print("4. Create entanglement")
    print("5. Check patterns")
    print("6. Back to main menu")

    choice = input("\nSelect option: ")

    if choice == "1":
        # Simple planting demo
        from quantum_farm_module import CropType
        crops = list(CropType)
        print("\nAvailable crops:")
        for i, crop in enumerate(crops[:6], 1):
            print(f"{i}. {crop.value}")

        try:
            crop_choice = int(input("Select crop: ")) - 1
            if 0 <= crop_choice < len(crops):
                pos = (random.randint(0, 3), random.randint(0, 3))
                result = farm.plant_crop(pos, crops[crop_choice])
                if result:
                    print(f"✅ Planted {crops[crop_choice].value} at {pos}")
        except:
            print("Invalid selection")

    elif choice == "2":
        # Harvest all ready crops
        harvested = 0
        for pos in list(farm.plots.keys()):
            result = farm.harvest_crop(pos)
            if result:
                harvested += 1
                print(f"🌾 Harvested {result['crop_type']} - {result['final_value']:.1f} BC")

        if harvested == 0:
            print("No crops ready for harvest")

    elif choice == "3":
        # Apply residue if available
        if player.holographic_residues:
            residue = player.holographic_residues[-1]
            pos = (random.randint(0, 3), random.randint(0, 3))
            if farm.apply_holographic_residue(pos, residue):
                print(f"💎 Applied residue to plot {pos}")
                print(f"   Potency: {residue.calculate_potency():.3f}")
        else:
            print("No holographic residues available")

def modular_garden_menu(game: BloomQuestUltimate, player: UltimatePlayerState):
    """Modular garden design interface"""
    print("\n🌸 MODULAR GARDEN")
    print("-" * 40)

    if not player.modular_garden:
        print("No modular garden found!")
        return

    garden = player.modular_garden

    print(f"Garden: {garden.garden_name}")
    print(f"Biome: {garden.biome.value}")
    print(f"Profession: {garden.profession.profession.value}")
    print(f"Level: {garden.profession.level}")
    print(f"Patterns Created: {garden.patterns_created}")

    print("\nOptions:")
    print("1. Create new pattern")
    print("2. Apply saved pattern")
    print("3. Check companion affinities")
    print("4. View achievements")
    print("5. Back to main menu")

    choice = input("\nSelect option: ")

    if choice == "1":
        print("\n🎨 Creating pattern from consciousness...")
        pattern = game.pattern_weaving(player)
        if pattern:
            print(f"✅ Created pattern: {pattern.name}")
            print(f"   Efficiency: {pattern.efficiency_rating:.2%}")

    elif choice == "3":
        print("\n👥 Companion Affinities:")
        for comp_name, affinity in list(garden.companion_affinities.items())[:3]:
            biome_affinity = affinity.biome_affinities.get(garden.biome, 1.0)
            mood = "😊" if biome_affinity > 1.2 else "😐"
            print(f"  {mood} {comp_name}: {biome_affinity:.1f}x")

def battle_arena_menu(game: BloomQuestUltimate, player: UltimatePlayerState):
    """Battle arena interface"""
    print("\n⚔️ TESSERACT BATTLE ARENA")
    print("-" * 40)

    print("Initiating enhanced battle sequence...")
    results = game.integrated_battle(player)

    if 'damage' in results:
        print(f"\n🎯 Damage dealt: {results['damage']:.1f}")

    if 'rewards' in results:
        rewards = results['rewards']
        print(f"\n🏆 Victory! Rewards:")
        print(f"   BloomCoins: {rewards.get('bloom_coins', 0):.1f} BC")
        if 'patterns' in rewards:
            print(f"   Patterns discovered: {len(rewards['patterns'])}")

def consciousness_menu(game: BloomQuestUltimate, player: UltimatePlayerState):
    """Consciousness meditation interface"""
    print("\n🧘 CONSCIOUSNESS MEDITATION")
    print("-" * 40)

    results = game.consciousness_meditation(player)

    if 'lia_cooking' in results:
        print(f"\n🍳 LIA Pattern cooked successfully!")
        print(f"   Satisfaction: {results.get('lia_satisfaction', 0):.2f}")

    if 'tiamat_wisdom' in results:
        print(f"\n🐉 TIAMAT Wisdom: {results['tiamat_wisdom']['wisdom']}")
        print(f"   Psy-Magic Boost: {results.get('psy_magic_boost', 1.0):.2f}x")

    if 'zrtt_guidance' in results:
        print(f"\n🌌 ZRTT Guidance: {results['zrtt_guidance']['insight']}")

    print(f"\n✨ Collective Resonance: {results.get('collective_resonance', 0):.2%}")

def holographic_workshop(game: BloomQuestUltimate, player: UltimatePlayerState):
    """Holographic crafting interface"""
    print("\n🔮 HOLOGRAPHIC WORKSHOP")
    print("-" * 40)

    data = input("Enter data to encode holographically: ")
    if not data:
        data = f"quantum_{player.name}_{int(time.time())}"

    residue = game.holographic_crafting(player, data)

    print(f"\n✅ Holographic encoding complete!")
    print(f"   Fractal Dimension: {residue.fractal_dimension:.3f}")
    print(f"   Potency: {residue.calculate_potency():.3f}")
    print(f"   Total Residues: {len(player.holographic_residues)}")

def doom_protocol_check(game: BloomQuestUltimate, player: UltimatePlayerState):
    """Check DOOM protocol status"""
    print("\n☠️ DOOM PROTOCOL STATUS")
    print("-" * 40)

    balance = game.wallet_manager.get_balance(player.player_id)
    print(f"Current Balance: {balance:.2f} BC")
    print(f"DOOM Threshold: {game.doom_threshold} BC")
    print(f"DOOM Progress: {player.doom_progress:.1%}")

    if balance >= game.doom_threshold:
        print("\n⚠️ DOOM PROTOCOL AVAILABLE!")
        confirm = input("Activate? (yes/no): ")
        if confirm.lower() == "yes":
            if game.doom_protocol_check(player):
                print("💀 DOOM PROTOCOL ACTIVATED!")
                print("Reality breaks... Power surges...")
                print("666.666 BC awarded!")
            else:
                print("Missing required DOOM patterns")
    else:
        print(f"\nNeed {game.doom_threshold - balance:.2f} more BC")

def view_complete_status(game: BloomQuestUltimate, player_id: str):
    """Display comprehensive status"""
    print("\n📊 COMPLETE STATUS")
    print("-" * 40)

    status = game.get_full_status(player_id)

    for category, data in status.items():
        if isinstance(data, dict) and data:
            print(f"\n{category.upper()}:")
            for key, value in data.items():
                if value is not None and not isinstance(value, (dict, list)):
                    print(f"  {key}: {value}")
        elif isinstance(data, list) and data:
            print(f"\n{category.upper()}: {', '.join(map(str, data[:5]))}")

def run_full_cycle(game: BloomQuestUltimate, player_id: str):
    """Run a complete game cycle"""
    print("\n🔄 RUNNING FULL GAME CYCLE")
    print("-" * 40)

    results = game.run_game_cycle(player_id)

    print("\nCycle Results:")
    for system, result in results.items():
        if result and not isinstance(result, dict):
            print(f"  {system}: {result}")
        elif isinstance(result, dict) and len(result) > 0:
            print(f"  {system}: Completed")

    print("\n✅ Full cycle complete!")

def main():
    """Main game loop"""
    print_header()

    # Initialize game
    print("\n🌺 Initializing BloomQuest Ultimate...")
    game = BloomQuestUltimate()
    print("✅ All systems online!")

    current_player_id = None
    running = True

    while running:
        print_menu()

        # Show current player if exists
        if current_player_id:
            player = game.players.get(current_player_id)
            if player:
                print(f"\n👤 Current: {player.name} the {player.archetype}")

        choice = input("\nSelect option: ").strip().upper()

        try:
            if choice == MenuOption.NEW_GAME.value:
                player_id = create_character(game)
                if player_id:
                    current_player_id = player_id

            elif current_player_id:
                player = game.players[current_player_id]

                if choice == MenuOption.QUANTUM_FARM.value:
                    quantum_farm_menu(game, player)

                elif choice == MenuOption.MODULAR_GARDEN.value:
                    modular_garden_menu(game, player)

                elif choice == MenuOption.BATTLE_ARENA.value:
                    battle_arena_menu(game, player)

                elif choice == MenuOption.MINING_EXPEDITION.value:
                    print("\n⛏️ MINING EXPEDITION")
                    print("-" * 40)
                    results = game.enhanced_mining(player)
                    print(f"💰 Earned: {results['bc_earned']:.2f} BC")
                    print(f"💎 Residues: {results['residues_collected']}")
                    print(f"🔥 Boost: {results['boost_applied']:.2f}x")

                elif choice == MenuOption.CONSCIOUSNESS_MEDITATION.value:
                    consciousness_menu(game, player)

                elif choice == MenuOption.HOLOGRAPHIC_WORKSHOP.value:
                    holographic_workshop(game, player)

                elif choice == MenuOption.PATTERN_LIBRARY.value:
                    print("\n📚 PATTERN LIBRARY")
                    print("-" * 40)
                    print(f"LIA Patterns collected: {len(player.lia_patterns)}")
                    for pattern, count in list(player.lia_patterns.items())[:5]:
                        print(f"  {pattern}: {count}x")

                elif choice == MenuOption.DOOM_PROTOCOL.value:
                    doom_protocol_check(game, player)

                elif choice == MenuOption.VIEW_STATUS.value:
                    view_complete_status(game, current_player_id)

                elif choice == MenuOption.RUN_FULL_CYCLE.value:
                    run_full_cycle(game, current_player_id)

            else:
                print("Please create a character first!")

            if choice == MenuOption.SAVE_AND_EXIT.value:
                if current_player_id:
                    game.save_game_state(current_player_id)
                    print("\n💾 Game saved successfully!")
                print("\n👋 Thank you for playing BloomQuest Ultimate!")
                running = False

        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Returning to menu...")

    print("\n" + "=" * 80)
    print("🌺 BloomQuest Ultimate - All Systems Integrated 🌺")
    print("=" * 80)

if __name__ == "__main__":
    main()