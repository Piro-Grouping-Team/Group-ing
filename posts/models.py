from django.db import models

# Create your models here.
class Meetings(models.Model):
    #meetHead = models.CharField(max_length=100)
    meetTime = models.DateField()
    meetPlace = models.CharField(max_length=100)
    meetStatus = models.integerField()
    meetName = models.CharField(max_length=100)
    meetStart = models.DateField()
    meetEnd = models.DateField()
    meetVote = models.IntegerField()
    meetMembers = models.IntegerField()