from django.urls import path
from .views import ProfileView, IndexView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', IndexView.as_view(), name="index")
    ]