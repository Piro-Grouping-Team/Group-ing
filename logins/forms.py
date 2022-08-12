# from dataclasses import field
from django import forms
from .models import User
# from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        min_length=5,
        max_length=20,
        label='아이디',
    )
    password1 = forms.CharField(
        min_length=8,
        max_length=16,
        label='비밀번호',
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        min_length=8,
        max_length=16,
        label='비밀번호 확인',
        widget=forms.PasswordInput,
    )
    class Meta:
        model = User
        fields = (
            'name',
            'nickname',
            'age',
            'username', 
            'password1', 
            'password2', 
            'email',
            'address',
            'addressDetail',
            'gender',
            )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        ###self.fields['username'].help_text = '5~20자 길이'

        ###self.fields['password1'].help_text = "8~16자 영문 대 소문자, 숫자, 특수문자를 사용하세요"
        
        ##이름
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "이름"}
        )
        ##닉네임
        self.fields["nickname"].widget.attrs.update(
            {"class": "form-control", "placeholder": "닉네임"}
        )
        
        ##나이
        self.fields["age"].widget.attrs.update(
            {"class": "form-control", "placeholder": "나이"}
        )

        ##아이디
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "아이디"}
        )

        ##이메일
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "example@example.com"}
        )

        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "비밀번호"}
        )

        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "비밀번호 확인"}
        )
        ###self.fields["password2"].help_text = "확인을 위해 이전과 동일한 비밀번호"

        self.fields["address"].widget.attrs.update(
            {"id": "address_kakao", "name" : "address", "placeholder": "주소"}
        )

        self.fields["addressDetail"].widget.attrs.update(
            {"name": "address_detail", "placeholder": "상세주소"}
        )

# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

#     def clean(self):
#         username = self.cleaned_data.get("username")
#         password = self.cleaned_data.get("password")

#         try:
#             user = User.objects.get(username=username)
#             if user.check_password(password):
#                 return self.cleaned_data
#             else:
#                 raise forms.ValidationError("비밀번호가 일치하지 않습니다!")
#         except User.DoesNotExist:
#             raise forms.ValidationError("해당 사용자가 존재하지 않습니다!")
