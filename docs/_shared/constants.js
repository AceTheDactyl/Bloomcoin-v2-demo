// BloomCoin phi-derived Constants Module
// All values derive algebraically from phi = (1+sqrt(5))/2

const PHI = (1 + Math.sqrt(5)) / 2;          // 1.618033988749895
const TAU = 1 / PHI;                          // 0.6180339887498949
const PHI_2 = PHI * PHI;                      // 2.618033988749895
const PHI_3 = PHI_2 * PHI;                    // 4.23606797749979
const PHI_4 = PHI_2 * PHI_2;                  // 6.854101966249685
const PHI_NEG1 = TAU;                         // 0.6180339887498949
const PHI_NEG2 = TAU * TAU;                   // 0.3819660112501051
const PHI_NEG4 = 1 / PHI_4;                   // 0.1458980337503154
const K = Math.sqrt(1 - PHI_NEG4);            // 0.9241596774498886 (Kuramoto coupling)
const Z_C = Math.sqrt(3) / 2;                 // 0.8660254037844386 (THE LENS)
const L4 = 7;                                  // Lucas(4) = phi^4 + phi^-4
const N_OSCILLATORS = L4 * 9;                 // 63

// Golden angles (degrees)
const GOLDEN_ANGLE_DEG = 360 / (PHI * PHI);   // 137.5077640...
const DYAD_ANGLE = 36;                        // Pentagonal dyad angle

// Verification assertions
console.assert(Math.abs(PHI * PHI - PHI - 1) < 1e-10, "phi^2 = phi + 1");
console.assert(Math.abs(PHI + TAU - PHI * TAU - 1) < 1e-10, "phi + tau = phi*tau + 1");
console.assert(L4 === Math.round(PHI_4 + PHI_NEG4), "L4 = phi^4 + phi^-4");
console.assert(Math.abs(PHI * TAU - 1) < 1e-10, "phi * tau = 1");

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        PHI, TAU, PHI_2, PHI_3, PHI_4,
        PHI_NEG1, PHI_NEG2, PHI_NEG4,
        K, Z_C, L4, N_OSCILLATORS,
        GOLDEN_ANGLE_DEG, DYAD_ANGLE
    };
}
