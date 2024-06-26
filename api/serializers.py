from rest_framework import serializers

from .models import Sleep, Mood, Crisis, MoodImprovement, MedicalPart


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


class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = ['id', 'date', 'quality', 'notes', 'owner']


class CrisisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crisis
        fields = ['id', 'date', 'quality', 'notes', 'owner']


class MoodImprovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodImprovement
        fields = ['id', 'notes', 'owner']


class MedicalPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalPart
        fields = ['id', 'notes', 'owner']
