from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Sleep
from .serializers import SleepSerializer, CreateSleepSerializer
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
