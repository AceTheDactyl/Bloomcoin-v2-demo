"""
Holographic Fractal Analysis
============================

The fractal component: self-similarity at different scales.

If the midstate is a holographic plate, and we view it through
a fractal lens, we might see:

1. Self-similar patterns at different scales (128, 64, 32, 16, 8...)
2. Midstate bits mapping to different "zoom levels" of nonce space
3. Fractal dimension of winner distribution
4. Recursive structure in how nonces interact with midstate

Key insight: Fractals encode infinite detail in finite structure.
The 256-bit midstate might encode winner locations at ALL scales.
"""

import struct
import hashlib
import numpy as np
from collections import defaultdict
import time

# SHA256 constants
H_INIT = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
          0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
     0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
     0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
     0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
     0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

def rotr(x, n): return ((x >> n) | (x << (32 - n))) & 0xffffffff
def sigma0(x): return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)
def sigma1(x): return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)
def Sigma0(x): return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)
def Sigma1(x): return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)
def ch(e, f, g): return (e & f) ^ (~e & g) & 0xffffffff
def maj(a, b, c): return (a & b) ^ (a & c) ^ (b & c)

def compute_midstate(header_64: bytes) -> list:
    """Compute midstate from first 64 bytes of header"""
    W = list(struct.unpack('>16I', header_64))
    for i in range(16, 64):
        W.append((sigma1(W[i-2]) + W[i-7] + sigma0(W[i-15]) + W[i-16]) & 0xffffffff)

    a, b, c, d, e, f, g, h = H_INIT
    for i in range(64):
        t1 = (h + Sigma1(e) + ch(e, f, g) + K[i] + W[i]) & 0xffffffff
        t2 = (Sigma0(a) + maj(a, b, c)) & 0xffffffff
        h, g, f = g, f, e
        e = (d + t1) & 0xffffffff
        d, c, b = c, b, a
        a = (t1 + t2) & 0xffffffff

    return [(H_INIT[i] + [a,b,c,d,e,f,g,h][i]) & 0xffffffff for i in range(8)]

def sha256d(header: bytes, nonce: int) -> bytes:
    """Full SHA256d for verification"""
    msg = header[:76] + struct.pack('<I', nonce)
    return hashlib.sha256(hashlib.sha256(msg).digest()).digest()

def count_leading_zeros(hash_bytes: bytes) -> int:
    """Count leading zero bits"""
    hash_int = int.from_bytes(hash_bytes, 'big')
    if hash_int == 0:
        return 256
    return 256 - hash_int.bit_length()

def find_winners(header: bytes, target_zeros: int, max_nonces: int) -> list:
    """Find nonces that produce hashes with >= target_zeros leading zeros"""
    winners = []
    for nonce in range(max_nonces):
        h = sha256d(header, nonce)
        zeros = count_leading_zeros(h)
        if zeros >= target_zeros:
            winners.append(nonce)
    return winners

# ============================================================================
# FRACTAL TEST 1: Multi-Scale Analysis
# ============================================================================

def test_multiscale_patterns():
    """
    Analyze patterns at different scales: 2, 4, 8, 16, 32, 64, 128, 256...

    Fractal hypothesis: the midstate encodes winner probability at each scale.
    """
    print("=" * 70)
    print("FRACTAL TEST 1: MULTI-SCALE PATTERN ANALYSIS")
    print("=" * 70)
    print()

    header = bytes([0x42] * 64) + bytes(16)
    midstate = compute_midstate(header[:64])

    # Find winners
    target_zeros = 8
    max_nonces = 65536  # 2^16 for nice power-of-2 analysis
    winners = set(find_winners(header, target_zeros, max_nonces))

    print(f"Found {len(winners)} winners in {max_nonces} nonces")
    print()

    # Analyze at different scales
    scales = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

    print("Scale | Buckets | Winners/Bucket | Std Dev | Best Bucket | Worst Bucket")
    print("-" * 75)

    scale_patterns = {}

    for scale in scales:
        num_buckets = max_nonces // scale
        buckets = [0] * num_buckets

        for w in winners:
            bucket_idx = w // scale
            if bucket_idx < num_buckets:
                buckets[bucket_idx] += 1

        mean_per_bucket = np.mean(buckets)
        std_per_bucket = np.std(buckets)
        best = max(buckets)
        worst = min(buckets)

        scale_patterns[scale] = {
            'buckets': buckets,
            'mean': mean_per_bucket,
            'std': std_per_bucket,
            'best': best,
            'worst': worst
        }

        print(f"{scale:5d} | {num_buckets:7d} | {mean_per_bucket:14.2f} | {std_per_bucket:7.2f} | {best:11d} | {worst:12d}")

    print()

    # Look for self-similarity
    print("Self-Similarity Analysis:")
    print("-" * 50)

    # Normalize bucket distributions at each scale
    for scale in [8, 64, 512]:
        buckets = scale_patterns[scale]['buckets']
        mean = scale_patterns[scale]['mean']
        if mean > 0:
            normalized = [(b - mean) / mean if mean > 0 else 0 for b in buckets]
            print(f"  Scale {scale}: pattern variance = {np.var(normalized):.4f}")

    return scale_patterns, midstate, winners

