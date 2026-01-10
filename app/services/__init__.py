# Импортируем все сервисы для удобного доступа
from app.services.user_service import UserService
from app.services.post_service import PostService
from app.services.feed_service import FeedService
from app.services.subscription_service import SubscriptionService
from app.services.cache_service import CacheService

__all__ = [
    "UserService",
    "PostService", 
    "FeedService",
    "SubscriptionService",
    "CacheService",
]
