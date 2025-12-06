# Сервис обучения

## Описание

## Установка
- [клонируйте репозиторий](https://github.com/AlexJharinov/Django_school)

## Запуск программы
Пере запуском проверьте, что рядом с файлом 
docker-compose.yml лежит файл .env.docker.

### Запуск всех сервисов 
- Команда - docker compose up --build

После первого запуска 
выполнить миграции и создать суперпользователя:
- Команда - docker compose exec web python manage.py migrate
- Команда - docker compose exec web python manage.py createsuperuser

### Остановка сервиса 
- Команда - docker compose down




## Информация 
По всем вопросам писать neftkom.otk@gmail.com


