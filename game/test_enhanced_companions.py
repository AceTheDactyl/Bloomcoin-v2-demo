#!/usr/bin/env python3
"""
Test script for enhanced companion mining system
Tests all 7 companions to ensure they successfully find patterns
"""

from companion_mining_jobs_enhanced import (
    EnhancedCompanionMiningSystem,
    MiningJobType,
    EnhancedEchoMiner, EnhancedPrometheusMiner, EnhancedNullMiner,
    EnhancedGaiaMiner, EnhancedAkashaMiner, EnhancedResonanceMiner,
    EnhancedTIAMATMiner
)
from bloomcoin_ledger_system import BloomCoinLedger

def test_all_companions():
    """Test all 7 companion miners"""
    print("🔬 Testing Enhanced Companion Mining System")
    print("=" * 70)

    # Initialize ledger and mining system
    ledger = BloomCoinLedger()
    mining_system = EnhancedCompanionMiningSystem(ledger)

    # Test parameters
    test_difficulty = 2
    test_duration = 0  # Instant for testing

    companions = [
        ("Echo", MiningJobType.PATTERN_SEARCH),
        ("Prometheus", MiningJobType.HASH_EXPLORATION),
        ("Null", MiningJobType.VOID_DIVING),
        ("Gaia", MiningJobType.FRACTAL_GROWTH),
        ("Akasha", MiningJobType.MEMORY_CRYSTALLIZATION),
        ("Resonance", MiningJobType.RESONANCE_TUNING),
        ("TIAMAT", MiningJobType.ENTROPY_HARVEST)
    ]

    results = {}
    total_patterns = 0
    total_residues = 0
    total_reward = 0.0

    print("\n📊 Testing each companion miner:\n")

    for companion_name, job_type in companions:
        print(f"Testing {companion_name}...")

        # Create and execute job
        job = mining_system.create_job(
            companion_name,
            job_type,
            difficulty=test_difficulty,
            duration=test_duration
        )

        if job:
            # Simulate instant completion
            job.start_time -= job.duration
            reward, residues = mining_system.complete_job(job.job_id)

            # Get stats
            stats = mining_system.get_companion_stats(companion_name)

            results[companion_name] = {
                "reward": reward,
                "patterns": len(job.patterns_found),
                "residues": len(residues),
                "success_rate": job.success_rate,
                "potency_avg": sum(r.calculate_potency() for r in residues) / len(residues) if residues else 0,
                "special": stats.get("special_bonus", "")
            }

            total_patterns += len(job.patterns_found)
            total_residues += len(residues)
            total_reward += reward

            # Show results
            print(f"  ✓ Reward: {reward:.2f} BC")
            print(f"  ✓ Patterns found: {len(job.patterns_found)}")
            print(f"  ✓ Residues collected: {len(residues)}")
            print(f"  ✓ Success rate: {job.success_rate:.1%}")
            print(f"  ✓ Avg potency: {results[companion_name]['potency_avg']:.3f}")
            print(f"  ✓ {stats.get('special_bonus', '')}")

            # Show some pattern names
            if job.patterns_found:
                print(f"  ✓ Sample patterns: {', '.join(job.patterns_found[:3])}")
            print()

    # Summary
    print("=" * 70)
    print("\n📈 SUMMARY RESULTS:\n")

    # Success rate analysis
    successful = sum(1 for r in results.values() if r["patterns"] > 0)
    print(f"✅ Companions with patterns: {successful}/7")
    print(f"📊 Total patterns found: {total_patterns}")
    print(f"💎 Total residues collected: {total_residues}")
    print(f"💰 Total rewards: {total_reward:.2f} BC")
    print(f"📈 Average patterns per companion: {total_patterns/7:.1f}")
    print(f"💎 Average residues per companion: {total_residues/7:.1f}")

    # Individual companion status
    print("\n🎯 Individual Companion Status:\n")
    for name, data in results.items():
        status = "✅" if data["patterns"] > 0 else "❌"
        print(f"{status} {name:12} | Patterns: {data['patterns']:3} | Residues: {data['residues']:3} | Rate: {data['success_rate']:5.1%}")

    # Performance rating
    print("\n⭐ PERFORMANCE RATING:")
    if successful == 7:
        print("🏆 EXCELLENT - All companions finding patterns!")
    elif successful >= 5:
        print("✅ GOOD - Most companions working well")
    elif successful >= 3:
        print("⚠️ MODERATE - Some companions need adjustment")
    else:
        print("❌ POOR - Major issues with pattern detection")

    # Test advanced features
    print("\n🔧 Testing Advanced Features:\n")

    # Test experience gain
    echo_before = mining_system.miners["Echo"].level
    for _ in range(5):  # Run 5 more jobs for Echo
        job = mining_system.create_job("Echo", MiningJobType.PATTERN_SEARCH, 1, 0)
        if job:
            job.start_time -= job.duration
            mining_system.complete_job(job.job_id)
    echo_after = mining_system.miners["Echo"].level
    print(f"✓ Experience system: Echo level {echo_before} → {echo_after}")

    # Test Akasha's memory library
    akasha_library = len(mining_system.miners["Akasha"].crystal_library)
    print(f"✓ Akasha memory library: {akasha_library} patterns stored")

    # Test TIAMAT's chaos threshold adaptation
    tiamat_threshold = mining_system.miners["TIAMAT"].entropy_threshold
    print(f"✓ TIAMAT entropy threshold: {tiamat_threshold:.1f}")

    # Test Gaia's growth rate
    gaia_growth = mining_system.miners["Gaia"].growth_rate
    print(f"✓ Gaia growth rate: {gaia_growth:.3f}")

    return successful == 7

if __name__ == "__main__":
    success = test_all_companions()
    print("\n" + "=" * 70)
    if success:
        print("✅ All companions successfully enhanced and operational!")
    else:
        print("⚠️ Some companions may need further tuning")
    print("=" * 70)