from . import views
from django.urls import path

appName = 'posts'

urlpatterns = [
    path('', views.main, name='main'),
    path('create/', views.create, name='create'),
    path('detail/', views.detail, name='detail'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
]