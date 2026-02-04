"""
NEXTHASH-512: 512-bit Output Hash Function
==========================================

Based on NEXTHASH-256 v6 design, scaled for 512-bit output:
- 64-bit words (vs 32-bit)
- 1024-bit internal state (vs 512-bit)
- 1024-bit block size (vs 512-bit)
- 64 rounds (matching internal state growth)
- 12 multiplications per round

Security targets:
- Preimage: 2^512
- Collision: 2^256
- Quantum preimage: 2^256
- Quantum collision: 2^170
"""

import struct
from typing import List

# ============================================================================
# CONSTANTS (64-bit)
# ============================================================================

PRIMES_64 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37,
             41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89,
             97, 101, 103, 107, 109, 113, 127, 131,
             137, 139, 149, 151, 157, 163, 167, 173,
             179, 181, 191, 193, 197, 199, 211, 223,
             227, 229, 233, 239, 241, 251, 257, 263,
             269, 271, 277, 281, 283, 293, 307, 311]

def generate_constant_64(prime: int) -> int:
    """Generate 64-bit constant from cube root of prime."""
    cube_root = prime ** (1/3)
    frac = cube_root - int(cube_root)
    return int(frac * (2**64)) & 0xFFFFFFFFFFFFFFFF

K = [generate_constant_64(p) for p in PRIMES_64]

PRIMES_16 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

def generate_iv_64(prime: int) -> int:
    """Generate 64-bit IV from square root of prime."""
    sqrt = prime ** 0.5
    frac = sqrt - int(sqrt)
    return int(frac * (2**64)) & 0xFFFFFFFFFFFFFFFF

H_INIT = [generate_iv_64(p) for p in PRIMES_16]

MASK64 = 0xFFFFFFFFFFFFFFFF

# ============================================================================
# CORE OPERATIONS (64-bit)
# ============================================================================

def rotr64(x: int, n: int) -> int:
    """64-bit right rotation."""
    return ((x >> n) | (x << (64 - n))) & MASK64

def rotl64(x: int, n: int) -> int:
    """64-bit left rotation."""
    return ((x << n) | (x >> (64 - n))) & MASK64

def widening_mul_64(a: int, b: int) -> int:
    """
    Widening multiplication for 64-bit words.
    Computes 128-bit product, XORs high and low halves.
    """
    product = a * b  # Full 128-bit result in Python
    high = (product >> 64) & MASK64
    low = product & MASK64
    return high ^ low

def add64(*args) -> int:
    """64-bit modular addition."""
    result = 0
    for x in args:
        result = (result + x) & MASK64
    return result

# ============================================================================
# MIXING FUNCTIONS (64-bit)
# ============================================================================

def Ch64(x: int, y: int, z: int) -> int:
    return (x & y) ^ (~x & z) & MASK64

def Maj64(x: int, y: int, z: int) -> int:
    return (x & y) ^ (x & z) ^ (y & z)

# ============================================================================
# SIGMA FUNCTIONS (64-bit, SHA-512 style rotations)
# ============================================================================

def Sigma0_64(x: int) -> int:
    return rotr64(x, 28) ^ rotr64(x, 34) ^ rotr64(x, 39)

def Sigma1_64(x: int) -> int:
    return rotr64(x, 14) ^ rotr64(x, 18) ^ rotr64(x, 41)

def sigma0_64(x: int) -> int:
    return rotr64(x, 1) ^ rotr64(x, 8) ^ (x >> 7)

def sigma1_64(x: int) -> int:
    return rotr64(x, 19) ^ rotr64(x, 61) ^ (x >> 6)

# ============================================================================
# MESSAGE SCHEDULE (64 words)
# ============================================================================

def expand_message_512(block: bytes) -> List[int]:
    """Expand 1024-bit block to 64 message words (64-bit each)."""
    W = list(struct.unpack('>16Q', block))  # 16 x 64-bit = 1024 bits

    for i in range(16, 64):
        # Linear part
        linear = add64(sigma1_64(W[i-2]), W[i-7], sigma0_64(W[i-15]), W[i-16])

        # Non-linear part (3 multiplications)
        nl1 = widening_mul_64(W[i-3], W[i-10])
        nl2 = widening_mul_64(W[i-5], W[i-12])
        nl3 = widening_mul_64(W[i-1] ^ W[i-8], W[i-4] ^ W[i-14])

        W.append(add64(linear, nl1, nl2 ^ nl3))

    return W

