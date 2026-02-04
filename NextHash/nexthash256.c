/*
 * NEXTHASH-256 v6 Reference Implementation
 * =========================================
 *
 * Compile: gcc -O3 -o nexthash256 nexthash256.c -DTEST_MAIN
 */

#include "nexthash256.h"
#include <string.h>

/* ========================================================================== */
/* Constants                                                                   */
/* ========================================================================== */

/* Round constants: Fractional parts of cube roots of first 52 primes */
static const uint32_t K[52] = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5
};

/* Initial state: Fractional parts of square roots of first 16 primes */
static const uint32_t H_INIT[16] = {
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
    0xcbbb9d5d, 0x629a292a, 0x9159015a, 0x152fecd8,
    0x67332667, 0x8eb44a87, 0xdb0c2e0d, 0x47b5481d
};

/* ========================================================================== */
/* Helper Functions                                                            */
/* ========================================================================== */

/* Right rotation */
static inline uint32_t rotr(uint32_t x, int n) {
    return (x >> n) | (x << (32 - n));
}

/* Left rotation */
static inline uint32_t rotl(uint32_t x, int n) {
    return (x << n) | (x >> (32 - n));
}

/* Widening multiplication: high ^ low of 64-bit product */
static inline uint32_t widening_mul(uint32_t a, uint32_t b) {
    uint64_t product = (uint64_t)a * (uint64_t)b;
    return (uint32_t)(product >> 32) ^ (uint32_t)product;
}

/* Boolean functions */
static inline uint32_t Ch(uint32_t x, uint32_t y, uint32_t z) {
    return (x & y) ^ (~x & z);
}

static inline uint32_t Maj(uint32_t x, uint32_t y, uint32_t z) {
    return (x & y) ^ (x & z) ^ (y & z);
}

/* Sigma functions */
static inline uint32_t Sigma0(uint32_t x) {
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22);
}

static inline uint32_t Sigma1(uint32_t x) {
    return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25);
}

static inline uint32_t sigma0(uint32_t x) {
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3);
}

static inline uint32_t sigma1(uint32_t x) {
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10);
}

/* ========================================================================== */
/* Message Schedule                                                            */
/* ========================================================================== */

static void expand_message(const uint8_t block[64], uint32_t W[52]) {
    int i;

    /* Parse block into 16 32-bit words (big-endian) */
    for (i = 0; i < 16; i++) {
        W[i] = ((uint32_t)block[i*4] << 24) |
               ((uint32_t)block[i*4 + 1] << 16) |
               ((uint32_t)block[i*4 + 2] << 8) |
               ((uint32_t)block[i*4 + 3]);
    }

    /* Expand to 52 words */
    for (i = 16; i < 52; i++) {
        uint32_t linear = sigma1(W[i-2]) + W[i-7] + sigma0(W[i-15]) + W[i-16];
        uint32_t nl1 = widening_mul(W[i-3], W[i-10]);
        uint32_t nl2 = widening_mul(W[i-5], W[i-12]);
        uint32_t nl3 = widening_mul(W[i-1] ^ W[i-8], W[i-4] ^ W[(i-14 < 0 ? i-14+52 : i-14)]);
        W[i] = linear + nl1 + (nl2 ^ nl3);
    }
}

/* ========================================================================== */
/* Round Function                                                              */
/* ========================================================================== */

static void nexthash_round(uint32_t state[16], uint32_t W_i, uint32_t K_i) {
    uint32_t a = state[0], b = state[1], c = state[2], d = state[3];
    uint32_t e = state[4], f = state[5], g = state[6], h = state[7];
    uint32_t i = state[8], j = state[9], k = state[10], l = state[11];
    uint32_t m = state[12], n = state[13], o = state[14], p = state[15];

    /* Upper half compression */
    uint32_t T1 = h + Sigma1(e) + Ch(e, f, g) + K_i + W_i;
    uint32_t T2 = Sigma0(a) + Maj(a, b, c);

    /* 10 widening multiplications */
    uint32_t M1 = widening_mul(a ^ i, e ^ m);
    uint32_t M2 = widening_mul(b ^ j, f ^ n);
    uint32_t M3 = widening_mul(c ^ k, g ^ o);
    uint32_t M4 = widening_mul(d ^ l, h ^ p);
    uint32_t M5 = widening_mul(a ^ m, e ^ i);
    uint32_t M6 = widening_mul(b ^ n, f ^ j);
    uint32_t M7 = widening_mul(c ^ o, g ^ k);
    uint32_t M8 = widening_mul(d ^ p, h ^ l);
    uint32_t M9 = widening_mul(a ^ p, d ^ m);
    uint32_t M10 = widening_mul(b ^ o, c ^ n);

    /* Lower half compression */
    uint32_t T3 = p + Sigma1(m) + Ch(m, n, o) + (K_i ^ 0x5A5A5A5A) + W_i;
    uint32_t T4 = Sigma0(i) + Maj(i, j, k);

    /* State update */
    state[0] = T1 + T2 + M1 + M5 + M9;
    state[1] = a + M6 + M10;
    state[2] = b;
    state[3] = c + M2 + M7;
    state[4] = d + T1 + M9;
    state[5] = e + M8;
    state[6] = f;
    state[7] = g + M3 + M10;
    state[8] = T3 + T4 + M1 + M5;
    state[9] = i + M6;
    state[10] = j;
    state[11] = k + M4 + M7;
    state[12] = l + T3 + M9;
    state[13] = m + M8;
    state[14] = n;
    state[15] = o + (M2 ^ M3 ^ M4) + M10;
}

