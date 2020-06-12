from django import forms
from django.utils import timezone
from frontend.models import UserSound, Production
import os
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UploadProductionForm(forms.Form):
    prod_title = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 30, 'rows': 1}))
    prod_description = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 30, 'rows': 10}))
    audio_file = forms.FileField()

    def clean(self):
        cleaned_data = super(UploadProductionForm, self).clean()
        file = cleaned_data.get("audio_file")
        if file:
            if not os.path.splitext(file.name)[1] in [".mp3", ".wav", ".aac", ".flac"]:
                raise ValidationError("Not an audio file.")
        else:
            raise ValidationError("Couldn't read uploaded file")
        return cleaned_data


class UploadSoundForm(forms.ModelForm):
    class Meta:
        model = UserSound
        fields = ['description', 'audio_file', 'title', 'location']

    def clean(self):
        cleaned_data = super(UploadSoundForm, self).clean()
        file = cleaned_data.get("audio_file")
        if file:
            if not os.path.splitext(file.name)[1] in [".MP3", ".mp3", ".wav", ".aac", ".flac"]:
                raise ValidationError("Not an audio file.")
        else:
            raise ValidationError("Couldn't read uploaded file")
        return cleaned_data

# class SignUpForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
#     last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
#     email = forms.EmailField(max_length=254, help_text='Required.')
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
