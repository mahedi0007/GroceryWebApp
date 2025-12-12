# backend/main.py
from fastapi import FastAPI  , Request , Form , Depends  , HTTPException
from fastapi.responses import HTMLResponse , RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .auth import router as auth_router
from fastapi.templating import Jinja2Templates 
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from . import crud
from .database import get_db
from sqlalchemy.orm import Session 
from typing import Optional 
from . import schemas



# Create DB tables
models.Base.metadata.create_all(bind=engine)

path = Path(__file__).resolve().parent 

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
def login(request: Request ):
    context = {"request": request, "title": "Login - GroceryApp", "message": "Hello from Jinja2!"}

    return templates.TemplateResponse("login.html", context)

@app.get("/register")
async def reg_user(request : Request ):
    context = {"request": request, "title": "Register - GroceryApp"}
    return templates.TemplateResponse("register.html", context)

@app.get("/profile", response_class=HTMLResponse)
def profile(request: Request ):
    context = {"request": request, "title": "Profile - GroceryApp"}

    return templates.TemplateResponse("profile.html", context)
 
@app.get("/index", response_class=HTMLResponse)
async def home(request : Request ):
    category_db= crud.get_categories(  next(get_db()) )
    category_db_list =[
        {
            "category_name":category.name
        } for category in category_db
    ]
    
    context = {"request": request, "title": "Home - GroceryApp"}
    return templates.TemplateResponse("index.html", context | {"category_db": category_db_list} )
#peoduct listing route
@app.get("/products", response_class=HTMLResponse)
async def products(request : Request ):
    category_db= crud.get_categories(  next(get_db()) )
    category_db_list_p =[
        {
            "category_name":category.name
        } for category in category_db
    ]
    context = {"request": request, "title": "Products - GroceryApp"}
    return templates.TemplateResponse("products.html", context  | {"category_db": category_db_list_p} )
#products api route
@app.get("/api/products")
async def get_products_api(db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return products

@app.get("/cart", response_class=HTMLResponse)
async def cart(request : Request ):
    context = {"request": request, "title": "Cart - GroceryApp"}
    return templates.TemplateResponse("cart.html", context)

@app.get("/checkout", response_class=HTMLResponse)
async def checkout(request: Request):
    context = {"request" :request, "title" :"checkout - GroceryApp"}
    return templates.TemplateResponse("checkout.html", context)

#admins side routes
#admin dashboard route

@app.get("/admin", response_class=HTMLResponse)
async def main_products(request: Request, db: Session = Depends(get_db)):
    products = crud.get_products(db)
    category = crud.get_categories(db)
    
    product_db = [
        {
            "request": request,
            "product_id": product.id, 
            "product_name": product.name,
            "product_description": product.description,
            "is_available": product.is_available,
            "product_category": product.category.name if product.category else "Uncategorized",
            "product_price": product.price,
            "product_quantity": product.quantity
        } for product in products
    ]

    category_db =[
        {
            "category_id": category.id,
            "category_name": category.name
        } for category in category
    ]
    
    
    return templates.TemplateResponse("admin/index.html" ,{"request": request, "products": product_db , "category_db": category_db})


@app.get("/admin/products", response_class=HTMLResponse)
async def add_products(request: Request):
    return templates.TemplateResponse("admin/addProducts.html", {"request": request})


# Fallback endpoint to accept form submissions (non-JS clients)
@app.post("/admin/products")
async def add_product_form(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    quantity: int = Form(...),
    is_available: bool = Form(False),
    image_url: Optional[str] = Form(None),
    category_id: Optional[int] = Form(None),
    db: Session = Depends(get_db),
):
    try:
        product_in = schemas.ProductCreate(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            is_available=is_available,
            image_url=image_url,
            category_id=category_id,
        )
        crud.create_product(db, product_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return RedirectResponse(url="/admin", status_code=303)

#delete product endpoint
@app.get("/admin/products/delete/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_product(db, product_id)
    if deleted: 
        return RedirectResponse(url="/admin", status_code=303)
    elif not deleted:
          return {"products are not deleted!"}
    else:
          raise HTTPException(status_code=404, detail="products not found")


# create categories form endpoint
@app.get("/admin/createCategories", response_class=HTMLResponse)
async def create_categories(request: Request , db :Session = Depends(get_db)):
    category = crud.get_categories(db)

    category_db =[
        {
            "category_id": category.id,
            "category_name": category.name
        } for category in category
    ]

    return templates.TemplateResponse("admin/createCategories.html", {"request": request , "category_db": category_db})

@app.post("/admin/categories/add")
async def add_category_form(
    category_name: str = Form(...),
    db: Session = Depends(get_db),
):
    name = category_name.strip()

    # Empty name
    if not name:
        return RedirectResponse(
            url="/admin/categories?error=Category name is required",
            status_code=303
        )

    # Duplicate category
    existing_category = db.query(models.Category).filter(models.Category.name == name).first()
    if existing_category:
        return RedirectResponse(
            url="/admin/categories?error=Category already exists",
            status_code=303
        )

    # Create new category
    try:
        new_category = models.Category(name=name)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
    except Exception as e:
        return RedirectResponse(
            url=f"/admin/categories?error=Failed to create category",
            status_code=303
        )

    # Success
    return RedirectResponse(
        url="/admin/categories?success=1",
        status_code=303
    )

#creating a delete category endpoint
@app.get("/admin/categories/delete/{category_id}")
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_category(db, category_id)
    if deleted: 
        return RedirectResponse(url="/admin/createCategories", status_code=303)
    elif not deleted:
        return {"category are not deleted!"}
    else:
        raise HTTPException(status_code=404, detail="Category not found")

