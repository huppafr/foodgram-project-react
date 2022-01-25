from django.contrib.admin import ModelAdmin, register

from .models import User, Follow


@register(User)
class UserAdmin(ModelAdmin):
    list_display = [
        'pk',
        'username',
        'email',
        'first_name',
        'last_name'
    ]
    list_filter = [
        'username',
        'email',
        'first_name',
        'last_name',
    ]
    search_fields = [
        'username',
        'email',
        'first_name',
        'last_name',
    ]
    empty_value_display = '-пусто-'


@register(Follow)
class FollowAdmin(ModelAdmin):
    list_display = [
        'pk',
        'subscriber',
        'author',
    ]
    list_filter = [
        'subscriber',
        'author',
    ]
    search_fields = [
        'subscriber',
        'author',
    ]
    empty_value_display = '-пусто-'
