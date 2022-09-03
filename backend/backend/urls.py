"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from foodgram_api.views import UserViewset, TokenCreateAPIView, \
    TokenDestroyAPIView, CurrentUserRetrieveAPIView, PasswordChangeAPIView, \
    TagViewset, IngredientViewset, RecipeViewset, SubscriptionListAPIView, \
    SubscriptionCreateDestroyAPIView, FavoritesCreateDestroyAPIView, \
    ShoppingCartCreateDestroyAPIView, ShoppingCartDownloadAPIView

router = DefaultRouter()
router.register('users', UserViewset)
router.register('tags', TagViewset)
router.register('ingredients', IngredientViewset)
router.register('recipes', RecipeViewset)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/token/login/", TokenCreateAPIView.as_view()),
    path("api/auth/token/logout/", TokenDestroyAPIView.as_view()),
    path("api/users/me/", CurrentUserRetrieveAPIView.as_view()),
    path("api/users/set_password/", PasswordChangeAPIView.as_view()),
    path("api/users/subscriptions/", SubscriptionListAPIView.as_view()),
    path("api/users/<int:user_pk>/subscribe/",
         SubscriptionCreateDestroyAPIView.as_view()),
    path("api/recipes/<int:recipe_id>/favorite/",
         FavoritesCreateDestroyAPIView.as_view()),
    path("api/recipes/<int:recipe_id>/shopping_cart/",
         ShoppingCartCreateDestroyAPIView.as_view()),
    path("api/recipes/download_shopping_cart/",
         ShoppingCartDownloadAPIView.as_view()),
    path("api/", include(router.urls)),

]
