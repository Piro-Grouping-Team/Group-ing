from tkinter import CASCADE
from django.db import models

from meetings.models import Meetings
from logins.models import User

# Create your models here.

#당일치기 history 모델
class meetDay(models.Model):
    #약속 pk
    meetId = models.ForeignKey(Meetings, on_delete=CASCADE, verbose_name='약속 PK', related_name='meetId')

    #user pk
    userId = models.ForeignKey(User, on_delete=CASCADE, verbose_name='사용자 PK', related_name='userId')

    #시작시간
    startTime = models.CharField

    #종료시간
    
    pass


#여행 history 모델
class meetTravel(models.Model):
    #약속 pk
    #user pk
    #시작 날짜(시간을 포함한)
    #종료 날짜

    pass


#당일치기 통계 모델
class meetDayInfo(models.Model):
    #약속 pk
    #년도
    #달
    #날짜
    #array필드 (인덱스가 시간인)

    pass


#여행 통계 모델
class meetTravelInfo(models.Model):
    #약속 pk
    #년도
    #달
    #array필드 ()

    pass