from django.db import models

# Create your models here.
from perfil.models import Profile


class Post(models.Model):
    content = models.CharField(max_length=500)
    date = models.DateField()

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')