/* ========================================================================== */
/* Permutation                                                                 */
/* ========================================================================== */

static void full_permutation(uint32_t state[16]) {
    uint32_t temp[16];
    temp[0] = state[0];  temp[1] = state[8];
    temp[2] = state[1];  temp[3] = state[9];
    temp[4] = state[2];  temp[5] = state[10];
    temp[6] = state[3];  temp[7] = state[11];
    temp[8] = state[4];  temp[9] = state[12];
    temp[10] = state[5]; temp[11] = state[13];
    temp[12] = state[6]; temp[13] = state[14];
    temp[14] = state[7]; temp[15] = state[15];
    memcpy(state, temp, 64);
}

/* ========================================================================== */
/* Compression Function                                                        */
/* ========================================================================== */

static void compress(uint32_t state[16], const uint8_t block[64]) {
    uint32_t W[52];
    uint32_t working[16];
    int round_num;

    expand_message(block, W);
    memcpy(working, state, 64);

    for (round_num = 0; round_num < 52; round_num++) {
        nexthash_round(working, W[round_num], K[round_num]);
        if ((round_num + 1) % 4 == 0) {
            full_permutation(working);
        }
    }

    /* Add working state to original state */
    for (int i = 0; i < 16; i++) {
        state[i] += working[i];
    }
}

/* ========================================================================== */
/* Finalization                                                                */
/* ========================================================================== */

static void finalize_hash(uint32_t state[16], uint8_t digest[32]) {
    uint32_t folded[8];
    int i, round;

    /* First fold: 16 words -> 8 words */
    for (i = 0; i < 8; i++) {
        uint32_t upper = state[i];
        uint32_t lower = state[i + 8];
        folded[i] = (upper ^ lower) +
                    widening_mul(upper, rotl(lower, 13)) +
                    widening_mul(lower, rotr(upper, 7)) +
                    widening_mul(upper ^ lower, rotr(upper, 3) ^ rotl(lower, 11)) +
                    rotr(upper ^ lower, i + 1);
    }

    /* Three rounds of final mixing */
    for (round = 0; round < 3; round++) {
        uint32_t new_folded[8];
        for (i = 0; i < 8; i++) {
            new_folded[i] = folded[i] +
                           widening_mul(folded[(i + 1) % 8], folded[(i + 5) % 8]) +
                           widening_mul(folded[(i + 2) % 8], folded[(i + 6) % 8]) +
                           rotr(folded[(i + 3) % 8], 7) +
                           rotl(folded[(i + 7) % 8], 11);
        }
        memcpy(folded, new_folded, 32);
    }

    /* Output digest (big-endian) */
    for (i = 0; i < 8; i++) {
        digest[i*4] = (uint8_t)(folded[i] >> 24);
        digest[i*4 + 1] = (uint8_t)(folded[i] >> 16);
        digest[i*4 + 2] = (uint8_t)(folded[i] >> 8);
        digest[i*4 + 3] = (uint8_t)folded[i];
    }
}

/* ========================================================================== */
/* Public API                                                                  */
/* ========================================================================== */

void nexthash256_init(nexthash256_ctx *ctx) {
    memcpy(ctx->state, H_INIT, 64);
    ctx->bitcount = 0;
    ctx->buflen = 0;
}

void nexthash256_update(nexthash256_ctx *ctx, const uint8_t *data, size_t len) {
    size_t i;

    ctx->bitcount += len * 8;

    /* Process any buffered data */
    if (ctx->buflen > 0) {
        size_t need = 64 - ctx->buflen;
        if (len < need) {
            memcpy(ctx->buffer + ctx->buflen, data, len);
            ctx->buflen += len;
            return;
        }
        memcpy(ctx->buffer + ctx->buflen, data, need);
        compress(ctx->state, ctx->buffer);
        data += need;
        len -= need;
        ctx->buflen = 0;
    }

    /* Process complete blocks */
    while (len >= 64) {
        compress(ctx->state, data);
        data += 64;
        len -= 64;
    }

    /* Buffer remaining data */
    if (len > 0) {
        memcpy(ctx->buffer, data, len);
        ctx->buflen = len;
    }
}

