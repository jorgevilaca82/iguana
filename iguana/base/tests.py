from django.utils.timezone import datetime
from django.contrib.auth import authenticate
from django.test import TestCase
from iguana.base.models.pessoa_fisica import PessoaFisica
from iguana.base.models.user import User


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
    def test_save_new(self):
        pf = PessoaFisica()
        self.assertIsNone(pf.pk)
        pf.save()
        self.assertIsNotNone(pf.pk)

    def test_timestamps(self):
        pf = PessoaFisica.objects.create(username="jose")
        self.assertIsInstance(pf, PessoaFisica)
        self.assertIsInstance(pf.created_at, datetime)
        self.assertIsInstance(pf.updated_at, datetime)

        old_update_at = pf.updated_at
        old_created_at = pf.created_at
        pf.email = "jose@iguana.com"
        pf.save()
        self.assertNotEquals(pf.updated_at, old_update_at)
        self.assertGreater(pf.updated_at, old_update_at)
        self.assertEquals(pf.created_at, old_created_at)
