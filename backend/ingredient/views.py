from rest_framework import viewsets

from .filters import IngredientFilter
from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter,)
    pagination_class = None
    search_fields = ('^name',)
