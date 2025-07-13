# --- SPECK Lightweight Encryption (Simplified 32/64 variant) ---
# NOTE: This version is designed for academic/demo purposes only, not production cryptography.

# Define the block word size for the cipher (we're using 16-bit words for simplicity)
WORD_SIZE = 16

# Create a bitmask based on the word size to ensure proper truncation (e.g., 0xFFFF for 16-bit)
MASK_VAL = 2 ** WORD_SIZE - 1

# Define the number of encryption rounds (standard is 22 for SPECK32/64, but we reduce to 10 for speed)
ROUNDS = 10


# --- Left circular rotation ---
def rol(x, r):
    """
    Performs a left rotate (circular shift) on x by r bits.
    Example: rol(0b1001, 2) => 0b0110
    """
    return ((x << r) & MASK_VAL) | (x >> (WORD_SIZE - r))


# --- Right circular rotation ---
def ror(x, r):
    """
    Performs a right rotate (circular shift) on x by r bits.
    Example: ror(0b1001, 2) => 0b0110
    """
    return (x >> r) | ((x << (WORD_SIZE - r)) & MASK_VAL)


# --- Key scheduling algorithm for SPECK ---
def speck_key_schedule(key):
    """
    Generates round keys from the provided key tuple.
    Args:
        key (tuple): A 4-element tuple of 16-bit words.

    Returns:
        list: A list of 16-bit round keys for each round.
    """
    k = [key[0]]         # Start with the first word as the initial round key
    l = list(key[1:])    # Remaining words go into the 'L' list

    # Perform key schedule operations for each round
    for i in range(ROUNDS - 1):
        # Rotate left entry right by 7, add current key, XOR with round index
        l.append((ror(l[i], 7) + k[i]) & MASK_VAL ^ i)

        # Rotate current key left by 2, XOR with new l[i+3]
        k.append(rol(k[i], 2) ^ l[-1])

    return k


# --- SPECK encryption function ---
def speck_encrypt(plain, key):
    """
    Encrypts a 32-bit block using the SPECK cipher.

    Args:
        plain (tuple): 2-element tuple of 16-bit words (plaintext).
        key (tuple): 4-element tuple of 16-bit words (master key).

    Returns:
        tuple: Encrypted 2-element tuple (ciphertext).
    """
    x, y = plain                       # Unpack 2-word plaintext block
    round_keys = speck_key_schedule(key)  # Generate round keys

    # Perform round-wise encryption
    for k in round_keys:
        x = (ror(x, 7) + y) & MASK_VAL ^ k
        y = rol(y, 2) ^ x

    return (x, y)                      # Return ciphertext tuple


# --- SPECK decryption function ---
def speck_decrypt(cipher, key):
    """
    Decrypts a 32-bit block using the SPECK cipher.

    Args:
        cipher (tuple): 2-element tuple of 16-bit words (ciphertext).
        key (tuple): 4-element tuple of 16-bit words (master key).

    Returns:
        tuple: Decrypted 2-element tuple (plaintext).
    """
    x, y = cipher                      # Unpack ciphertext block
    round_keys = speck_key_schedule(key)  # Regenerate the same round keys

    # Perform decryption in reverse order of rounds
    for k in reversed(round_keys):
        y = ror(y ^ x, 2)
        x = rol(((x ^ k) - y) & MASK_VAL, 7)

    return (x, y)                      # Return plaintext tuple


# --- Helper: Convert 4-character string into a 2-word block (each 16-bit) ---
def string_to_block(s):
    """
    Converts a 4-character string into a pair of 16-bit integers (little-endian).

    Args:
        s (str): A 4-character string (e.g., 'MID1')

    Returns:
        tuple: (int16, int16) representation of the string
    """
    b = s.encode("utf-8")                         # Encode string to bytes
    b = b.ljust(4, b'\x00')[:4]                   # Ensure exactly 4 bytes, pad with nulls if needed
    return int.from_bytes(b[:2], 'little'), int.from_bytes(b[2:], 'little')


# --- Helper: Convert encrypted 2-word block back into string ---
def block_to_string(b):
    """
    Converts a tuple of 2 integers (16-bit words) back into a 4-character string.

    Args:
        b (tuple): Encrypted or decrypted block (x, y)

    Returns:
        str: Original 4-character string
    """
    return (b[0].to_bytes(2, 'little') + b[1].to_bytes(2, 'little')).decode("utf-8", errors="ignore").rstrip('\x00')
