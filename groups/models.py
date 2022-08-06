from django.db import models
from logins.models import User

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=40, verbose_name='그룹명')
    head = models.CharField(max_length=20, verbose_name='그룹장')
    code = models.CharField(max_length=30, verbose_name='그룹 코드')
    introduction = models.TextField(null=True, blank=True, verbose_name='그룹 소개')
    purpose = models.TextField(null=True, blank=True, verbose_name='그룹 목적')
    # tendency = models.ForeignKey() => 키워드에서 외래키 걸기
    
    members = models.ManyToManyField(User, related_name='members_group')
    blackList = models.ManyToManyField(User, blank=True, related_name='blackList_group')

    #이미지 업로드 경로 추가 
    image = models.ImageField(null=True, blank=True, upload_to='groups/%Y%m%d', verbose_name='그룹 대표사진')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    