from .                               import forms
from .tokens                         import account_activation_token
from .models                         import User

from django.shortcuts                import render, redirect
from django.contrib.auth             import authenticate, login, logout
from django.core.mail                import EmailMessage
from django.views                    import View
from django.http                     import HttpResponse
from django.contrib.sites.shortcuts  import get_current_site
from django.utils.http               import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding           import force_bytes, force_str
from django.template.loader          import render_to_string


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

class SignUp(View):
    def get(self, request):
        form = forms.SignUpForm()
        return render(request, 'logins/signup.html', {"form":form})
    
    def post(self, request):
        form = forms.SignUpForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
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
        nickname = request.POST['nickname']
        email = request.POST['email']
        age = request.POST['age']
        address = request.POST['address']
        addressDetail = request.POST['addressDetail']
        gender = request.POST['gender']

        User.objects.filter(id=id).update(nickname=nickname, email=email, age=age, address=address, addressDetail=addressDetail, gender=gender)
        print(User.objects.filter(id=id).update(nickname=nickname, email=email, age=age, address=address, addressDetail=addressDetail, gender=gender))
        return redirect('logins:main')
    else:
        genders = ['남성', '여성', '선택안함']
        user = User.objects.get(id=id)
        context={'user':user, 'genders':genders}
        return render(request, template_name='logins/update.html', context=context)

def mypage(request):
    return render(request, 'logins/mypage.html')

# class SignUp(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response((serializer.data), status=status.HTTP_200_OK)
#         return Response((serializer.errors), status=status.HTTP_200_OK)

# class UserActivate(APIView):
#     # permission_classes = (permission.AllowAny, )

#     def get(self, request, uidb64, token):
#         try:
#             uid = force_str(urlsafe_base64_decode(uidb64.encode('utf-8')))
#             user = User.objects.get(pk=uid)
#         except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None
        
#         try:
#             if user is not None and account_activation_token.check_token(user, token):
#                 user.is_active=True
#                 user.save()
#                 return Response(user.email + '계정이 활성화 되었습니다.', status=status.HTTP_200_OK)
#             else:
#                 return Response('만료된 링크입니다.', status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             print(traceback.format_exc())

# class SignUp(APIView):
#     def post(self, request):
#         if request.method == "POST":
#             form = forms.SignUpForm(request.Post)
#             if form.is_valid():
#                 form.save()
#                 username = form.cleaned_data_get('username')
#                 raw_password = form.cleaned_data('password1')
#                 user = authenticate(username = username, password=raw_password)
#                 serializer = UserSerializer(data=request.data)
#                 if serializer.is_valid():
#                     serializer.save()
#                     return Response((serializer.data), status=status.HTTP_200_OK)
#             return redirect('logins/main.html')
#         else:
#             form = forms.SignUpForm()
#             return render(request, 'logins/signup.html', {'form': form})



# class SignUp(View):
    
#     def post(self, request):#입력값을 받는다
#         data = json.loads(request.body)
#         User(
#             name = data['name'],
#             email = data['email'],
#             password = data['password']
#         ).save()
#         return JsonResponse({'message': 'SUCCESS'}, status=200)
        # data = json.loads(request.body)# 입력값을 코드를 짜기 편하게 값을 받고
        # try:
        #     if re.search("[^a-zA-Z0-9]{6,12}$",data['user']):
        #         return JsonResponse({'message':'id check'}, status=400)
        #     elif re.search(r"[^A-Za-z0-9!@#$]{6,12}$",data['password']):
        #         return JsonResponse({'message':'password check'}, status=400)
        #     else:
        #         try: # 만약 로그인정보가 틀려 오류가 날때 를 대비하여 try, except 문으로 작성한다
        #             User.objects.get(user=data['user'])
        #             return JsonResponse({'message':'EXISTS ID'}, status=401)
        #         except User.DoesNotExist:
        #             user = User.objects.create(
        #                 user    = data['user'],
        #                 email = data['email'],
        #                 password  = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt()).decode('utf-8'),
        #                 is_active = False
        #             )
                    
        #             current_site = get_current_site(request)
        #             domain = current_site.domain
        #             uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        #             token = account_activation_token.make_token(user)
        #             message_data = message(domain, uidb64, token)

        #             mail_title = "이메일 인증을 완료해주세요"
        #             mail_to = data['email']
        #             email = EmailMessage(mail_title, message_data, to=[mail_to])
        #             email.send()

        #         return JsonResponse({'message':'SUCCESS'}, status=200)

        # except KeyError:
        #     return JsonResponse({'message':'key wrong'}, status=402)
        # except TypeError:
        #     return JsonResponse({'message':'type wrong'}, status=403)
        # except ValidationError:
        #     return JsonResponse({'message':'VALIDATION_ERROR'}, status=404)

    # def get(self, request):
    #     user_data = User.objects.values()
    #     return JsonResponse({'users':list(user_data)}, status=200)

# class Activate(View):
#     def get(self, request, uidb64, token):
#         try:
#             uid = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#             user_dic = jwt.decode(token,SECRET_KEY,algorithm='HS256')
#             if user.id == user_dic["user"]:
#                 user.is_active = True
#                 user.save()
#                 return redirect("http://10.58.5.40:3000/signin")

#             return JsonResponse({'message':'auth fail'}, status=400)
#         except ValidationError:
#             return JsonResponse({'message':'type_error'}, status=400)
#         except KeyError:
#             return JsonResponse({'message':'INVALID_KEY'}, status=400)
# class SignUpView(View):
#     def post(self, request):
#         data = json.loads(request.body)
#         try:
#             validate_email(data["email"])

#             if User.objects.filter(email=data["email"]).exists():
#                 return JsonResponse({"message" : "EXISTS_EMAIL"}, status=400)

#             user = User.objects.create(
#                 email     = data["email"],
#                 password  = bcrypt.hashpw(data["password"].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8"),
#                 is_active = False 
#             )

#             current_site = get_current_site(request) 
#             domain       = current_site.domain
#             uidb64       = urlsafe_base64_encode(force_bytes(user.pk))
#             token        = account_activation_token.make_token(user)
#             message_data = message(domain, uidb64, token)

#             mail_title = "이메일 인증을 완료해주세요"
#             mail_to    = data['email']
#             email      = EmailMessage(mail_title, message_data, to=[mail_to])
#             email.send()         
 
#             return JsonResponse({"message" : "SUCCESS"}, status=200)

#         except KeyError:
#             return JsonResponse({"message" : "INVALID_KEY"}, status=400)
#         except TypeError:
#             return JsonResponse({"message" : "INVALID_TYPE"}, status=400)
#         except ValidationError:
#             return JsonResponse({"message" : "VALIDATION_ERROR"}, status=400)

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
# def signup_view(request):
#     if request.method == "POST":
#         print(request.POST)
#         form = forms.SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             print(form)
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#         return redirect('logins:main')
#     else:
#         form = forms.SignUpForm()
#     return render(request, 'logins/signup.html', {'form' : form})

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