from django.db import models
from django.db.models.fields.related import OneToOneField
from django.utils.translation import ugettext_lazy as _
from iguana.base.models.user import User
from django.contrib.auth.models import UserManager
from localflavor.br.models import BRCPFField


class Naturalidade(models.Model):
    """Compreende tanto a Naturalidade (Cidade/Estado) quanto a Nacionalidade."""

    pais = models.ForeignKey(
        "base.Pais", verbose_name=_("País"), on_delete=models.PROTECT
    )
    cidade_estado = models.CharField(_("Cidade/Estado"), max_length=150)
    nato = models.BooleanField(_("Nato"), default=True)
    pais_origem = models.ForeignKey(
        "base.Pais",
        verbose_name=_("País origem"),
        on_delete=models.PROTECT,
        related_name="pais_origem",
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.cidade_estado}, {self.pais}"


class PessoaFisicaQuerySet(models.QuerySet):
    NACIONAIS = dict(naturalidade__pais__sigla="BR")

    def nacionais(self):
        return self.filter(**self.NACIONAIS)

    def estrangeiros(self):
        return self.exclude(**self.NACIONAIS)


class PessoaFisicaManager(UserManager.from_queryset(PessoaFisicaQuerySet)):
    pass


class PessoaFisica(User):
    class Meta:
        ordering = ["-pk"]

    objects = PessoaFisicaManager()

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

    class Raca(models.IntegerChoices):
        BRANCO = 1, _("Branco")
        PRETO = 2, _("Preto, Negro ou Afrodescendente")
        PARDO = 3, _("Pardo, Mulato ou Mestiço")
        AMARELO = 4, _("Amarelo ou Indiano/Asiático")
        INDIGENA = 5, _("Indígena")

    cpf = BRCPFField(unique=True)
    sexo = models.CharField(max_length=1, choices=Genero.choices, null=True, blank=True)
    estado_civil = models.PositiveSmallIntegerField(
        choices=EstadoCivil.choices, null=True, blank=True
    )
    tipo_sanguineo = models.CharField(
        max_length=3, choices=TipoSanguineo.choices, blank=True, null=True
    )
    raca = models.PositiveSmallIntegerField(
        _("Raça"), choices=Raca.choices, null=True, blank=True
    )
    falecido = models.BooleanField(default=False)
    naturalidade = models.OneToOneField(
        "base.Naturalidade",
        verbose_name=_("Naturalidade"),
        on_delete=models.SET_NULL,
        null=True,
    )
    nome_mae = models.CharField(_("Nome da mãe"), max_length=150)
    nome_pai = models.CharField(_("Nome do pai"), max_length=150, null=True)

    dependentes = models.ManyToManyField(
        "self",
        through="base.RelacaoDependencia",
        through_fields=("responsavel", "dependente"),
        symmetrical=False,
    )

    @property
    def nome_completo(self):
        return self.get_full_name()

    @nome_completo.setter
    def nome_completo(self, value):
        splited = value.split()
        self.first_name = splited[0]
        self.last_name = " ".join(splited[1:])

    def save(self, *args, **kwargs) -> None:
        self.username = self.username or self.cpf
        return super().save(*args, **kwargs)


class DocumentoIdentificacao(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["pessoa_fisica_id", "tipo"],
                name="unique_pessoa_fisica_id_tipo",
            )
        ]

    class Tipo(models.TextChoices):
        RG = "RG", _("RG")
        CTPS = "CTPS", _("Cateira de Trabalho - CTPS")
        CNH = "CNH", _("Carteira Nacional de Habilitação - CNH")
        TITULO_ELEITOR = "TITULO_ELEITOR", _("Título de Eleitor")
        PASSAPORTE = "PASSAPORTE", _("Passaporte")
        RESERVISTA = "RESERV", _("Certificado de Reservista")
        CERTIDAO_NASCIMENTO = "CERT_NASC", _("Certidão de Nascimento")

    tipo = models.CharField(_("Tipo"), max_length=50, choices=Tipo.choices)

    pessoa_fisica = models.ForeignKey(
        "base.PessoaFisica", verbose_name=_("Pessoa Física"), on_delete=models.CASCADE
    )


class RelacaoDependencia(models.Model):
    """
    Descreve a relação de dependência e grau de parentesco
    entre dependente e responsável sendo ambos
    pessoas físicas
    """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["responsavel", "dependente"],
                name="relacao_resp_dep_uniq",
            )
        ]

    class Parentesco(models.IntegerChoices):
        """
        Grau de parentesco do responsável com o dependente
        """

        PAI_MAE = 1, _("Pai/Mãe")
        AVO = 2, _("Avó/Avó")
        TIO = 3, _("Tio/Tia")
        PRIMO = 4, _("Primo/Prima")
        OUTRO = 5, _("Outro")

    responsavel = models.ForeignKey(
        "base.PessoaFisica",
        verbose_name=_("Responsável"),
        on_delete=models.PROTECT,
        related_name="_deps",
    )
    dependente = models.ForeignKey(
        "base.PessoaFisica",
        verbose_name=_("Dependente"),
        on_delete=models.SET_NULL,
        related_name="responsaveis",
        null=True,
    )

    parentesco = models.PositiveSmallIntegerField(
        _("Parentesco"), choices=Parentesco.choices
    )
