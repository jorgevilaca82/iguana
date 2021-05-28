from django.db import models
from django.utils.translation import ugettext_lazy as _
from iguana.base.models.mixins import HasNomeMixin, HasSiglaMixin


class Pais(HasSiglaMixin, HasNomeMixin, models.Model):
    def __str__(self):
        return f"{self.nome} ({self.sigla})"
