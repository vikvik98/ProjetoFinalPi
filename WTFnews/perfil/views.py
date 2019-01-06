from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime

from django.views.generic.base import View

from perfil.models import *


# Create your views here.
from usuarios.forms import ChangePasswordForm


@login_required
def index(request):
    loged_profile = get_loged_profile(request)
    all_profiles = Profile.objects.exclude(name=loged_profile.name)
    loged_profile_friends = loged_profile.friends.all()
    profiles = []

    for profile in all_profiles:
        if profile not in loged_profile_friends:
            profiles.append(profile)

    return render(request, 'index.html', {'loged_profile': loged_profile,
                                          'profiles': profiles})


@login_required
def get_loged_profile(request):
    return request.user.profile




@login_required
def show_profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    loged_profile = get_loged_profile(request)
    is_friend = profile in loged_profile.friends.all()

    return render(request, 'profile.html',
                  {'profile': profile,
                   'is_friend':is_friend})


@login_required
def show_loged_profile(request):
    loged_profile = get_loged_profile(request)

    return render(request, 'loged_profile.html',
                  {'loged_profile': loged_profile})


@login_required
def invite(request, profile_id):
    guest_profile = Profile.objects.get(id=profile_id)
    loged_profile = get_loged_profile(request)

    if not Invitation.objects.filter(inviter=loged_profile, guest=guest_profile):
        loged_profile.invite(guest_profile, datetime.now())

    return redirect('index')


@login_required
def accept(request, invitation_id):
    invitation = Invitation.objects.get(id=invitation_id)
    loged_profile = get_loged_profile(request)
    loged_profile.accept_invitation(invitation)
    return redirect('index')


@login_required
def decline(request, invitation_id):
    invitation = Invitation.objects.get(id=invitation_id)
    loged_profile = get_loged_profile(request)
    loged_profile.decline_invitation(invitation)
    return redirect('index')


@login_required
def undo_friendship(request, profile_id):
    ex_friend = Profile.objects.get(id=profile_id)
    loged_profile = get_loged_profile(request)
    loged_profile.friends.remove(ex_friend)
    return redirect('index')



# def change_password(request):
#     loged_profile = get_loged_profile(request)
#     if request.method == 'POST':
#
#         change_passwordform = ChangePasswordForm(request.POST)
#
#         if change_passwordform.is_valid(loged_profile):
#             loged_profile.set_password(change_passwordform.cleaned_data['new_password'])
#             loged_profile.save()
#             return redirect('loged_profile')
#
#         else:
#             change_passwordform = ChangePasswordForm()
#             return render(request, 'change_password.html', {'change_passwordform':change_passwordform})
#
#     else:
#         change_passwordform = ChangePasswordForm()
#         return render(request, 'change_password.html', {'change_passwordform': change_passwordform})

class ChangePasswordView(View):

    template_name = 'change_password.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        loged_profile = get_loged_profile(request)
        change_passwordform = ChangePasswordForm(request.POST)
        change_passwordform.valid = True
        change_passwordform.is_valid()
        old_password = change_passwordform.cleaned_data['old_password']
        new_password = change_passwordform.cleaned_data['new_password']
        co_new_password = change_passwordform.cleaned_data['co_new_password']
        print(loged_profile.user.password)


        if not loged_profile.user.check_password(old_password):
            change_passwordform.add_error("The old password is not correct.")
            change_passwordform.valid = False


        if new_password != co_new_password:
            change_passwordform.add_error("The new password is not the same as the password confirmation.")
            change_passwordform.valid = False

        if change_passwordform.is_valid():
            loged_profile.user.set_password(change_passwordform.cleaned_data['new_password'])
            loged_profile.user.save()
            return redirect('show_loged_profile')

        return render(request, self.template_name, {'form': change_passwordform})