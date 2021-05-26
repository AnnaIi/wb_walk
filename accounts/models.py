from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    # переопределенны класс пользователя
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
