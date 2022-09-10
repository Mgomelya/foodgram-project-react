from django_filters import rest_framework as filters

from .models import Recipe, User


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Recipe
        fields = [
            'tags',
            'author',
        ]
