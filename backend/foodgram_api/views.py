from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework import viewsets, mixins, generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, \
    HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from .models import User, Tag, Ingredient, Recipe, Favorites
from .serializers import UserSerializer, PasswordChangeSerializer, \
    TagSerializer, IngredientSerializer, RecipeSerializer, FavoritesSerializer


class UserViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer


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


class TokenDestroyAPIView(generics.DestroyAPIView):
    queryset = Token.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        token = Token.objects.get(user=self.request.user)
        return token


class PasswordChangeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            current_password = request.data.get('current_password')
            if check_password(current_password, user.password):
                user.set_password(request.data.get('new_password'))
                return Response(status=HTTP_204_NO_CONTENT)
            else:
                Response(
                    data={'error': 'Текущий пароль неверный'},
                    status=HTTP_400_BAD_REQUEST
                )
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
    serializer_class = RecipeSerializer


class FavoritesViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