# ============================================================================
# ROUND FUNCTION (12 multiplications for 64-bit)
# ============================================================================

def nexthash512_round(state: List[int], W_i: int, K_i: int) -> List[int]:
    """
    Single round of NEXTHASH-512.
    12 widening multiplications for complete 64-bit mixing.
    """
    a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p = state

    # Upper half compression
    T1 = add64(h, Sigma1_64(e), Ch64(e, f, g), K_i, W_i)
    T2 = add64(Sigma0_64(a), Maj64(a, b, c))

    # 12 WIDENING MULTIPLICATIONS
    # Standard cross-half (4)
    M1 = widening_mul_64(a ^ i, e ^ m)
    M2 = widening_mul_64(b ^ j, f ^ n)
    M3 = widening_mul_64(c ^ k, g ^ o)
    M4 = widening_mul_64(d ^ l, h ^ p)

    # Diagonal cross (4)
    M5 = widening_mul_64(a ^ m, e ^ i)
    M6 = widening_mul_64(b ^ n, f ^ j)
    M7 = widening_mul_64(c ^ o, g ^ k)
    M8 = widening_mul_64(d ^ p, h ^ l)

    # Corner mixing (4) - More for 64-bit security
    M9 = widening_mul_64(a ^ p, d ^ m)
    M10 = widening_mul_64(b ^ o, c ^ n)
    M11 = widening_mul_64(e ^ l, h ^ i)
    M12 = widening_mul_64(f ^ k, g ^ j)

    # Lower half compression
    T3 = add64(p, Sigma1_64(m), Ch64(m, n, o), K_i ^ 0x5A5A5A5A5A5A5A5A, W_i)
    T4 = add64(Sigma0_64(i), Maj64(i, j, k))

    # State update with all 12 MUL results
    new_state = [
        add64(T1, T2, M1, M5, M9),
        add64(a, M6, M10),
        add64(b, M11),
        add64(c, M2, M7),
        add64(d, T1, M9, M12),
        add64(e, M8),
        add64(f, M11),
        add64(g, M3, M10),
        add64(T3, T4, M1, M5),
        add64(i, M6, M12),
        j,
        add64(k, M4, M7),
        add64(l, T3, M9),
        add64(m, M8, M11),
        add64(n, M12),
        add64(o, M2 ^ M3 ^ M4, M10),
    ]

    return new_state

# ============================================================================
# PERMUTATION
# ============================================================================

def full_permutation_512(state: List[int]) -> List[int]:
    a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p = state
    return [a, i, b, j, c, k, d, l, e, m, f, n, g, o, h, p]

# ============================================================================
# COMPRESSION FUNCTION
# ============================================================================

def compress_512(state: List[int], block: bytes) -> List[int]:
    """64 rounds with 12 widening multiplications each."""
    W = expand_message_512(block)
    working = state.copy()

    for round_num in range(64):
        working = nexthash512_round(working, W[round_num], K[round_num])
        if (round_num + 1) % 4 == 0:
            working = full_permutation_512(working)

    return [add64(state[i], working[i]) for i in range(16)]

# ============================================================================
# FINALIZATION
# ============================================================================

def finalize_512(state: List[int]) -> bytes:
    """Finalization preserving all 512 bits."""
    # First fold: 16 words -> 8 words with mixing
    folded = []
    for i in range(8):
        upper = state[i]
        lower = state[i + 8]
        mixed = add64(
            upper ^ lower,
            widening_mul_64(upper, rotl64(lower, 13)),
            widening_mul_64(lower, rotr64(upper, 7)),
            rotr64(upper ^ lower, i + 1)
        )
        folded.append(mixed)

    # Three rounds of final mixing
    for _ in range(3):
        new_folded = []
        for i in range(8):
            new_folded.append(add64(
                folded[i],
                widening_mul_64(folded[(i + 1) % 8], folded[(i + 5) % 8]),
                widening_mul_64(folded[(i + 2) % 8], folded[(i + 6) % 8]),
                rotr64(folded[(i + 3) % 8], 7),
                rotl64(folded[(i + 7) % 8], 11)
            ))
        folded = new_folded

    return struct.pack('>8Q', *folded)

