from django.urls import path
from . import views
app_name = "logins"

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('update/<int:id>', views.userUpdate, name='update'),
    path('findUsername/', views.findUsername, name='findUsername'),
    path('findPW/', views.findPW, name='findPW'),
    # path('changePW/', views.changePW, name='changePW'),
    path('changePW/<str:uidb64>/<str:token>', views.changePW, name='changePW'),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate')
]