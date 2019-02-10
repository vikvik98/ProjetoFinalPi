from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.generic.base import View

from perfil.models import Profile
from usuarios.forms import SingUpForm, ChangePasswordForm, CustomAuthenticationForm


class SingUpView(View):
    template_name = 'register.html'

    def get(self, request):
        form = SingUpForm()
        return render(request, self.template_name, {'form': form})

    @transaction.atomic
    def post(self, request):
        form = SingUpForm(request.POST)
        if form.is_valid():
            data_form = form.cleaned_data
            user = User.objects.create_user(username=data_form['name'],
                                            email=data_form['email'],
                                            password=data_form['password'])

            profile = Profile(name=data_form['name'], user=user)
            profile.save()
            return redirect('login')

        return render(request, self.template_name, {'form': form})


class LoginCustomView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'login.html'

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active:
            return redirect('activate_profile', user.id)
        login(self.request, user)
        return redirect(self.get_success_url())


class ChangePasswordView(View):
    template_name = 'change_password.html'

    def get(self, request):
        form = ChangePasswordForm(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ChangePasswordForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            return redirect('show_logged_profile')

        return render(request, self.template_name, {'form': form})


def activate_profile(request, id):
    user = User.objects.get(id=id)
    login(request, user)

    return render(request, 'activate_profile.html', {'user': user})


def enable(request, id):
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()
    login(request, user)
    return redirect('index')


def getUser(request, username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None
