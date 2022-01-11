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
        help_text='Выберите автора', # доделать 
    )
    name = models.TextField(
        verbose_name='Название рецепта',
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
        verbose_name='Описание рецепта',
        help_text='Введите текст публикации',
    )
    #ingredients
    #tag
    coocking_time = models.CharField(
        max_length = 30,
        verbose_name='Время приготовления',
        help_text='Введите время приготовления блюда',
    )

    def __str__(self):
        return self.name


''' 
Тег должен описываться такими полями:
Название.
Цветовой HEX-код (например, #49B64E).
Slug.
Все поля обязательны для заполнения и уникальны.
'''
class Tag(models.Model):
    name = models.TextField(
        verbose_name='Название тега',
        help_text='Введите название для тега',
    )
    color = 
    slug = 
    pass

'''
Данные об ингредиентах хранятся в нескольких связанных таблицах. 
В результате на стороне пользователя ингредиент должен описываться такими полями:

Название.
Количество.
Единицы измерения.
Все поля обязательны для заполнения.
'''

class Ingredient(models.Model):
    pass