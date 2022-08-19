import re
from secrets import choice
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from .models import Post, PostImg
from meetings.models import Meetings
from .forms import PostForm, PostImgForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def main(request):
    # todo 키워드 검색
    #if request.GET.get('search'):
    #    search = request.GET.get('search')
    #    posts = Post.objects.filter(logKeywords__contains=search)

    if request.GET.get('openRange'):
        # todo 공개범위 에따른 로그인 판별 필요
        # ?????????????????????????
        openRange = request.GET.get('openRange')
        if openRange == '0':
            posts = Post.objects.filter(openRange=0, userId = request.user.id)
        elif openRange == '1':
            #???????
            
            posts = Post.objects.filter(openRange=1)
        else:
            posts = Post.objects.filter(openRange=2)
    else:
        posts = Post.objects.filter(openRange=2)

    
    context = {
        'posts': posts,
    }

    return render(request, 'posts/main.html', context)


def detail(request, postId):
    #todo 상세페이지 로그인 판별 필요 
    #(비공개인 경우는 로그인한 유저만 접근 가능)
    # 그룹공개 설정 필요 (로그인한 유저가 그룹에 속한 경우)
    post = Post.objects.get(id=postId)
    context = {
        'post': post,
    }
    return render(request, 'posts/detail.html', context)

@login_required
def create(request):
    imgFormSet = modelformset_factory(PostImg, form=PostImgForm, max_num=3, extra=1)
    if request.method == 'POST':
        postForm = PostForm(request.POST)
        formset = imgFormSet(request.POST, request.FILES, queryset=PostImg.objects.none())

        if postForm.is_valid() and formset.is_valid():
            post = postForm.save(commit=False)
            post.userId = request.user
            meetId = request.POST.get('meetId')
            post.meetId = Meetings.objects.get(id=meetId)
            places = request.POST.getlist('place[]')
            placesJson = { 'places': places }
            post.places = placesJson
            print(placesJson)
            post.save()
            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    photo = PostImg(logId=post, image=image)
                    photo.save()
            
            return redirect('posts:detail', postId=post.id)
        else:
            print(postForm.errors, formset.errors)
    else:
        if request.GET.get('meetId'):
            meetId = request.GET.get('meetId')
            meeting = Meetings.objects.get(id=meetId)
            postForm = PostForm(initial={'logTitle': meeting.meetName, 'userId': request.user})
            formset = imgFormSet(queryset=PostImg.objects.none())
            openRanges = Post.openRangeChoices
            context = {
                #'keywords': Post.keyWords,
                'openRanges': openRanges,
                'postForm': postForm,
                'formset': formset,
                'meeting': meeting,
            }
            return render(request, 'posts/create.html', context)
        else:
            postForm = PostForm()
            formset = imgFormSet(queryset=PostImg.objects.none())
            openRanges = Post.openRangeChoices
            context = {
                #'keywords': Post.keyWords,
                'openRanges': openRanges,
                'postForm': postForm,
                'formset': formset,
            }
            return render(request, 'posts/create.html', context)

    

    

@login_required
def update(request, postId):

    # 로그인 되어있는 유저가 이 게시물의 저자 라면 업데이트 페이지로 이동가능
    # 아니라면 디테일페이지로 강제 이동 (알림 메세지)

    nowpost = Post.objects.get(id=postId)
    if (nowpost.userId == request.user.id):
        if request.method == 'POST':
            nowpost.logTitle = request.POST.get('logTitle')
            nowpost.logDate = request.POST.get('logDate')
            nowpost.logLike = request.POST.get('logLike')
            nowpost.logKeywords = request.POST.get('logKeywords')
            nowpost.logImgs = request.POST.get('logImgs')
            nowpost.logContent = request.POST.get('logContent')
            nowpost.openRange = request.POST.get('openRange')
            nowpost.save()
            return redirect('posts:detail', postId=postId)
        else:
            openRanges = Post.openRangeChoices
            context = {
                'post': nowpost,
                'openRanges': openRanges,
           }
            return render(request, 'posts/update.html', context)
    else:
        return redirect('posts:detail', postId=postId)


@login_required
def delete(request, postId):
    # 로그인 되어있으면 삭제 가능
    # 아니라면 디테일페이지로 강제 이동 (알림 메세지)
    if request.method == 'POST':
        nowpost = Post.objects.get(id=postId)
        if nowpost.userId == request.user.id:
            nowpost.delete()
            return redirect('posts:main')
        else:
            return redirect('posts:detail', postId=postId)