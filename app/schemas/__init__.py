# Импортируем все схемы для удобного доступа
from app.schemas.user import (
    UserBase, UserCreate, UserUpdate, UserResponse, 
    UserLogin, Token, TokenWithUser
)
from app.schemas.post import (
    PostBase, PostCreate, PostUpdate, PostResponse,
    UserInPost, FeedResponse
)
from app.schemas.subscription import (
    SubscriptionCreate, SubscriptionResponse, SubscriptionsList
)

__all__ = [
    # User schemas
    "UserBase", "UserCreate", "UserUpdate", "UserResponse",
    "UserLogin", "Token", "TokenWithUser",
    
    # Post schemas
    "PostBase", "PostCreate", "PostUpdate", "PostResponse",
    "UserInPost", "FeedResponse",
    
    # Subscription schemas
    "SubscriptionCreate", "SubscriptionResponse", "SubscriptionsList",
]
