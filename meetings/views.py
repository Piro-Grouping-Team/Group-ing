from multiprocessing import context
from tokenize import group
from tracemalloc import start
from django.shortcuts import render, redirect

from meetCalendar.models import meetDayInfo, meetDayVote, meetTravelInfo
from meetCalendar.utils import dateContinue
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

def dayCandidate(meetId):
    #1. meetDayInfo에서 meetId에 해당하는 모든 객체를 블러오기
    meeting = Meetings.objects.get(id=meetId)
    periodInfo = meetDayInfo.objects.filter(meetId=meetId)

    #2. 불러온 객체를 파이썬 리스트화 하기
    periodInfoList = []
    for period in periodInfo:
        users = period.meetUsers.all()
        tmp = []
        tmpName = []
        for name in users:
            tmpName.append(name)
        tmp.append(period.year)
        tmp.append(period.month)
        tmp.append(period.day)
        tmp.append(period.hour)
        tmp.append(tmpName)
        periodInfoList.append(tmp)
    print("정렬 전: ", periodInfoList)

    #3. periodInfoList를 연도, 월, 일 순으로 정렬하기
    periodInfoList = sorted(periodInfoList)
    print("정렬 후 : ", periodInfoList)

    #4. Sliding Window를 사용해 인원수와 구성이 동일한 시간대를 별도의 리스트에 저장.
    start = 0
    end = 1
    length = len(periodInfoList)
    candidate = []

    while start < length:
        tmp2 = periodInfoList[start]
        for i in range(4):
            tmp2.append(periodInfoList[start][i])
        while end < length:
            if tmp2[4] == periodInfoList[end][4]:
                if (tmp2[5] == periodInfoList[end][0]) and (tmp2[6] == periodInfoList[end][1]) and (tmp2[7] == periodInfoList[end][2]):
                    tmp2[8] = periodInfoList[end][3]
                    end += 1
                    continue          
                else:
                    break;
            else:
                break
        candidate.append(tmp2)
        start = end
        end = start
    print("후보 : ", candidate)

    #5. 4에서 만든 별도의 리스트를 인원수 기준 내림차 순으로 정렬 후 앞에서부터 3개 슬라이싱치기
    candidate = sorted(candidate, key=lambda x:len(x[4]), reverse=True)
    print("최종 후보 : ", candidate[:3])
    voteList = []
    for can in candidate[:3]:
        mdv = meetDayVote.objects.create(meetId=meeting, year=can[0], month=can[1], day=can[2], startTime=can[3], endTime=can[8])
        for person in can[4]:
            mdv.validUser.add(person)
        voteList.append(mdv)
   
    return voteList




def travelCandidate(meetId):
    #1. meetTravelInfo에서 meetId에 해당하는 모든 객체를 블러오기
    meeting = Meetings.objects.get(meetId)
    periodInfo = meetTravelInfo.objects.filter(meetId=meetId)

    #2. 불러온 객체를 파이썬 리스트화 하기
    periodInfoList = []
    for period in periodInfo:
        users = period.meetUsers.all()
        tmp = []
        tmpName = []
        for name in users:
            tmpName.append(name)
        tmp.append(period.year)
        tmp.append(period.month)
        tmp.append(period.day)
        tmp.append(tmpName)
        periodInfoList.append(tmp)
    print("정렬 전: ", periodInfoList)

    #3. periodInfoList를 연도, 월, 일 순으로 정렬하기
    periodInfoList = sorted(periodInfoList)
    print("정렬 후 : ", periodInfoList)

    #4. Sliding Window를 사용해 인원수와 구성이 동일한 시간대를 별도의 리스트에 저장.
    start = 0
    end = 1
    length = len(periodInfoList)
    candidate = []

    while start < length:
        tmp2 = periodInfoList[start]
        for i in range(3):
            tmp2.append(periodInfoList[start][i])
        while end < length:
            if tmp2[3] == periodInfoList[end][3]:
                if dateContinue(tmp2[4:], periodInfoList[end]):
                    for j in range(3):
                        tmp2[j+4] = periodInfoList[end][j]
                    end += 1
                    continue
                else:
                    break;
            else:
                break
        candidate.append(tmp2)
        start = end
        end = start+1
    print("후보 : ", candidate)

    #5. 4에서 만든 별도의 리스트를 인원수 기준 내림차 순으로 정렬 후 앞에서부터 3개 슬라이싱치기
    candidate = sorted(candidate, key=lambda x:len(x[3]), reverse=True)
    print("최종 후보 : ",candidate[:3])
    
    return candidate[:3]


def changeStatus(request,id, meetId):
    meeting = Meetings.objects.get(id=meetId)

    if meeting.meetStatus == 0 :
        meeting.meetStatus = 1
        meeting.save()

        if meeting.meetType == 'today':
            dayCandidate(meetId)
            return redirect('meetCalendar:voteDayCandidate', meetId)
        else:
            return redirect('meetCalendar:voteTravelCandidate', meetId)

    elif meeting.meetStatus == 1 :
        meeting.meetStatus = 2
        meeting.save()

        return redirect('meetings:detail', meeting.meetGroupId.id, meetId)

    