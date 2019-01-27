from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic.base import View

from perfil.forms import DisableProfileForm
from perfil.models import Profile, Invitation
from postagens.models import Post
from django.core.paginator import Paginator


@login_required
def index(request):
    logged_profile = get_logged_profile(request)
    logged_profile_friends = logged_profile.friends.all()
    inviters_profiles = logged_profile.inviters_profiles.all()
    guests_profiles = logged_profile.guests_profiles.all()
    blocked_list = logged_profile.blocked.all()
    blockers_list = logged_profile.blockers.all()

    suggested_profiles = Profile.objects.exclude(id__in=inviters_profiles) \
        .exclude(id__in=guests_profiles) \
        .exclude(id__in=logged_profile_friends) \
        .exclude(id__in=blocked_list) \
        .exclude(id__in=blockers_list) \
        .exclude(id=logged_profile.id)

    sent_invitations = logged_profile.sent_invitations.all()
    received_invitations = logged_profile.received_invitations.all()
    posts = get_posts(request)
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    if 'search' in request.GET:
        search_term = request.GET['search']
        search_profiles = Profile.objects.filter(name__icontains=search_term) \
            .exclude(id__in=blockers_list)

        return render(request, 'search_profile.html',
                      {'search_profiles': search_profiles,
                       'search_term': search_term})

    return render(request, 'index.html', {
        'logged_profile': logged_profile,
        'suggested_profiles': suggested_profiles,
        'sent_invitations': sent_invitations,
        'received_invitations': received_invitations,
        'logged_profile_friends': logged_profile_friends,
        'posts': posts
    })


@login_required
def get_posts(request):
    logged_profile = get_logged_profile(request)
    friends = logged_profile.friends.all()
    posts = Post.objects.filter(
        Q(profile__in=friends) | Q(profile=logged_profile)
    ).order_by('-date')

    return posts


@login_required
def search_profile(request):
    if 'search' in request.GET:
        search_term = request.GET['search']
        search_profiles = Profile.objects.filter(name__icontains=search_term)

        return render(request, 'search_profile',
                      {'search_profiles': search_profiles,
                       'search_term': search_term})


@login_required
def get_logged_profile(request):
    return request.user.profile


@login_required
def show_profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    logged_profile = get_logged_profile(request)
    posts = profile.posts.all()
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    if profile.id == logged_profile.id:
        return show_logged_profile(request)

    if profile in logged_profile.blockers.all():
        return show_blockers_profile(request)

    invitation = Invitation.objects.filter(
        (Q(guest=profile) & Q(inviter=logged_profile)) |
        (Q(guest=logged_profile) & Q(inviter=profile))
    )

    is_friend = profile in logged_profile.friends.all()
    is_guest = False
    is_inviter = False

    if not is_friend and invitation:
        invitation = invitation[0]
        if invitation.guest == profile:
            is_guest = True
        elif invitation.inviter == profile:
            is_inviter = True

    return render(request, 'profile.html',
                  {'profile': profile,
                   'logged_profile': logged_profile,
                   'invitation': invitation,
                   'is_friend': is_friend,
                   'is_guest': is_guest,
                   'is_inviter': is_inviter,
                   'posts': posts})


@login_required
def show_logged_profile(request):
    logged_profile = get_logged_profile(request)
    friends_list = logged_profile.friends.all()
    blocked_list = logged_profile.blocked.all()
    all_profiles = Profile.objects.exclude(id=logged_profile.id)
    posts = logged_profile.posts.all()
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'logged_profile.html',
                  {'logged_profile': logged_profile,
                   "friends_list": friends_list,
                   "blocked_list": blocked_list,
                   "all_profiles": all_profiles,
                   'posts':posts})


@login_required
def invite(request, profile_id):
    guest_profile = Profile.objects.get(id=profile_id)
    logged_profile = get_logged_profile(request)
    logged_profile.invite(guest_profile)
    return redirect('index')


@login_required
def cancel_invitation(request, invitation_id):
    invitation = Invitation.objects.get(id=invitation_id)
    logged_profile = get_logged_profile(request)
    invitation.cancel(logged_profile)
    return redirect('index')


@login_required
@transaction.atomic
def accept(request, invitation_id):
    invitation = Invitation.objects.get(id=invitation_id)
    logged_profile = get_logged_profile(request)
    invitation.accept(logged_profile)
    return redirect('index')


@login_required
def decline(request, invitation_id):
    invitation = Invitation.objects.get(id=invitation_id)
    logged_profile = get_logged_profile(request)
    invitation.decline(logged_profile)
    return redirect('index')


@login_required
def undo_friendship(request, profile_id):
    ex_friend = Profile.objects.get(id=profile_id)
    logged_profile = get_logged_profile(request)
    logged_profile.friends.remove(ex_friend)
    return redirect('index')


class DisableProfileView(View):
    template_post = 'disable_profile.html'

    def get(self, request):
        return render(request, self.template_post)

    def post(self, request):
        disable_profile = DisableProfileForm(request.POST)
        logged_profile = get_logged_profile(request)
        if disable_profile.is_valid():
            logged_profile.reason_disable = disable_profile.cleaned_data['text']
            logged_profile.save()
            logged_profile.user.is_active = False
            logged_profile.user.save()
            return redirect('logout')

        return render(request, self.template_post, {'form': disable_profile})


@login_required
def make_superuser(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    logged_profile = get_logged_profile(request)
    logged_profile.change_to_superuser(profile)

    return redirect('show_profile', profile_id)


@login_required
def give_up_superuser(request):
    request.user.is_superuser = False
    request.user.save()

    return redirect('show_logged_profile')


@login_required
@transaction.atomic
def block_user(request, profile_id):
    blocked_profile = Profile.objects.get(id=profile_id)
    logged_profile = get_logged_profile(request)

    if blocked_profile in logged_profile.friends.all():
        undo_friendship(request, blocked_profile.id)

    elif blocked_profile in logged_profile.guests_profiles.all():
        invitation = logged_profile.sent_invitations \
            .get(guest=blocked_profile)

        if invitation:
            invitation.cancel(logged_profile)

    elif blocked_profile in logged_profile.inviters_profiles.all():
        invitation = logged_profile.received_invitations \
            .get(inviter=blocked_profile)

        if invitation:
            invitation.decline(logged_profile)

    logged_profile.blocked.add(blocked_profile)
    return redirect('show_profile', blocked_profile.id)


@login_required
def unblock_user(request, profile_id):
    unblock_profile = Profile.objects.get(id=profile_id)
    logged_profile = get_logged_profile(request)
    logged_profile.blocked.remove(unblock_profile)

    return redirect('show_profile', unblock_profile.id)


@login_required
def show_blockers_profile(request):
    return render(request, 'blockers_profile.html')
