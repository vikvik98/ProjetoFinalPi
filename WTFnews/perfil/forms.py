from django import forms



class DisableProfileForm(forms.Form):
    text = forms.CharField(required=True)

    def is_valid(self):
        valid = True
        if not super(DisableProfileForm, self).is_valid():
            self.add_error('Please, Check the reported data.')
            valid = False


        return valid

    def add_error(self, message):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS,
                                         forms.utils.ErrorList())

        errors.append(message)
