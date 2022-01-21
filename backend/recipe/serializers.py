from django.contrib.auth import get_user_model
from rest_framework import serializers

from .fields import Base64ImageField
from .models import Recipe, Tag, IngredientAmount
from users.models import UserSubscription
from ingredient.models import Ingredient


from users.models import UserSubscription

from .services import (add_recipe_with_ingredients_tags,
                       update_recipe_with_ingredients_tags)


User = get_user_model()




class UserSerializer(serializers.ModelSerializer):
    """
    Define here to avoid circular imports
    """
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        ]

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return UserSubscription.objects.filter(
            subscriber=user, subscription=obj
        ).exists()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']

# class Hex2NameColor(serializers.Field):
#     # При чтении данных ничего не меняем - просто возвращаем как есть
#     def to_representation(self, value):
#         return value
#     # При записи код цвета конвертируется в его название
#     def to_internal_value(self, data):
#         try:
#             # Если имя цвета существует, то конвертируем код в название
#             data = webcolors.hex_to_name(data)
#         except ValueError:
#             # Иначе возвращаем ошибку
#             raise serializers.ValidationError('Для этого цвета нет имени')
#         # Возвращаем данные в новом формате
#         return data


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'



class IngredientAmountSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    id = serializers.ReadOnlyField(source='ingredient.id')
    #amount = serializers.ReadOnlyField(source='ingredient_amounts')
    

    class Meta:
        model = IngredientAmount
        fields = [
            'id',
            'name',
            'measurement_unit',
            'amount'
        ]



class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientAmountSerializer(
        many=True,
        source='ingredient_amounts'
    )
    is_favorited = serializers.BooleanField(read_only=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        ]


class IngredientWriteSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(write_only=True)
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Ingredient
        fields = [
            'id',
            'amount'
        ]


class RecipeWriteSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientWriteSerializer(many=True)
    author = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    image = Base64ImageField(max_length=False, use_url=True)
    is_favorited = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        return add_recipe_with_ingredients_tags(validated_data)

    def update(self, instance, validated_data):
        return update_recipe_with_ingredients_tags(validated_data, instance)

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context=self.context).data

    class Meta:
        model = Recipe
        fields = [
            'tags',
            'ingredients',
            'author',
            'image',
            'name',
            'text',
            'cooking_time',
            'is_favorited'
        ]


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'image',
            'cooking_time',
        ]



# class RecipeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Recipe
#         fields = '__all__'

#     def __str__(self):
#         return self.name


# class RecipeListSerializer(serializers.ModelSerializer):
#     author = UserSerializer(read_only=True)
#     tags = TagSerializer(many=True, read_only=True)
#     #ingredients = IngredientSerializer(many=True, read_only=True)
#     ingredients = IngredientAmountSerializer(
#         many=True,
#         source='ingredient_amounts'
#     )
#     is_favorited = serializers.BooleanField(read_only=True)
#     is_in_shopping_cart = serializers.BooleanField(read_only=True)
#     image = Base64ImageField()


#     class Meta:
#         model = Recipe
#         fields = (
#             'id',
#             'tags',
#             'author',
#             'name',
#             'ingredients', 
#             'is_favorited',
#             'is_in_shopping_cart',
#             'name',
#             'image',
#             'text',
#             'cooking_time',
#         ) # доделай







