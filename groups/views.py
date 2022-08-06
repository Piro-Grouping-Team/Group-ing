from django.shortcuts import redirect, render
from django.contrib import messages
from groups.forms import GroupForm
from .models import Group
from logins.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def main(request):
    currentUser= request.user.id
    groups = Group.objects.filter(members=currentUser)
    context = {
        'groups' : groups
    }
    return render(request, 'groups/main.html', context=context)

def create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.head = request.user.username
            group.code = request.user.username
            group.save()
            group.members.add(request.user.id)
            return redirect(f'/groups/group/{group.id}')
        else:
            form = GroupForm()
            context = {
            'form' : form
            }
            return render(request, template_name='groups/create.html', context=context)
    else:
        form = GroupForm()
        context = {
            'form' : form
        }
        return render(request, template_name='groups/create.html', context=context)

def join(request):
    if request.method == 'POST':
        code = request.POST['code']
        user = request.user.id

        # 케이스별로 예외처리 논의 필요
        try:    
            group = Group.objects.get(code=code)
        except Group.DoesNotExist:
            messages.error(request, '유효하지 않은 그룹 코드입니다.')
            return redirect('/groups/join/')
        
        try:
            group.blackList.get(id=user)
            messages.error(request, '그룹의 블랙리스트에 등록되어있습니다.')
            return redirect('/groups/join/')
        except:
            try: 
                group.members.get(id=user)
                messages.error(request, '이미 해당 그룹의 멤버입니다.')
                return redirect('/groups/join/')
            except:
                group.members.add(user)
                return redirect(f'/groups/group/{group.id}')  
    else:
        return render(request, template_name='groups/join.html')

def detail(request, id):
    group = Group.objects.get(id = id)
    user = request.user
    members = group.members.all()
    context = {
        'group' : group,
        'members' : members,
        'user' : user
    }
    return render(request, template_name='groups/detail.html', context=context)

def leave(request, id):
    if request.method == 'POST':
        user = request.user.id
        group = Group.objects.get(id=id)
        group.members.remove(user)
    
    return redirect('/groups/')

def modify(request, id):
    group = Group.objects.get(id=id)
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group.name = form.cleaned_data['name']
            group.introduction = form.cleaned_data['introduction']
            group.purpose = form.cleaned_data['purpose']
            group.image = form.cleaned_data['image']
            group.save()
            return redirect(f'/groups/group/{group.id}')
    else:
        form = GroupForm(instance=group)
        context = {
            'form' : form,
            'group' : group
        }
        return render(request, template_name='groups/modify.html', context=context)