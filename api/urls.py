from django.urls import path
from .views import SleepList, MoodList, ApiOverview, CrisisList, MoodImprovementList


urlpatterns = [
    path('sleep/', SleepList.as_view(), name='sleep-list'),
    path('', ApiOverview.as_view(), name='index'),
    path('mood/', MoodList.as_view(), name='mood-list'),
    path('crisis/', CrisisList.as_view(), name='crisis-list'),
    path('moodimprovement/', MoodImprovementList.as_view(), name='mood-improvement'),
]
