from multiprocessing import context
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt



from meetings.models import Meetings

# Create your views here.


def main(request, meetId):


    context = {
        'meetId': meetId,
    }

    return render(request, 'meetCalendar/main.html',context)

@csrf_exempt
def getDates(request):
    req = json.loads(request.body)
    meetId = req['meetId']
    meet = Meetings.objects.get(id=meetId)
    startDate = meet.meetStart
    endDate = meet.meetEnd

    return JsonResponse({'startDate': startDate, 'endDate': endDate});