from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from datetime import datetime
import uuid
from app.services.post_service import PostService
from app.services.subscription_service import SubscriptionService
from app.services.cache_service import CacheService
from app.models.post import Post

class FeedService:
    def __init__(self, db: Session):
        self.db = db
        self.post_service = PostService(db)
        self.subscription_service = SubscriptionService(db)
        self.cache_service = CacheService()
    
    def generate_feed(
        self, 
        user_id: uuid.UUID, 
        limit: int = 20, 
        cursor: Optional[datetime] = None
    ) -> Tuple[List[Post], Optional[datetime]]:
        """Сгенерировать ленту для пользователя"""
        
        # Проверяем кеш
        cache_key = f"{user_id}:{cursor.isoformat() if cursor else 'first'}"
        cached = self.cache_service.get_cached_feed(cache_key)
        
        if cached:
            print(f"Используем кешированную ленту для пользователя {user_id}")
            # В реальном приложении здесь нужно десериализовать посты
            # Для простоты возвращаем пустой список
            return [], None
        
        # Получаем подписки пользователя
        subscription_ids = self.subscription_service.get_subscription_ids(user_id)
        
        if not subscription_ids:
            return [], None
        
        # Получаем посты от авторов, на которых подписан пользователь
        posts = self.post_service.get_posts_by_user_ids(
            user_ids=subscription_ids,
            limit=limit,
            cursor=cursor
        )
        
        # Определяем курсор для следующей страницы
        next_cursor = posts[-1].created_at if posts else None
        
        # Кешируем результат
        # В реальном приложении нужно сериализовать посты
        self.cache_service.cache_feed(cache_key, [])  # 5 минут
        
        return posts, next_cursor
    
    def add_post_to_feeds(self, post: Post) -> None:
        """Добавить пост в ленты подписчиков"""
        # В реальном приложении здесь:
        # 1. Получаем всех подписчиков автора
        # 2. Добавляем пост в их кешированные ленты
        # 3. Инвалидируем кеш или добавляем пост в начало
        
        # Для простоты просто инвалидируем кеш всех подписчиков
        subscription_service = SubscriptionService(self.db)
        subscribers = subscription_service.get_subscribers(post.user_id)
        
        for subscriber in subscribers:
            self.cache_service.invalidate_feed_cache(str(subscriber.subscriber_id))
    
    def invalidate_user_feed(self, user_id: uuid.UUID) -> None:
        """Инвалидировать кеш ленты пользователя"""
        self.cache_service.invalidate_feed_cache(str(user_id))
