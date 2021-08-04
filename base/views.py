from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm, CreateUserForm
from .filters import TaskFilter

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method=="POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account created successfully for'+username)
                return redirect('login')

        context = {'form':form}
        return render(request, 'base/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method=="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Username or Password is incorrect')
        context={}
        return render(request, 'base/login.html', context)
    
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    tasks = Task.objects.filter(user=request.user)
    myFilter = TaskFilter(request.GET, queryset=tasks)
    tasks = myFilter.qs

    context = {'tasks':tasks, 'myFilter':myFilter}
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def createTask(request):
    form = TaskForm()
    form.instance.user = request.user
    if request.method=="POST":
        
        form = TaskForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'base/taskForm.html', context)

@login_required(login_url='login')
def updateTask(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method=="POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid:
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'base/taskForm.html', context)

@login_required(login_url='login')
def deleteTask(request, pk):
    task = Task.objects.get(id=pk)
    if request.method=="POST":
        task.delete()
        return redirect('/')

    context = {'task':task}
    return render(request, 'base/delete.html', context)

