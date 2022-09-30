from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Card(models.Model):
    created_at = models.DateField(auto_now_add=True)
    profession = models.CharField(max_length=30, null=False, default="profession")
    description = models.TextField(max_length=210, null=True, blank=True)
    phone = models.CharField(max_length=15, null=False, default="0646756938")
    email = models.EmailField(max_length=254)
    photo = models.ImageField(max_length=300, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta():
        ordering = ['-user']