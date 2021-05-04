from django.db import models
from django.utils.translation import ugettext_lazy as _
from iguana.base.models.user import User
from localflavor.br.models import BRCNPJField


class PessoaJuridica(User):

    cnpj = BRCNPJField(unique=True)

    @property
    def nome_fantasia(self):
        return self.first_name

    @nome_fantasia.setter
    def nome_fantasia(self, value):
        self.first_name = value

    @property
    def razao_social(self):
        return self.last_name

    @razao_social.setter
    def razao_social(self, value):
        self.last_name = value

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s (%s)" % (self.first_name, self.last_name)
        return full_name.strip()
