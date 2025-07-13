# --- FastAPI Imports ---
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import hashlib
import time

# --- FastAPI app instance ---
app = FastAPI()

# --- In-memory "database" to hold merchants (temporary, replace with DB later) ---
merchants_db = {}

# --- Request body structure for merchant registration ---
class MerchantRegisterRequest(BaseModel):
    name: str
    ifsc: str
    password: str
    balance: float

# --- Utility function to generate 16-digit Merchant ID using SHA-256 ---
def generate_merchant_id(name: str, password: str, timestamp: str) -> str:
    """
    Combines merchant name, password, and time to create a SHA-256 hash,
    then slices the first 16 hexadecimal characters as the MID.
    """
    base_string = name + password + timestamp
    hash_val = hashlib.sha256(base_string.encode()).hexdigest()
    return hash_val[:16]

# --- Utility function to hash password ---
def hash_password(password: str) -> str:
    """ Hashes a password using bcrypt. """

# --- POST /register/merchant API route ---
@app.post("/register/merchant")
def register_merchant(payload: MerchantRegisterRequest):
    """
    Registers a new merchant and generates a 16-digit MID using SHA256.

    Returns:
        dict: Merchant ID and success message.
    """
    # Timestamp to ensure MID uniqueness
    timestamp = str(time.time())

    # Generate Merchant ID (MID)
    mid = generate_merchant_id(payload.name, payload.password, timestamp)

    # Check if MID already exists (very unlikely)
    if mid in merchants_db:
        raise HTTPException(status_code=400, detail="Merchant already exists")

    # Hash the password before storing
    hashed_password = hash_password(payload.password)

    # Store in in-memory DB
    merchants_db[mid] = {
        "name": payload.name,
        "ifsc": payload.ifsc,
        "password": hashed_password,  # Store hashed password
        "balance": payload.balance,
        "created_at": timestamp
    }

    return {
        "message": "Merchant registered successfully",
        "mid": mid
    }
