from django_filters import rest_framework as filters

from .models import Recipe, User


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_in_shopping_cart = filters.BooleanFilter(method= 'filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = [
            'tags',
            'author',
        ]
    def filter_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            # TODO: dopilit'
            return queryset
        return queryset

