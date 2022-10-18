from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):

    created_at = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=25)
    photo = models.ImageField(max_length=300, null=True, blank=True)
    description = models.TextField(max_length=135, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta():
        ordering = ['-user']