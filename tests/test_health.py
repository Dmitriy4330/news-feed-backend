import pytest
from httpx import AsyncClient
import sys
import os
from app.main import app
# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем только если нужно, но пока простой тест
def test_simple():
    """Простой тест для CI"""
    assert 1 + 1 == 2

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert "status" in response.json()