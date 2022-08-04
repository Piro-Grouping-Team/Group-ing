from django.shortcuts import redirect, render

from groups.forms import GroupForm
from .models import Group
from logins.models import User

# Create your views here.
def main(request):
    group = Group.objects.first()
    print(group)
    return render(request, 'groups/main.html')

def create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.head = request.user.username
            group.code = request.user.username
            group.save()
            group.member.add(request.user.id)
        return redirect('/groups/')
    else:
        form = GroupForm()
        context = {
            'form' : form
        }
        return render(request, template_name='groups/create.html', context=context)

def join(requsest):
    pass

def detail(request, id):
    pass