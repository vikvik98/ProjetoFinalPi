from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from perfil.models import *


# Create your views here.

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