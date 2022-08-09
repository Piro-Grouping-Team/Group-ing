from multiprocessing import context
from tokenize import group
from tracemalloc import start
from django.shortcuts import render, redirect
from .models import Meetings, Group, User

from django.contrib.auth.decorators import login_required
# Create your views here.

#목록 페이지 
#필터링 공개범위 :개인 그룹 전체
# 검색 a. 키워드 b. 제목
#목록 페이지 썸네일과 제목

#todo 생성페이지
@login_required
def create(request,id):
    group = Group.objects.get(id=id)
    if group.members.filter(id = request.user.id).exists() == False:
        print('그룹에 속해있지 않아요 ')
        # todo 다이렉션 설정 필요
        return redirect('groups:detail', id)


    if request.method =='POST':
        meetHead = User.objects.get(id=request.user.id)
        meetGroupId = Group.objects.get(id=id)
        meetName = request.POST['meetName']
        meetTime = request.POST['meetTime']
        meetPlace = request.POST['meetPlace']
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']

        meetings = Meetings(meetHead=meetHead,meetName=meetName,meetGroupId=meetGroupId,  meetTime=meetTime, meetPlace=meetPlace, meetStart=startDate, meetEnd=endDate)
        meetings.save()

        return redirect('meetings:detail',id,meetings.id)

    context = {
        'group': group,
        }

    return render(request, 'meetings/create.html',context)

@login_required
def update(request, id, meetId):
    # todo 약속을 만든사람인지 판별
    group = Group.objects.get(id=id)
    meetings = Meetings.objects.get(id=meetId)


    if meetings.meetHead.id != request.user.id:
        print('작성자가 아닙니다')
        return redirect('groups:detail', id)
    
    if request.method =='POST':

        meetings.meetName = request.POST['meetName']
        meetings.meetTime = request.POST['meetTime']
        meetings.meetPlace = request.POST['meetPlace']
        meetings.save()

        return redirect('meetings:detail',id,meetings.id)
    
    meetings = Meetings.objects.get(id=meetId)
    context = {
        'meeting': meetings,
        'group': group,

    }
    return render(request, 'meetings/update.html',context)

#todo 디테일 페이지 - 모집중/ 투표중/ 픽스  
@login_required
def detail(request, id,meetId):
    meeting = Meetings.objects.get(id=meetId)
    group = Group.objects.get(id=id)

    if group.members.filter(id = request.user.id).exists() == False:
        print('그룹에 속해있지 않아요')
        # todo 다이렉션 설정 필요
        return redirect('groups:detail', id)

    context = {
        'meeting': meeting,
        'group': group,
    }

    return render(request, 'meetings/detail.html',context)

@login_required
def delete(request, id, meetId):
    meeting = Meetings.objects.get(id=meetId)
    group = Group.objects.get(id=id)

    if meeting.meetHead.id != request.user.id:
        print('작성자가 아닙니다')
        return redirect('groups:detail', id)

    meeting.delete()
    return redirect('groups:detail', id)