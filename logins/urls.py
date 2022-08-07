from django.urls import path
from . import views
app_name = "logins"

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('/signup', SignUpView.as_view()),
    path('signup/', views.signup_view, name='signup'),
    # path('/activate/<str:uidb64>/<str:token>', Activate.as_view())
]