void nexthash256_final(nexthash256_ctx *ctx, uint8_t digest[32]) {
    uint8_t pad[128];
    size_t padlen;

    /* Pad to 56 bytes mod 64 */
    padlen = (ctx->buflen < 56) ? (56 - ctx->buflen) : (120 - ctx->buflen);

    pad[0] = 0x80;
    memset(pad + 1, 0, padlen - 1);

    /* Append 64-bit length (big-endian) */
    pad[padlen] = (uint8_t)(ctx->bitcount >> 56);
    pad[padlen + 1] = (uint8_t)(ctx->bitcount >> 48);
    pad[padlen + 2] = (uint8_t)(ctx->bitcount >> 40);
    pad[padlen + 3] = (uint8_t)(ctx->bitcount >> 32);
    pad[padlen + 4] = (uint8_t)(ctx->bitcount >> 24);
    pad[padlen + 5] = (uint8_t)(ctx->bitcount >> 16);
    pad[padlen + 6] = (uint8_t)(ctx->bitcount >> 8);
    pad[padlen + 7] = (uint8_t)ctx->bitcount;

    nexthash256_update(ctx, pad, padlen + 8);

    finalize_hash(ctx->state, digest);

    /* Clear sensitive data */
    memset(ctx, 0, sizeof(*ctx));
}

void nexthash256(const uint8_t *data, size_t len, uint8_t digest[32]) {
    nexthash256_ctx ctx;
    nexthash256_init(&ctx);
    nexthash256_update(&ctx, data, len);
    nexthash256_final(&ctx, digest);
}

/* ========================================================================== */
/* HMAC-NEXTHASH-256                                                           */
/* ========================================================================== */

void hmac_nexthash256(const uint8_t *key, size_t keylen,
                      const uint8_t *data, size_t datalen,
                      uint8_t digest[32]) {
    uint8_t k_ipad[64], k_opad[64];
    uint8_t temp_key[32];
    nexthash256_ctx ctx;
    size_t i;

    /* If key > 64 bytes, hash it */
    if (keylen > 64) {
        nexthash256(key, keylen, temp_key);
        key = temp_key;
        keylen = 32;
    }

    /* Prepare inner and outer keys */
    memset(k_ipad, 0x36, 64);
    memset(k_opad, 0x5C, 64);
    for (i = 0; i < keylen; i++) {
        k_ipad[i] ^= key[i];
        k_opad[i] ^= key[i];
    }

    /* Inner hash: H(k_ipad || data) */
    nexthash256_init(&ctx);
    nexthash256_update(&ctx, k_ipad, 64);
    nexthash256_update(&ctx, data, datalen);
    nexthash256_final(&ctx, digest);

    /* Outer hash: H(k_opad || inner_hash) */
    nexthash256_init(&ctx);
    nexthash256_update(&ctx, k_opad, 64);
    nexthash256_update(&ctx, digest, 32);
    nexthash256_final(&ctx, digest);
}

/* ========================================================================== */
/* Test Main                                                                   */
/* ========================================================================== */

#ifdef TEST_MAIN

#include <stdio.h>

static void print_hex(const uint8_t *data, size_t len) {
    for (size_t i = 0; i < len; i++) {
        printf("%02x", data[i]);
    }
    printf("\n");
}

int main(void) {
    uint8_t digest[32];

    printf("NEXTHASH-256 v6 C Implementation\n");
    printf("================================\n\n");

    /* Test vectors */
    printf("Test Vectors:\n");

    nexthash256((uint8_t*)"", 0, digest);
    printf("  \"\" -> ");
    print_hex(digest, 32);

    nexthash256((uint8_t*)"abc", 3, digest);
    printf("  \"abc\" -> ");
    print_hex(digest, 32);

    const char *fox = "The quick brown fox jumps over the lazy dog";
    nexthash256((uint8_t*)fox, strlen(fox), digest);
    printf("  \"The quick brown fox...\" -> ");
    print_hex(digest, 32);

    /* HMAC test */
    printf("\nHMAC-NEXTHASH-256:\n");
    hmac_nexthash256((uint8_t*)"key", 3, (uint8_t*)"message", 7, digest);
    printf("  HMAC(\"key\", \"message\") -> ");
    print_hex(digest, 32);

    printf("\nC implementation complete.\n");
    return 0;
}

#endif /* TEST_MAIN */
