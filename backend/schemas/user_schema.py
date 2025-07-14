# --- Import Pydantic base model ---
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# --- Shared base schema for user (common fields used in multiple schemas) ---
class UserBase(BaseModel):
    name: str                          # User's full name
    ifsc: str                          # IFSC code of the bank branch
    balance: float                     # Initial account balance
    mobile_number: str                 # Registered mobile number

# --- Schema used when creating a user ---
class UserCreate(UserBase):
    password: str                      # Login password (will be hashed)
    pin: str                           # UPI transaction PIN (will be hashed)

# --- Schema used when updating user information ---
class UserUpdate(BaseModel):
    name: Optional[str] = None         # Optional update: name
    ifsc: Optional[str] = None         # Optional update: IFSC
    balance: Optional[float] = None    # Optional update: balance
    password: Optional[str] = None     # Optional update: password
    pin: Optional[str] = None          # Optional update: PIN
    mobile_number: Optional[str] = None  # Optional update: mobile number

# --- Schema used when returning user information (read-only) ---
class User(UserBase):
    id: str                            # UID (User ID)
    created_at: datetime               # Account creation timestamp

    class Config:
        orm_mode = True               # Enables compatibility with ORM (SQLAlchemy model)
