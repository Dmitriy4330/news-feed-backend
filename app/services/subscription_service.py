from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.subscription import Subscription
from app.models.user import User
from typing import List, Optional
import uuid

class SubscriptionService:
    def __init__(self, db: Session):
        self.db = db
    
    def subscribe(self, subscriber_id: uuid.UUID, author_id: uuid.UUID) -> Optional[Subscription]:
        """Подписаться на пользователя"""
        # Нельзя подписаться на самого себя
        if subscriber_id == author_id:
            raise ValueError("Нельзя подписаться на самого себя")
        
        # Проверяем, существует ли автор
        author = self.db.query(User).filter(User.id == author_id).first()
        if not author:
            raise ValueError("Автор не найден")
        
        # Проверяем, не подписан ли уже
        existing = self.db.query(Subscription).filter(
            Subscription.subscriber_id == subscriber_id,
            Subscription.author_id == author_id
        ).first()
        
        if existing:
            raise ValueError("Вы уже подписаны на этого пользователя")
        
        # Создаём подписку
        subscription = Subscription(
            subscriber_id=subscriber_id,
            author_id=author_id
        )
        
        self.db.add(subscription)
        self.db.commit()
        self.db.refresh(subscription)
        
        return subscription
    
    def unsubscribe(self, subscriber_id: uuid.UUID, author_id: uuid.UUID) -> bool:
        """Отписаться от пользователя"""
        subscription = self.db.query(Subscription).filter(
            Subscription.subscriber_id == subscriber_id,
            Subscription.author_id == author_id
        ).first()
        
        if not subscription:
            return False
        
        self.db.delete(subscription)
        self.db.commit()
        
        return True
    
    def get_subscriptions(self, user_id: uuid.UUID) -> List[Subscription]:
        """Получить всех, на кого подписан пользователь"""
        return self.db.query(Subscription)\
            .filter(Subscription.subscriber_id == user_id)\
            .all()
    
    def get_subscribers(self, author_id: uuid.UUID) -> List[Subscription]:
        """Получить всех подписчиков пользователя"""
        return self.db.query(Subscription)\
            .filter(Subscription.author_id == author_id)\
            .all()
    
    def is_subscribed(self, subscriber_id: uuid.UUID, author_id: uuid.UUID) -> bool:
        """Проверить, подписан ли пользователь"""
        subscription = self.db.query(Subscription).filter(
            Subscription.subscriber_id == subscriber_id,
            Subscription.author_id == author_id
        ).first()
        
        return subscription is not None
    
    def get_subscription_ids(self, user_id: uuid.UUID) -> List[uuid.UUID]:
        """Получить ID авторов, на которых подписан пользователь"""
        subscriptions = self.get_subscriptions(user_id)
        return [sub.author_id for sub in subscriptions]
