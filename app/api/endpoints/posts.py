from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
import uuid
from app.core.database import get_db
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.api.dependencies import get_current_user, get_post_service, get_feed_service
from app.services.post_service import PostService
from app.services.feed_service import FeedService

router = APIRouter(prefix="/posts", tags=["Посты"])

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    current_user_id: uuid.UUID = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service),
    feed_service: FeedService = Depends(get_feed_service)
):
    """Создание нового поста"""
    post = post_service.create_post(current_user_id, post_data)
    
    # Добавляем пост в ленты подписчиков
    feed_service.add_post_to_feeds(post)
    
    return post

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: uuid.UUID = Path(...),
    post_service: PostService = Depends(get_post_service)
):
    """Получение поста по ID"""
    post = post_service.get_post_by_id(post_id)
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден"
        )
    
    return post

@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: uuid.UUID = Path(...),
    update_data: PostUpdate = None,
    current_user_id: uuid.UUID = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service)
):
    """Обновление поста"""
    post = post_service.update_post(post_id, current_user_id, update_data)
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден или у вас нет прав на его изменение"
        )
    
    return post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: uuid.UUID = Path(...),
    current_user_id: uuid.UUID = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service),
    feed_service: FeedService = Depends(get_feed_service)
):
    """Удаление поста"""
    deleted = post_service.delete_post(post_id, current_user_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден или у вас нет прав на его удаление"
        )
    
    # Инвалидируем кеш лент
    feed_service.invalidate_user_feed(current_user_id)
