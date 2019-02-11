from django import forms
from django.utils.translation import gettext_lazy as _


class DisableProfileForm(forms.Form):
    text = forms.CharField(required=True)

    def is_valid(self):
        valid = True
        if not super(DisableProfileForm, self).is_valid():
            self.add_error(_('Please, Check the reported data.'))
            valid = False

        return valid

    def add_error(self, message):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS,
                                         forms.utils.ErrorList())

        errors.append(message)



class CommentForm(forms.Form):
    text = forms.CharField(required=True)

    def is_valid(self):
        valid = True
        if not super(CommentForm, self).is_valid():
            self.add_error(_('Please, Check the reported data.'))
            valid = False

        return valid

    def add_error(self, message):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS,
                                         forms.utils.ErrorList())

        errors.append(message)
