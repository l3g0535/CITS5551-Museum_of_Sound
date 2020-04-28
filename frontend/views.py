from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.http import Http404
from django.utils import timezone
from datetime import datetime, date, time, timedelta
from .forms import UploadProductionForm, UploadSoundForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.files.storage import default_storage
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse, HttpResponseRedirect
import uuid
import json
import os
from frontend.models import Tag, UserSound, Production
from django.    core import management
from django.conf import settings
import requests
from django.contrib.auth import login, authenticate


def landing(request):
    return render(request, 'frontend/landing.html')


def loggin(request):
    return render(request, 'frontend/login-page.html')


def sound_explore(request):
    return render(request, 'frontend/explore.html')


def get_tags():
    tags = Tag.objects.values("tag_content").annotate(
        num=Count('tag_content')).order_by('-num')[:20]
    return tags


def sound_list(request):
    tags = get_tags()
    sound_list = UserSound.objects.filter(
        is_approved="Y").order_by('-upload_time')
    paginator = Paginator(sound_list, 5)
    page = request.GET.get('page')
    sounds = paginator.get_page(page)
    return render(request, 'frontend/sound_list.html', {'sounds': sounds, 'tags': tags})


def production_list(request):
    tags = get_tags()
    prod_list = Production.objects.filter(
        is_approved="Yes").order_by('-upload_time')
    print(type(prod_list))
    paginator = Paginator(prod_list, 5)
    page = request.GET.get('page')
    prods = paginator.get_page(page)
    return render(request, 'frontend/prod_list.html', {'prods': prods, 'tags': tags})


def sound_detail(request, pk):
    tags = get_tags()
    sounds = get_object_or_404(UserSound, pk=pk)
    return render(request, 'frontend/sound_detail.html', {'sound': sounds, 'tags': tags})

# Todo serves tag when tag doesn't exist


def tag_filter(request, tag):
    if not Tag.objects.filter(tag_content=tag).exists():
        raise Http404("Tag doesn't exist.")
    tags = get_tags()
    sounds = UserSound.objects.filter(tag__tag_content=tag, is_approved="Yes")
    return render(request, 'frontend/sound_list.html', {'sounds': sounds, 'head': tag, 'tags': tags})


def date_filter(request, arg):
    tags = get_tags()
    date_start = datetime.strptime(arg, '%Y-%m-%d')
    date_end = datetime.strptime(arg, '%Y-%m-%d') + timedelta(days=1)
    tags = Tag.objects.distinct()
    distinct_dates = UserSound.objects.values('upload_time')
    sounds = UserSound.objects.filter(
        is_approved="Yes", upload_time__gte=date_start, upload_time__lt=date_end)
    if not sounds.exists():
        raise Http404("No sounds on this date.")
    return render(request, 'frontend/filter.html', {'sounds': sounds, 'head': arg, 'tags': tags})


def search_tag(request):
    tags = get_tags()
    query = request.GET.get('q')
    if Tag.objects.filter(tag_content=query):
        return tag_filter(request, query)
    else:
        return render(request, 'frontend/empty_search.html', {'tags': tags})


@login_required
def upload_production(request):
    if request.method == "POST":
        form = UploadProductionForm(request.POST, request.FILES)
        if form.is_valid():
            upload = Production()
            upload.upload_time = timezone.now()
            upload.uploader_id = request.user
            upload.audio_file.name = handle_upload(
                settings.PROD_DIR, form.cleaned_data['audio_file'])
            upload.prod_title = form.cleaned_data['prod_title']
            upload.prod_description = form.cleaned_data['prod_description']
            upload.save()
            return render(request, 'frontend/verification.html', {'production': upload, 'title': 'Upload a production', 'username': upload.uploader_id.username})
    else:
        form = UploadProductionForm()
    return render(request, 'frontend/production_upload.html', {'form': form})


def handle_upload(root, file):
    file_ext = os.path.splitext(file.name)[1]
    if not file_ext:
        # TODO test this, it changes every non compatible file type to .wav?
        file_ext = ".wav"
    filename = root + uuid.uuid4().hex + file_ext
    with default_storage.open(filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return filename


def sound_upload(request):
    if request.method == "POST":
        print('in post')
        form = UploadSoundForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            print('valid post')
            upload = UserSound()
            upload.description = form.cleaned_data['description']
            upload.upload_time = timezone.now()
            upload.audio_file.name = handle_upload(
                settings.SOUND_DIR, form.cleaned_data['audio_file'])
            print(upload.sound_id)
            print(upload.is_approved)
            print(upload.audio_file)
            # TODO fix this when DB is up
            upload.save()
            print('upload worked')
            return render(request, 'frontend/verification.html', {'production': upload, 'title': 'Upload a sound'})
    else:
        form = UploadSoundForm()
    return render(request, 'frontend/sound_upload.html', {'form': form})


@ensure_csrf_cookie
def user_record(request):
    response_success = response = {'status': 1, 'message': ("Ok")}
    response_fail = response = {'status': 0, 'message': (
        "Server error, please reload the page.")}
    if request.method == 'POST':
        try:
            desc = request.POST['descrip']
            uploaded_file = request.FILES['sound']
            print(uploaded_file)
            upload = UserSound()
            upload.upload_time = timezone.now()
            upload.description = desc
            upload.audio_file.name = handle_upload(
                settings.SOUND_DIR, uploaded_file)
            upload.save()
            response = response_success
        except Exception as e:
            print(e)
            response_fail = {'status': 0, 'message': "An error occurred. \n"}
            response = response_fail
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        return render(request, 'frontend/user_record.html')


def signup(request):
    return render(request, 'frontend/signup.html')


def help(request):
    return render(request, 'frontend/blog-post.html')


@login_required
def download(request):
    management.call_command('download_to_local')
    return redirect('frontend/usersound/')


@login_required
def tagging(request):
    management.call_command('tagging')
    return redirect('frontend/usersound/')


@login_required
def view_and_edit_profile(request):
    return redirect('frontend/view_edit_profile')
