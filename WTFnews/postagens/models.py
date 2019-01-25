from django.db import models

from perfil.models import Profile


class Post(models.Model):
    content = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='posts')
