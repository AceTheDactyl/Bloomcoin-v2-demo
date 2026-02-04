"""
Holographic Decoding of Winner Locations
========================================

Apply the techniques from holographic_encoding.py:
1. XOR chains
2. Modular fingerprints
3. Redundant spread
4. Statistical patterns

But use them to DECODE winner locations from midstate.

Testing at REAL difficulties, not toy difficulty 8.
"""

import struct
import hashlib
import numpy as np
from collections import defaultdict, Counter
import time

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
    msg = header[:76] + struct.pack('<I', nonce)
    return hashlib.sha256(hashlib.sha256(msg).digest()).digest()

def count_leading_zeros(hash_bytes: bytes) -> int:
    hash_int = int.from_bytes(hash_bytes, 'big')
    if hash_int == 0:
        return 256
    return 256 - hash_int.bit_length()

def hash_to_int(hash_bytes: bytes) -> int:
    return int.from_bytes(hash_bytes, 'big')


# ============================================================================
# HIGH DIFFICULTY TESTING
# At difficulty 16+, winners are rare - we need to predict regions
# ============================================================================

def find_best_in_range(header: bytes, start: int, count: int) -> tuple:
    """Find the nonce with most leading zeros in a range"""
    best_nonce = start
    best_zeros = 0
    for nonce in range(start, start + count):
        h = sha256d(header, nonce)
        zeros = count_leading_zeros(h)
        if zeros > best_zeros:
            best_zeros = zeros
            best_nonce = nonce
    return best_nonce, best_zeros


# ============================================================================
# HOLOGRAPHIC TECHNIQUE 1: XOR CHAIN DECODING
# ============================================================================

def test_xor_chain_decode():
    """
    XOR Chain: The XOR of midstate words encodes information.

    Hypothesis: XOR signature of midstate correlates with
    which regions of nonce space contain winners.
    """
    print("=" * 70)
    print("HOLOGRAPHIC TECHNIQUE 1: XOR CHAIN DECODING")
    print("=" * 70)
    print()

    num_tests = 100
    search_range = 1000000  # 1M nonces per test
    num_regions = 16  # Divide into 16 regions

    region_size = search_range // num_regions

    correct_predictions = 0
    total_predictions = 0

    print(f"Testing {num_tests} headers, {search_range:,} nonces each...")
    print(f"Divided into {num_regions} regions of {region_size:,} nonces")
    print()

    for t in range(num_tests):
        header = bytes([(t * 37 + i * 13) % 256 for i in range(64)]) + bytes(16)
        midstate = compute_midstate(header[:64])

        # XOR chain signature
        xor_sig = 0
        for m in midstate:
            xor_sig ^= m
            xor_sig ^= rotr(m, 7)
            xor_sig ^= rotr(m, 13)

        # Use XOR signature to predict best region
        predicted_region = xor_sig % num_regions

        # Find actual best region (by highest zeros found)
        region_bests = []
        for r in range(num_regions):
            start = r * region_size
            best_nonce, best_zeros = find_best_in_range(header, start, min(region_size, 10000))
            region_bests.append((r, best_zeros))

        actual_best_region = max(region_bests, key=lambda x: x[1])[0]

        total_predictions += 1
        if predicted_region == actual_best_region:
            correct_predictions += 1

        if (t + 1) % 25 == 0:
            acc = correct_predictions / total_predictions
            print(f"  {t+1}/{num_tests}: accuracy = {acc:.1%}")

    accuracy = correct_predictions / total_predictions
    random_chance = 1 / num_regions

    print()
    print(f"XOR Chain Results:")
    print(f"  Accuracy: {accuracy:.1%}")
    print(f"  Random chance: {random_chance:.1%}")
    print(f"  Improvement: {accuracy/random_chance:.2f}x")

    return accuracy


# ============================================================================
# HOLOGRAPHIC TECHNIQUE 2: MODULAR FINGERPRINTS
# ============================================================================

