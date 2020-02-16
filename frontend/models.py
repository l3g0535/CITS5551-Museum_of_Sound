
from django.db import models
from django.conf import settings
import os.path
import os

from django.utils.safestring import mark_safe

from django.contrib.staticfiles.storage import staticfiles_storage
from django.dispatch import receiver

class Production(models.Model):
    storage_location ='productions'
    prod_id = models.AutoField(primary_key=True)
    prod_title = models.TextField(null=False)
    prod_description = models.TextField(default="")
    upload_time = models.DateTimeField()
    audio_file = models.FileField()
    uploader_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_approved = models.CharField(max_length=256, choices=[('Yes', 'Yes'), ('No', 'No')], default="No")
    def audio_file_player(self):
        """audio player tag for admin"""
        if self.audio_file:
            player_string = '<audio preload="metadata" controls><source src="%s">Your browser does not support the audio element.</audio>' % (self.audio_file.url)
            return mark_safe(player_string)

class UserSound(models.Model):
    sound_id = models.AutoField(primary_key=True)
    upload_time = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    audio_file = models.FileField()
    is_approved = models.CharField(max_length=256, choices=[('Yes', 'Yes'), ('No', 'No')], default="No")
    is_tagged = models.BooleanField(default=False)
    def audio_file_player(self):
        """audio player tag for admin"""
        if self.audio_file:
            player_string = '<audio preload="metadata" controls><source src="%s">Your browser does not support the audio element.</audio>' % (self.audio_file.url)
            return mark_safe(player_string)
    def tags(self):
        tags = [x.tag_content for x in Tag.objects.filter(sound_id = self.sound_id)]
        return tags

class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    sound_id = models.ForeignKey(UserSound, on_delete=models.CASCADE)
    tag_content = models.TextField(null=False)

@receiver(models.signals.post_delete, sender=UserSound)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.audio_file:
        instance.audio_file.delete(save=False)

@receiver(models.signals.post_delete, sender=Production)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.audio_file:
        instance.audio_file.delete(save=False)
