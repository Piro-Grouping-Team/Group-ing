from django.contrib import admin
from .models import Post, PostImg

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'logTitle', 'openRange', 'userId']


@admin.register(PostImg)
class PostImgAdmin(admin.ModelAdmin):
    list_display = ['logId', 'image']
