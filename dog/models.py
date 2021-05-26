from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class Breed(models.Model):
    """
        Порода собаки
    """

    class Meta:
        verbose_name = _('Breed')
        verbose_name_plural = _('Breeds')
        get_latest_by = ['sort', 'name']

    name = models.CharField(max_length=255, verbose_name=_('Breed'))
    sort = models.IntegerField(blank=True, default=0, verbose_name=_('Sorted'))

    def __str__(self):
        return self.name


class Dog(models.Model):
    """
        Карточка собаки
    """
    class Meta:
        verbose_name = _('Dog')
        verbose_name_plural = _('Dogs')

    FEMALE = 'f'
    MALE = 'm'
    SEX = [
        (FEMALE, _('Female')),
        (MALE, _('Mail'))
    ]
    breed = models.ForeignKey(Breed, null=True, on_delete=models.PROTECT, verbose_name=_('Breed'))
    full_name = models.CharField(max_length=255, verbose_name=_('Full name'))
    nickname = models.CharField(max_length=255, blank=True, verbose_name=_('Nickname'))
    birthday = models.DateField(verbose_name=_('Birthday'), null=True)
    sex = models.CharField(max_length=1, choices=SEX, default=FEMALE, verbose_name=_('Sex'))
    is_sterilized = models.BooleanField(blank=True, default=False, verbose_name=_('Is sterilized'))
    microchip_number = models.CharField(max_length=15, blank=True, default='', verbose_name=_('Microchip number'))
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, verbose_name=_('Creator'),
                                on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Updated'))

    def get_nickname(self):
        if not self.nickname:
            return self.full_name
        else:
            return self.nickname

    def __str__(self):
        return self.get_nickname()


class DogAction(models.Model):
    """
    действия над собакой
    """
    class Meta:
        verbose_name = _('Dog action')
        verbose_name_plural = _('Dog actions')
    WALK = 'w'  # прогулка с собакой
    USER_ACTION = 'u'  # пользовательская задача
    TYPE = [(WALK, _('Walk')),
            (USER_ACTION, _('User action'))]
    type = models.CharField(max_length=1, choices=TYPE)
    start_action = models.DateTimeField(verbose_name=_('Start action'))
    end_action = models.DateTimeField(blank=True, null=True, verbose_name=_('End action'))
    dog = models.ForeignKey(Dog, verbose_name=_('Dog'), on_delete=models.CASCADE,)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), on_delete=models.CASCADE,)