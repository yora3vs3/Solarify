from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.


class UserProduction(models.Model):
    amount = models.FloatField()  # DECIMAL
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    Hybrid = models.CharField(max_length=266)

    def __str__(self):
        return self.Hybrid

    class Meta:
        ordering: ['-date']


class Hybrid(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
