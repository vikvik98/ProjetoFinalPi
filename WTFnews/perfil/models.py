from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Perfil(models.Model):
    nome = models.CharField(max_length=250, null=False)
    usuario = models.OneToOneField(User, related_name='perfil', on_delete=models.CASCADE)

