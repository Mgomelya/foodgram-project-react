from .models import ShoppingCartItem, User, IngredientToRecipe, Ingredient


def create_shopping_cart_list(user: User):
    cart_items = ShoppingCartItem.objects.filter(user=user)
    cart_dict = {

    }
    for item in cart_items:
        recipe = item.recipe
        for ingredient in recipe.ingredients.all():
            if ingredient.id in cart_dict.keys():
                cart_dict[ingredient.id] += IngredientToRecipe.objects.get(
                    recipe=recipe, ingredient=ingredient).amount
            else:
                cart_dict[ingredient.id] = IngredientToRecipe.objects.get(
                    recipe=recipe, ingredient=ingredient).amount
    output = []
    for ingredient_id, amount in cart_dict.items():
        ingredient = Ingredient.objects.get(id=ingredient_id)
        output.append(
            f'{ingredient.name} - {amount} {ingredient.measurement_unit}'
        )
    return '\n'.join(output).encode('utf-8')