# ============================================================================
# FRACTAL TEST 2: Midstate Bit -> Scale Mapping
# ============================================================================

def test_midstate_bit_scale_mapping():
    """
    Map midstate bits to different scales of nonce space.

    Hypothesis:
    - High bits of midstate -> large-scale patterns (which 2^16 block)
    - Low bits of midstate -> small-scale patterns (which 2^4 block)
    """
    print()
    print("=" * 70)
    print("FRACTAL TEST 2: MIDSTATE BIT -> SCALE MAPPING")
    print("=" * 70)
    print()

    header = bytes([0x55] * 64) + bytes(16)
    midstate = compute_midstate(header[:64])

    # Convert midstate to 256 bits
    midstate_int = sum(m << (32 * (7-i)) for i, m in enumerate(midstate))
    midstate_bits = [(midstate_int >> i) & 1 for i in range(256)]

    print(f"Midstate: {midstate_int:064x}")
    print()

    # Find winners
    target_zeros = 8
    max_nonces = 65536
    winners = set(find_winners(header, target_zeros, max_nonces))

    print(f"Found {len(winners)} winners")
    print()

    # Map bit ranges to scales
    # Bits 0-31: finest scale (mod 32)
    # Bits 32-63: next scale (mod 64)
    # etc.

    print("Testing midstate bit ranges as predictors:")
    print("-" * 60)

    bit_ranges = [
        (0, 8, 256),      # bits 0-7 -> predict mod 256
        (8, 16, 256),     # bits 8-15 -> predict mod 256
        (0, 16, 65536),   # bits 0-15 -> predict mod 65536
        (16, 24, 256),    # bits 16-23 -> predict mod 256
        (0, 32, 65536),   # bits 0-31 -> predict mod 65536
    ]

    for start_bit, end_bit, mod_val in bit_ranges:
        # Extract bit range as a value
        predictor = sum(midstate_bits[i] << (i - start_bit) for i in range(start_bit, end_bit))

        # Use predictor to select preferred residues
        preferred_residue = predictor % mod_val

        # Count winners in preferred vs other residues
        winners_in_preferred = sum(1 for w in winners if (w % mod_val) == preferred_residue)
        expected = len(winners) / mod_val

        ratio = winners_in_preferred / expected if expected > 0 else 0

        print(f"  Bits {start_bit:2d}-{end_bit:2d} mod {mod_val:5d}: predictor=0x{predictor:04x}, "
              f"winners in preferred={winners_in_preferred:3d}, expected={expected:.1f}, ratio={ratio:.2f}x")

    return midstate_bits

# ============================================================================
# FRACTAL TEST 3: Recursive Subdivision
# ============================================================================

