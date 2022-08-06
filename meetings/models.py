from email.policy import default
from django.db import models

# Create your models here.
class Meetings(models.Model):
    #meetHead = models.CharField(max_length=100)
    meetName = models.CharField(max_length=100)
    meetTime = models.DateField()
    meetPlace = models.CharField(max_length=100)
    meetStatus = models.IntegerField(default=0) #0:모집중, 1:투표중, 2:픽스
    meetStart = models.DateField()
    meetEnd = models.DateField()
    meetVote = models.IntegerField(default=0)
    meetMembers = models.IntegerField(default=0) 

    def __str__(self):
        return self.meetName