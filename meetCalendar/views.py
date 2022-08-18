import datetime
import json
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
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
    meetId = req['meetId']
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
    meetId = req['meetId']
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

    return JsonResponse({'startDate': startDate, 'endDate': endDate, 'meetType': meetType});

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
