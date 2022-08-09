from tokenize import group
from django.db import models
from meetings.models import Meetings
# Create your models here.

#id 기본으로 있음
class MeetingMember(models.Model):
    meetId = models.ForeignKey(Meetings, on_delete=models.CASCADE)
    #groupId = models.ForeignKey('Group', on_delete=models.CASCADE)
    #userId = models.ForeignKey('User', on_delete=models.CASCADE)
    availableDate = models.DateField()
    availableStarttime = models.DateField()
    availableEndtime = models.DateField()




#todo 다른 모델이랑 연결필요