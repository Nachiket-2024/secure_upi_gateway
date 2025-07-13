# --- Imports ---
import hashlib
import time

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
    # Get current timestamp in seconds if needed
    timestamp = str(int(time.time())) if use_time else ""

    # Concatenate inputs to form a unique seed
    seed = name + password + timestamp

    # Create SHA-256 hash of the seed string
    hash_object = hashlib.sha256(seed.encode())

    # Convert the hash into a hexadecimal string and take first 16 characters
    unique_id = hash_object.hexdigest()[:16]

    return unique_id
