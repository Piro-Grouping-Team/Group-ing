from django.db import models
from django.contrib.postgres.fields import ArrayField  
from meetings.models import Meetings
from logins.models import User

# Create your models here.

#당일치기 history 모델
class meetDay(models.Model):
    TIME_CHOICE = (
        ('0', '00 ~ 01'),
        ('1', '01 ~ 02'),
        ('2', '02 ~ 03'),
        ('3', '03 ~ 04'),
        ('4', '04 ~ 05'),
        ('5', '05 ~ 06'),
        ('6', '06 ~ 07'),
        ('7', '07 ~ 08'),
        ('8', '08 ~ 09'),
        ('9', '09 ~ 10'),
        ('10', '10 ~ 11'),
        ('11', '11 ~ 12'),
        ('12', '12 ~ 13'),
        ('13', '13 ~ 14'),
        ('14', '14 ~ 15'),
        ('15', '15 ~ 16'),
        ('16', '16 ~ 17'),
        ('17', '17 ~ 18'),
        ('18', '18 ~ 19'),
        ('19', '19 ~ 20'),
        ('20', '20 ~ 21'),
        ('21', '21 ~ 22'),
        ('22', '22 ~ 23'),
        ('23', '23 ~ 00'),
    )


    #약속 pk
    meetId = models.ForeignKey(Meetings, on_delete=models.CASCADE, verbose_name='약속 PK')

    #user pk
    userId = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='사용자 PK')

    #가능 날짜
    validDate = models.DateField()

    #시작 시간
    startTime = models.CharField(max_length=20,choices=TIME_CHOICE)

    #종료시간
    endTime = models.CharField(max_length=20, choices=TIME_CHOICE)
    


#여행 history 모델
class meetTravel(models.Model):
    TIME_CHOICE = (
        ('0', '00 ~ 01'),
        ('1', '01 ~ 02'),
        ('2', '02 ~ 03'),
        ('3', '03 ~ 04'),
        ('4', '04 ~ 05'),
        ('5', '05 ~ 06'),
        ('6', '06 ~ 07'),
        ('7', '07 ~ 08'),
        ('8', '08 ~ 09'),
        ('9', '09 ~ 10'),
        ('10', '10 ~ 11'),
        ('11', '11 ~ 12'),
        ('12', '12 ~ 13'),
        ('13', '13 ~ 14'),
        ('14', '14 ~ 15'),
        ('15', '15 ~ 16'),
        ('16', '16 ~ 17'),
        ('17', '17 ~ 18'),
        ('18', '18 ~ 19'),
        ('19', '19 ~ 20'),
        ('20', '20 ~ 21'),
        ('21', '21 ~ 22'),
        ('22', '22 ~ 23'),
        ('23', '23 ~ 00'),
    )

    
    #약속 pk
    meetId = models.ForeignKey(Meetings, on_delete=models.CASCADE, verbose_name='약속 PK')
    #user pk
    userId = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='사용자 PK')
    #시작 날짜(시간을 포함한)
    startDate = models.DateField(verbose_name='시작 날짜',)
    startTime = models.CharField(max_length=20,choices=TIME_CHOICE)
    #종료 날짜
    endDate = models.DateField(verbose_name='종료 날짜')
    endTime = models.CharField(max_length=20, choices=TIME_CHOICE)


#당일치기 통계 모델
class meetDayInfo(models.Model):
    #약속 pk
    meetId = models.ForeignKey(Meetings, on_delete=models.CASCADE, verbose_name='약속 PK')
    #년도
    year = models.IntegerField()
    #달
    month = models.IntegerField()
    #날짜
    day = models.IntegerField()
    #시간대
    hour = models.IntegerField()

    meetUsers = models.ManyToManyField(User, related_name='meetUser')
    


#여행 통계 모델
class meetTravelInfo(models.Model):
    #약속 pk
    meetId = models.ForeignKey(Meetings, on_delete=models.CASCADE , verbose_name='약속 PK')
    #년도
    year = models.IntegerField()
    #달
    month = models.IntegerField()
    #날짜
    day = models.IntegerField()
    #사람 카운트
    meetUsers = models.ManyToManyField(User, related_name='travelUser')

    #array필드 ()
