from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import crud
from app.db.db import get_db
from app.schemas import CategoryCreate, CategoryResponse, CategoryUpdate

# Инициализируем роутер с базовым префиксом и тегом для документации Swagger
router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """
    Создать новую категорию товаров.
    Возвращает код 201 Created при успешном создании.
    """
    return crud.create_category(db=db, title=category.title)


@router.get("/", response_model=List[CategoryResponse], status_code=status.HTTP_200_OK)
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список всех категорий с поддержкой пагинации (skip, limit).
    """
    return crud.get_categories(db=db, skip=skip, limit=limit)


@router.get("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def read_category_by_id(category_id: int, db: Session = Depends(get_db)):
    """
    Получить конкретную категорию по её ID.
    Если категория не найдена — возвращает ошибку 404 Not Found.
    """
    db_category = crud.get_category_by_id(db=db, category_id=category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Category with ID {category_id} not found"
        )
    return db_category


@router.put("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def update_category_title(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    """
    Обновить название существующей категории.
    Если категория не найдена — возвращает ошибку 404 Not Found.
    """
    updated_cat = crud.update_category(db=db, category_id=category_id, new_title=category.title)
    if not updated_cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Category with ID {category_id} not found"
        )
    return updated_cat


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category_by_id(category_id: int, db: Session = Depends(get_db)):
    """
    Удалить категорию по её ID.
    При успешном удалении возвращает код 204 No Content (тело ответа пустое).
    Если категория не найдена — возвращает ошибку 404 Not Found.
    """
    success = crud.delete_category(db=db, category_id=category_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Category with ID {category_id} not found"
        )
    return None
