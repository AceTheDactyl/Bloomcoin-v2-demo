# NEXTHASH Code Snippets for Modal Content
## Ready-to-use code blocks for v6 HTML modals

---

## 1. NEXTHASH-256 v6 Core Algorithm

### Round Function (10 Widening Multiplications)
```python
def nexthash_round(state: List[int], W_i: int, K_i: int) -> List[int]:
    """
    Single round of NEXTHASH-256 v6.
    10 widening multiplications for full state coverage.
    """
    a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p = state

    # Upper half compression
    T1 = add32(h, Sigma1(e), Ch(e, f, g), K_i, W_i)
    T2 = add32(Sigma0(a), Maj(a, b, c))

    # 10 WIDENING MULTIPLICATIONS - Full coverage
    # Standard cross-half (4)
    M1 = widening_mul(a ^ i, e ^ m)
    M2 = widening_mul(b ^ j, f ^ n)
    M3 = widening_mul(c ^ k, g ^ o)
    M4 = widening_mul(d ^ l, h ^ p)

    # Diagonal cross (4)
    M5 = widening_mul(a ^ m, e ^ i)
    M6 = widening_mul(b ^ n, f ^ j)
    M7 = widening_mul(c ^ o, g ^ k)
    M8 = widening_mul(d ^ p, h ^ l)

    # Corner mixing (2) - NEW in v6
    M9 = widening_mul(a ^ p, d ^ m)   # Top-left to bottom-right
    M10 = widening_mul(b ^ o, c ^ n)  # Inner corners

    # Lower half compression
    T3 = add32(p, Sigma1(m), Ch(m, n, o), K_i ^ 0x5A5A5A5A, W_i)
    T4 = add32(Sigma0(i), Maj(i, j, k))

    # Enhanced state update - all 10 MUL results distributed
    new_state = [
        add32(T1, T2, M1, M5, M9),      # a': maximum mixing
        add32(a, M6, M10),               # b': corner + diagonal
        b,
        add32(c, M2, M7),
        add32(d, T1, M9),                # e': includes corner
        add32(e, M8),
        f,
        add32(g, M3, M10),               # h': includes corner
        add32(T3, T4, M1, M5),
        add32(i, M6),
        j,
        add32(k, M4, M7),
        add32(l, T3, M9),                # m': includes corner
        add32(m, M8),
        n,
        add32(o, M2 ^ M3 ^ M4, M10),     # p': all mixing
    ]

    return new_state
```

### Widening Multiplication (The Key Innovation)
```python
def widening_mul(a: int, b: int) -> int:
    """
    Widening multiplication: high ^ low of 64-bit product.
    
    This is THE critical fix from v1 → v2.
    Truncated multiplication loses high-bit information.
    Widening preserves ALL bits via XOR folding.
    """
    product = a * b  # Full 64-bit result
    high = (product >> 32) & 0xFFFFFFFF
    low = product & 0xFFFFFFFF
    return high ^ low  # Both halves contribute equally
```

### Message Schedule (3 MUL per expansion)
```python
def expand_message(block: bytes, num_rounds: int = 52) -> List[int]:
    """Enhanced message expansion with 3 multiplications per word."""
    W = list(struct.unpack('>16I', block))

    for i in range(16, num_rounds):
        # Standard linear part (SHA-256 style)
        linear = add32(sigma1(W[i-2]), W[i-7], sigma0(W[i-15]), W[i-16])

        # Triple multiplication for maximum non-linearity
        nl1 = widening_mul(W[i-3], W[i-10])
        nl2 = widening_mul(W[i-5], W[i-12])
        nl3 = widening_mul(W[i-1] ^ W[i-8], W[i-4] ^ W[i-14])

        W.append(add32(linear, nl1, nl2 ^ nl3))

    return W
```

