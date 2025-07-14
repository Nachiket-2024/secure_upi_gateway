from pydantic import BaseModel
from datetime import datetime

# --- Schema for blockchain block ---
class Block(BaseModel):
    id: str
    transaction_id: str
    prev_hash: str
    timestamp: datetime

    class Config:
        orm_mode = True
