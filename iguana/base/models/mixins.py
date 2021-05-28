import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class HasSiglaMixin(models.Model):
    """Possiu atributo sigla"""

    class Meta:
        abstract = True

    sigla = models.CharField(_("Sigla"), max_length=15)

    def __str__(self) -> str:
        return self.sigla


class HasNomeMixin(models.Model):
    """Possiu atributo nome"""

    class Meta:
        abstract = True

    nome = models.CharField(_("Nome"), max_length=150)

    def __str__(self) -> str:
        return self.nome


class HasTituloMixin(models.Model):
    """
    Models que possuem um atributo Título
    """

    class Meta:
        abstract = True

    titulo = models.CharField(_("Título"), max_length=150)

    def __str__(self):
        return self.titulo


class HasDescricaoMixin(models.Model):
    """Possui atributo descrição"""

    class Meta:
        abstract = True

    descricao = models.CharField(_("Descrição"), max_length=255)

    def __str__(self) -> str:
        return self.descricao


class HasObservacaoMixin(models.Model):
    """Possiu atributo observação"""

    class Meta:
        abstract = True

    observacao = models.TextField(_("Observação"), null=True, blank=True)

    def __str__(self) -> str:
        return self.observacao


class Timestamps(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)


class UUIDMixin(models.Model):
    """
    Models que precisam de UUID como chave primária
    """

    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class HasDateTimeRangeMixin(models.Model):
    """Possui data de inicio e fim"""

    class Meta:
        abstract = True

    started_at = models.DateTimeField(_("Started At"))
    ended_at = models.DateTimeField(_("Ended At"), blank=True, null=True)

    def is_datetime_in_range(self, datetime):
        if self.ended_at is None:
            return True
        return self.started_at < datetime < self.ended_at

    def is_now_in_range(self):
        return self.is_datetime_in_range(timezone.localtime())


class HasIsActiveFlagMixin(models.Model):
    """Possui atributo flag de ativo"""

    class Meta:
        abstract = True

    is_active = models.BooleanField(_("Active"), default=True)

    def activate(self):
        self.is_active = True

    def inactivate(self):
        self.is_active = False


class GeoLocationMixin(models.Model):
    """Possui geolocalização (lat, long)"""

    class Meta:
        abstract = True

    latitude = models.FloatField(
        _("Latitude"), validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )

    longitude = models.FloatField(
        _("Longitude"), validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )

    def get_location(self):
        return self.latitude, self.longitude
