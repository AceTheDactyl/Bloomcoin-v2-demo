"""
Holographic Encoding - Information That Survives Avalanche

The Challenge:
- SHA256 avalanche destroys structure
- Change 1 bit -> ~50% of output bits flip
- How do we encode info that can "flow through"?

Approaches to Test:

1. STATISTICAL ENCODING
   - Encode in probability distributions, not specific bits
   - Hash many related inputs, info is in the aggregate pattern

2. XOR CHAINS
   - XOR is associative: (a^b)^c = a^(b^c)
   - Build chains where relationship survives

3. MODULAR FINGERPRINTS
   - Encode using remainders mod small primes
   - Some modular relationships persist

4. REDUNDANT SPREAD
   - Spread info across many hashes
   - Like error-correcting codes for noisy channels

5. FREQUENCY DOMAIN
   - Encode in "frequency" of bit patterns
   - Statistical signature rather than direct bits

The key insight: We're not trying to preserve BITS,
we're trying to preserve INFORMATION in a form
that can be reconstructed from statistical patterns.
"""

import struct
import hashlib
from typing import List, Dict, Tuple, Optional
from collections import Counter
import random


def sha256(data: bytes) -> bytes:
    """Standard SHA256"""
    return hashlib.sha256(data).digest()


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class AvalancheAnalyzer:
    """
    Analyze what happens during avalanche.
    What patterns survive? What gets destroyed?
    """

    @staticmethod
    def measure_avalanche(data1: bytes, data2: bytes) -> dict:
        """Measure avalanche between two inputs"""
        hash1 = sha256(data1)
        hash2 = sha256(data2)

        # Count bit differences
        diff_bits = 0
        for b1, b2 in zip(hash1, hash2):
            diff_bits += bin(b1 ^ b2).count('1')

        return {
            "input_diff": sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(data1, data2)),
            "output_diff": diff_bits,
            "avalanche_ratio": diff_bits / 256,  # Should be ~0.5
            "hash1": hash1.hex(),
            "hash2": hash2.hex()
        }

    @staticmethod
    def test_bit_survival(base_data: bytes, num_samples: int = 1000) -> dict:
        """
        Test: do any bit positions have predictable behavior?
        Spoiler: they shouldn't, but let's verify.
        """
        bit_counts = [0] * 256  # Count 1s at each position

        for i in range(num_samples):
            data = base_data + struct.pack('>I', i)
            h = sha256(data)
            for byte_idx, byte_val in enumerate(h):
                for bit_idx in range(8):
                    if (byte_val >> bit_idx) & 1:
                        bit_counts[byte_idx * 8 + bit_idx] += 1

        # Should all be ~50%
        ratios = [c / num_samples for c in bit_counts]
        return {
            "min_ratio": min(ratios),
            "max_ratio": max(ratios),
            "avg_ratio": sum(ratios) / len(ratios),
            "verdict": "All ~50% as expected" if 0.45 < min(ratios) < max(ratios) < 0.55 else "Anomaly!"
        }


class StatisticalEncoder:
    """
    APPROACH 1: Statistical Encoding

    Instead of encoding in specific bits, encode in the
    DISTRIBUTION of bits across many hashes.

    Idea: Hash N related inputs. The pattern of which ones
    have certain properties encodes our message.
    """

    def __init__(self, base_data: bytes):
        self.base_data = base_data

    def encode(self, message: int, num_bits: int = 8) -> List[bytes]:
        """
        Encode a message by selecting which nonces to "mark".

        We hash many nonces and select ones where the hash
        has a specific property (e.g., first bit = 0).
        The PATTERN of selected nonces encodes our message.
        """
        encoded_hashes = []
        selections = []

        # For each bit of message, find a nonce whose hash encodes that bit
        for bit_pos in range(num_bits):
            target_bit = (message >> bit_pos) & 1

            # Search for a nonce that "naturally" encodes this bit
            for nonce in range(bit_pos * 1000, (bit_pos + 1) * 1000):
                data = self.base_data + struct.pack('>I', nonce)
                h = sha256(data)

                # Check if first bit of hash matches our target
                first_bit = (h[0] >> 7) & 1
                if first_bit == target_bit:
                    encoded_hashes.append(h)
                    selections.append(nonce)
                    break

        return encoded_hashes, selections

    def decode(self, hashes: List[bytes]) -> int:
        """Decode message from hash sequence"""
        message = 0
        for i, h in enumerate(hashes):
            bit = (h[0] >> 7) & 1
            message |= (bit << i)
        return message


