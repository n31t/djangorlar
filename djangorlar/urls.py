from django.contrib import admin
from django.urls import path

from apps.tasks.views import (
    welcome_view,
    users_view,
    city_time_view,
    counter_view,
    counter_increment,
    counter_reset,
    get_time_api,
    hello_name_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome_view, name='welcome'),
    path('users/', users_view, name='users'),
    path('city-time/', city_time_view, name='city_time'),
    path('cnt/', counter_view, name='counter'),
    path('cnt/increment/', counter_increment, name='counter_increment'),
    path('cnt/reset/', counter_reset, name='counter_reset'),
    path('api/time/', get_time_api, name='get_time_api'),
    # Legacy route
    path('hello/', hello_name_view, name='hello_name_view')
]
