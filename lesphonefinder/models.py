from django.db import models

class Location(models.Model):
    lati = models.FloatField()
    longi = models.FloatField()
