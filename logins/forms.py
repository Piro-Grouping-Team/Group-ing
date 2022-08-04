from dataclasses import field
from django import forms
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        print(model)
        # fields = '__all__'
        fields = ('username', 'password1', 'password2', 'email')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields["username"].help_text = "기호, 영어 소문자, 숫자를 혼합하여 8자리 이상"
        
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", }
        )
        self.fields["password1"].help_text = "기호, 영어 소문자, 숫자를 혼합하여 8자리 이상"

        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", }
        )
        self.fields["password2"].help_text = "확인을 위해 이전과 동일한 비밀번호"


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
