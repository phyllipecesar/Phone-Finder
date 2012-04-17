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
