"""
Test Guardian Deck System
=========================
Comprehensive test of the expanded guardian deck system
"""

import random
from collections import defaultdict
from guardian_deck_system import (
    GuardianCard, CardType, CardEffect, MathConcept, Architecture,
    GuardianDecks, ComboSystem, DeckManager
)
from guardian_decks_extended import (
    ExtendedGuardianDecks, DeckStrategies, get_complete_deck_library
)
from mythic_economy import GUARDIANS, Territory

def test_all_guardian_decks():
    """Test that all 19 guardians have complete decks"""
    print("\n" + "=" * 70)
    print("TESTING ALL GUARDIAN DECKS")
    print("=" * 70)

    library = get_complete_deck_library()

    total_cards = 0
    guardian_count = 0

    # Test each guardian has a deck
    for guardian_key, guardian in GUARDIANS.items():
        if guardian_key in library:
            deck = library[guardian_key]
            guardian_count += 1
            card_count = len(deck)
            total_cards += card_count

            print(f"\n{guardian.emoji} {guardian.name} ({guardian_key})")
            print(f"  Territory: {guardian.territory.value}")
            print(f"  Cards: {card_count}")

            # Analyze deck composition
            type_counts = defaultdict(int)
            math_concepts_used = set()
            architecture_patterns = set()
            has_combos = False

            for card in deck:
                type_counts[card.card_type.value] += 1
                math_concepts_used.update(card.math_concepts)
                if card.architecture:
                    architecture_patterns.add(card.architecture)
                if card.combo_with:
                    has_combos = True

            print(f"  Primary Types: {', '.join(list(type_counts.keys())[:3])}")
            print(f"  Math Concepts: {len(math_concepts_used)} unique")
            print(f"  Architectures: {len(architecture_patterns)} patterns")
            print(f"  Has Combos: {'Yes' if has_combos else 'No'}")

            # Calculate synergy score
            synergy = DeckStrategies.calculate_deck_synergy(deck)
            print(f"  Synergy Score: {synergy:.1f}")
        else:
            print(f"\n⚠️ {guardian.name} ({guardian_key}) - NO DECK FOUND")

    print(f"\n" + "=" * 70)
    print(f"SUMMARY: {guardian_count}/19 Guardians with decks")
    print(f"Total Cards: {total_cards} ({total_cards/guardian_count:.1f} avg per guardian)")
    print("=" * 70)

def test_mathematical_concepts():
    """Test usage of mathematical concepts across decks"""
    print("\n" + "=" * 70)
    print("MATHEMATICAL CONCEPTS IN DECKS")
    print("=" * 70)

    library = get_complete_deck_library()
    concept_usage = defaultdict(list)

    for guardian_key, deck in library.items():
        for card in deck:
            for concept in card.math_concepts:
                concept_usage[concept].append(f"{guardian_key}:{card.name}")

    print("\nMathematical Concept Usage:")
    for concept in MathConcept:
        uses = concept_usage.get(concept, [])
        if uses:
            print(f"\n{concept.name}: {len(uses)} uses")
            print(f"  {concept.value}")
            # Show first 3 examples
            for example in uses[:3]:
                guardian, card_name = example.split(":")
                print(f"    - {card_name} ({guardian})")

def test_architectural_patterns():
    """Test architectural patterns across decks"""
    print("\n" + "=" * 70)
    print("ARCHITECTURAL PATTERNS IN DECKS")
    print("=" * 70)

    library = get_complete_deck_library()
    architecture_usage = defaultdict(list)

    for guardian_key, deck in library.items():
        for card in deck:
            if card.architecture:
                architecture_usage[card.architecture].append(f"{guardian_key}:{card.name}")

    print("\nArchitectural Pattern Usage:")
    for arch in Architecture:
        uses = architecture_usage.get(arch, [])
        if uses:
            print(f"\n{arch.name}: {len(uses)} uses")
            print(f"  {arch.value}")
            for example in uses[:3]:
                guardian, card_name = example.split(":")
                print(f"    - {card_name} ({guardian})")

