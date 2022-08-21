# Generated by Django 4.1 on 2022-08-20 18:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('meetings', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='meetTravelInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('day', models.IntegerField()),
                ('meetId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetings.meetings', verbose_name='약속 PK')),
                ('meetUsers', models.ManyToManyField(related_name='travelUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='meetTravel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateField(verbose_name='시작 날짜')),
                ('startTime', models.CharField(choices=[('0', '00 ~ 01'), ('1', '01 ~ 02'), ('2', '02 ~ 03'), ('3', '03 ~ 04'), ('4', '04 ~ 05'), ('5', '05 ~ 06'), ('6', '06 ~ 07'), ('7', '07 ~ 08'), ('8', '08 ~ 09'), ('9', '09 ~ 10'), ('10', '10 ~ 11'), ('11', '11 ~ 12'), ('12', '12 ~ 13'), ('13', '13 ~ 14'), ('14', '14 ~ 15'), ('15', '15 ~ 16'), ('16', '16 ~ 17'), ('17', '17 ~ 18'), ('18', '18 ~ 19'), ('19', '19 ~ 20'), ('20', '20 ~ 21'), ('21', '21 ~ 22'), ('22', '22 ~ 23'), ('23', '23 ~ 00')], max_length=20)),
                ('endDate', models.DateField(verbose_name='종료 날짜')),
                ('endTime', models.CharField(choices=[('0', '00 ~ 01'), ('1', '01 ~ 02'), ('2', '02 ~ 03'), ('3', '03 ~ 04'), ('4', '04 ~ 05'), ('5', '05 ~ 06'), ('6', '06 ~ 07'), ('7', '07 ~ 08'), ('8', '08 ~ 09'), ('9', '09 ~ 10'), ('10', '10 ~ 11'), ('11', '11 ~ 12'), ('12', '12 ~ 13'), ('13', '13 ~ 14'), ('14', '14 ~ 15'), ('15', '15 ~ 16'), ('16', '16 ~ 17'), ('17', '17 ~ 18'), ('18', '18 ~ 19'), ('19', '19 ~ 20'), ('20', '20 ~ 21'), ('21', '21 ~ 22'), ('22', '22 ~ 23'), ('23', '23 ~ 00')], max_length=20)),
                ('meetId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetings.meetings', verbose_name='약속 PK')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='사용자 PK')),
            ],
        ),
        migrations.CreateModel(
            name='meetDayInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('day', models.IntegerField()),
                ('hour', models.IntegerField()),
                ('meetId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetings.meetings', verbose_name='약속 PK')),
                ('meetUsers', models.ManyToManyField(related_name='meetUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='meetDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('validDate', models.DateField()),
                ('startTime', models.CharField(choices=[('0', '00 ~ 01'), ('1', '01 ~ 02'), ('2', '02 ~ 03'), ('3', '03 ~ 04'), ('4', '04 ~ 05'), ('5', '05 ~ 06'), ('6', '06 ~ 07'), ('7', '07 ~ 08'), ('8', '08 ~ 09'), ('9', '09 ~ 10'), ('10', '10 ~ 11'), ('11', '11 ~ 12'), ('12', '12 ~ 13'), ('13', '13 ~ 14'), ('14', '14 ~ 15'), ('15', '15 ~ 16'), ('16', '16 ~ 17'), ('17', '17 ~ 18'), ('18', '18 ~ 19'), ('19', '19 ~ 20'), ('20', '20 ~ 21'), ('21', '21 ~ 22'), ('22', '22 ~ 23'), ('23', '23 ~ 00')], max_length=20)),
                ('endTime', models.CharField(choices=[('0', '00 ~ 01'), ('1', '01 ~ 02'), ('2', '02 ~ 03'), ('3', '03 ~ 04'), ('4', '04 ~ 05'), ('5', '05 ~ 06'), ('6', '06 ~ 07'), ('7', '07 ~ 08'), ('8', '08 ~ 09'), ('9', '09 ~ 10'), ('10', '10 ~ 11'), ('11', '11 ~ 12'), ('12', '12 ~ 13'), ('13', '13 ~ 14'), ('14', '14 ~ 15'), ('15', '15 ~ 16'), ('16', '16 ~ 17'), ('17', '17 ~ 18'), ('18', '18 ~ 19'), ('19', '19 ~ 20'), ('20', '20 ~ 21'), ('21', '21 ~ 22'), ('22', '22 ~ 23'), ('23', '23 ~ 00')], max_length=20)),
                ('meetId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetings.meetings', verbose_name='약속 PK')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='사용자 PK')),
            ],
        ),
    ]
