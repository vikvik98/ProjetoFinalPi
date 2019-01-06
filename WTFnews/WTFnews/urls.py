"""WTFnews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from usuarios.views import SingUpView
from django.contrib.auth import views as v
from perfil import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('sign-up/', SingUpView.as_view(), name='signup'),
    path('login/', v.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', v.LogoutView.as_view(template_name='login.html'), name='logout'),
    path('profile/<int:profile_id>', views.show_profile, name='show_profile'),
    path('loged-profile/', views.show_loged_profile, name='show_loged_profile'),
    path('profile/<int:profile_id>/invite', views.invite, name='invite'),
    path('profile/<int:profile_id>/remove', views.undo_friendship, name='undo_friendship'),
    path('invitation/<int:invitation_id>/accept', views.accept, name='accept'),
    path('invitation/<int:invitation_id>/decline', views.decline, name='decline'),


]
