#!/bin/bash

NGINX_CONF="./nginx/nginx.conf"

echo "=== Blue-Green Switch ==="

# Определяем активную версию
if grep -q "server app_blue:8000;" "$NGINX_CONF" && ! grep -q "backup" "$NGINX_CONF"; then
    echo "Активна: BLUE"
    echo "Переключаем на GREEN..."
    
    # Изменяем конфигурацию
    sed -i 's/server app_blue:8000;/server app_blue:8000 backup;/' "$NGINX_CONF"
    sed -i 's/server app_green:8000 backup;/server app_green:8000;/' "$NGINX_CONF"
    
    ACTIVE="GREEN"
    OLD="BLUE"
    
elif grep -q "server app_green:8000;" "$NGINX_CONF" && ! grep -q "backup" "$NGINX_CONF"; then
    echo "Активна: GREEN"
    echo "Переключаем на BLUE..."
    
    sed -i 's/server app_green:8000;/server app_green:8000 backup;/' "$NGINX_CONF"
    sed -i 's/server app_blue:8000 backup;/server app_blue:8000;/' "$NGINX_CONF"
    
    ACTIVE="BLUE"
    OLD="GREEN"
else
    echo "Ошибка: Не могу определить активную версию"
    exit 1
fi

echo "Конфигурация обновлена"
echo "Перезапускаем nginx..."
docker compose -f docker-compose.prod.yml restart nginx

echo "✅ Переключено на $ACTIVE"
echo "Старая версия ($OLD) теперь в резерве"
echo ""
echo "Проверка здоровья:"
sleep 3
curl -f http://localhost/health && echo "✓ Health check пройден" || echo "⚠ Health check не пройден"