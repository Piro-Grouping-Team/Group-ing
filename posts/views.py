from secrets import choice
from django.shortcuts import render, redirect
from .models import Post
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

    post = Post.objects.get(logId=postId)
    context = {
        'post': post,
    }
    return render(request, 'posts/detail.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        logTitle = request.POST.get('logTitle')
        logDate = request.POST.get('logDate')
        logLike = request.POST.get('logLike')
        # logKeywords = request.POST.get('logKeywords')
        # logImgs = request.POST.get('logImgs')
        logContent = request.POST.get('logContent')
        # openRange = request.POST.get('openRange')
        userId = request.user
        
        nowpost = Post.objects.create(userId=userId ,logTitle=logTitle, logDate=logDate, logLike=logLike, logContent=logContent)

        return redirect('posts:detail', postId=nowpost.logId)

    openRanges = Post.openRangeChoices
    context = {
        #'keywords': Post.keyWords,
        'openRanges': openRanges,
    }

    return render(request, 'posts/create.html', context)

@login_required
def update(request, postId):

    # 로그인 되어있는 유저가 이 게시물의 저자 라면 업데이트 페이지로 이동가능
    # 아니라면 디테일페이지로 강제 이동 (알림 메세지)

    nowpost = Post.objects.get(logId=postId)
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
        nowpost = Post.objects.get(logId=postId)
        if nowpost.userId == request.user.id:
            nowpost.delete()
            return redirect('posts:main')
        else:
            return redirect('posts:detail', postId=postId)