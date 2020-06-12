from django import forms
from django.utils import timezone
from frontend.models import UserSound, Production
import os
from django.core.exceptions import ValidationError
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UploadProductionForm(forms.ModelForm):

    class Meta:
        model = Production
        fields = ['prod_title', 'audio_file', 'prod_description', ]
    # prod_title = forms.CharField(
    #     widget=forms.Textarea(attrs={'cols': 30, 'rows': 1}))
    # prod_description = forms.CharField(
    #     widget=forms.Textarea(attrs={'cols': 30, 'rows': 10}))
    # audio_file = forms.FileField()

    def clean(self):
        cleaned_data = super(UploadProductionForm, self).clean()
        file = cleaned_data.get("audio_file")
        if file:
            if not os.path.splitext(file.name)[1] in [".mp3", ".wav", ".aac", ".flac"]:
                raise ValidationError("Not an audio file.")
            if file._size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (
                    filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(file._size)))
        else:
            raise ValidationError("Couldn't read uploaded file")
        return cleaned_data


class UploadSoundForm(forms.ModelForm):
    class Meta:
        model = UserSound
        fields = ['description', 'audio_file',
                  'title', 'location', 'image_file']

    def clean(self):
        cleaned_data = super(UploadSoundForm, self).clean()
        file = cleaned_data.get("audio_file")
        if file:
            if not os.path.splitext(file.name)[1] in [".MP3", ".mp3", ".wav", ".aac", ".flac"]:
                raise ValidationError("Not an audio file.")
            if file._size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (
                    filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(file._size)))
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
