from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.core.database import get_db
from app.schemas.subscription import SubscriptionResponse, SubscriptionCreate, SubscriptionsList
from app.api.dependencies import get_current_user, get_subscription_service, get_feed_service
from app.services.subscription_service import SubscriptionService
from app.services.feed_service import FeedService

router = APIRouter(prefix="/subscriptions", tags=["Подписки"])

@router.post("/{author_id}", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
async def subscribe_to_user(
    author_id: uuid.UUID = Path(...),
    current_user_id: uuid.UUID = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(get_subscription_service),
    feed_service: FeedService = Depends(get_feed_service)
):
    """Подписаться на пользователя"""
    try:
        subscription = subscription_service.subscribe(current_user_id, author_id)
        
        # Инвалидируем кеш ленты после подписки
        feed_service.invalidate_user_feed(current_user_id)
        
        return subscription
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unsubscribe_from_user(
    author_id: uuid.UUID = Path(...),
    current_user_id: uuid.UUID = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(get_subscription_service),
    feed_service: FeedService = Depends(get_feed_service)
):
    """Отписаться от пользователя"""
    unsubscribed = subscription_service.unsubscribe(current_user_id, author_id)
    
    if not unsubscribed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Подписка не найдена"
        )
    
    # Инвалидируем кеш ленты после отписки
    feed_service.invalidate_user_feed(current_user_id)

@router.get("/my", response_model=SubscriptionsList)
async def get_my_subscriptions(
    current_user_id: uuid.UUID = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(get_subscription_service)
):
    """Получить мои подписки"""
    subscriptions = subscription_service.get_subscriptions(current_user_id)
    
    return {
        "subscriptions": subscriptions,
        "total": len(subscriptions)
    }

@router.get("/subscribers", response_model=SubscriptionsList)
async def get_my_subscribers(
    current_user_id: uuid.UUID = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(get_subscription_service)
):
    """Получить моих подписчиков"""
    subscribers = subscription_service.get_subscribers(current_user_id)
    
    return {
        "subscriptions": subscribers,
        "total": len(subscribers)
    }
