from rest_framework import serializers
from frontend.models import UserSound, Production


class UserSoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSound
        fields = ("sound_id",
                  "user_id",
                  "image_file",
                  "title",
                  "upload_time",
                  "description" ,
                  "audio_file",
                  "approve_choices",
                  "is_approved",
                  "is_tagged"
                 )