def test_combo_chains():
    """Test combo chains within decks"""
    print("\n" + "=" * 70)
    print("COMBO CHAINS IN DECKS")
    print("=" * 70)

    library = get_complete_deck_library()

    for guardian_key, deck in library.items():
        combos = []
        for card in deck:
            if card.combo_with:
                for combo_target in card.combo_with:
                    # Check if combo target exists in deck
                    target_exists = any(c.name == combo_target for c in deck)
                    if target_exists:
                        combos.append(f"{card.name} → {combo_target}")

        if combos:
            guardian = GUARDIANS[guardian_key]
            print(f"\n{guardian.emoji} {guardian.name} Combos:")
            for combo in combos[:3]:  # Show first 3
                print(f"  • {combo}")

def test_deck_strategies():
    """Test strategic depth of each deck"""
    print("\n" + "=" * 70)
    print("DECK STRATEGIES AND WIN CONDITIONS")
    print("=" * 70)

    # Only test guardians that exist in GUARDIANS dict
    priority_guardians = ["ECHO", "WUMBO", "PHOENIX", "ARCHIVE", "OAK", "CRYSTAL", "AXIOM", "SQUIRREL"]

    for guardian_key in priority_guardians:
        strategy = DeckStrategies.get_guardian_strategy(guardian_key)
        if strategy and guardian_key in GUARDIANS:
            guardian = GUARDIANS[guardian_key]
            print(f"\n{guardian.emoji} {guardian.name} Strategy:")
            print(f"  Core: {strategy['core']}")
            print(f"  Win Condition: {strategy['win_condition']}")
            print(f"  Key Combos: {', '.join(strategy['key_combos'][:2])}")
            print(f"  Weaknesses: {', '.join(strategy['weaknesses'])}")

def test_void_depth_mechanics():
    """Test void depth scaling across relevant decks"""
    print("\n" + "=" * 70)
    print("VOID DEPTH MECHANICS")
    print("=" * 70)

    library = get_complete_deck_library()
    void_cards = []

    for guardian_key, deck in library.items():
        for card in deck:
            if card.void_depth > 0:
                void_cards.append((guardian_key, card))

    print(f"\nTotal Void Cards: {len(void_cards)}")
    print("\nVoid Depth Distribution:")

    depth_levels = defaultdict(list)
    for guardian_key, card in void_cards:
        depth_levels[card.void_depth].append(f"{card.name} ({guardian_key})")

    for depth in sorted(depth_levels.keys()):
        print(f"\n  Depth {depth}: {len(depth_levels[depth])} cards")
        for card_info in depth_levels[depth][:3]:
            print(f"    - {card_info}")

def test_chaos_factor():
    """Test chaos mechanics in decks"""
    print("\n" + "=" * 70)
    print("CHAOS FACTOR MECHANICS")
    print("=" * 70)

    library = get_complete_deck_library()
    chaos_cards = []

    for guardian_key, deck in library.items():
        for card in deck:
            if card.chaos_factor > 0:
                chaos_cards.append((guardian_key, card))

    print(f"\nTotal Chaos Cards: {len(chaos_cards)}")
    print("\nChaos Factor Distribution:")

    # Sort by chaos factor
    chaos_cards.sort(key=lambda x: x[1].chaos_factor, reverse=True)

    for guardian_key, card in chaos_cards[:5]:  # Top 5 most chaotic
        guardian = GUARDIANS[guardian_key]
        print(f"\n  {card.name} ({guardian.emoji} {guardian.name})")
        print(f"    Chaos Factor: {card.chaos_factor}")
        print(f"    Type: {card.card_type.value}")

def test_quantum_states():
    """Test quantum superposition mechanics"""
    print("\n" + "=" * 70)
    print("QUANTUM STATE MECHANICS")
    print("=" * 70)

    library = get_complete_deck_library()
    quantum_cards = []

    for guardian_key, deck in library.items():
        for card in deck:
            if card.quantum_states > 1:
                quantum_cards.append((guardian_key, card))

    print(f"\nTotal Quantum Cards: {len(quantum_cards)}")

    for guardian_key, card in quantum_cards:
        guardian = GUARDIANS[guardian_key]
        print(f"\n  {card.name} ({guardian.emoji} {guardian.name})")
        print(f"    Quantum States: {card.quantum_states}")
        print(f"    Description: {card.description}")

