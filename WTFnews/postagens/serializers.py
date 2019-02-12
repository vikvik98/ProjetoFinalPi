from rest_framework import serializers
from postagens.models import *
from perfil.models import *

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('url', 'pk', 'name', 'posts')

class PostSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.ReadOnlyField(source='profile.name')
    class Meta:
        model = Post
        fields = ('url', 'pk', 'profile', 'content', 'date', 'photo')