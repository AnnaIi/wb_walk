from django.contrib import admin
from .models import Breed, Dog, DogAction


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    pass


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    pass


@admin.register(DogAction)
class DogActionAdmin(admin.ModelAdmin):
    pass
