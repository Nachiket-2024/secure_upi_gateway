# --- Standard SQLAlchemy imports for defining database models ---
from sqlalchemy import Column, String, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from ..database.database import Base

# --- Define the MerchantModel class representing the merchants table ---
class MerchantModel(Base):
    __tablename__ = 'merchants'  # Name of the table in the PostgreSQL database

    # --- Primary key: Unique Merchant ID (generated using SHA256, 16-digit hex) ---
    id = Column(String, primary_key=True, index=True)

    # --- Name of the merchant (used for hashing and display) ---
    name = Column(String, nullable=False)

    # --- IFSC code of the branch associated with this merchant ---
    ifsc = Column(String, nullable=False)

    # --- Account balance of the merchant ---
    balance = Column(Float, default=0.0)

    # --- Password field: stores hashed password securely ---
    password = Column(String, nullable=False)

    # --- Timestamp of account creation (automatically set to current time) ---
    created_at = Column(DateTime(timezone=True), server_default=func.now())
