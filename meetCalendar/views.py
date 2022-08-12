from multiprocessing import context
import json
from django.http import JsonResponse
from django.shortcuts import render

from meetings.models import Meetings

# Create your views here.


def main(request, meetId):


    context = {
        'meetId': meetId,
    }

    return render(request, 'meetCalendar/main.html',context)


def getDates(request, meetId):
    req = json.loads(request.body)
    meetId = req['meetId']
    meet = Meetings.objects.get(id=meetId)
    startDate = meet.startDate
    endDate = meet.endDate

    return JsonResponse({'startDate': startDate, 'endDate': endDate});