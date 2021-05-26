from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ShelterUser, Shelter, ShelterDog
from django.http import Http404
from django.shortcuts import redirect
from dog.models import Dog, DogAction
from dog.forms import DogForm
import datetime
from django.conf import settings
from calendar import monthrange


class QueryVolunteerView(LoginRequiredMixin, View):
    """
    вью для подачи заявки на волонтера
    """

    def get(self, request, shelter_id):
        try:
            shelter = Shelter.objects.get(pk=shelter_id)
        except Shelter.DoesNotExist:
            raise Http404('Приют отсутствует')
        ShelterUser.objects.get_or_create(shelter=shelter, user=request.user, access=ShelterUser.VOLUNTEER)
        return redirect('profile')


class DirectorMonitorView(LoginRequiredMixin, View):
    """
    главная страница директора
    """

    def get(self, request, shelter_id):
        try:
            shelter = Shelter.objects.get(pk=shelter_id)
        except Shelter.DoesNotExist:
            raise Http404('Приют отсутствует')
        user = ShelterUser.objects.get(shelter=shelter, user=request.user, access=ShelterUser.DIRECTOR)
        if not user:
            return redirect('profile')
        dogs = Dog.objects.filter(shelterdog__shelter=shelter)
        users = ShelterUser.objects.filter(shelter=shelter, access=ShelterUser.VOLUNTEER).order_by('is_active')
        return render(request, 'shelter/director_monitor.html', {'dogs': dogs, 'users': users, 'shelter': shelter})


class ConfirmVolunteerView(LoginRequiredMixin, View):
    """
    одобрение директором волонтера
    """

    def get(self, request, shelter_id, user_id):
        try:
            shelter = Shelter.objects.get(pk=shelter_id)
        except Shelter.DoesNotExist:
            raise Http404('Приют отсутствует')
        user = ShelterUser.objects.get(shelter=shelter, user=request.user, access=ShelterUser.DIRECTOR)
        if not user:
            return redirect('profile')
        ShelterUser.objects.filter(user_id=user_id, shelter=shelter, access=ShelterUser.VOLUNTEER).update(
            is_active=True)
        return redirect('director_monitor', shelter_id=shelter_id)


class DirectorEditDogView(LoginRequiredMixin, View):
    """
    вьюха для добавления собаки
    """

    def get(self, request, shelter_id, dog_id=None):
        try:
            shelter = Shelter.objects.get(pk=shelter_id)
        except Shelter.DoesNotExist:
            raise Http404('Приют отсутствует')
        user = ShelterUser.objects.get(shelter=shelter, user=request.user, access=ShelterUser.DIRECTOR)
        if not user:
            return redirect('profile')
        if dog_id:
            try:
                dog = Dog.objects.get(pk=dog_id)
            except Dog.DoesNotExist:
                raise Http404('Собака отсутствует')
        else:
            dog = None
        form = DogForm(instance=dog)
        return render(request, 'shelter/edit_dog.html', {'shelter': shelter, 'form': form})

    def post(self, request, shelter_id, dog_id=None):
        try:
            shelter = Shelter.objects.get(pk=shelter_id)
        except Shelter.DoesNotExist:
            raise Http404('Приют отсутствует')
        user = ShelterUser.objects.get(shelter=shelter, user=request.user, access=ShelterUser.DIRECTOR)
        if not user:
            return redirect('profile')
        if dog_id:
            try:
                dog = Dog.objects.get(pk=dog_id)
            except Dog.DoesNotExist:
                raise Http404('Собака отсутствует')
        else:
            dog = None
        form = DogForm(data=request.POST, instance=dog)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user
            post.save()
            if not dog_id:
                ShelterDog(shelter=shelter, dog=post, start=datetime.datetime.today()).save()
            return redirect('director_monitor', shelter.id)
        return render(request, 'shelter/edit_dog.html', {'shelter': shelter, 'form': form})


