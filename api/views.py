from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Sleep, Mood, Crisis
from .serializers import SleepSerializer, CreateSleepSerializer, MoodSerializer, CrisisSerializer
from django.views.generic import TemplateView


class SleepList(generics.ListCreateAPIView):
    queryset = Sleep.objects.all()  # get all objects from database
    # only logged in users can view and create data
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SleepSerializer
        return CreateSleepSerializer

    def perform_create(self, serializer):
        # set the owner of the sleep to the current user
        serializer.save(owner=self.request.user)


class ApiOverview(TemplateView):
    template_name = "index.html"


class MoodList(generics.ListCreateAPIView):
    queryset = Mood.objects.all()  # get all objects from database
    permission_classes = [IsAuthenticated]
    serializer_class = MoodSerializer

    def perform_create(self, serializer):
        # set the owner of the sleep to the current user
        serializer.save(owner=self.request.user)


class CrisisList(generics.ListCreateAPIView):
    queryset = Crisis.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CrisisSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
   
