import pytest
import os

# Устанавливаем переменные окружения для тестов
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/newsfeed_test"
os.environ["REDIS_URL"] = "redis://localhost:6379"
os.environ["SECRET_KEY"] = "test-secret-key-for-ci"