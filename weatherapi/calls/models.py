from django.db import models

class City(models.Model):
    name = models.CharField(max_length=85)
    state = models.CharField(max_length=25)
    weather = models.CharField(max_length=15, default="None")
    temperature = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    wind = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
