from rest_framework.routers import DefaultRouter
from recipe.views import RecipeViewSet, TagViewSet
from users.views import CustomUserViewSet, SubscriptionViewSet
from ingredient.views import IngredientViewSet
from django.urls import path, include



router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(
    r'users/subscriptions',
    SubscriptionViewSet,
    basename='subscriptions'
)
router.register(r'users', CustomUserViewSet, basename='custom-users')

urlpatterns = [
    path('', include(router.urls)),


]
