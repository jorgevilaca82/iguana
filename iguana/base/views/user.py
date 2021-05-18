from iguana.base import models as m
from iguana.base import serializers as s
from rest_framework import generics

from django.contrib.auth import get_user_model


class UserTelefoneAPIViewMixin:
    serializer_class = s.UserTelefoneModelSerializer

    def get_queryset(self):
        return m.Telefone.objects.filter(user=self.kwargs["user_pk"])


class UserTelefoneListCreateAPIView(
    UserTelefoneAPIViewMixin, generics.ListCreateAPIView
):
    pass


class UserTelefoneRetrieveUpdateDestroyAPIView(
    UserTelefoneAPIViewMixin, generics.RetrieveUpdateDestroyAPIView
):
    pass


class UserEnderecoAPIViewMixin:
    serializer_class = s.UserEnderecoModelSerializer

    def get_queryset(self):
        return m.Endereco.objects.filter(user=self.kwargs["user_pk"])


class UserEnderecoListCreateAPIView(
    UserEnderecoAPIViewMixin, generics.ListCreateAPIView
):
    pass


class UserEnderecoRetrieveUpdateDestroyAPIView(
    UserEnderecoAPIViewMixin, generics.RetrieveUpdateDestroyAPIView
):
    pass
