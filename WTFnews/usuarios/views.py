from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.models import User
from perfil.models import Profile
from usuarios.forms import SingUpForm
from django.contrib.auth import authenticate, login



class SingUpView(View):

    template_name = 'register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = SingUpForm(request.POST)
        if form.is_valid():
            data_form = form.cleaned_data
            user = User.objects.create_user(username= data_form['name'],
                                            email= data_form['email'],
                                            password= data_form['password'])

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
            login(request,user)
            return redirect('index')

        if getUser(request, username):
            return redirect('activate_profile', getUser(request, username).id)

        return redirect('login')

def activate_profile(request, id):
    user = User.objects.get(id=id)

    return render(request, 'activate_profile.html' , {'user': user})

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