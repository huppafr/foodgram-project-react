from django.db import models
from django.utils.translation import gettext_lazy as _

from django.core.validators import MinValueValidator
from django.db.models.constraints import UniqueConstraint

from recipe.models import Recipe

# CHOICES = (
#         ('mass', 'масса'),
#         ('volume', 'объем'),
#         ('quantity', 'количество'),
#         ('percent', 'процент'),
#         ('miscellaneous', 'разное'),
#     )

#масса = _('масса'), _('масса')
     # объем = _('объем'), _('объем')
     # количество = _('количество'), _('количество')
     # процент = _('процент'), _('процент')
     # разное = _('разное'), _('разное')


# class MeasurementUnit(models.Model):
#     #class Metrics(models.TextChoices):
#     #    mass = _('mass'), _('mass')
#     #    volume = _('volume'), _('volume')
#     #    quantity = _('quantity'), _('quantity')
#     #    percent = _('percent'), _('percent')
#     #    miscellaneous = _('miscellaneous'), _('miscellaneous')

#     name = models.CharField(
#         max_length=255,
#         verbose_name=_('name'),
#     )
    
#     metric = models.CharField(
#         max_length=255,
#         choices=CHOICES,
#         verbose_name=_('metric'),
#     )

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['name', 'metric'], name='unique_measurement_metric'
#             )
#         ]
#         verbose_name = _('Measurement unit')
#         verbose_name_plural = _('Measurement units')
#         ordering = ['metric', 'name']

#     def __str__(self):
#         return self.name
class Ingredient(models.Model):
    """The model describes the recipe ingredient."""
    name = models.CharField("Название",
                            max_length=200,
                            default='some ingredient',
                            blank=False)
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
    """Model for describing the amount of ingredients."""
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
            MinValueValidator(limit_value=0, message="Amount can`t be smaller then 0")
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



# class Ingredient(models.Model):
#     name = models.CharField(
#         max_length=255,
#         unique=True,
#         verbose_name=_('name'),
#         db_index=True,
#     )
#     measurement_unit = models.ForeignKey(
#         'MeasurementUnit',
#         related_name='ingredients',
#         on_delete=models.CASCADE,
#         verbose_name=_('measurement unit'),
#     )

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['name', 'measurement_unit'],
#                 name='unique_ingredient_unit',
#             )
#         ]
#         verbose_name = _('Ingredient')
#         verbose_name_plural = _('Ingredients')
#         ordering = ['name', 'measurement_unit', ]

#     def __str__(self):
#         return self.name
