# praktikum_new_diplom
pip install docker docker-compose psycopg2 psycopg2-binary
pip install django django-autoslug django-uuslug


<!-- Если у вас macOS или Windows, загрузите PostgreSQL с сайта https://www.postgresql.org/download/ и установите.
Также потребуется адаптер PostgreSQL под названием Psycopg2 для Python. Эта команда установит его: -->
pip install psycopg2
pip install django-environ
pip install pillow djangorestframework coverage django-filter
pip install djoser 
pip install webcolors reportlab

pip install gunicorn 


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