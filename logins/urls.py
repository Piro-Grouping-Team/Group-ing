from django.urls import path
from . import views
app_name = "logins"

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('update/<int:id>', views.userUpdate, name='update'),
    path('findUsername/', views.findUsername, name='findUsername'),
    # path('findPW/', views.findPW, name='findPW'),
    # path('changePW/', views.changePW, name='changePW'),
    path('mypage/', views.mypage, name='mypage'),
    path('find/id', views.FindIdView.as_view(), name='findId'),
    path('find/id/find', views.axiosFindIdView, name='axiosId'),
    path('find/id/show', views.showId, name='showId'),
    path('find/pw', views.FindPwView.as_view(), name='findPw'),
    path('find/pw/find', views.axiosFindPwView, name='axiosPw'),
    path('find/pw/reset', views.authPwResetView, name='findPwReset'),
    path('find/auth', views.authConfirmView, name='findAuth'),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate')
]