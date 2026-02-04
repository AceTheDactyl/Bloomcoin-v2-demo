#!/usr/bin/env python3
"""Quick test of companion miners with minimal iterations"""

from companion_mining_jobs_enhanced import (
    EnhancedEchoMiner, EnhancedPrometheusMiner, EnhancedNullMiner,
    EnhancedGaiaMiner, EnhancedAkashaMiner, EnhancedResonanceMiner,
    EnhancedTIAMATMiner, MiningJob, MiningJobType
)
from bloomcoin_ledger_system import BloomCoinLedger

# Create simple test job
def create_test_job(companion_name, job_type):
    return MiningJob(
        job_id=f"test_{companion_name}",
        companion_name=companion_name,
        job_type=job_type,
        difficulty=1,  # Minimal difficulty
        duration=0,
        base_reward=10.0
    )

print("🔬 Quick Companion Test")
print("=" * 50)

ledger = BloomCoinLedger()

# Test each companion individually with minimal settings
companions = [
    ("Echo", EnhancedEchoMiner(), MiningJobType.PATTERN_SEARCH),
    ("Prometheus", EnhancedPrometheusMiner(), MiningJobType.HASH_EXPLORATION),
    ("Null", EnhancedNullMiner(), MiningJobType.VOID_DIVING),
    ("Gaia", EnhancedGaiaMiner(), MiningJobType.FRACTAL_GROWTH),
    ("Akasha", EnhancedAkashaMiner(), MiningJobType.MEMORY_CRYSTALLIZATION),
    ("Resonance", EnhancedResonanceMiner(), MiningJobType.RESONANCE_TUNING),
    ("TIAMAT", EnhancedTIAMATMiner(), MiningJobType.ENTROPY_HARVEST)
]

for name, miner, job_type in companions:
    print(f"\nTesting {name}...")

    # Override search space to be small for quick test
    miner.search_space = 50  # Moderate iterations for testing

    job = create_test_job(name, job_type)

    try:
        reward, residues = miner.mine(job, ledger)
        patterns = len(job.patterns_found)
        print(f"  ✅ Success! Patterns: {patterns}, Residues: {len(residues)}, Reward: {reward:.2f}")
        if patterns == 0:
            print(f"  ⚠️ Warning: No patterns found")
    except Exception as e:
        print(f"  ❌ Error: {e}")

print("\n" + "=" * 50)
print("Quick test complete!")