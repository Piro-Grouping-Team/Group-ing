from .                               import forms
from .tokens                         import account_activation_token
from .models                         import User

from django.shortcuts                import render, redirect
from django.contrib                  import messages
from django.contrib.auth             import authenticate, login, logout
from django.core.mail                import EmailMessage
from django.views                    import View
from django.http                     import HttpResponse
from django.contrib.sites.shortcuts  import get_current_site
from django.utils.http               import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding           import force_bytes, force_str
from django.template.loader          import render_to_string
from django.contrib.auth             import update_session_auth_hash
from django.contrib.auth.decorators  import login_required

# Create your views here.
def main(request):
    context = {'state' : False}
    return render(request, 'logins/main.html', context=context)

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if User.objects.filter(username = username).exists():
            if User.objects.get(username = username).is_active:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                else:
                    messages.info(request, '아이디, 비밀번호를 잘못 입력')
            else:
                messages.info(request, '이메일인증이 되지않았습니다.')
        else:
            messages.info(request, '아이디, 비밀번호를 잘못 입력')
    return render(request, 'logins/login.html')

def logout_view(request):
    logout(request)
    return redirect('logins:login')

class SignUp(View):
    def get(self, request):
        form = forms.SignUpForm()
        return render(request, 'logins/signup.html', {"form":form})
    
    def post(self, request):
        form = forms.SignUpForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('logins/account_email.html',                         {
                'user': user,
                'domain': current_site.domain,
                'id': urlsafe_base64_encode(force_bytes(user.id)).encode().decode(),
                'token': account_activation_token.make_token(user),
            })
            
            mail_subject = 'Activate your accout'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return redirect('logins:main')
        print(form.error_messages)

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(user)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('logins:login')
    else:
        return HttpResponse('Activation link is invalid')

def userUpdate(request, id):
    if request.method == 'POST':
        email = request.POST['email']
        age = request.POST['age']
        address = request.POST['address']
        addressDetail = request.POST['addressDetail']
        gender = request.POST['gender']
        profileImg = request.POST['profileImg']

        User.objects.filter(id=id).update(email=email, age=age, address=address, addressDetail=addressDetail, gender=gender, profileImg=profileImg)
        return redirect('/')
    else:
        genders = ['남성', '여성', '선택안함']
        user = User.objects.get(id=id)
        context={'user':user, 'genders':genders}
        return render(request, template_name='logins/update.html', context=context)

def findUsername(request):
    errorMessage=''
    context = {'errorMessage' : errorMessage}
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        if User.objects.filter(name = name, email = email).exists():
            user = User.objects.get(name=name, email=email)
            current_site = get_current_site(request)
            message = render_to_string('logins/findUsername_email.html', {
                'user': user,
                'domain': current_site.domain,
            })
            mail_subject = 'Find your Username'
            to_email = user.email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return redirect('logins:main')

        else:
            errorMessage='일치하는 정보가 없습니다.'
            return render(request, template_name='logins/findUsername.html', context=context)
    return render(request, template_name='logins/findUsername.html', context=context)

def findPW(request):
    errorMessage=''
    context = {'errorMessage' : errorMessage}
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        if User.objects.filter(username=username, name = name, email = email).exists():
            user = User.objects.get(username=username, name=name, email=email)
            current_site = get_current_site(request)
            print(urlsafe_base64_encode(force_bytes(user.id)).encode().decode())
            print(account_activation_token.make_token(user))
            message = render_to_string('logins/findPW_email.html', {
                'user': user,
                'domain': current_site.domain,
                'id': urlsafe_base64_encode(force_bytes(user.id)).encode().decode(),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Find your PW'
            to_email = user.email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return redirect('logins:login')

        else:
            errorMessage='일치하는 정보가 없습니다.'
            return render(request, template_name='logins/findPW.html', context=context)
    return render(request, template_name='logins/findPW.html', context=context)

def changePW(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = forms.CustomPasswordChangeForm(user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, '비밀번호가 성공적으로 변경되었습니다!')
                return redirect('/')
            else:
                messages.error(request, '오류를 수정해주세요')
        else:
            form = forms.CustomPasswordChangeForm(request.user)
            print(form)
        return render(request, 'logins/changePW.html', {'form': form})
