from iguana.base import models as m
from rest_framework import fields, serializers, validators

from django.contrib.auth import get_user_model


class UserEnderecoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Endereco
        fields = [
            "tipo",
            "tipo_display",
            "cep",
            "logradouro",
            "bairro",
            "numero",
            "cidade",
            "uf",
            "complemento",
            "principal",
        ]

    tipo_display = fields.CharField(source="get_tipo_display", read_only=True)


class UserTelefoneModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Telefone


class PessoaFisicaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.PessoaFisica
        fields = [
            "id",
            "nome_completo",
            "cpf",
            "email",
            "estado_civil",
            "estado_civil_display",
            "sexo",
            "tipo_sanguineo",
            "falecido",
        ]

    nome_completo = fields.CharField(max_length=255)
    email = fields.EmailField(max_length=254)
    sexo = fields.CharField(max_length=1)
    estado_civil_display = fields.CharField(
        source="get_estado_civil_display", read_only=True
    )


class PessoaJuridicaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.PessoaJuridica
        fields = [
            "id",
            "cnpj",
        ]
