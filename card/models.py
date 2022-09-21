from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Card(models.Model):
    created_at = models.DateField(auto_now_add=True)
    profession = models.CharField(max_length=20, null=False, default="profession")
    phone = models.CharField(max_length=15, null=False, default="0646756938")
    email = models.EmailField(max_length=254)
    photo = models.ImageField(max_length=20, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta():
        ordering = ['user']