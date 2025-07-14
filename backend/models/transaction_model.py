# --- Import necessary components from SQLAlchemy ---
from sqlalchemy import Column, String, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from ..database.database import Base

# --- Define the TransactionModel representing a transaction entry in the database ---
class TransactionModel(Base):
    __tablename__ = "transactions"  # Name of the table in the PostgreSQL database

    # --- Primary key: unique transaction ID (could be a SHA256 hash) ---
    id = Column(String, primary_key=True, index=True)

    # --- UID of the user who is making the payment ---
    uid = Column(String, nullable=False)

    # --- MID of the merchant who is receiving the payment ---
    mid = Column(String, nullable=False)

    # --- Amount being transferred in the transaction ---
    amount = Column(Float, nullable=False)

    # --- Timestamp of when the transaction was created (auto set using PostgreSQL NOW()) ---
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
