from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''Модель пользователя'''
    first_name = models.CharField('first name', max_length=150)
    last_name = models.CharField('last name', max_length=150)
    email = models.EmailField('email address', unique=True)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['last_name']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Follow(models.Model):
    '''Модель, описывающая подписку пользователей друг на друга'''
    author = models.ForeignKey(
        User,
        related_name='author_follow',
        on_delete=models.CASCADE,
        verbose_name='you_Who_have_been_subscribed_to_people'
    )

    subscriber = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE,
        verbose_name="People_who_u_subscribed",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'author'], name='unique_subscription'
            ),
        ]
        verbose_name = 'Подписку'
        verbose_name_plural = 'Подписки'
