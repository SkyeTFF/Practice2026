from app.db.db import engine, Base, SessionLocal
from app.db.crud import create_category, create_book

def init_database():
    # 1. Создаем таблицы в БД (если они еще не созданы)
    Base.metadata.create_all(bind=engine)
    print("[INFO] Таблицы успешно созданы в базе данных.")

    # 2. Открываем сессию для работы с данными
    db = SessionLocal()
    try:
        # 3. Создаем категории
        cat_fiction = create_category(db, title="Фантастика")
        cat_science = create_category(db, title="Наука и IT")
        print("[INFO] Категории успешно добавлены.")

        # 4. Добавляем книги для категории "Фантастика"
        create_book(db, title="Дюна", price=850.00, category_id=cat_fiction.id, description="Легендарный роман Фрэнка Герберта.")
        create_book(db, title="Основание", price=720.50, category_id=cat_fiction.id, description="Классика от Айзека Азимова.")
        create_book(db, title="Автостопом по галактике", price=540.00, category_id=cat_fiction.id, description="Юмористическая фантастика.")

        # 5. Добавляем книги для категории "Наука и IT"
        create_book(db, title="Изучаем Python", price=2500.00, category_id=cat_science.id, description="Подробное руководство Марка Лутца.")
        create_book(db, title="Чистый код", price=1200.00, category_id=cat_science.id, description="Бестселлер Роберта Мартина.")
        print("[INFO] Книги успешно добавлены.")

    except Exception as ex:
        print(f"[ERROR] Произошла ошибка при наполнении БД: {ex}")
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
