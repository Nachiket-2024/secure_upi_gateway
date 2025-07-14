# --- Import FastAPI core and route modules ---
from fastapi import FastAPI  # Import FastAPI class to create the application instance

# --- Import routers for various API domains ---
from .api import (  # Import all API route modules from the api package
    merchant_routes,              # Routes for merchant operations
    transaction_routes,           # Routes for handling transactions
    user_routes,                  # Routes for user-related operations
    merchant_qr_routes,           # Routes for generating merchant QR codes
    upi_machine_routes,           # Routes to scan QR codes via machine (camera/image)
    bank_routes,                  # Routes that simulate UPI payment processing
    blockchain_routes             # Routes to fetch and verify blockchain integrity
)

# --- Initialize FastAPI app instance ---
app = FastAPI()  # Create the FastAPI application object

# --- Register all API routers with proper prefixes and tags ---
app.include_router(merchant_routes.router)         # Mount merchant routes at /merchants
app.include_router(transaction_routes.router)      # Mount transaction routes at /transactions
app.include_router(user_routes.router)             # Mount user routes at /users
app.include_router(merchant_qr_routes.router)      # Mount QR generation routes at /merchant-qr
app.include_router(upi_machine_routes.router)      # Mount image-based QR scanning at /upi-machine
app.include_router(bank_routes.router)             # Mount UPI bank processor at /bank
app.include_router(blockchain_routes.router)       # Mount blockchain fetch/verify endpoints at /blockchain
