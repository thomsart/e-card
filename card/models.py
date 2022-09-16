from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Photo(models.model):
    created_at = models.DateField(auto_now_add=True)
    photo = models.ImageField(height_field="H", width_field="w", max_length=10, null=True)
    user = models.ForeignKey(User)