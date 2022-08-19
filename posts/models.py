from django.db import models
from django.forms import JSONField
from meetings.models import Meetings
from groups.models import User
# Create your models here.
class Post(models.Model):

    openRangeChoices = (
        ('비공개', '비공개'),
        ('그룹공개', '그룹공개'),
        ('전체공개', '전체공개'),
    )

    meetId = models.ForeignKey(Meetings, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    logDate = models.DateTimeField(blank=True, null=True)
    logLike = models.IntegerField(default=0)
    places = JSONField()
    # logImgs = models.ArrayField(models.ImageField(blank = True,upload_to='images'),null = True)
    logTitle = models.CharField(max_length=100)
    logContent = models.TextField()
    openRange = models.CharField(choices=openRangeChoices, max_length=10)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    #다녀간 장소 추가하기

    def __str__(self):
        return str(self.logId)

    class Meta:
        db_table = 'post'


class PostImg(models.Model):
    logId = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='images')

    def __str__(self):
        return str(self.imgId)
 