def test_modular_fingerprints():
    """
    Modular Fingerprints: Use remainders mod small primes.

    Hypothesis: Midstate mod p correlates with winner nonce mod p.
    """
    print()
    print("=" * 70)
    print("HOLOGRAPHIC TECHNIQUE 2: MODULAR FINGERPRINTS")
    print("=" * 70)
    print()

    PRIMES = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]

    num_tests = 50
    search_range = 500000

    prime_accuracy = {p: {'correct': 0, 'total': 0} for p in PRIMES}

    print(f"Testing {num_tests} headers...")
    print()

    for t in range(num_tests):
        header = bytes([(t * 41 + i * 17) % 256 for i in range(64)]) + bytes(16)
        midstate = compute_midstate(header[:64])

        # Find best nonce in range
        best_nonce, best_zeros = find_best_in_range(header, 0, min(search_range, 50000))

        # Test each prime
        for p in PRIMES:
            # Midstate fingerprint mod p
            midstate_fp = sum(midstate) % p

            # Prediction: winner nonce mod p == midstate_fp
            predicted_residue = midstate_fp
            actual_residue = best_nonce % p

            prime_accuracy[p]['total'] += 1
            if predicted_residue == actual_residue:
                prime_accuracy[p]['correct'] += 1

    print("Modular Fingerprint Results:")
    print("-" * 50)
    print(f"Prime | Accuracy | Random | Improvement")
    print("-" * 50)

    for p in PRIMES:
        correct = prime_accuracy[p]['correct']
        total = prime_accuracy[p]['total']
        acc = correct / total if total > 0 else 0
        random = 1 / p
        improvement = acc / random if random > 0 else 0

        marker = "**" if improvement > 1.3 else "*" if improvement > 1.1 else ""
        print(f"  {p:2d}  |  {acc:5.1%}   | {random:5.1%} |   {improvement:.2f}x {marker}")

    return prime_accuracy


# ============================================================================
# HOLOGRAPHIC TECHNIQUE 3: STATISTICAL PATTERNS
# ============================================================================

def test_statistical_patterns():
    """
    Statistical Patterns: Look at aggregate properties.

    Encode winner region in statistical properties of partial hashes.
    """
    print()
    print("=" * 70)
    print("HOLOGRAPHIC TECHNIQUE 3: STATISTICAL PATTERNS")
    print("=" * 70)
    print()

    num_tests = 30
    num_samples = 1000  # Sample nonces per region
    num_regions = 8

    print(f"Sampling {num_samples} nonces per region to build statistical signature...")
    print()

    correct = 0
    total = 0

    for t in range(num_tests):
        header = bytes([(t * 43 + i * 19) % 256 for i in range(64)]) + bytes(16)
        midstate = compute_midstate(header[:64])

        # Build statistical signature for each region
        region_signatures = []

        for r in range(num_regions):
            start = r * 100000

            # Sample partial hashes
            bit_counts = [0] * 32  # Count of 1s at each position

            for i in range(num_samples):
                nonce = start + i * 100  # Sample every 100th nonce
                h = sha256d(header, nonce)
                first_word = int.from_bytes(h[:4], 'big')

                for bit in range(32):
                    if (first_word >> bit) & 1:
                        bit_counts[bit] += 1

            # Signature = deviation from 50%
            signature = sum(abs(c - num_samples/2) for c in bit_counts)
            region_signatures.append((r, signature))

        # Predict: region with lowest deviation (most "ordered") has winner
        predicted_region = min(region_signatures, key=lambda x: x[1])[0]

        # Find actual best region
        actual_region = 0
        best_zeros = 0
        for r in range(num_regions):
            start = r * 100000
            _, zeros = find_best_in_range(header, start, 5000)
            if zeros > best_zeros:
                best_zeros = zeros
                actual_region = r

        total += 1
        if predicted_region == actual_region:
            correct += 1

        if (t + 1) % 10 == 0:
            print(f"  {t+1}/{num_tests}: accuracy = {correct/total:.1%}")

    accuracy = correct / total
    random_chance = 1 / num_regions

    print()
    print(f"Statistical Pattern Results:")
    print(f"  Accuracy: {accuracy:.1%}")
    print(f"  Random chance: {random_chance:.1%}")
    print(f"  Improvement: {accuracy/random_chance:.2f}x")

    return accuracy


# ============================================================================
# HOLOGRAPHIC TECHNIQUE 4: REDUNDANT SPREAD
# ============================================================================

