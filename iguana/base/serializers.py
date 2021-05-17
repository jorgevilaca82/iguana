from iguana.base import models as m
from rest_framework import fields, serializers


class TelefoneModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Telefone
        fields = ["id", "numero"]


class UserModelSerializerMixin(serializers.ModelSerializer):
    telefones = TelefoneModelSerializer(
        required=False, many=True, source="base_telefone_related"
    )


class PessoaFisicaModelSerializer(
    UserModelSerializerMixin, serializers.ModelSerializer
):
    class Meta:
        model = m.PessoaFisica
        fields = [
            "id",
            "nome_completo",
            "cpf",
            "email",
            "estado_civil",
            "sexo",
            "tipo_sanguineo",
            "falecido",
            "telefones",
        ]

    nome_completo = fields.CharField(max_length=255)
    email = fields.EmailField(max_length=254)
    sexo = fields.CharField(max_length=1)


class PessoaJuridicaModelSerializer(
    UserModelSerializerMixin, serializers.ModelSerializer
):
    class Meta:
        model = m.PessoaJuridica
        fields = [
            "id",
            "cnpj",
            "telefones",
        ]
