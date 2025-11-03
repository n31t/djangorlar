from django.urls import path
from . import views

urlpatterns = [
    path('', view = views.home, name='home'),
    path('users/', view = views.users, name='users'),
    path('city-time/', view = views.city_time, name='city_time'),
    path('cnt/', view = views.counter, name='counter'),
]