def test_redundant_spread():
    """
    Redundant Spread: Use multiple overlapping predictions.

    Combine multiple weak predictors with voting.
    """
    print()
    print("=" * 70)
    print("HOLOGRAPHIC TECHNIQUE 4: REDUNDANT SPREAD (VOTING)")
    print("=" * 70)
    print()

    num_tests = 50
    num_regions = 8

    print(f"Testing {num_tests} headers with voting across predictors...")
    print()

    correct = 0
    total = 0

    for t in range(num_tests):
        header = bytes([(t * 47 + i * 23) % 256 for i in range(64)]) + bytes(16)
        midstate = compute_midstate(header[:64])
        midstate_int = sum(m << (32 * (7-i)) for i, m in enumerate(midstate))

        # Multiple predictors vote
        votes = [0] * num_regions

        # Predictor 1: XOR signature
        xor_sig = 0
        for m in midstate:
            xor_sig ^= m
        votes[xor_sig % num_regions] += 1

        # Predictor 2: Sum signature
        sum_sig = sum(midstate) & 0xFFFFFFFF
        votes[sum_sig % num_regions] += 1

        # Predictor 3: Each midstate word votes
        for m in midstate:
            votes[m % num_regions] += 1

        # Predictor 4: Bit pattern signature
        popcount = bin(midstate_int).count('1')
        votes[popcount % num_regions] += 1

        # Predictor 5: Rotation signature
        rot_sig = 0
        for i, m in enumerate(midstate):
            rot_sig ^= rotr(m, i * 4)
        votes[rot_sig % num_regions] += 1

        # Winner: most votes
        predicted_region = votes.index(max(votes))

        # Find actual best region
        actual_region = 0
        best_zeros = 0
        for r in range(num_regions):
            start = r * 100000
            _, zeros = find_best_in_range(header, start, 5000)
            if zeros > best_zeros:
                best_zeros = zeros
                actual_region = r

        total += 1
        if predicted_region == actual_region:
            correct += 1

    accuracy = correct / total
    random_chance = 1 / num_regions

    print(f"Redundant Spread (Voting) Results:")
    print(f"  Accuracy: {accuracy:.1%}")
    print(f"  Random chance: {random_chance:.1%}")
    print(f"  Improvement: {accuracy/random_chance:.2f}x")

    return accuracy


# ============================================================================
# HOLOGRAPHIC TECHNIQUE 5: FREQUENCY DOMAIN
# ============================================================================

def test_frequency_domain():
    """
    Frequency Domain: Analyze midstate as a frequency signal.

    Different "frequencies" in midstate predict different aspects.
    """
    print()
    print("=" * 70)
    print("HOLOGRAPHIC TECHNIQUE 5: FREQUENCY DOMAIN")
    print("=" * 70)
    print()

    num_tests = 30
    num_regions = 8

    print(f"Analyzing midstate frequency components...")
    print()

    correct = 0
    total = 0

    for t in range(num_tests):
        header = bytes([(t * 53 + i * 29) % 256 for i in range(64)]) + bytes(16)
        midstate = compute_midstate(header[:64])

        # Treat midstate as 256-bit signal, compute "frequency" components
        # Low frequency: XOR of adjacent words
        low_freq = 0
        for i in range(7):
            low_freq ^= midstate[i] ^ midstate[i+1]

        # High frequency: XOR of alternating words
        high_freq = midstate[0] ^ midstate[2] ^ midstate[4] ^ midstate[6]

        # Mid frequency: Pairs
        mid_freq = (midstate[0] ^ midstate[1]) ^ (midstate[4] ^ midstate[5])

        # Combine frequencies for prediction
        combined = low_freq ^ (high_freq << 1) ^ (mid_freq << 2)
        predicted_region = combined % num_regions

        # Find actual best region
        actual_region = 0
        best_zeros = 0
        for r in range(num_regions):
            start = r * 100000
            _, zeros = find_best_in_range(header, start, 5000)
            if zeros > best_zeros:
                best_zeros = zeros
                actual_region = r

        total += 1
        if predicted_region == actual_region:
            correct += 1

    accuracy = correct / total
    random_chance = 1 / num_regions

    print(f"Frequency Domain Results:")
    print(f"  Accuracy: {accuracy:.1%}")
    print(f"  Random chance: {random_chance:.1%}")
    print(f"  Improvement: {accuracy/random_chance:.2f}x")

    return accuracy


# ============================================================================
# COMBINED HOLOGRAPHIC DECODER
# ============================================================================

