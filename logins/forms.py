from django import forms
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm

# class LoginForm(forms.Form):
#     username = forms.CharField(
#         min_length=5,
#         max_length=20,
#         label='아이디',
#         widget=forms.TextInput,
#         error_messages={
#             'required': '아이디를 입력해주세요.'
#         },
#     )
#     password = forms.CharField(
#         min_length=8,
#         max_length=16,
#         label='비밀번호',
#         widget=forms.PasswordInput,
#         error_messages={
#             'required': '비밀번호를 입력해주세요.'
#         },
#     )

#     def clean(self):
#         cleaned_data = super().clean()
#         username = cleaned_data.get('username')
#         password = cleaned_data.get('password')

#         if username and password:
#             try:
#                 user = User.objects.get(username=username)
#             except User.DoesNotExist:
#                 self.add_error('username', '아이디가 존재하지 않습니다.')
#                 return
            
#             if not user.is_active:
#                 self.add_error('username', '이메일인증을 하지 않았습니다.')

#             elif not check_password(password, user.password):
#                 self.add_error('password', '비밀번호가 틀렸습니다.')



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
            'username', 
            'password1', 
            'password2', 
            'name',
            'nickname',
            'age',
            'phoneNumber',
            'email',
            'profileImg',
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

# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = get_user_model()
#         fields = (
#             'nickname', 
#             'email', 
#             'age', 
#             'address',
#             'addressDetail',
#             'profileImg',
#             'gender',
#             'intro',
#             )

class UpdateUser(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'nickname', 
            'email', 
            'age', 
            'address',
            'addressDetail',
            'profileImg',
            'gender',
            'intro',
            )

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = '기존 비밀번호'
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': False,
        })
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].help_text = "8~16자 영문 대 소문자, 숫자, 특수문자를 사용하세요"
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
        })
    
    def clean_new_password1(self):
        old_password = self.cleaned_data.get('old_password')
        new_password1 = self.cleaned_data.get('new_password1')

        if old_password and new_password1:
            if old_password == new_password1:
                raise forms.ValidationError('새로운 비밀번호는 기존 비밀번호와 다르게 입력해주세요.')
        return new_password1


class FindIdForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput,
    )
    email = forms.EmailField(
        widget=forms.EmailInput,
    )

    class Meta:
        field = ('name', 'email')
    
    def __init__(self, *args, **kwargs):
        super(FindIdForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = '이름'
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'id' : 'id_form_name',
        })
        self.fields['email'].label = '이메일'
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'id' : 'id_form_email',
        })

class FindPwForm(forms.Form):
    username = forms.CharField(
        min_length=5,
        max_length=20,
        widget=forms.TextInput,
    )
    name = forms.CharField(
        widget=forms.TextInput,
    )
    email = forms.EmailField(
        widget=forms.EmailInput,
    )
    class Meta:
        field = ('username', 'name', 'email')
    
    def __init__(self, *args, **kwargs):
        super(FindPwForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = '아이디'
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'id' : 'pw_form_id',
        })

        self.fields['name'].label = '이름'
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'id' : 'pw_form_name',
        })

        self.fields['email'].label = '이메일'
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'id' : 'pw_form_email',
        })

class CustomSetPasswordForm(SetPasswordForm):

    class Meta:
        field = ('new_password1', 'new_password2')
    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].widget.attrs.update({
            'class': 'forms-control',
        })

        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({
            'class': 'forms-control',
        })
