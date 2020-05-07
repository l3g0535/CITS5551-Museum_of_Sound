
from django.db import models
from django.conf import settings
import os.path
import os
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib.staticfiles.storage import staticfiles_storage
from django.dispatch import receiver


class Production(models.Model):
    storage_location = 'productions'
    prod_id = models.AutoField(primary_key=True)
    prod_title = models.TextField(null=False)
    prod_description = models.TextField(default="")
    upload_time = models.DateTimeField()
    audio_file = models.FileField()
    uploader_id = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, default="", blank=True)
    is_approved = models.CharField(max_length=256, choices=[
                                   ('Y', 'YES'), ('N', 'NO')], default='N')

    def audio_file_player(self):
        """audio player tag for admin"""
        if self.audio_file:
            player_string = '<audio preload="metadata" controls><source src="%s">Your browser does not support the audio element.</audio>' % (
                self.audio_file.url)
            return mark_safe(player_string)


class UserSound(models.Model):
    sound_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT,
                             default="", blank=True, null=True)
    image_file = models.FileField(null=True)
    title = models.CharField(max_length=50, default='')
    upload_time = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    audio_file = models.FileField()
    approve_choices = [('Y', 'YES'), ('N', 'NO')]
    is_approved = models.CharField(
        max_length=3, choices=approve_choices, default='N')
    is_tagged = models.BooleanField(default=False)

    def audio_file_player(self):
        """audio player tag for admin"""
        if self.audio_file:
            player_string = '<audio preload="metadata" controls><source src="%s">Your browser does not support the audio element.</audio>' % (
                self.audio_file.url)
            return mark_safe(player_string)

    def tags(self):
        tags = [x.tag_content for x in Tag.objects.filter(
            sound_id=self.sound_id)]
        return tags

# de-normalised tag table allows for simpler and more efficient queries at the cost of minimal storage space


# class Tag(models.Model):
#     tag_id = models.AutoField(primary_key=True)
#     sound_id = models.ForeignKey(UserSound, on_delete=models.CASCADE)
#     tag_content = models.TextField(null=False)


# @receiver(models.signals.post_delete, sender=UserSound)
# def auto_delete_file_on_delete(sender, instance, **kwargs):
#     if instance.audio_file:
#         instance.audio_file.delete(save=False)


# @receiver(models.signals.post_delete, sender=Production)
# def auto_delete_file_on_delete(sender, instance, **kwargs):
#     if instance.audio_file:
#         instance.audio_file.delete(save=False)
