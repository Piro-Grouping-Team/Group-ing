from django.urls import path, include
from . import views
app_name='meetCalendar'

urlpatterns = [
    path('<int:meetId>/',views.main,name='main'),  
    path('<int:meetId>/create/', views.create, name='create'),
    path('getDates/',views.getDates,name='getDates'),
    path('getDayInfo/',views.getDayInfo,name='getDayInfo'),
    path('getTravelInfo/',views.getTravelInfo,name='getTravelInfo'),
    path('<int:meetId>/voteDayCandidate/',views.voteDayCandidate,name='voteDayCandidate'),
    path('<int:meetId>/voteTravelCandidate/',views.voteTravelCandidate,name='voteTravelCandidate'),
    path('<int:meetId>/fixDayCandidate/',views.fixDayCandidate,name='fixDayCandidate'),
    path('<int:meetId>/fixTravelCandidate/',views.fixTravelCandidate,name='fixTravelCandidate'),
]  