# News Feed API

Бэкенд для новостной ленты с подписками на пользователей.

## Функциональность

- Регистрация и аутентификация пользователей (JWT)
- Создание, редактирование, удаление постов
- Подписка/отписка на пользователей
- Лента новостей 

## Как запустить:

### 1. Клонирование репозитория
git clone https://github.com/ваш-логин/news-feed-backend.git
cd news-feed-backend
### 2. Запуск контейнеров
docker-compose up -d
### 3. Установка зависимостей
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
### 4. Запуск сервера
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
### 5. Документация API
Открываем в браузере: http://localhost:8000/docs

## API Endpoints
### Аутентификация
POST /auth/register - регистрация

POST /auth/login - вход

### Посты
POST /posts/ - создать пост

GET /posts/{id} - получить пост

PUT /posts/{id} - обновить пост

DELETE /posts/{id} - удалить пост

### Подписки
POST /subscriptions/{author_id} - подписаться

DELETE /subscriptions/{author_id} - отписаться

GET /subscriptions/my - мои подписки

### Лента
GET /feed/?limit=20&cursor=... - получить ленту

## Сделали это
### Кудрявцев Александр
### Ситжанова Элина
### Казанин Дмитрий
