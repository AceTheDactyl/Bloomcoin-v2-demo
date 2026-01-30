"""
Lucas Matrix Operations for BloomCoin
======================================

This module implements the fundamental 2x2 Fibonacci matrix and its powers,
which form the algebraic foundation for BloomCoin's nonce generation.

Mathematical Foundation:
    The matrix R = [[0, 1], [1, 1]] has the property:

    R^n = [[F_{n-1}, F_n    ],
           [F_n,     F_{n+1}]]

    where F_n is the nth Fibonacci number.

    Key Identity (Lucas Trace Formula):
        tr(R^n) = F_{n-1} + F_{n+1} = L_n

    This connects the matrix to Lucas numbers, which are used for:
    - Nonce generation (deterministic but algebraically structured)
    - Block timing (Lucas-scheduled intervals)
    - Difficulty adjustment

Cross-References:
    - constants.py: PHI, lucas(), fibonacci(), LUCAS_SEQUENCE
    - SINGULARITY_ENGINE.py: R(z) = 1/(1+z) recursion
    - self_reference_framework_complete.py: Level 3 Structure (sl(2,R))
    - resonance_formalism.md: Lucas number mass formulas

Author: BloomCoin Framework
"""

from typing import Tuple, Optional
import numpy as np

from ..constants import PHI, TAU, L4, lucas as lucas_binet, fibonacci as fibonacci_binet


# =============================================================================
# FUNDAMENTAL MATRIX
# =============================================================================

# The Fibonacci matrix R
# R^n produces Fibonacci numbers in its entries
# tr(R^n) = L_n (Lucas numbers)
R_MATRIX = np.array([[0, 1], [1, 1]], dtype=np.uint64)

# Identity matrix for exponentiation base case
I_MATRIX = np.array([[1, 0], [0, 1]], dtype=np.uint64)


# =============================================================================
# MATRIX OPERATIONS
# =============================================================================

def matrix_multiply_mod(A: np.ndarray, B: np.ndarray, mod: int) -> np.ndarray:
    """
    Multiply two 2x2 matrices modulo m.

    Args:
        A: 2x2 numpy array (uint64)
        B: 2x2 numpy array (uint64)
        mod: Modulus for all operations

    Returns:
        A @ B mod m as 2x2 numpy array

    Note:
        Uses Python integers internally to avoid uint64 overflow,
        then converts back to numpy array.
    """
    # Extract as Python ints to avoid overflow
    a00, a01 = int(A[0, 0]), int(A[0, 1])
    a10, a11 = int(A[1, 0]), int(A[1, 1])
    b00, b01 = int(B[0, 0]), int(B[0, 1])
    b10, b11 = int(B[1, 0]), int(B[1, 1])

    # Compute product elements with mod
    c00 = (a00 * b00 + a01 * b10) % mod
    c01 = (a00 * b01 + a01 * b11) % mod
    c10 = (a10 * b00 + a11 * b10) % mod
    c11 = (a10 * b01 + a11 * b11) % mod

    return np.array([[c00, c01], [c10, c11]], dtype=np.uint64)


def matrix_power_mod(base: np.ndarray, exp: int, mod: int) -> np.ndarray:
    """
    Compute base^exp mod m using binary exponentiation.

    This is the CORE ALGORITHM for efficient Lucas/Fibonacci computation.
    Complexity: O(log(exp)) matrix multiplications.

    Args:
        base: 2x2 numpy array
        exp: Non-negative integer exponent
        mod: Modulus for all operations

    Returns:
        base^exp mod m as 2x2 numpy array

    Example:
        R = np.array([[0, 1], [1, 1]], dtype=np.uint64)
        R_10 = matrix_power_mod(R, 10, 2**64)
        # R_10[0,1] = F_10 = 55
        # tr(R_10) = L_10 = 123

    Connection to Framework:
        This implements the "iterate" operation from ComputationalGround
        in self_reference_framework_complete.py.
    """
    if exp < 0:
        raise ValueError("Exponent must be non-negative")

    if mod <= 0:
        raise ValueError("Modulus must be positive")

    # Base case: M^0 = I
    if exp == 0:
        return I_MATRIX.copy()

    # Binary exponentiation
    result = I_MATRIX.copy()
    current = base.copy()

    while exp > 0:
        if exp & 1:  # exp is odd
            result = matrix_multiply_mod(result, current, mod)
        current = matrix_multiply_mod(current, current, mod)
        exp >>= 1

    return result


# =============================================================================
# LUCAS AND FIBONACCI VIA MATRIX
# =============================================================================

