from iguana.base.models.pessoa_fisica import PessoaFisica
from rest_framework import generics as g
from rest_framework import serializers as s


class PessoaFisicaSerializer(s.ModelSerializer):
    class Meta:
        model = PessoaFisica
        fields = [
            "nome_completo",
            "cpf",
            "email",
            "estado_civil",
            "sexo",
            "tipo_sanguineo",
            "falecido",
        ]

    nome_completo = s.CharField(max_length=255)
    email = s.CharField(max_length=254)
    sexo = s.CharField(max_length=1)


class PessoaFisicaMixin:
    queryset = PessoaFisica.objects.all()
    serializer_class = PessoaFisicaSerializer


class PessoaFisicaList(PessoaFisicaMixin, g.ListCreateAPIView):
    pass


class PessoaFisicaDetail(g.RetrieveUpdateDestroyAPIView):
    pass
