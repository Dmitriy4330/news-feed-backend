from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.core.database import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.post import PostResponse
from app.api.dependencies import get_current_user, get_user_service, get_post_service
from app.services.user_service import UserService
from app.services.post_service import PostService

router = APIRouter(prefix="/users", tags=["Пользователи"])

@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    current_user_id: uuid.UUID = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Получение профиля текущего пользователя"""
    user = user_service.get_user_by_id(current_user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    return user

@router.put("/me", response_model=UserResponse)
async def update_my_profile(
    update_data: UserUpdate,
    current_user_id: uuid.UUID = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Обновление профиля текущего пользователя"""
    user = user_service.update_user(current_user_id, update_data)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    return user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_profile(
    user_id: uuid.UUID,
    user_service: UserService = Depends(get_user_service)
):
    """Получение профиля пользователя по ID"""
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    return user

@router.get("/{user_id}/posts", response_model=List[PostResponse])
async def get_user_posts(
    user_id: uuid.UUID,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    post_service: PostService = Depends(get_post_service)
):
    """Получение постов пользователя"""
    posts = post_service.get_user_posts(user_id, limit, offset)
    return posts
