from django.urls import include, path
from ingredient.views import IngredientsViewSet
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from recipe.views import TagViewSet, RecipeViewSet

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
