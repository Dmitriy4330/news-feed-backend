from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

# Базовые схемы
class PostBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)

# Схема для создания поста
class PostCreate(PostBase):
    pass

# Схема для обновления поста
class PostUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=5000)

# Схема пользователя в посте (сокращённая)
class UserInPost(BaseModel):
    id: uuid.UUID
    username: str
    
    class Config:
        from_attributes = True

# Схема для ответа с постом
class PostResponse(PostBase):
    id: uuid.UUID
    user_id: uuid.UUID
    user: UserInPost
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Схема для ленты
class FeedResponse(BaseModel):
    posts: List[PostResponse]
    next_cursor: Optional[datetime] = None
    has_more: bool
