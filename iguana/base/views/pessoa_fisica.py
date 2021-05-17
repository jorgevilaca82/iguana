from iguana.base import models as m
from iguana.base import serializers as s
from rest_framework import generics


class PessoaFisicaAPIViewMixin:
    queryset = m.PessoaFisica.objects.all()
    serializer_class = s.PessoaFisicaModelSerializer


class PessoaFisicaListCreateAPIView(
    PessoaFisicaAPIViewMixin, generics.ListCreateAPIView
):
    pass


class PessoaFisicaRetrieveUpdateDestroyAPIView(
    PessoaFisicaAPIViewMixin, generics.RetrieveUpdateDestroyAPIView
):
    pass
