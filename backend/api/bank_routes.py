# --- FastAPI and dependencies ---
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from hashlib import sha256
from datetime import datetime

# --- Import LWC decryption function ---
from encryption.lwc_speck import decrypt_speck

# --- Database session ---
from ..database.database import get_db

# --- Schema for request validation ---
from ..schemas.transaction_request_schema import TransactionRequest

# --- ORM Models ---
from ..models.user_model import UserModel
from ..models.merchant_model import MerchantModel
from ..models.transaction_model import TransactionModel
from ..models.block_model import BlockModel

# --- Initialize router ---
router = APIRouter(prefix="/bank", tags=["Bank"])

# --- UPI Transaction Processor ---
@router.post("/process-transaction/")
def process_transaction(data: TransactionRequest, db: Session = Depends(get_db)):
    # Step 1: Decrypt the encrypted MID from QR
    try:
        merchant_id = decrypt_speck(data.encrypted_mid)
    except:
        raise HTTPException(status_code=400, detail="Invalid encrypted MID")

    # Step 2: Search for user by MMID (hash of UID + mobile)
    users = db.query(UserModel).all()
    matched_user = None
    for user in users:
        computed_mmid = sha256((user.id + user.mobile_number).encode()).hexdigest()[:16]
        if computed_mmid == data.mmid:
            matched_user = user
            break
    if not matched_user:
        raise HTTPException(status_code=404, detail="User with MMID not found")

    # Step 3: Validate PIN using SHA256 (consider bcrypt for production)
    hashed_pin = sha256(data.pin.encode()).hexdigest()
    if hashed_pin != matched_user.pin:
        raise HTTPException(status_code=401, detail="Invalid PIN")

    # Step 4: Ensure user has enough balance
    if matched_user.balance < data.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # Step 5: Fetch merchant by ID and ensure they exist
    merchant = db.query(MerchantModel).filter(MerchantModel.id == merchant_id).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")

    # Step 6: Deduct amount from user and credit to merchant
    matched_user.balance -= data.amount
    merchant.balance += data.amount

    # Step 7: Generate unique Transaction ID using SHA256
    now = datetime.now()
    tid = sha256(f"{matched_user.id}{merchant.id}{now.timestamp()}".encode()).hexdigest()[:16]

    # --- Step 8: Create and store transaction record ---
    transaction = TransactionModel(
        id=tid,
        uid=matched_user.id,
        mid=merchant.id,
        amount=data.amount,
        timestamp=now
    )

    db.add(transaction)
    db.commit()  # Commit transaction so its ID exists before referencing in blockchain

    # --- Step 9: Create Blockchain Block ---
    # Fetch last block to get previous hash
    last_block = db.query(BlockModel).order_by(BlockModel.timestamp.desc()).first()
    prev_hash = last_block.id if last_block else "0"

    # Generate current block hash
    block_content = f"{tid}{prev_hash}{now.timestamp()}"
    current_hash = sha256(block_content.encode()).hexdigest()

    # Create block record
    block = BlockModel(
        id=current_hash,
        transaction_id=tid,
        prev_hash=prev_hash
    )

    db.add(block)
    db.commit()  # Commit block separately

    return {
        "message": "Transaction successful",
        "transaction_id": tid,
        "from_user": matched_user.id,
        "to_merchant": merchant.id,
        "amount": data.amount
    }
