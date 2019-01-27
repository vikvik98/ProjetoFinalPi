from django import forms
from pyuploadcare.dj.forms import ImageField


class AddPostForm(forms.Form):
    text = forms.CharField(required=False)
    photo = ImageField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        photo = cleaned_data.get('photo')
        if not text and not photo:
            raise forms.ValidationError("Please, add a photo or text.")
        return cleaned_data
