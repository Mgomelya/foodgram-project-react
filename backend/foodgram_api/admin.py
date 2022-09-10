from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import IngredientToRecipe, Recipe, Tag, Subscription, Favorites, \
    User, Ingredient, ShoppingCartItem


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
    ]


class IngredientToRecipeInline(admin.TabularInline):
    model = IngredientToRecipe


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    search_fields = [
        'username',
        'email',
    ]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientToRecipeInline,
    ]
    list_filter = [
        'author',
        'tags',
    ]
    search_fields = [
        'name',
    ]
    list_display = [
        'name',
        'author',
        'favorited',
    ]

    def favorited(self, obj):
        return Favorites.objects.filter(recipe=obj).count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    pass


@admin.register(ShoppingCartItem)
class ShoppingCartItem(admin.ModelAdmin):
    pass
