import hashlib
import time
import os
from Crypto.Protocol.KDF import PBKDF2

# --- Utility function to hash a password using PBKDF2 ---
def hash_password(password: str) -> str:
    """
    Hashes a password using PBKDF2 (from PyCryptodome) with a salt.
    
    Args:
        password (str): The plain text password to be hashed.
    
    Returns:
        str: The hexadecimal string of the hashed password.
    """
    salt = os.urandom(16)  # Generate a random 16-byte salt
    hashed_password = PBKDF2(password.encode(), salt, dkLen=32, count=1000000)  # PBKDF2 hash
    return f"{salt.hex()}${hashed_password.hex()}"  # Return both salt and hashed password

# --- Function to generate a unique hash from name, password, and timestamp ---
def generate_secure_id(name: str, password: str, use_time: bool = True) -> str:
    """
    Generates a 16-digit hexadecimal UID or MID using SHA-256 hashing.

    Args:
        name (str): Name of the user or merchant.
        password (str): Their password.
        use_time (bool): Whether to include current timestamp in the hash.

    Returns:
        str: A 16-character hexadecimal ID (e.g., UID or MID)
    """
    timestamp = str(int(time.time())) if use_time else ""
    seed = name + password + timestamp  # Concatenate name, password, and timestamp
    hash_object = hashlib.sha256(seed.encode())  # SHA-256 hashing
    unique_id = hash_object.hexdigest()[:16]  # First 16 characters as UID/MID
    return unique_id
