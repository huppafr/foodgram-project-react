# FoodGram

``` http://huppas-foodgram.ddnsking.com/ ```


«Продуктовый помощник»: сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.


## Технологии
- Python 3.9
- Django 4.0.2
- gunicorn 20.0.4
- Nginx 1.18
- Docker 20.10.6
- PostgreSQL 12.4

## Установка:
Для установки Docker выполните следующие команды:
```
- curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh 
```
Далее используйте следущие команды:
1. Создайте папку yamdb
```
- mkdir foodgram
```
И скопируйте туда проект

2. Создайте .env файл со следующим содержимым:
```
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

## Подготовка инфраструктуры:

1. Клонируйте репозиторий на локальный компьютер
2. Создайте и активируйте виртуальное окружение
```bash
python3 -m venv venv
. venv/bin/activate
```
3. Установите зависимости
```bash
pip install -r requirements.txt
```
4. Выполните миграции
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Создайте администратора
```bash
python manage.py createsuperuser
```
6. Запустите проект локально
```bash
python manage.py runserver
```

Готово, проект доступен по адресу http://127.0.0.1:8000/


### Запуск сайта локально из директории backend/
``` python manage.py runserver ```
### Запуск сервера из ubuntu осуществляется командой
``` docker-compose up ```
### команда для удаления базы данных и всех volumes
``` docker-compose down -v```
### команда для создания суперпользователя, работает только с запущенным контейнером
``` docker-compose exec backend python manage.py createsuperuser ```
### Команда для заполнения ингредиентами
``` docker-compose exec backend python manage.py loaddata fixtures/ingredients.json ```
### команда для заполнения проекта статикой
``` docker-compose exec backend python manage.py collectstatic ```

[![Django-app workflow](https://github.com/huppafr/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/huppafr/foodgram-project-react/actions/workflows/main.yml)

## ToDo
- Реализовать почтовый сервер

## Автор

- Хюппенен Артём