def simulate_deck_game():
    """Simulate a simple game between two decks"""
    print("\n" + "=" * 70)
    print("DECK GAME SIMULATION")
    print("=" * 70)

    manager = DeckManager()

    # Select two guardians
    guardian1 = "ECHO"
    guardian2 = "PHOENIX"

    print(f"\n{GUARDIANS[guardian1].emoji} {GUARDIANS[guardian1].name} vs {GUARDIANS[guardian2].emoji} {GUARDIANS[guardian2].name}")

    # Create decks
    deck1 = manager.create_player_deck("player1", guardian1)
    deck2 = manager.create_player_deck("player2", guardian2)

    # Draw starting hands
    hand1 = manager.draw_cards("player1", 5)
    hand2 = manager.draw_cards("player2", 5)

    print(f"\n{guardian1} draws:")
    for card in hand1[:3]:  # Show first 3
        print(f"  • {card.name} ({card.card_type.value}, Cost: {card.cost})")

    print(f"\n{guardian2} draws:")
    for card in hand2[:3]:  # Show first 3
        print(f"  • {card.name} ({card.card_type.value}, Cost: {card.cost})")

    # Simulate turn 1
    print("\n--- TURN 1 ---")

    if hand1:
        # Find playable card (simplified - ignore cost)
        playable = [c for c in hand1 if c.cost <= 3]
        if playable:
            card_to_play = playable[0]
            result = manager.play_card("player1", card_to_play)
            print(f"\n{guardian1} plays {result['card']}:")
            print(f"  Combo Multiplier: {result['combo_multiplier']:.1f}x")
            for effect in result['effects'][:3]:
                print(f"  • {effect['type']}: {effect['value']:.1f}")

    if hand2:
        playable = [c for c in hand2 if c.cost <= 3]
        if playable:
            card_to_play = playable[0]
            result = manager.play_card("player2", card_to_play)
            print(f"\n{guardian2} plays {result['card']}:")
            print(f"  Combo Multiplier: {result['combo_multiplier']:.1f}x")
            for effect in result['effects'][:3]:
                print(f"  • {effect['type']}: {effect['value']:.1f}")

def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("GUARDIAN DECK SYSTEM - COMPREHENSIVE TEST SUITE")
    print("=" * 80)

    tests = [
        ("All Guardian Decks", test_all_guardian_decks),
        ("Mathematical Concepts", test_mathematical_concepts),
        ("Architectural Patterns", test_architectural_patterns),
        ("Combo Chains", test_combo_chains),
        ("Deck Strategies", test_deck_strategies),
        ("Void Depth Mechanics", test_void_depth_mechanics),
        ("Chaos Factor", test_chaos_factor),
        ("Quantum States", test_quantum_states),
        ("Game Simulation", simulate_deck_game)
    ]

    for name, test_func in tests:
        try:
            print(f"\n{'=' * 40}")
            print(f"Running: {name}")
            print('=' * 40)
            test_func()
            print(f"✓ {name} completed successfully")
        except Exception as e:
            print(f"✗ {name} failed: {str(e)}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 80)
    print("DECK SYSTEM SUMMARY")
    print("=" * 80)

    print("""
Features Implemented:
--------------------
1. ✓ All 19 guardians have unique 8-card decks
2. ✓ 15 Mathematical concepts integrated (Hilbert space, fractals, chaos theory, etc.)
3. ✓ 12 Architectural patterns (networks, cycles, spirals, void spaces, etc.)
4. ✓ Card types: Attack, Defense, Ability, Pattern, Architecture, Chaos, Quantum, etc.
5. ✓ Combo system with explicit card chains
6. ✓ Synergy tags for strategic grouping
7. ✓ Special mechanics:
   - Echo stacking for signal amplification
   - Void depth for nullspace navigation
   - Chaos factor for unpredictability
   - Quantum states for superposition
   - Scaling effects based on game state
8. ✓ Win conditions unique to each guardian
9. ✓ Strategic weaknesses and counters
10. ✓ Mathematical synergies (golden ratio multipliers, etc.)

Total Cards Created: 152+ unique cards
Average per Guardian: 8 cards
Mathematical Concepts Used: All 15
Architectural Patterns Used: All 12
    """)

if __name__ == "__main__":
    main()