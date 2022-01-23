
# from slugger import AutoSlugField
from django.core.validators import RegexValidator

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Exists, OuterRef
from django.utils.translation import gettext_lazy as _

#from ingredient.models import Ingredient
# from .utils import unique_slugify
from django.utils.html import format_html
from users.models import User



class Tag(models.Model):
    """The model describes the tags for fetching by recipes."""
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
        blank=False
    )

    def colored_name(self):
        """Color in format HEX."""
        return format_html(
            '<span style="color: #{};">{}</span>',
            self.color,
        )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name




class Recipe(models.Model):
    """The model describes recipes published by the user."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор публикации"
    )
    name = models.CharField("Название",
                            max_length=200,
                            unique=True,
                            default='блюдо от шефповара',
                            blank=False)
    image = models.ImageField("Картинка",
                              blank=False)
    text = models.TextField("Текстовое описание",
                            blank=False)
    tags = models.ManyToManyField("Tag",
                                  related_name="recipes",
                                  verbose_name="Теги",
                                  )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(limit_value=1, message="Time smaller 1")
        ],
        verbose_name="Время приготовления",
        default=40,
        blank=False
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






# class RecipeQuerySet(models.QuerySet):
#     def with_tags_and_authors(self):
#         return self.select_related('author').prefetch_related(
#             'tags', 'ingredients'
#         )

#     def with_favorited(self, user):
#         sub_qs = FavouriteRecipe.objects.filter(
#             user=user,
#             recipe=OuterRef('id'),
#             is_favorited=True,
#         )
#         return self.annotate(is_favorited=Exists(sub_qs))

#     def with_shopping_cart(self, user):
#         sub_qs = FavouriteRecipe.objects.filter(
#             user=user,
#             recipe=OuterRef('id'),
#             is_in_shopping_cart=True,
#         )
#         return self.annotate(is_in_shopping_cart=Exists(sub_qs))

#     def with_favorited_shopping_cart(self, user):
#         return self.with_favorited(user=user).with_shopping_cart(user=user)




# class Recipe(models.Model):
#     author = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         related_name='recipe',
#         on_delete=models.SET_NULL,
#         null=True,
#         verbose_name='Автор публикации',
#         help_text='Выберите автора', # доделать 
#     )
#     name = models.TextField(
#         verbose_name='Название рецепта',
#         help_text='Введите название для публикации',
#     )
#     image = models.ImageField(
#         upload_to='recipe/',   # додумать
#         blank=True,
#         null=True,
#         verbose_name='Изображение',
#         help_text='Выбрать файл',
#     )
#     text = models.TextField(
#         verbose_name='Описание рецепта',
#         help_text='Введите текст публикации',
#     )
#     # ingredients = models.ManyToManyField(
#     #     Ingredient,
#     #     verbose_name='Ингредиенты',
#     #     related_name='recipe_ingredients',
#     #     through='Amount',
#     #     through_fields=('recipe', 'ingredient')
#     # )
#     # ingredients = models.ForeignKey(
#     #     Ingredient,
#     #     related_name='recipe',
#     #     on_delete=models.CASCADE,
#     #     #through='RecipeIngredient',
#     #     verbose_name=_('ingredients'),
#     # )
#     ingredients = models.ManyToManyField(
#         'ingredient.Ingredient',
#         related_name='recipes',
#         through='IngredientAmount',
#         verbose_name=_('ingredients'),
#         )
#     tags = models.ManyToManyField(
#         'Tag',
#         related_name='recipe',
#         verbose_name='Тег',
#         help_text='Выберите тег',
#         )
#     cooking_time = models.PositiveSmallIntegerField(
#         verbose_name='Время приготовления',
#         help_text='Введите время приготовления блюда',
#     )
#     created_date = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name=_('created date'),
#     )
#     objects = models.Manager()
#     recipe_objects = RecipeQuerySet.as_manager()

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['author', 'name'],
#                 name='unique_recipe_author',
#             )
#         ]
#         verbose_name = _('Recipe')
#         verbose_name_plural = _('Recipes')
#         ordering = ['-created_date']

#     def __str__(self):
#         return self.name

#     def list_tags(self):
#         return self.tags.values_list('name', flat=True)



# class FavouriteRecipe(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         related_name='favourite_recipes',
#         on_delete=models.CASCADE,
#         verbose_name=_('user'),
#     )
#     recipe = models.ForeignKey(
#         'Recipe',
#         related_name='in_favourites',
#         on_delete=models.CASCADE,
#         verbose_name=_('recipe'),
#     )
#     is_in_shopping_cart = models.BooleanField(
#         default=False,
#         verbose_name=_('is in shopping cart')
#     )
#     is_favorited = models.BooleanField(
#         default=False,
#         verbose_name=_('is in favorites')
#     )
#     added_to_favorites = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name=_('added at')
#     )
#     added_to_shopping_cart = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name=_('added at')
#     )

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['user', 'recipe'],
#                 name='unique_favorite_recipe',
#             )
#         ]
#         verbose_name = _('Favorites')
#         verbose_name_plural = _('Favorites')
#         ordering = ['-added_to_favorites', '-added_to_shopping_cart']

#     def __str__(self):
#         return f'{self.user.username} - {self.recipe.name}'


