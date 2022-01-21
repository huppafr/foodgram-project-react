# from django.contrib.auth import get_user_model
# from django.db import models
# from slugger import AutoSlugField
# from django.conf import settings
# from django.utils.translation import gettext_lazy as _
# from ingredient.models import Ingredient
# from django.db.models import Exists, OuterRef
# from django.core.validators import MinValueValidator

# from .utils import unique_slugify

from slugger import AutoSlugField

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Exists, OuterRef
from django.utils.translation import gettext_lazy as _

#from ingredient.models import Ingredient
from .utils import unique_slugify
from django.utils.html import format_html



'''
Данные об ингредиентах хранятся в нескольких связанных таблицах. 
В результате на стороне пользователя ингредиент должен описываться такими полями:

Название.
Количество.
Единицы измерения.
Все поля обязательны для заполнения.
'''










# class Ingredient(models.Model):
#     name = models.CharField(
#         max_length=255,
#         unique=True,
#         verbose_name='Название ингридиента',
#         help_text='Введите название ингридиента'
#     )
#     amount = models.CharField(
#         max_length = 30,
#         verbose_name='Количество ингридиентов',
#         help_text='Введите количество ингридиентов'
#     )
#     measurement_unit = models.CharField(
#         max_length = 10,
#         verbose_name='Единицы измерения',
#         help_text='Выберите единицы измерения'
#     )

#     def __str__(self):
#         return self.name





''' 
Тег должен описываться такими полями:
Название.
Цветовой HEX-код (например, #49B64E).
Slug.
Все поля обязательны для заполнения и уникальны.
'''

# def instance_mz_slug(instance):
#     return instance.mz_name

# def slugify_value(value):
#     return value.replace(' ', '-')

class Tag(models.Model):
    name = models.TextField(
        unique=True,
        verbose_name='Название тега',
        help_text='Введите название для тега',
    )
    color = models.CharField(
        max_length=16,
        unique=True,
        verbose_name='Цвет тега',
        help_text='Введите цвет для тега',
    )
    slug = AutoSlugField(
        populate_from='name',
        editable=False,
        unique = True,
        max_length= 50,
        blank=False,
        verbose_name='URL-адрес тега',
        help_text='Введите URL-адрес для тега',
    )

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['id']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = unique_slugify(self.name, self.__class__)
        return super().save(*args, **kwargs)
 
    
#тестовый класс
# class Ingredient(models.Model):
#     """
#     model Ingredient
#     """

#     class Meta:
#         verbose_name = 'Ингредиент'
#         verbose_name_plural = 'Ингредиенты'
#         ordering = ('name',)

#     name = models.CharField(
#         verbose_name='Название ингредиента',
#         max_length=200,
#         db_index=True
#     )
#     unit = models.CharField(
#         verbose_name='Единица измерения',
#         max_length=20
#     )

#     def __str__(self):
#         return self.name





        

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
class RecipeQuerySet(models.QuerySet):
    def with_tags_and_authors(self):
        return self.select_related('author').prefetch_related(
            'tags', 'ingredients'
        )

    def with_favorited(self, user):
        sub_qs = FavouriteRecipe.objects.filter(
            user=user,
            recipe=OuterRef('id'),
            is_favorited=True,
        )
        return self.annotate(is_favorited=Exists(sub_qs))

    def with_shopping_cart(self, user):
        sub_qs = FavouriteRecipe.objects.filter(
            user=user,
            recipe=OuterRef('id'),
            is_in_shopping_cart=True,
        )
        return self.annotate(is_in_shopping_cart=Exists(sub_qs))

    def with_favorited_shopping_cart(self, user):
        return self.with_favorited(user=user).with_shopping_cart(user=user)


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='recipe',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Автор публикации',
        help_text='Выберите автора', # доделать 
    )
    name = models.TextField(
        verbose_name='Название рецепта',
        help_text='Введите название для публикации',
    )
    image = models.ImageField(
        upload_to='recipe/',   # додумать
        blank=True,
        null=True,
        verbose_name='Изображение',
        help_text='Выбрать файл',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Введите текст публикации',
    )
    # ingredients = models.ManyToManyField(
    #     Ingredient,
    #     verbose_name='Ингредиенты',
    #     related_name='recipe_ingredients',
    #     through='Amount',
    #     through_fields=('recipe', 'ingredient')
    # )
    # ingredients = models.ForeignKey(
    #     Ingredient,
    #     related_name='recipe',
    #     on_delete=models.CASCADE,
    #     #through='RecipeIngredient',
    #     verbose_name=_('ingredients'),
    # )
    ingredients = models.ManyToManyField(
        'ingredient.Ingredient',
        related_name='recipes',
        through='IngredientAmount',
        verbose_name=_('ingredients'),
        )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipe',
        verbose_name='Тег',
        help_text='Выберите тег',
        )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='Введите время приготовления блюда',
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created date'),
    )
    objects = models.Manager()
    recipe_objects = RecipeQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'name'],
                name='unique_recipe_author',
            )
        ]
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
        ordering = ['-created_date']

    def __str__(self):
        return self.name

    def list_tags(self):
        return self.tags.values_list('name', flat=True)

#тестовый класс
# class Amount(models.Model):
#     """
#     An intermediate model between the "Ingredient" and "Recipe" models,
#     shows the quantity of ingredient in a particular recipe.
#     """

#     class Meta:
#         verbose_name = 'Количество ингредиента'
#         verbose_name_plural = 'Количество ингредиентов'

#     recipe = models.ForeignKey(
#         Recipe,
#         verbose_name='Рецепт',
#         on_delete=models.CASCADE,
#         related_name='amount_recipes'
#     )
#     ingredient = models.ForeignKey(
#         Ingredient,
#         verbose_name='Ингредиент',
#         on_delete=models.CASCADE,
#         related_name='ingredients'
#     )
#     units = models.PositiveIntegerField(
#         verbose_name='Количество/объем',
#         default=0,
#     )

#     def __str__(self):
#         return str(self.units)

# # тестовый класс
# class RecipeIngredient(models.Model):
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
#                                related_name='recipe_ingredients')
#     ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
#                                    related_name='recipe_ingredients')
#     amount = models.PositiveIntegerField(validators=(
#                                    MinValueValidator(1),
#                                    MaxValueValidator(10000)))

#     def __str__(self):
#         return self.ingredient.title


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        related_name='ingredient_amounts',
        on_delete=models.CASCADE,
        verbose_name=_('recipe')
    )
    ingredient = models.ForeignKey(
        'ingredient.Ingredient',
        related_name='ingredient_amounts',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('ingredient')
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name=_('ingredient amount')
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient',
            )
        ]
        verbose_name = _('Ingredient amount')
        verbose_name_plural = _('Ingredient amounts')
        ordering = ['id']

    def __str__(self):
        return f'{self.recipe.name} - {self.ingredient.name}'


class FavouriteRecipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='favourite_recipes',
        on_delete=models.CASCADE,
        verbose_name=_('user'),
    )
    recipe = models.ForeignKey(
        'Recipe',
        related_name='in_favourites',
        on_delete=models.CASCADE,
        verbose_name=_('recipe'),
    )
    is_in_shopping_cart = models.BooleanField(
        default=False,
        verbose_name=_('is in shopping cart')
    )
    is_favorited = models.BooleanField(
        default=False,
        verbose_name=_('is in favorites')
    )
    added_to_favorites = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('added at')
    )
    added_to_shopping_cart = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('added at')
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe',
            )
        ]
        verbose_name = _('Favorites')
        verbose_name_plural = _('Favorites')
        ordering = ['-added_to_favorites', '-added_to_shopping_cart']

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'


