from django.urls import include, path
from . import views
from django.views.generic import TemplateView
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
from django.conf import settings
from users import views as user_views

# from django.conf.urls.static import static


urlpatterns = [

    # path('', views.user_record, name='sound_list'),
    #path('', views.user_record, name='sound_list'),

    #re_path(r'^api/soundlist/', views.get_sound_list),

    path('', views.landing, name='landing'),
    path('explore', views.sound_explore, name='sound_explore'),
    path('production', views.production_list, name='production_list'),
    path('soundlist/', views.sound_list, name='sound_list'),
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
    path('need_help', views.help, name='needhelp'),
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('accounts/login/',
         auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]