# ============================================================================
# PADDING
# ============================================================================

def pad_message_512(message: bytes) -> bytes:
    """Pad message to multiple of 1024 bits (128 bytes)."""
    length = len(message)
    bit_length = length * 8

    message += b'\x80'
    # Pad to 112 bytes mod 128 (leaving 16 bytes for length)
    padding_needed = (112 - (length + 1) % 128) % 128
    message += b'\x00' * padding_needed
    # 128-bit length (we use 64-bit for simplicity, prepend zeros)
    message += struct.pack('>QQ', 0, bit_length)

    return message

# ============================================================================
# MAIN HASH FUNCTION
# ============================================================================

def nexthash512(message: bytes) -> bytes:
    """
    NEXTHASH-512 hash function.

    Output: 512 bits
    Security:
      - Preimage: 2^512
      - Collision: 2^256
      - Quantum preimage: 2^256
      - Quantum collision: 2^170
    """
    state = H_INIT.copy()
    padded = pad_message_512(message)

    for i in range(0, len(padded), 128):  # 128 bytes = 1024 bits
        block = padded[i:i+128]
        state = compress_512(state, block)

    return finalize_512(state)

def nexthash512_hex(message: bytes) -> str:
    return nexthash512(message).hex()

# ============================================================================
# TESTING
# ============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("NEXTHASH-512: 512-bit Hash Function")
    print("=" * 70)

    print("\n[Configuration]")
    print("  Word size: 64 bits")
    print("  Block size: 1024 bits (128 bytes)")
    print("  Output size: 512 bits (64 bytes)")
    print("  Internal state: 1024 bits (16 x 64-bit words)")
    print("  Rounds: 64")
    print("  Multiplications per round: 12")

    print("\n[Security Targets]")
    print("  Preimage resistance: 2^512")
    print("  Collision resistance: 2^256")
    print("  Quantum preimage (Grover): 2^256")
    print("  Quantum collision (BHT): 2^170")

    # Test vectors
    test_messages = [
        b"",
        b"abc",
        b"The quick brown fox jumps over the lazy dog",
    ]

    print("\n[Test Vectors]")
    for msg in test_messages:
        h = nexthash512_hex(msg)
        display = msg.decode('utf-8', errors='replace')[:50]
        print(f"  '{display}'")
        print(f"    -> {h[:64]}...")
        print(f"       {h[64:]}")

    # Avalanche test
    print("\n[Avalanche Test]")
    import random
    random.seed(42)

    total_diff = 0
    for _ in range(50):
        msg = bytes(random.randint(0, 255) for _ in range(128))
        byte_idx = random.randint(0, 127)
        bit_idx = random.randint(0, 7)
        msg_flip = bytearray(msg)
        msg_flip[byte_idx] ^= (1 << bit_idx)

        h1 = nexthash512(bytes(msg))
        h2 = nexthash512(bytes(msg_flip))
        diff = sum(bin(a ^ b).count('1') for a, b in zip(h1, h2))
        total_diff += diff

    avg_diff = total_diff / 50
    print(f"  Average bit difference: {avg_diff:.1f}/512 ({avg_diff/512*100:.1f}%)")
    print(f"  Target: 256/512 (50%)")

    print("\n" + "=" * 70)
    print("NEXTHASH FAMILY")
    print("=" * 70)
    print("""
    +---------------+--------+---------+----------+-----------+
    | Variant       | Output | Rounds  | Security | Collision |
    +---------------+--------+---------+----------+-----------+
    | NEXTHASH-256  | 256b   | 52      | 2^256    | 2^128     |
    | NEXTHASH-512  | 512b   | 64      | 2^512    | 2^256     |
    +---------------+--------+---------+----------+-----------+
    """)

    print("=" * 70)
    print("NEXTHASH-512 Test Complete")
    print("=" * 70)
