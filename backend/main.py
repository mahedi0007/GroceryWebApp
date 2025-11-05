# backend/main.py
from fastapi import FastAPI  , Request 
from fastapi.responses import HTMLResponse 
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .auth import router as auth_router
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="GroceryApp Backend")

templates = Jinja2Templates(directory="backend/templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Allow frontend (adjust origin if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

@app.get("/login", response_class=HTMLResponse)
def login(request: Request):
    context = {"request": request, "title": "Login - GroceryApp", "message": "Hello from Jinja2!"}
    return templates.TemplateResponse("login.html", context)

@app.get("/register")
async def reg_user(request : Request ):
    context = {"request": request, "title": "Register - GroceryApp"}
    return templates.TemplateResponse("register.html", context)
