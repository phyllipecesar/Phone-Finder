from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
# Create your models here.


class Mobile(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField("phone's name", max_length=30)
    description = models.CharField("phone's description", max_length=30)
    identifier = models.CharField("phone's identifier", max_length=30)

    
