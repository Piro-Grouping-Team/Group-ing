from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('', views.main, name='main'),
    path('create/', views.create, name='create'),
    path('join/', views.join, name='join'),
    path('group/<int:id>/', views.detail, name='detail'),
    path('group/<int:id>/members', views.members, name='members'),
    path('leave/<int:id>/', views.leave, name='leave'),
    path('modify/<int:id>/', views.modify, name='modify'),
    path('getGroup/', views.getGroup, name='getGroup'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('handOverHead/<int:id>', views.handOverHead, name='handOverHead'),
    path('group/<int:id>/blackList', views.blackList, name='blackList'),
    path('group/<int:id>/addBlackList', views.addBlackList, name='addBlackList'),
    path('group/removeBlackList', views.removeBlackList, name='removeBlackList'),
    path('leaveForce/<int:id>/', views.leaveForce, name='leaveForce'),


]