import os
import sys
from logging.config import fileConfig

# Добавляем путь к проекту в sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.insert(0, project_dir)

from alembic import context
from sqlalchemy import engine_from_config, pool

# Импортируем наши настройки
from app.core.config import settings

# Импортируем Base из нашей базы данных
from app.core.database import Base

# Импортируем все модели (ВАЖНО: после импорта Base!)
from app.models.user import User
from app.models.post import Post
from app.models.subscription import Subscription

# Конфигурация Alembic
config = context.config

# Настройка логгирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Устанавливаем URL базы данных из наших настроек
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Передаём метаданные наших моделей Alembic
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Запуск миграций в офлайн-режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Запуск миграций в онлайн-режиме."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()