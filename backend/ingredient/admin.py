from django.contrib.admin import ModelAdmin, register

from .models import Ingredient, IngredientAmount


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = [
        'pk',
        'name',
        'measurement_unit',
    ]
    list_filter = ['name',]
    search_fields = ['name',]
    empty_value_display = '-пусто-'


@register(IngredientAmount)
class IngredientAmountAdmin(ModelAdmin):
    list_display = [
        'pk',
        'amount',
        'ingredient',
        'recipe',
    ]
    list_filter = ['ingredient', 'recipe',]
    search_fields = ['recipe',]
    empty_value_display = '-пусто-'
    
