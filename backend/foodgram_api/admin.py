from django.contrib import admin

from .models import IngredientToRecipe, Recipe, Tag


class IngredientToRecipeInline(admin.TabularInline):
    model = IngredientToRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientToRecipeInline,
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
