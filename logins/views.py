from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from . import forms
from .models import User

# Create your views here.
def main(request):
    return render(request, 'logins/main.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            print("인증성공") 
        else:
            print("인증실패")
    return render(request, 'logins/login.html')

def logout_view(request):
    logout(request)
    return redirect('logins:login')

def signup_view(request):
    if request.method == "POST":
        print(request.POST)
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            print(form)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            print(form)
            login(request, user)
            return redirect('logins:main')
    else:
        form = forms.SignUpForm()
    return render(request, 'logins/signup.html', {'form' : form})