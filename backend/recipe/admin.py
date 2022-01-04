from django.contrib import admin

from .models import Recipe

class RecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "name", "image", "description", "coocking_time",)
    search_fields = ("name", "author",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"


admin.site.register(Recipe, RecipeAdmin)