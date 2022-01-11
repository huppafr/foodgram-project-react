from rest_framework.routers import DefaultRouter
from recipe.views import RecipeViewSet
from django.urls import path, include



router = DefaultRouter()
router.register('recipes', RecipeViewSet)


urlpatterns = [
    path('', include(router.urls)),


]
