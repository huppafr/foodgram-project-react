from django.contrib import admin

from django.contrib.admin import ModelAdmin, register
from django.utils.translation import gettext_lazy as _

from .models import Recipe, Tag
from ingredient.models import IngredientAmount



@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'color',)
    ordering = ('name',)
    empty_value_display = '-'

'''
@register(Ingredient)
class IngredientAdmin(ModelAdmin):

@register(IngredientAmount)
class IngredientAmountAdmin(ModelAdmin):

'''

# @register(Recipe)
# class RecipeAdmin(ModelAdmin):
#     # fields = (
#     #     'author', 'name',  'cooking_time'
#     # )
#     list_display = (
#         'author',
#         'name',
#         'text',
#         #'get_ingredients',
#         #'ingredients',
#         'get_tags',
#         'created_date',
#         'image',
#         'cooking_time',
#         'get_favorites',
#     )
#     filter_horizontal = ('tags',)
#     search_fields = ('author',)
#     list_filter = ('author', 'name', 'tags', 'ingredients', 'cooking_time')
#     ordering = ('created_date', 'author')
#     empty_value_display = '-'

#     @display(description=_('Теги'))
#     def get_tags(self, obj):
#         qs = obj.list_tags()
#         if qs:
#             return list(qs)
#         return None
#     # тестовая
#     @display(description=_('Ингредиенты'))
#     def get_ingredients(self, obj):
#         qs = obj.list_ingredients()
#         if qs:
#             return list(qs)
#         return None

#     @display(description=_('Added to favorites,number'))
#     def get_favorites(self, obj):
#         qs = obj.in_favourites.count()
#         if qs:
#             return qs
#         return None

class TagInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1
    verbose_name = 'Тег'
    verbose_name_plural = 'Теги'


class LikesInline(admin.TabularInline):
    model = Recipe.favorite_this.through
    extra = 1
    verbose_name = 'Пользователь'
    verbose_name_plural = 'Добавили в избранное'


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    fk_name = 'recipe'
    extra = 1
    verbose_name = 'Ингридиент'
    verbose_name_plural = 'Ингридиенты'




@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = [
        'pk',
        'name',
        'image',
        'text',
        'cooking_time',
        'author',
    ]
    exclude = ['ingredients', 'tags', 'who_likes_it',]
    inlines = [
        IngredientAmountInline,
        TagInline,
        LikesInline,
    ]
    list_filter = ['name', 'cooking_time', 'author',]
    search_fields = ['name','author',]
    empty_value_display = '-пусто-'