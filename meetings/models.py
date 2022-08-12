from email.policy import default
from django.db import models
from groups.models import Group,User

# Create your models here.
class Meetings(models.Model):
    meetHead = models.ForeignKey(User, on_delete=models.CASCADE)
    meetGroupId = models.ForeignKey(Group, on_delete=models.CASCADE)
    meetName = models.CharField(max_length=100)
    meetTime = models.DateField(null=True)
    meetPlace = models.CharField(max_length=100)
    meetStatus = models.IntegerField(default=0) #0:모집중, 1:투표중, 2:픽스
    meetStart = models.DateField()
    meetEnd = models.DateField()
    meetVote = models.IntegerField(default=0)
    meetMembers = models.IntegerField(default=0)
    meetPurpose = models.CharField(null=True, max_length=100)

    def __str__(self):
        return self.meetName