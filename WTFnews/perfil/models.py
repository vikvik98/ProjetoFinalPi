from django.db import models
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



    def invite(self, invited_profile, date):
        if (invited_profile not in self.guests_profiles.all()) and\
                (invited_profile not in self.inviters_profiles.all()):
            invitation = Invitation(inviter=self, guest=invited_profile, send_date=date)
            invitation.save()
            return True
        return False

    def accept_invitation(self, invitation):
        if invitation.guest == self:
            invitation.accept()
            return True
        return False

    def decline_invitation(self, invitation):
        if invitation.guest == self:
            invitation.decline()
            return True
        return False

    def cancel_invitation(self, invitation):
        if invitation.inviter == self:
            invitation.decline()
            return True
        return False


class Invitation(models.Model):

    inviter = models.ForeignKey(Profile, related_name='sent_invitations', on_delete=models.CASCADE)
    guest = models.ForeignKey(Profile, related_name='received_invitations', on_delete=models.CASCADE)
    send_date = models.DateTimeField(default=timezone.now())

    def accept(self):
        self.guest.friends.add(self.inviter)
        self.delete()

    def decline(self):
        self.delete()
