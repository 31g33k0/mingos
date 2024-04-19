from django.contrib import admin
from .models import Sleep, Mood, Crisis, MoodImprovement

admin.site.register(Sleep)
admin.site.register(Mood)
admin.site.register(Crisis)
admin.site.register(MoodImprovement)
