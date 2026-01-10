from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.services.user_service import UserService
import uuid

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> uuid.UUID:
    """Получение текущего пользователя из JWT токена"""
    token = credentials.credentials
    
    try:
        # Декодируем токен
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный токен"
            )
        
        return uuid.UUID(user_id)
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен"
        )
    
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный формат ID пользователя"
        )

def get_user_service(db: Session = Depends(get_db)):
    """Зависимость для UserService"""
    return UserService(db)

def get_post_service(db: Session = Depends(get_db)):
    """Зависимость для PostService"""
    from app.services.post_service import PostService
    return PostService(db)

def get_feed_service(db: Session = Depends(get_db)):
    """Зависимость для FeedService"""
    from app.services.feed_service import FeedService
    return FeedService(db)

def get_subscription_service(db: Session = Depends(get_db)):
    """Зависимость для SubscriptionService"""
    from app.services.subscription_service import SubscriptionService
    return SubscriptionService(db)
