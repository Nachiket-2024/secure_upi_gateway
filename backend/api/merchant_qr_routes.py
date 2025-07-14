# --- FastAPI and dependencies ---
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

# --- Local utilities ---
from encryption.lwc_speck import encrypt_speck
from utils.qr_generator import generate_qr_code, qr_image_to_base64

# --- Create QR route group ---
router = APIRouter(
    prefix="/merchant-qr",
    tags=["Merchant QR"]
)

# --- Generate QR from given MID ---
@router.get("/{mid}")
def generate_merchant_qr(mid: str):
    try:
        encrypted_mid = encrypt_speck(mid)               # Step 1: Encrypt MID
        qr_img = generate_qr_code(encrypted_mid)         # Step 2: Generate QR image
        base64_img = qr_image_to_base64(qr_img)          # Step 3: Convert to base64

        return JSONResponse(content={
            "mid": mid,
            "encrypted_mid": encrypted_mid,
            "qr_base64_png": base64_img
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
