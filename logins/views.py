import json
import bcrypt
from . import forms
from .tokens                import account_activation_token
from .models import User
from .text import message
# from my_settings            import SECRET_KEY, EMAIL
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage

from django.views                    import View
from django.http                     import HttpResponse, JsonResponse
from django.core.exceptions          import ValidationError
from django.core.validators          import validate_email
from django.contrib.sites.shortcuts  import get_current_site
from django.utils.http               import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail                import EmailMessage
from django.utils.encoding           import force_bytes, force_str

email = EmailMessage(
    'Hello',                # 제목
    'Body goes here',       # 내용
    to=['xb253q@gmail.com']
)
email.send()

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

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            validate_email(data["email"])

            if User.objects.filter(email=data["email"]).exists():
                return JsonResponse({"message" : "EXISTS_EMAIL"}, status=400)

            user = User.objects.create(
                email     = data["email"],
                password  = bcrypt.hashpw(data["password"].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8"),
                is_active = False 
            )

            current_site = get_current_site(request) 
            domain       = current_site.domain
            uidb64       = urlsafe_base64_encode(force_bytes(user.pk))
            token        = account_activation_token.make_token(user)
            message_data = message(domain, uidb64, token)

            mail_title = "이메일 인증을 완료해주세요"
            mail_to    = data['email']
            email      = EmailMessage(mail_title, message_data, to=[mail_to])
            email.send()         
 
            return JsonResponse({"message" : "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message" : "INVALID_KEY"}, status=400)
        except TypeError:
            return JsonResponse({"message" : "INVALID_TYPE"}, status=400)
        except ValidationError:
            return JsonResponse({"message" : "VALIDATION_ERROR"}, status=400)

# def signup_view(request):
#     if request.method == "POST":
#         form = forms.SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             user = User.objects.create_user(
#                 username=request.POST["username"],
#                 password=request.POST["password1"])
#             user.save()
#             current_site = get_current_site(request) 
#             message = render_to_string('logins/user_activate_email.html',                         {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
#                 'token': account_activation_token.make_token(user),
#             })
#             mail_subject = "회원가입 인증 메일입니다."
#             user_email = user.email
#             email = EmailMessage(mail_subject, message, to=[user_email])
#             email.send()
#             return HttpResponse(
#                 '<div style="font-size: 40px; width: 100%; height:100%; display:flex; text-align:center; '
#                 'justify-content: center; align-items: center;">'
#                 '입력하신 이메일<span>로 인증 링크가 전송되었습니다.</span>'
#                 '</div>'
#             )
#             # login(request, user)
#         return redirect('logins:main')
#     else:
#         form = forms.SignUpForm()

#     return render(request, 'logins/signup.html', {'form' : form})
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
            login(request, user)
        return redirect('logins:main')
    else:
        form = forms.SignUpForm()
    return render(request, 'logins/signup.html', {'form' : form})

# def activate(request, uid64, token):

#     uid = force_str(urlsafe_base64_decode(uid64))
#     user = User.objects.get(pk=uid)

#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         auth.login(request, user)
#         return redirect('account:home')
#     else:
#         return HttpResponse('비정상적인 접근입니다.')