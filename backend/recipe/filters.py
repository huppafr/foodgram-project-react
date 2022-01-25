from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter
from users.models import User

from .models import Recipe


class RecipeFilter(FilterSet):
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_in_shopping_cart = filters.BooleanFilter(method='cart_filter')
    is_favorited = filters.BooleanFilter(method='favorite_filter')

    def cart_filter(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(shopping_cart__id=self.request.user.id)
        return queryset

    def favorite_filter(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorite_this__id=self.request.user.id)
        return queryset

    class Meta:
        model = Recipe
        fields = ['author', 'tags']


class IngredientFilter(SearchFilter):
    search_param = 'name'
