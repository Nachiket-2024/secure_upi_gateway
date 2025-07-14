# --- QR code generator using qrcode and Pillow ---
import qrcode
from PIL import Image
import io
import base64

# --- Generate QR code from a given encrypted string (usually encrypted MID) ---
def generate_qr_code(data: str) -> Image.Image:
    qr = qrcode.QRCode(
        version=1,                # QR version (1 = 21x21)
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,              # Size of each box
        border=4                  # Border width
    )
    qr.add_data(data)            # Add encrypted data
    qr.make(fit=True)            # Fit to size

    img = qr.make_image(fill_color="black", back_color="white")
    return img                   # Returns PIL image object

# --- Convert PIL image to base64 string (to return in API response) ---
def qr_image_to_base64(img: Image.Image) -> str:
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_base64            # Safe to embed in JSON response
