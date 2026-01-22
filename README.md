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


## CI/CD Pipeline с Blue-Green деплоем

### Архитектура пайплайна:

### GitHub Actions Workflow:
1. **test** — запускает pytest с PostgreSQL и Redis в services
2. **build-and-push** — собирает Docker образ и пушит в Docker Hub
3. **deploy** — информационная больше стадия (архитектура Blue-Green)

### Blue-Green деплой:
- **app_blue** и **app_green** — две идентичные версии приложения
- **nginx** — балансировщик, переключает трафик между версиями
- **PostgreSQL + Redis** — общие для обеих версий

### Локальный запуск:
# Сборка образов
docker build -f Dockerfile.prod -t news-feed-backend:blue .
docker build -f Dockerfile.prod -t news-feed-backend:green .

# Запуск всей инфры
docker-compose --env-file .env.prod -f docker-compose.prod.yml up -d

# Проверка
curl http://localhost/health

# Переключение версий
./scripts/blue-green-switch.sh


## Сделали это
### Кудрявцев Александр
### Ситжанова Элина
### Казанин Дмитрий