def lucas_trace(n: int, mod: int = 2**32) -> int:
    """
    Compute L_n mod m via matrix trace.

    This is the CORE PRIMITIVE for nonce generation in BloomCoin.
    Uses the identity: tr(R^n) = L_n

    Args:
        n: Lucas index (non-negative)
        mod: Modulus (default 2^32 for 32-bit nonces)

    Returns:
        L_n mod m

    Mathematical Identity:
        tr(R^n) = R^n[0,0] + R^n[1,1] = F_{n-1} + F_{n+1} = L_n

    Performance:
        O(log n) time complexity via binary exponentiation.

    Example:
        lucas_trace(4) == 7   # L_4 = 7 (the normalization integer!)
        lucas_trace(10) == 123
        lucas_trace(17) == 3571

    Connection to Framework:
        L_n appears throughout the framework:
        - L_4 = 7: Minimum bloom rounds, block time in minutes
        - L_10 = 123: Difficulty adjustment interval
        - L_17 = 3571: Tau mass formula component
    """
    if n < 0:
        raise ValueError("Lucas index must be non-negative")

    if n == 0:
        return 2 % mod  # L_0 = 2
    if n == 1:
        return 1 % mod  # L_1 = 1

    R_n = matrix_power_mod(R_MATRIX, n, mod)

    # tr(R^n) = R^n[0,0] + R^n[1,1]
    trace = (int(R_n[0, 0]) + int(R_n[1, 1])) % mod

    return trace


def fibonacci_mod(n: int, mod: int = 2**64) -> int:
    """
    Compute F_n mod m via matrix element.

    Args:
        n: Fibonacci index (non-negative)
        mod: Modulus

    Returns:
        F_n mod m

    Mathematical Identity:
        F_n = R^n[0,1] = R^n[1,0]

    Example:
        fibonacci_mod(7) == 13   # F_7 = 13 (First Stable Resonance!)
        fibonacci_mod(10) == 55
        fibonacci_mod(13) == 233
    """
    if n < 0:
        raise ValueError("Fibonacci index must be non-negative")

    if n == 0:
        return 0
    if n == 1:
        return 1 % mod

    R_n = matrix_power_mod(R_MATRIX, n, mod)

    return int(R_n[0, 1]) % mod


def fibonacci_pair_mod(n: int, mod: int = 2**64) -> Tuple[int, int]:
    """
    Compute (F_n, F_{n+1}) mod m simultaneously.

    More efficient than computing each separately.

    Args:
        n: Fibonacci index
        mod: Modulus

    Returns:
        (F_n mod m, F_{n+1} mod m)
    """
    if n < 0:
        raise ValueError("Fibonacci index must be non-negative")

    if n == 0:
        return (0, 1 % mod)

    R_n = matrix_power_mod(R_MATRIX, n, mod)

    F_n = int(R_n[0, 1]) % mod
    F_n1 = int(R_n[1, 1]) % mod

    return (F_n, F_n1)


# =============================================================================
# LUCAS NONCE GENERATION
# =============================================================================

def lucas_nonce(block_height: int, attempt: int, mod: int = 2**32) -> int:
    """
    Generate a deterministic nonce using Lucas numbers.

    The nonce is derived from the block height and attempt number
    using the Lucas trace formula, providing algebraic structure
    to what would otherwise be random nonce searching.

    Args:
        block_height: Current block height
        attempt: Mining attempt number within this block
        mod: Modulus for nonce space (default 2^32)

    Returns:
        Nonce value in [0, mod)

    Formula:
        nonce = L_{height + attempt} mod m

    This creates a deterministic sequence of nonces that:
    1. Is reproducible given height and attempt
    2. Has the algebraic structure of Lucas numbers
    3. Covers the nonce space pseudo-randomly
    """
    index = block_height + attempt
    return lucas_trace(index, mod)


def lucas_nonce_batch(
    block_height: int,
    start_attempt: int,
    count: int,
    mod: int = 2**32
) -> np.ndarray:
    """
    Generate a batch of Lucas nonces efficiently.

    Uses the recurrence L_{n+1} = L_n + L_{n-1} to generate
    consecutive nonces without repeated matrix exponentiation.

    Args:
        block_height: Current block height
        start_attempt: Starting attempt number
        count: Number of nonces to generate
        mod: Modulus

    Returns:
        Array of nonce values
    """
    if count <= 0:
        return np.array([], dtype=np.uint32)

    nonces = np.zeros(count, dtype=np.uint32)

    # Compute first two values via matrix
    base_index = block_height + start_attempt

    if base_index == 0:
        L_prev = 2  # L_0
        L_curr = 1  # L_1
    elif base_index == 1:
        L_prev = 1  # L_1
        L_curr = 3  # L_2
    else:
        # Get L_{base_index-1} and L_{base_index}
        L_prev = lucas_trace(base_index - 1, mod)
        L_curr = lucas_trace(base_index, mod)

    # Handle edge case for first element
    if base_index == 0:
        nonces[0] = L_prev  # L_0 = 2
        if count > 1:
            nonces[1] = L_curr  # L_1 = 1
        start_idx = 2
    else:
        nonces[0] = L_curr
        start_idx = 1

    # Use recurrence for remaining: L_{n+1} = L_n + L_{n-1}
    for i in range(start_idx, count):
        L_next = (L_prev + L_curr) % mod
        nonces[i] = L_next
        L_prev = L_curr
        L_curr = L_next

    return nonces


