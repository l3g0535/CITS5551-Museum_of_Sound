import requests, os, uuid
from django.conf import settings
from chatbot.models import FBUserSound, FBUser
from frontend.models import UserSound
from django.core.management.base import BaseCommand, CommandError
from django.core.files.storage import default_storage

class Command(BaseCommand):

    def handle(self, *args, **options):
        uploaded_sounds = []
        unlocalised = self.get_list_of_unlocalised()
        for sound in unlocalised:
            if self.localise(sound):
                uploaded_sounds.append(sound.sound_id)
        FBUserSound.objects.filter(pk__in=uploaded_sounds).update(is_uploaded='Yes')

    def get_list_of_unlocalised(self):
        group = FBUserSound.objects.filter(is_uploaded="No")
        return group

    def download_to_local(self,url):
        r = requests.get(url)
        filename = settings.SOUND_DIR + uuid.uuid4().hex +".aac" #AAC to make safari work
        with default_storage.open(filename, 'wb+') as destination:
                destination.write(r.content)
        return filename

    def localise(self,sound):
        path = self.download_to_local(sound.remote_location)
        new_sound = UserSound()
        new_sound.upload_time = sound.upload_time
        new_sound.description = sound.description
        new_sound.audio_file.name = path
        new_sound.is_approved = 'No'
        new_sound.save()
        return True
