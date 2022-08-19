import datetime
import json
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt

from .utils import dateContinue
from .forms import meetDayForm, meetTravelForm
from django.contrib import messages

from meetCalendar.models import meetDay, meetTravel, meetTravelInfo,meetDayInfo
from logins.models import User
from meetings.models import Meetings

# Create your views here.


def main(request, meetId):

    #test = meetTravelInfo.objects.filter(meetId=meetId)
    #print(test[0].meetUsers.count())
    #test2 = test.filter(year=2022,month=8,day=18)
    #print(test2[0].meetUsers.all())
    #users = test[0].meetUsers.all()
    #print(users[0].username)

    context = {
        'meetId': meetId,
    }

    return render(request, 'meetCalendar/main.html',context)

@csrf_exempt
def getDayInfo(request):
    req = json.loads(request.body)
    meetId = req['meetId1']
    year = req['viewYear']
    month = req['viewMonth']
    month +=1
    meet = Meetings.objects.get(id=meetId)
    meetDayInfos = meetDayInfo.objects.filter(meetId=meet,year=year,month=month)

    dayInfo = []
    for meetDay in meetDayInfos:
        dayInfo.append({
            'year' : meetDay.year,
            'month' : meetDay.month,
            'day' : meetDay.day,
            'hour' : meetDay.hour,
            'userCount' : meetDay.meetUsers.count(),
        })
        
    return JsonResponse({'dayInfo':dayInfo})

@csrf_exempt
def getTravelInfo(request):
    req = json.loads(request.body)
    meetId = req['meetId1']
    year = req['viewYear']
    month = req['viewMonth']
    month +=1
    meet = Meetings.objects.get(id=meetId)
    meetTravelInfos = meetTravelInfo.objects.filter(meetId=meet,year=year,month=month)

    travelInfo = []
    for meetTravel in meetTravelInfos:
        travelInfo.append({
            'year' : meetTravel.year,
            'month' : meetTravel.month,
            'day' : meetTravel.day,
            'userCount' : meetTravel.meetUsers.count(),
        })
        
    return JsonResponse({'travelInfo':travelInfo})


@csrf_exempt
def getDates(request):
    req = json.loads(request.body)
    meetId = req['meetId']
    meet = Meetings.objects.get(id=meetId)
    startDate = meet.meetStart
    endDate = meet.meetEnd
    meetType = meet.meetType

    meetCount = meet.meetMembers.count()

    return JsonResponse({'startDate': startDate, 'endDate': endDate, 'meetType': meetType, 'meetCount': meetCount});

#login 체크 필요?????
def create(request, meetId):
    meeting = Meetings.objects.get(id=meetId)
    if meeting.meetType == 'today':
        form = meetDayForm()
    elif meeting.meetType == 'travel':
        form = meetTravelForm()


    if request.method == 'POST':
        if meeting.meetType == 'today':

            form = meetDayForm(request.POST)

            if form.is_valid():
              meetDay = form.save(commit=False)
              meetDay.meetId = meeting
              meetDay.userId = request.user
              meeting.meetMembers.add(request.user)
              meetDay.save()
              savemeetDayInfo(meetDay)
              return redirect('meetCalendar:main', meeting.id)
            else:
                messages.error(request, '입력이 잘못되었습니다. 다시 입력해주세요.')

        elif meeting.meetType == 'travel':
            form = meetTravelForm(request.POST)

            if form.is_valid():
                meetTravel = form.save(commit=False)
                meetTravel.meetId = meeting
                meetTravel.userId = request.user
                meeting.meetMembers.add(request.user)
                meetTravel.save()
                saveTravelInfo(meetTravel)
                return redirect('meetCalendar:main', meeting.id)
            else:
                messages.error(request, '입력이 잘못되었습니다. 다시 입력해주세요.')
            
                
    context={
            'form' : form,
            'meetId' : meetId,
            'meeting' : meeting,
            'meetTimes' : meetTravelForm.TIME_CHOICE,
        }


    return render(request, template_name='meetCalendar/create.html',context=context)

def saveTravelInfo (meetTravel):
    meetId = meetTravel.meetId
    userId = meetTravel.userId
    startDate = meetTravel.startDate
    endDate = meetTravel.endDate
    #시작 날짜부터 종료 날짜까지 반복
    #해당 날짜에 시작시간부터 종료시간까지 저장
    delta = datetime.timedelta(days=1)
    while startDate <= endDate:

        year = startDate.year
        month = startDate.month
        day = startDate.day

        if meetTravelInfo.objects.filter(meetId=meetId,year=year,month=month,day=day).exists():
            meetTravelInfo.objects.get(meetId=meetId,year=year,month=month,day=day).meetUsers.add(userId)
            
        else:
            meetTravelInfo.objects.create(meetId=meetId,year=year,month=month,day=day)
            meetTravelInfo.objects.get(meetId=meetId,year=year,month=month,day=day).meetUsers.add(userId)
        
        startDate += delta
            

def savemeetDayInfo(meetDay):
    meetId = meetDay.meetId
    userId = meetDay.userId
    validDate = meetDay.validDate
    year = validDate.year
    month = validDate.month
    day = validDate.day
    startTime = int(meetDay.startTime)
    endTime = int(meetDay.endTime)
    print (startTime, type(startTime))

    
    while startTime <= endTime:
        if meetDayInfo.objects.filter(meetId=meetId,year=year,month=month,day=day,hour=startTime).exists():
            meetDayInfo.objects.get(meetId=meetId,year=year,month=month,day=day,hour=startTime).meetUsers.add(userId)
        else:
            meetDayInfo.objects.create(meetId=meetId,year=year,month=month,day=day,hour=startTime)
            meetDayInfo.objects.get(meetId=meetId,year=year,month=month,day=day,hour=startTime).meetUsers.add(userId)
        startTime += 1

def dayCandidate(meetId):
    #1. meetDayInfo에서 meetId에 해당하는 모든 객체를 블러오기
    periodInfo = meetDayInfo.objects.filter(meetId=meetId)

    #2. 불러온 객체를 파이썬 리스트화 하기
    periodInfoList = []
    for period in periodInfo:
        users = period.meetUsers.all()
        tmp = []
        tmpName = []
        for name in users:
            tmpName.append(name.username)
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
    return candidate[:3]




def travelCandidate(meetId):
    #1. meetTravelInfo에서 meetId에 해당하는 모든 객체를 블러오기
    periodInfo = meetTravelInfo.objects.filter(meetId=meetId)

    #2. 불러온 객체를 파이썬 리스트화 하기
    periodInfoList = []
    for period in periodInfo:
        users = period.meetUsers.all()
        tmp = []
        tmpName = []
        for name in users:
            tmpName.append(name.username)
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

def voteDayCandidate(request, meetId):
    candidate = dayCandidate(meetId)
    if request.method == 'POST':
        pass
    else:
        context = {
            'candidate' : candidate
        }

        return render(request, template_name='meetCalendar/voteDayCandidate.html', context=context)

def voteTravelCandidate(request, meetId):
    candidate = travelCandidate(meetId)
    if request.method == 'POST':
        pass
    else:
        context = {
            'candidate' : candidate
        }

        return render(request, template_name='meetCalendar/voteTravelCandidate.html', context=context)

