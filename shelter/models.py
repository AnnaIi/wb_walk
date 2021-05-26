from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from dog.models import Dog


class Shelter(models.Model):
    """
    класс приюта
    """
    class Meta:
        verbose_name = _('Shelter')
        verbose_name_plural = _('Shelters')
    name = models.CharField(max_length=255, verbose_name=_('Shelter name'))
    description = models.TextField(blank=True, default='', verbose_name=_('Description'))
    def __str__(self):
        return self.name



class ShelterDog(models.Model):
    """
    связь между приютом и собакой
    """
    class Meta:
        verbose_name = _('Shelter dog')
        verbose_name_plural = _('Shelter dog')
    start = models.DateField(verbose_name=_('Start'))
    end = models.DateField(null=True, verbose_name=_('End'))
    shelter = models.ForeignKey(Shelter, verbose_name=_('Shelter'), on_delete=models.CASCADE, )
    dog = models.ForeignKey(Dog, verbose_name=_('Dog'), on_delete=models.CASCADE, )


class ShelterUser(models.Model):
    """
    связь между приютом и пользователем
    """
    class Meta:
        verbose_name = _('Shelter user')
        verbose_name_plural = _('Shelter user')
    DIRECTOR = 'd'  # директор, может добавлять собак
    GUARD = 'g'  # охранник, может выпускать/принимать собак с прогулки
    VOLUNTEER = 'v'  # волонтер, может гулять собаку из этого приюта

    ACCESS = [
        (DIRECTOR, _('Director')),
        (GUARD, _('Guard')),
        (VOLUNTEER, _('Volunteer')),
    ]
    shelter = models.ForeignKey(Shelter, verbose_name=_('Shelter'), on_delete=models.CASCADE, )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), on_delete=models.CASCADE,)
    access = models.CharField(max_length=3, choices=ACCESS, default=VOLUNTEER, verbose_name=_('Access'))
    is_active = models.BooleanField(blank=True, default=False, verbose_name=_('Is_active'))
    def __str__(self):
        return f"{self.user.username} / {self.shelter.name} ({self.access})"
