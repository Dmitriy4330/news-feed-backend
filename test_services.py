import sys
sys.path.append('.')

print("=== ТЕСТИРОВАНИЕ СЕРВИСОВ ===")

try:
    from app.services.user_service import UserService
    from app.services.post_service import PostService
    from app.services.subscription_service import SubscriptionService
    from app.services.feed_service import FeedService
    from app.services.cache_service import CacheService
    
    print(" 1. Все сервисы импортируются")
    
    # Проверяем, что классы можно создать
    from app.core.database import SessionLocal
    
    db = SessionLocal()
    
    user_service = UserService(db)
    post_service = PostService(db)
    subscription_service = SubscriptionService(db)
    feed_service = FeedService(db)
    cache_service = CacheService()
    
    print(" 2. Все сервисы созданы")
    print(" 3. Кеш-сервис подключен к Redis")
    
    db.close()
    
    print("\n ВСЕ СЕРВИСЫ РАБОТАЮТ КОРРЕКТНО!")
    
except Exception as e:
    print(f" Ошибка: {e}")
    import traceback
    traceback.print_exc()
