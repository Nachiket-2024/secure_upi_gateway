# --- Import Pydantic BaseModel for defining request/response schemas ---
from pydantic import BaseModel
from datetime import datetime  # To represent timestamp using datetime for PostgreSQL

# --- Base schema shared by all transaction-related operations ---
class TransactionBase(BaseModel):
    uid: str                   # User ID of the payer
    mid: str                   # Merchant ID of the payee
    amount: float              # Amount being transferred

# --- Schema used when creating a transaction (POST request) ---
class TransactionCreate(TransactionBase):
    pass  # Inherits everything from TransactionBase with no additional fields

# --- Schema used when returning transaction data (response model) ---
class Transaction(TransactionBase):
    id: str                   # Unique Transaction ID (can be SHA256 hash)
    timestamp: datetime       # Time when the transaction occurred

    class Config:
        orm_mode = True       # Enables compatibility with ORM models (like SQLAlchemy)
