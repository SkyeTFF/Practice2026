from app.db.db import SessionLocal
from app.db.crud import get_categories, get_books

def main():
    db = SessionLocal()
    try:
        print("\n=== СПИСОК КАТЕГОРИЙ ===")
        categories = get_categories(db)
        for cat in categories:
            print(f"ID: {cat.id} | Название: {cat.title}")

        print("\n=== СПИСОК КНИГ ===")
        books = get_books(db)
        for book in books:
            print(f"ID: {book.id} | Название: '{book.title}' | Цена: {book.price} руб. | Категория ID: {book.category_id}")
            if book.description:
                print(f"   Описание: {book.description}")
            print("-" * 40)

    finally:
        db.close()

if __name__ == "__main__":
    main()
