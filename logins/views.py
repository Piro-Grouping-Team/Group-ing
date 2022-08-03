from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from . import forms
# Create your views here.
def main(request):
    return render(request, 'logins/main.html')

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            print("인증성공")
        else:
            print("인증실패")
    return render(request, 'logins/login.html')

def signup(request):
    if request.method == "POST":
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main.html')
    else:
        form = forms.SignUpForm()
    return render(request, 'logins/signup.html', {'form' : form})