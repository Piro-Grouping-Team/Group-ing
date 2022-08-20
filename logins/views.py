import json


from .                               import forms
from .tokens                         import account_activation_token
from .models                         import User
from .helper                         import email_auth_num

from django.shortcuts                import render, redirect
from django.contrib                  import messages
from django.contrib.auth             import authenticate, login, logout
from django.core.mail                import EmailMessage
from django.conf                     import settings
from django.views                    import View
from django.views.generic            import FormView
from django.http                     import HttpResponse, JsonResponse
from django.contrib.sites.shortcuts  import get_current_site
from django.utils.http               import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding           import force_bytes, force_str
from django.template.loader          import render_to_string
from django.contrib.auth             import update_session_auth_hash
from django.core.exceptions          import PermissionDenied

# Create your views here.
def main(request):
    return render(request, 'main.html')

# class LoginView(FormView):
#     template_name = 'logins/login.html'
#     form_class = forms.LoginForm
#     success_url = '/'

#     def form_valid(self, form):
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")

#         user = authenticate(self.request, username=username, password=password)
#         if user is not None:
#             self.request.session['username'] = username
#             login(self.request, user)

#             # Session Maintain Test

#             remember_session = self.request.POST.get('remember_session', False)
#             if remember_session:
#                 settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False

#             # try:
#             #     remember_session = self.request.POST['remember_session']
#             #     if remember_session:
#             #         settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
#             # except MultiValueDictKeyError:
#             #     settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
            
#         return super().form_valid(form)

def login_view(request):
    error_messages=''
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
                    error_messages='아이디, 비밀번호를 잘못 입력하였습니다.'
            else:
                error_messages='이메일인증이 되지않았습니다.'
        else:
            error_messages='아이디, 비밀번호를 잘못 입력하였습니다.'
    context = {'error_messages': error_messages}
    return render(request, 'logins/login.html', context=context)

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
            
            mail_subject = '[Group-ing] 회원가입 인증메일입니다.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return redirect('/')
        print(form.errors)

def usernameCheck(request):
    req = json.loads(request.body)
    username = req['username']
    print(username)
    if User.objects.filter(username=username).exists():
        duplicate = 'fail'
    else:
        duplicate = 'pass'
    return JsonResponse({'result': duplicate})

def emailCheck(request):
    req = json.loads(request.body)
    email = req['email']
    if User.objects.filter(email=email).exists():
        duplicate = 'fail'
    else:
        duplicate = 'pass'
    return JsonResponse({'result': duplicate})

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

# def userUpdate(request, id):
#     if request.method == 'POST':
#         nickname = request.POST['nickname']
#         email = request.POST['email']
#         age = request.POST['age']
#         phoneNumber = request.POST['phoneNumber']
#         address = request.POST['address']
#         addressDetail = request.POST['addressDetail']
#         gender = request.POST['gender']
#         profileImg = request.FILES['profileImg']
#         intro = request.POST['intro']

#         User.objects.filter(id=id).update(nickname=nickname, email=email, age=age, profileImg=profileImg, address=address, addressDetail=addressDetail, gender=gender, intro=intro)
#         return redirect('logins:mypage')
#     else:
#         userChangeForm = forms.UpdateUser(instance=request.user)
#         genders = ['남성', '여성', '선택안함']
#         context={'userChangeForm':userChangeForm, 'genders':genders}
#         return render(request, template_name='logins/update.html', context=context)

def userUpdate(request, id):
    if request.method == 'POST':
        userChangeForm = forms.UpdateUser(request.POST, request.FILES, instance=request.user)
        if userChangeForm.is_valid():
            userChangeForm.save()
            messages.success(request, '회원정보가 수정되었습니다.')
            return redirect('logins:mypage')
        print(userChangeForm.errors)
    else:
        userChangeForm = forms.UpdateUser(instance=request.user)
        genders = ['남성', '여성', '선택안함']
        context={'userChangeForm':userChangeForm, 'genders':genders}
        return render(request, template_name='logins/update.html', context=context)

def mypage(request):
    return render(request, 'logins/mypage.html')

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

def changePW(request, id):
    try:
        user = User.objects.get(pk=id)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user:
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
        return render(request, 'logins/changePW.html', {'form': form})