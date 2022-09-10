import os

from django.conf import settings
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, \
    HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from .filters import RecipeFilter
from .mixins import CreateDestroyMixin
from .models import User, Tag, Ingredient, Recipe, Favorites, Subscription, \
    ShoppingCartItem
from .serializers import UserSerializer, PasswordChangeSerializer, \
    TagSerializer, IngredientSerializer, RecipeSerializer, \
    RecipeCreateUpdateSerializer, SubscriptionSerializer, \
    ShoppingCartSerializer
from .shopping_cart import create_shopping_cart_list


class UserViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = serializer.validated_data.pop('password')
        user = serializer.save()
        user.set_password(password)
        user.save()


class CurrentUserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class TokenCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if {'email', 'password'}.issubset(request.data):
            user = authenticate(
                request,
                email=request.data.get('email'),
                password=request.data.get('password')
            )
            if user is not None:
                if user.is_active:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response(
                        data={'auth_token': token.key},
                        status=HTTP_201_CREATED
                    )
        return Response(
            data={
                'error': 'Неверная пара логин/пароль '
                         'или пользователь неактивен'},
            status=HTTP_400_BAD_REQUEST
        )


class TokenDestroyAPIView(generics.GenericAPIView):
    queryset = Token.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        token = Token.objects.get(user=self.request.user)
        return token

    def post(self, request):
        token = self.get_object()
        token.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class PasswordChangeAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class TagViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RecipeCreateUpdateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavoritesCreateDestroyAPIView(CreateDestroyMixin,
                                    generics.GenericAPIView):
    queryset = Favorites.objects.all()
    serializer_class = RecipeSerializer
    error_message = 'Рецепта нет в избранном'
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):

        queryset = self.get_queryset()
        try:
            return queryset.get(recipe=self.get_recipe(),
                                user=self.request.user)
        except queryset.model.DoesNotExist:
            return queryset.none()

    def get_recipe(self):
        return get_object_or_404(Recipe, id=self.kwargs.get('recipe_id'))

    def create(self, request, *args, **kwargs):
        recipe = self.get_recipe()
        print(recipe)
        print(self.request.user)
        favorite, created = Favorites.objects.get_or_create(
            recipe=recipe,
            user=self.request.user
        )
        if not created:
            return Response(data={'errors': 'Рецепт уже есть в избранном'},
                            status=HTTP_400_BAD_REQUEST
                            )
        else:
            serializer = self.get_serializer_class()(instance=recipe,
                                                     context=self.get_serializer_context())
            return Response(data=serializer.data, status=HTTP_201_CREATED)


class SubscriptionListAPIView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(subscriber=self.request.user)


class SubscriptionCreateDestroyAPIView(CreateDestroyMixin,
                                       generics.GenericAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    error_message = 'Ошибка отписки'
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        try:
            return queryset.get(user=self.get_user(),
                                subscriber=self.request.user)
        except queryset.model.DoesNotExist:
            return None

    def create(self, request, *args, **kwargs):
        user = self.get_user()

        if self.request.user.id == user.id:
            return Response(
                data={'errors': 'Нельзя подписаться на самого себя'},
                status=HTTP_400_BAD_REQUEST
            )
        subscription, created = Subscription.objects.get_or_create(
            subscriber=self.request.user,
            user=user
        )
        if not created:
            return Response(data={'errors': 'Подписка уже оформлена'},
                            status=HTTP_400_BAD_REQUEST
                            )
        else:
            serializer = self.get_serializer_class()(instance=subscription)
            return Response(data=serializer.data, status=HTTP_201_CREATED)


class ShoppingCartCreateDestroyAPIView(CreateDestroyMixin,
                                       generics.GenericAPIView):
    serializer_class = ShoppingCartSerializer
    error_message = 'Рецепт отсутствует в списке покупок'
    permission_classes = [permissions.IsAuthenticated]

    def get_recipe(self):
        return get_object_or_404(Recipe, id=self.kwargs.get('recipe_id'))

    def get_queryset(self):
        return ShoppingCartItem.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        try:
            return queryset.get(recipe=self.get_recipe(),
                                user=self.request.user)
        except queryset.model.DoesNotExist:
            return None

    def create(self, request, *args, **kwargs):
        recipe = self.get_recipe()
        favorite, created = ShoppingCartItem.objects.get_or_create(
            recipe=recipe,
            user=self.request.user
        )
        if not created:
            return Response(data={'errors': 'Рецепт уже в списке покупок'},
                            status=HTTP_400_BAD_REQUEST
                            )
        else:
            serializer = self.get_serializer_class()(instance=recipe)
            return Response(data=serializer.data, status=HTTP_201_CREATED)


class ShoppingCartDownloadAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = create_shopping_cart_list(self.request.user)
        file_path = os.path.join(settings.MEDIA_ROOT,
                                 f'{self.request.user.username}.txt')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(data)
        with open(file_path, 'r', encoding='utf-8') as f:
            file_data = f.read()
        response = Response(data, content_type='text/plain')
        file_name = f'{self.request.user.username}.txt'
        response[
            'Content-Disposition'] = f'attachment; file_name="{file_name}"'
        return response
