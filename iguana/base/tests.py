from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.test import TestCase
from django.utils.timezone import datetime
from iguana.base.models.endereco import Endereco
from iguana.base.models.pessoa_fisica import PessoaFisica
from iguana.base.models.telefone import Telefone
from iguana.base.models.user import User
from rest_framework import status
from rest_framework.test import APIClient


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
    def setUp(self) -> None:
        self.pf1 = PessoaFisica.objects.create_user(
            username="jose", email="jose@iguana.com", password="jose", cpf="81662104286"
        )
        return super().setUp()

    def test_save_new(self):
        pf = PessoaFisica(cpf="47571343208")
        self.assertIsNone(pf.pk)
        pf.save()
        self.assertIsNotNone(pf.pk)

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
        pf = PessoaFisica(cpf="81662104285")  # cpf inválido
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


class PessoaFisicaWebApiTests(TestCase):
    fixtures = ("user.json", "pessoafisica.json")

    def setUp(self) -> None:
        self.client = APIClient()
        self.client.login(username="iguana_user", password="iguana")
        return super().setUp()

    def test_get_list(self):
        response = self.client.get(
            "/api/pessoafisica.json", HTTP_ACCEPT="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNot(len(response.json()["results"]), 0)
        self.assertGreaterEqual(response.json()["count"], 2)

    def test_create(self):
        response = self.client.post(
            "/api/pessoafisica.json",
            data=dict(
                nomecompleto="Jose da Silva",
                cpf="47571343208",
                estado_civil=PessoaFisica.EstadoCivil.SOLTEIRO,
                sexo=PessoaFisica.Genero.MASCULINO,
                tipo_sanguineo=PessoaFisica.TipoSanguineo.O_POSITIVO,
            ),
            content_type="application/json",
        )
        print(response)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
