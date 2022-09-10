from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import User, Tag, Ingredient, Recipe, IngredientToRecipe, \
    Favorites, Subscription


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        validate_password(password)
        return attrs


class PasswordChangeSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        current_password = attrs.get('current_password')
        user = self.context['request'].user
        validate_password(new_password)
        if not check_password(current_password, user.password):
            raise ValidationError('Текущий паррль неверный')
        return attrs


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientToRecipeSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientToRecipe
        fields = ['name',
                  'measurement_unit',
                  'amount']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class IngredientCreateUpdateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientToRecipe
        fields = [
            'id',
            'amount',
        ]

class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = IngredientCreateUpdateSerializer(many=True)
    class Meta:
        model = Recipe
        fields = [
            'image',
            'ingredients',
            'tags',
            'name',
            'text',
            'cooking_time'
        ]

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        tags = validated_data.pop('tags', None)
        if not ingredients:
            raise ValidationError('Ингридиенты не выбраны')
        if not tags:
            raise ValidationError('Тэги не выбраны')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        IngredientToRecipe.objects.bulk_create([
            IngredientToRecipe(ingredient=ingredient.get('id'),
                               recipe=recipe, amount=ingredient.get('amount'))
            for ingredient in ingredients
        ])
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        tags = validated_data.pop('tags', None)
        if ingredients:
            instance.ingredients.clear()
            IngredientToRecipe.objects.bulk_create([
                IngredientToRecipe(ingredient=ingredient.get('id'),
                                   recipe=instance,
                                   amount=ingredient.get('amount'))
                for ingredient in ingredients
            ])
        if tags:
            instance.tags.set(tags)
        return instance

    def to_representation(self, instance):
        serializer = RecipeSerializer(instance, context=self.context)
        return serializer.data

class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientToRecipeSerializer(source='ingredienttorecipe_set',
                                               many=True)
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__'


class SubscribedUserSerializer(UserSerializer):
    def get_recipes_count(self, obj):
        return obj.recipes.count()

    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    email = serializers.ReadOnlyField(source='user.email')
    id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeSerializer(many=True, source='user.recipe_set')
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        ]

    def get_is_subscribed(self, obj):
        if obj.user.subscriptions.filter(subscriber=obj.user).count():
            return True
        else:
            return False

    def get_recipes_count(self, obj):
        return obj.user.recipe_set.count()


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'image',
            'cooking_time'
        ]
