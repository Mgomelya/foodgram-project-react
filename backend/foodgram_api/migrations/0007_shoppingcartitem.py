# Generated by Django 3.2.15 on 2022-08-31 18:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodgram_api', '0006_auto_20220830_2035'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingCartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodgram_api.recipe', verbose_name='рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to=settings.AUTH_USER_MODEL, verbose_name='тот на кого подписываются')),
            ],
            options={
                'unique_together': {('user', 'recipe')},
            },
        ),
    ]
