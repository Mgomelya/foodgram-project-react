from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models


class User(AbstractUser):
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]
    USERNAME_FIELD = 'email'

    email = models.EmailField(unique=True, verbose_name='email')


class Tag(models.Model):
    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    name = models.CharField(max_length=255, verbose_name='название')
    color = models.CharField(max_length=7, validators=[MinLengthValidator(7)],
                             verbose_name='цветовой hex-код')
    slug = models.SlugField(verbose_name='слаг')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    class Meta:
        verbose_name = 'ингридиент'
        verbose_name_plural = 'ингридиенты'

    name = models.CharField(max_length=255,
                            verbose_name='название')
    measurement_unit = models.CharField(max_length=10,
                                        verbose_name='единицы измерения')

    def __str__(self):
        return self.name


class IngredientToRecipe(models.Model):
    class Meta:
        verbose_name = 'связь ингредиента с рецептом'
        verbose_name_plural = 'связи ингредиентов с рецептами'

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='amount',
                                   verbose_name='ингредиент')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE,
                               verbose_name='рецепт')
    amount = models.PositiveIntegerField(verbose_name='количество')


class Recipe(models.Model):
    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='автор')
    name = models.CharField(max_length=255, verbose_name='название')
    image = models.ImageField(verbose_name='картинка')
    text = models.TextField(verbose_name='описание')
    ingredients = models.ManyToManyField(Ingredient,
                                         through=IngredientToRecipe,
                                         verbose_name='ингредиенты')
    tags = models.ManyToManyField(Tag, verbose_name='тэги')
    cooking_time = models.PositiveIntegerField(
        verbose_name='время приготовления в минутах')

    def __str__(self):
        return self.name


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='пользователь',
                             related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='рецепт')


class Subscription(models.Model):
    class Meta:
        unique_together = ['user', 'subscriber']

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='тот на кого подписываются',
                             related_name='subscribers')
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE,
                                   verbose_name='подписчик',
                                   related_name='subscriptions')

    def clean(self):
        if self.user.id == self.subscriber.id:
            raise ValidationError(message='Нельзя подписаться на самого себя')


class ShoppingCartItem(models.Model):
    class Meta:
        unique_together = [
            'user',
            'recipe'
        ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='тот на кого подписываются',
                             related_name='cart_items')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='рецепт')
