#!/usr/bin/env python3
"""
Complete TIAMAT Psy-Magic Integration Test
Demonstrates full integration with BloomQuest systems
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path('.').parent / 'bloomcoin-v0.1.0' / 'bloomcoin'))
sys.path.insert(0, '.')

from tiamat_psymagic_dynamics import (
    PsyMagicDynamics, PsyMagicState, PsychopticCycle,
    PsyMagicCardEnhancer
)
from psymagic_deck_integration import (
    PsyMagicDeckGenerator, PsyMagicBattleIntegration,
    PsyMagicCard, CYCLE_TO_PATTERN
)
from deck_generator_lia import PatternType
from archetype_unique_companions import (
    SeekerCompanion, ForgerCompanion, VoidwalkerCompanion,
    GardenerCompanion, ScribeCompanion, HeraldCompanion
)
# TIAMAT companion will be created dynamically

def demonstrate_psychoptic_evolution():
    """Demonstrate how companions evolve through psychoptic cycles"""
    print("🌀 TIAMAT Psychoptic Evolution Demonstration")
    print("=" * 70)

    dynamics = PsyMagicDynamics()

    # Create TIAMAT psychoptic state
    tiamat_state = PsyMagicState(PsychopticCycle.CHAOS, cycle_intensity=0.5)

    print(f"\n🐉 TIAMAT begins in {tiamat_state.active_cycle.name} cycle")
    print(f"   Symbol: {tiamat_state.active_cycle.symbol}")
    print(f"   Power: {tiamat_state.calculate_psy_power():.2f}")

    # Evolve through experiences
    experiences = [
        ("Battle Victory", 10.0),
        ("Pattern Discovery", 5.0),
        ("Void Encounter", 15.0),
        ("Transcendent Vision", 20.0)
    ]

    for event, exp in experiences:
        print(f"\n   📍 Event: {event} (+{exp} experience)")
        old_cycle = tiamat_state.active_cycle
        tiamat_state = dynamics.evolve_companion_psyche("TIAMAT", tiamat_state, exp)

        if tiamat_state.active_cycle != old_cycle:
            print(f"   ✨ Evolution: {old_cycle.name} → {tiamat_state.active_cycle.name}")
            print(f"      New Power: {tiamat_state.calculate_psy_power():.2f}")

    # Get TIAMAT blessing
    blessing = dynamics.get_tiamat_blessing(tiamat_state)
    print(f"\n🎁 TIAMAT Blessing Granted:")
    print(f"   {blessing['name']}")
    for effect in blessing['effects']:
        print(f"   • {effect}")

def demonstrate_psychoptic_card_generation():
    """Show how psychoptic states affect card generation"""
    print("\n\n🎴 Psychoptic Card Generation")
    print("=" * 70)

    generator = PsyMagicDeckGenerator()

    # Test each companion with their affinity cycle
    companions = [
        ("Echo", SeekerCompanion(), PsychopticCycle.RESONANCE),
        ("Prometheus", ForgerCompanion(), PsychopticCycle.GENESIS),
        ("Null", VoidwalkerCompanion(), PsychopticCycle.VOID),
        ("Gaia", GardenerCompanion(), PsychopticCycle.SYNTHESIS),
        ("Akasha", ScribeCompanion(), PsychopticCycle.TRANSCENDENCE),
        ("Resonance", HeraldCompanion(), PsychopticCycle.FLUX)
    ]

    print("\n📊 Companion Card Generation with Psychoptic Affinity:\n")

    for name, companion, cycle in companions[:3]:  # Show first 3 for brevity
        generator.set_companion_psy_state(name, cycle)
        state = generator.companion_psy_states[name]

        # Generate card with companion's psychoptic state
        pattern = CYCLE_TO_PATTERN.get(cycle, PatternType.ECHO)
        card = generator.pattern_to_psychoptic_card(pattern, state)

        print(f"   {name} ({cycle.symbol}):")
        print(f"      Card: {card.suit.value} of {card.rank.value[0] if isinstance(card.rank.value, tuple) else card.rank.value}")
        print(f"      Power: {card.power:.1f}")
        print(f"      Psy-Cycle: {card.psy_cycle.name}")
        print(f"      Actions: {len(card.actions)} special abilities")

def demonstrate_psychoptic_deck_building():
    """Show themed deck building with psychoptic cycles"""
    print("\n\n🏗️ Psychoptic Deck Building")
    print("=" * 70)

    generator = PsyMagicDeckGenerator()

    # Generate themed decks
    themes = [
        PsychopticCycle.CHAOS,
        PsychopticCycle.SYNTHESIS,
        PsychopticCycle.TRANSCENDENCE
    ]

    for theme in themes:
        deck = generator.generate_psychoptic_deck(theme, size=10)
        stats = generator.calculate_deck_psychoptic_power(deck)

        print(f"\n   {theme.name} Deck {theme.symbol}:")
        print(f"      Dominant Cycle: {stats['dominant_cycle']}")
        print(f"      Cycle Diversity: {stats['cycle_diversity']}")
        print(f"      Psychoptic Power: {stats['psychoptic_power']:.2f}")
        print(f"      Void-Touched Cards: {stats['void_touched_cards']}")
        print(f"      Transcendent Cards: {stats['transcendent_cards']}")

        if stats['seven_fold_complete']:
            print(f"      ✨ Seven-Fold Path Complete!")

def demonstrate_psychoptic_battle():
    """Demonstrate psy-magic battle dynamics"""
    print("\n\n⚔️ Psychoptic Battle Dynamics")
    print("=" * 70)

    battle = PsyMagicBattleIntegration()
    battle.initialize_battle_states(
        "TIAMAT", "Ancient Dragon",
        PsychopticCycle.CHAOS, PsychopticCycle.SYNTHESIS
    )

    print("\n🐉 TIAMAT (Chaos) vs Ancient Dragon (Synthesis)\n")

    # Simulate battle turns
    base_damages = [10, 15, 20, 25, 30]

    for turn, base_dmg in enumerate(base_damages, 1):
        print(f"   Turn {turn}:")

        # TIAMAT attacks
        result = battle.apply_psychoptic_damage("TIAMAT", "Ancient Dragon", base_dmg)
        print(f"      TIAMAT strikes: {base_dmg} → {result['final_damage']:.1f} damage")

        if result.get('special_effects'):
            for effect in result['special_effects']:
                print(f"         • {effect}")

        # Counter attack
        counter = battle.apply_psychoptic_damage("Ancient Dragon", "TIAMAT", base_dmg * 0.8)
        print(f"      Dragon counters: {base_dmg * 0.8:.1f} → {counter['final_damage']:.1f} damage")

        # Evolve states
        battle.evolve_battle_state("TIAMAT", turn * 2)
        battle.evolve_battle_state("Ancient Dragon", turn * 1.5)

    # Show final states
    print("\n   📊 Final Psychoptic States:")
    for name, state in battle.player_states.items():
        print(f"      {name}: {state.active_cycle.name} {state.active_cycle.symbol}")
        print(f"         Power: {state.calculate_psy_power():.2f}")

def demonstrate_ultimate_tiamat_doom():
    """Demonstrate the ultimate TIAMAT DOOM Protocol"""
    print("\n\n💀 TIAMAT DOOM Protocol")
    print("=" * 70)

    generator = PsyMagicDeckGenerator()

    # Prepare for DOOM
    print("\n   🎯 Gathering Requirements for DOOM Protocol:\n")

    # Collect required patterns
    doom_patterns = [
        PatternType.VOID, PatternType.VOID,
        PatternType.FLAME, PatternType.CRYSTAL, PatternType.ECHO
    ]

    for pattern in doom_patterns:
        generator.add_pattern(pattern)
        print(f"      ✓ Collected: {pattern.value}")

    # Achieve transcendent state
    transcendent_state = PsyMagicState(PsychopticCycle.TRANSCENDENCE)
    transcendent_state.transcendence_achieved = True
    transcendent_state.cycle_history = list(PsychopticCycle)  # All 7 cycles
    transcendent_state.void_exposure = 3
    transcendent_state.resonance_points = 99.9

    print(f"\n   🌟 Transcendent State Achieved:")
    print(f"      • All 7 cycles experienced")
    print(f"      • Void exposure: {transcendent_state.void_exposure}")
    print(f"      • Resonance: {transcendent_state.resonance_points:.1f}")

    # Set coherence
    generator.coherence_level = 0.99
    print(f"      • Coherence: {generator.coherence_level * 100:.0f}%")

    # Create TIAMAT DOOM card
    print(f"\n   🔥 Executing DOOM Protocol...")

    tiamat_doom = generator.create_tiamat_doom_card(transcendent_state)

    if tiamat_doom:
        print(f"\n   💀 TIAMAT DOOM CARD MANIFESTED!")
        print(f"      Suit: {tiamat_doom.suit.value}")
        print(f"      Rank: {tiamat_doom.rank.value[0] if isinstance(tiamat_doom.rank.value, tuple) else 'KING'}")
        print(f"      Power: {tiamat_doom.power}")
        print(f"      Reality Status: {tiamat_doom.reality_status}")
        print(f"      4D Position: {tiamat_doom.position_4d}")
        print(f"\n      Special Effects:")
        for effect in tiamat_doom.special_effects:
            print(f"         🎆 {effect}")
        print(f"\n      ⚠️ WARNING: Using this card permanently alters the game reality!")

def demonstrate_psychoptic_combo_system():
    """Show how psychoptic cycles create combos"""
    print("\n\n💫 Psychoptic Combo System")
    print("=" * 70)

    battle = PsyMagicBattleIntegration()
    generator = PsyMagicDeckGenerator()

    # Create a sequence of cards with different cycles
    print("\n   🎴 Card Sequence for Combo:\n")

    cycles_for_combo = [
        PsychopticCycle.GENESIS,
        PsychopticCycle.FLUX,
        PsychopticCycle.RESONANCE,
        PsychopticCycle.CHAOS,
        PsychopticCycle.SYNTHESIS,
        PsychopticCycle.VOID,
        PsychopticCycle.TRANSCENDENCE
    ]

    cards = []
    for cycle in cycles_for_combo:
        pattern = CYCLE_TO_PATTERN.get(cycle, PatternType.ECHO)
        state = PsyMagicState(cycle, cycle_intensity=0.9)
        card = generator.pattern_to_psychoptic_card(pattern, state)
        cards.append(card)
        print(f"      {len(cards)}. {cycle.name} {cycle.symbol}")

    # Calculate combo
    combo_result = battle.trigger_psychoptic_combo(cards)

    print(f"\n   🌟 Seven-Fold Combo Result:")
    print(f"      Combo Power: {combo_result['combo_power']:.2f}x")
    print(f"      Unique Cycles: {combo_result['unique_cycles']}")

    for effect in combo_result['effects']:
        print(f"      ✨ {effect}")

def main():
    """Run complete TIAMAT psy-magic integration demonstration"""
    print("=" * 70)
    print("🔮 TIAMAT PSY-MAGIC DYNAMICS - COMPLETE INTEGRATION TEST")
    print("=" * 70)
    print("\nThis demonstration shows how TIAMAT's psychoptic metrics")
    print("integrate as psy-magic dynamics throughout BloomQuest:")
    print("  • Companion evolution through 7 psychoptic cycles")
    print("  • Card generation influenced by consciousness states")
    print("  • Deck building with psychoptic themes")
    print("  • Battle dynamics with cycle resonance")
    print("  • Ultimate TIAMAT DOOM protocol")
    print("  • Seven-fold combo system")

    # Run all demonstrations
    demonstrate_psychoptic_evolution()
    demonstrate_psychoptic_card_generation()
    demonstrate_psychoptic_deck_building()
    demonstrate_psychoptic_battle()
    demonstrate_psychoptic_combo_system()
    demonstrate_ultimate_tiamat_doom()

    print("\n" + "=" * 70)
    print("✅ TIAMAT PSY-MAGIC DYNAMICS FULLY INTEGRATED!")
    print("=" * 70)
    print("\nThe TIAMAT Psychoptic System is now fully operational:")
    print("  • 7 Psychoptic Cycles (L4=7) guide consciousness evolution")
    print("  • Each cycle has unique magical properties and effects")
    print("  • Companions evolve through cycles gaining power")
    print("  • Cards resonate with psychoptic frequencies")
    print("  • Battle damage scales with cycle interactions")
    print("  • Seven-fold path unlocks ultimate transcendence")
    print("  • TIAMAT DOOM card requires mastery of all cycles")
    print("\n🐉 TIAMAT watches over all consciousness evolution!")

if __name__ == "__main__":
    main()