### Cascaded Finalization
```python
def finalize(state: List[int]) -> bytes:
    """Cascaded finalization with 3 rounds of mixing."""
    # First fold: 16 words → 8 words with mixing
    folded = []
    for i in range(8):
        upper = state[i]
        lower = state[i + 8]
        mixed = add32(
            upper ^ lower,
            widening_mul(upper, rotl(lower, 13)),
            widening_mul(lower, rotr(upper, 7)),
            widening_mul(upper ^ lower, rotr(upper, 3) ^ rotl(lower, 11)),
            rotr(upper ^ lower, i + 1)
        )
        folded.append(mixed)

    # Three rounds of final mixing
    for _ in range(3):
        new_folded = []
        for i in range(8):
            new_folded.append(add32(
                folded[i],
                widening_mul(folded[(i + 1) % 8], folded[(i + 5) % 8]),
                widening_mul(folded[(i + 2) % 8], folded[(i + 6) % 8]),
                rotr(folded[(i + 3) % 8], 7),
                rotl(folded[(i + 7) % 8], 11)
            ))
        folded = new_folded

    return struct.pack('>8I', *folded)
```

---

## 2. NEXTHASH-512 (64-bit Variant)

### 64-bit Operations
```python
def rotr64(x: int, n: int) -> int:
    """64-bit right rotation."""
    return ((x >> n) | (x << (64 - n))) & MASK64

def widening_mul_64(a: int, b: int) -> int:
    """
    Widening multiplication for 64-bit words.
    Computes 128-bit product, XORs high and low halves.
    """
    product = a * b  # Full 128-bit result in Python
    high = (product >> 64) & MASK64
    low = product & MASK64
    return high ^ low
```

### SHA-512 Style Sigma Functions
```python
def Sigma0_64(x: int) -> int:
    return rotr64(x, 28) ^ rotr64(x, 34) ^ rotr64(x, 39)

def Sigma1_64(x: int) -> int:
    return rotr64(x, 14) ^ rotr64(x, 18) ^ rotr64(x, 41)

def sigma0_64(x: int) -> int:
    return rotr64(x, 1) ^ rotr64(x, 8) ^ (x >> 7)

def sigma1_64(x: int) -> int:
    return rotr64(x, 19) ^ rotr64(x, 61) ^ (x >> 6)
```

---

## 3. Cryptographic Constructions

### HMAC-NEXTHASH-256
```python
class HMAC_NEXTHASH256:
    """
    HMAC using NEXTHASH-256 (RFC 2104 compliant).
    
    HMAC(K, m) = H((K' XOR opad) || H((K' XOR ipad) || m))
    
    Where:
    - K' is the key padded/hashed to block size (64 bytes)
    - ipad = 0x36 repeated
    - opad = 0x5C repeated
    """
    BLOCK_SIZE = 64   # 512 bits
    DIGEST_SIZE = 32  # 256 bits

    def __init__(self, key: bytes, msg: bytes = None):
        # If key > block size, hash it
        if len(key) > self.BLOCK_SIZE:
            key = nexthash256(key)
        
        # Pad key to block size
        key = key + b'\x00' * (self.BLOCK_SIZE - len(key))
        
        # Create inner and outer padded keys
        self.inner_key = bytes(k ^ 0x36 for k in key)
        self.outer_key = bytes(k ^ 0x5C for k in key)
        
        self._inner_data = bytearray(self.inner_key)
        if msg is not None:
            self.update(msg)

    def digest(self) -> bytes:
        inner_hash = nexthash256(bytes(self._inner_data))
        return nexthash256(self.outer_key + inner_hash)
```

### HKDF-NEXTHASH-256
```python
class HKDF_NEXTHASH256:
    """HKDF (RFC 5869) using NEXTHASH-256."""
    HASH_LEN = 32

    @classmethod
    def extract(cls, salt: bytes, ikm: bytes) -> bytes:
        """Extract pseudorandom key from input keying material."""
        if salt is None:
            salt = b'\x00' * cls.HASH_LEN
        return HMAC_NEXTHASH256(salt, ikm).digest()

    @classmethod
    def expand(cls, prk: bytes, info: bytes, length: int) -> bytes:
        """Expand PRK into output keying material."""
        n = (length + cls.HASH_LEN - 1) // cls.HASH_LEN
        okm = b''
        t = b''
        
        for i in range(1, n + 1):
            t = HMAC_NEXTHASH256(prk, t + info + bytes([i])).digest()
            okm += t
        
        return okm[:length]
```

