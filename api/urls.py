from django.urls import path
from .views import SleepList

urlpatterns = [
    path('sleep/', SleepList.as_view(), name='sleep-list'),
]
