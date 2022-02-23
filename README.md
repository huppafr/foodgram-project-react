# FoodGram

``` http://huppas-foodgram.ddnsking.com/ ```


«Продуктовый помощник»: сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.


## Технологии
- Python 3.9
- Django 4.0.2
- gunicorn 20.0.4
- Nginx 1.18
- Docker 20.10.6


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
- Покрыть проект тестами
- Реализовать почтовый сервер

## Автор

- Хюппенен Артём
