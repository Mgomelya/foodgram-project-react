from django.shortcuts import get_object_or_404
from rest_framework import mixins, status
from rest_framework.response import Response

from .models import User


class CreateDestroyMixin(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin):
    """ Mixin для создания и удаления объектов для избранного и подписок"""
    error_message = None

    def get_user(self):
        return get_object_or_404(User, id=self.kwargs.get('user_pk'))

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data={'errors': self.error_message},
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
