from rest_framework import serializers

from .models import Sleep


class SleepSerializer(serializers.ModelSerializer):
    class Meta:
        # The required fields are the model, and the fields that will be
        # displayed back to the user.
        model = Sleep
        fields = ['id', 'date', 'hours', 'quality', 'notes', 'owner']


class CreateSleepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sleep
        # We do not want to let the user control the owner field.
        fields = ['date', 'hours', 'quality', 'notes']
