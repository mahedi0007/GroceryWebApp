from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models
from . import schemas

# Category CRUD
def create_category(db: Session, category: schemas.CategoryCreate):
    existing = db.query(models.Category).filter(models.Category.name == category.name).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session):
    return db.query(models.Category).all()

# crud.py
def delete_category(db: Session, category_id: int):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()
        return True
    return False



# Product CRUD
def create_product(db: Session, product: schemas.ProductCreate):
    data = product.dict()
    category_id = data.get("category_id")
    if category_id is not None:
        # ensure the referenced category exists to avoid FK integrity errors
        category = db.query(models.Category).filter(models.Category.id == category_id).first()
        if not category:
            raise ValueError(f"Category with id={category_id} does not exist")

    db_product = models.Product(**data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session):
    return db.query(models.Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        return None
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False
