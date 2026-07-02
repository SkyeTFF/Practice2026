from pydantic import BaseModel, Field
from typing import Optional

# ==================== СХЕМЫ ДЛЯ КАТЕГОРИЙ (CATEGORIES) ====================

class CategoryBase(BaseModel):
    """Базовая схема категории (общие поля)"""
    title: str = Field(..., max_length=100, description="Название категории")

class CategoryCreate(CategoryBase):
    """Схема для создания новой категории"""
    pass

class CategoryUpdate(CategoryBase):
    """Схема для обновления категории"""
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        # Для Pydantic v2 (современный стандарт)
        from_attributes = True  
        # Для обратной совместимости с Pydantic v1
        orm_mode = True


# ==================== СХЕМЫ ДЛЯ КНИГ (BOOKS) ====================

class BookBase(BaseModel):
    """Базовая схема книги (общие поля)"""
    title: str = Field(..., max_length=255, description="Название книги")
    description: Optional[str] = Field(None, description="Описание книги")
    price: float = Field(..., gt=0, description="Цена книги (должна быть строго больше 0)")
    url: Optional[str] = Field(None, description="Ссылка на товар")

class BookCreate(BookBase):
    """Схема для создания книги (требует привязку к категории)"""
    category_id: int = Field(..., description="ID категории, к которой относится книга")

class BookUpdate(BaseModel):
    """Схема для частичного обновления книги (все поля опциональны)"""
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    url: Optional[str] = None
    category_id: Optional[int] = None

class BookResponse(BookBase):
    id: int
    category_id: int

    class Config:
        # Для Pydantic v2 (современный стандарт)
        from_attributes = True  
        # Для обратной совместимости с Pydantic v1
        orm_mode = True  
