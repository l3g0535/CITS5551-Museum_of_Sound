from django.contrib import admin

# Register your models here.
from django.db import models

# Create your models here.
from django.contrib import admin
from chatbot.models import FBUser
from .models import Production, UserSound
import os

# Register your models here.
def mark_approved(self, request, queryset):
    queryset.update(is_approved="Yes")

@admin.register(UserSound)
class SoundsAdmin(admin.ModelAdmin):
    list_display = ('upload_time','description', 'audio_file_player','tags','is_approved')
    #readonly_fields = ('upload_time','description','audio_file','tags','is_tagged')
    list_filter = ('is_approved', )
    actions = [mark_approved]

@admin.register(FBUser)
class SoundsAdmin(admin.ModelAdmin):
    pass

@admin.register(Production)
class SoundsAdmin(admin.ModelAdmin):
    list_display = ('prod_title','uploader_id','upload_time','audio_file_player')
    readonly_fields = ('prod_title','uploader_id','upload_time','audio_file_player','prod_description')
    list_filter = ('is_approved', )
    actions = [mark_approved]

class ImportAdmin(admin.ModelAdmin):
    change_list_template = 'admin/frontend/UserSound/change_list.html'

