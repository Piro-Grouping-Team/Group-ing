from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .forms import SignUpForm
from django.shortcuts                import render, redirect

from allauth.socialaccount.models import SocialLogin

class SocialAccountAdpater(DefaultSocialAccountAdapter):

    # def save_user(self, request, sociallogin, form=None):
    #     print(sociallogin.token)
    #     return super(SocialAccountAdpater, self).save_user(request, sociallogin, form)
    def save_user(self, request, sociallogin, form=None):
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            print(form)
            if form.is_valid():
                user = super(SocialAccountAdpater, self).save_user(request, sociallogin, form)
                user.is_active=True
                user.save()
                print(user)
                return redirect('logins:main')

        form = SignUpForm()
        print('바보')
        return render(request, 'logins/signup.html', {"form":form})
        return super().save_user(request, sociallogin, form)