from django.db import models

# Create your models here.

#당일치기 history 모델
class meetDay(models.Model):
    #약속 pk
    #user pk
    #시작시간
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