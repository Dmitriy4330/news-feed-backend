import os
import sys
from logging.config import fileConfig

# КРИТИЧЕСКИ ВАЖНО: добавляем путь к проекту
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_dir)

from alembic import context
from sqlalchemy import engine_from_config, pool

# Импортируем ВАШИ настройки
from app.core.config import settings

# Импортируем ВАШ Base из database.py
from app.core.database import Base

# Импортируем ВАШИ модели (после Base!)
# Это нужно, чтобы Alembic их увидел
import app.models.user
import app.models.post
import app.models.subscription

# Конфигурация Alembic
config = context.config

# Настройка логгирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Устанавливаем URL БД из ВАШИХ настроек
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# КРИТИЧЕСКИ ВАЖНО: передаём метаданные ВАШИХ моделей
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
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
