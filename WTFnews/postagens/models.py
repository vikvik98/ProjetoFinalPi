from django.db import models
from pyuploadcare.dj.models import ImageField

from perfil.models import Profile


class Post(models.Model):
    content = models.CharField(max_length=500, null=True)
    date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='posts')
    photo = ImageField(null=True, blank=True, manual_crop="")




    def delete(self, using=None, keep_parents=False):
        if self.photo:
            self.photo.delete()
        return super(Post, self).delete()


class Commentary(models.Model):
    message = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
