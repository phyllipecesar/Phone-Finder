from django.db import models
from lesphonefinder.accounts.models import Mobile

class Location(models.Model):
    lati = models.FloatField()
    longi = models.FloatField()
    modification_date = models.DateTimeField(auto_now_add=True)
    mobile = models.ForeignKey(Mobile)

    def get_description(self):
        return u"""<b>Latitude:</b> %s ; <b>Longitude:</b> %s<br/><b>Date:</b> %s
""" % (self.lati, self.longi, self.modification_date)

MAXIMUM_LEN_LOCATIONS = 10
ACTIVITIES = [ 0, 1 ]
activities_name = [ 'Take a Photo', 'Play a sound' ]


class Activity(models.Model):

    mobile = models.ForeignKey(Mobile)
    activity = models.IntegerField()
    def description(self):
        return activities_name[self.activity]
