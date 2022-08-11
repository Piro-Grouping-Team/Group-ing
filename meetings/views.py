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
        # 각 인자가 안들어올 수 있어서, modelForm 만드시고 validation 체크하시는 게
        # 좋을 것 같습니다.
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
    # Group의 경우 마지막 리턴 값에만 필요한데, 작성자 체크하기 전에
    # 호출하는 건 비효율적으로 보입니다.
    # 만약 작성자가 아닌 경우, 그룹을 계속 호출하는 비효율이 발생합니다.
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

    # 동일한 객체에 대해 2번 호출하고 있습니다.
    meetings = Meetings.objects.get(id=meetId)
    context = {
        'meeting': meetings,
        'group': group,

    }
    return render(request, 'meetings/update.html',context)

#todo 디테일 페이지 - 모집중/ 투표중/ 픽스
@login_required
def detail(request, id,meetId):
    # Group의 경우 마지막 리턴 값에만 필요한데, 작성자 체크하기 전에
    # 호출하는 건 비효율적으로 보입니다.
    # 만약 작성자가 아닌 경우, 그룹을 계속 호출하는 비효율이 발생합니다.
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
    # Group의 경우 마지막 리턴 값에만 필요한데, 작성자 체크하기 전에
    # 호출하는 건 비효율적으로 보입니다.
    # 만약 작성자가 아닌 경우, 그룹을 계속 호출하는 비효율이 발생합니다.
    meeting = Meetings.objects.get(id=meetId)
    group = Group.objects.get(id=id)

    if meeting.meetHead.id != request.user.id:
        print('작성자가 아닙니다')
        return redirect('groups:detail', id)

    meeting.delete()
    return redirect('groups:detail', id)
