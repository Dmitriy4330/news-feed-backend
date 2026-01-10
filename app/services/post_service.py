from sqlalchemy.orm import Session
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate
from typing import List, Optional
import uuid
from datetime import datetime

class PostService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_post(self, user_id: uuid.UUID, post_data: PostCreate) -> Post:
        """Создание нового поста"""
        post = Post(
            user_id=user_id,
            content=post_data.content
        )
        
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        
        return post
    
    def get_post_by_id(self, post_id: uuid.UUID) -> Optional[Post]:
        """Получение поста по ID"""
        return self.db.query(Post).filter(Post.id == post_id).first()
    
    def get_user_posts(self, user_id: uuid.UUID, limit: int = 20, offset: int = 0) -> List[Post]:
        """Получение постов пользователя"""
        return self.db.query(Post)\
            .filter(Post.user_id == user_id)\
            .order_by(Post.created_at.desc())\
            .offset(offset)\
            .limit(limit)\
            .all()
    
    def update_post(self, post_id: uuid.UUID, user_id: uuid.UUID, update_data: PostUpdate) -> Optional[Post]:
        """Обновление поста"""
        post = self.db.query(Post)\
            .filter(Post.id == post_id, Post.user_id == user_id)\
            .first()
        
        if not post:
            return None
        
        if update_data.content is not None:
            post.content = update_data.content
        
        self.db.commit()
        self.db.refresh(post)
        
        return post
    
    def delete_post(self, post_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        """Удаление поста"""
        post = self.db.query(Post)\
            .filter(Post.id == post_id, Post.user_id == user_id)\
            .first()
        
        if not post:
            return False
        
        self.db.delete(post)
        self.db.commit()
        
        return True
    
    def get_posts_by_user_ids(self, user_ids: List[uuid.UUID], limit: int = 20, cursor: Optional[datetime] = None) -> List[Post]:
        """Получение постов по списку ID пользователей (для ленты)"""
        query = self.db.query(Post)\
            .filter(Post.user_id.in_(user_ids))\
            .order_by(Post.created_at.desc())\
            .limit(limit)
        
        if cursor:
            query = query.filter(Post.created_at < cursor)
        
        return query.all()
