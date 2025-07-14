# --- Import SQLAlchemy components for defining the ORM model ---
from sqlalchemy import Column, String, Float, DateTime, func
from ..database.database import Base  # Import shared declarative base for table mapping

# --- Define the UserModel class which maps to the "users" table in the database ---
class UserModel(Base):
    __tablename__ = "users"  # Table name in PostgreSQL

    # --- Primary key: UID (User ID), 16-char hex string generated using SHA256 ---
    id = Column(String, primary_key=True, index=True)

    # --- Name of the user ---
    name = Column(String, nullable=False)

    # --- IFSC code of the user's bank branch ---
    ifsc = Column(String, nullable=False)

    # --- User's account balance ---
    balance = Column(Float, default=0.0)

    # --- Hashed password stored securely (not raw password) ---
    password = Column(String, nullable=False)

    # --- User's mobile number (used in MMID generation) ---
    mobile_number = Column(String, unique=True, nullable=False)

    # --- PIN used for authorizing UPI payments (hashed) ---
    pin = Column(String, nullable=False)

    # --- UID creation timestamp ---
    created_at = Column(DateTime(timezone=True), server_default=func.now())
