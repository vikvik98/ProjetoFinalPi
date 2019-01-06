from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.models import User
from perfil.models import Profile
from usuarios.forms import SingUpForm



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