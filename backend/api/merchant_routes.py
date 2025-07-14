# --- FastAPI and typing imports ---
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import uuid4  # For generating unique IDs if needed (alternative to SHA256)
from hashlib import sha256
from datetime import datetime

# --- Local project imports ---
from ..models.merchant_model import MerchantModel
from ..schemas.merchant_schema import MerchantCreate, Merchant, MerchantUpdate
from ..database.database import get_db  # Dependency that provides DB session
from passlib.context import CryptContext  # For password hashing

# --- Initialize the router for merchant endpoints ---
router = APIRouter(
    prefix="/merchant",
    tags=["Merchant"]
)

# --- Initialize a password hashing context (using bcrypt) ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Utility function to hash password ---
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# --- Generate unique Merchant ID using SHA256 hash ---
def generate_merchant_id(name: str, password: str, created_at: datetime) -> str:
    seed = f"{name}{password}{created_at.timestamp()}"
    return sha256(seed.encode()).hexdigest()[:16]  # Take first 16 hex characters

# --- Create a new merchant ---
@router.post("/", response_model=Merchant)
def create_merchant(merchant: MerchantCreate, db: Session = Depends(get_db)):
    # --- Generate creation timestamp ---
    created_at = datetime.now()

    # --- Generate unique MID (16-character hex from SHA256) ---
    mid = generate_merchant_id(merchant.name, merchant.password, created_at)

    # --- Hash the password before storing ---
    hashed_password = hash_password(merchant.password)

    # --- Check if MID already exists (should be unique) ---
    existing = db.query(MerchantModel).filter(MerchantModel.id == mid).first()
    if existing:
        raise HTTPException(status_code=400, detail="Merchant ID collision. Try again.")

    # --- Create the ORM merchant object ---
    db_merchant = MerchantModel(
        id=mid,
        name=merchant.name,
        ifsc=merchant.ifsc,
        balance=merchant.balance,
        password=hashed_password,
        created_at=created_at
    )

    # --- Add to DB and commit ---
    db.add(db_merchant)
    db.commit()
    db.refresh(db_merchant)

    return db_merchant

# --- Get a merchant by ID ---
@router.get("/{merchant_id}", response_model=Merchant)
def get_merchant(merchant_id: str, db: Session = Depends(get_db)):
    merchant = db.query(MerchantModel).filter(MerchantModel.id == merchant_id).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return merchant

# --- Update merchant details ---
@router.put("/{merchant_id}", response_model=Merchant)
def update_merchant(merchant_id: str, updates: MerchantUpdate, db: Session = Depends(get_db)):
    merchant = db.query(MerchantModel).filter(MerchantModel.id == merchant_id).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")

    # --- Update fields if they are provided ---
    if updates.name:
        merchant.name = updates.name
    if updates.ifsc:
        merchant.ifsc = updates.ifsc
    if updates.balance is not None:
        merchant.balance = updates.balance
    if updates.password:
        merchant.password = hash_password(updates.password)

    db.commit()
    db.refresh(merchant)
    return merchant

# --- Delete merchant account ---
@router.delete("/{merchant_id}")
def delete_merchant(merchant_id: str, db: Session = Depends(get_db)):
    merchant = db.query(MerchantModel).filter(MerchantModel.id == merchant_id).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")

    db.delete(merchant)
    db.commit()
    return {"detail": "Merchant deleted successfully"}
