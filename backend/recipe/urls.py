from rest_framework.routers import DefaultRouter
from recipe.views import RecipeViewSet, TagViewSet
from users.views import UserViewSet
from ingredient.views import IngredientsViewSet
from django.urls import path, include
# from django.views.generic import TemplateView



router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    # path('auth/', include('djoser.urls.authtoken')),
    # path(
    #     'redoc/',
    #     TemplateView.as_view(template_name='redoc.html'),
    #     name='redoc'
    # ),


]
