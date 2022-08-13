from django.urls import path, include
from . import views
app_name='meetCalendar'

urlpatterns = [
    path('<int:meetId>/',views.main,name='main'),  
    path('<int:meetId>/create/', views.create, name='create'),
    path('getDates/',views.getDates,name='getDates'),
]  