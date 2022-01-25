from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.constraints import UniqueConstraint
from recipe.models import Recipe


class Ingredient(models.Model):
    """Модель, описывающая ингридиент для рецепта"""
    name = models.CharField(
        "Название",
        max_length=200,
        default='some ingredient',
        blank=False
    )
    measurement_unit = models.CharField(
        "Единицы измерения",
        max_length=20,
        default="шт",
        blank=False
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    """Модель, описывающая количество одного ингридиента для блюда"""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredient_amount",
        verbose_name="Ингредиент"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name="ingredients",
        verbose_name="Рецепт"
    )
    amount = models.PositiveSmallIntegerField(
        blank=False,
        validators=[
            MinValueValidator(
                limit_value=0,
                message="Amount can`t be smaller then 0"
            )
        ],
        verbose_name="Количество"
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient'
            )
        ]
        verbose_name = "Количество ингредиента"
        verbose_name_plural = "Количества ингредиентов"

    def __str__(self) -> str:
        return self.ingredient.name
