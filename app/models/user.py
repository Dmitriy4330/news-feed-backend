import uuid
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship  # ДОБАВЬТЕ ЭТОТ ИМПОРТ!
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Временно закомментируем relationships, чтобы они не мешали
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", foreign_keys="Subscription.subscriber_id", backref="subscriber")
    subscribers = relationship("Subscription", foreign_keys="Subscription.author_id", backref="author")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"