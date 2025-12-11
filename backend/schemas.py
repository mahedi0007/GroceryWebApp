# backend/schemas.py
from pydantic import BaseModel, EmailStr , ConfigDict
from typing import Optional



class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
       # orm_mode = True
       from_attributes=True

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)



class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    is_available: Optional[bool] = True
    image_url: Optional[str] = None
    category_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    is_available: Optional[bool] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None

class ProductResponse(ProductBase):
    id: int
    category: Optional[CategoryResponse] = None
    model_config = ConfigDict(from_attributes=True)