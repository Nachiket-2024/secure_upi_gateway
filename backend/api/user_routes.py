# --- FastAPI and utility imports ---
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from hashlib import sha256

# --- Password hashing ---
from passlib.context import CryptContext

# --- Pydantic schemas ---
from ..schemas.user_schema import UserCreate, User, UserUpdate

# --- SQLAlchemy model ---
from ..models.user_model import UserModel

# --- DB session provider ---
from ..database.database import get_db

# --- Initialize password context using bcrypt ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Initialize router for user routes ---
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# --- Utility to hash passwords and PINs securely ---
def hash_secret(secret: str) -> str:
    return pwd_context.hash(secret)

# --- Utility to generate UID (User ID) as 16-digit hex string ---
def generate_uid(name: str, password: str, timestamp: float) -> str:
    seed = f"{name}{password}{timestamp}"
    return sha256(seed.encode()).hexdigest()[:16]

# --- Utility to generate MMID (Mobile Money Identifier) ---
def generate_mmid(uid: str, mobile_number: str) -> str:
    mmid_raw = uid + mobile_number
    return sha256(mmid_raw.encode()).hexdigest()[:12]

# --- Route to register a new user ---
@router.post("/", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # --- Check if mobile number is already used ---
    existing_user = db.query(UserModel).filter(UserModel.mobile_number == user.mobile_number).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Mobile number already registered.")

    # --- Generate UID using hashed inputs and current time ---
    from time import time
    timestamp = time()
    uid = generate_uid(user.name, user.password, timestamp)

    # --- Hash password and pin before storing ---
    hashed_password = hash_secret(user.password)
    hashed_pin = hash_secret(user.pin)

    # --- Create ORM model instance ---
    db_user = UserModel(
        id=uid,
        name=user.name,
        ifsc=user.ifsc,
        balance=user.balance,
        password=hashed_password,
        pin=hashed_pin,
        mobile_number=user.mobile_number
    )

    # --- Save user to DB ---
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

# --- Get user details by UID ---
@router.get("/{user_id}", response_model=User)
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

# --- Optional: Update user profile partially ---
@router.put("/{user_id}", response_model=User)
def update_user(user_id: str, updates: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # --- Apply updates only for fields provided ---
    if updates.name is not None:
        user.name = updates.name
    if updates.ifsc is not None:
        user.ifsc = updates.ifsc
    if updates.balance is not None:
        user.balance = updates.balance
    if updates.mobile_number is not None:
        user.mobile_number = updates.mobile_number
    if updates.password is not None:
        user.password = hash_secret(updates.password)
    if updates.pin is not None:
        user.pin = hash_secret(updates.pin)

    db.commit()
    db.refresh(user)
    return user
