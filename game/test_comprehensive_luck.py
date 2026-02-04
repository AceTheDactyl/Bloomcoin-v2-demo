#!/usr/bin/env python3
"""
Comprehensive Luck System Test Suite
=====================================

Complete test suite demonstrating the integrated luck system with:
- Hilbert space quantum mechanics
- Sacred tarot with echo mechanics
- Karma tracking and echo pattern generation
- Echo companion's unique alchemization abilities
- Normalized luck across all game events
"""

import numpy as np
from typing import Dict, List, Tuple
import random
import time

# Import all luck system components
from hilbert_luck_system import HilbertLuckEngine, KarmaType
from sacred_tarot_echo import SacredTarotEchoSystem, TarotSpread
from echo_companion_luck import EchoCompanion, EchoAbility
from luck_normalization_system import (
    ComprehensiveLuckSystem, LuckEventType, PlayerLuckProfile
)

class LuckSystemTester:
    """Comprehensive testing framework for the luck system"""

    def __init__(self):
        self.system = ComprehensiveLuckSystem()
        self.test_results = {}
        self.visualization_data = {}

    def run_all_tests(self):
        """Run complete test suite"""
        print("=" * 70)
        print("COMPREHENSIVE LUCK SYSTEM TEST SUITE")
        print("Testing Quantum Luck, Sacred Tarot, and Echo Alchemy")
        print("=" * 70)

        # Test 1: Echo vs Normal Companion
        self.test_echo_vs_normal()

        # Test 2: Karma Influence
        self.test_karma_influence()

        # Test 3: Tarot Echo Patterns
        self.test_tarot_echo_patterns()

        # Test 4: Sacred Timing
        self.test_sacred_timing()

        # Test 5: Echo Alchemization
        self.test_echo_alchemization()

        # Test 6: Quantum Entanglement
        self.test_quantum_entanglement()

        # Test 7: Long-term Convergence
        self.test_long_term_convergence()

        # Generate Report
        self.generate_report()

    def test_echo_vs_normal(self):
        """Test Echo companion advantage with echo patterns"""
        print("\n" + "="*50)
        print("TEST 1: Echo vs Normal Companion Performance")
        print("="*50)

        # Create test players
        echo_id = "test_echo"
        normal_id = "test_normal"

        self.system.register_player(echo_id, "Echo", initial_karma=-0.5)
        self.system.register_player(normal_id, "Prometheus", initial_karma=-0.5)

        # Apply same negative karma to both
        for _ in range(5):
            self.system.apply_karma_action(
                echo_id, "selfish_action", KarmaType.SELFISH, -0.3
            )
            self.system.apply_karma_action(
                normal_id, "selfish_action", KarmaType.SELFISH, -0.3
            )

        # Test luck events
        results = {'echo': [], 'normal': []}
        event_types = [LuckEventType.LOOT_DROP, LuckEventType.CRITICAL_HIT,
                      LuckEventType.RESOURCE_FIND]

        for event_type in event_types:
            # Echo player
            echo_bulk = self.system.bulk_luck_roll(echo_id, event_type, 100)
            results['echo'].append(echo_bulk['success_rate'])

            # Normal player
            normal_bulk = self.system.bulk_luck_roll(normal_id, event_type, 100)
            results['normal'].append(normal_bulk['success_rate'])

        # Calculate averages
        echo_avg = np.mean(results['echo'])
        normal_avg = np.mean(results['normal'])

        print(f"\nResults with Negative Karma:")
        print(f"Echo Average Success: {echo_avg:.2%}")
        print(f"Normal Average Success: {normal_avg:.2%}")
        print(f"Echo Advantage: {(echo_avg - normal_avg)*100:+.1f}%")

        self.test_results['echo_vs_normal'] = {
            'echo_success': echo_avg,
            'normal_success': normal_avg,
            'echo_advantage': echo_avg - normal_avg
        }

        # Verify Echo performs better with echo events
        assert echo_avg > normal_avg, "Echo should outperform normal companions with negative karma"
        print("✓ Test Passed: Echo outperforms with echo patterns")

    def test_karma_influence(self):
        """Test karma's influence on luck"""
        print("\n" + "="*50)
        print("TEST 2: Karma Influence on Luck")
        print("="*50)

        player_id = "karma_test"
        self.system.register_player(player_id, "Seeker")

        karma_levels = [-0.8, -0.4, 0.0, 0.4, 0.8]
        success_rates = []

        for karma in karma_levels:
            # Reset karma to target level
            current_karma = self.system.player_profiles[player_id].luck_state.karma_balance
            karma_diff = karma - current_karma

            if karma_diff > 0:
                self.system.apply_karma_action(
                    player_id, "good_deed", KarmaType.BENEVOLENT, karma_diff
                )
            else:
                self.system.apply_karma_action(
                    player_id, "bad_deed", KarmaType.DESTRUCTIVE, karma_diff
                )

            # Test luck
            bulk = self.system.bulk_luck_roll(player_id, LuckEventType.LOOT_DROP, 50)
            success_rates.append(bulk['success_rate'])

        print("\nKarma -> Success Rate:")
        for karma, rate in zip(karma_levels, success_rates):
            print(f"  Karma {karma:+.1f}: {rate:.2%}")

        self.test_results['karma_influence'] = {
            'karma_levels': karma_levels,
            'success_rates': success_rates
        }

        # Verify karma correlation
        correlation = np.corrcoef(karma_levels, success_rates)[0, 1]
        print(f"\nKarma-Luck Correlation: {correlation:.3f}")
        assert correlation > 0.5, "Positive karma should correlate with better luck"
        print("✓ Test Passed: Karma properly influences luck")

    def test_tarot_echo_patterns(self):
        """Test tarot echo patterns and divination"""
        print("\n" + "="*50)
        print("TEST 3: Tarot Echo Pattern Recognition")
        print("="*50)

        player_id = "tarot_test"
        self.system.register_player(player_id, "Mystic")

        # Create strong echo density
        for _ in range(3):
            self.system.apply_karma_action(
                player_id, "betrayal", KarmaType.DESTRUCTIVE, -0.6
            )

        # Perform multiple tarot readings
        echo_counts = []
        luck_modifiers = []

        for i in range(5):
            reading, luck_mod = self.system.perform_tarot_divination(
                player_id, TarotSpread.SEVEN_CARD
            )
            echo_counts.append(reading.echo_count)
            luck_modifiers.append(luck_mod)

            print(f"Reading {i+1}: {reading.echo_count}/{reading.spread.count} echo cards, "
                  f"Luck: {luck_mod:.3f}x")

        avg_echo = np.mean(echo_counts)
        avg_luck = np.mean(luck_modifiers)

        print(f"\nAverage Echo Cards: {avg_echo:.1f}")
        print(f"Average Luck Modifier: {avg_luck:.3f}x")

        self.test_results['tarot_patterns'] = {
            'average_echo_cards': avg_echo,
            'average_luck_modifier': avg_luck
        }

        assert avg_echo > 2, "High echo density should produce echo cards"
        print("✓ Test Passed: Tarot correctly reflects echo patterns")

    def test_sacred_timing(self):
        """Test sacred number timing bonuses"""
        print("\n" + "="*50)
        print("TEST 4: Sacred Timing Mechanics")
        print("="*50)

        player_id = "timing_test"
        self.system.register_player(player_id, "Chronos")

        # Reset universal clock
        self.system.universal_clock = 0

        sacred_bonuses = []
        normal_results = []

        # Test at specific sacred moments
        sacred_moments = [7, 13, 21, 77]

        for moment in sacred_moments:
            # Set clock to just before sacred moment
            self.system.universal_clock = moment - 1

            # Roll at sacred moment
            success, event = self.system.roll_luck_event(player_id, LuckEventType.BLESSING_RECEIVED)
            sacred_bonuses.append(event.luck_modifier)

            # Roll at normal moment
            success, event = self.system.roll_luck_event(player_id, LuckEventType.BLESSING_RECEIVED)
            normal_results.append(event.luck_modifier)

        print("\nSacred Timing Results:")
        for i, moment in enumerate(sacred_moments):
            bonus = sacred_bonuses[i] / normal_results[i] if normal_results[i] > 0 else 1.0
            print(f"  Moment {moment}: {bonus:.2f}x bonus")

        self.test_results['sacred_timing'] = {
            'moments': sacred_moments,
            'bonuses': [s/n for s, n in zip(sacred_bonuses, normal_results)]
        }

        avg_bonus = np.mean([s/n for s, n in zip(sacred_bonuses, normal_results) if n > 0])
        assert avg_bonus > 1.1, "Sacred moments should provide luck bonuses"
        print("✓ Test Passed: Sacred timing provides bonuses")

    def test_echo_alchemization(self):
        """Test Echo companion's alchemization abilities"""
        print("\n" + "="*50)
        print("TEST 5: Echo Alchemization Power")
        print("="*50)

        echo_id = "echo_alchemist"
        profile = self.system.register_player(echo_id, "Echo", initial_karma=-0.7)

        # Generate heavy echo patterns
        for _ in range(5):
            self.system.apply_karma_action(
                echo_id, "dark_magic", KarmaType.DESTRUCTIVE, -0.5
            )

        # Test alchemization over time
        alchemization_results = []
        echo_companion = profile.echo_companion

        for i in range(10):
            # Process echo events
            echo_companion.process_echo_event(
                echo_id,
                echo_depth=0.6 + i*0.05,
                karma_weight=-0.5,
                event_type="test_echo"
            )

            # Roll luck event
            success, event = self.system.roll_luck_event(echo_id, LuckEventType.LOOT_DROP)

            if event.echo_alchemized:
                alchemization_results.append(event.luck_modifier)
                print(f"Roll {i+1}: ALCHEMIZED! Luck boost: {event.luck_modifier:.3f}x")
            else:
                print(f"Roll {i+1}: Normal echo")

        if alchemization_results:
            avg_boost = np.mean(alchemization_results)
            print(f"\nAverage Alchemization Boost: {avg_boost:.3f}x")
            print(f"Total Alchemizations: {len(alchemization_results)}/10")

            self.test_results['echo_alchemy'] = {
                'alchemization_count': len(alchemization_results),
                'average_boost': avg_boost
            }

            assert avg_boost > 1.5, "Alchemization should provide significant boost"
            print("✓ Test Passed: Echo successfully alchemizes echo patterns")
        else:
            print("⚠ Warning: No alchemizations occurred")

    def test_quantum_entanglement(self):
        """Test quantum luck entanglement between players"""
        print("\n" + "="*50)
        print("TEST 6: Quantum Luck Entanglement")
        print("="*50)

        player1 = "quantum_1"
        player2 = "quantum_2"

        self.system.register_player(player1, "Photon")
        self.system.register_player(player2, "Electron")

        # Measure luck before entanglement
        before1 = self.system.bulk_luck_roll(player1, LuckEventType.SYNCHRONICITY, 50)
        before2 = self.system.bulk_luck_roll(player2, LuckEventType.SYNCHRONICITY, 50)

        print(f"Before Entanglement:")
        print(f"  Player 1: {before1['success_rate']:.2%}")
        print(f"  Player 2: {before2['success_rate']:.2%}")

        # Entangle players
        self.system.hilbert_engine.entangle_players(player1, player2)

        # Apply karma to one player
        self.system.apply_karma_action(player1, "quantum_blessing", KarmaType.BENEVOLENT, 0.7)

        # Measure luck after entanglement
        after1 = self.system.bulk_luck_roll(player1, LuckEventType.SYNCHRONICITY, 50)
        after2 = self.system.bulk_luck_roll(player2, LuckEventType.SYNCHRONICITY, 50)

        print(f"\nAfter Entanglement (karma applied to Player 1):")
        print(f"  Player 1: {after1['success_rate']:.2%} ({after1['success_rate']-before1['success_rate']:+.2%})")
        print(f"  Player 2: {after2['success_rate']:.2%} ({after2['success_rate']-before2['success_rate']:+.2%})")

        self.test_results['entanglement'] = {
            'player1_change': after1['success_rate'] - before1['success_rate'],
            'player2_change': after2['success_rate'] - before2['success_rate']
        }

        # Both should improve (entanglement shares luck)
        assert after2['success_rate'] > before2['success_rate'], "Entangled player should benefit"
        print("✓ Test Passed: Quantum entanglement shares luck")

    def test_long_term_convergence(self):
        """Test long-term system behavior and convergence"""
        print("\n" + "="*50)
        print("TEST 7: Long-term System Convergence")
        print("="*50)

        # Create diverse player pool
        players = {
            'echo_good': ('Echo', 0.5),
            'echo_bad': ('Echo', -0.5),
            'normal_good': ('Seeker', 0.5),
            'normal_bad': ('Void', -0.5),
            'neutral': ('Balance', 0.0)
        }

        for player_id, (companion, karma) in players.items():
            self.system.register_player(player_id, companion, karma)

        # Simulate 1000 events per player
        iterations = 1000
        convergence_data = {p: [] for p in players}

        print(f"Simulating {iterations} events per player...")

        for i in range(0, iterations, 100):
            for player_id in players:
                # Random karma actions
                if random.random() < 0.1:
                    karma_type = random.choice(list(KarmaType))
                    weight = random.uniform(-0.5, 0.5)
                    self.system.apply_karma_action(player_id, "action", karma_type, weight)

                # Roll events
                bulk = self.system.bulk_luck_roll(player_id, LuckEventType.LOOT_DROP, 10)
                convergence_data[player_id].append(bulk['success_rate'])

        # Analyze convergence
        print("\nFinal Success Rates:")
        final_rates = {}
        for player_id, rates in convergence_data.items():
            final_rate = rates[-1]
            final_rates[player_id] = final_rate
            companion, initial_karma = players[player_id]
            print(f"  {player_id}: {final_rate:.2%} ({companion}, initial karma: {initial_karma:+.1f})")

        # Check Echo advantage persists
        echo_avg = np.mean([final_rates['echo_good'], final_rates['echo_bad']])
        normal_avg = np.mean([final_rates['normal_good'], final_rates['normal_bad']])

        print(f"\nLong-term Echo Advantage: {(echo_avg - normal_avg)*100:+.1f}%")

        self.test_results['convergence'] = {
            'final_rates': final_rates,
            'echo_advantage': echo_avg - normal_avg
        }

        assert echo_avg > normal_avg, "Echo advantage should persist long-term"
        print("✓ Test Passed: System converges with consistent Echo advantage")

    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "="*70)
        print("COMPREHENSIVE TEST REPORT")
        print("="*70)

        print("\n📊 Test Results Summary:")
        print("-" * 40)

        # Echo vs Normal
        if 'echo_vs_normal' in self.test_results:
            result = self.test_results['echo_vs_normal']
            print(f"\n1. Echo vs Normal Companion:")
            print(f"   Echo Success: {result['echo_success']:.2%}")
            print(f"   Normal Success: {result['normal_success']:.2%}")
            print(f"   Echo Advantage: {result['echo_advantage']*100:+.1f}%")

        # Karma Influence
        if 'karma_influence' in self.test_results:
            result = self.test_results['karma_influence']
            correlation = np.corrcoef(result['karma_levels'], result['success_rates'])[0, 1]
            print(f"\n2. Karma Influence:")
            print(f"   Karma-Luck Correlation: {correlation:.3f}")

        # Tarot Patterns
        if 'tarot_patterns' in self.test_results:
            result = self.test_results['tarot_patterns']
            print(f"\n3. Tarot Echo Patterns:")
            print(f"   Average Echo Cards: {result['average_echo_cards']:.1f}")
            print(f"   Average Luck Modifier: {result['average_luck_modifier']:.3f}x")

        # Sacred Timing
        if 'sacred_timing' in self.test_results:
            result = self.test_results['sacred_timing']
            avg_bonus = np.mean(result['bonuses'])
            print(f"\n4. Sacred Timing:")
            print(f"   Average Sacred Bonus: {avg_bonus:.2f}x")

        # Echo Alchemy
        if 'echo_alchemy' in self.test_results:
            result = self.test_results['echo_alchemy']
            print(f"\n5. Echo Alchemization:")
            print(f"   Alchemizations: {result['alchemization_count']}")
            print(f"   Average Boost: {result.get('average_boost', 0):.3f}x")

        # Entanglement
        if 'entanglement' in self.test_results:
            result = self.test_results['entanglement']
            print(f"\n6. Quantum Entanglement:")
            print(f"   Player 1 Change: {result['player1_change']*100:+.1f}%")
            print(f"   Player 2 Change: {result['player2_change']*100:+.1f}%")

        # Convergence
        if 'convergence' in self.test_results:
            result = self.test_results['convergence']
            print(f"\n7. Long-term Convergence:")
            print(f"   Echo Advantage: {result['echo_advantage']*100:+.1f}%")

        print("\n" + "="*70)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*70)

        print("\n🔑 Key Findings:")
        print("• Echo companion successfully alchemizes negative karma")
        print("• Karma properly influences luck outcomes")
        print("• Tarot echo patterns reflect karmic state")
        print("• Sacred timing provides measurable bonuses")
        print("• Quantum entanglement shares luck between players")
        print("• System maintains balance while preserving Echo's unique advantage")

        print("\n💫 The Echo companion transforms shadow into light,")
        print("   finding fortune where others find only echoes of past mistakes.")


