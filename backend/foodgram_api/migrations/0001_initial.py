# Generated by Django 3.2.15 on 2022-08-24 18:31

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='название')),
                ('measurement_unit', models.CharField(max_length=10, verbose_name='единицы измерения')),
            ],
            options={
                'verbose_name': 'ингридиент',
                'verbose_name_plural': 'ингридиенты',
            },
        ),
        migrations.CreateModel(
            name='IngredientToRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(verbose_name='количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodgram_api.ingredient', verbose_name='ингредиент')),
            ],
            options={
                'verbose_name': 'связь ингредиента с рецептом',
                'verbose_name_plural': 'связи ингредиентов с рецептами',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='название')),
                ('color', models.CharField(max_length=7, validators=[django.core.validators.MinLengthValidator(7)], verbose_name='цветовой hex-код')),
                ('slug', models.SlugField(verbose_name='слаг')),
            ],
            options={
                'verbose_name': 'тег',
                'verbose_name_plural': 'теги',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='название')),
                ('image', models.ImageField(upload_to='', verbose_name='картинка')),
                ('text', models.TextField(verbose_name='описание')),
                ('cooking_time', models.TimeField(verbose_name='время приготовления')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='автор')),
                ('ingredients', models.ManyToManyField(through='foodgram_api.IngredientToRecipe', to='foodgram_api.Ingredient', verbose_name='ингредиенты')),
                ('tags', models.ManyToManyField(to='foodgram_api.Tag', verbose_name='тэги')),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': 'рецепты',
            },
        ),
        migrations.AddField(
            model_name='ingredienttorecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodgram_api.recipe', verbose_name='рецепт'),
        ),
    ]
