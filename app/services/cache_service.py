import json
from typing import Optional, Any
import redis
from app.core.config import settings

class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(settings.REDIS_URL)
    
    def get(self, key: str) -> Optional[str]:
        """Получить значение по ключу"""
        value = self.redis_client.get(key)
        return value.decode('utf-8') if value else None
    
    def set(self, key: str, value: str, expire: int = 300) -> bool:
        """Установить значение с TTL (по умолчанию 5 минут)"""
        return self.redis_client.setex(key, expire, value)
    
    def delete(self, key: str) -> bool:
        """Удалить значение по ключу"""
        return bool(self.redis_client.delete(key))
    
    def exists(self, key: str) -> bool:
        """Проверить существование ключа"""
        return bool(self.redis_client.exists(key))
    
    # Методы для работы с JSON
    def get_json(self, key: str) -> Optional[Any]:
        """Получить JSON значение"""
        value = self.get(key)
        return json.loads(value) if value else None
    
    def set_json(self, key: str, value: Any, expire: int = 300) -> bool:
        """Установить JSON значение"""
        return self.set(key, json.dumps(value), expire)
    
    # Специфичные методы для ленты
    def get_feed_cache_key(self, user_id: str, cursor: Optional[str] = None) -> str:
        """Получить ключ кеша для ленты"""
        if cursor:
            return f"feed:{user_id}:{cursor}"
        return f"feed:{user_id}:first"
    
    def cache_feed(self, user_id: str, feed_data: list, cursor: Optional[str] = None) -> bool:
        """Закешировать ленту"""
        key = self.get_feed_cache_key(user_id, cursor)
        return self.set_json(key, feed_data)
    
    def get_cached_feed(self, user_id: str, cursor: Optional[str] = None) -> Optional[list]:
        """Получить закешированную ленту"""
        key = self.get_feed_cache_key(user_id, cursor)
        return self.get_json(key)
    
    def invalidate_feed_cache(self, user_id: str) -> None:
        """Инвалидировать кеш ленты пользователя"""
        # Находим и удаляем все ключи, начинающиеся с feed:{user_id}:
        pattern = f"feed:{user_id}:*"
        keys = self.redis_client.keys(pattern)
        if keys:
            self.redis_client.delete(*keys)
