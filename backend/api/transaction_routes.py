# --- FastAPI imports for routing and dependency injection ---
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from hashlib import sha256                     # For generating unique transaction IDs
from datetime import datetime                  # To generate timestamp for each transaction

# --- Local imports (relative paths) ---
from ..database.database import get_db         # Dependency to get DB session
from ..models.transaction_model import TransactionModel  # SQLAlchemy ORM model
from ..schemas.transaction_schema import TransactionCreate, Transaction  # Pydantic schemas

# --- Initialize API router with prefix and tags for grouping in docs ---
router = APIRouter(
    prefix="/transactions",                    # All routes will be under this prefix
    tags=["Transactions"]                      # Group label in Swagger UI
)

# --- Utility function to generate a SHA256-based unique transaction ID ---
def generate_transaction_id(uid: str, mid: str, amount: float, timestamp: datetime) -> str:
    seed = f"{uid}{mid}{amount}{timestamp.timestamp()}"     # Combine core transaction fields
    return sha256(seed.encode()).hexdigest()[:16]            # Return first 16 hex chars

# --- Route to create a new transaction ---
@router.post("/", response_model=Transaction)
def create_transaction(
    transaction: TransactionCreate,                        # Incoming validated request data
    db: Session = Depends(get_db)                          # DB session injected via dependency
):
    now = datetime.now()                                   # Generate current timestamp
    tid = generate_transaction_id(                         # Generate transaction ID
        transaction.uid,
        transaction.mid,
        transaction.amount,
        now
    )

    # --- Check for rare collision of transaction ID ---
    existing = db.query(TransactionModel).filter(TransactionModel.id == tid).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Transaction ID conflict. Try again."
        )

    # --- Construct a TransactionModel instance with the data ---
    db_transaction = TransactionModel(
        id=tid,
        uid=transaction.uid,
        mid=transaction.mid,
        amount=transaction.amount,
        timestamp=now
    )

    # --- Add transaction to database and persist ---
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)   # Refresh to return updated DB object

    return db_transaction        # Response will match the Transaction Pydantic schema

# --- Route to fetch all transactions ---
@router.get("/", response_model=list[Transaction])
def get_all_transactions(db: Session = Depends(get_db)):
    transactions = db.query(TransactionModel).all()         # Fetch all rows from DB
    return transactions                                     # Return list of transactions

# --- Route to fetch a single transaction by its ID ---
@router.get("/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: str, db: Session = Depends(get_db)):
    transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )
    return transaction