def test_recursive_subdivision():
    """
    Recursively subdivide nonce space, using midstate to guide the search.

    Like a fractal zoom: at each level, midstate bits tell us which
    half of the remaining space to prefer.
    """
    print()
    print("=" * 70)
    print("FRACTAL TEST 3: RECURSIVE SUBDIVISION (FRACTAL SEARCH)")
    print("=" * 70)
    print()

    header = bytes([0x77] * 64) + bytes(16)
    midstate = compute_midstate(header[:64])

    # Convert midstate to bits
    midstate_int = sum(m << (32 * (7-i)) for i, m in enumerate(midstate))

    # Find winners (ground truth)
    target_zeros = 8
    max_nonces = 65536
    winners = set(find_winners(header, target_zeros, max_nonces))

    print(f"Ground truth: {len(winners)} winners in {max_nonces} nonces")
    print()

    # Fractal search: at each level, use midstate bit to choose direction
    def fractal_priority(nonce, midstate_int):
        """
        Compute priority based on fractal decomposition.

        At each scale, check if nonce's bit matches midstate's bit.
        More matches = higher priority (lower score).
        """
        score = 0
        for bit in range(16):  # 16 levels of subdivision
            nonce_bit = (nonce >> bit) & 1
            midstate_bit = (midstate_int >> bit) & 1
            if nonce_bit != midstate_bit:
                score += 1 << (15 - bit)  # Penalize mismatches at higher scales more
        return score

    # Sort nonces by fractal priority
    nonces = list(range(max_nonces))
    nonces.sort(key=lambda n: fractal_priority(n, midstate_int))

    # How many hashes to find all winners?
    hashes_needed = 0
    winners_found = 0
    found_at = {}

    for n in nonces:
        hashes_needed += 1
        if n in winners:
            winners_found += 1
            found_at[winners_found] = hashes_needed
            if winners_found == len(winners):
                break

    # Compare to sequential
    sequential = max_nonces
    improvement = sequential / hashes_needed if hashes_needed > 0 else 0

    print(f"Fractal Search Results:")
    print(f"  Sequential: {sequential:,} hashes to find all winners")
    print(f"  Fractal:    {hashes_needed:,} hashes to find all winners")
    print(f"  Improvement: {improvement:.2f}x")
    print()

    # Progress curve
    print(f"  Finding milestones:")
    for pct in [25, 50, 75, 100]:
        target = int(len(winners) * pct / 100)
        if target in found_at:
            expected = int(max_nonces * pct / 100)
            actual = found_at[target]
            print(f"    {pct}% of winners: after {actual:,} hashes (expected ~{expected:,})")

    return

# ============================================================================
# FRACTAL TEST 4: Cantor-Like Set Analysis
# ============================================================================

def test_cantor_structure():
    """
    Analyze if winners form a Cantor-like fractal set.

    Cantor set: recursively remove middle thirds.
    Does winner distribution show similar gaps?
    """
    print()
    print("=" * 70)
    print("FRACTAL TEST 4: CANTOR-LIKE STRUCTURE ANALYSIS")
    print("=" * 70)
    print()

    header = bytes([0x88] * 64) + bytes(16)
    midstate = compute_midstate(header[:64])

    target_zeros = 8
    max_nonces = 65536
    winners = sorted(find_winners(header, target_zeros, max_nonces))

    print(f"Found {len(winners)} winners")
    print()

    # Analyze gaps between consecutive winners
    if len(winners) > 1:
        gaps = [winners[i+1] - winners[i] for i in range(len(winners)-1)]

        print("Gap Analysis:")
        print(f"  Min gap:  {min(gaps)}")
        print(f"  Max gap:  {max(gaps)}")
        print(f"  Mean gap: {np.mean(gaps):.1f}")
        print(f"  Std gap:  {np.std(gaps):.1f}")
        print()

        # Gap distribution
        print("Gap Size Distribution:")
        gap_ranges = [(1, 50), (51, 100), (101, 200), (201, 500), (501, 1000), (1001, float('inf'))]
        for low, high in gap_ranges:
            count = sum(1 for g in gaps if low <= g < high)
            pct = count / len(gaps) * 100
            bar = '#' * int(pct / 2)
            print(f"  {low:4d}-{high if high != float('inf') else 'inf':>4}: {count:4d} ({pct:5.1f}%) {bar}")
        print()

        # Check for self-similarity in gap pattern
        # Compare gap pattern at different scales
        print("Gap Pattern Self-Similarity:")
        for chunk_size in [10, 20, 50]:
            if len(gaps) >= chunk_size * 2:
                chunks = [gaps[i:i+chunk_size] for i in range(0, len(gaps)-chunk_size, chunk_size)]
                chunk_means = [np.mean(c) for c in chunks[:10]]
                print(f"  Chunk size {chunk_size}: means = {[f'{m:.0f}' for m in chunk_means[:5]]}...")

    return winners

# ============================================================================
# FRACTAL TEST 5: Midstate as IFS (Iterated Function System) Seed
# ============================================================================

