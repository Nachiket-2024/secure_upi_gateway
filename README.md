# Centralized UPI Payment Gateway Backend

This is the backend implementation of a Centralized UPI Payment Gateway system integrating blockchain, lightweight cryptography (SPECK), and quantum cryptography simulations.

## Overview

The backend is built with FastAPI and PostgreSQL, providing REST APIs for:

- Merchant management  
- User accounts and authentication  
- Transaction processing with UPI logic  
- QR code scanning and decryption  
- Blockchain-based transaction recording  
- Lightweight cryptography for data encryption/decryption  
- A simulation of Shor's algorithm (quantum cryptography) kept separate  

## Tech Stack (Backend)

- Python 3.10+  
- FastAPI  
- SQLAlchemy ORM  
- PostgreSQL  
- SPECK Lightweight Cryptography  
- SHA256 hashing  

## Getting Started

1. Create a `.env` file in the root with your PostgreSQL connection string, e.g.:  
   `DATABASE_URL=postgresql://username:password@localhost:5432/yourdb`  

2. Install dependencies:  
   `pip install -r requirements.txt`  

3. Run the server locally:  
   `uvicorn main:app --reload`  

4. Access API docs at:  
   [http://localhost:8000/docs](http://localhost:8000/docs)  

## Notes

- The Shor's algorithm quantum simulation is kept separate for demonstration and is not part of the live API.  
- This backend is under active development and currently supports only core UPI transaction flows.
