from django.db import models

# Create your models here.
class Post(models.Model):

    openRangeChoices = (
        ('0', '비공개'),
        ('1', '그룹공개'),
        ('2', '전체공개'),
    )

    logId = models.IntegerField(primary_key=True)
   #meetId = ForeignKey(Meet, on_delete=models.CASCADE)
   #userId = ForeignKey(User, on_delete=models.CASCADE)
    logDate = models.DateTimeField()
    logLike = models.IntegerField()
    logImgs = models.ArrayField(models.ImageField(blank = True,upload_to='images'),null = True)
    logTitle = models.CharField(max_length=100)
    logContent = models.TextField()
    openRange = models.IntegerField(choices=openRangeChoices)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    #다녀간 장소 추가하기

    def __str__(self):
        return str(self.logId)

    class Meta:
        db_table = 'post'
