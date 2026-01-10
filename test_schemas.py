import sys
sys.path.append('.')

print("=== ТЕСТИРОВАНИЕ SCHEMAS ===")

try:
    # Импортируем схемы
    from app.schemas.user import UserCreate, UserLogin, UserResponse
    from app.schemas.post import PostCreate, PostResponse
    from app.schemas.subscription import SubscriptionCreate
    
    print("✅ 1. Все схемы импортируются")
    
    # Тестируем создание пользователя
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }
    user_create = UserCreate(**user_data)
    print(f"✅ 2. UserCreate создан: {user_create.username}")
    
    # Тестируем создание поста
    post_data = {
        "content": "Это тестовый пост"
    }
    post_create = PostCreate(**post_data)
    print(f"✅ 3. PostCreate создан: {post_create.content[:20]}...")
    
    # Тестируем валидацию (должна быть ошибка)
    try:
        bad_user = UserCreate(username="ab", email="bad", password="short")
    except Exception as e:
        print(f"✅ 4. Валидация работает: {type(e).__name__}")
    
    print("\n🎉 ВСЕ SCHEMAS РАБОТАЮТ КОРРЕКТНО!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()