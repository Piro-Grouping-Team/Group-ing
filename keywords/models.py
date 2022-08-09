from django.db import models

# Create your models here.
class Keyword(models.Model):
    keyword = models.CharField(max_length=40, blank=True, verbose_name='성향 키워드', unique=True)
