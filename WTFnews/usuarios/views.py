from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.base import View

from perfil.models import Profile
from usuarios.forms import SingUpForm, ChangePasswordForm


class SingUpView(View):
    template_name = 'register.html'

    def get(self, request):
        return render(request, self.template_name)

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


class LoginCustomView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')

        if getUser(request, username):
            return redirect('activate_profile', getUser(request, username).id)

        return redirect('login')


class ChangePasswordView(View):
    template_name = 'change_password.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        logged_profile = request.user.profile
        change_passwordform = ChangePasswordForm(request.POST)
        change_passwordform.valid = True
        change_passwordform.is_valid()
        old_password = change_passwordform.cleaned_data['old_password']
        new_password = change_passwordform.cleaned_data['new_password']
        co_new_password = change_passwordform.cleaned_data['co_new_password']

        if not logged_profile.user.check_password(old_password):
            change_passwordform.add_error("The old password is not correct.")
            change_passwordform.valid = False

        if new_password != co_new_password:
            change_passwordform.add_error("The new password is not the same as the password confirmation.")
            change_passwordform.valid = False

        if change_passwordform.is_valid():
            logged_profile.user.set_password(change_passwordform.cleaned_data['new_password'])
            logged_profile.user.save()
            update_session_auth_hash(request, logged_profile.user)
            return redirect('show_logged_profile')

        return render(request, self.template_name, {'form': change_passwordform})


def activate_profile(request, id):
    user = User.objects.get(id=id)

    return render(request, 'activate_profile.html', {'user': user})


def enable(request, id):
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()
    return redirect('index')


def getUser(request, username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None
