from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from datetime import datetime

from perfil.models import Profile, Invitation


# Create your views here.
from usuarios.forms import ChangePasswordForm


@login_required
def index(request):

    logged_profile = get_loged_profile(request)
    logged_profile_friends = logged_profile.friends.all()
    inviters_profiles = logged_profile.inviters_profiles.all()
    guests_profiles = logged_profile.guests_profiles.all()

    suggested_profiles = Profile.objects.exclude(id__in=inviters_profiles)\
        .exclude(id__in=guests_profiles)\
        .exclude(id__in=logged_profile_friends)\
        .exclude(id=logged_profile.id)

    sent_invitations = logged_profile.sent_invitations.all()
    received_invitations = logged_profile.received_invitations.all()

    return render(request, 'index.html', {
        'logged_profile': logged_profile,
        'suggested_profiles': suggested_profiles,
        'sent_invitations': sent_invitations,
        'received_invitations': received_invitations,
        'logged_profile_friends': logged_profile_friends
    })


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

    loged_profile.invite(guest_profile, datetime.now())

    return redirect('index')


def cancel_invitation(request, invitation_id):
    invitation = Invitation.objects.get(id=invitation_id)
    logged_profile = get_loged_profile(request)

    logged_profile.cancel_invitation(invitation)

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