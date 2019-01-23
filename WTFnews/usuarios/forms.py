from django import forms
from django.contrib.auth.models import User

class SingUpForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)

    def is_valid(self):
        valid = True
        if not super(SingUpForm, self).is_valid():
            self.add_error('Please, Check the reported data.')
            valid = False

        user_exists = User.objects.filter(username=self.cleaned_data['name']).exists()
        if user_exists:
            self.add_error('This email is already being used.')
            valid = False

        return valid

    def add_error(self, message):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS,
                                         forms.utils.ErrorList())

        errors.append(message)



class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(required=True)
    new_password = forms.CharField(required=True)
    co_new_password = forms.CharField(required=True)
    valid = True

    def is_valid(self):

        if not super(ChangePasswordForm, self).is_valid():
            self.add_error('Please, Check the reported data.')
            self.valid = False

        # if not self.check_old_password():
        #     self.add_error("The old password is not correct.")
        #     valid = False
        #
        # if not self.check_new_old_password():
        #     self.add_error("The new password is not the same as the password confirmation.")
        #     valid = False

        return self.valid

    def add_error(self, message):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS,
                                         forms.utils.ErrorList())

        errors.append(message)


    # def check_old_password(self,logged_profile):
    #
    #     if self.cleaned_data['old_password'] == logged_profile.email:
    #         return True
    #     else:
    #         return False
    #
    #
    # def check_new_old_password(self):
    #     if self.cleaned_data['new_password'] == self.cleaned_data['co_new_password']:
    #         return True
    #     else:
    #         return False