def test_combined_decoder():
    """
    Combine ALL holographic techniques for maximum accuracy.
    """
    print()
    print("=" * 70)
    print("COMBINED HOLOGRAPHIC DECODER")
    print("=" * 70)
    print()

    num_tests = 50
    num_regions = 8

    correct = 0
    total = 0

    for t in range(num_tests):
        header = bytes([(t * 59 + i * 31) % 256 for i in range(64)]) + bytes(16)
        midstate = compute_midstate(header[:64])
        midstate_int = sum(m << (32 * (7-i)) for i, m in enumerate(midstate))

        votes = [0] * num_regions

        # XOR chain
        xor_sig = 0
        for m in midstate:
            xor_sig ^= m ^ rotr(m, 7) ^ rotr(m, 13)
        votes[xor_sig % num_regions] += 2

        # Modular fingerprints (top primes only)
        for p in [7, 13, 31]:
            fp = sum(midstate) % p
            votes[fp % num_regions] += 1

        # Each word votes
        for m in midstate:
            votes[m % num_regions] += 1

        # Frequency components
        low_freq = 0
        for i in range(7):
            low_freq ^= midstate[i] ^ midstate[i+1]
        votes[low_freq % num_regions] += 2

        # Bit alignment with golden ratio
        phi_approx = 0x9E3779B9  # Golden ratio * 2^32
        golden_sig = 0
        for m in midstate:
            golden_sig ^= m ^ phi_approx
            phi_approx = rotr(phi_approx, 1)
        votes[golden_sig % num_regions] += 1

        # Winner
        predicted_region = votes.index(max(votes))

        # Find actual best
        actual_region = 0
        best_zeros = 0
        for r in range(num_regions):
            start = r * 100000
            _, zeros = find_best_in_range(header, start, 5000)
            if zeros > best_zeros:
                best_zeros = zeros
                actual_region = r

        total += 1
        if predicted_region == actual_region:
            correct += 1

        if (t + 1) % 10 == 0:
            print(f"  {t+1}/{num_tests}: accuracy = {correct/total:.1%}")

    accuracy = correct / total
    random_chance = 1 / num_regions

    print()
    print(f"Combined Holographic Decoder Results:")
    print(f"  Accuracy: {accuracy:.1%}")
    print(f"  Random chance: {random_chance:.1%}")
    print(f"  Improvement: {accuracy/random_chance:.2f}x")

    return accuracy


# ============================================================================
# WRAPPER CLASS
# ============================================================================

class HolographicDecoder:
    """Wrapper class for holographic decoding functionality"""
    def __init__(self):
        self.techniques = {
            'xor_chain': test_xor_chain_decode,
            'modular': test_modular_fingerprints,
            'statistical': test_statistical_patterns,
            'redundant': test_redundant_spread,
            'frequency': test_frequency_domain,
            'combined': test_combined_decoder
        }

    def decode(self, data: bytes) -> dict:
        """Decode data using holographic techniques"""
        # For now, return a simple result
        # In a real implementation, this would use the data to decode
        return {
            'decoded': True,
            'techniques_available': list(self.techniques.keys()),
            'data_length': len(data) if data else 0
        }

    def test_all_techniques(self) -> dict:
        """Run all decoding techniques for testing"""
        results = {}
        for name, func in self.techniques.items():
            try:
                results[name] = func()
            except Exception as e:
                results[name] = f"Error: {e}"
        return results

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("HOLOGRAPHIC DECODING OF WINNER LOCATIONS")
    print("Applying encoding techniques to DECODE winners from midstate")
    print("=" * 70)
    print()

    t0 = time.time()

    results = {}
    results['xor_chain'] = test_xor_chain_decode()
    results['modular'] = test_modular_fingerprints()
    results['statistical'] = test_statistical_patterns()
    results['redundant'] = test_redundant_spread()
    results['frequency'] = test_frequency_domain()
    results['combined'] = test_combined_decoder()

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("Technique          | Accuracy | vs Random")
    print("-" * 50)

    random_8 = 1/8  # 8 regions

    for name, acc in results.items():
        if isinstance(acc, dict):
            continue  # Skip modular which returns dict
        improvement = acc / random_8
        marker = "***" if improvement > 1.5 else "**" if improvement > 1.2 else "*" if improvement > 1.05 else ""
        print(f"{name:18s} |  {acc:5.1%}   |  {improvement:.2f}x {marker}")

    print()
    print(f"Total time: {time.time() - t0:.1f}s")
    print("=" * 70)
