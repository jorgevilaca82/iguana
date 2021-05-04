from iguana.base.models.mixins import Timestamps
from django.db import models
from iguana.base.models.user import UserRelatedModel
from django.core.validators import RegexValidator


class TelefoneRegexValidator(RegexValidator):
    regex = r"^(\+?\d{2}\s?)?(\(\d{2}\)|\d{2})\s?(\d{4,5})(\-?)(\d{4})$"


class Telefone(UserRelatedModel, Timestamps, models.Model):
    class Meta:
        unique_together = ("user", "numero")

    numero = models.CharField(max_length=120, validators=[TelefoneRegexValidator()])
    observacoes = models.TextField(null=True, blank=True)
