# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .auth import router as auth_router

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="GroceryApp Backend")

# Allow frontend (adjust origin if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "GroceryApp API running"}
