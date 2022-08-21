from django.urls import path
from . import views

app_name = 'meetings'

urlpatterns = [
    path('create/', views.create, name='create'),
    path('update/<int:meetId>', views.update, name='update'),
    path('detail/<int:meetId>/', views.detail, name='detail'),
    path('delete/<int:meetId>/', views.delete, name='delete'),
    path('changeStatus/<int:meetId>/', views.changeStatus, name='changeStatus'),
]