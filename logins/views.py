import json
import random

from .                               import forms
from .tokens                         import account_activation_token
from .models                         import User
from .helper                         import email_auth_num

from django.shortcuts                import render, redirect
from django.contrib                  import messages
from django.contrib.auth             import authenticate, login, logout
from django.core.mail                import EmailMessage
from django.views                    import View
from django.http                     import HttpResponse, JsonResponse
from django.contrib.sites.shortcuts  import get_current_site
from django.utils.http               import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding           import force_bytes, force_str
from django.template.loader          import render_to_string
from django.utils.decorators         import method_decorator
from django.contrib.auth             import update_session_auth_hash
from django.core.exceptions          import PermissionDenied
from django.core.serializers.json    import DjangoJSONEncoder

# Create your views here.
def main(request):
    return render(request, 'main.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if User.objects.filter(username = username).exists():
            if User.objects.get(username = username).is_active:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')
                else:
                    messages.info(request, '아이디, 비밀번호를 잘못 입력')
            else:
                messages.info(request, '이메일인증이 되지않았습니다.')
        else:
            messages.info(request, '아이디, 비밀번호를 잘못 입력')
    return render(request, 'logins/login.html')


def logout_view(request):
    logout(request)
    return redirect('/')

class SignUp(View):
    def get(self, request):
        form = forms.SignUpForm()
        return render(request, 'logins/signup.html', {"form":form})
    
    def post(self, request):
        form = forms.SignUpForm(request.POST, request.FILES)
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
            return redirect('/')
        print(form.error_messages)

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/')
    else:
        return HttpResponse('Activation link is invalid')

def userUpdate(request, id):
    if request.method == 'POST':
        nickname = request.POST['nickname']
        email = request.POST['email']
        age = request.POST['age']
        # phoneNumber = request.POST['phoneNumber']
        address = request.POST['address']
        addressDetail = request.POST['addressDetail']
        gender = request.POST['gender']
        # profileImg = request.POST['profileImg']
        intro = request.POST['intro']

        User.objects.filter(id=id).update(nickname=nickname, email=email, age=age, address=address, addressDetail=addressDetail, gender=gender, intro=intro)
        return redirect('logins:mypage')
    else:
        genders = ['남성', '여성', '선택안함']
        user = User.objects.get(id=id)
        context={'user':user, 'genders':genders}
        return render(request, template_name='logins/update.html', context=context)

def mypage(request):
    return render(request, 'logins/mypage.html')

def findUsername(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        if User.objects.filter(name = name, email = email).exists():
            user = User.objects.get(name=name, email=email)
            randomNumber = random.randint(100000, 999999)
            message = render_to_string('logins/findUsername_email.html', {
                'user': user,
                'randomNumber': randomNumber,
            })
            mail_subject = 'Find your Username'
            to_email = user.email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return redirect('/')

        else:
            messages.info(request, '일치하는 정보가 없습니다.')
    return render(request, template_name='logins/findUsername.html')

# @method_decorator(logout_message_required, name='dispatch')
class FindIdView(View):
    template_name = 'logins/findId.html'
    findId = forms.FindIdForm

    def get(self, request):
        if request.method == 'GET':
            form = self.findId(None)
            return render(request, self.template_name, {'form': form, })

def axiosFindIdView(request):
    req = json.loads(request.body)
    name = req['name']
    email = req['email']
    user = User.objects.get(name=name, email=email)

    if user:
        authNum = email_auth_num()
        user.auth = authNum
        user.save()
        message = render_to_string('logins/findId_email.html', {
            'name': name,
            'authNum':authNum,
        })
        mail_subject = '[Group-ing] 아이디 찾기 인증메일입니다.'
        to_email = user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
    print(user.username)
    return JsonResponse({'result': user.email})

def showId(request):
    sessionUser = request.session['auth']
    currentUser = User.objects.get(email=sessionUser)
    username = currentUser.username
    context = {'username': username}
    return render(request, 'logins/showId.html', context=context)


# @method_decorator(decorators.logout_message_required, name='dispatch')
class FindPwView(View):
    template_name = 'logins/findPw.html'
    findPw = forms.FindPwForm

    def get(self, request):
        if request.method == 'GET':
            form = self.findPw(None)
            return render(request, self.template_name, {'form': form, })

def axiosFindPwView(request):
    req = json.loads(request.body)
    username = req['username']
    name = req['name']
    email = req['email']
    user = User.objects.get(username=username, name=name, email=email)

    if user:
        authNum = email_auth_num()
        user.auth = authNum
        user.save()
        message = render_to_string('logins/findPw_email.html', {
            'username': username,
            'authNum':authNum,
        })
        mail_subject = '[Group-ing] 비밀번호 찾기 인증메일입니다.'
        to_email = user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
    return JsonResponse({'result': user.email})

def authConfirmView(request):
    req = json.loads(request.body)
    email = req['email']
    inputAuthNum = req['inputAuthNum']

    user = User.objects.get(email=email, auth=inputAuthNum)
    user.auth = ''
    user.save()
    request.session['auth'] = user.email

    return JsonResponse({'result': user.email, 'username': user.username})

def authPwResetView(request):
    if request.method == 'GET':
        if not request.session.get('auth', False):
            raise PermissionDenied

    if request.method == 'POST':
        sessionUser = request.session['auth']
        currentUser = User.objects.get(email=sessionUser)
        login(request, currentUser, backend='django.contrib.auth.backends.ModelBackend')
        resetPwForm = forms.CustomSetPasswordForm(request.user, request.POST)
        if resetPwForm.is_valid():
            currentUser = resetPwForm.save()
            messages.success(request, '비밀번호 변경완료! 변경된 비밀번호로 로그인하세요.')
            logout(request)
            return redirect('logins:login')
        else:
            logout(request)
            request.session['auth'] = sessionUser
    else:
        resetPwForm = forms.CustomSetPasswordForm(request.user)
    
    return render(request, 'logins/passwordReset.html', {'form':resetPwForm})

# def findPW(request):
#     errorMessage=''
#     context = {'errorMessage' : errorMessage}
#     if request.method == 'POST':
#         username = request.POST['username']
#         name = request.POST['name']
#         email = request.POST['email']
#         if User.objects.filter(username=username, name = name, email = email).exists():
#             user = User.objects.get(username=username, name=name, email=email)
#             current_site = get_current_site(request)
#             print(urlsafe_base64_encode(force_bytes(user.id)).encode().decode())
#             print(account_activation_token.make_token(user))
#             message = render_to_string('logins/findPW_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'id': urlsafe_base64_encode(force_bytes(user.id)).encode().decode(),
#                 'token': account_activation_token.make_token(user),
#             })
#             mail_subject = 'Find your PW'
#             to_email = user.email
#             email = EmailMessage(mail_subject, message, to=[to_email])
#             email.send()
#             return redirect('logins:login')
#         else:
#             errorMessage='일치하는 정보가 없습니다.'
#             return render(request, template_name='logins/findPW.html', context=context)
#     return render(request, template_name='logins/findPW.html', context=context)

# def changePW(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         if request.method == 'POST':
#             form = forms.CustomPasswordChangeForm(user, request.POST)
#             if form.is_valid():
#                 user = form.save()
#                 update_session_auth_hash(request, user)
#                 messages.success(request, '비밀번호가 성공적으로 변경되었습니다!')
#                 return redirect('/')
#             else:
#                 messages.error(request, '오류를 수정해주세요')
#         else:
#             form = forms.CustomPasswordChangeForm(request.user)
#             print(form)
#         return render(request, 'logins/changePW.html', {'form': form})