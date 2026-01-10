from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import uuid
from app.core.database import get_db
from app.schemas.post import FeedResponse
from app.api.dependencies import get_current_user, get_feed_service
from app.services.feed_service import FeedService

router = APIRouter(prefix="/feed", tags=["Лента"])

@router.get("/", response_model=FeedResponse)
async def get_feed(
    current_user_id: uuid.UUID = Depends(get_current_user),
    limit: int = Query(20, ge=1, le=100),
    cursor: Optional[datetime] = Query(None),
    feed_service: FeedService = Depends(get_feed_service)
):
    """Получение ленты новостей"""
    posts, next_cursor = feed_service.generate_feed(
        user_id=current_user_id,
        limit=limit,
        cursor=cursor
    )
    
    return {
        "posts": posts,
        "next_cursor": next_cursor,
        "has_more": next_cursor is not None and len(posts) == limit
    }
