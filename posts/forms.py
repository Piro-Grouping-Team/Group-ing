from dataclasses import field
from django import forms
from requests import request

from .models import Post, PostImg

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['logTitle','logContent','openRange']

    logTitle = forms.CharField(error_messages = {'required': '제목을 입력해 주세요'},max_length=100)
    logContent = forms.CharField(error_messages = {'required': '내용을 입력해 주세요'},max_length=100)
    openRange = forms.ChoiceField(choices=Post.openRangeChoices, widget=forms.RadioSelect)


class PostImgForm(forms.ModelForm):
    class Meta:
        model = PostImg
        fields = ['image']

    image = forms.ImageField(required=False)
