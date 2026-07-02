from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import crud
from app.db.db import get_db
from app.db.models import Book
from app.schemas import BookCreate, BookResponse, BookUpdate

# Инициализируем роутер с базовым префиксом и тегом для документации Swagger
router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_new_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Создать новую книгу.
    Валидация: Проверяет, существует ли указанный category_id в базе данных.
    """
    # Бизнес-логика: проверка существования категории
    if not crud.get_category_by_id(db, book.category_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with ID {book.category_id} does not exist. Cannot create book."
        )
    return crud.create_book(
        db=db, title=book.title, price=book.price, 
        category_id=book.category_id, description=book.description, url=book.url
    )


@router.get("/", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
def read_books(
    category_id: Optional[int] = Query(None, description="Фильтр книг по ID категории"),
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Получить список всех книг.
    Поддерживает пагинацию и фильтрацию через query-параметр: `/books?category_id=1`.
    """
    query = db.query(Book)
    if category_id is not None:
        query = query.filter(Book.category_id == category_id)
    return query.offset(skip).limit(limit).all()


@router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
def read_book_by_id(book_id: int, db: Session = Depends(get_db)):
    """
    Получить конкретную книгу по её ID.
    Если книга не найдена — возвращает ошибку 404 Not Found.
    """
    db_book = crud.get_book_by_id(db=db, book_id=book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    return db_book


@router.put("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
def update_book_fields(book_id: int, book_data: BookUpdate, db: Session = Depends(get_db)):
    """
    Обновить данные существующей книги (поддерживает частичное обновление).
    Валидация: Если передается новый category_id, проверяется его существование в БД.
    """
    # 1. Проверяем, существует ли сама книга
    if not crud.get_book_by_id(db, book_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )

    # Преобразуем входящие Pydantic-данные в словарь, исключая неуказанные поля
    update_dict = book_data.model_dump(exclude_unset=True)
    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )

    # 2. Бизнес-логика: проверка категории при её изменении
    if "category_id" in update_dict:
        new_cat_id = update_dict["category_id"]
        if not crud.get_category_by_id(db, new_cat_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with ID {new_cat_id} does not exist. Cannot move book."
            )

    # 3. Вызов обновления
    return crud.update_book(db=db, book_id=book_id, **update_dict)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book_by_id(book_id: int, db: Session = Depends(get_db)):
    """
    Удалить книгу по её ID.
    Если книга не найдена — возвращает ошибку 404 Not Found.
    """
    success = crud.delete_book(db=db, book_id=book_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    return None