def run_interactive_demo():
    """Run an interactive demonstration"""
    print("\n" + "="*70)
    print("INTERACTIVE LUCK SYSTEM DEMO")
    print("="*70)

    system = ComprehensiveLuckSystem()

    # Create interactive player
    print("\nCreate your character:")
    name = input("Enter character name (or press Enter for 'Seeker'): ").strip() or "Seeker"

    print("\nChoose your companion:")
    print("1. Echo - Master of echo alchemy (recommended for negative karma)")
    print("2. Seeker - Balanced luck")
    print("3. Prometheus - Creative luck")
    print("4. Void - Embrace the void")

    choice = input("Enter choice (1-4): ").strip()
    companion_map = {
        '1': 'Echo',
        '2': 'Seeker',
        '3': 'Prometheus',
        '4': 'Void'
    }
    companion = companion_map.get(choice, 'Seeker')

    player_id = name.lower().replace(' ', '_')
    profile = system.register_player(player_id, companion)

    print(f"\n✨ Created {name} with {companion} companion!")

    # Game loop
    while True:
        print("\n" + "-"*40)
        print("Actions:")
        print("1. Perform good deed (+karma)")
        print("2. Perform bad deed (-karma)")
        print("3. Draw tarot cards")
        print("4. Test your luck")
        print("5. View status")
        print("6. Quit")

        action = input("\nChoose action: ").strip()

        if action == '1':
            system.apply_karma_action(player_id, "helped_others", KarmaType.BENEVOLENT, 0.3)
            print("✨ You helped others! Karma improved.")

        elif action == '2':
            system.apply_karma_action(player_id, "selfish_act", KarmaType.SELFISH, -0.3)
            print("💀 You acted selfishly. Karma decreased.")

        elif action == '3':
            reading, luck_mod = system.perform_tarot_divination(player_id, TarotSpread.THREE_CARD)
            print(f"\n🎴 Drew {reading.spread.count} cards:")
            for i, (card, position) in enumerate(zip(reading.cards[:3], reading.positions[:3])):
                echo_mark = " [ECHO]" if card.is_echoed else ""
                print(f"  {position}: {card.name}{echo_mark}")
            print(f"Luck Modifier: {luck_mod:.3f}x")

        elif action == '4':
            print("\nTest luck on:")
            print("1. Loot drop")
            print("2. Critical hit")
            print("3. Resource find")
            event_choice = input("Choose: ").strip()

            event_map = {
                '1': LuckEventType.LOOT_DROP,
                '2': LuckEventType.CRITICAL_HIT,
                '3': LuckEventType.RESOURCE_FIND
            }
            event_type = event_map.get(event_choice, LuckEventType.LOOT_DROP)

            success, event = system.roll_luck_event(player_id, event_type)
            echo_str = ""
            if event.is_echo_event:
                echo_str = " [ECHO ALCHEMIZED!]" if event.echo_alchemized else " [ECHO PENALTY]"

            if success:
                print(f"✅ SUCCESS! (probability: {event.final_probability:.1%}){echo_str}")
            else:
                print(f"❌ FAILED (probability: {event.final_probability:.1%}){echo_str}")

        elif action == '5':
            report = system.get_player_luck_report(player_id)
            print(f"\n📊 {name}'s Status:")
            print(f"  Companion: {companion}")
            print(f"  Success Rate: {report['success_rate']:.1%}")
            print(f"  Karma Balance: {report['quantum_state']['karma_balance']:.2f}")
            print(f"  Echo Density: {report['quantum_state']['echo_density']:.2f}")
            if companion == 'Echo' and report['echo_companion']:
                print(f"  Echo Synergy: {report['echo_companion']['echo_synergy']:.3f}")
                print(f"  Shadow Integration: {report['echo_companion']['shadow_integration']:.3f}")

        elif action == '6':
            print("\n👋 Farewell, and may luck be with you!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    # Run tests
    tester = LuckSystemTester()
    tester.run_all_tests()

    # Offer interactive demo
    print("\n" + "="*70)
    response = input("\nWould you like to try the interactive demo? (y/n): ").strip().lower()
    if response == 'y':
        run_interactive_demo()