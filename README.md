# Posts service

## Запуск вручную

### Установка

- Склонируйте проект `git clone https://github.com/mihett05/posts-service.git`
- Передите в папку с проектом `cd posts-service`
- (Если poetry не установлен) Установите poetry `pip3 install poetry` или `pip install poetry`
- Установите зависимости проекта `poetry install`
- Сделайте миграции `poetry run python manage.py migrate`

### Запуск сервера

- Запустите сервер (напримре, на 8000 порту) `poetry run python manage.py runserver 8000`
- Откройте приложение по ссылке http://localhost:8000/

### Запуск тестов

- Запустите `poetry run python manage.py test`

## Запуск через Docker

### Установка

- Склонируйте проект `git clone https://github.com/mihett05/posts-service.git`
- `docker compose build`

### Запуск сервера

- Запуск на 8000 порту `docker compose up`
