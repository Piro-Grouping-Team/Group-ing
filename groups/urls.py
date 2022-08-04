from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('', views.main, name='main'),
    path('create/', views.create, name='create'),
    path('join/', views.join, name='join'),

]