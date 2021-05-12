from iguana.base.models.pessoa_fisica import PessoaFisica
from rest_framework import fields, generics, serializers


class PessoaFisicaModelSerializer(serializers.ModelSerializer):
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

    nome_completo = fields.CharField(max_length=255)
    email = fields.EmailField(max_length=254)
    sexo = fields.CharField(max_length=1)


class PessoaFisicaAPIViewMixin:
    queryset = PessoaFisica.objects.all()
    serializer_class = PessoaFisicaModelSerializer


class PessoaFisicaListCreateAPIView(
    PessoaFisicaAPIViewMixin, generics.ListCreateAPIView
):
    pass


class PessoaFisicaRetrieveUpdateDestroyAPIView(
    PessoaFisicaAPIViewMixin, generics.RetrieveUpdateDestroyAPIView
):
    pass
