from django.db import models
from django.utils.translation import ugettext_lazy as _
from iguana.base.models.user import User
from localflavor.br.models import BRCPFField


class PessoaFisica(User):
    class Meta:
        ordering = ["-pk"]

    class Genero(models.TextChoices):
        MASCULINO = "M", _("Masculino")
        FEMININO = "F", _("Feminino")
        INDEFINIDO = "I", _("Indefinido")
        NAO_INFORMADO = "N", _("Não Informado")

    class EstadoCivil(models.IntegerChoices):
        SOLTEIRO = 0, _("Solteiro")
        CASADO = 1, _("Casado")
        VIUVO = 2, _("Viúvo")
        DIVORCIADO = 3, _("Divorciado")
        UNIAO_ESTAVEL = 4, _("União estável")

    class TipoSanguineo(models.TextChoices):
        A_POSITIVO = "A+"
        A_NEGATIVO = "A-"
        B_POSITIVO = "B+"
        B_NEGATIVO = "B-"
        AB_POSITIVO = "AB+"
        AB_NEGATIVO = "AB-"
        O_POSITIVO = "O+"
        O_NEGATIVO = "O-"

    cpf = BRCPFField(unique=True)
    sexo = models.CharField(max_length=1, choices=Genero.choices, null=True, blank=True)
    estado_civil = models.PositiveSmallIntegerField(
        choices=EstadoCivil.choices, null=True, blank=True
    )
    tipo_sanguineo = models.CharField(
        max_length=3, choices=TipoSanguineo.choices, blank=True, null=True
    )
    falecido = models.BooleanField(default=False)

    @property
    def nome_completo(self):
        return self.get_full_name()

    @nome_completo.setter
    def nome_completo(self, value):
        splited = value.split()
        self.first_name = splited[0]
        self.last_name = " ".join(splited[1:])
