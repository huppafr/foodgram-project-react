from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# Create your models here.
"""
Рецепт должен описываться такими полями:

Автор публикации (пользователь).
Название.
Картинка.
Текстовое описание.
Ингредиенты: продукты для приготовления блюда по рецепту. Множественное поле, выбор из предустановленного списка, с указанием количества и единицы измерения.
Тег (можно установить несколько тегов на один рецепт, выбор из предустановленных).
Время приготовления в минутах.
Все поля обязательны для заполнения.
"""

class Recipe(models.Model):
    author = models.ForeignKey(

    )
    #name
    #image

    description = models.TextField(
        verbose_name='Публикация',
        help_text='Введите текст публикации',
    )

    #ingredients
    #tag
    coocking_time = models.CharField(
        max_length = 30,
        help_text='Введите текст публикации',
    )



    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор статьи',
        help_text='Выберите автора',
    )
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Сообщество',
        help_text='Выберите сообщество',
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True,
        verbose_name='Изображение',
        help_text='Выбрать файл',
    )