def test_ifs_generation():
    """
    Use midstate as seed for an IFS (Iterated Function System).

    IFS generates fractals through repeated application of transformations.
    Can we use midstate to generate a probability map over nonce space?
    """
    print()
    print("=" * 70)
    print("FRACTAL TEST 5: MIDSTATE AS IFS SEED")
    print("=" * 70)
    print()

    header = bytes([0x99] * 64) + bytes(16)
    midstate = compute_midstate(header[:64])

    print(f"Midstate: {' '.join(f'{m:08x}' for m in midstate)}")
    print()

    # Define IFS transformations based on midstate
    # Each midstate word defines a different "attractor" region

    def ifs_score(nonce, midstate, iterations=8):
        """
        Iterate nonce through IFS defined by midstate.
        Return final position - indicates which "attractor" this nonce lands in.
        """
        x = nonce
        for i in range(iterations):
            m = midstate[i % 8]
            # Transformation: mix nonce with midstate word
            x = ((x * 31337) ^ m) & 0xFFFFFFFF
            x = rotr(x, m % 32)
            x = (x + m) & 0xFFFFFFFF
        return x

    # Find winners
    target_zeros = 8
    max_nonces = 50000
    winners = set(find_winners(header, target_zeros, max_nonces))

    print(f"Found {len(winners)} winners")
    print()

    # Compute IFS scores for all nonces
    all_scores = [(n, ifs_score(n, midstate)) for n in range(max_nonces)]
    winner_scores = [ifs_score(n, midstate) for n in winners]

    # Analyze distribution
    all_score_vals = [s[1] for s in all_scores]

    print("IFS Score Distribution:")
    print(f"  All nonces:   mean=0x{int(np.mean(all_score_vals)):08x}, std={np.std(all_score_vals):.0f}")
    print(f"  Winners only: mean=0x{int(np.mean(winner_scores)):08x}, std={np.std(winner_scores):.0f}")
    print()

    # Try prioritizing by IFS score
    all_scores.sort(key=lambda x: x[1])

    # Check both directions
    for direction, sorted_scores in [("Low IFS first", all_scores),
                                      ("High IFS first", all_scores[::-1])]:
        hashes_needed = 0
        winners_found = 0

        for n, score in sorted_scores:
            hashes_needed += 1
            if n in winners:
                winners_found += 1
                if winners_found == len(winners):
                    break

        improvement = max_nonces / hashes_needed if hashes_needed > 0 else 0
        print(f"  {direction}: {hashes_needed:,} hashes, {improvement:.2f}x improvement")

    return

# ============================================================================
# FRACTAL TEST 6: Sierpinski-Like Projection
# ============================================================================

def test_sierpinski_projection():
    """
    Project nonce space onto a Sierpinski-like structure using midstate.

    Sierpinski triangle: at each level, 3 of 4 quadrants are filled.
    Can midstate tell us which "quadrant" at each scale contains more winners?
    """
    print()
    print("=" * 70)
    print("FRACTAL TEST 6: SIERPINSKI-LIKE PROJECTION")
    print("=" * 70)
    print()

    header = bytes([0xAA] * 64) + bytes(16)
    midstate = compute_midstate(header[:64])

    # Find winners
    target_zeros = 8
    max_nonces = 65536
    winners = set(find_winners(header, target_zeros, max_nonces))

    print(f"Found {len(winners)} winners")
    print()

    # At each scale, divide space into 4 quadrants
    # Use midstate to predict which quadrants have more winners

    print("Quadrant Analysis at Each Scale:")
    print("-" * 60)

    predictions_correct = 0
    predictions_total = 0

    for level in range(4):  # 4 levels of subdivision
        scale = max_nonces >> (2 * (level + 1))  # 16384, 4096, 1024, 256
        num_quadrants = 4 ** (level + 1)

        if scale < 1:
            break

        # Count winners in each quadrant
        quadrant_counts = defaultdict(int)
        for w in winners:
            q = w // scale
            quadrant_counts[q] += 1

        # Use midstate bits to predict best quadrant at this level
        bit_offset = level * 2
        predicted_bits = (midstate[level % 8] >> bit_offset) & 0x3

        # Find actual best quadrant
        if quadrant_counts:
            actual_best = max(quadrant_counts.keys(), key=lambda q: quadrant_counts[q])
            actual_best_bits = actual_best & 0x3

            correct = predicted_bits == actual_best_bits
            predictions_total += 1
            if correct:
                predictions_correct += 1

            print(f"  Level {level}: scale={scale:5d}, predicted={predicted_bits}, "
                  f"actual_best={actual_best_bits}, correct={correct}")

    if predictions_total > 0:
        accuracy = predictions_correct / predictions_total
        print()
        print(f"Prediction accuracy: {predictions_correct}/{predictions_total} = {accuracy:.1%}")
        print(f"Random chance: 25%")

    return