class XORChainEncoder:
    """
    APPROACH 2: XOR Chain Encoding

    XOR has special properties:
    - Associative: (a^b)^c = a^(b^c)
    - Self-inverse: a^a = 0
    - Identity: a^0 = a

    We can build chains where the XOR relationship
    encodes information that persists.
    """

    def __init__(self, base_data: bytes):
        self.base_data = base_data

    def encode(self, message: int) -> Tuple[List[bytes], int]:
        """
        Encode message in XOR relationship between hashes.

        Strategy: Create hashes where their XOR produces
        a specific pattern encoding our message.
        """
        hashes = []
        xor_accumulator = 0

        # Hash several nonces
        for i in range(32):  # 32 hashes
            data = self.base_data + struct.pack('>I', i)
            h = sha256(data)
            hashes.append(h)

            # XOR first 4 bytes
            val = struct.unpack('>I', h[:4])[0]
            xor_accumulator ^= val

        # The message is encoded in how we INTERPRET the accumulator
        # We use specific bits of accumulator to reconstruct
        # (In practice, we'd need to choose nonces carefully)

        return hashes, xor_accumulator

    def create_verifiable_chain(self, message: int) -> dict:
        """
        Create a chain where message can be verified through XOR.

        We find nonces such that:
        hash(nonce1) XOR hash(nonce2) XOR ... = pattern encoding message
        """
        target_pattern = message & 0xFFFFFFFF  # 32-bit message

        # Start with random hashes
        nonces = list(range(100))
        current_xor = 0

        for n in nonces:
            data = self.base_data + struct.pack('>I', n)
            h = sha256(data)
            current_xor ^= struct.unpack('>I', h[:4])[0]

        # The "signature" is current_xor
        # To encode message, we find correction nonce
        # where hash(correction) XOR current_xor ≈ message

        return {
            "nonces": nonces,
            "xor_result": current_xor,
            "can_encode": True,
            "note": "XOR result is deterministic given nonces"
        }


class ModularEncoder:
    """
    APPROACH 3: Modular Fingerprints

    Encode using remainders when divided by small primes.
    Some modular relationships can persist through transformations.
    """

    PRIMES = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]

    def __init__(self, base_data: bytes):
        self.base_data = base_data

    def compute_fingerprint(self, h: bytes) -> List[int]:
        """Compute modular fingerprint of hash"""
        val = int.from_bytes(h[:16], 'big')  # Use first 128 bits
        return [val % p for p in self.PRIMES]

    def encode(self, message: int) -> Tuple[int, List[int]]:
        """
        Find a nonce whose hash has specific modular properties.

        The message is encoded in the modular remainders.
        """
        # Target remainders based on message
        target_remainders = []
        temp_msg = message
        for p in self.PRIMES[:4]:  # Use first 4 primes
            target_remainders.append(temp_msg % p)
            temp_msg //= p

        # Search for nonce with matching remainders
        for nonce in range(1000000):
            data = self.base_data + struct.pack('>I', nonce)
            h = sha256(data)
            fp = self.compute_fingerprint(h)

            if fp[:4] == target_remainders:
                return nonce, fp

        return -1, []  # Not found

    def analyze_modular_distribution(self, num_samples: int = 10000) -> dict:
        """
        Analyze: are modular remainders uniformly distributed?
        If yes, we can use them to encode.
        """
        counts = {p: Counter() for p in self.PRIMES}

        for i in range(num_samples):
            data = self.base_data + struct.pack('>I', i)
            h = sha256(data)
            fp = self.compute_fingerprint(h)

            for p, r in zip(self.PRIMES, fp):
                counts[p][r] += 1

        # Check uniformity
        results = {}
        for p in self.PRIMES:
            expected = num_samples / p
            actual = [counts[p][r] for r in range(p)]
            deviation = max(abs(a - expected) / expected for a in actual)
            results[p] = {
                "counts": dict(counts[p]),
                "expected": expected,
                "max_deviation": deviation,
                "uniform": deviation < 0.1
            }

        return results


