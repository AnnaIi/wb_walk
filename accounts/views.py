from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from shelter.models import Shelter, ShelterUser


class ProfileView(LoginRequiredMixin, View):
    """
    отображение профиля пользователя
    """

    def get(self, request, *args, **kwargs):
        shelters = Shelter.objects.all()
        for shelter in shelters:
            # получаю все роли для этого пользователя
            res = ShelterUser.objects.filter(user=request.user, shelter=shelter)
            if not res:
                # если нет ролей
                shelter.no_info = True
            else:
                # если есть то пихаю в roles
                shelter.roles = res
        return render(request, 'accounts/profile.html', {'shelters': shelters})


class IndexView(View):
    """
    отображение профиля пользователя
    """

    def get(self, request, *args, **kwargs):

        return render(request, 'default_index.html', )