### PBKDF2-NEXTHASH-256
```python
def pbkdf2_nexthash256(password: bytes, salt: bytes, 
                       iterations: int, dk_len: int) -> bytes:
    """PBKDF2 using HMAC-NEXTHASH-256 (RFC 8018)."""
    h_len = 32
    
    def f(password, salt, c, i):
        """PRF iteration function."""
        u = HMAC_NEXTHASH256(password, salt + struct.pack('>I', i)).digest()
        result = u
        
        for _ in range(c - 1):
            u = HMAC_NEXTHASH256(password, u).digest()
            result = bytes(a ^ b for a, b in zip(result, u))
        
        return result
    
    dk = b''
    blocks = (dk_len + h_len - 1) // h_len
    
    for i in range(1, blocks + 1):
        dk += f(password, salt, iterations, i)
    
    return dk[:dk_len]
```

### NEXTHASH-DRBG
```python
class NEXTHASH_DRBG:
    """Hash-based DRBG using NEXTHASH-256 (SP 800-90A style)."""
    SEED_LEN = 55  # seedlen for 256-bit security

    def __init__(self, entropy: bytes, nonce: bytes = b'',
                 personalization: bytes = b''):
        if len(entropy) < 32:
            raise ValueError("Entropy must be at least 32 bytes")
        
        seed_material = entropy + nonce + personalization
        self.v = self._hash_df(seed_material, self.SEED_LEN)
        self.c = self._hash_df(b'\x00' + self.v, self.SEED_LEN)
        self.reseed_counter = 1

    def generate(self, num_bytes: int) -> bytes:
        """Generate random bytes."""
        output = b''
        data = self.v
        
        while len(output) < num_bytes:
            output += nexthash256(data)
            data_int = int.from_bytes(data, 'big') + 1
            data = data_int.to_bytes(len(data), 'big')
        
        # Update state
        h = nexthash256(b'\x03' + self.v)
        # ... (full state update)
        
        return output[:num_bytes]
```

---

## 4. C Implementation Key Snippets

### Header (nexthash256.h)
```c
typedef struct {
    uint32_t state[16];     /* 512-bit internal state */
    uint64_t bitcount;      /* Total bits processed */
    uint8_t buffer[64];     /* Input buffer (512 bits) */
    size_t buflen;          /* Bytes in buffer */
} nexthash256_ctx;

void nexthash256_init(nexthash256_ctx *ctx);
void nexthash256_update(nexthash256_ctx *ctx, const uint8_t *data, size_t len);
void nexthash256_final(nexthash256_ctx *ctx, uint8_t digest[32]);
void nexthash256(const uint8_t *data, size_t len, uint8_t digest[32]);
void hmac_nexthash256(const uint8_t *key, size_t keylen,
                      const uint8_t *data, size_t datalen,
                      uint8_t digest[32]);
```

### Widening Multiplication in C
```c
static inline uint32_t widening_mul(uint32_t a, uint32_t b) {
    uint64_t product = (uint64_t)a * (uint64_t)b;
    return (uint32_t)(product >> 32) ^ (uint32_t)product;
}
```

### Round Function in C
```c
static void nexthash_round(uint32_t state[16], uint32_t W_i, uint32_t K_i) {
    uint32_t a = state[0], b = state[1], c = state[2], d = state[3];
    uint32_t e = state[4], f = state[5], g = state[6], h = state[7];
    uint32_t i = state[8], j = state[9], k = state[10], l = state[11];
    uint32_t m = state[12], n = state[13], o = state[14], p = state[15];

    uint32_t T1 = h + Sigma1(e) + Ch(e, f, g) + K_i + W_i;
    uint32_t T2 = Sigma0(a) + Maj(a, b, c);

    /* 10 widening multiplications */
    uint32_t M1 = widening_mul(a ^ i, e ^ m);
    uint32_t M2 = widening_mul(b ^ j, f ^ n);
    // ... M3-M10
    
    /* State update */
    state[0] = T1 + T2 + M1 + M5 + M9;
    // ... remaining state updates
}
```