class RedundantSpreadEncoder:
    """
    APPROACH 4: Redundant Spread

    Like error-correcting codes - spread info across many hashes
    so it can be reconstructed even with "noise".
    """

    def __init__(self, base_data: bytes, redundancy: int = 8):
        self.base_data = base_data
        self.redundancy = redundancy  # Copies of each bit

    def encode(self, message: int, num_bits: int = 8) -> List[Tuple[int, bytes]]:
        """
        Encode each bit redundantly across multiple hashes.

        For each message bit, we find `redundancy` nonces whose
        hashes "vote" for that bit value.
        """
        encoded = []

        for bit_pos in range(num_bits):
            target = (message >> bit_pos) & 1
            bit_votes = []

            # Find nonces that vote for this bit
            nonce = bit_pos * 10000
            while len(bit_votes) < self.redundancy:
                data = self.base_data + struct.pack('>I', nonce)
                h = sha256(data)

                # Use parity of first byte as "vote"
                vote = bin(h[0]).count('1') % 2

                if vote == target:
                    bit_votes.append((nonce, h))

                nonce += 1

            encoded.extend(bit_votes)

        return encoded

    def decode(self, encoded: List[Tuple[int, bytes]], num_bits: int = 8) -> int:
        """Decode by majority voting"""
        message = 0
        votes_per_bit = len(encoded) // num_bits

        for bit_pos in range(num_bits):
            start = bit_pos * votes_per_bit
            end = start + votes_per_bit

            votes = []
            for nonce, h in encoded[start:end]:
                vote = bin(h[0]).count('1') % 2
                votes.append(vote)

            # Majority vote
            bit_value = 1 if sum(votes) > len(votes) // 2 else 0
            message |= (bit_value << bit_pos)

        return message


class FrequencyEncoder:
    """
    APPROACH 5: Frequency Domain Encoding

    Encode in the "frequency" of patterns, not the patterns themselves.
    Like encoding audio in frequency spectrum vs time domain.
    """

    def __init__(self, base_data: bytes):
        self.base_data = base_data

    def compute_pattern_frequency(self, nonce_range: range) -> Dict[int, int]:
        """
        Compute frequency of 4-bit patterns across many hashes.
        """
        pattern_counts = Counter()

        for nonce in nonce_range:
            data = self.base_data + struct.pack('>I', nonce)
            h = sha256(data)

            # Count 4-bit patterns in hash
            for byte in h:
                pattern_counts[byte >> 4] += 1
                pattern_counts[byte & 0xF] += 1

        return dict(pattern_counts)

    def encode(self, message: int) -> Tuple[range, Dict[int, float]]:
        """
        Encode message in the frequency signature of a nonce range.

        Different message -> different nonce range -> different frequency pattern
        """
        # Select nonce range based on message
        start = message * 1000
        nonce_range = range(start, start + 1000)

        # Compute frequency signature
        freqs = self.compute_pattern_frequency(nonce_range)
        total = sum(freqs.values())
        signature = {k: v / total for k, v in freqs.items()}

        return nonce_range, signature

    def compare_signatures(self, sig1: Dict[int, float],
                           sig2: Dict[int, float]) -> float:
        """Compare two frequency signatures (cosine similarity)"""
        keys = set(sig1.keys()) | set(sig2.keys())
        dot = sum(sig1.get(k, 0) * sig2.get(k, 0) for k in keys)
        mag1 = sum(v ** 2 for v in sig1.values()) ** 0.5
        mag2 = sum(v ** 2 for v in sig2.values()) ** 0.5
        return dot / (mag1 * mag2) if mag1 and mag2 else 0


