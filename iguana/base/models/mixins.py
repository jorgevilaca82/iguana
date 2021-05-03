from django.db import models
from django.utils.translation import ugettext_lazy as _


class Timestamps(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
