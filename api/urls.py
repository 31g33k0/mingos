from django.urls import path
from .views import SleepList
from .views import ApiOverview


urlpatterns = [
    path('sleep/', SleepList.as_view(), name='sleep-list'),
    path('', ApiOverview.as_view(), name='index')
]
