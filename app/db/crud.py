from sqlalchemy.orm import Session
from app.db.models import Category, Book

# ==================== CRUD ДЛЯ CATEGORIES ====================

def create_category(db: Session, title: str):
    db_category = Category(title=title)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()

def get_category_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def update_category(db: Session, category_id: int, new_title: str):
    db_category = get_category_by_id(db, category_id)
    if db_category:
        db_category.title = new_title
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = get_category_by_id(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False


# ==================== CRUD ДЛЯ BOOKS ====================

def create_book(db: Session, title: str, price: float, category_id: int, description: str = None, url: str = None):
    db_book = Book(
        title=title, 
        description=description, 
        price=price, 
        url=url, 
        category_id=category_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Book).offset(skip).limit(limit).all()

def get_book_by_id(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def update_book(db: Session, book_id: int, **kwargs):
    """
    Принимает именованные аргументы для обновления полей книги.
    Пример: update_book(db, 1, price=599.00, description="Новое описание")
    """
    db_book = get_book_by_id(db, book_id)
    if db_book:
        for key, value in kwargs.items():
            if hasattr(db_book, key):
                setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = get_book_by_id(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    return False
