# --- Import required libraries ---
import random  # For generating random integers used in factor trials
import time    # For benchmarking how long factorization takes

# --- Convert a truncated hex string (64-bit SHA hash) to an integer ---
def truncated_hex_to_int(truncated_hex):
    """Convert a truncated hex string to an integer."""
    return int(truncated_hex, 16)

# --- Generate modulus N = UID_int * PIN ---
def generate_modulus_from_truncated(truncated_hex, pin):
    """Generate modulus N from truncated SHA-256 hex and PIN."""
    uid_int = truncated_hex_to_int(truncated_hex)  # Convert hex to integer
    pin_int = int(pin)                             # Convert PIN to integer
    return uid_int * pin_int                       # Return modulus

# --- Compute the greatest common divisor (Euclidean algorithm) ---
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# --- Modular exponentiation: (a^b mod n) ---
def mod_exp(a, b, n):
    result = 1
    while b > 0:
        if b % 2 == 1:
            result = (result * a) % n
        a = (a * a) % n
        b = b // 2
    return result

# --- Find the period r such that a^r ≡ 1 (mod N) ---
def find_period(a, N, max_attempts=1000000):
    r = 1
    while mod_exp(a, r, N) != 1 and r < max_attempts:
        r += 1
    return r if r < max_attempts else None

# --- Simulated version of Shor's algorithm for classical machines ---
def shor_factor(N, max_attempts=1000000):
    if N % 2 == 0:
        return [2, N // 2]  # Quick exit for even N

    for _ in range(5):  # Try up to 5 random bases `a`
        a = random.randint(2, N - 1)
        if gcd(a, N) != 1:
            continue  # Skip if a shares a factor with N
        r = find_period(a, N, max_attempts)
        if r and r % 2 == 0:  # Only if r is even
            x = mod_exp(a, r // 2, N)
            if x not in (1, N - 1):
                f1 = gcd(x + 1, N)
                f2 = gcd(x - 1, N)
                if f1 * f2 == N:
                    return sorted([f1, f2])  # Return factors
                return None
    return None  # Return None if no factors found

# --- End-to-end vulnerability checker using simulated Shor's logic ---
def check_vulnerability_from_truncated(truncated_hex, pin, max_attempts=1000000):
    """Check vulnerability given a truncated SHA256 hex string and PIN."""
    print(f"\nTruncated SHA-256 (64 bits): {truncated_hex}")
    print(f"PIN: {pin}")

    # Generate modulus N = UID * PIN
    N = generate_modulus_from_truncated(truncated_hex, pin)
    print(f"→ N = {N}")

    # Start timer
    start = time.time()

    # Attempt to factor N using simulated Shor's algorithm
    factors = shor_factor(N, max_attempts=max_attempts)

    # End timer
    end = time.time()

    # Print result
    if factors:
        print(f"VULNERABLE! Factors found: {factors}")
    else:
        print("Secure (within classical Shor simulation limits)")

    print(f"Time taken: {end - start:.3f} seconds")

# --- Run test cases if executed directly ---
if __name__ == "__main__":
    test_cases = [
        ("3d2e1f8c6a7b9c01", "1000"),
        ("abcdef1234567890", "3571"),
        ("f1e2d3c4b5a69717", "9901"),
        ("b33fb33fb33fb33f", "2025"),
    ]

    # Loop through and evaluate each test case
    for hex_val, pin_val in test_cases:
        check_vulnerability_from_truncated(hex_val, pin_val)
