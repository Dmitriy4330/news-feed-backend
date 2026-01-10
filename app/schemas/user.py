from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

# Базовые схемы - используем простой str для email
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5, max_length=100)

# Схема для создания пользователя (регистрация)
class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

# Схема для обновления пользователя
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[str] = Field(None, min_length=5, max_length=100)

# Схема для ответа (без пароля)
class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Схема для аутентификации
class UserLogin(BaseModel):
    email: str = Field(..., min_length=5, max_length=100)
    password: str

# Схема для токена
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Схема для токена с данными пользователя
class TokenWithUser(Token):
    user: UserResponse
