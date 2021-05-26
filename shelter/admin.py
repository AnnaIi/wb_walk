from django.contrib import admin
from .models import Shelter, ShelterDog, ShelterUser

@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    pass

@admin.register(ShelterDog)
class ShelterDogAdmin(admin.ModelAdmin):
    pass

@admin.register(ShelterUser)
class ShelterUserAdmin(admin.ModelAdmin):
    pass

