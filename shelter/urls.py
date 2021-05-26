from django.urls import path
from .views import QueryVolunteerView, DirectorMonitorView, ConfirmVolunteerView, DirectorEditDogView, GuardMonitorView, \
    AddWalkView, EndWalkView, DirectorCalendar

urlpatterns = [
    path('query_volunteer/<int:shelter_id>', QueryVolunteerView.as_view(), name='query_volunteer'),
    path('director_monitor/<int:shelter_id>', DirectorMonitorView.as_view(), name='director_monitor'),
    path('confirm_volunteer/<int:shelter_id>/<int:user_id>', ConfirmVolunteerView.as_view(), name='confirm_volunteer'),
    path('director_add_dog/<int:shelter_id>', DirectorEditDogView.as_view(), name='director_add_dog'),
    path('director_edit_dog/<int:shelter_id>/<int:dog_id>', DirectorEditDogView.as_view(), name='director_edit_dog'),
    path('guard_monitor/<int:shelter_id>', GuardMonitorView.as_view(), name='guard_monitor'),
    path('add_walk/<int:shelter_id>', AddWalkView.as_view(), name='add_walk'),
    path('end_walk/<int:shelter_id>', EndWalkView.as_view(), name='end_walk'),
    path('director_calendar/<int:shelter_id>', DirectorCalendar.as_view(), name='director_calendar'),
]
