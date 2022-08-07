from multiprocessing import context
from tokenize import group
from tracemalloc import start
from django.shortcuts import render, redirect
from .models import Meetings, Group

from django.contrib.auth.decorators import login_required
# Create your views here.

#목록 페이지 
#필터링 공개범위 :개인 그룹 전체
# 검색 a. 키워드 b. 제목
#목록 페이지 썸네일과 제목
@login_required
def main(request):

    
    meetings = Meetings.objects.all()

    context = {
        'meetings': meetings,
    }
    return render(request, 'meetings/main.html')

#todo 생성페이지
@login_required
def create(request,id):
    if request.method =='POST':
        meetGroupId = Group.objects.get(id=id)
        meetName = request.POST['meetName']
        meetTime = request.POST['meetTime']
        meetPlace = request.POST['meetPlace']
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']

        meetings = Meetings(meetName=meetName,meetGroupId=meetGroupId,  meetTime=meetTime, meetPlace=meetPlace, meetStart=startDate, meetEnd=endDate)
        meetings.save()

        return redirect('meetings:detail',id,meetings.id)

    group = Group.objects.get(id=id)
    context = {
        'group': group,
        }

    return render(request, 'meetings/create.html',context)

@login_required
def update(request, id, meetId):
    group = Group.objects.get(id=id)
    if request.method =='POST':
        meetings = Meetings.objects.get(id=meetId)

        meetings.meetName = request.POST['meetName']
        meetings.meetTime = request.POST['meetTime']
        meetings.meetPlace = request.POST['meetPlace']
        meetings.startDate = request.POST['startDate']
        meetings.endDate = request.POST['endDate']
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
    groupId =id
    meeting = Meetings.objects.get(id=meetId)

    context = {
        'meeting': meeting,
    }

    return render(request, 'meetings/detail.html',context)

