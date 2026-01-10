from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from app.core.config import settings

# ВРЕМЕННОЕ РЕШЕНИЕ для тестирования - без bcrypt
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ВРЕМЕННАЯ проверка пароля - прямое сравнение"""
    # ВНИМАНИЕ: Это только для тестирования API! 
    # В реальном проекте нужно использовать bcrypt или argon2
    return plain_password == hashed_password

def get_password_hash(password: str) -> str:
    """ВРЕМЕННОЕ хеширование пароля - возвращает как есть"""
    # ВНИМАНИЕ: Это только для тестирования API!
    # В реальном проекте пароли должны быть захешированы
    return password  # Просто возвращаем пароль как есть

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создает JWT токен"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt