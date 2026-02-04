"""
Holographic Encoding Stress Test

Push the encoding to its limits.
At what corruption rate does it fail?
Can we increase redundancy to survive worse conditions?
"""

import struct
import hashlib
from typing import List, Tuple
from dataclasses import dataclass
import random


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


@dataclass
class Fragment:
    index: int
    nonce: int
    hash_value: bytes
    bit: int


class HolographicCodec:
    """
    Holographic encoder/decoder with configurable redundancy.
    """

    def __init__(self, base_key: bytes, redundancy: int = 4):
        self.base_key = base_key
        self.redundancy = redundancy

    def encode(self, message: int, num_bits: int = 32) -> List[Fragment]:
        """Encode message with redundancy"""
        fragments = []

        for bit_pos in range(num_bits):
            target = (message >> bit_pos) & 1
            search_start = bit_pos * 1000
            found = 0

            for nonce in range(search_start, search_start + 10000):
                if found >= self.redundancy:
                    break

                data = self.base_key + struct.pack('>II', nonce, bit_pos)
                h = sha256(data)
                natural_bit = (h[0] >> 7) & 1

                if natural_bit == target:
                    fragments.append(Fragment(
                        index=len(fragments),
                        nonce=nonce,
                        hash_value=h,
                        bit=target
                    ))
                    found += 1

        return fragments

    def decode(self, fragments: List[Fragment], num_bits: int = 32) -> int:
        """Decode using majority voting"""
        frags_per_bit = len(fragments) // num_bits
        message = 0

        for bit_pos in range(num_bits):
            start = bit_pos * frags_per_bit
            end = start + frags_per_bit
            votes = [f.bit for f in fragments[start:end]]

            # Majority vote
            bit = 1 if sum(votes) > len(votes) // 2 else 0
            message |= (bit << bit_pos)

        return message


def corrupt_fragments(fragments: List[Fragment], rate: float) -> Tuple[List[Fragment], int]:
    """Corrupt fragments at given rate"""
    result = []
    corrupted = 0

    for f in fragments:
        if random.random() < rate:
            result.append(Fragment(f.index, f.nonce, f.hash_value, 1 - f.bit))
            corrupted += 1
        else:
            result.append(f)

    return result, corrupted


def run_stress_test():
    print("=" * 70)
    print("HOLOGRAPHIC ENCODING STRESS TEST")
    print("=" * 70)

    codec = HolographicCodec(b"StressTest", redundancy=4)
    test_message = 0xDEADBEEF  # 32-bit test message

    print(f"\nTest message: 0x{test_message:08x}")
    print(f"Redundancy: {codec.redundancy}x per bit")
    print()

    # Encode
    fragments = codec.encode(test_message)
    print(f"Fragments created: {len(fragments)}")
    print()

    # Test various corruption rates
    print("Corruption Rate | Corrupted | Decoded      | Match")
    print("-" * 60)

    corruption_rates = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]

    for rate in corruption_rates:
        random.seed(42)  # Reproducible
        corrupted_frags, num_corrupted = corrupt_fragments(fragments, rate)
        decoded = codec.decode(corrupted_frags)
        match = decoded == test_message

        status = "OK" if match else "FAILED"
        print(f"    {rate*100:5.1f}%      |   {num_corrupted:3d}     | 0x{decoded:08x}  | {status}")

    # Now test with higher redundancy
    print()
    print("=" * 70)
    print("INCREASING REDUNDANCY")
    print("=" * 70)

    for redundancy in [4, 8, 16, 32]:
        codec = HolographicCodec(b"StressTest", redundancy=redundancy)
        fragments = codec.encode(test_message)

        print(f"\nRedundancy: {redundancy}x ({len(fragments)} fragments)")
        print("-" * 50)

        # Find breaking point
        last_success = 0
        for rate in [0.1, 0.2, 0.3, 0.4, 0.45, 0.49]:
            random.seed(42)
            corrupted_frags, _ = corrupt_fragments(fragments, rate)
            decoded = codec.decode(corrupted_frags)
            if decoded == test_message:
                last_success = rate

        print(f"  Survives up to ~{last_success*100:.0f}% corruption")

    # Theoretical limit
    print()
    print("=" * 70)
    print("THEORETICAL ANALYSIS")
    print("=" * 70)
    print("""
  With majority voting and N copies per bit:
  - Need > 50% of copies to be correct
  - If corruption rate = p, probability correct bit = 1 - p
  - Probability majority correct = sum of binomial(N, k) * (1-p)^k * p^(N-k)
    for k > N/2

  For large N:
  - Can survive corruption rates approaching 50%
  - At exactly 50%, it's random (50/50 chance per bit)
  - Above 50%, majority voting INVERTS (would need to flip result)

  KEY INSIGHT:
  - Majority voting has a hard limit at 50% corruption
  - But in practice, even ~40% corruption starts causing errors
  - More redundancy = closer to theoretical limit
  - 32x redundancy can survive ~45% corruption reliably
    """)

    # What about XOR signature for verification?
    print()
    print("=" * 70)
    print("XOR SIGNATURE VERIFICATION")
    print("=" * 70)

    codec = HolographicCodec(b"XORTest", redundancy=8)
    fragments = codec.encode(test_message)

    # Compute original XOR signature
    original_xor = 0
    for f in fragments:
        original_xor ^= struct.unpack('>I', f.hash_value[:4])[0]

    print(f"Original XOR signature: 0x{original_xor:08x}")
    print()

    # Check if XOR can detect corruption
    for rate in [0.1, 0.2, 0.3]:
        random.seed(42)
        corrupted_frags, num_corrupted = corrupt_fragments(fragments, rate)

        # XOR doesn't change for bit flips in .bit field (we only flip metadata)
        # But if we model hash corruption...
        corrupted_xor = 0
        for f in corrupted_frags:
            corrupted_xor ^= struct.unpack('>I', f.hash_value[:4])[0]

        xor_match = corrupted_xor == original_xor
        decoded = codec.decode(corrupted_frags)
        content_match = decoded == test_message

        print(f"  {rate*100:.0f}% corruption: XOR match={xor_match}, Content match={content_match}")

    print()
    print("  Note: XOR signature detects hash corruption, not bit metadata corruption")
    print("  For full verification, need both XOR check AND majority voting")


if __name__ == "__main__":
    run_stress_test()
