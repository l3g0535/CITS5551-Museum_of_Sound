# Generated by Django 3.0.2 on 2020-06-12 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_auto_20200611_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='tag_content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='usersound',
            name='location',
            field=models.TextField(blank=True, null=True),
        ),
    ]
