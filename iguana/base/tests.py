import json

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.timezone import datetime
from iguana.base.models.endereco import Endereco
from iguana.base.models.pessoa_fisica import PessoaFisica
from iguana.base.models.telefone import Telefone
from iguana.base.models.user import User
from rest_framework import status
from rest_framework.test import APITestCase


class UserTests(TestCase):
    def setUp(self) -> None:
        extra_fields = dict()
        self.new_user = User.objects.create_user(
            "iguana_user",
            email="iguana_user@iguana.test",
            password="iguana",
            **extra_fields
        )
        return super().setUp()

    def test_user_creation_success(self):
        self.assertIsInstance(self.new_user, User)
        self.assertIsNotNone(self.new_user.pk)

    def test_user_can_authenticate(self):
        authenticated_user = authenticate(username="iguana_user", password="iguana")
        self.assertIsNotNone(authenticated_user)
        self.assertIsInstance(authenticated_user, User)


class PessoaFisicaModelTests(TestCase):
    CPF_VALIDO = "47571343208"
    CPF_INVALIDO = "81662104285"

    def setUp(self) -> None:

        self.pf1 = PessoaFisica.objects.create_user(
            username="jose", email="jose@iguana.com", password="jose", cpf="81662104286"
        )
        return super().setUp()

    def test_save_new(self):
        """
        O minimo necessário para salvar uma pessoa fisica é o cpf.
        Isso é interessante em casos de importação onde nem todos os dados
        estão disponíveis. Por isso mantemos no model somente validações críticas
        """
        pf = PessoaFisica(cpf=self.CPF_VALIDO)
        self.assertIsNone(pf.pk)
        pf.save()
        self.assertIsNotNone(pf.pk)
        self.assertIs(pf.documentoidentificacao_set.count(), 0)
        self.assertIs(pf.base_telefone_related.count(), 0)
        self.assertIs(pf.base_endereco_related.count(), 0)

    def test_is_user(self):
        self.assertIsInstance(self.pf1, User)

    def test_timestamps(self):
        self.assertIsInstance(self.pf1, PessoaFisica)
        self.assertIsInstance(self.pf1.created_at, datetime)
        self.assertIsInstance(self.pf1.updated_at, datetime)

        old_update_at = self.pf1.updated_at
        old_created_at = self.pf1.created_at
        self.pf1.email = "jose@iguana.com"
        self.pf1.save()
        self.assertNotEquals(self.pf1.updated_at, old_update_at)
        self.assertGreater(self.pf1.updated_at, old_update_at)
        self.assertEquals(self.pf1.created_at, old_created_at)

    def test_pode_validar_cpf(self):
        pf = PessoaFisica(cpf=self.CPF_INVALIDO)
        with self.assertRaises(ValidationError) as cm:  # cm: Context Manager
            pf.full_clean()

        self.assertIn("cpf", cm.exception.error_dict)

    def test_tem_relacionamento_com_endereco(self):
        enderecos = self.pf1.base_endereco_related.all()
        self.assertIsInstance(enderecos, QuerySet)
        novo_endereco = self.pf1.base_endereco_related.create(
            principal=True, tipo=Endereco.Tipo.RESIDENCIAL
        )
        self.assertIsInstance(novo_endereco, Endereco)
        self.assertEquals(novo_endereco.user.pessoafisica, self.pf1)

        self.assertIs(novo_endereco.principal, True)
        # cria um novo endereco principal
        novo_endereco_principal = self.pf1.base_endereco_related.create(
            principal=True, tipo=Endereco.Tipo.RESIDENCIAL
        )
        self.assertIs(novo_endereco_principal.principal, True)

        # o primeiro endereço deixa de ser o principal automaticamente
        novo_endereco.refresh_from_db()
        self.assertIs(novo_endereco.principal, False)

    def test_tem_relacionamento_com_telefone(self):
        telefones = self.pf1.base_telefone_related.all()
        self.assertIsInstance(telefones, QuerySet)
        novo_telefone = self.pf1.base_telefone_related.create()
        self.assertIsInstance(novo_telefone, Telefone)
        self.assertEquals(novo_telefone.user.pessoafisica, self.pf1)


class PessoaFisicaWebApiTests(APITestCase):
    fixtures = ("user.json", "pessoafisica.json")

    JSON_CONTENT_TYPE = "application/json"

    def setUp(self) -> None:
        # self.client = APIClient()
        # self.client.login(username="iguana_user", password="iguana")

        self.pf_list_path = reverse_lazy("pessoafisica-list")
        self.pf_detail_path = reverse_lazy("pessoafisica-detail")

        return super().setUp()

    def test_get_list(self):
        response = self.client.get(self.pf_list_path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNot(len(response.json()["results"]), 0)
        self.assertGreaterEqual(response.json()["count"], 2)

    def test_create(self):
        # user = User.objects.first()
        # self.client.force_authenticate(user=user)
        valid_payload = dict(
            nome_completo="Jose da Silva",
            email="jose@gmail.com",
            cpf="47571343208",
            estado_civil=PessoaFisica.EstadoCivil.SOLTEIRO,
            sexo=PessoaFisica.Genero.MASCULINO,
            tipo_sanguineo=PessoaFisica.TipoSanguineo.O_POSITIVO,
        )
        response = self.client.post(
            self.pf_list_path,
            data=json.dumps(valid_payload),
            content_type=self.JSON_CONTENT_TYPE,
        )
        # print(json.dumps(valid_payload))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(status.is_success(response.status_code))
