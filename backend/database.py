# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

#user side database configuration
# Example: mysql+pymysql://username:password@localhost:3306/grocerydb
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:toor@localhost:3306/groceryApp")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#admin side database configuration
