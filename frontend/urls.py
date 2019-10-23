from django.urls import include, path
from . import views
from django.views.generic import TemplateView


urlpatterns = [

    # path('', views.user_record, name='sound_list'),
    #path('', views.user_record, name='sound_list'),

    path('', views.landing, name='sound_list'),
    path('production', views.production_list, name='production_list'),
    path('signup', views.signup, name='signup'),
    path('sound/<int:pk>/', views.sound_detail, name='sound_detail'),
    path('tag/<tag>', views.tag_filter, name='tag'),
    path('date/<arg>', views.date_filter, name='date'),
    path('production/upload', views.upload_production, name='upload_prod'),
    path('search', views.search_tag, name='search_tag'),
    path('sound/record', views.user_record, name='user_record'),
    path('sound/upload', views.sound_upload, name='sound_upload'),
    path('privacy', TemplateView.as_view(
        template_name="frontend/privacy.html"), name='privacy'),
    path('aboutus', TemplateView.as_view(
        template_name="frontend/aboutus.html"), name='aboutus'),
    path('licensing', TemplateView.as_view(
        template_name="frontend/licensing.html"), name='licensing'),
    path('admin/download', views.download, name='download'),
    path('admin/tagging', views.tagging, name='tagging'),
    path('login', views.loggin, name='login')
]