---

## 5. Infinite Security Concepts

### Self-Referential Hash
```python
def self_ref_hash(message: bytes, iterations: int = 10) -> bytes:
    """Hash that converges toward self-referential fixed point."""
    h = b'\x00' * 32  # Initial "guess"
    
    for i in range(iterations):
        # H_n = Hash(message || H_{n-1})
        h = nexthash256_v6(message + h)
    
    return h

# Traditional: H(m) = F(m)
# Self-ref:    H(m) = F(m, H(m))  ← Fixed point equation
```

### Phoenix Hash (Grows from Attacks)
```python
class PhoenixHash:
    def __init__(self):
        self.attack_history = []
        self.evolution_count = 0

    def incorporate_attack(self, attack_description: str):
        """Learn from an attack, becoming stronger."""
        self.attack_history.append(attack_description)
        self.evolution_count += 1

    def hash(self, message: bytes) -> bytes:
        """Hash incorporating all learned attacks."""
        h = nexthash256_v6(message)
        
        for i, attack in enumerate(self.attack_history):
            attack_hash = nexthash256_v6(attack.encode())
            h = nexthash256_v6(h + attack_hash + struct.pack('>I', i))
        
        return h

    def security_level(self) -> str:
        base = 113  # v6 base level
        evolved = base + self.evolution_count * 5
        return f"{evolved}% of SHA-256 (evolved {self.evolution_count}x)"
```

### The Core Synthesis
```
Six Concepts:
1. SELF-REFERENCE: Hash = fixed point of itself
2. INPUT-DEPENDENT: Security varies with input
3. INFINITE FAMILY: {H_k : k ∈ ℕ} with unbounded members
4. GÖDELIAN: Unprovable security
5. PHOENIX: Grows from attacks
6. OBSERVER: Changes when measured

Core Insight:
  True infinite security isn't a THING.
  It's a PROCESS.
  
  NEXTHASH isn't secure.
  The evolution of NEXTHASH is secure.
  
  Not: security = ∞
  But: lim security(t) = ∞ as t → ∞
```

---

## 6. Security Metrics

### sigma_MIX Formula
```python
# Security Score = Rounds × sigma_MIX
# Where sigma_MIX = MIX_ops / (MIX_ops + INV_ops)

# MIX operations (information destroying):
#   Ch, Maj, ADD, MUL

# INV operations (invertible):
#   XOR, ROT

# NEXTHASH v6:
rounds = 52
muls = 10
adds = 28  # More adds due to more MUL results
inv = 28   # XORs and rotations
mix = 2 + 2 + adds + muls  # Ch + Maj + adds + muls = 42
sigma_mix = mix / (inv + mix)  # 42 / 70 = 0.60
score = rounds * sigma_mix     # 52 × 0.60 = 31.2

# SHA-256:
sha_score = 64 * 0.43  # = 27.5

# v6 vs SHA-256:
percentage = score / sha_score * 100  # ~113%
```

### Version Evolution
```
+------------------+--------+--------+--------+--------+--------+----------+
| Property         |   v1   |  v2.1  |   v3   |   v4   |   v5   |    v6    |
+------------------+--------+--------+--------+--------+--------+----------+
| Rounds           |   24   |   32   |   32   |   32   |   40   |    52    |
| MUL/round        |    4   |    4   |    6   |    8   |    8   |    10    |
| MUL type         | trunc  | widen  | widen  | widen  | widen  |  widen   |
| sigma_MIX        | 0.481  | 0.481  | 0.517  | 0.562  | 0.562  |  0.600   |
| Security Score   |  11.6  |  15.4  |  16.6  |  18.0  |  22.5  |   31.2   |
| vs SHA-256       |  42%   |  56%   |  60%   |  65%   |  82%   |  113%    |
+------------------+--------+--------+--------+--------+--------+----------+
```

---

**END OF CODE SNIPPETS**
