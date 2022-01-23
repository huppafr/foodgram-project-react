from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

#from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

#from recipe.serializers import RecipeFavoriteSerializer

#from .models import UserSubscription
from recipe.models import Recipe

User = get_user_model()


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        min_length=8,
        max_length=128,
        write_only=True,
    )
    current_password = serializers.CharField(write_only=True)


class M2MUserRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']
        read_only_fields = ['name', 'image', 'cooking_time']


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request:
            return False
        user = request.user
        if not user.is_authenticated:
            return False
        return user.author_follow.filter(subscriber=obj).exists()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password',
        ]
        extra_kwargs = {'password': {'write_only': True}}


class UserSubscriptionSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        recipes_limit = None
        request = self.context.get('request')
        if request:
            recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit and recipes_limit.isdigit():
            recipes_limit = int(recipes_limit)
        queryset = obj.recipes.all()[:recipes_limit]
        serializer = M2MUserRecipeSerializer(queryset, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password',
            'recipes',
            'recipes_count'
        ]
        extra_kwargs = {'password': {'write_only': True}}




# class UserSerializer(UserCreateSerializer):
#     is_subscribed = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = [
#             'email',
#             'id',
#             'username',
#             'first_name',
#             'last_name',
#             'is_subscribed',
#             'password'
#         ]
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }

#     def get_is_subscribed(self, obj):
#         user = self.context['request'].user
#         if user.is_anonymous:
#             return False
#         return UserSubscription.objects.filter(
#             subscriber=user, subscription=obj
#         ).exists()


# class SubscriptionSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(source='subscription.email')
#     id = serializers.EmailField(source='subscription.id')
#     username = serializers.EmailField(source='subscription.username')
#     first_name = serializers.EmailField(source='subscription.first_name')
#     last_name = serializers.EmailField(source='subscription.last_name')
#     is_subscribed = serializers.SerializerMethodField(read_only=True)
#     recipes_count = serializers.SerializerMethodField(read_only=True)
#     recipes = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = UserSubscription
#         fields = [
#             'email',
#             'id',
#             'username',
#             'first_name',
#             'last_name',
#             'is_subscribed',
#             'recipes',
#             'recipes_count'
#         ]

#     def get_is_subscribed(self, obj):
#         user = self.context['request'].user
#         if user.is_anonymous:
#             return False
#         return UserSubscription.objects.filter(
#             subscriber=user, subscription=obj.subscription
#         ).exists()

#     def get_recipes_count(self, obj):
#         return obj.subscription.recipes.count()

#     def get_recipes(self, obj):
#         recipes = obj.subscription.recipes.all()[:3]
#         return RecipeFavoriteSerializer(recipes, many=True).data


# class SubscriptionWriteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserSubscription
#         fields = [
#             'subscriber',
#             'subscription',
#         ]

#     def validate_subscription(self, value):
#         request = self.context['request']
#         if not request.user == value:
#             return value
#         raise serializers.ValidationError(
#             _('Вы не можете подписаться на себя')
#         )