from django import forms
from django.contrib.auth.models import User

class SingUpForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)

    def is_valid(self):
        valid = True
        if not super(SingUpForm, self).is_valid():
            self.add_error('Por favor, Verifique os dados informados')
            valid = False

        user_exists = User.objects.filter(username=self.cleaned_data['name']).exists()
        if user_exists:
            self.add_error('Este email já está sendo usado.')
            valid = False

        return valid

    def add_error(self, message):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS,
                                         forms.utils.ErrorList())

        errors.append(message)