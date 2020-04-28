# Generated by Django 2.1 on 2020-04-28 14:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Production',
            fields=[
                ('prod_id', models.AutoField(primary_key=True, serialize=False)),
                ('prod_title', models.TextField()),
                ('prod_description', models.TextField(default='')),
                ('upload_time', models.DateTimeField()),
                ('audio_file', models.FileField(upload_to='')),
                ('is_approved', models.CharField(choices=[('Y', 'YES'), ('N', 'NO')], default='N', max_length=256)),
                ('uploader_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tag_id', models.AutoField(primary_key=True, serialize=False)),
                ('tag_content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserSound',
            fields=[
                ('sound_id', models.AutoField(primary_key=True, serialize=False)),
                ('upload_time', models.DateTimeField()),
                ('description', models.TextField(blank=True, null=True)),
                ('audio_file', models.FileField(upload_to='')),
                ('is_approved', models.CharField(choices=[('Y', 'YES'), ('N', 'NO')], default='N', max_length=3)),
                ('is_tagged', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='tag',
            name='sound_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.UserSound'),
        ),
    ]
