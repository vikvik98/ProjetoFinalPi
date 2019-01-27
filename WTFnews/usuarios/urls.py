from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as v
from django.urls import path

from usuarios.views import SingUpView, LoginCustomView, ChangePasswordView, enable

urlpatterns = [
    path('sign-up/', SingUpView.as_view(), name='signup'),
    path('login/', LoginCustomView.as_view(template_name='login.html'), name='login'),
    path('logout/', v.LogoutView.as_view(template_name='login.html'), name='logout'),
    path('password-reset/', v.PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', v.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', v.PasswordResetConfirmView
         .as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', v.PasswordResetCompleteView
         .as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('logged/change-password', login_required(ChangePasswordView.as_view()), name='change_password'),
    path('enable/<int:id>', enable, name='enable'),
]
