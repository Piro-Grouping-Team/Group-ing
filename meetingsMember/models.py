from tokenize import group
from django.db import models
from django.db.utils import ForeignKey
# Create your models here.

#id 기본으로 있음
class MeetingMember(models.Model):
    meetId = ForeignKey('Meetings', on_delete=models.CASCADE)
    #groupId = ForeignKey('Group', on_delete=models.CASCADE)
    #userId = ForeignKey('User', on_delete=models.CASCADE)
    availableDate = models.DateField()
    availableStarttime = models.DateField()
    availableEndtime = models.DateField()




#todo 다른 모델이랑 연결필요