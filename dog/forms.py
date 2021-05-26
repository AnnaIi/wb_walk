from django.forms import ModelForm
from .models import Dog


class DogForm(ModelForm):
    class Meta:
        model = Dog
        fields = ['breed', 'full_name', 'nickname', 'birthday', 'sex', 'is_sterilized', 'microchip_number']
