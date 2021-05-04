from django.contrib.auth.models import AbstractUser
from django.db import models
from iguana.base.models.mixins import Timestamps
from django.contrib.auth import get_user_model


class User(Timestamps, AbstractUser):
    def get_endereco_principal(self):
        return self.base_endereco_related.get(principal=True)


class UserRelatedModel(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
