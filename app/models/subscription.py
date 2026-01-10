import uuid
from sqlalchemy import Column, DateTime, ForeignKey, func, PrimaryKeyConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    subscriber_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Составной первичный ключ
    __table_args__ = (
        PrimaryKeyConstraint('subscriber_id', 'author_id'),
        Index('idx_subscriptions_author', 'author_id'),
    )
    
    def __repr__(self):
        return f"<Subscription(subscriber={self.subscriber_id}, author={self.author_id})>"