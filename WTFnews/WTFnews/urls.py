from django.contrib import admin
from django.urls import path, include

from perfil import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('profile/', include('perfil.urls')),
    path('post/', include('postagens.urls')),
    path('user/', include('usuarios.urls')),
]
