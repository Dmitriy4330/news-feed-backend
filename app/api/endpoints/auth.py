from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserLogin, TokenWithUser, UserResponse
from app.services.user_service import UserService
from app.api.dependencies import get_user_service

router = APIRouter(prefix="/auth", tags=["Аутентификация"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Регистрация нового пользователя"""
    try:
        user = user_service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=TokenWithUser)
async def login(
    login_data: UserLogin,
    user_service: UserService = Depends(get_user_service)
):
    """Вход в систему"""
    user = user_service.authenticate_user(login_data.email, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )
    
    # Создаём токен
    token = user_service.create_access_token_for_user(user)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }
