from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.html import format_html

from users.models import User


class Tag(models.Model):
    """Модель описания тегов для рецептов"""
    name = models.CharField("Название", max_length=200)
    hexcolor_regex = RegexValidator(
        regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$',
        message=(
            'Enter valid hex color number'
        )
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        validators=[hexcolor_regex],
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        "URL-адрес тега",
        unique=True,
        max_length=200,
    )


    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name

    def colored_name(self):
        """Color in format HEX."""
        return format_html(
            '<span style="color: #{};">{}</span>',
            self.color,
        )


class Recipe(models.Model):
    """Модель описывает рецепты, добавленные пользователем"""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор публикации"
    )
    name = models.CharField(
        "Название",
        max_length=200,
        unique=True,
        default='блюдо от шефповара',
    )
    image = models.ImageField(
        "Картинка",
    )
    text = models.TextField(
        "Текстовое описание",
    )
    tags = models.ManyToManyField(
        "Tag",
        related_name="recipes",
        verbose_name="Теги",
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(limit_value=1, message="Time smaller 1")
        ],
        verbose_name="Время приготовления",
        default=40,
    )
    favorite_this = models.ManyToManyField(
        User,
        related_name='favourite_recipes',
        verbose_name='Кому понравилось'
    )
    shopping_cart = models.ManyToManyField(
        User,
        related_name='shopping_carts',
        verbose_name='Кто хочет купить'
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