class GuardMonitorView(LoginRequiredMixin, View):
    """
    монитор охранника
    """

    def get(self, request, shelter_id):
        try:
            shelter = Shelter.objects.get(pk=shelter_id)
        except Shelter.DoesNotExist:
            raise Http404('Приют отсутствует')
        user = ShelterUser.objects.get(shelter=shelter, user=request.user, access=ShelterUser.GUARD)
        if not user:
            return redirect('profile')

        dogs = Dog.objects.filter(shelterdog__shelter=shelter)
        users = ShelterUser.objects.filter(shelter=shelter, access=ShelterUser.VOLUNTEER, is_active=True)
        dog_actions = DogAction.objects.filter(type=DogAction.WALK, dog__in=dogs, end_action__isnull=True).order_by(
            'user__username')
        user_not_show = []
        dog_not_show = []
        for da in dog_actions:
            user_not_show.append(da.user_id)
            dog_not_show.append(da.dog_id)

        return render(request, 'shelter/guard_monitor.html',
                      {'dogs': dogs, 'users': users, 'shelter': shelter, 'dog_actions': dog_actions,
                       'user_not_show': user_not_show, 'dog_not_show': dog_not_show})


class AddWalkView(LoginRequiredMixin, View):
    """
    добавляем событие прогулки собаки
    """

    def post(self, request, shelter_id):

        try:
            shelter = Shelter.objects.get(pk=shelter_id)
        except Shelter.DoesNotExist:
            raise Http404('Приют отсутствует')
        if not request.POST.get('user'):
            #  в случае, если не передали данные по пользователю, ничего не делаю
            return redirect('guard_monitor', shelter.id)
        user = ShelterUser.objects.get(shelter=shelter, user=request.user, access=ShelterUser.GUARD)
        if not user:
            return redirect('profile')
        try:
            user_ = ShelterUser.objects.get(shelter=shelter, user_id=request.POST.get('user'), is_active=True,
                                            access=ShelterUser.VOLUNTEER)
        except Shelter.DoesNotExist:
            raise Http404('Пользователь не имеет прав на прогулку')
        for dog_id in request.POST.getlist('dog'):
            if not ShelterDog.objects.filter(shelter=shelter, dog_id=dog_id):
                continue
            DogAction(type=DogAction.WALK, user=user_.user, dog_id=dog_id, start_action=datetime.datetime.now()).save()
        return redirect('guard_monitor', shelter.id)


class EndWalkView(LoginRequiredMixin, View):
    """
    заканчиваем событие прогулки собаки
    """

    def post(self, request, shelter_id):

        try:
            shelter = Shelter.objects.get(pk=shelter_id)
        except Shelter.DoesNotExist:
            raise Http404('Приют отсутствует')
        user = ShelterUser.objects.get(shelter=shelter, user=request.user, access=ShelterUser.GUARD)
        if not user:
            return redirect('profile')
        for d in request.POST.getlist('da'):
            if not DogAction.objects.filter(id=d, dog__shelterdog__shelter=shelter):
                continue
            DogAction.objects.filter(id=d).update(end_action=datetime.datetime.now())
        return redirect('guard_monitor', shelter.id)


class DirectorCalendar(LoginRequiredMixin, View):
    def get(self, request, shelter_id):
        try:
            shelter = Shelter.objects.get(pk=shelter_id)
        except Shelter.DoesNotExist:
            raise Http404('Приют отсутствует')
        user = ShelterUser.objects.get(shelter=shelter, user=request.user, access=ShelterUser.DIRECTOR)
        if not user:
            return redirect('profile')
        date_start = datetime.datetime.now()
        date_start = date_start.replace(day=1)
        start_date, days_count = monthrange(date_start.year, date_start.month)
        dogs = ShelterDog.objects.filter(shelter=shelter).all()
        dog_ids = []
        for dog in dogs:
            dog_ids.append(dog.dog_id)
        # показываю только законченные прогулки
        actions = DogAction.objects.filter(dog_id__in=dog_ids, start_action__gte=date_start,
                                           end_action__lt=date_start + datetime.timedelta(days=days_count))
        values = {}
        for action in actions:
            if not values.get(action.dog_id):
                values[action.dog_id] = {}
            if not values[action.dog_id].get(action.start_action.day):
                values[action.dog_id][action.start_action.day] = []
                values[action.dog_id][action.start_action.day].append(action)
        all_days = range(1, days_count)
        full_values = {}
        for dog in dogs:
            dog.values = []
            for day in all_days:
                try:
                    dog.values.append(values[dog.dog_id][day])
                except:
                    dog.values.append([])
        return render(request, 'shelter/director_calendar.html',
                      {'all_days': all_days, 'dogs': dogs, 'shelter': shelter, 'values': values,})