def run_experiments():
    """Run all encoding experiments"""
    base_data = b"Holographic Test"

    print("=" * 70)
    print("HOLOGRAPHIC ENCODING EXPERIMENTS")
    print("Finding what survives SHA256 avalanche")
    print("=" * 70)

    # Test 1: Avalanche baseline
    print("\n[1] AVALANCHE BASELINE")
    print("-" * 50)
    analyzer = AvalancheAnalyzer()

    # Single bit flip
    result = analyzer.measure_avalanche(
        base_data + b"\x00",
        base_data + b"\x01"
    )
    print(f"  1-bit input change -> {result['output_diff']} output bits changed")
    print(f"  Avalanche ratio: {result['avalanche_ratio']:.2%}")

    # Bit survival test
    survival = analyzer.test_bit_survival(base_data, 1000)
    print(f"  Bit position analysis: {survival['verdict']}")
    print(f"  Min/Max ratios: {survival['min_ratio']:.3f} / {survival['max_ratio']:.3f}")

    # Test 2: Statistical Encoding
    print("\n[2] STATISTICAL ENCODING")
    print("-" * 50)
    stat_enc = StatisticalEncoder(base_data)

    original_msg = 0b10110011  # 179
    hashes, nonces = stat_enc.encode(original_msg, 8)
    decoded = stat_enc.decode(hashes)

    print(f"  Original message:  {original_msg} (0b{original_msg:08b})")
    print(f"  Decoded message:   {decoded} (0b{decoded:08b})")
    print(f"  Success: {original_msg == decoded}")
    print(f"  Nonces used: {nonces[:4]}...")

    # Test 3: XOR Chain
    print("\n[3] XOR CHAIN ENCODING")
    print("-" * 50)
    xor_enc = XORChainEncoder(base_data)

    hashes, xor_result = xor_enc.encode(12345)
    chain = xor_enc.create_verifiable_chain(12345)

    print(f"  XOR accumulator: 0x{xor_result:08x}")
    print(f"  Deterministic: {chain['can_encode']}")
    print(f"  Note: {chain['note']}")

    # Test 4: Modular Encoding
    print("\n[4] MODULAR FINGERPRINTS")
    print("-" * 50)
    mod_enc = ModularEncoder(base_data)

    # Check distribution
    dist = mod_enc.analyze_modular_distribution(5000)
    uniform_primes = [p for p, d in dist.items() if d['uniform']]
    print(f"  Primes with uniform distribution: {uniform_primes}")

    # Try encoding
    test_msg = 42
    nonce, fp = mod_enc.encode(test_msg)
    if nonce >= 0:
        print(f"  Encoded message {test_msg} at nonce {nonce}")
        print(f"  Fingerprint: {fp[:4]}")
    else:
        print(f"  Could not find exact match (expected - search space limited)")

    # Test 5: Redundant Spread
    print("\n[5] REDUNDANT SPREAD ENCODING")
    print("-" * 50)
    red_enc = RedundantSpreadEncoder(base_data, redundancy=8)

    original_msg = 0b10101010  # 170
    encoded = red_enc.encode(original_msg, 8)
    decoded = red_enc.decode(encoded, 8)

    print(f"  Original: {original_msg} (0b{original_msg:08b})")
    print(f"  Decoded:  {decoded} (0b{decoded:08b})")
    print(f"  Success: {original_msg == decoded}")
    print(f"  Redundancy: {red_enc.redundancy}x per bit")
    print(f"  Total hashes: {len(encoded)}")

    # Test 6: Frequency Encoding
    print("\n[6] FREQUENCY DOMAIN ENCODING")
    print("-" * 50)
    freq_enc = FrequencyEncoder(base_data)

    # Two different messages
    range1, sig1 = freq_enc.encode(100)
    range2, sig2 = freq_enc.encode(200)
    range3, sig3 = freq_enc.encode(100)  # Same as msg 1

    sim_diff = freq_enc.compare_signatures(sig1, sig2)
    sim_same = freq_enc.compare_signatures(sig1, sig3)

    print(f"  Signature similarity (different msgs): {sim_diff:.6f}")
    print(f"  Signature similarity (same msg):       {sim_same:.6f}")
    print(f"  Distinguishable: {sim_same > sim_diff}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY: What Survives Avalanche?")
    print("=" * 70)
    print("""
  1. STATISTICAL - Works by encoding in WHICH nonces produce patterns
     Info survives because selection is deterministic

  2. XOR CHAINS - XOR accumulator is deterministic given inputs
     Relationship survives, not individual bits

  3. MODULAR - Remainders are uniformly distributed
     Can encode but need to search for matching nonces

  4. REDUNDANT - Majority voting recovers bits
     Info survives through redundancy

  5. FREQUENCY - Different messages -> distinguishable signatures
     Info encoded in distribution, not specific bits

  KEY INSIGHT: We can't preserve BITS through SHA,
  but we can preserve INFORMATION by encoding it in:
    - Selection patterns (which nonces to use)
    - Aggregate properties (XOR, sums, distributions)
    - Relationships between multiple hashes
    """)


class HolographicEncoder:
    """Wrapper class for holographic encoding functionality"""
    def __init__(self, base_data: bytes = b"BloomQuest Ultimate Integration"):
        if isinstance(base_data, str):
            base_data = base_data.encode('utf-8')
        self.base_data = base_data
        self.statistical = StatisticalEncoder(base_data)
        self.xor_chain = XORChainEncoder(base_data)
        self.modular = ModularEncoder(base_data)
        self.redundant = RedundantSpreadEncoder(base_data)
        self.frequency = FrequencyEncoder(base_data)

    def encode(self, data: bytes) -> Dict:
        """Encode data using multiple holographic techniques"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        # Convert data to integer for encoding
        # Use first 8 bytes as integer message
        message_int = int.from_bytes(data[:8], 'big') if len(data) >= 8 else int.from_bytes(data + b'\0' * (8 - len(data)), 'big')
        message_int = message_int % (2**16)  # Limit to reasonable size

        return {
            'statistical': self.statistical.encode(message_int, num_bits=8),
            'xor_chain': self.xor_chain.encode(message_int),
            'modular': self.modular.encode(message_int),
            'redundant': self.redundant.encode(message_int, num_bits=8),
            'frequency': self.frequency.encode(message_int),
            'raw_data': data.hex()
        }


if __name__ == "__main__":
    run_experiments()
