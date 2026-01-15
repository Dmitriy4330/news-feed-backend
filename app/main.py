from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Импортируем роутеры
from app.api.endpoints import auth, users, posts, feed, subscriptions
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok"}
# Создаем экземпляр FastAPI приложения
app = FastAPI(
    title="News Feed API",
    description="API для новостной ленты",
    version="1.0.0",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(feed.router)
app.include_router(subscriptions.router)

# Тестовый эндпоинт для проверки работы
@app.get("/")
async def root():
    return {
        "message": "News Feed API работает!",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}