from django.db import models, IntegrityError
from django.utils import timezone
from django.contrib.auth.models import User


class Profile(models.Model):

    name = models.CharField(max_length=80)
    user = models.OneToOneField(User, related_name='profile',
                                on_delete=models.CASCADE)
    friends = models.ManyToManyField('self')
    guests_profiles = models.ManyToManyField('self', through='Invitation',
                                             related_name='inviters_profiles',
                                             symmetrical=False)

    blocked = models.ManyToManyField('self', related_name='blockers',
                                     symmetrical=False)

    reason_disable = models.CharField(max_length=200, default="No have")

    def is_superuser(self):
        return self.user.is_superuser

    def change_to_superuser(self, profile):
        if self.user.is_superuser:
            profile.user.is_superuser = True
            profile.user.save()
            return
        raise PermissionError

    def give_up_superuser(self):
        self.user.is_superuser = False
        self.user.save()

    def invite(self, invited_profile):
        if (invited_profile not in self.guests_profiles.all()) and\
                (invited_profile not in self.inviters_profiles.all()):
            invitation = Invitation(inviter=self, guest=invited_profile)
            invitation.save()
            return
        raise IntegrityError("This profile is already a guest or invited you.")

    def delete_post(self, post):
        if post.profile == self or self.is_superuser():
            post.delete()
            return
        raise PermissionError("You don't have permission to this operation.")


class Invitation(models.Model):

    inviter = models.ForeignKey(Profile, related_name='sent_invitations', on_delete=models.CASCADE)
    guest = models.ForeignKey(Profile, related_name='received_invitations', on_delete=models.CASCADE)
    send_date = models.DateTimeField(auto_now_add=True)

    def accept(self, logged):
        if logged == self.guest:
            logged.friends.add(self.inviter)
            self.delete()
            return
        raise PermissionError("You don't have permission to this operation.")

    def decline(self, logged):
        if logged == self.guest:
            self.delete()
            return
        raise PermissionError("You don't have permission to this operation.")

    def cancel(self, logged):
        if logged == self.inviter:
            self.delete()
            return
        raise PermissionError("You don't have permission to cancel this")
