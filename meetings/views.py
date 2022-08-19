from multiprocessing import context
from tokenize import group
from tracemalloc import start
from django.shortcuts import render, redirect
from .models import Meetings, Group, User
from .forms import MeetingForm, MeetingUpdateForm

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
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.meetHead = request.user
            meeting.meetGroupId = group
            meeting.save()
            meeting.meetMembers.add(request.user)

            return redirect('meetings:detail',id,meeting.id)
        else:
            print(form.errors)
    else:
        form = MeetingForm()

    meetType = Meetings.meetType
    context = {
        'group': group,
        'form': form,
        'meetType': meetType,
        }

    return render(request, 'meetings/create.html',context)

@login_required
def update(request, id, meetId):
    # todo 약속을 만든사람인지 판별
    meetings = Meetings.objects.get(id=meetId)


    if meetings.meetHead.id != request.user.id:
        print('작성자가 아닙니다')
        return redirect('groups:detail', id)
    
    if request.method =='POST':
        form = MeetingUpdateForm(request.POST, instance=meetings)
        if form.is_valid():
            meetings.save()
            return redirect('meetings:detail',id,meetings.id)
        else:
            print(form.errors)

    else:
        form = MeetingUpdateForm(instance=meetings)
    
    group = Group.objects.get(id=id)
    context = {
        'meeting': meetings,
        'group': group,
        'form': form,
    }
    return render(request, 'meetings/update.html',context)

#todo 디테일 페이지 - 모집중/ 투표중/ 픽스  
@login_required
def detail(request, id,meetId):
    group = Group.objects.get(id=id)

    if group.members.filter(id = request.user.id).exists() == False:
        print('그룹에 속해있지 않아요')
        # todo 다이렉션 설정 필요
        return redirect('groups:detail', id)

    meeting = Meetings.objects.get(id=meetId)
    meetUsers = meeting.meetMembers.all()
    myMeetUsers = {}
    for meetUser in meetUsers:
        myMeetUsers[meetUser.nickname] = meetUser.profileImg
    
    context = {
        'meeting': meeting,
        'group': group,
        'meetUsersName': myMeetUsers,
    }

    return render(request, 'meetings/detail.html',context)

@login_required
def delete(request, id, meetId):
    meeting = Meetings.objects.get(id=meetId)

    if meeting.meetHead.id != request.user.id:
        print('작성자가 아닙니다')
        return redirect('groups:detail', id)

    meeting.delete()
    return redirect('groups:detail', id)