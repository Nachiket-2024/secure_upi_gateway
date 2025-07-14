# --- Import AES from pycryptodome for block encryption ---
from Crypto.Cipher import AES

# --- Fixed encryption key (must be 16 bytes for AES-128) ---
KEY = b'SecureSPECKKey!!'  # 16 bytes = 128 bits

# --- AES block size (fixed for ECB mode) ---
BLOCK_SIZE = 16

# --- Function to pad input data to a multiple of block size using PKCS7 padding ---
def pad(data: bytes) -> bytes:
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)         # Number of padding bytes needed
    return data + bytes([pad_len] * pad_len)                # Add padding (e.g., \x04\x04\x04\x04)

# --- Function to remove padding after decryption ---
def unpad(data: bytes) -> bytes:
    pad_len = data[-1]                                      # Last byte indicates padding length
    return data[:-pad_len]                                  # Remove padding bytes

# --- Encrypt a plaintext string using AES ECB mode (acts as lightweight cipher) ---
def encrypt_speck(plain_text: str) -> str:
    cipher = AES.new(KEY, AES.MODE_ECB)                     # Create AES cipher in ECB mode
    padded_data = pad(plain_text.encode())                  # Convert to bytes and pad
    encrypted = cipher.encrypt(padded_data)                 # Encrypt padded data
    return encrypted.hex()                                  # Return as hex string (safe for QR)

# --- Decrypt hex string back to original plaintext ---
def decrypt_speck(cipher_hex: str) -> str:
    cipher = AES.new(KEY, AES.MODE_ECB)                     # Create AES cipher in ECB mode
    encrypted_bytes = bytes.fromhex(cipher_hex)             # Convert hex to raw bytes
    decrypted_padded = cipher.decrypt(encrypted_bytes)      # Decrypt bytes
    return unpad(decrypted_padded).decode()                 # Remove padding and decode to string
