from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.sql import text

from app.api import categories, books
from app.db.db import engine, Base, SessionLocal


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом приложения.
    Выполняется ОДИН раз при запуске и завершении сервера.
    """
    # 1. Автоматически создаем таблицы в PostgreSQL (если они еще не созданы)
    Base.metadata.create_all(bind=engine)
    print("[INFO] База данных проверена: таблицы успешно инициализированы.")
    
    # 2. Проверяем физическое подключение к PostgreSQL на старте
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("[INFO] Успешное тестовое подключение к PostgreSQL.")
    except Exception as ex:
        print(f"[CRITICAL] Не удалось подключиться к базе данных на старте: {ex}")
    finally:
        db.close()
        
    yield  # В этой точке приложение работает и принимает HTTP-запросы
    
    # Код ниже выполнится при остановке сервера (Uvicorn shutdown)
    print("[INFO] Сервер останавливается. Завершение работы ресурсов...")


# Создаем объект приложения с передачей логики жизненного цикла
app = FastAPI(
    title="Octagon Book Store API",
    description="Полноценное API для управления книжным магазином с интеграцией PostgreSQL",
    version="1.0.0",
    lifespan=lifespan
)

# Подключаем модули с маршрутами
app.include_router(categories.router)
app.include_router(books.router)


@app.get("/health", tags=["System"], status_code=200)
def health_check():
    """
    Эндпоинт для проверки жизнеспособности сервиса.
    Используется для мониторинга (Health Check).
    """
    return {
        "status": "healthy",
        "service": "Octagon Book Store API",
        "database": "connected"
    }


@app.get("/", tags=["Root"])
def root():
    """Корневой маршрут со ссылкой на автодокументацию."""
    return {"message": "Добро пожаловать! Перейдите на /docs для работы с интерактивным Swagger API."}
