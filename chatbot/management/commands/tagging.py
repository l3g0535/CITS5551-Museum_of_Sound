#This file runs on the sound storage server as a chron job
from chatbot.models import FBUserSound
from frontend.models import UserSound, Tag
from django.core.management.base import BaseCommand, CommandError

import nltk
nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import words
english_words = set(words.words())
stop_words = set(stopwords.words('english'))


class Command(BaseCommand):

    def handle(self, *args, **options):
        to_tag = self.get_to_tag()
        for sound in to_tag:
            self.tag(sound)
            sound.is_tagged = True
            sound.save()

    def get_to_tag(self):
        group = UserSound.objects.filter(is_approved="Yes",is_tagged=False)
        return group

    def tag(self, sound):
        tags = self.get_tags(sound.description)
        self.write_tags(tags, sound)

    def get_tags(self, desc):
        tags = nltk.word_tokenize(desc)
        tags = [word.lower() for word in tags if word.isalpha()]
        tags = [word for word in tags if word not in stop_words]
        tags = [word for word in tags if word in english_words]
        return tags


    def write_tags(self, tags, sound):
        for tag in tags:
            new_tag = Tag(sound_id = sound, tag_content=tag)
            new_tag.save()
