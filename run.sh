#!/bin/bash

CONTAINER_NAME="bot"
IMAGE_NAME="khtkarimzhonov/bot.onson-mail.uz:latest"

# Переменные окружения
BOT_TOKEN=
WEBHOOK_URL=
BASE_SITE=

# Если контейнер существует — остановить и удалить
if [ "$(docker ps -a -q -f name=^/${CONTAINER_NAME}$)" ]; then
    echo "Stopping and removing existing container: $CONTAINER_NAME"
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

# Загружаем свежий образ
echo "Pulling latest image: $IMAGE_NAME"
docker pull $IMAGE_NAME

# Запускаем новый контейнер с переменными окружения
echo "Starting new container: $CONTAINER_NAME"
docker run -d \
    --name $CONTAINER_NAME \
    -p 5000:80 \
    -e BOT_TOKEN=$BOT_TOKEN \
    -e BASE_SITE=$BASE_SITE \
    -e WEBHOOK_URL=$WEBHOOK_URL \
    $IMAGE_NAME
