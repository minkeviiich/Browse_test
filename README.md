Проект FastAPI RabbitMQ Selenium
Этот проект представляет собой приложение FastAPI, которое интегрируется с RabbitMQ и Selenium для обработки URL-адресов. Приложение предоставляет конечную точку для приёма URL-адресов и добавляет их в очередь RabbitMQ. Приложение-потребитель читает из очереди и использует Selenium для открытия URL-адресов в браузере, логирования исходного кода страницы.

# Настройка и запуск

1. Клонирование репозитория

git clone https://github.com/minkeviiich/Brows_test.git
cd Browse_test

2. Сборка и запуск с Docker Compose
Используйте Docker Compose для сборки и запуска сервисов.

make build
make up

Эта команда соберёт Docker-образы и запустит следующие сервисы:

app: Приложение FastAPI, предоставляющее конечную точку /browse.

rabbitmq: Сервер RabbitMQ для очередей сообщений.

selenium-hub: Selenium Hub для управления сессиями браузера.

chrome: Узел с браузером Chrome для Selenium.

consumer: Сервис-потребитель для обработки URL из очереди RabbitMQ.

3. Доступ к сервисам

FastAPI: http://localhost:8000/docs

RabbitMQ Management: http://localhost:15672 (логин по умолчанию: guest, пароль: guest)

Selenium Hub: http://localhost:4444

4. Примеры команд для проверки логов

Просмотр логов приложения:
docker compose logs app

Просмотр логов consumer:
docker compose logs consumer

Просмотр логов RabbitMQ:
docker compose logs rabbitmq

Просмотр логов Selenium Hub:
docker compose logs selenium-hub

5. API

POST /browse
Принимает JSON-переменную с URL и добавляет её в очередь RabbitMQ.

# Конфигурация проекта

Этот проект использует переменные окружения, которые должны быть определены в файле `.env`.

## Пример .env файла

Создайте файл `.env` на основе примера `.env.example` и заполните необходимые значения.

- RABBITMQ_PORT=5672
- RABBITMQ_MANAGEMENT_PORT=15672
- APP_PORT=8000
- SELENIUM_HUB_PORT=4444
- SELENIUM_EVENT_BUS_PUBLISH_PORT=4442
- SELENIUM_EVENT_BUS_SUBSCRIBE_PORT=4443
- CHROME_NODE_PORT=5555