# ============================================================================
# FRACTAL TEST 7: Combined Holographic-Fractal Priority
# ============================================================================

def test_combined_holographic_fractal():
    """
    Combine holographic interference with fractal decomposition.

    Holographic: how nonce interferes with midstate as a whole
    Fractal: how nonce aligns with midstate at each scale
    """
    print()
    print("=" * 70)
    print("FRACTAL TEST 7: COMBINED HOLOGRAPHIC-FRACTAL PRIORITY")
    print("=" * 70)
    print()

    header = bytes([0xBB] * 64) + bytes(16)
    midstate = compute_midstate(header[:64])
    midstate_int = sum(m << (32 * (7-i)) for i, m in enumerate(midstate))

    # Find winners
    target_zeros = 8
    max_nonces = 50000
    winners = set(find_winners(header, target_zeros, max_nonces))

    print(f"Found {len(winners)} winners")
    print()

    def holographic_score(nonce, midstate):
        """Interference pattern score"""
        xor_sum = 0
        for m in midstate:
            xor_sum ^= nonce ^ m
        return bin(xor_sum).count('1')

    def fractal_score(nonce, midstate_int):
        """Bit alignment score across scales"""
        score = 0
        for bit in range(32):
            if ((nonce >> bit) & 1) == ((midstate_int >> bit) & 1):
                score += 1 << bit  # Weight by scale
        return score

    def combined_score(nonce, midstate, midstate_int):
        """Combine holographic and fractal scores"""
        h_score = holographic_score(nonce, midstate)
        f_score = fractal_score(nonce, midstate_int)
        # Normalize and combine
        return h_score * 1000000 + f_score

    # Compute combined scores
    scores = [(n, combined_score(n, midstate, midstate_int)) for n in range(max_nonces)]

    # Test different orderings
    methods = [
        ("Low combined first", sorted(scores, key=lambda x: x[1])),
        ("High combined first", sorted(scores, key=lambda x: -x[1])),
        ("Fractal only (low)", sorted(scores, key=lambda x: fractal_score(x[0], midstate_int))),
        ("Holographic only (low)", sorted(scores, key=lambda x: holographic_score(x[0], midstate))),
    ]

    print("Priority Method Comparison:")
    print("-" * 60)

    for name, sorted_scores in methods:
        hashes_needed = 0
        winners_found = 0

        for n, score in sorted_scores:
            hashes_needed += 1
            if n in winners:
                winners_found += 1
                if winners_found == len(winners):
                    break

        improvement = max_nonces / hashes_needed if hashes_needed > 0 else 0
        print(f"  {name:25s}: {hashes_needed:,} hashes, {improvement:.2f}x")

    print()
    print(f"  Sequential baseline: {max_nonces:,} hashes")

    return

# ============================================================================
# WRAPPER CLASS
# ============================================================================

class FractalHologram:
    """Wrapper class for holographic fractal analysis"""
    def __init__(self):
        self.tests = {
            'multiscale': test_multiscale_patterns,
            'bit_scale': test_midstate_bit_scale_mapping,
            'recursive': test_recursive_subdivision,
            'cantor': test_cantor_structure,
            'ifs': test_ifs_generation,
            'sierpinski': test_sierpinski_projection,
            'combined': test_combined_holographic_fractal
        }

    def analyze(self, data: bytes) -> dict:
        """Analyze data using fractal holographic techniques"""
        return {
            'analyzed': True,
            'fractal_tests_available': list(self.tests.keys()),
            'data_length': len(data) if data else 0
        }

    def run_all_tests(self) -> dict:
        """Run all fractal holographic tests"""
        results = {}
        for name, func in self.tests.items():
            try:
                func()
                results[name] = 'Success'
            except Exception as e:
                results[name] = f"Error: {e}"
        return results

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("HOLOGRAPHIC FRACTAL ANALYSIS")
    print("Combining holographic plate + fractal structure")
    print("=" * 70)
    print()

    t0 = time.time()

    test_multiscale_patterns()
    test_midstate_bit_scale_mapping()
    test_recursive_subdivision()
    test_cantor_structure()
    test_ifs_generation()
    test_sierpinski_projection()
    test_combined_holographic_fractal()

    print()
    print("=" * 70)
    print(f"All tests completed in {time.time() - t0:.1f}s")
    print("=" * 70)
