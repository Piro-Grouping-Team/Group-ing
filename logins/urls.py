from django.urls import path
from . import views
app_name = "logins"

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('update/<int:id>', views.userUpdate, name='update'),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
    path('mypage/', views.mypage, name='mypage'),
]