# =============================================================================
# VERIFICATION UTILITIES
# =============================================================================

def verify_lucas_identity(n: int) -> bool:
    """
    Verify L_n = F_{n-1} + F_{n+1} for given n.

    Args:
        n: Index to verify (must be >= 1)

    Returns:
        True if identity holds
    """
    if n < 1:
        return n == 0  # L_0 = 2 is special

    L_n = lucas_trace(n, 2**64)
    F_prev = fibonacci_mod(n - 1, 2**64)
    F_next = fibonacci_mod(n + 1, 2**64)

    return L_n == (F_prev + F_next)


def verify_matrix_eigenvalues() -> dict:
    """
    Verify R matrix has eigenvalues PHI and -1/PHI.

    The eigenvalues of R = [[0,1],[1,1]] are:
        lambda_1 = PHI = (1 + sqrt(5)) / 2
        lambda_2 = -1/PHI = (1 - sqrt(5)) / 2

    Returns:
        Dictionary with verification results
    """
    # Compute eigenvalues numerically
    R = np.array([[0, 1], [1, 1]], dtype=np.float64)
    eigenvalues = np.linalg.eigvals(R)

    # Sort by magnitude (PHI > |-1/PHI|)
    eigenvalues = sorted(eigenvalues, key=lambda x: -abs(x))

    lambda_1 = eigenvalues[0]
    lambda_2 = eigenvalues[1]

    return {
        'lambda_1': float(lambda_1),
        'lambda_2': float(lambda_2),
        'expected_lambda_1': PHI,
        'expected_lambda_2': -1/PHI,
        'lambda_1_match': abs(lambda_1 - PHI) < 1e-10,
        'lambda_2_match': abs(lambda_2 - (-1/PHI)) < 1e-10,
        'product_is_minus_one': abs(lambda_1 * lambda_2 - (-1)) < 1e-10,
        'sum_is_one': abs(lambda_1 + lambda_2 - 1) < 1e-10,
    }


def get_matrix_at_power(n: int) -> np.ndarray:
    """
    Get R^n as a regular numpy array (for inspection).

    Args:
        n: Power

    Returns:
        R^n as 2x2 numpy array with Python int entries
    """
    if n < 0:
        raise ValueError("Power must be non-negative")

    if n == 0:
        return np.array([[1, 0], [0, 1]])

    # Use large modulus to get exact values for reasonable n
    mod = 10**18
    R_n = matrix_power_mod(R_MATRIX, n, mod)

    return np.array([[int(R_n[0, 0]), int(R_n[0, 1])],
                     [int(R_n[1, 0]), int(R_n[1, 1])]])


# =============================================================================
# CROSS-REFERENCE UTILITIES
# =============================================================================

def lucas_mass_indices() -> dict:
    """
    Return Lucas indices used in mass formulas from resonance_formalism.md.

    These are the specific indices that appear in the tau mass formula
    and other physical predictions.
    """
    return {
        'L_7': lucas_trace(7, 2**64),    # 29
        'L_10': lucas_trace(10, 2**64),  # 123
        'L_17': lucas_trace(17, 2**64),  # 3571
        'tau_mass_formula': 'L_17 - L_10 + L_7 = 3571 - 123 + 29 = 3477',
        'tau_mass_actual_MeV': 1776.86,
        'note': 'The formula gives dimensionless ratio, not direct mass',
    }


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    # Constants
    'R_MATRIX',
    'I_MATRIX',
    # Matrix operations
    'matrix_multiply_mod',
    'matrix_power_mod',
    # Lucas/Fibonacci
    'lucas_trace',
    'fibonacci_mod',
    'fibonacci_pair_mod',
    # Nonce generation
    'lucas_nonce',
    'lucas_nonce_batch',
    # Verification
    'verify_lucas_identity',
    'verify_matrix_eigenvalues',
    'get_matrix_at_power',
    # Cross-reference
    'lucas_mass_indices',
]
