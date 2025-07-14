# --- Import BaseModel from Pydantic for request/response schema definitions ---
from pydantic import BaseModel
from datetime import datetime  # For timestamp fields compatible with PostgreSQL

# --- Base schema for all merchant-related operations ---
class MerchantBase(BaseModel):
    name: str                   # Name of the merchant
    ifsc: str                   # IFSC code of the bank branch the merchant is registered with
    balance: float              # Account balance of the merchant

# --- Schema used when creating a new merchant account (input to POST API) ---
class MerchantCreate(MerchantBase):
    password: str               # Plain password (will be hashed before storing)

# --- Schema used when updating merchant details (input to PUT/PATCH API) ---
class MerchantUpdate(MerchantBase):
    password: str | None = None # Optional: update password if provided
    balance: float | None = None # Optional: update balance if provided

# --- Schema used when returning merchant data from the database (output format) ---
class Merchant(MerchantBase):
    id: str                     # Unique merchant ID (MID), generated using SHA256
    created_at: datetime        # Account creation timestamp (PostgreSQL-compatible)

    class Config:
        orm_mode = True         # Enables compatibility with SQLAlchemy ORM models
