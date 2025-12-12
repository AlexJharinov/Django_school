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

## Настройка сервера
Проект разворачивается на удалённом сервере с 
использованием Docker и GitHub Actions. 
Ниже приведена пошаговая инструкция по настройке окружения, 
сервера и автоматического деплоя.

### 1. Требования

Для работы проекта необходимы:

- Python 3.12+
- Docker + Docker Compose
- PostgreSQL (в контейнере)
- Redis (в контейнере)
- Nginx (в контейнере)
- GitHub репозиторий
- Доступ к серверу по SSH
---

### 2. Настройка сервера

#### 2.1. Подключение к серверу

```bash

ssh username@SERVER_IP

### 2.2. Установка Docker и Docker Compose

sudo apt update
sudo apt install -y ca-certificates curl gnupg

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

Проыерка:
docker --version
docker compose version

### 3. Клонирование проекта на сервер

cd ~
git clone https://github.com/<your-username>/Django_school.git
cd Django_school       


### 4. Запуск проекта

sudo docker compose up --build -d

### Настройка GITHUB Action 

Настройте файл deploy.yml

Добавте SSH-ключи на сервер и в GITHUB-secrets

Принцип работы делаешь push -> GitHub запускает workflow -> 
запускаются тесты если все ок -> Запускается деплой
если ошибки отсутствуют 

## Информация 
По всем вопросам писать neftkom.otk@gmail.com


