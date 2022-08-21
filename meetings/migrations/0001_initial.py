# Generated by Django 4.1 on 2022-08-21 07:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Meetings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meetName', models.CharField(max_length=100)),
                ('meetStartTime', models.DateTimeField(blank=True, null=True)),
                ('meetEndTime', models.DateTimeField(blank=True, null=True)),
                ('meetPlace', models.CharField(max_length=100)),
                ('meetStatus', models.IntegerField(default=0)),
                ('meetStart', models.DateField()),
                ('meetEnd', models.DateField()),
                ('meetType', models.CharField(choices=[('today', '당일 약속'), ('travel', '여행 약속')], default='today', max_length=20)),
                ('meetPurpose', models.CharField(max_length=100, null=True)),
                ('meetGroupId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.group')),
                ('meetHead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('meetMembers', models.ManyToManyField(related_name='meetMembers', to=settings.AUTH_USER_MODEL)),
                ('meetVote', models.ManyToManyField(blank=True, related_name='voteUsers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
