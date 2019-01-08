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
from perfil.views import ChangePasswordView, AddPostView
from django.contrib.auth import views as v
from perfil import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('sign-up/', SingUpView.as_view(), name='signup'),
    path('add-post/', AddPostView.as_view(), name='add_post'),
    path('password-reset/', v.PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', v.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         v.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/', v.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('login/', v.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', v.LogoutView.as_view(template_name='login.html'), name='logout'),
    path('profile/<int:profile_id>', views.show_profile, name='show_profile'),
    path('loged-profile/', views.show_loged_profile, name='show_loged_profile'),
    path('loged-profile/change-password', login_required(ChangePasswordView.as_view()), name='change_password'),
    path('profile/<int:profile_id>/invite', views.invite, name='invite'),
    path('invite/<int:invitation_id>/cancel', views.cancel_invitation, name='cancel_invitation'),
    path('profile/<int:profile_id>/remove', views.undo_friendship, name='undo_friendship'),
    path('invitation/<int:invitation_id>/accept', views.accept, name='accept'),
    path('invitation/<int:invitation_id>/decline', views.decline, name='decline'),
    path('profile/<int:profile_id>/make-superuser', views.make_superuser, name='make_superuser'),
    path('profile-logged/give-up-superuser', views.give_up_superuser, name='give_up_superuser'),
    path('delete/<int:post_id>', views.delete_post, name='delete_post'),
    path('block-user/<int:profile_id>', views.block_user, name='block_user'),
    path('unblock-user/<int:profile_id>', views.unblock_user, name='unblock_user'),
    path('blockers-profile/', views.show_blockers_profile, name='blockers_profile'),
    path('search-profile/', views.search_profile, name='search_profile'),


]
