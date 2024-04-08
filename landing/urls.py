from django.urls import include, path
from .views import Landing

urlpatterns = [
    path('', Landing.as_view(), name='landingPage'),
]
