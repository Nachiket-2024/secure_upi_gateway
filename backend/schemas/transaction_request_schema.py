# --- Schema for incoming UPI transaction requests (from UPI machine to bank) ---
from pydantic import BaseModel

class TransactionRequest(BaseModel):
    mmid: str                 # MMID of the user (computed from UID + mobile)
    pin: str                  # User's PIN (plaintext, will be hashed and verified)
    amount: float             # Amount to be transferred
    encrypted_mid: str        # Encrypted Merchant ID from QR code
