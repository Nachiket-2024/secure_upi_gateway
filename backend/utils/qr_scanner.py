# --- QR code scanner using pyzbar and OpenCV ---
from pyzbar.pyzbar import decode
from PIL import Image
from encryption.lwc_speck import decrypt_speck

# --- Function to decode QR image and decrypt the MID ---
def scan_qr_and_decrypt(image: Image.Image) -> str:
    decoded_data = decode(image)  # Scan QR for any barcodes/QR codes
    if not decoded_data:
        raise ValueError("No QR code detected in the image.")

    # Assume the first detected QR is valid
    encrypted_mid = decoded_data[0].data.decode("utf-8")
    mid = decrypt_speck(encrypted_mid)  # Decrypt using SPECK logic
    return mid
