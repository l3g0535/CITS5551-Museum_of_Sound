
from .models import FBUserSound, FBUser
from datetime import datetime
from django.utils import timezone
from . import messages

def upload_to_db(sender_id, sound_url, description):
    new_sound = FBUserSound()
    new_sound.upload_time = timezone.now()
    new_sound.description = description
    new_sound.remote_location = sound_url
    new_sound.is_approved = 'No'
    new_sound.save()
    messages.send_confirmation(sender_id, description, sound_url)

def update_userstate(sender_id, state):
    FBUser.objects.filter(user_id=sender_id).update(time_of_last=timezone.now(), state=state)
