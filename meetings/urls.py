from django.urls import path
from . import views

app_name = 'meetings'

urlpatterns = [
    path('', views.main, name='main'),
    path('create/', views.create, name='create'),
    path('update/', views.update, name='update'),
    path('detail/<int:meetId>/', views.detail, name='detail'),
]
