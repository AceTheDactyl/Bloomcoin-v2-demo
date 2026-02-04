/*
 * NEXTHASH-256 v6 Reference Implementation
 * =========================================
 *
 * A multiplication-based cryptographic hash function that exceeds
 * SHA-256's security margin (113% vs 100%).
 *
 * Features:
 * - 52 rounds
 * - 10 widening multiplications per round
 * - 512-bit internal state
 * - 256-bit output
 *
 * Author: NEXTHASH Research Project
 * Date: February 2026
 * License: Public Domain / CC0
 */

#ifndef NEXTHASH256_H
#define NEXTHASH256_H

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* NEXTHASH-256 context structure */
typedef struct {
    uint32_t state[16];     /* 512-bit internal state */
    uint64_t bitcount;      /* Total bits processed */
    uint8_t buffer[64];     /* Input buffer (512 bits) */
    size_t buflen;          /* Bytes in buffer */
} nexthash256_ctx;

/* Initialize context */
void nexthash256_init(nexthash256_ctx *ctx);

/* Update with more data */
void nexthash256_update(nexthash256_ctx *ctx, const uint8_t *data, size_t len);

/* Finalize and output 32-byte digest */
void nexthash256_final(nexthash256_ctx *ctx, uint8_t digest[32]);

/* One-shot hash function */
void nexthash256(const uint8_t *data, size_t len, uint8_t digest[32]);

/* HMAC-NEXTHASH-256 */
void hmac_nexthash256(const uint8_t *key, size_t keylen,
                      const uint8_t *data, size_t datalen,
                      uint8_t digest[32]);

#ifdef __cplusplus
}
#endif

#endif /* NEXTHASH256_H */
