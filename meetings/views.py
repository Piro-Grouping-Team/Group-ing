from multiprocessing import context
from django.shortcuts import render
from .models import Meetings

# Create your views here.

#목록 페이지 
#필터링 공개범위 :개인 그룹 전체
# 검색 a. 키워드 b. 제목
#목록 페이지 썸네일과 제목

def main(request):

    
    meetings = Meetings.objects.all()

    context = {
        'meetings': meetings,
    }
    return render(request, 'meetings/main.html')

#todo 생성페이지
def create(request):

    context = {

        }

    return render(request, 'meetings/create.html')

def update(request, meetId):
    return render(request, 'meetings/update.html')

#todo 디테일 페이지 - 모집중/ 투표중/ 픽스  
def detail(request, meetId):

    

    return render(request, 'meetings/detail.html')

