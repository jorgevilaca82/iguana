from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from iguana.base.models.mixins import Timestamps
from iguana.base.models.user import UserRelatedModel
from localflavor.br.models import BRPostalCodeField, BRStateField


class Endereco(UserRelatedModel, Timestamps, models.Model):
    class Tipo(models.IntegerChoices):
        COMERCIAL = 1, _("Comercial")
        RESIDENCIAL = 2, _("Residencial")
        RURAL = 3, _("Rural")

    tipo = models.IntegerField(choices=Tipo.choices)
    cep = BRPostalCodeField()
    logradouro = models.CharField(max_length=255)
    bairro = models.CharField(max_length=120)
    numero = models.CharField(max_length=120)
    cidade = models.CharField(max_length=120)
    uf = BRStateField()
    complemento = models.CharField(max_length=255, blank=True, null=True)
    principal = models.BooleanField(default=False)


@receiver(signals.post_save, sender=Endereco)
def garante_unico_endereco_principal_por_usurio_post_save_receiver(
    sender, instance=None, **kwargs
):
    """
    Garente que entre os endereços cadastrados para o usuário
    exista apenas um principal
    """
    if instance.principal:
        instance.user.base_endereco_related.exclude(pk=instance.pk).update(
            principal=False
        )
