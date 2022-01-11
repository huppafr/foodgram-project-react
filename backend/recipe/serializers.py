from rest_framework import serializers
# import webcolors

from .models import Recipe, Tag


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


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'

    def __str__(self):
        return self.name


class RecipeListSerializer(serializers.ModelSerializer):
    #color = serializers.ChoiceField(choices=CHOICES)
    
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'author') # доделай

class TagSerializer(serializers.ModelSerializer):
    #cats = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Tag
        fields = '__all__'