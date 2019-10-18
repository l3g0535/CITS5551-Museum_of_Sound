from django.db import models
from django.conf import settings
import os.path
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.staticfiles.storage import staticfiles_storage

class FBUserSound(models.Model):
    sound_id = models.AutoField(primary_key=True)
    upload_time = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    remote_location = models.TextField(default="Missing")
    is_uploaded = models.CharField(max_length=256, choices=[('Yes', 'Yes'), ('No', 'No')], default="No")

class FBUser(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    state = models.IntegerField(blank=True, null=True)
    time_of_last = models.DateTimeField(blank=True, null=True)

class PendingSound(models.Model):
    sound_id = models.AutoField(primary_key=True)
    remote_location = models.TextField(default="Missing")
    user = models.ForeignKey(FBUser, on_delete=models.CASCADE)
