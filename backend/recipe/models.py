from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# Create your models here.
"""
Рецепт должен описываться такими полями:

Автор публикации (пользователь). ++++
Название.
Картинка. ++++
Текстовое описание. ++++
Ингредиенты: продукты для приготовления блюда по рецепту. Множественное поле,
  выбор из предустановленного списка, с указанием количества и единицы измерения.
Тег (можно установить несколько тегов на один рецепт, выбор из предустановленных).
Время приготовления в минутах.
Все поля обязательны для заполнения.
"""

class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Recipes',
        verbose_name='Автор публикации',
        help_text='Выберите автора',
    )
    name = models.TextField(
        verbose_name='Название',
        help_text='Введите название для публикации',
    )
    image = models.ImageField(
        upload_to='posts/',   # додумать
        blank=True,
        null=True,
        verbose_name='Изображение',
        help_text='Выбрать файл',
    )
    description = models.TextField(
        verbose_name='Публикация',
        help_text='Введите текст публикации',
    )
    #ingredients
    #tag
    coocking_time = models.CharField(
        max_length = 30,
        verbose_name='Время приготовления',
        help_text='Введите время приготовления блюда',
    )
