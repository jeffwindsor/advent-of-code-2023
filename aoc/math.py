"""Number and math utility functions."""

import math
from functools import reduce


def count_continuous_segments(sorted_coords: list[int]) -> int:
    """
    Count continuous segments in sorted coordinates.

    Args:
        sorted_coords: List of sorted integers

    Returns:
        Number of continuous segments

    Examples:
        >>> count_continuous_segments([0, 1, 2, 5, 6])
        2  # Two segments: [0,1,2] and [5,6]
        >>> count_continuous_segments([0, 1, 2])
        1  # One segment
        >>> count_continuous_segments([0, 2, 4])
        3  # Three segments
    """
    if not sorted_coords:
        return 0

    segments = 1
    for i in range(1, len(sorted_coords)):
        if sorted_coords[i] != sorted_coords[i - 1] + 1:
            segments += 1
    return segments


def count_digits(n: int) -> int:
    """
    Count the number of digits in a positive integer.

    Args:
        n: A non-negative integer

    Returns:
        The number of digits in n (e.g., 123 -> 3, 0 -> 1)

    Examples:
        >>> count_digits(0)
        1
        >>> count_digits(123)
        3
        >>> count_digits(9999)
        4
    """
    if n == 0:
        return 1
    count = 0
    while n > 0:
        count += 1
        n //= 10
    return count


def calculate_toggle_states(toggles: list[int], size: int) -> list[bool]:
    """
    Calculate final states after multiple toggles.

    Each element in toggles represents an index to toggle. An element
    is ON if toggled an odd number of times (parity-based).

    Args:
        toggles: List of indices that were toggled
        size: Total number of elements

    Returns:
        List of final boolean states (True = ON)

    Examples:
        >>> calculate_toggle_states([0, 1, 0, 2], 3)
        [False, True, True]
        >>> calculate_toggle_states([1, 3, 2, 3], 5)
        [False, True, True, False, False]
    """
    from collections import Counter
    counts = Counter(toggles)
    return [counts.get(i, 0) % 2 == 1 for i in range(size)]


def gcd(a: int, b: int) -> int:
    """
    Calculate the Greatest Common Divisor of two numbers.

    Args:
        a: First integer
        b: Second integer

    Returns:
        Greatest common divisor of a and b

    Examples:
        >>> gcd(12, 8)
        4
        >>> gcd(17, 19)
        1
        >>> gcd(100, 50)
        50
    """
    return math.gcd(a, b)


def lcm(a: int, b: int) -> int:
    """
    Calculate the Least Common Multiple of two numbers.

    Args:
        a: First integer
        b: Second integer

    Returns:
        Least common multiple of a and b

    Examples:
        >>> lcm(12, 8)
        24
        >>> lcm(3, 5)
        15
        >>> lcm(10, 15)
        30
    """
    return abs(a * b) // math.gcd(a, b)


def lcm_multiple(numbers: list[int]) -> int:
    """
    Calculate the LCM of multiple numbers.

    Args:
        numbers: List of integers

    Returns:
        Least common multiple of all numbers

    Examples:
        >>> lcm_multiple([2, 3, 4])
        12
        >>> lcm_multiple([5, 10, 15])
        30
    """
    return reduce(lcm, numbers)


def gcd_multiple(numbers: list[int]) -> int:
    """
    Calculate the GCD of multiple numbers.

    Args:
        numbers: List of integers

    Returns:
        Greatest common divisor of all numbers

    Examples:
        >>> gcd_multiple([12, 18, 24])
        6
        >>> gcd_multiple([10, 15, 20])
        5
    """
    return reduce(math.gcd, numbers)


def is_prime(n: int) -> bool:
    """
    Check if a number is prime.

    Args:
        n: Integer to check

    Returns:
        True if n is prime, False otherwise

    Examples:
        >>> is_prime(2)
        True
        >>> is_prime(17)
        True
        >>> is_prime(4)
        False
        >>> is_prime(1)
        False
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Check odd divisors up to sqrt(n)
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def primes_up_to(n: int) -> list[int]:
    """
    Generate all prime numbers up to n using Sieve of Eratosthenes.

    Args:
        n: Upper bound (inclusive)

    Returns:
        List of all prime numbers up to n

    Examples:
        >>> primes_up_to(10)
        [2, 3, 5, 7]
        >>> primes_up_to(20)
        [2, 3, 5, 7, 11, 13, 17, 19]
    """
    if n < 2:
        return []

    # Sieve of Eratosthenes
    is_prime_arr = [True] * (n + 1)
    is_prime_arr[0] = is_prime_arr[1] = False

    for i in range(2, int(n**0.5) + 1):
        if is_prime_arr[i]:
            for j in range(i * i, n + 1, i):
                is_prime_arr[j] = False

    return [i for i, prime in enumerate(is_prime_arr) if prime]


def prime_factors(n: int) -> dict[int, int]:
    """
    Find prime factorization of n.

    Args:
        n: Integer to factorize

    Returns:
        Dictionary mapping prime factors to their exponents

    Examples:
        >>> prime_factors(12)
        {2: 2, 3: 1}
        >>> prime_factors(100)
        {2: 2, 5: 2}
        >>> prime_factors(17)
        {17: 1}
    """
    if n < 2:
        return {}

    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def mod_inverse(a: int, m: int) -> int:
    """
    Calculate modular multiplicative inverse of a mod m.

    Args:
        a: Number to find inverse of
        m: Modulus

    Returns:
        x such that (a * x) % m == 1

    Raises:
        ValueError: If modular inverse doesn't exist

    Examples:
        >>> mod_inverse(3, 11)
        4
        >>> mod_inverse(10, 17)
        12
    """
    # Extended Euclidean Algorithm
    def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        gcd_val, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd_val, x, y

    gcd_val, x, _ = extended_gcd(a % m, m)
    if gcd_val != 1:
        raise ValueError(f"Modular inverse doesn't exist for {a} mod {m}")
    return (x % m + m) % m


def chinese_remainder_theorem(remainders: list[int], moduli: list[int]) -> int:
    """
    Solve system of congruences using Chinese Remainder Theorem.

    Args:
        remainders: List of remainders
        moduli: List of moduli (must be pairwise coprime)

    Returns:
        Solution x such that x ≡ remainders[i] (mod moduli[i]) for all i

    Examples:
        >>> chinese_remainder_theorem([2, 3, 1], [3, 4, 5])
        11
    """
    total = 0
    prod = reduce(lambda a, b: a * b, moduli)

    for remainder, modulus in zip(remainders, moduli):
        p = prod // modulus
        total += remainder * mod_inverse(p, modulus) * p

    return total % prod


__all__ = [
    "count_continuous_segments",
    "count_digits",
    "calculate_toggle_states",
    "gcd",
    "lcm",
    "lcm_multiple",
    "gcd_multiple",
    "is_prime",
    "primes_up_to",
    "prime_factors",
    "mod_inverse",
    "chinese_remainder_theorem",
]
