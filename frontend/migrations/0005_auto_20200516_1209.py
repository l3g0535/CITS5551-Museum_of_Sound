# Generated by Django 3.0.2 on 2020-05-16 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0004_auto_20200516_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='production',
            name='audio_file',
            field=models.FileField(upload_to=''),
        ),
    ]
