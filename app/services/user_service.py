from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password, create_access_token
from typing import Optional
import uuid

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: UserCreate) -> User:
        """Создание нового пользователя"""
        # Проверяем, существует ли пользователь с таким email или username
        existing_user = self.db.query(User).filter(
            (User.email == user_data.email) | (User.username == user_data.username)
        ).first()
        
        if existing_user:
            if existing_user.email == user_data.email:
                raise ValueError("Пользователь с таким email уже существует")
            else:
                raise ValueError("Пользователь с таким username уже существует")
        
        # Хешируем пароль
        hashed_password = get_password_hash(user_data.password)
        
        # Создаём пользователя
        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Аутентификация пользователя"""
        user = self.db.query(User).filter(User.email == email).first()
        
        if not user:
            return None
        
        if not verify_password(password, user.password_hash):
            return None
        
        return user
    
    def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Получение пользователя по ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Получение пользователя по email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def update_user(self, user_id: uuid.UUID, update_data: UserUpdate) -> Optional[User]:
        """Обновление данных пользователя"""
        user = self.get_user_by_id(user_id)
        
        if not user:
            return None
        
        # Обновляем только переданные поля
        update_dict = update_data.dict(exclude_unset=True)
        
        for field, value in update_dict.items():
            setattr(user, field, value)
        
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def create_access_token_for_user(self, user: User) -> str:
        """Создание JWT токена для пользователя"""
        token_data = {"sub": str(user.id), "email": user.email}
        return create_access_token(token_data)
