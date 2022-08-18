# Generated by Django 4.1 on 2022-08-16 09:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('keywords', '0001_initial'),
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='blackList',
            field=models.ManyToManyField(blank=True, related_name='blackList_group', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='group',
            name='keywords',
            field=models.ManyToManyField(blank=True, related_name='keywords_group', to='keywords.keyword'),
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(related_name='members_group', to=settings.AUTH_USER_MODEL),
        ),
    ]
