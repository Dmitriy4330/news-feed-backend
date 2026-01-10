from pydantic import BaseModel
from datetime import datetime
import uuid

# Схема для создания подписки
class SubscriptionCreate(BaseModel):
    author_id: uuid.UUID

# Схема для ответа с подпиской
class SubscriptionResponse(BaseModel):
    subscriber_id: uuid.UUID
    author_id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

# Схема для списка подписок
class SubscriptionsList(BaseModel):
    subscriptions: list[SubscriptionResponse]
    total: int
