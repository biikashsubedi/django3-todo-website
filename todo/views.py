from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def index(requests):
    return render(requests, 'index.html')

def signupuser(requests):
    if requests.method =='GET':
        return render(requests, 'signup.html', {'signup':UserCreationForm()})
    else:
        # Create new user
        if requests.POST['password1']==requests.POST['password2']:
            try:
                user = User.objects.create_user(requests.POST['username'], password=requests.POST['password1'])
                user.save()
                login(requests, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(requests, 'signup.html', {'signup': UserCreationForm(), 'error_msg': 'Username already taken, please choose another'})
        else:
            #Tell user password doesn't match
            return render(requests, 'signup.html', {'signup':UserCreationForm(), 'error_msg':'Password did not match'})

def loginuser(requests):
    if requests.method == "GET":
        return render(requests, 'login.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(requests, username=requests.POST['username'], password=requests.POST['password'])
        if user is None:
            return render(requests, 'login.html', {'form':AuthenticationForm(), 'error_msg': 'Username and Password did not matched'})
        else:
            login(requests, user)
            return redirect('currenttodos')

@login_required
def currenttodos(requests):
    todos = Todo.objects.filter(user=requests.user, datecompleted__isnull=True)
    return render(requests, 'todo/currenttodos.html', {'todos':todos})

@login_required
def completedtodos(requests):
    todos = Todo.objects.filter(user=requests.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(requests, 'todo/completedtodos.html', {'todos':todos})

@login_required
def createtodo(requests):
    if requests.method == 'GET':
        return render(requests, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(requests.POST)
            newtodo = form.save(commit=False)
            newtodo.user = requests.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(requests, 'todo/createtodo.html', {'form': TodoForm(), 'error_msg':'Bad data Entry'})

@login_required
def logoutuser(requests):
    if requests.method=='POST':
        logout(requests)
        return redirect('index')

@login_required
def viewtodo(requests, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=requests.user)
    if requests.method == 'GET':
        form = TodoForm(instance=todo)
        return render(requests, 'todo/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(requests.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(requests, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error_msg':'Data Entry Error'})

@login_required
def completetodo(requests, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=requests.user)
    if requests.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(requests, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=requests.user)
    if requests.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.delete()
        return redirect('currenttodos')