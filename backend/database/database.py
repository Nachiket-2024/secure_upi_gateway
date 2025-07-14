# --- SQLAlchemy imports for DB connection, ORM base, and session handling ---
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- OS and dotenv for environment variable management ---
import os
from dotenv import load_dotenv

# --- Load environment variables from a .env file into the environment ---
load_dotenv()

# --- Get the PostgreSQL database URL from the .env file ---
# Format: postgresql://username:password@hostname:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL")

# --- Create the SQLAlchemy engine using the database URL ---
engine = create_engine(DATABASE_URL)

# --- Create a configured "SessionLocal" class for handling DB sessions ---
# autocommit=False: prevents automatic commits
# autoflush=False: disables automatic flush of changes
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Define a common base class for all ORM models ---
# This base will be inherited by all models (e.g., MerchantModel, TransactionModel)
Base = declarative_base()

# --- Dependency to provide a SQLAlchemy DB session to FastAPI route handlers ---
# This function is used with Depends() to inject a scoped session per request
def get_db():
    db = SessionLocal()     # Create a new DB session
    try:
        yield db            # Provide the session to the route
    finally:
        db.close()          # Always close the session after the request is done
