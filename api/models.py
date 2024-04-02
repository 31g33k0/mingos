from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator


class Sleep(models.Model):
    date = models.DateTimeField(default=datetime.now, blank=True)
    hours = models.FloatField(null=False, blank=False)
    quality = models.IntegerField(default=5, validators=[MinValueValidator(0),
                                                         MaxValueValidator(5)])
    notes = models.TextField(null=False, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              null=False, blank=False)

    # This is the readable representation of the model, otherwise
    # it would just be displayed as 'Sleep object(1)'
    def __str__(self):
        return f'{self.date} - {self.hours} hours'
