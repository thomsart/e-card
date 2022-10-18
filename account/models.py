from django.db import models
from django.contrib.auth.models import User


class Phone(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=15)