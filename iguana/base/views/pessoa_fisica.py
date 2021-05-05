from rest_framework import generics as g
from rest_framework import serializers as s
from iguana.base.models.pessoa_fisica import PessoaFisica


class PessoaFisicaSerializer(s.ModelSerializer):
    class Meta:
        model = PessoaFisica
        fields = [
            "nome_completo",
            "cpf",
            "estado_civil",
            "sexo",
            "tipo_sanguineo",
            "falecido",
        ]


class PessoaFisicaList(g.ListCreateAPIView):
    queryset = PessoaFisica.objects.all()
    serializer_class = PessoaFisicaSerializer
