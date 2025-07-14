# --- SQLAlchemy imports ---
from sqlalchemy import Column, String, DateTime, ForeignKey, func
from ..database.database import Base

# --- ORM Model representing a Blockchain Block ---
class BlockModel(Base):
    __tablename__ = "blockchain"

    # Current block's hash (acts as primary key)
    id = Column(String, primary_key=True, index=True)

    # Transaction ID from the transactions table (foreign key)
    transaction_id = Column(String, ForeignKey("transactions.id"), nullable=False)

    # Hash of the previous block
    prev_hash = Column(String, nullable=False)

    # Timestamp when block was created
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
