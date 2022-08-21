from . import views
from django.urls import path

app_name = 'posts'

urlpatterns = [
    path('', views.main, name='main'),
    path('create/', views.create, name='create'),
    path('detail/<int:postId>', views.detail, name='detail'),
    path('update/<int:postId>', views.update, name='update'),
    path('delete/<int:postId>', views.delete, name='delete'),
]