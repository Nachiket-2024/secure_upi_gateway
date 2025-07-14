# --- FastAPI and dependencies ---
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from hashlib import sha256

# --- Local imports ---
from ..database.database import get_db
from ..models.block_model import BlockModel
from ..schemas.block_schema import Block

router = APIRouter(prefix="/blockchain", tags=["Blockchain"])

# --- Get entire blockchain ---
@router.get("/", response_model=list[Block])
def get_full_blockchain(db: Session = Depends(get_db)):
    blocks = db.query(BlockModel).order_by(BlockModel.timestamp).all()
    return blocks

# --- Validate blockchain integrity ---
@router.get("/validate")
def validate_blockchain(db: Session = Depends(get_db)):
    blocks = db.query(BlockModel).order_by(BlockModel.timestamp).all()

    if not blocks:
        return {"valid": True, "message": "Blockchain is empty"}

    for i in range(1, len(blocks)):
        prev = blocks[i - 1]
        curr = blocks[i]

        # Recalculate expected hash of current block
        expected_hash = sha256(
            f"{curr.transaction_id}{prev.id}{curr.timestamp.timestamp()}".encode()
        ).hexdigest()

        if curr.id != expected_hash:
            return {
                "valid": False,
                "message": f"Tampering detected at block {i} (ID: {curr.id})"
            }

    return {"valid": True, "message": "Blockchain is valid and untampered"}
