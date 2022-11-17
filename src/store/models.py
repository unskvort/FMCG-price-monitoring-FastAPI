from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)


class Product(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    article: int = Field(unique=True)
    name: str
    category: int = Field(default=None, foreign_key="category.id")
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
    price: int


class PriceRecord(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    product: int = Field(default=None, foreign_key="product.id")
    price: int
    updated_at: Optional[datetime] = datetime.now()
