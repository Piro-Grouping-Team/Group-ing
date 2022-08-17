from django.db import models
from django.contrib.postgres.fields import ArrayField  
from meetings.models import Meetings
from logins.models import User

# Create your models here.

#당일치기 history 모델
class meetDay(models.Model):
    #약속 pk
    meetId = models.ForeignKey(Meetings, on_delete=models.CASCADE, verbose_name='약속 PK')

    #user pk
    userId = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='사용자 PK')

    #시작시간
    startTime = models.DateTimeField(verbose_name='시작시간')

    #종료시간
    endTime = models.DateTimeField(verbose_name='종료시간')
    
    pass


#여행 history 모델
class meetTravel(models.Model):
    #약속 pk
    meetId = models.ForeignKey(Meetings, on_delete=models.CASCADE, verbose_name='약속 PK')
    #user pk
    userId = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='사용자 PK')
    #시작 날짜(시간을 포함한)
    startDate = models.DateTimeField(verbose_name='시작 날짜')
    #종료 날짜
    endDate = models.DateTimeField(verbose_name='종료 날짜')
    pass


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
    #시간대별 카운트
    hours = ArrayField(
        ArrayField(models.IntegerField()),
        size=24,
        )
    #array필드 (인덱스가 시간인)
    pass


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
    meetUsers = models.ManyToManyField(User, related_name='meetUser')

    #array필드 ()
  
    pass
