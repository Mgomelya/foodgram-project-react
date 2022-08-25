import json
from foodgram_api.models import Ingredient
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Команда для загрузки ингредиентов из json-файла'

    def handle(self, *args, **options):
        with open('../data/ingredients.json', 'r', encoding='UTF-8') as file:
            json_data = json.load(file)
        Ingredient.objects.bulk_create(
            [Ingredient(**item_data) for item_data in json_data]
        )


