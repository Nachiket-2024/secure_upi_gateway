# --- FastAPI imports for handling file uploads ---
from fastapi import APIRouter, UploadFile, File, HTTPException

# --- PIL for image handling ---
from PIL import Image

# --- Local utility to decode and decrypt QR ---
from ..utils.qr_scanner import scan_qr_and_decrypt

# --- Define router for UPI machine-related routes ---
router = APIRouter(
    prefix="/upi-machine",
    tags=["UPI Machine"]
)

# --- Endpoint to accept QR image and return decrypted Merchant ID ---
@router.post("/scan-qr/")
async def scan_merchant_qr(file: UploadFile = File(...)):
    try:
        # Load uploaded file as image
        image = Image.open(file.file)

        # Extract encrypted MID and decrypt using SPECK
        merchant_id = scan_qr_and_decrypt(image)

        return {
            "message": "QR code scanned successfully",
            "merchant_id": merchant_id
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
