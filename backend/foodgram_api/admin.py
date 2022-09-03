from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import IngredientToRecipe, Recipe, Tag, Subscription, Favorites, \
    User


class IngredientToRecipeInline(admin.TabularInline):
    model = IngredientToRecipe


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientToRecipeInline,
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    pass
