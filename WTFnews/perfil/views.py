from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.db.models import Q
from datetime import datetime

from perfil.models import Profile, Invitation
from postagens.forms import AddPostForm
from postagens.models import Post
from usuarios.forms import ChangePasswordForm


# Create your views here.



@login_required
def index(request):

    logged_profile = get_loged_profile(request)
    logged_profile_friends = logged_profile.friends.all()
    inviters_profiles = logged_profile.inviters_profiles.all()
    guests_profiles = logged_profile.guests_profiles.all()
    blocked_list = logged_profile.blocked.all()
    blockers_list = logged_profile.blockers.all()


    suggested_profiles = Profile.objects.exclude(id__in=inviters_profiles)\
        .exclude(id__in=guests_profiles)\
        .exclude(id__in=logged_profile_friends) \
        .exclude(id__in=blocked_list)\
        .exclude(id__in=blockers_list)\
        .exclude(id=logged_profile.id)\


    sent_invitations = logged_profile.sent_invitations.all()
    received_invitations = logged_profile.received_invitations.all()
    posts = get_posts(request)
    search_term = ''
    if 'search' in request.GET:
        search_term = request.GET['search']
        search_profiles = Profile.objects.filter(name__icontains=search_term).exclude(id__in=blockers_list)

        return render(request, 'search_profile.html', {'search_profiles': search_profiles, 'search_term': search_term})






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
    posts = []
    loged_profile = get_loged_profile(request)
    friends = loged_profile.friends.all()
    for friend in friends:
        for post in friend.posts.all():
            posts.append(post)

    for post in loged_profile.posts.all():
        posts.append(post)

    return posts


@login_required
def search_profile(request):
    search_term = ''
    if 'search' in request.GET:
        search_term = request.GET['search']
        search_profiles = Profile.objects.filter(name__icontains=search_term)

        return render(request, 'search_profile', {'search_profiles': search_profiles, 'search_term':search_term})




@login_required
def get_loged_profile(request):
    return request.user.profile


@login_required
def show_profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    logged_profile = get_loged_profile(request)

    if profile.id == logged_profile.id:
        return show_loged_profile(request)

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
                   'is_inviter': is_inviter})


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



class AddPostView(View):

    template_post = 'add_post.html'

    def get(self,request):
        return render(request, self.template_post)

    def post(self, request):
        add_postform = AddPostForm(request.POST)
        if add_postform.is_valid():
            print(add_postform.cleaned_data['text'])
            post = Post(content=add_postform.cleaned_data['text'], date=datetime.now())
            post.profile = get_loged_profile(request)
            post.save()
            return redirect('index')

        return render(request, self.template_post, {'form': add_postform})




@login_required
def make_superuser(request, profile_id):
    if not request.user.is_superuser:
        raise PermissionError

    profile = Profile.objects.get(id=profile_id)
    profile.change_to_superuser()

    return redirect('show_profile', profile_id)

@login_required
def give_up_superuser(request):
    request.user.is_superuser = False
    request.user.save()

    return redirect('show_loged_profile')

@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    loged_profile = get_loged_profile(request)
    loged_profile.delete_post(post)
    return redirect('index')

@login_required
def block_user(request, profile_id):
    profile_blocked = Profile.objects.get(id=profile_id)
    loged_profile = get_loged_profile(request)
    loged_profile.blocked.add(profile_blocked)
    undo_friendship(request,profile_blocked.id)
    return redirect('index')

@login_required
def unblock_user(request, profile_id):
    unblock_profile = Profile.objects.get(id=profile_id)
    logged_profile = get_loged_profile(request)
    logged_profile.blocked.remove(unblock_profile)
    

    return redirect('index')

@login_required
def show_blockers_profile(request):
    return render(request, 'blockers_profile.html')