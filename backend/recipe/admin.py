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