from django.contrib.auth.models import AbstractUser
from iguana.base.models.mixins import Timestamps


class User(Timestamps, AbstractUser):
    pass
